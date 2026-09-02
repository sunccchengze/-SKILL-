#!/usr/bin/env python3
"""Materialize the complete skill union from pinned full-source submodules.

The checked-in compact library remains a fast searchable index. This script
copies every file from every skill package into a local ignored full-library,
retains conflicting same-path versions, and omits obsolete archives by default.
It never edits a source submodule.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

ARCHIVE_SUFFIXES = (
    ".zip", ".7z", ".rar", ".tar", ".tar.gz", ".tgz", ".tar.bz2", ".tbz2",
    ".tar.xz", ".txz", ".gz", ".bz2",
)
IGNORED_PARTS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache"}


@dataclass(frozen=True)
class Source:
    id: str
    path: Path
    skill_subdir: str | None = None
    skill_paths: tuple[str, ...] = ()
    package_paths: tuple[str, ...] = ()


AGGREGATES = (
    Source("turbine", REPO / "full-sources/aggregate-turbine", "技能库&准则"),
    Source("wind", REPO / "full-sources/aggregate-wind", "技能库&准则"),
    Source("repo", REPO / "full-sources/aggregate-repo", "技能库&准则"),
)
DIRECT = (
    Source("human-writing", REPO / "full-sources/human-writing"),
    Source("victor-design", REPO / "full-sources/victor-design"),
    Source("openwiki", REPO / "full-sources/openwiki"),
    Source("screencoder", REPO / "full-sources/screencoder"),
)
RESEARCH = (
    Source("academic-research-skills", REPO / "full-sources/research/academic-research-skills"),
    Source("academic-research-skills-codex", REPO / "full-sources/research/academic-research-skills-codex"),
    Source("nature-skills", REPO / "full-sources/research/nature-skills"),
    Source("scientific-agent-skills", REPO / "full-sources/research/scientific-agent-skills"),
    Source("aris", REPO / "full-sources/research/aris"),
    Source("ai-research-skills", REPO / "full-sources/research/ai-research-skills"),
    Source("research-paper-writing-skills", REPO / "full-sources/research/research-paper-writing-skills"),
    Source("paperspine", REPO / "full-sources/research/paperspine"),
    Source("paper-craft-skills", REPO / "full-sources/research/paper-craft-skills"),
    Source("hermes-agent", REPO / "full-sources/research/hermes-agent"),
    Source("hamelnb", REPO / "full-sources/research/hamelnb"),
)
OFFICIAL = (
    Source("openai-plugins", REPO / "full-sources/official/openai-plugins"),
    Source("openai-skills", REPO / "full-sources/official/openai-skills"),
    Source("vercel-agent-skills", REPO / "full-sources/official/vercel-agent-skills"),
    Source("microsoft-skills", REPO / "full-sources/official/microsoft-skills"),
)
CURATED = (
    Source("cyberppt", REPO / "full-sources/curated/cyberppt", skill_paths=("SKILL.md",)),
    Source(
        "figures4papers", REPO / "full-sources/curated/figures4papers",
        skill_paths=("scientific-figure-making/SKILL.md",),
    ),
    Source(
        "anydoc", REPO / "full-sources/curated/anydoc",
        skill_paths=("skills/convert-documents-to-markdown/SKILL.md",),
    ),
    Source("img2threejs", REPO / "full-sources/curated/img2threejs", skill_paths=("SKILL.md",)),
    Source(
        "video-shotcraft", REPO / "full-sources/curated/video-shotcraft",
        skill_paths=("SKILL.md",),
    ),
    Source(
        "simple-english", REPO / "full-sources/curated/simple-english",
        skill_paths=("skills/simple-english/SKILL.md",),
    ),
    Source(
        "design-evaluation", REPO / "full-sources/curated/design-evaluation",
        skill_paths=("skills/design-evaluation/SKILL.md",),
    ),
    Source("qiaomu-seo", REPO / "full-sources/curated/qiaomu-seo", skill_paths=("SKILL.md",)),
    Source(
        "bolt-slides", REPO / "full-sources/curated/bolt-slides",
        skill_paths=(".bolt/skills/slides/SKILL.md",), package_paths=(".",),
    ),
    Source(
        "sssf", REPO / "full-sources/curated/sssf",
        skill_paths=(".claude/skills/sssf/SKILL.md",),
    ),
    Source(
        "trace-file-lineage", REPO / "full-sources/curated/trace-file-lineage",
        skill_paths=("skills/trace-file-lineage/SKILL.md",),
    ),
    Source(
        "high-stakes-analytics", REPO / "full-sources/curated/high-stakes-analytics",
        skill_paths=("SKILL.md",),
    ),
    Source(
        "record-browser-gif", REPO / "full-sources/curated/record-browser-gif",
        skill_paths=(".agents/skills/record-browser-gif/SKILL.md",),
    ),
    Source(
        "popular-web-designs", REPO / "full-sources/curated/popular-web-designs",
        skill_paths=("skills-seed/popular-web-designs/SKILL.md",),
    ),
    Source(
        "better-accessibility", REPO / "full-sources/curated/better-accessibility",
        skill_paths=(".agents/skills/better-accessibility/SKILL.md",),
    ),
    Source(
        "ai-copywriter", REPO / "full-sources/curated/ai-copywriter",
        skill_paths=("SKILL.md",),
    ),
    Source(
        "bento-slides", REPO / "full-sources/curated/bento-slides",
        skill_paths=("plugins/bento-slides/skills/bento-slides/SKILL.md",),
    ),
    Source(
        "change-traceability-review",
        REPO / "full-sources/curated/change-traceability-review",
        skill_paths=(".agents/skills/change-traceability-review/SKILL.md",),
    ),
    Source(
        "oil-motion", REPO / "full-sources/curated/oil-motion",
        skill_paths=("SKILL.md",), package_paths=(".",),
    ),
    Source(
        "novel-outline", REPO / "full-sources/curated/novel-outline",
        skill_paths=("skills/novel-outline/SKILL.md",),
    ),
    Source(
        "story-to-handdrawn-video",
        REPO / "full-sources/curated/story-to-handdrawn-video",
        skill_paths=("skill-package/story-to-handdrawn-video/SKILL.md",),
        package_paths=(".",),
    ),
    Source(
        "human-review", REPO / "full-sources/curated/human-review",
        skill_paths=("src/SKILL.md",), package_paths=(".",),
    ),
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def is_archive(path: Path) -> bool:
    name = path.name.casefold()
    return any(name.endswith(suffix) for suffix in ARCHIVE_SUFFIXES)


def is_notice_file(path: Path) -> bool:
    name = path.name.casefold()
    return path.is_file() and (
        name in {"license", "notice", "copying"}
        or name.startswith(("license.", "license-", "notice.", "notice-", "copying."))
    )


def source_files(root: Path, keep_archives: bool):
    for path in sorted(root.rglob("*")):
        if not path.is_file() and not path.is_symlink():
            continue
        relative = path.relative_to(root)
        if any(part in IGNORED_PARTS for part in relative.parts):
            continue
        if not keep_archives and is_archive(path):
            yield path, relative, "archive"
            continue
        yield path, relative, "file"


def copy_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source.is_symlink():
        if destination.exists() or destination.is_symlink():
            destination.unlink()
        destination.symlink_to(os.readlink(source))
    else:
        shutil.copy2(source, destination)


def destination_has_type_conflict(destination: Path, root: Path) -> bool:
    """Return whether a file/symlink cannot occupy this merged-tree path."""
    if destination.exists() or destination.is_symlink():
        return True
    for parent in destination.parents:
        if parent == root:
            break
        if parent.is_symlink() or (parent.exists() and not parent.is_dir()):
            return True
    return False


def require_sources() -> None:
    missing = []
    for source in (*AGGREGATES, *DIRECT, *RESEARCH, *OFFICIAL, *CURATED):
        root = source.path / source.skill_subdir if source.skill_subdir else source.path
        if not (source.path / ".git").exists() or not root.is_dir():
            missing.append(str(source.path.relative_to(REPO)))
    if missing:
        lines = "\n  - ".join(missing)
        raise SystemExit(
            "Full sources are not initialized:\n  - " + lines +
            "\nRun: git submodule update --init --recursive"
        )


def safe_clean(output: Path) -> None:
    resolved_repo = REPO.resolve()
    resolved_output = output.resolve()
    if resolved_output == resolved_repo or resolved_repo not in resolved_output.parents:
        raise SystemExit(f"Refusing to clean unsafe output path: {resolved_output}")
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPO / "full-library")
    parser.add_argument(
        "--keep-archives", action="store_true",
        help="also copy zip/tar/gz/7z/rar files (off by default)",
    )
    parser.add_argument(
        "--no-clean", action="store_true",
        help="merge into an existing output instead of recreating it",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    require_sources()
    output = args.output.resolve()
    if not args.no_clean:
        safe_clean(output)
    else:
        output.mkdir(parents=True, exist_ok=True)

    manifest: dict[str, object] = {
        "formatVersion": 1,
        "archivePolicy": "kept" if args.keep_archives else "excluded-as-redundant",
        "aggregateSources": [],
        "directSources": [],
        "researchSources": [],
        "officialSources": [],
        "curatedSources": [],
        "counts": {
            "copied": 0,
            "identicalDuplicates": 0,
            "samePathVariants": 0,
            "excludedArchives": 0,
        },
    }
    counts = manifest["counts"]

    # Merge aggregate skill directories. Identical paths/content collapse into
    # one file. Same-path/different-content versions are retained losslessly.
    union_root = output / "skills"
    seen: dict[str, tuple[str, str]] = {}
    for source in AGGREGATES:
        root = source.path / str(source.skill_subdir)
        source_record = {"id": source.id, "path": str(root.relative_to(REPO)), "files": 0}
        for path, relative, kind in source_files(root, args.keep_archives):
            if kind == "archive":
                counts["excludedArchives"] += 1
                continue
            key = relative.as_posix()
            file_digest = digest(path) if not path.is_symlink() else "symlink:" + os.readlink(path)
            source_record["files"] += 1
            primary_destination = union_root / relative
            if key not in seen:
                # A path can be an implicit directory in one collection and a
                # file/symlink in another (or sit below a prior symlink). Keep
                # the later representation as a source variant instead of
                # deleting the already-materialized subtree.
                if destination_has_type_conflict(primary_destination, union_root):
                    variant = output / "source-variants" / source.id / relative
                    copy_file(path, variant)
                    counts["samePathVariants"] += 1
                    counts["copied"] += 1
                    continue
                copy_file(path, primary_destination)
                seen[key] = (file_digest, source.id)
                counts["copied"] += 1
                continue
            prior_digest, prior_source = seen[key]
            if prior_digest == file_digest:
                counts["identicalDuplicates"] += 1
                continue
            variant = output / "source-variants" / source.id / relative
            copy_file(path, variant)
            counts["samePathVariants"] += 1
            counts["copied"] += 1
        manifest["aggregateSources"].append(source_record)

    # Direct projects are namespaced, so every non-archive file is copied.
    direct_root = output / "direct"
    for source in DIRECT:
        source_record = {"id": source.id, "path": str(source.path.relative_to(REPO)), "files": 0}
        for path, relative, kind in source_files(source.path, args.keep_archives):
            if kind == "archive":
                counts["excludedArchives"] += 1
                continue
            copy_file(path, direct_root / source.id / relative)
            source_record["files"] += 1
            counts["copied"] += 1
        manifest["directSources"].append(source_record)

    for group_name, sources, destination_root in (
        ("researchSources", RESEARCH, output / "research"),
        ("officialSources", OFFICIAL, output / "official"),
    ):
        for source in sources:
            source_record = {
                "id": source.id,
                "path": str(source.path.relative_to(REPO)),
                "files": 0,
            }
            for path, relative, kind in source_files(source.path, args.keep_archives):
                if kind == "archive":
                    counts["excludedArchives"] += 1
                    continue
                copy_file(path, destination_root / source.id / relative)
                source_record["files"] += 1
                counts["copied"] += 1
            manifest[group_name].append(source_record)

    # Curated repositories may contain adjacent, unselected skills. Copy only
    # the explicitly audited package directories so the materialized layer
    # preserves the exact 2 requested + 10 round-one + 10 round-two boundary.
    curated_root = output / "curated"
    for source in CURATED:
        source_destination = curated_root / source.id
        source_record = {
            "id": source.id,
            "path": str(source.path.relative_to(REPO)),
            "selectedSkillPaths": list(source.skill_paths),
            "files": 0,
        }
        package_roots = (
            {source.path / package_path for package_path in source.package_paths}
            if source.package_paths
            else {(source.path / skill_path).parent for skill_path in source.skill_paths}
        )
        if source.path not in package_roots:
            for notice in sorted(path for path in source.path.iterdir() if is_notice_file(path)):
                copy_file(notice, source_destination / notice.name)
                source_record["files"] += 1
                counts["copied"] += 1
        for package in sorted(package_roots):
            package_relative = package.relative_to(source.path)
            destination = source_destination / package_relative
            for path, relative, kind in source_files(package, args.keep_archives):
                if kind == "archive":
                    counts["excludedArchives"] += 1
                    continue
                copy_file(path, destination / relative)
                source_record["files"] += 1
                counts["copied"] += 1
        manifest["curatedSources"].append(source_record)

    skill_entries = sorted(
        str(path.relative_to(output)) for path in output.rglob("SKILL.md")
        if "source-variants" not in path.parts
    )
    manifest["skillEntryCount"] = len(skill_entries)
    manifest["skillEntries"] = skill_entries
    (output / "MANIFEST.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"output": str(output), **counts, "skillEntries": len(skill_entries)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
