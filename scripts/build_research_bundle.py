#!/usr/bin/env python3
"""Build the portable, human-in-the-loop research workflow skill archive."""

from __future__ import annotations

import gzip
import hashlib
import json
import os
import re
import shutil
import subprocess
import tarfile
import tempfile
from collections import Counter
from pathlib import Path, PurePosixPath

from catalog_aliases import annotate_alias, is_alias, load_alias_index

REPO = Path(__file__).resolve().parents[1]
BUNDLE = REPO / "bundles" / "research-workflow-kit"
ARCHIVE = BUNDLE / "research-workflow-kit.tar.gz"
VERSION = "2026.08.16"
BLOCKED_REDISTRIBUTION = {
    "hamelnb": "No explicit upstream license was found at the pinned commit; metadata retained without payload.",
    "paper-craft-skills": "Upstream README claims MIT but the pinned source has no standalone license file; metadata retained without payload.",
}
STATIC_FILES = (
    "README.md",
    "START_HERE.md",
    "INSTALL.md",
    "WORKFLOW.md",
    "ETHICS.md",
    "PLATFORM_COMPATIBILITY.md",
    "VALIDATION.md",
    "LICENSE_AND_ATTRIBUTION.md",
)
SELF_SKILLS = (
    ("research-workflow-kit", "research-workflow-orchestrator", "skills/research-workflow-kit/research-workflow-orchestrator"),
    ("research-workflow-kit", "research-question-protocol", "skills/research-workflow-kit/research-question-protocol"),
    ("research-workflow-kit", "systematic-evidence-synthesis", "skills/research-workflow-kit/systematic-evidence-synthesis"),
    ("research-workflow-kit", "qualitative-mixed-methods", "skills/research-workflow-kit/qualitative-mixed-methods"),
    ("research-workflow-kit", "reproducible-research-analysis", "skills/research-workflow-kit/reproducible-research-analysis"),
    ("research-workflow-kit", "academic-integrity-ai-disclosure", "skills/research-workflow-kit/academic-integrity-ai-disclosure"),
    ("skill-repository", "research-expert-system", "skills/research-expert-system"),
    ("skill-repository", "ai-research-senpai-council", "skills/community/nuwa-distilled/ai-research-senpai-council"),
)
OFFICIAL_SKILLS = (
    ("jupyter-notebook", "skills/.curated/jupyter-notebook"),
    ("pdf", "skills/.curated/pdf"),
    ("notion-research-documentation", "skills/.curated/notion-research-documentation"),
)
IGNORE_NAMES = {
    ".git",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "__pycache__",
    "node_modules",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def source_head(path: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "HEAD"],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.strip()


def frontmatter_description(skill_file: Path, fallback: str) -> str:
    text = skill_file.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return fallback
    block = text.split("---", 2)[1]
    lines = block.splitlines()
    for index, line in enumerate(lines):
        match = re.match(r"^(\s*)description:\s*(.*?)\s*$", line)
        if not match:
            continue
        value = match.group(2).strip()
        if value in {"|", "|-", "|+", ">", ">-", ">+"}:
            base_indent = len(match.group(1))
            body: list[str] = []
            for following in lines[index + 1 :]:
                if following.strip() and len(following) - len(following.lstrip()) <= base_indent:
                    break
                if following.strip():
                    body.append(following.strip())
            value = " ".join(body)
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        return value or fallback
    return fallback


def safe_rel(path: Path, root: Path) -> Path:
    rel = path.resolve().relative_to(root.resolve())
    if ".." in rel.parts:
        raise RuntimeError(f"unsafe path: {path}")
    return rel


def ignore_copy(_: str, names: list[str]) -> set[str]:
    return {name for name in names if name in IGNORE_NAMES or name.endswith((".pyc", ".pyo"))}


def copy_package(source: Path, destination: Path) -> None:
    if not source.is_dir() or not (source / "SKILL.md").is_file():
        raise RuntimeError(f"invalid skill package: {source}")
    for path in source.rglob("*"):
        if path.is_symlink():
            raise RuntimeError(f"portable payload cannot contain symlink: {path}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, destination, ignore=ignore_copy)


def declaration_files(root: Path, kind: str) -> list[str]:
    dependency_names = {
        "requirements.txt",
        "pyproject.toml",
        "package.json",
        "environment.yml",
        "environment.yaml",
        "setup.py",
        "setup.cfg",
        "Pipfile",
        "poetry.lock",
        "uv.lock",
        "Cargo.toml",
        "Dockerfile",
        "compose.yml",
        "compose.yaml",
    }
    platform_names = {"openai.yaml", "plugin.json", "marketplace.json", ".mcp.json"}
    selected = dependency_names if kind == "dependency" else platform_names
    result = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        name = path.name
        matches = name in selected
        if kind == "dependency" and name.startswith("requirements") and name.endswith(".txt"):
            matches = True
        if matches:
            result.append(path.relative_to(root).as_posix())
    return sorted(result)


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
        if path.is_symlink():
            raise RuntimeError(f"unexpected symlink in staged payload: {path}")
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


def skill_id(source_id: str, package_rel: Path) -> str:
    return f"{source_id}::{package_rel.as_posix()}"


def compatibility_for(source_id: str) -> str:
    if source_id == "research-workflow-kit":
        return "cross-platform-guidance"
    if source_id == "skill-repository":
        return "cross-platform-guidance"
    if source_id in {"academic-research-skills-codex", "openai-skills"}:
        return "codex-native-guidance-portable"
    if source_id in {"aris", "hermes-agent"}:
        return "source-specific-runtime"
    if source_id in {"ai-research-skills", "scientific-agent-skills", "nature-skills"}:
        return "domain-library-guidance"
    return "cross-platform-guidance"


def entry_record(
    *,
    source_id: str,
    name: str,
    description: str,
    source_repository: str,
    source_commit: str | None,
    source_license: str,
    source_path: str,
    package_rel: Path,
    payload_path: Path | None,
    package_sha256: str | None,
    bundled: bool,
    dependency_files: list[str] | None = None,
    platform_files: list[str] | None = None,
    metadata_reason: str | None = None,
    alias_of: str | None = None,
) -> dict:
    record = {
        "id": skill_id(source_id, package_rel),
        "name": name,
        "description": description,
        "sourceId": source_id,
        "sourceRepository": source_repository,
        "sourceCommit": source_commit,
        "sourceLicense": source_license,
        "sourcePath": source_path,
        "packageRelative": package_rel.as_posix(),
        "entryRelative": "SKILL.md",
        "bundled": bundled,
        "payloadPath": payload_path.as_posix() if payload_path else None,
        "packageSha256": package_sha256,
        "compatibility": "metadata-only" if not bundled else compatibility_for(source_id),
        "platformRequirements": {
            "classification": "metadata-only" if not bundled else compatibility_for(source_id),
            "declarationFiles": platform_files or [],
            "universalCommandInterface": False,
            "note": "Source-specific commands are examples, not guaranteed host commands; inspect the selected SKILL and current platform before invocation.",
        },
        "dependencies": {
            "declarationFiles": dependency_files or [],
            "autoInstalled": False,
            "status": (
                "metadata-only; payload and dependency declarations are not redistributed"
                if not bundled
                else (
                    "machine-readable declaration files preserved at the exact relative paths listed"
                    if dependency_files
                    else "no recognized machine-readable dependency file in this package; inspect SKILL.md for optional tools/services"
                )
            ),
        },
        "dependencyVerification": (
            "self-contained guidance; inspect selected workflow for optional tools"
            if source_id == "research-workflow-kit"
            else "upstream declarations preserved; runtime dependencies are not auto-installed and must be verified before activation"
        ),
        "securityReview": (
            "maintained human-in-the-loop workflow"
            if source_id == "research-workflow-kit"
            else "pinned source and package boundary verified; runtime behavior not exhaustively audited"
        ),
        "profiles": [],
    }
    if metadata_reason:
        record["metadataOnlyReason"] = metadata_reason
    if alias_of:
        record["aliasOfSourcePath"] = alias_of
    return record


def stage_upstream(stage: Path, source_locks: dict[str, dict]) -> tuple[list[dict], int]:
    catalog = load_json(REPO / "catalog" / "research-skills.json")["skills"]
    alias_index = load_alias_index()
    records: list[dict] = []
    aliases = 0
    for raw in catalog:
        item = annotate_alias(raw, alias_index)
        source_id = str(item["sourceId"])
        source = source_locks[source_id]
        source_root = REPO / source["submodulePath"]
        if not (source_root / ".git").exists():
            raise RuntimeError(
                f"research source is not initialized: {source_id}; run git submodule update --init --recursive full-sources/research"
            )
        actual_head = source_head(source_root)
        if actual_head != source["commit"]:
            raise RuntimeError(f"source pin mismatch for {source_id}: {actual_head} != {source['commit']}")
        skill_file = REPO / item["path"]
        package = skill_file.parent
        package_rel = package.relative_to(source_root)
        fallback = str(item.get("description", name_from_package(package_rel)))
        description = frontmatter_description(skill_file, fallback)
        payload_rel: Path | None = None
        package_sha: str | None = None
        dependency_files: list[str] = []
        platform_files: list[str] = []
        bundled = True
        reason = None
        alias_of = None
        if is_alias(item):
            aliases += 1
            bundled = False
            alias_of = str(item.get("aliasOf", ""))
            reason = f"Exact duplicate alias suppressed ({item.get('aliasReason', 'alias')}; {item.get('aliasEvidence', 'verified equivalence')})."
        elif source_id in BLOCKED_REDISTRIBUTION:
            bundled = False
            reason = BLOCKED_REDISTRIBUTION[source_id]
        else:
            payload_rel = Path("vault") / source_id / package_rel
            destination = stage / payload_rel
            copy_package(package, destination)
            package_sha = tree_hash(destination)
            dependency_files = declaration_files(destination, "dependency")
            platform_files = declaration_files(destination, "platform")
        records.append(
            entry_record(
                source_id=source_id,
                name=str(item["name"]),
                description=description,
                source_repository=source["repository"],
                source_commit=source["commit"],
                source_license=source["license"],
                source_path=str(item["path"]),
                package_rel=package_rel,
                payload_path=payload_rel,
                package_sha256=package_sha,
                bundled=bundled,
                dependency_files=dependency_files,
                platform_files=platform_files,
                metadata_reason=reason,
                alias_of=alias_of,
            )
        )
    return records, aliases


def name_from_package(package_rel: Path) -> str:
    return package_rel.name.replace("_", "-")


def stage_additional(stage: Path, official_lock: dict) -> list[dict]:
    records: list[dict] = []
    repo_url = "https://github.com/sunccchengze/-SKILL-"
    for source_id, name, source_path_text in SELF_SKILLS:
        package = REPO / source_path_text
        payload_rel = Path("vault") / source_id / name
        destination = stage / payload_rel
        copy_package(package, destination)
        adaptation = None
        if name == "research-expert-system":
            # The repository skill links to ../../guides/RESEARCH.md. Rebase that
            # maintained local link so an individually installed package remains complete.
            references = destination / "references"
            references.mkdir()
            shutil.copy2(REPO / "guides" / "RESEARCH.md", references / "RESEARCH.md")
            skill_text = (destination / "SKILL.md").read_text(encoding="utf-8")
            skill_text = skill_text.replace(
                "[`../../guides/RESEARCH.md`](../../guides/RESEARCH.md)",
                "[`references/RESEARCH.md`](references/RESEARCH.md)",
            ).replace("`guides/RESEARCH.md`", "`references/RESEARCH.md`")
            (destination / "SKILL.md").write_text(skill_text, encoding="utf-8")
            adaptation = "Rebased maintained guide link and bundled guides/RESEARCH.md as references/RESEARCH.md for standalone installation."
        record = entry_record(
            source_id=source_id,
            name=name,
            description=frontmatter_description(package / "SKILL.md", name),
            source_repository=repo_url,
            source_commit=None,
            source_license="NOASSERTION (repository has no root license)",
            source_path=source_path_text + "/SKILL.md",
            package_rel=Path(name),
            payload_path=payload_rel,
            package_sha256=tree_hash(destination),
            bundled=True,
            dependency_files=declaration_files(destination, "dependency"),
            platform_files=declaration_files(destination, "platform"),
        )
        if adaptation:
            record["bundleAdaptation"] = adaptation
        records.append(record)

    source_id = "openai-skills"
    source_root = REPO / official_lock["submodulePath"]
    if not (source_root / ".git").exists():
        raise RuntimeError(
            "official OpenAI source is not initialized; run git submodule update --init full-sources/official/openai-skills"
        )
    actual_head = source_head(source_root)
    if actual_head != official_lock["commit"]:
        raise RuntimeError(f"source pin mismatch for openai-skills: {actual_head} != {official_lock['commit']}")
    for name, package_text in OFFICIAL_SKILLS:
        package_rel = Path(package_text)
        package = source_root / package_rel
        payload_rel = Path("vault") / source_id / package_rel
        destination = stage / payload_rel
        copy_package(package, destination)
        records.append(
            entry_record(
                source_id=source_id,
                name=name,
                description=frontmatter_description(package / "SKILL.md", name),
                source_repository=official_lock["repository"],
                source_commit=official_lock["commit"],
                source_license="per-skill (bundled LICENSE.txt)",
                source_path=f"{official_lock['submodulePath']}/{package_text}/SKILL.md",
                package_rel=package_rel,
                payload_path=payload_rel,
                package_sha256=tree_hash(destination),
                bundled=True,
                dependency_files=declaration_files(destination, "dependency"),
                platform_files=declaration_files(destination, "platform"),
            )
        )
    return records


def copy_licenses(stage: Path, source_locks: dict[str, dict]) -> None:
    for source_id, source in source_locks.items():
        source_root = REPO / source["submodulePath"]
        destination = stage / "licenses" / source_id
        copied = False
        for path in sorted(source_root.iterdir()):
            lower = path.name.casefold()
            if path.is_file() and lower.startswith(("license", "notice", "copying")):
                destination.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, destination / path.name)
                copied = True
        if not copied:
            destination.mkdir(parents=True, exist_ok=True)
            (destination / "NO_LICENSE_FILE.txt").write_text(
                BLOCKED_REDISTRIBUTION.get(
                    source_id,
                    f"No source-level license file was copied. Catalog declaration: {source['license']}.",
                )
                + "\n",
                encoding="utf-8",
            )


def find_id(records: list[dict], source_id: str, name: str, path_contains: str | None = None) -> str:
    matches = [
        item
        for item in records
        if item["sourceId"] == source_id
        and item["name"] == name
        and item["bundled"]
        and (path_contains is None or path_contains in item["sourcePath"])
    ]
    if len(matches) != 1:
        raise RuntimeError(f"expected one profile skill for {source_id}/{name}/{path_contains}, found {len(matches)}")
    return matches[0]["id"]


def build_profiles(records: list[dict]) -> list[dict]:
    f = lambda source, name, contains=None: find_id(records, source, name, contains)
    custom = [
        f("research-workflow-kit", "research-workflow-orchestrator"),
        f("research-workflow-kit", "research-question-protocol"),
        f("research-workflow-kit", "systematic-evidence-synthesis"),
        f("research-workflow-kit", "qualitative-mixed-methods"),
        f("research-workflow-kit", "reproducible-research-analysis"),
        f("research-workflow-kit", "academic-integrity-ai-disclosure"),
    ]
    scientific_core = [
        f("scientific-agent-skills", name)
        for name in (
            "paper-lookup",
            "citation-management",
            "literature-review",
            "experimental-design",
            "statistical-analysis",
            "scientific-writing",
            "peer-review",
            "pyzotero",
            "exploratory-data-analysis",
        )
    ]
    core = custom + scientific_core + [
        f("openai-skills", "jupyter-notebook"),
        f("openai-skills", "pdf"),
    ]
    literature = [custom[0], custom[1], custom[2], custom[5]] + scientific_core[:3] + [
        f("scientific-agent-skills", "pyzotero"),
        f("nature-skills", "nature-academic-search"),
        f("nature-skills", "nature-literature-pipeline"),
        f("nature-skills", "nature-paper-card"),
        f("nature-skills", "nature-reader"),
        f("nature-skills", "nature-ref-verifier"),
        f("nature-skills", "nature-downloader"),
        f("openai-skills", "pdf"),
        f("openai-skills", "notion-research-documentation"),
    ]
    quantitative = [custom[0], custom[1], custom[4], custom[5]] + [
        f("scientific-agent-skills", name)
        for name in (
            "experimental-design",
            "statistical-analysis",
            "statistical-power",
            "exploratory-data-analysis",
            "scientific-visualization",
            "matplotlib",
            "seaborn",
            "statsmodels",
            "pymc",
            "uncertainty-and-units",
        )
    ] + [f("openai-skills", "jupyter-notebook")]
    qualitative = [custom[0], custom[1], custom[2], custom[3], custom[5]] + [
        f("scientific-agent-skills", name)
        for name in ("literature-review", "citation-management", "scientific-writing", "peer-review")
    ] + [f("openai-skills", "pdf")]
    writing = [custom[0], custom[2], custom[4], custom[5]] + [
        f("scientific-agent-skills", name)
        for name in ("scientific-writing", "peer-review", "citation-management", "venue-templates", "scientific-visualization")
    ] + [
        f("nature-skills", name)
        for name in (
            "nature-writing",
            "nature-polishing",
            "nature-reviewer",
            "nature-citation",
            "nature-statistics",
            "nature-figure",
            "nature-data",
        )
    ] + [
        f("paperspine", "paper-spine", "dist/codex"),
        f("research-paper-writing-skills", "research-paper-writing"),
    ]
    ml = [custom[0], custom[1], custom[4], custom[5]] + [
        item["id"] for item in records if item["bundled"] and item["sourceId"] in {"ai-research-skills", "aris"}
    ]
    life = [custom[0], custom[1], custom[4], custom[5]] + [
        item["id"] for item in records if item["bundled"] and item["sourceId"] == "scientific-agent-skills"
    ]
    ars = [custom[0], custom[1], custom[2], custom[5]] + [
        item["id"]
        for item in records
        if item["bundled"] and item["sourceId"] in {"academic-research-skills", "academic-research-skills-codex"}
    ]
    everything = [item["id"] for item in records if item["bundled"]]

    def unique(items: list[str]) -> list[str]:
        return list(dict.fromkeys(items))

    return [
        {"name": "core", "description": "Permissive/self-contained cross-disciplinary starting set; default recommendation.", "risk": "review each selected SKILL before use", "skillIds": unique(core)},
        {"name": "literature-evidence", "description": "Search, lawful full text, PDF, citation, evidence extraction and synthesis.", "risk": "database/API access and citation support still require verification", "skillIds": unique(literature)},
        {"name": "quantitative", "description": "Design, power, statistics, Notebook execution, uncertainty and visualization.", "risk": "methods must match the design; run code and inspect assumptions", "skillIds": unique(quantitative)},
        {"name": "qualitative-mixed", "description": "Authorized, de-identified qualitative and mixed-methods research.", "risk": "human interpretation, consent, privacy and ethics approval required", "skillIds": unique(qualitative)},
        {"name": "writing-publication", "description": "Evidence-bounded manuscript, figures, review, revision and disclosure.", "risk": "not a ghostwriting or automatic submission workflow", "skillIds": unique(writing)},
        {"name": "ml-experiment", "description": "Large AI/ML engineering and bounded autonomous experiment collection.", "risk": "very large; source-specific runtimes, explicit budgets and human gates required", "skillIds": unique(ml)},
        {"name": "life-science-vault", "description": "Large scientific/domain library with biology, medicine, chemistry, materials and computation.", "risk": "research only; domain expertise, safety review and package dependencies required", "skillIds": unique(life)},
        {"name": "ars-noncommercial", "description": "Academic Research Skills and Codex adapter under CC BY-NC 4.0.", "risk": "non-commercial license; adapter commands require compatible Codex setup", "skillIds": unique(ars)},
        {"name": "everything", "description": "Every redistributable payload in the offline vault.", "risk": "discovery/archive only; never load or activate all skills at once", "skillIds": unique(everything)},
    ]


def assign_install_names_and_profiles(records: list[dict], profiles: list[dict]) -> None:
    bundled = [item for item in records if item["bundled"]]
    name_counts = Counter(item["name"] for item in bundled)
    source_name_counts = Counter((item["sourceId"], item["name"]) for item in bundled)
    for item in records:
        if not item["bundled"]:
            item["installName"] = None
            continue
        if name_counts[item["name"]] == 1:
            install_name = item["name"]
        elif source_name_counts[(item["sourceId"], item["name"])] == 1:
            install_name = f"{item['sourceId']}--{item['name']}"
        else:
            suffix = hashlib.sha256(item["id"].encode("utf-8")).hexdigest()[:8]
            install_name = f"{item['sourceId']}--{item['name']}--{suffix}"
        item["installName"] = re.sub(r"[^a-zA-Z0-9._-]+", "-", install_name)
    membership: dict[str, list[str]] = {item["id"]: [] for item in records}
    for profile in profiles:
        for identifier in profile["skillIds"]:
            membership[identifier].append(profile["name"])
    for item in records:
        item["profiles"] = membership[item["id"]]
        item["defaultActivation"] = "core" in item["profiles"]


def write_manifest(stage: Path, records: list[dict], profiles: list[dict], aliases: int, sources: dict[str, dict]) -> dict:
    records.sort(key=lambda item: (item["sourceId"], item["packageRelative"], item["id"]))
    manifest = {
        "formatVersion": 1,
        "name": "research-workflow-kit",
        "version": VERSION,
        "generatedAt": "2026-08-16T00:00:00+08:00",
        "language": "zh-CN-default-with-original-source-language",
        "policy": {
            "humanInTheLoop": True,
            "normativeFormats": ["Markdown", "CSV/TSV", "JSONL", "BibTeX/RIS", "Jupyter Notebook"],
            "neverAutomatic": [
                "change the primary research question",
                "process unauthorized sensitive data",
                "fabricate data or citations",
                "purchase resources",
                "contact third parties",
                "publish or submit a manuscript",
            ],
            "fullVaultActivation": "forbidden; search metadata and load only the current stage's minimal complementary set",
        },
        "summary": {
            "entries": len(records),
            "bundledPayloads": sum(item["bundled"] for item in records),
            "metadataOnly": sum(not item["bundled"] for item in records),
            "exactAliasesSuppressed": aliases,
            "profiles": len(profiles),
        },
        "sourcePins": [
            {
                key: source.get(key)
                for key in ("id", "repository", "commit", "license", "submodulePath", "role")
            }
            for source in sources.values()
        ],
        "skills": records,
    }
    text = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    (stage / "MANIFEST.json").write_text(text, encoding="utf-8")
    (BUNDLE / "MANIFEST.json").write_text(text, encoding="utf-8")
    profiles_dir = BUNDLE / "profiles"
    if profiles_dir.exists():
        shutil.rmtree(profiles_dir)
    profiles_dir.mkdir(parents=True)
    stage_profiles = stage / "profiles"
    stage_profiles.mkdir(parents=True)
    for profile in profiles:
        profile_text = json.dumps(profile, ensure_ascii=False, indent=2) + "\n"
        (profiles_dir / f"{profile['name']}.json").write_text(profile_text, encoding="utf-8")
        (stage_profiles / f"{profile['name']}.json").write_text(profile_text, encoding="utf-8")
    return manifest


def copy_static(stage: Path) -> None:
    for name in STATIC_FILES:
        shutil.copy2(BUNDLE / name, stage / name)
    shutil.copytree(BUNDLE / "tools", stage / "tools", ignore=ignore_copy)
    shutil.copytree(BUNDLE / "project-template", stage / "project-template", ignore=ignore_copy)


def deterministic_tar(source_root: Path, archive: Path) -> None:
    archive.parent.mkdir(parents=True, exist_ok=True)
    temp_archive = archive.with_suffix(archive.suffix + ".tmp")
    with temp_archive.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, compresslevel=9, mtime=0) as gz:
            with tarfile.open(fileobj=gz, mode="w", format=tarfile.PAX_FORMAT) as tar:
                paths = [source_root] + sorted(source_root.rglob("*"), key=lambda p: p.as_posix())
                for path in paths:
                    arcname = Path("research-workflow-kit") / path.relative_to(source_root)
                    info = tar.gettarinfo(str(path), arcname.as_posix())
                    info.uid = 0
                    info.gid = 0
                    info.uname = "root"
                    info.gname = "root"
                    info.mtime = 0
                    if path.is_file():
                        with path.open("rb") as handle:
                            tar.addfile(info, handle)
                    else:
                        tar.addfile(info)
    temp_archive.replace(archive)


