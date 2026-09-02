#!/usr/bin/env python3
"""Build metadata for skills pinned from official platform repositories.

The catalog records Git blob IDs and pinned source commits, but does not copy
upstream packages into the main repository. Initialize the official submodules
before running this script.
"""

from __future__ import annotations

import json
import subprocess
from collections import Counter
from pathlib import Path, PurePosixPath

from build_catalog import category_for, normalize_name, parse_frontmatter_text

REPO = Path(__file__).resolve().parents[1]
LOCK = REPO / "catalog" / "sources.lock.json"
OUTPUT = REPO / "catalog" / "official-skills.json"


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


def tree_entries(root: Path, commit: str) -> list[tuple[str, str]]:
    """Return (path, blob SHA) pairs for every SKILL.md at the pinned commit."""
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

    entries: list[tuple[str, str]] = []
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
            entries.append((path, digest))
    return sorted(entries)


def build_source(source: dict[str, object]) -> list[dict[str, object]]:
    root = REPO / str(source["submodulePath"])
    if not (root / ".git").exists():
        raise SystemExit(
            f"official source is not initialized: {root.relative_to(REPO)}\n"
            f"Run: git submodule update --init {root.relative_to(REPO)}"
        )

    commit = str(source["commit"])
    head = git(root, "rev-parse", "HEAD")
    if head != commit:
        raise SystemExit(
            f"official source checkout is not pinned: {root.relative_to(REPO)} "
            f"(expected {commit}, found {head})"
        )

    entries = tree_entries(root, commit)
    expected = int(source["skillCount"])
    if len(entries) != expected:
        raise SystemExit(
            f"skill count changed for {source['id']}: expected {expected}, found {len(entries)}"
        )

    records: list[dict[str, object]] = []
    for source_path, blob_sha in entries:
        skill_path = root / PurePosixPath(source_path)
        text = skill_path.read_text(encoding="utf-8", errors="replace")
        fallback_name = PurePosixPath(source_path).parent.name
        display_name, description, valid_frontmatter = parse_frontmatter_text(text, fallback_name)
        if not description:
            description = (
                f"Pinned official skill from {source['publisher']}: {source_path}"
            )
        relative_path = f"{source['submodulePath']}/{source_path}"
        records.append(
            {
                "id": f"{source['id']}:{source_path}",
                "name": normalize_name(display_name),
                "displayName": display_name,
                "description": description,
                "category": category_for(display_name, description, relative_path),
                "tier": "official-source",
                "collection": source["id"],
                "path": relative_path,
                "sourceId": source["id"],
                "sourcePublisher": source["publisher"],
                "sourceCommit": commit,
                "sourceLicense": source["license"],
                "sourceStatus": source.get("status", "current"),
                "gitBlobSha": blob_sha,
                "frontmatter": "valid" if valid_frontmatter else "legacy",
                "requiresSubmoduleInit": True,
            }
        )
    return records


def main() -> None:
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    sources = lock.get("officialSources", [])
    if not sources:
        raise SystemExit("catalog/sources.lock.json has no officialSources")

    records = [record for source in sources for record in build_source(source)]
    by_source = Counter(str(record["sourceId"]) for record in records)
    by_category = Counter(str(record["category"]) for record in records)
    payload = {
        "formatVersion": 1,
        "count": len(records),
        "generatedFrom": "catalog/sources.lock.json officialSources",
        "bySource": dict(sorted(by_source.items())),
        "byCategory": dict(sorted(by_category.items())),
        "skills": sorted(
            records,
            key=lambda record: (
                str(record["name"]), str(record["sourceId"]), str(record["path"])
            ),
        ),
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Cataloged {len(records)} official skill entry points in {OUTPUT.relative_to(REPO)}")


if __name__ == "__main__":
    main()
