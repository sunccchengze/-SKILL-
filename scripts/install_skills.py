#!/usr/bin/env python3
"""Copy selected cataloged skill packages into another Agent skill directory."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

from catalog_aliases import annotate_alias, is_alias, load_alias_index

REPO = Path(__file__).resolve().parents[1]
CATALOGS = (
    REPO / "catalog" / "skills.json",
    REPO / "catalog" / "official-skills.json",
    REPO / "catalog" / "research-skills.json",
    REPO / "catalog" / "curated-skills.json",
)
TIER_RANK = {
    "maintained": 0,
    "router": 1,
    "official-source": 2,
    "curated-source": 3,
    "community": 4,
    "tool-bundled": 5,
    "full-source": 6,
    "bundled": 7,
    "variant": 9,
}


def normalize(name: str) -> str:
    name = name.casefold().strip().replace("_", "-")
    return re.sub(r"-+", "-", re.sub(r"\s+", "-", name))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", action="append", required=True, help="exact catalog skill name; repeatable")
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument(
        "--source",
        help="optional collection/source ID when an exact name exists in multiple sources",
    )
    parser.add_argument(
        "--path",
        help="optional exact catalog path for duplicate names within one source",
    )
    parser.add_argument("--force", action="store_true", help="replace an existing target package")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def load_records() -> list[dict[str, object]]:
    if not CATALOGS[0].is_file():
        raise SystemExit("catalog missing; run: python scripts/build_catalog.py")
    records: list[dict[str, object]] = []
    for catalog in CATALOGS:
        if catalog.is_file():
            records.extend(json.loads(catalog.read_text(encoding="utf-8"))["skills"])
    alias_index = load_alias_index()
    return [annotate_alias(record, alias_index) for record in records]


def submodule_path(record: dict[str, object]) -> Path:
    relative = Path(str(record["path"]))
    parts = relative.parts
    if len(parts) >= 3 and parts[:2] in {
        ("full-sources", "official"),
        ("full-sources", "research"),
        ("full-sources", "curated"),
    }:
        return Path(*parts[:3])
    return relative.parent


def source_hint(record: dict[str, object]) -> str:
    source_id = str(record.get("sourceId", record.get("collection", "")))
    submodule = submodule_path(record)
    return (
        f"skill source is not initialized: {source_id}\n"
        f"Run: git submodule update --init {submodule.as_posix()}"
    )


def is_notice_file(path: Path) -> bool:
    name = path.name.casefold()
    return path.is_file() and (
        name in {"license", "notice", "copying"}
        or name.startswith(("license.", "license-", "notice.", "notice-", "copying."))
    )


def copy_ancestor_notices(
    record: dict[str, object], source_package: Path, destination: Path
) -> int:
    """Preserve source/plugin-level legal files omitted by package-only copies."""
    if not record.get("requiresSubmoduleInit"):
        return 0
    source_root = REPO / submodule_path(record)
    current = source_package.parent
    copied = 0
    while current == source_root or source_root in current.parents:
        for notice in sorted(path for path in current.iterdir() if is_notice_file(path)):
            target = destination / "UPSTREAM_NOTICES" / notice.relative_to(source_root)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(notice, target)
            copied += 1
        if current == source_root:
            break
        current = current.parent
    return copied


def main() -> None:
    args = parse_args()
    records = load_records()
    if args.path and len(args.name) != 1:
        raise SystemExit("--path can only be used with one --name")

    selected = []
    for requested in args.name:
        wanted = normalize(requested)
        matches = [
            record
            for record in records
            if record["name"] == wanted and record["tier"] != "variant"
        ]
        if args.source:
            matches = [
                record
                for record in matches
                if args.source in {record.get("sourceId"), record.get("collection")}
            ]
        if args.path:
            matches = [record for record in matches if record.get("path") == args.path]
        if not args.source and not args.path:
            matches = [record for record in matches if not is_alias(record)]
        if not matches:
            filters = ""
            if args.source:
                filters += f" in source {args.source}"
            if args.path:
                filters += f" at path {args.path}"
            raise SystemExit(f"skill not found: {requested}{filters}")
        matches.sort(
            key=lambda record: (
                is_alias(record),
                TIER_RANK.get(str(record["tier"]), 8),
                record.get("sourceStatus") == "upstream-deprecated",
                str(record.get("sourceId", "")),
                str(record["path"]),
            )
        )
        selected.append(matches[0])

    target_root = args.target.expanduser().resolve()
    for record in selected:
        skill_file = REPO / str(record["path"])
        source_package = REPO / str(record.get("sourcePackagePath", skill_file.parent.relative_to(REPO)))
        destination = target_root / normalize(str(record["name"]))
        provenance = str(record.get("sourceId", record.get("collection", record["tier"])))
        license_name = record.get("sourceLicense")
        license_suffix = f", license: {license_name}" if license_name else ""
        status = record.get("sourceStatus")
        status_suffix = f", status: {status}" if status and status != "current" else ""
        alias_reason = record.get("aliasReason")
        alias_suffix = f", alias: {alias_reason}" if alias_reason else ""
        print(
            f"{record['name']} [{provenance}{license_suffix}{status_suffix}{alias_suffix}]: "
            f"{source_package} -> {destination}"
        )
        if args.dry_run:
            continue
        if not skill_file.is_file():
            if record.get("requiresSubmoduleInit"):
                raise SystemExit(source_hint(record))
            raise SystemExit(f"skill package is missing: {skill_file.relative_to(REPO)}")
        target_root.mkdir(parents=True, exist_ok=True)
        if destination.exists():
            if not args.force:
                raise SystemExit(f"target exists (use --force): {destination}")
            shutil.rmtree(destination)
        # The repository router is a single root file; installing it must not
        # copy this entire repository into the target.
        if skill_file == REPO / "SKILL.md":
            destination.mkdir(parents=True)
            shutil.copy2(skill_file, destination / "SKILL.md")
        else:
            shutil.copytree(source_package, destination)
            # A selected skill may intentionally package a repository-level
            # scaffold (for example Bolt Slides). Expose the selected entry at
            # the install root while retaining its original upstream path.
            if source_package / "SKILL.md" != skill_file:
                installed_entry = destination / "SKILL.md"
                if installed_entry.exists():
                    raise SystemExit(
                        f"selected entry would overwrite package SKILL.md: {skill_file}"
                    )
                shutil.copy2(skill_file, installed_entry)
        notice_count = copy_ancestor_notices(record, source_package, destination)
        if notice_count:
            print(f"  preserved {notice_count} ancestor license/notice file(s)")


if __name__ == "__main__":
    main()
