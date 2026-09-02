#!/usr/bin/env python3
"""Validate catalog integrity, import provenance, and repository size policy."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import tarfile
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md",
    "AGENTS.md",
    "SKILL.md",
    "catalog/sources.lock.json",
    "catalog/import-report.json",
    "catalog/skills.json",
    "catalog/research-skills.json",
    "catalog/official-skills.json",
    "catalog/curated-skills.json",
    "catalog/overlap-policy.json",
    "scripts/catalog_aliases.py",
    "scripts/build_official_catalog.py",
    "scripts/build_curated_catalog.py",
    "governance/CONSTITUTION.md",
    "governance/QUALITY_GATES.md",
    "skills/community/human-writing/SKILL.md",
    "skills/core/research-expert-system/SKILL.md",
    "guides/RESEARCH.md",
    "skills/core/official-source-router/SKILL.md",
    "guides/OFFICIAL_SOURCES.md",
    "guides/CURATED_SOURCES.md",
    "skills/community/victor-design/SKILL.md",
    "tools/openwiki/SKILL.md",
    "tools/screencoder/SKILL.md",
    "tools/openwiki/package.json",
    "tools/openwiki/LICENSE",
    "tools/screencoder/README.md",
    "tools/screencoder/UPSTREAM.md",
    "tools/screencoder/LICENSE",
    "tools/opencut/SKILL.md",
    "tools/rustdesk/SKILL.md",
    "tools/spec-kit/SKILL.md",
    "guides/TOOLS.md",
    "scripts/setup_tools.sh",
    "scripts/run_opencut.sh",
    "scripts/run_rustdesk.sh",
    "scripts/verify_tools.sh",
    "scripts/build_categories.py",
    "scripts/build_starter_bundle.py",
    "categories/README.md",
    "catalog/category-summary.json",
    "bundles/newcomer-starter-pack/README.md",
    "bundles/newcomer-starter-pack/manifest.json",
    "bundles/newcomer-starter-pack/newcomer-starter-pack.tar.gz",
    "bundles/newcomer-starter-pack/SHA256SUMS",
    "bundles/research-workflow-kit/README.md",
    "bundles/research-workflow-kit/START_HERE.md",
    "bundles/research-workflow-kit/MANIFEST.json",
    "bundles/research-workflow-kit/SHA256SUMS",
    "bundles/research-workflow-kit/VALIDATION_RESULT.md",
    "bundles/research-workflow-kit/research-workflow-kit.tar.gz",
    "bundles/research-workflow-kit/tools/research_kit.py",
    "scripts/build_research_bundle.py",
]
COMMUNITY_PRUNED_EXTENSIONS = {
    ".zip", ".tar", ".gz", ".7z", ".rar", ".mp4", ".mov", ".avi",
    ".gif", ".psd", ".pptx", ".docx", ".pdf", ".ttf", ".woff",
    ".woff2", ".png", ".jpg", ".jpeg", ".webp", ".icns", ".mp3",
}
# Keep a narrow file-count headroom for maintained deep-tier packages. The
# byte cap and per-community-file cap remain the primary anti-bloat controls.
# Deep-tier Nuwa packages add source/claim ledgers, six research passes, a CLI,
# and adversarial tests. The modern-application program completed at 10,221
# measured files; retain narrow maintenance headroom and recalculate before
# another import.
MAX_FILES = 10_300
MAX_BYTES = 129 * 1024 * 1024
# Directly retrievable deterministic bundle archives are deliverables, not compact
# source payload. Keep the original 128 MiB policy for everything else and cap
# each explicitly approved archive separately.
APPROVED_BUNDLE_ARCHIVES = {
    "bundles/research-workflow-kit/research-workflow-kit.tar.gz": 64 * 1024 * 1024,
}
MAX_COMMUNITY_FILE_BYTES = 500_000


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def instructional_sha256(path: Path) -> str:
    content = path.read_bytes().replace(b"\r\n", b"\n")
    if content.startswith(b"---\n"):
        parts = content.split(b"---\n", 2)
        if len(parts) == 3:
            content = parts[2]
    return hashlib.sha256(content.strip()).hexdigest()


def validate_overlap_policy(
    catalogs: list[dict[str, object]], errors: list[str]
) -> int:
    policy = json.loads(
        (REPO / "catalog/overlap-policy.json").read_text(encoding="utf-8")
    )
    aliases = policy.get("aliases", [])
    if policy.get("formatVersion") != 1:
        fail(errors, "unsupported overlap policy format")
    if policy.get("count") != len(aliases):
        fail(errors, "overlap policy count is stale")

    expected_by_reason = Counter(
        {
            "packaging-duplicate": 16,
            "equivalent-instruction-body": 12,
            "superseded-source": 16,
            "host-specific-alias": 1,
        }
    )
    actual_by_reason = Counter(str(alias.get("reason", "")) for alias in aliases)
    if actual_by_reason != expected_by_reason:
        fail(errors, "overlap policy reason counts do not match the audited cleanup")
    if policy.get("byReason") != dict(actual_by_reason):
        fail(errors, "overlap policy byReason summary is stale")

    records_by_path: dict[str, list[dict[str, object]]] = {}
    for catalog in catalogs:
        for record in catalog.get("skills", []):
            records_by_path.setdefault(str(record.get("path", "")), []).append(record)

    alias_paths = [str(alias.get("path", "")) for alias in aliases]
    if "" in alias_paths or len(alias_paths) != len(set(alias_paths)):
        fail(errors, "overlap policy alias paths are missing or duplicated")
    alias_path_set = set(alias_paths)
    for alias in aliases:
        path = str(alias.get("path", ""))
        canonical_path = str(alias.get("canonicalPath", ""))
        if len(records_by_path.get(path, [])) != 1:
            fail(errors, f"overlap alias does not resolve uniquely: {path}")
        if len(records_by_path.get(canonical_path, [])) != 1:
            fail(errors, f"overlap canonical does not resolve uniquely: {canonical_path}")
        if canonical_path in alias_path_set:
            fail(errors, f"overlap canonical is itself suppressed: {canonical_path}")
        source_record = records_by_path.get(path, [{}])[0]
        canonical_record = records_by_path.get(canonical_path, [{}])[0]
        reason = alias.get("reason")
        if alias.get("evidence") == "exact-git-blob":
            if source_record.get("gitBlobSha") != canonical_record.get("gitBlobSha"):
                fail(errors, f"exact-blob overlap evidence mismatch: {path}")
        if reason == "packaging-duplicate":
            if (
                alias.get("evidence") != "exact-git-blob"
                or source_record.get("sourceId") != canonical_record.get("sourceId")
            ):
                fail(errors, f"invalid packaging overlap: {path}")
        elif reason == "equivalent-instruction-body":
            if (
                source_record.get("sourceId") != "ai-research-skills"
                or canonical_record.get("sourceId") != "hermes-agent"
                or source_record.get("name") != canonical_record.get("name")
            ):
                fail(errors, f"invalid AI Research/Hermes preference: {path}")
        elif reason == "superseded-source":
            if (
                source_record.get("sourceId") != "openai-skills"
                or canonical_record.get("sourceId") != "openai-plugins"
                or source_record.get("name") != canonical_record.get("name")
            ):
                fail(errors, f"invalid deprecated OpenAI successor: {path}")
        elif reason == "host-specific-alias":
            if (
                source_record.get("sourceId") != "hermes-agent"
                or canonical_record.get("sourceId") != "popular-web-designs"
                or source_record.get("name") != "popular-web-designs"
            ):
                fail(errors, f"invalid curated host-specific preference: {path}")
    return len(aliases)


def validate_official_catalog(
    lock: dict[str, object], errors: list[str], warnings: list[str]
) -> int:
    """Validate catalog-to-lock identity and, when initialized, pinned trees."""
    catalog_path = REPO / "catalog/official-skills.json"
    if not catalog_path.is_file():
        return 0
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    sources = lock.get("officialSources", [])
    source_by_id = {source["id"]: source for source in sources}
    records = catalog.get("skills", [])
    expected_count = sum(int(source["skillCount"]) for source in sources)
    if catalog.get("count") != expected_count or len(records) != expected_count:
        fail(errors, f"official catalog count mismatch: expected={expected_count}")

    paths = [str(record.get("path", "")) for record in records]
    identities = [str(record.get("id", "")) for record in records]
    if len(paths) != len(set(paths)):
        fail(errors, "official catalog contains duplicate paths")
    if "" in identities or len(identities) != len(set(identities)):
        fail(errors, "official catalog identities are missing or duplicated")
    actual_by_source = Counter(str(record.get("sourceId", "")) for record in records)
    expected_by_source = {
        str(source["id"]): int(source["skillCount"]) for source in sources
    }
    if dict(actual_by_source) != expected_by_source:
        fail(errors, "official catalog per-source counts do not match source locks")
    if catalog.get("bySource") != dict(sorted(expected_by_source.items())):
        fail(errors, "official catalog bySource summary is stale")

    catalog_paths_by_source: dict[str, set[str]] = {
        source_id: set() for source_id in source_by_id
    }
    for record in records:
        source_id = str(record.get("sourceId", ""))
        source = source_by_id.get(source_id)
        path = str(record.get("path", ""))
        if source is None:
            fail(errors, f"unknown official catalog source: {path}")
            continue
        prefix = str(source["submodulePath"]) + "/"
        if not path.startswith(prefix):
            fail(errors, f"official catalog path mismatch: {path}")
            continue
        source_relative = path[len(prefix) :]
        catalog_paths_by_source[source_id].add(source_relative)
        if record.get("id") != f"{source_id}:{source_relative}":
            fail(errors, f"official catalog identity mismatch: {path}")
        if record.get("sourceCommit") != source["commit"]:
            fail(errors, f"official catalog commit mismatch: {path}")
        if record.get("sourcePublisher") != source["publisher"]:
            fail(errors, f"official catalog publisher mismatch: {path}")
        if record.get("sourceLicense") != source["license"]:
            fail(errors, f"official catalog license mismatch: {path}")
        if record.get("sourceStatus") != source.get("status", "current"):
            fail(errors, f"official catalog status mismatch: {path}")
        if not re.fullmatch(r"[0-9a-f]{40,64}", str(record.get("gitBlobSha", ""))):
            fail(errors, f"invalid official catalog blob ID: {path}")
        if record.get("frontmatter") not in {"valid", "legacy"}:
            fail(errors, f"invalid official frontmatter status: {path}")
        if record.get("requiresSubmoduleInit") is not True:
            fail(errors, f"official catalog missing initialization marker: {path}")

    for source_id, source in source_by_id.items():
        root = REPO / str(source["submodulePath"])
        # Compact clones may intentionally leave gitlinks uninitialized. The
        # lock/catalog checks above still run; tree-level checks run whenever
        # this source is present.
        if not (root / ".git").exists():
            warnings.append(
                f"official source not initialized; skipped tree validation: {source_id}"
            )
            continue
        head = subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
        ).strip()
        if head != source["commit"]:
            fail(errors, f"official checkout commit mismatch: {source_id}")
        discovered = {
            path.relative_to(root).as_posix()
            for path in root.rglob("SKILL.md")
            if ".git" not in path.relative_to(root).parts
        }
        if discovered != catalog_paths_by_source[source_id]:
            fail(errors, f"official catalog tree coverage mismatch: {source_id}")
        for relative in sorted(catalog_paths_by_source[source_id]):
            skill_file = root / relative
            if not skill_file.is_file():
                fail(errors, f"official catalog path missing: {source_id}/{relative}")
                continue
            blob_sha = subprocess.check_output(
                ["git", "-C", str(root), "hash-object", relative], text=True
            ).strip()
            record = next(
                item
                for item in records
                if item.get("sourceId") == source_id
                and str(item.get("path", "")).endswith("/" + relative)
            )
            if blob_sha != record["gitBlobSha"]:
                fail(errors, f"official catalog blob mismatch: {source_id}/{relative}")
    return len(records)


def validate_curated_catalog(
    lock: dict[str, object], errors: list[str], warnings: list[str]
) -> int:
    """Validate the exact requested and two one-month-velocity selections."""
    catalog_path = REPO / "catalog/curated-skills.json"
    if not catalog_path.is_file():
        return 0
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    sources = lock.get("curatedSources", [])
    source_by_id = {str(source["id"]): source for source in sources}
    if len(source_by_id) != len(sources):
        fail(errors, "curated source IDs are duplicated")
    records = catalog.get("skills", [])
    expected_count = sum(int(source["skillCount"]) for source in sources)
    if expected_count != 22:
        fail(errors, f"curated lock must select 22 total skills, found={expected_count}")
    if catalog.get("count") != expected_count or len(records) != expected_count:
        fail(errors, f"curated catalog count mismatch: expected={expected_count}")

    selections: Counter[str] = Counter()
    for source in sources:
        selections[str(source.get("selection", ""))] += int(source["skillCount"])
    expected_selections = {
        "one-month-star-velocity": 10,
        "one-month-star-velocity-round-2": 10,
        "user-requested": 2,
    }
    if dict(selections) != expected_selections:
        fail(errors, f"curated selection quota mismatch: {dict(selections)}")

    trend_audit = lock.get("curatedTrendAudit", {})
    if trend_audit.get("selectedSkillCount") != 10:
        fail(errors, "curated round-one audit must record exactly 10 selections")
    if trend_audit.get("window") != "2026-07-14 through 2026-08-14":
        fail(errors, "curated round-one audit window is missing or changed")
    if trend_audit.get("auditedAt") != "2026-08-14":
        fail(errors, "curated round-one audit snapshot date is missing or changed")

    round_two_sources = [
        source for source in sources
        if source.get("selection") == "one-month-star-velocity-round-2"
    ]
    if len(round_two_sources) != 10:
        fail(errors, f"curated round-two audit must pin 10 sources, found={len(round_two_sources)}")
    round_two_audit = lock.get("curatedTrendAuditRound2", {})
    if round_two_audit.get("selectedSkillCount") != 10:
        fail(errors, "curated round-two audit must record exactly 10 selections")
    if round_two_audit.get("window") != "2026-07-14 through 2026-08-14":
        fail(errors, "curated round-two audit window is missing or changed")
    if round_two_audit.get("auditedAt") != "2026-08-14":
        fail(errors, "curated round-two audit snapshot date is missing or changed")
    round_two_stars = sum(int(source.get("starsAtAudit", 0)) for source in round_two_sources)
    if round_two_stars != 67_998 or round_two_audit.get("observedStarsTotal") != round_two_stars:
        fail(errors, f"curated round-two star snapshot mismatch: {round_two_stars}")
    if catalog.get("bySelection") != dict(sorted(expected_selections.items())):
        fail(errors, "curated catalog bySelection summary is stale")

    # Round two must add distinct skill content, not merely another submodule
    # path to a body already present in the compact layer or round one.
    earlier_hashes: dict[str, list[str]] = {}
    for skill_file in (REPO / "skills").rglob("SKILL.md"):
        digest = sha256(skill_file)
        earlier_hashes.setdefault(digest, []).append(
            skill_file.relative_to(REPO).as_posix()
        )
    for source in sources:
        if source.get("selection") == "one-month-star-velocity-round-2":
            continue
        root = REPO / str(source["submodulePath"])
        for relative in source.get("skillPaths", []):
            skill_file = root / str(relative)
            if skill_file.is_file():
                earlier_hashes.setdefault(sha256(skill_file), []).append(
                    skill_file.relative_to(REPO).as_posix()
                )
    round_two_hashes: dict[str, str] = {}
    for source in round_two_sources:
        root = REPO / str(source["submodulePath"])
        for relative in source.get("skillPaths", []):
            skill_file = root / str(relative)
            if not skill_file.is_file():
                continue
            digest = sha256(skill_file)
            if digest in earlier_hashes:
                fail(
                    errors,
                    f"curated round-two skill duplicates existing content: "
                    f"{source['id']} -> {', '.join(earlier_hashes[digest])}",
                )
            if digest in round_two_hashes:
                fail(
                    errors,
                    f"curated round-two skills duplicate each other: "
                    f"{source['id']} and {round_two_hashes[digest]}",
                )
            round_two_hashes[digest] = str(source["id"])

    paths = [str(record.get("path", "")) for record in records]
    identities = [str(record.get("id", "")) for record in records]
    if len(paths) != len(set(paths)):
        fail(errors, "curated catalog contains duplicate paths")
    if "" in identities or len(identities) != len(set(identities)):
        fail(errors, "curated catalog identities are missing or duplicated")
    actual_by_source = Counter(str(record.get("sourceId", "")) for record in records)
    expected_by_source = {
        str(source["id"]): int(source["skillCount"]) for source in sources
    }
    if dict(actual_by_source) != expected_by_source:
        fail(errors, "curated catalog per-source counts do not match source locks")
    if catalog.get("bySource") != dict(sorted(expected_by_source.items())):
        fail(errors, "curated catalog bySource summary is stale")

    records_by_source: dict[str, dict[str, dict[str, object]]] = {
        source_id: {} for source_id in source_by_id
    }
    for record in records:
        source_id = str(record.get("sourceId", ""))
        source = source_by_id.get(source_id)
        path = str(record.get("path", ""))
        if source is None:
            fail(errors, f"unknown curated catalog source: {path}")
            continue
        prefix = str(source["submodulePath"]) + "/"
        if not path.startswith(prefix):
            fail(errors, f"curated catalog path mismatch: {path}")
            continue
        source_relative = path[len(prefix) :]
        records_by_source[source_id][source_relative] = record
        selected_parent = Path(source_relative).parent.as_posix()
        package_relative = str(source.get("packagePath", selected_parent))
        expected_package = str(source["submodulePath"])
        if package_relative not in {"", "."}:
            expected_package += "/" + package_relative
        if record.get("sourcePackagePath") != expected_package:
            fail(errors, f"curated catalog package path mismatch: {path}")
        if source_relative not in source.get("skillPaths", []):
            fail(errors, f"unselected curated path was cataloged: {path}")
        if record.get("id") != f"{source_id}:{source_relative}":
            fail(errors, f"curated catalog identity mismatch: {path}")
        for record_key, source_key in (
            ("sourceCommit", "commit"),
            ("sourcePublisher", "publisher"),
            ("sourceLicense", "license"),
            ("sourceSelection", "selection"),
        ):
            if record.get(record_key) != source.get(source_key):
                fail(errors, f"curated catalog {record_key} mismatch: {path}")
        if not re.fullmatch(r"[0-9a-f]{40,64}", str(record.get("gitBlobSha", ""))):
            fail(errors, f"invalid curated catalog blob ID: {path}")
        if record.get("frontmatter") not in {"valid", "legacy"}:
            fail(errors, f"invalid curated frontmatter status: {path}")
        if record.get("requiresSubmoduleInit") is not True:
            fail(errors, f"curated catalog missing initialization marker: {path}")

    for source_id, source in source_by_id.items():
        selected = [str(path) for path in source.get("skillPaths", [])]
        if len(selected) != int(source["skillCount"]) or len(selected) != len(set(selected)):
            fail(errors, f"curated selected-path count mismatch: {source_id}")
        if set(selected) != set(records_by_source[source_id]):
            fail(errors, f"curated lock/catalog selection mismatch: {source_id}")
        if source.get("selection") in {
            "one-month-star-velocity", "one-month-star-velocity-round-2"
        }:
            created_date = str(source.get("createdAt", ""))[:10]
            if not "2026-07-14" <= created_date <= "2026-08-14":
                fail(errors, f"curated trend source falls outside audit window: {source_id}")
            if not isinstance(source.get("starsAtAudit"), int) or source["starsAtAudit"] <= 0:
                fail(errors, f"curated trend source lacks star evidence: {source_id}")
            if source.get("license") not in {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause"}:
                fail(errors, f"curated trend source is not permissively licensed: {source_id}")
        if source.get("selection") == "one-month-star-velocity-round-2":
            if not re.fullmatch(r"[0-9a-f]{40}", str(source.get("tree", ""))):
                fail(errors, f"curated round-two source lacks a pinned tree: {source_id}")
            if not re.fullmatch(
                r"2026-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z",
                str(source.get("pushedAt", "")),
            ):
                fail(errors, f"curated round-two source lacks push-time evidence: {source_id}")
        root = REPO / str(source["submodulePath"])
        if not (root / ".git").exists():
            warnings.append(
                f"curated source not initialized; skipped tree validation: {source_id}"
            )
            continue
        head = subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
        ).strip()
        if head != source["commit"]:
            fail(errors, f"curated checkout commit mismatch: {source_id}")
        if source.get("selection") == "one-month-star-velocity-round-2":
            tree = subprocess.check_output(
                ["git", "-C", str(root), "rev-parse", "HEAD^{tree}"], text=True
            ).strip()
            if tree != source["tree"]:
                fail(errors, f"curated checkout tree mismatch: {source_id}")
        for relative, record in records_by_source[source_id].items():
            skill_file = root / relative
            if not skill_file.is_file():
                fail(errors, f"curated catalog path missing: {source_id}/{relative}")
                continue
            blob_sha = subprocess.check_output(
                ["git", "-C", str(root), "hash-object", relative], text=True
            ).strip()
            if blob_sha != record["gitBlobSha"]:
                fail(errors, f"curated catalog blob mismatch: {source_id}/{relative}")
    return len(records)


def validate_navigation_and_bundle(
    all_catalogs: list[dict[str, object]],
    alias_paths: set[str],
    errors: list[str],
) -> None:
    """Keep additive category indexes and the 100-skill archive reproducible."""
    visible = [
        record
        for catalog in all_catalogs
        for record in catalog.get("skills", [])
        if record.get("tier") != "variant" and record.get("path") not in alias_paths
    ]
    by_category = Counter(str(record.get("category", "")) for record in visible)
    summary_path = REPO / "catalog/category-summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    raw_count = sum(len(catalog.get("skills", [])) for catalog in all_catalogs)
    if summary.get("formatVersion") != 1:
        fail(errors, "category summary has an unsupported format")
    if summary.get("rawCatalogEntries") != raw_count:
        fail(errors, "category summary raw count is stale")
    if summary.get("defaultVisibleEntries") != len(visible):
        fail(errors, "category summary visible count is stale")
    summary_categories = summary.get("categories", [])
    summary_by_id = {str(item.get("id", "")): item for item in summary_categories}
    if len(summary_by_id) != 9 or set(summary_by_id) != set(by_category):
        fail(errors, "category summary does not cover the nine catalog categories")
    for category, count in by_category.items():
        item = summary_by_id.get(category, {})
        if item.get("count") != count:
            fail(errors, f"category count is stale: {category}")
        readme = REPO / "categories" / category / "README.md"
        tsv = REPO / "categories" / category / "skills.tsv"
        if not readme.is_file() or not tsv.is_file():
            fail(errors, f"category navigation files are missing: {category}")
        elif len(tsv.read_text(encoding="utf-8").splitlines()) != count + 1:
            fail(errors, f"category TSV row count is stale: {category}")

    bundle_root = REPO / "bundles/newcomer-starter-pack"
    manifest = json.loads((bundle_root / "manifest.json").read_text(encoding="utf-8"))
    skills = manifest.get("skills", [])
    names = [str(item.get("name", "")) for item in skills]
    paths = [str(item.get("path", "")) for item in skills]
    if manifest.get("formatVersion") != 1 or manifest.get("count") != 100 or len(skills) != 100:
        fail(errors, "newcomer bundle must contain exactly 100 manifest entries")
    if "" in names or len(names) != len(set(names)):
        fail(errors, "newcomer bundle names are missing or duplicated")
    if "" in paths or len(paths) != len(set(paths)):
        fail(errors, "newcomer bundle paths are missing or duplicated")
    records_by_path = {
        str(record.get("path", "")): record
        for catalog in all_catalogs
        for record in catalog.get("skills", [])
    }
    for item in skills:
        path = str(item.get("path", ""))
        record = records_by_path.get(path)
        if record is None or record.get("tier") == "variant" or path in alias_paths:
            fail(errors, f"newcomer bundle entry is not default-visible: {path}")
            continue
        if not (REPO / path).is_file():
            fail(errors, f"newcomer bundle entry is not locally available: {path}")
        for key in ("name", "category", "tier", "sha256", "description"):
            if item.get(key) != record.get(key):
                fail(errors, f"newcomer bundle manifest is stale for {key}: {path}")
    if summary.get("starterBundleEntries") != 100:
        fail(errors, "category summary starter count is stale")
    starter_by_category = Counter(str(item.get("category", "")) for item in skills)
    for category, item in summary_by_id.items():
        if item.get("starterCount") != starter_by_category[category]:
            fail(errors, f"category starter count is stale: {category}")

    readme_text = (bundle_root / "README.md").read_text(encoding="utf-8")
    for phrase in ("技能吸收与调用报告", "明确调用", "完整应用", "不要一次吞下 100 项"):
        if phrase not in readme_text:
            fail(errors, f"newcomer instructions are missing required phrase: {phrase}")
    for name in names:
        if f"`{name}`" not in readme_text:
            fail(errors, f"newcomer README does not list skill: {name}")

    archive = bundle_root / "newcomer-starter-pack.tar.gz"
    checksum_line = (bundle_root / "SHA256SUMS").read_text(encoding="utf-8").strip()
    expected_checksum = checksum_line.split()[0] if checksum_line else ""
    if expected_checksum != sha256(archive):
        fail(errors, "newcomer archive checksum is stale")
    try:
        with tarfile.open(archive, "r:gz") as handle:
            archive_members = handle.getmembers()
            member_names = [member.name for member in archive_members]
            members = set(member_names)
            if len(members) != len(member_names):
                fail(errors, "newcomer archive contains duplicate member paths")
            for member in archive_members:
                member_path = Path(member.name)
                if member_path.is_absolute() or ".." in member_path.parts:
                    fail(errors, f"newcomer archive contains unsafe path: {member.name}")
                if member.issym() or member.islnk():
                    link_path = Path(member.linkname)
                    resolved_parts = (member_path.parent / link_path).parts
                    if link_path.is_absolute() or ".." in resolved_parts:
                        fail(errors, f"newcomer archive contains unsafe link: {member.name}")
    except (OSError, tarfile.TarError) as exc:
        fail(errors, f"newcomer archive is invalid: {exc}")
        members = set()
    required_members = {
        "newcomer-starter-pack/START_HERE.md",
        "newcomer-starter-pack/MANIFEST.json",
        "newcomer-starter-pack/LICENSE_AND_ATTRIBUTION.md",
        "newcomer-starter-pack/THIRD_PARTY_NOTICE.md",
    }
    required_members.update(
        f"newcomer-starter-pack/skills/{name}/SKILL.md" for name in names
    )
    missing_members = required_members - members
    if missing_members:
        fail(errors, f"newcomer archive is missing {len(missing_members)} required members")

    research_root = REPO / "bundles/research-workflow-kit"
    research_manifest = json.loads((research_root / "MANIFEST.json").read_text(encoding="utf-8"))
    research_skills = research_manifest.get("skills", [])
    research_ids = [str(item.get("id", "")) for item in research_skills]
    research_summary = research_manifest.get("summary", {})
    if research_manifest.get("formatVersion") != 1 or len(research_ids) != len(set(research_ids)):
        fail(errors, "research bundle manifest is malformed or contains duplicate IDs")
    if research_summary.get("entries") != len(research_skills):
        fail(errors, "research bundle manifest entry count is stale")
    if research_summary.get("bundledPayloads") != sum(bool(item.get("bundled")) for item in research_skills):
        fail(errors, "research bundle payload count is stale")
    if research_summary.get("metadataOnly") != sum(not item.get("bundled") for item in research_skills):
        fail(errors, "research bundle metadata-only count is stale")
    for item in research_skills:
        if not item.get("bundled") and not item.get("metadataOnlyReason"):
            fail(errors, f"research metadata-only entry lacks reason: {item.get('id')}")
    profile_files = list((research_root / "profiles").glob("*.json"))
    profile_names = set()
    for profile_file in profile_files:
        profile = json.loads(profile_file.read_text(encoding="utf-8"))
        profile_names.add(str(profile.get("name", "")))
        unknown = set(profile.get("skillIds", [])) - set(research_ids)
        if unknown:
            fail(errors, f"research profile has unknown skill IDs: {profile_file.name}")
    if research_summary.get("profiles") != len(profile_names):
        fail(errors, "research bundle profile count is stale")

    research_archive = research_root / "research-workflow-kit.tar.gz"
    checksum_line = (research_root / "SHA256SUMS").read_text(encoding="utf-8").strip()
    expected_checksum = checksum_line.split()[0] if checksum_line else ""
    if expected_checksum != sha256(research_archive):
        fail(errors, "research bundle archive checksum is stale")
    research_members: set[str] = set()
    try:
        with tarfile.open(research_archive, "r:gz") as handle:
            archive_members = handle.getmembers()
            member_names = [member.name for member in archive_members]
            research_members = set(member_names)
            if len(research_members) != len(member_names):
                fail(errors, "research bundle archive contains duplicate member paths")
            for member in archive_members:
                member_path = Path(member.name)
                if member_path.is_absolute() or ".." in member_path.parts:
                    fail(errors, f"research bundle archive contains unsafe path: {member.name}")
                if member.issym() or member.islnk():
                    fail(errors, f"research bundle archive contains a forbidden link: {member.name}")
    except (OSError, tarfile.TarError) as exc:
        fail(errors, f"research bundle archive is invalid: {exc}")
    for required in (
        "research-workflow-kit/MANIFEST.json",
        "research-workflow-kit/START_HERE.md",
        "research-workflow-kit/tools/research_kit.py",
        "research-workflow-kit/project-template/00-governance/research-charter.md",
    ):
        if required not in research_members:
            fail(errors, f"research bundle archive is missing required member: {required}")


def main() -> None:
    errors: list[str] = []
    warnings: list[str] = []

    for relative in REQUIRED:
        if not (REPO / relative).is_file():
            fail(errors, f"missing required file: {relative}")

    lock_path = REPO / "catalog/sources.lock.json"
    report_path = REPO / "catalog/import-report.json"
    catalog_path = REPO / "catalog/skills.json"
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)

    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    all_sources = (
        lock["aggregateSources"]
        + lock["directSources"]
        + lock.get("toolSources", [])
        + lock.get("researchSources", [])
        + lock.get("officialSources", [])
        + lock.get("curatedSources", [])
    )
    source_ids = [str(source.get("id", "")) for source in all_sources]
    if "" in source_ids or len(source_ids) != len(set(source_ids)):
        fail(errors, "source IDs are missing or duplicated across lock sections")
    for source in all_sources:
        if not re.fullmatch(r"[0-9a-f]{40}", source.get("commit", "")):
            fail(errors, f"invalid pinned commit for source {source.get('id')}")
    for source in lock["directSources"] + lock.get("toolSources", []):
        installed = REPO / source["installedAt"]
        if not installed.exists():
            fail(errors, f"source adapter is not installed: {source['id']} -> {installed}")

    gitlinks = {}
    listing = subprocess.check_output(
        ["git", "ls-files", "-s", "full-sources"], cwd=REPO, text=True
    )
    for line in listing.splitlines():
        mode, digest, _stage, path = line.split(maxsplit=3)
        if mode == "160000":
            gitlinks[path] = digest
    for source in all_sources:
        submodule_path = source.get("submodulePath")
        if not submodule_path:
            fail(errors, f"full-source submodule path missing from lock: {source['id']}")
        elif gitlinks.get(submodule_path) != source["commit"]:
            fail(errors, f"full-source gitlink mismatch: {source['id']} -> {submodule_path}")

    official_count = validate_official_catalog(lock, errors, warnings)
    curated_count = validate_curated_catalog(lock, errors, warnings)

    report = json.loads(report_path.read_text(encoding="utf-8"))
    local_nuwa_creations = report.get("localNuwaCreations", [])
    local_nuwa_names: list[str] = []
    local_nuwa_outputs: list[str] = []
    for record in local_nuwa_creations:
        name = str(record.get("name", ""))
        output_path = str(record.get("outputPath", ""))
        local_nuwa_names.append(name)
        local_nuwa_outputs.append(output_path)
        output = REPO / output_path
        if record.get("status") != "nuwa-deep-tier-original":
            fail(errors, f"local Nuwa creation has invalid status: {name}")
        if not output.is_file():
            fail(errors, f"local Nuwa creation is missing: {output_path}")
            continue
        if sha256(output) != record.get("sha256"):
            fail(errors, f"local Nuwa creation hash mismatch: {output_path}")
        if instructional_sha256(output) != record.get("instructionSha256"):
            fail(errors, f"local Nuwa creation instruction hash mismatch: {output_path}")
        validation_path = REPO / str(record.get("validationPath", ""))
        if not validation_path.is_file():
            fail(errors, f"local Nuwa validation record is missing: {name}")
        source_urls = record.get("sourceURLs", [])
        if not isinstance(source_urls, list) or len(source_urls) < 3 or not all(
            isinstance(url, str) and url.startswith("https://") for url in source_urls
        ):
            fail(errors, f"local Nuwa creation needs at least three HTTPS sources: {name}")
    if "" in local_nuwa_names or len(local_nuwa_names) != len(set(local_nuwa_names)):
        fail(errors, "local Nuwa creation names are missing or duplicated")
    if "" in local_nuwa_outputs or len(local_nuwa_outputs) != len(set(local_nuwa_outputs)):
        fail(errors, "local Nuwa creation output paths are missing or duplicated")

    report_records = report["canonical"] + report["variants"]
    instruction_identities: list[tuple[str, str]] = []
    for record in report_records:
        output = REPO / record["outputPath"]
        if not output.is_file():
            fail(errors, f"imported skill missing: {record['outputPath']}")
            continue
        if sha256(output) != record["sha256"]:
            fail(errors, f"imported skill hash mismatch: {record['outputPath']}")
        instruction_digest = instructional_sha256(output)
        if instruction_digest != record.get("instructionSha256"):
            fail(errors, f"imported instruction hash mismatch: {record['outputPath']}")
        instruction_identities.append((str(record["name"]), instruction_digest))
        if set(Path(record["sourcePath"]).parts) & {"test", "tests", "fixtures"}:
            fail(errors, f"test fixture was imported as a skill: {record['sourcePath']}")

    expected_report_count = report["counts"]["canonicalSkills"] + report["counts"]["variantSkills"]
    if len(report_records) != expected_report_count:
        fail(errors, "import report counts do not match its records")
    if len(instruction_identities) != len(set(instruction_identities)):
        fail(errors, "import report retains duplicate same-name instructional bodies")
    alias_groups = report.get("aliases", [])
    alias_count = sum(len(group.get("aliases", [])) for group in alias_groups)
    if report.get("formatVersion") != 2:
        fail(errors, "import report must use normalized-instruction format version 2")
    if report["counts"].get("instructionBodyGroups") != len(alias_groups):
        fail(errors, "import report instruction-body group count is stale")
    if report["counts"].get("retainedInstructionBodies") != len(report_records):
        fail(errors, "import report retained-body count is stale")
    if report["counts"].get("sourceAliases") != alias_count:
        fail(errors, "import report source-alias count is stale")
    if report["counts"].get("externalCanonicalGroups") != sum(
        "canonicalOutputPath" in group for group in alias_groups
    ):
        fail(errors, "import report external-canonical count is stale")
    if report["counts"].get("sourceCandidates") != len(alias_groups) + alias_count:
        fail(errors, "import report source candidates are not fully represented by alias groups")
    records_by_source_path = {str(record["sourcePath"]): record for record in report_records}
    group_identities: list[tuple[str, str]] = []
    for group in alias_groups:
        identity = (str(group.get("name", "")), str(group.get("instructionSha256", "")))
        group_identities.append(identity)
        canonical_record = records_by_source_path.get(str(group.get("canonicalSourcePath", "")))
        canonical_output = group.get("canonicalOutputPath")
        if canonical_output:
            output = REPO / str(canonical_output)
            if not output.is_file() or instructional_sha256(output) != identity[1]:
                fail(errors, f"import alias group has invalid maintained canonical: {identity[0]}")
        elif not canonical_record or canonical_record.get("instructionSha256") != identity[1]:
            fail(errors, f"import alias group has no retained canonical: {identity[0]}")
        for alias in group.get("aliases", []):
            reason = alias.get("reason")
            alias_digest = str(alias.get("sha256", ""))
            if reason not in {"byte-identical", "frontmatter-only"}:
                fail(errors, f"invalid compact alias reason: {alias.get('path')}")
            if not re.fullmatch(r"[0-9a-f]{64}", alias_digest):
                fail(errors, f"invalid compact alias hash: {alias.get('path')}")
            if reason == "byte-identical" and alias_digest != group.get("sha256"):
                fail(errors, f"misclassified byte-identical alias: {alias.get('path')}")
            if reason == "frontmatter-only" and alias_digest == group.get("sha256"):
                fail(errors, f"misclassified frontmatter-only alias: {alias.get('path')}")
    if len(group_identities) != len(set(group_identities)):
        fail(errors, "import report contains duplicate instruction-body groups")

    community_root = REPO / "skills/community"
    for path in community_root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.casefold() in COMMUNITY_PRUNED_EXTENSIONS:
            fail(errors, f"pruned media/archive present in community import: {path.relative_to(REPO)}")
        if path.stat().st_size > MAX_COMMUNITY_FILE_BYTES:
            fail(errors, f"oversized community file: {path.relative_to(REPO)}")

    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    research_catalog = json.loads((REPO / "catalog/research-skills.json").read_text(encoding="utf-8"))
    official_catalog = json.loads((REPO / "catalog/official-skills.json").read_text(encoding="utf-8"))
    curated_catalog = json.loads((REPO / "catalog/curated-skills.json").read_text(encoding="utf-8"))
    all_catalogs = [catalog, research_catalog, official_catalog, curated_catalog]
    overlap_alias_count = validate_overlap_policy(all_catalogs, errors)
    overlap_policy = json.loads(
        (REPO / "catalog/overlap-policy.json").read_text(encoding="utf-8")
    )
    alias_paths = {str(alias["path"]) for alias in overlap_policy["aliases"]}
    validate_navigation_and_bundle(all_catalogs, alias_paths, errors)
    raw_catalog_entries = sum(len(item.get("skills", [])) for item in all_catalogs)
    default_visible_entries = sum(
        record.get("tier") != "variant" and record.get("path") not in alias_paths
        for item in all_catalogs
        for record in item.get("skills", [])
    )
    expected_overlap_summary = {
        "catalog": "catalog/overlap-policy.json",
        "rawCatalogEntries": raw_catalog_entries,
        "defaultVisibleEntries": default_visible_entries,
        "suppressedAliases": overlap_alias_count,
    }
    if lock.get("overlapPolicy") != expected_overlap_summary:
        fail(errors, "source lock overlap summary is stale")
    expected_research = sum(source["skillCount"] for source in lock.get("researchSources", []))
    if research_catalog.get("count") != expected_research or len(research_catalog.get("skills", [])) != expected_research:
        fail(errors, f"research catalog count mismatch: expected={expected_research}")
    research_by_id = {source["id"]: source for source in lock.get("researchSources", [])}
    for record in research_catalog.get("skills", []):
        source = research_by_id.get(record.get("sourceId"))
        if not source or record.get("sourceCommit") != source["commit"]:
            fail(errors, f"research catalog source mismatch: {record.get('path')}")
        elif not str(record.get("path", "")).startswith(source["submodulePath"] + "/"):
            fail(errors, f"research catalog path mismatch: {record.get('path')}")

    discovered = [
        path for path in REPO.rglob("SKILL.md")
        if ".git" not in path.relative_to(REPO).parts
        and "node_modules" not in path.relative_to(REPO).parts
        and path.relative_to(REPO).parts[:1] != ("full-sources",)
    ]
    if catalog["count"] != len(catalog["skills"]) or catalog["count"] != len(discovered):
        fail(errors, f"catalog is stale: catalog={catalog['count']} discovered={len(discovered)}")
    for record in catalog["skills"]:
        path = REPO / record["path"]
        if not path.is_file() or sha256(path) != record["sha256"]:
            fail(errors, f"catalog hash/path mismatch: {record['path']}")

    missing_licenses = [name for name, value in report["licenses"].items() if value is None]
    if missing_licenses:
        warnings.append(
            "aggregate collections without a discoverable collection-level license: "
            + ", ".join(sorted(missing_licenses))
        )

    files = [
        path for path in REPO.rglob("*")
        if path.is_file()
        and ".git" not in path.relative_to(REPO).parts
        and "node_modules" not in path.relative_to(REPO).parts
        and path.relative_to(REPO).parts[:1] != ("full-sources",)
    ]
    total_bytes = sum(path.stat().st_size for path in files)
    approved_archive_bytes = 0
    for relative, maximum in APPROVED_BUNDLE_ARCHIVES.items():
        archive = REPO / relative
        if not archive.is_file():
            fail(errors, f"approved bundle archive is missing: {relative}")
            continue
        size = archive.stat().st_size
        approved_archive_bytes += size
        if size > maximum:
            fail(errors, f"approved bundle archive exceeded cap: {relative}: {size} > {maximum}")
    policy_bytes = total_bytes - approved_archive_bytes
    if len(files) > MAX_FILES:
        fail(errors, f"repository file policy exceeded: {len(files)} > {MAX_FILES}")
    if policy_bytes > MAX_BYTES:
        fail(errors, f"repository byte policy exceeded excluding approved archives: {policy_bytes} > {MAX_BYTES}")

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    print(
        f"Validated {len(discovered)} compact skills, {official_count} official-source skills, "
        f"{curated_count} curated-source skills, {len(report_records)} imported bodies, "
        f"{overlap_alias_count} searchable aliases, {len(files)} files, "
        f"{total_bytes / (1024 * 1024):.1f} MiB."
    )
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