def main() -> None:
    lock = load_json(REPO / "catalog" / "sources.lock.json")
    research_sources = {source["id"]: source for source in lock["researchSources"]}
    official = next(source for source in lock["officialSources"] if source["id"] == "openai-skills")
    with tempfile.TemporaryDirectory(prefix="research-kit-") as temporary:
        stage = Path(temporary) / "research-workflow-kit"
        stage.mkdir(parents=True)
        copy_static(stage)
        records, aliases = stage_upstream(stage, research_sources)
        records.extend(stage_additional(stage, official))
        copy_licenses(stage, research_sources)
        profiles = build_profiles(records)
        assign_install_names_and_profiles(records, profiles)
        manifest_sources = {**research_sources, official["id"]: official}
        manifest = write_manifest(stage, records, profiles, aliases, manifest_sources)
        deterministic_tar(stage, ARCHIVE)
    archive_sha = hashlib.sha256(ARCHIVE.read_bytes()).hexdigest()
    (BUNDLE / "SHA256SUMS").write_text(
        f"{archive_sha}  {ARCHIVE.name}\n", encoding="utf-8"
    )
    summary = manifest["summary"]
    print(
        f"built {ARCHIVE.relative_to(REPO)}: {ARCHIVE.stat().st_size / 1024 / 1024:.2f} MiB, "
        f"{summary['entries']} entries, {summary['bundledPayloads']} payloads, "
        f"{summary['metadataOnly']} metadata-only, sha256={archive_sha}"
    )


if __name__ == "__main__":
    main()
