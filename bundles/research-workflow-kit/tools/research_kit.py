#!/usr/bin/env python3
"""Inspect, verify, install, and scaffold the portable research workflow kit."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "MANIFEST.json"
PROFILES_DIR = ROOT / "profiles"
TEMPLATE_DIR = ROOT / "project-template"


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"missing required file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid JSON in {path}: {exc}") from exc


def manifest() -> dict:
    data = read_json(MANIFEST_PATH)
    if data.get("formatVersion") != 1 or not isinstance(data.get("skills"), list):
        raise SystemExit("unsupported or malformed MANIFEST.json")
    return data


def profiles() -> dict[str, dict]:
    result = {}
    for path in sorted(PROFILES_DIR.glob("*.json")):
        data = read_json(path)
        result[data["name"]] = data
    return result


def safe_relative(value: str) -> Path:
    pure = PurePosixPath(value)
    if pure.is_absolute() or ".." in pure.parts:
        raise ValueError(f"unsafe relative path: {value}")
    return Path(*pure.parts)


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*"), key=lambda p: p.as_posix()):
        if path.is_symlink():
            raise ValueError(f"symlink is not allowed in portable payload: {path}")
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix().encode("utf-8")
        digest.update(len(rel).to_bytes(8, "big"))
        digest.update(rel)
        size = path.stat().st_size
        digest.update(size.to_bytes(8, "big"))
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    return digest.hexdigest()


def selected_entries(data: dict, profile_name: str | None, ids: list[str]) -> list[dict]:
    index = {entry["id"]: entry for entry in data["skills"]}
    selected_ids: list[str] = []
    if profile_name:
        profile_index = profiles()
        if profile_name not in profile_index:
            raise SystemExit(
                f"unknown profile {profile_name!r}; choose: {', '.join(sorted(profile_index))}"
            )
        selected_ids.extend(profile_index[profile_name]["skillIds"])
    selected_ids.extend(ids)
    if not selected_ids:
        raise SystemExit("select --profile or at least one --id")
    missing = sorted(set(selected_ids) - set(index))
    if missing:
        raise SystemExit("manifest does not contain: " + ", ".join(missing))
    seen = set()
    result = []
    for skill_id in selected_ids:
        if skill_id not in seen:
            seen.add(skill_id)
            result.append(index[skill_id])
    return result


def cmd_doctor(_: argparse.Namespace) -> int:
    data = manifest()
    ps = profiles()
    bundled = sum(bool(item.get("bundled")) for item in data["skills"])
    blocked = len(data["skills"]) - bundled
    missing = []
    for item in data["skills"]:
        if item.get("bundled"):
            package = ROOT / safe_relative(item["payloadPath"])
            entry = package / safe_relative(item["entryRelative"])
            if not package.is_dir() or not entry.is_file():
                missing.append(item["id"])
    print(f"Research Workflow Kit {data.get('version', 'unknown')}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Entries: {len(data['skills'])} ({bundled} payload, {blocked} metadata-only)")
    print("Profiles: " + ", ".join(f"{name}={len(p['skillIds'])}" for name, p in ps.items()))
    if missing:
        print("BROKEN payload entries: " + ", ".join(missing), file=sys.stderr)
        return 1
    print("Quick doctor: PASS")
    print("Run `python3 tools/research_kit.py verify` for hashes and all profile references.")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    data = manifest()
    entries = data["skills"]
    if args.profile:
        entries = selected_entries(data, args.profile, [])
    for item in entries:
        state = "payload" if item.get("bundled") else "metadata-only"
        profiles_text = ",".join(item.get("profiles", [])) or "-"
        print(f"{item['id']}\t{state}\t{profiles_text}\t{item.get('description', '')}")
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    data = manifest()
    terms = [term.casefold() for term in args.query.split() if term.strip()]
    scored = []
    for item in data["skills"]:
        fields = {
            "name": str(item.get("name", "")).casefold(),
            "description": str(item.get("description", "")).casefold(),
            "source": str(item.get("sourceId", "")).casefold(),
            "profiles": " ".join(item.get("profiles", [])).casefold(),
        }
        score = 0
        for term in terms:
            if term in fields["name"]:
                score += 10
            if term in fields["description"]:
                score += 4
            if term in fields["source"]:
                score += 2
            if term in fields["profiles"]:
                score += 1
        if score:
            scored.append((score, item))
    scored.sort(key=lambda pair: (-pair[0], pair[1]["id"]))
    for score, item in scored[: args.limit]:
        state = "payload" if item.get("bundled") else "metadata-only"
        print(f"[{score:02}] {item['id']} ({state})\n     {item.get('description', '')}")
    return 0


def cmd_install(args: argparse.Namespace) -> int:
    data = manifest()
    entries = selected_entries(data, args.profile, args.id)
    blocked = [entry for entry in entries if not entry.get("bundled")]
    if blocked and not args.skip_metadata_only:
        details = ", ".join(f"{x['id']} ({x.get('metadataOnlyReason', 'not bundled')})" for x in blocked)
        raise SystemExit("selection includes metadata-only entries; use --skip-metadata-only: " + details)
    entries = [entry for entry in entries if entry.get("bundled")]
    target = args.target.expanduser().resolve()
    for item in entries:
        source = ROOT / safe_relative(item["payloadPath"])
        destination = target / item["installName"]
        print(f"{item['id']}: {source} -> {destination}")
        if args.dry_run:
            continue
        if destination.exists():
            if not args.force:
                raise SystemExit(f"target exists (use --force): {destination}")
            if destination.is_symlink() or not destination.is_dir():
                destination.unlink()
            else:
                shutil.rmtree(destination)
        target.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, destination)
        provenance = {
            key: item.get(key)
            for key in (
                "id",
                "name",
                "sourceId",
                "sourceRepository",
                "sourceCommit",
                "sourceLicense",
                "sourcePath",
                "packageSha256",
                "compatibility",
            )
        }
        (destination / "RESEARCH_KIT_PROVENANCE.json").write_text(
            json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        license_dir = ROOT / "licenses" / item["sourceId"]
        if license_dir.is_dir():
            shutil.copytree(license_dir, destination / "UPSTREAM_NOTICES", dirs_exist_ok=True)
    if not args.dry_run:
        print(f"Installed {len(entries)} skill package(s) into {target}")
    return 0


def cmd_init_project(args: argparse.Namespace) -> int:
    target = args.path.expanduser().resolve()
    if target.exists() and any(target.iterdir()) and not args.force:
        raise SystemExit(f"target is not empty (use --force to merge/replace template files): {target}")
    print(f"{TEMPLATE_DIR} -> {target}")
    if args.dry_run:
        return 0
    if not TEMPLATE_DIR.is_dir():
        raise SystemExit("project-template is missing")
    target.mkdir(parents=True, exist_ok=True)
    for source in sorted(TEMPLATE_DIR.rglob("*")):
        if not source.is_file():
            continue
        destination = target / source.relative_to(TEMPLATE_DIR)
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists() and not args.force:
            raise SystemExit(f"template target exists (use --force): {destination}")
        shutil.copy2(source, destination)
    print("Project scaffold created. Start with 00-governance/research-charter.md.")
    return 0


def cmd_verify(_: argparse.Namespace) -> int:
    data = manifest()
    ps = profiles()
    errors: list[str] = []
    ids = [item.get("id") for item in data["skills"]]
    if len(ids) != len(set(ids)):
        errors.append("manifest IDs are not unique")
    index = {item["id"]: item for item in data["skills"]}
    for name, profile in ps.items():
        unknown = sorted(set(profile.get("skillIds", [])) - set(index))
        if unknown:
            errors.append(f"profile {name} has unknown IDs: {unknown}")
    checked = 0
    for item in data["skills"]:
        if not item.get("bundled"):
            if not item.get("metadataOnlyReason"):
                errors.append(f"metadata-only entry lacks reason: {item['id']}")
            continue
        try:
            package = ROOT / safe_relative(item["payloadPath"])
            entry = package / safe_relative(item["entryRelative"])
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if not package.is_dir():
            errors.append(f"missing package: {item['id']}")
            continue
        if not entry.is_file():
            errors.append(f"missing SKILL entry: {item['id']}")
            continue
        try:
            actual = tree_hash(package)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if actual != item.get("packageSha256"):
            errors.append(f"hash mismatch: {item['id']}")
        checked += 1
    if not TEMPLATE_DIR.is_dir() or not (TEMPLATE_DIR / "00-governance" / "research-charter.md").is_file():
        errors.append("project template is incomplete")
    if errors:
        print("VERIFY FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"VERIFY PASS: {checked} payload packages, {len(ps)} profiles, {len(ids)} manifest entries")
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    subs = root.add_subparsers(dest="command", required=True)

    doctor = subs.add_parser("doctor", help="quick structure and environment check")
    doctor.set_defaults(func=cmd_doctor)

    listing = subs.add_parser("list", help="list manifest entries")
    listing.add_argument("--profile")
    listing.set_defaults(func=cmd_list)

    search = subs.add_parser("search", help="search local manifest metadata")
    search.add_argument("query")
    search.add_argument("--limit", type=int, default=20)
    search.set_defaults(func=cmd_search)

    install = subs.add_parser("install", help="install a profile or selected skill IDs")
    install.add_argument("--profile")
    install.add_argument("--id", action="append", default=[])
    install.add_argument("--target", type=Path, required=True)
    install.add_argument("--dry-run", action="store_true")
    install.add_argument("--force", action="store_true")
    install.add_argument("--skip-metadata-only", action="store_true")
    install.set_defaults(func=cmd_install)

    init_project = subs.add_parser("init-project", help="copy the research project scaffold")
    init_project.add_argument("path", type=Path)
    init_project.add_argument("--dry-run", action="store_true")
    init_project.add_argument("--force", action="store_true")
    init_project.set_defaults(func=cmd_init_project)

    verify = subs.add_parser("verify", help="verify package hashes and profile references")
    verify.set_defaults(func=cmd_verify)
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        return int(args.func(args))
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
