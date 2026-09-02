#!/usr/bin/env python3
"""Build metadata for the explicitly selected curated skill packages.

The catalog records Git blob IDs and pinned source commits without copying
upstream packages into the main repository. A curated source may contain other
SKILL.md files; only lock-declared ``skillPaths`` are cataloged.
"""

from __future__ import annotations

import json
import subprocess
from collections import Counter
from pathlib import Path, PurePosixPath

from build_catalog import category_for, normalize_name, parse_frontmatter_text

REPO = Path(__file__).resolve().parents[1]
LOCK = REPO / "catalog" / "sources.lock.json"
OUTPUT = REPO / "catalog" / "curated-skills.json"


def git(root: Path, *args: str) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(root), *args], text=True, stderr=subprocess.PIPE
        ).strip()
    except (FileNotFoundError, subprocess.CalledProcessError) as error:
        detail = getattr(error, "stderr", "").strip()
        message = f"cannot inspect initialized source {root.relative_to(REPO)}"
        if detail:
            message += f": {detail}"
        raise SystemExit(message) from error


def skill_blobs(root: Path, commit: str) -> dict[str, str]:
    """Return every SKILL.md path and Git blob ID at the pinned commit."""
    try:
        raw = subprocess.check_output(
            ["git", "-C", str(root), "ls-tree", "-r", "-z", commit],
            stderr=subprocess.PIPE,
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as error:
        detail = getattr(error, "stderr", b"").decode(errors="replace").strip()
        message = f"cannot read pinned tree for {root.relative_to(REPO)}"
        if detail:
            message += f": {detail}"
        raise SystemExit(message) from error

    entries: dict[str, str] = {}
    for item in raw.split(b"\0"):
        if not item:
            continue
        metadata, encoded_path = item.split(b"\t", 1)
        mode, kind, digest = metadata.decode("ascii").split()
        path = encoded_path.decode("utf-8", errors="surrogateescape")
        if (
            mode in {"100644", "100755"}
            and kind == "blob"
            and PurePosixPath(path).name == "SKILL.md"
        ):
            entries[path] = digest
    return entries


def selected_paths(source: dict[str, object]) -> list[str]:
    values = source.get("skillPaths", [])
    if not isinstance(values, list) or not values:
        raise SystemExit(f"curated source {source['id']} has no skillPaths selection")
    paths = [str(value) for value in values]
    if len(paths) != len(set(paths)):
        raise SystemExit(f"curated source {source['id']} repeats a selected skill path")
    for value in paths:
        path = PurePosixPath(value)
        if path.is_absolute() or ".." in path.parts or path.name != "SKILL.md":
            raise SystemExit(f"unsafe curated skill path for {source['id']}: {value}")
    return paths


def build_source(source: dict[str, object]) -> list[dict[str, object]]:
    root = REPO / str(source["submodulePath"])
    if not (root / ".git").exists():
        raise SystemExit(
            f"curated source is not initialized: {root.relative_to(REPO)}\n"
            f"Run: git submodule update --init {root.relative_to(REPO)}"
        )

    commit = str(source["commit"])
    head = git(root, "rev-parse", "HEAD")
    if head != commit:
        raise SystemExit(
            f"curated source checkout is not pinned: {root.relative_to(REPO)} "
            f"(expected {commit}, found {head})"
        )

    selected = selected_paths(source)
    expected = int(source["skillCount"])
    if len(selected) != expected:
        raise SystemExit(
            f"skill selection count changed for {source['id']}: "
            f"expected {expected}, found {len(selected)}"
        )
    blobs = skill_blobs(root, commit)
    missing = [path for path in selected if path not in blobs]
    if missing:
        raise SystemExit(
            f"selected paths missing at pinned commit for {source['id']}: "
            + ", ".join(missing)
        )

    records: list[dict[str, object]] = []
    for source_path in selected:
        selected_path = PurePosixPath(source_path)
        package_path = PurePosixPath(str(source.get("packagePath", selected_path.parent)))
        if package_path.is_absolute() or ".." in package_path.parts:
            raise SystemExit(f"unsafe curated package path for {source['id']}: {package_path}")
        if package_path != PurePosixPath(".") and package_path not in selected_path.parents:
            raise SystemExit(
                f"curated package path does not contain selected skill for {source['id']}: "
                f"{package_path}"
            )
        if not (root / package_path).is_dir():
            raise SystemExit(
                f"curated package path is not a directory for {source['id']}: {package_path}"
            )
        skill_path = root / selected_path
        text = skill_path.read_text(encoding="utf-8", errors="replace")
        fallback_name = PurePosixPath(source_path).parent.name
        if fallback_name in {"", "."}:
            fallback_name = str(source["id"])
        display_name, description, valid_frontmatter = parse_frontmatter_text(
            text, fallback_name
        )
        if not description:
            description = (
                f"Pinned curated skill from {source['publisher']}: {source_path}"
            )
        relative_path = f"{source['submodulePath']}/{source_path}"
        relative_package = str(source["submodulePath"])
        if package_path != PurePosixPath("."):
            relative_package += f"/{package_path.as_posix()}"
        record: dict[str, object] = {
            "id": f"{source['id']}:{source_path}",
            "name": normalize_name(display_name),
            "displayName": display_name,
            "description": description,
            "category": category_for(display_name, description, relative_path),
            "tier": "curated-source",
            "collection": source["id"],
            "path": relative_path,
            "sourcePackagePath": relative_package,
            "sourceId": source["id"],
            "sourcePublisher": source["publisher"],
            "sourceCommit": commit,
            "sourceLicense": source["license"],
            "sourceSelection": source["selection"],
            "gitBlobSha": blobs[source_path],
            "frontmatter": "valid" if valid_frontmatter else "legacy",
            "requiresSubmoduleInit": True,
        }
        for key in ("createdAt", "starsAtAudit"):
            if key in source:
                record[key] = source[key]
        records.append(record)
    return records


def main() -> None:
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    sources = lock.get("curatedSources", [])
    if not sources:
        raise SystemExit("catalog/sources.lock.json has no curatedSources")

    records = [record for source in sources for record in build_source(source)]
    by_source = Counter(str(record["sourceId"]) for record in records)
    by_category = Counter(str(record["category"]) for record in records)
    by_selection = Counter(str(record["sourceSelection"]) for record in records)
    payload = {
        "formatVersion": 1,
        "count": len(records),
        "generatedFrom": "catalog/sources.lock.json curatedSources.skillPaths",
        "bySource": dict(sorted(by_source.items())),
        "byCategory": dict(sorted(by_category.items())),
        "bySelection": dict(sorted(by_selection.items())),
        "skills": sorted(
            records,
            key=lambda record: (
                str(record["name"]), str(record["sourceId"]), str(record["path"])
            ),
        ),
    }
    OUTPUT.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"Cataloged {len(records)} curated skill entry points in "
        f"{OUTPUT.relative_to(REPO)}"
    )


if __name__ == "__main__":
    main()
