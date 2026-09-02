#!/usr/bin/env python3
"""Build the compact semantic union used by this repository.

The source repositories contain many duplicated harness exports, translations,
application sources, tests, archives, and large media files. This importer
keeps every distinct normalized instructional body while selecting one
resource-complete canonical package per logical skill name. Distinct same-name
alternatives are kept as lightweight variants; byte-identical and
frontmatter-only copies are recorded as provenance-preserving aliases.

This script does not clone repositories. Pass existing checkouts so that a
refresh is explicit and inspectable.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

SOURCE_BRANCHES = {
    "turbine": "arena/019feb03-turbine-blade-ai-platform",
    "wind": "arena/019feb53-wind-farm-viz",
    "repo": "arena/019ff697-repo",
}

# These trees are byte-identical or generated aliases of a retained collection.
COLLECTION_ALIASES = {
    "addyosmani-agent-skills": "agent-skills-main",
    "obra-superpowers": "superpowers-main",
    "Qwen-MM-Plugins": "qwen-mm-plugins",
    "Understand-Anything": "understand-anything",
    # Its 19 core skills are byte-identical to nature-skills; the latter has
    # the cleaner package layout. Two additional skills remain available from
    # other retained collections.
    "codex-research-workflow": "nature-skills",
}

# A maintained first-party import is installed separately for this name. An
# aggregate copy with the same normalized instructions is indexed as source
# provenance rather than emitted as a redundant variant.
RESERVED_CANONICAL_PATHS = {"human-writing": "skills/community/human-writing/SKILL.md"}

COMMON_RESOURCE_DIRS = {
    "assets",
    "data",
    "examples",
    "fonts",
    "helpers",
    "references",
    "resources",
    "scripts",
    "templates",
}

PRUNED_DIRS = {
    ".git",
    ".next",
    ".venv",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "fixtures",
    "node_modules",
    "test",
    "tests",
}

PRUNED_FILENAMES = {".gitattributes", ".gitignore", ".gitmodules"}

# Community imports are an agent-readable knowledge distribution, not an asset
# mirror. Maintained skills explicitly requested by the repository owner are
# copied separately without this media filter.
PRUNED_EXTENSIONS = {
    ".7z",
    ".avi",
    ".docx",
    ".gif",
    ".gz",
    ".icns",
    ".jpeg",
    ".jpg",
    ".mov",
    ".mp3",
    ".mp4",
    ".pdf",
    ".png",
    ".pptx",
    ".psd",
    ".rar",
    ".tar",
    ".ttf",
    ".webp",
    ".woff",
    ".woff2",
    ".zip",
}

MAX_COMMUNITY_FILE_BYTES = 500_000

COLLECTION_RANK = {
    "skills-main": 0,
    "superpowers-main": 1,
    "scientific-agent-skills": 2,
    "agent-skills-main": 3,
    "ECC": 4,
}

HARNESS_OR_TRANSLATION_DIRS = {
    ".agents",
    ".claude",
    ".cursor",
    ".gemini",
    ".kiro",
    "docs",
}


@dataclass(frozen=True)
class Candidate:
    source_label: str
    source_root: Path
    path: Path
    relative_path: Path
    digest: str
    instruction_digest: str
    name: str
    description: str

    @property
    def collection(self) -> str:
        return self.relative_path.parts[0]

    @property
    def package_relative_path(self) -> Path:
        return self.relative_path.parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalized_instruction_bytes(path: Path) -> bytes:
    """Return the executable instructions, ignoring packaging metadata only."""
    content = path.read_bytes().replace(b"\r\n", b"\n")
    if content.startswith(b"---\n"):
        parts = content.split(b"---\n", 2)
        if len(parts) == 3:
            content = parts[2]
    return content.strip()


def instructional_sha256(path: Path) -> str:
    return hashlib.sha256(normalized_instruction_bytes(path)).hexdigest()


def parse_frontmatter(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    match = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.DOTALL)
    if not match:
        return path.parent.name, ""

    frontmatter = match.group(1)
    name_match = re.search(
        r"(?m)^name:\s*[\"']?([^\n\"']+)", frontmatter
    )
    description_match = re.search(
        r"(?m)^description:\s*[\"']?([^\n\"']+)", frontmatter
    )
    name = name_match.group(1).strip() if name_match else path.parent.name
    description = description_match.group(1).strip() if description_match else ""
    return name, description


def normalize_name(name: str) -> str:
    normalized = name.strip().casefold().replace("_", "-")
    normalized = re.sub(r"\s+", "-", normalized)
    normalized = re.sub(r"-+", "-", normalized)
    return normalized


def candidate_score(candidate: Candidate) -> tuple[int, int, int, int, str, str]:
    parts = candidate.relative_path.parts
    generated_penalty = 100 * sum(
        part in HARNESS_OR_TRANSLATION_DIRS for part in parts
    )
    return (
        generated_penalty,
        COLLECTION_RANK.get(candidate.collection, 50),
        len(parts),
        len(str(candidate.relative_path)),
        str(candidate.relative_path),
        candidate.source_label,
    )


def iter_candidates(source_label: str, source_root: Path) -> Iterable[Candidate]:
    for skill_path in sorted(source_root.rglob("SKILL.md")):
        relative_path = skill_path.relative_to(source_root)
        if relative_path.parts[0] in COLLECTION_ALIASES:
            continue
        # Fixture skills intentionally contain malformed metadata and collision
        # cases. They test an upstream loader; they are not usable capabilities.
        if any(part in {"test", "tests", "fixtures"} for part in relative_path.parts):
            continue
        name, description = parse_frontmatter(skill_path)
        yield Candidate(
            source_label=source_label,
            source_root=source_root,
            path=skill_path,
            relative_path=relative_path,
            digest=sha256(skill_path),
            instruction_digest=instructional_sha256(skill_path),
            name=normalize_name(name),
            description=description,
        )


def should_copy_community_file(
    path: Path, source_root: Path, active_skill: Path
) -> bool:
    if not path.is_file():
        return False
    if path.stat().st_size > MAX_COMMUNITY_FILE_BYTES:
        return False
    # A legitimate package may itself be named "build" or "coverage". Always
    # retain its selected entry point; pruning applies to companion files.
    if path == active_skill:
        return True
    relative_path = path.relative_to(source_root)
    if any(part in PRUNED_DIRS for part in relative_path.parts):
        return False
    if path.name in PRUNED_FILENAMES:
        return False
    if path.suffix.casefold() in PRUNED_EXTENSIONS:
        return False
    # Nested skill packages are selected independently. This prevents a parent
    # package from accidentally restoring a variant or exact duplicate.
    if path.name == "SKILL.md":
        return False
    return True


def candidate_package_files(candidate: Candidate) -> Iterable[Path]:
    package_root = candidate.path.parent
    relative_package = package_root.relative_to(candidate.source_root)

    # A SKILL.md at a collection root often sits beside an entire application.
    # Keep direct files and recognized skill resource directories only.
    if len(relative_package.parts) == 1:
        for child in sorted(package_root.iterdir()):
            if should_copy_community_file(
                child, candidate.source_root, candidate.path
            ):
                yield child
            elif child.is_dir() and child.name in COMMON_RESOURCE_DIRS:
                for nested in sorted(child.rglob("*")):
                    if should_copy_community_file(
                        nested, candidate.source_root, candidate.path
                    ):
                        yield nested
        return

    for path in sorted(package_root.rglob("*")):
        if should_copy_community_file(path, candidate.source_root, candidate.path):
            yield path


def safe_reset_directory(path: Path, repository_root: Path) -> None:
    resolved_repo = repository_root.resolve()
    resolved_path = path.resolve()
    if resolved_path == resolved_repo or resolved_repo not in resolved_path.parents:
        raise RuntimeError(f"refusing to reset unsafe path: {resolved_path}")
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def copy_candidate_package(
    candidate: Candidate, community_root: Path
) -> tuple[Path, int]:
    destination_package = community_root / candidate.package_relative_path
    copied = 0
    for source_file in candidate_package_files(candidate):
        relative_inside_package = source_file.relative_to(candidate.path.parent)
        destination = destination_package / relative_inside_package
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists() and sha256(destination) == sha256(source_file):
            continue
        shutil.copy2(source_file, destination)
        copied += 1
    return destination_package / "SKILL.md", copied


def variant_destination(candidate: Candidate, variants_root: Path) -> Path:
    return variants_root / candidate.package_relative_path / "SKILL.md"


def copy_licenses(
    collections: set[str], source_roots: list[tuple[str, Path]], licenses_root: Path
) -> dict[str, dict[str, str] | None]:
    license_index: dict[str, dict[str, str] | None] = {}
    for collection in sorted(collections, key=str.casefold):
        found: tuple[str, Path] | None = None
        for source_label, source_root in source_roots:
            collection_root = source_root / collection
            for filename in ("LICENSE", "LICENSE.md", "COPYING"):
                candidate = collection_root / filename
                if candidate.is_file():
                    found = source_label, candidate
                    break
            if found:
                break

        if not found:
            license_index[collection] = None
            continue

        source_label, license_path = found
        destination = licenses_root / collection / license_path.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(license_path, destination)
        license_index[collection] = {
            "source": source_label,
            "sourcePath": str(license_path),
            "outputPath": str(destination.relative_to(licenses_root.parent.parent)),
            "sha256": sha256(license_path),
        }
    return license_index


def build_union(
    repository_root: Path,
    source_roots: list[tuple[str, Path]],
) -> dict[str, object]:
    community_root = repository_root / "skills" / "community"
    variants_root = repository_root / "skills" / "variants"
    licenses_root = repository_root / "third_party" / "licenses"
    catalog_root = repository_root / "catalog"

    safe_reset_directory(community_root, repository_root)
    safe_reset_directory(variants_root, repository_root)
    safe_reset_directory(licenses_root, repository_root)
    catalog_root.mkdir(parents=True, exist_ok=True)

    # A relative path with identical content in later aggregate sources adds no
    # information. A same-path changed body would remain a distinct candidate.
    candidates: list[Candidate] = []
    seen_path_and_hash: set[tuple[Path, str]] = set()
    for source_label, source_root in source_roots:
        for candidate in iter_candidates(source_label, source_root):
            key = candidate.relative_path, candidate.digest
            if key in seen_path_and_hash:
                continue
            seen_path_and_hash.add(key)
            candidates.append(candidate)

    by_name: dict[str, list[Candidate]] = defaultdict(list)
    for candidate in candidates:
        by_name[candidate.name].append(candidate)

    canonical: list[Candidate] = []
    variants: list[Candidate] = []
    aliases: list[dict[str, object]] = []
    alias_group_by_identity: dict[tuple[str, str], dict[str, object]] = {}

    for skill_name, same_name_candidates in sorted(by_name.items()):
        by_instruction_hash: dict[str, list[Candidate]] = defaultdict(list)
        for candidate in same_name_candidates:
            by_instruction_hash[candidate.instruction_digest].append(candidate)

        unique_bodies: list[Candidate] = []
        for instruction_digest, equivalent_copies in sorted(by_instruction_hash.items()):
            preferred = min(equivalent_copies, key=candidate_score)
            unique_bodies.append(preferred)
            alias_group: dict[str, object] = {
                "name": skill_name,
                "instructionSha256": instruction_digest,
                "sha256": preferred.digest,
                "canonicalSourcePath": str(preferred.relative_path),
                "aliases": [
                    {
                        "source": item.source_label,
                        "path": str(item.relative_path),
                        "sha256": item.digest,
                        "reason": (
                            "byte-identical"
                            if item.digest == preferred.digest
                            else "frontmatter-only"
                        ),
                    }
                    for item in sorted(equivalent_copies, key=candidate_score)
                    if item != preferred
                ],
            }
            aliases.append(alias_group)
            alias_group_by_identity[(skill_name, instruction_digest)] = alias_group

        unique_bodies.sort(key=candidate_score)
        reserved_path = RESERVED_CANONICAL_PATHS.get(skill_name)
        if reserved_path:
            reserved_file = repository_root / reserved_path
            reserved_digest = (
                instructional_sha256(reserved_file) if reserved_file.is_file() else None
            )
            for candidate in unique_bodies:
                if candidate.instruction_digest == reserved_digest:
                    alias_group_by_identity[
                        (skill_name, candidate.instruction_digest)
                    ]["canonicalOutputPath"] = reserved_path
                else:
                    variants.append(candidate)
        else:
            canonical.append(unique_bodies[0])
            variants.extend(unique_bodies[1:])

    canonical_records: list[dict[str, object]] = []
    copied_files = 0
    for candidate in sorted(canonical, key=lambda item: str(item.relative_path)):
        output_path, copied = copy_candidate_package(candidate, community_root)
        copied_files += copied
        canonical_records.append(
            {
                "name": candidate.name,
                "description": candidate.description,
                "collection": candidate.collection,
                "source": candidate.source_label,
                "sourcePath": str(candidate.relative_path),
                "outputPath": str(output_path.relative_to(repository_root)),
                "sha256": candidate.digest,
                "instructionSha256": candidate.instruction_digest,
            }
        )

    variant_records: list[dict[str, object]] = []
    for candidate in sorted(variants, key=lambda item: str(item.relative_path)):
        destination = variant_destination(candidate, variants_root)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(candidate.path, destination)
        variant_records.append(
            {
                "name": candidate.name,
                "description": candidate.description,
                "collection": candidate.collection,
                "source": candidate.source_label,
                "sourcePath": str(candidate.relative_path),
                "outputPath": str(destination.relative_to(repository_root)),
                "sha256": candidate.digest,
                "instructionSha256": candidate.instruction_digest,
            }
        )

    collections = {candidate.collection for candidate in candidates}
    license_index = copy_licenses(collections, source_roots, licenses_root)

    result: dict[str, object] = {
        "formatVersion": 2,
        "policy": {
            "mode": "compact-semantic-union",
            "canonicalRule": "one resource-complete package per normalized skill name",
            "variantRule": "every distinct normalized instructional body for a same-name skill is retained",
            "aliasRule": "byte-identical and frontmatter-only copies are indexed with source provenance but not copied",
            "instructionNormalization": "strip YAML frontmatter and outer whitespace; normalize CRLF to LF",
            "communityMaxFileBytes": MAX_COMMUNITY_FILE_BYTES,
            "prunedExtensions": sorted(PRUNED_EXTENSIONS),
            "collectionAliases": COLLECTION_ALIASES,
        },
        "counts": {
            "sourceCandidates": len(candidates),
            "logicalNames": len(by_name),
            "canonicalSkills": len(canonical_records),
            "variantSkills": len(variant_records),
            "copiedCanonicalFiles": copied_files,
            "instructionBodyGroups": len(aliases),
            "retainedInstructionBodies": len(canonical_records) + len(variant_records),
            "sourceAliases": sum(len(group["aliases"]) for group in aliases),
            "externalCanonicalGroups": sum(
                "canonicalOutputPath" in group for group in aliases
            ),
        },
        "canonical": canonical_records,
        "variants": variant_records,
        "aliases": aliases,
        "licenses": license_index,
    }

    output = catalog_root / "import-report.json"
    output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="destination repository root",
    )
    parser.add_argument("--turbine", type=Path, required=True)
    parser.add_argument("--wind", type=Path, required=True)
    parser.add_argument("--repo-source", type=Path, required=True)
    return parser.parse_args()


def resolve_skill_root(checkout: Path) -> Path:
    skill_root = checkout / "技能库&准则"
    if not skill_root.is_dir():
        raise FileNotFoundError(f"skill source directory not found: {skill_root}")
    return skill_root


def main() -> None:
    args = parse_args()
    repository_root = args.repo.resolve()
    source_roots = [
        ("turbine", resolve_skill_root(args.turbine.resolve())),
        ("wind", resolve_skill_root(args.wind.resolve())),
        ("repo", resolve_skill_root(args.repo_source.resolve())),
    ]
    report = build_union(repository_root, source_roots)
    counts = report["counts"]
    print(
        "Imported {canonicalSkills} canonical skills and {variantSkills} "
        "distinct variants from {sourceCandidates} source candidates.".format(
            **counts
        )
    )


if __name__ == "__main__":
    main()
