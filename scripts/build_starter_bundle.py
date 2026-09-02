#!/usr/bin/env python3
"""Validate and reproducibly package the 100-skill newcomer starter bundle."""

from __future__ import annotations

import gzip
import hashlib
import json
import os
import shutil
import tarfile
import tempfile
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BUNDLE = REPO / "bundles/newcomer-starter-pack"
MANIFEST = BUNDLE / "manifest.json"
ARCHIVE = BUNDLE / "newcomer-starter-pack.tar.gz"
CHECKSUM = BUNDLE / "SHA256SUMS"
CATALOGS = (
    "catalog/skills.json",
    "catalog/official-skills.json",
    "catalog/research-skills.json",
    "catalog/curated-skills.json",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def clean(value: object, limit: int | None = None) -> str:
    text = " ".join(str(value or "").replace("|", "\\|").split())
    if limit and len(text) > limit:
        return text[: limit - 1].rstrip() + "…"
    return text


def load_records() -> dict[str, dict[str, object]]:
    records = {}
    for relative in CATALOGS:
        for record in json.loads((REPO / relative).read_text(encoding="utf-8"))["skills"]:
            records[str(record["path"])] = record
    return records


def validate_manifest(manifest: dict[str, object]) -> list[dict[str, object]]:
    records = load_records()
    skills = list(manifest.get("skills", []))
    errors = []
    if manifest.get("formatVersion") != 1:
        errors.append("unsupported manifest format")
    if manifest.get("count") != 100 or len(skills) != 100:
        errors.append(f"starter bundle must contain exactly 100 skills, found {len(skills)}")
    names = [str(item.get("name", "")) for item in skills]
    paths = [str(item.get("path", "")) for item in skills]
    if "" in names or len(names) != len(set(names)):
        errors.append("starter skill names are empty or duplicated")
    if "" in paths or len(paths) != len(set(paths)):
        errors.append("starter skill paths are empty or duplicated")
    if [item.get("ordinal") for item in skills] != list(range(1, len(skills) + 1)):
        errors.append("starter ordinals are not contiguous")

    for item in skills:
        path = str(item.get("path", ""))
        record = records.get(path)
        source = REPO / path
        if record is None:
            errors.append(f"catalog entry is missing: {path}")
            continue
        if not source.is_file():
            errors.append(f"starter source is not locally available: {path}")
            continue
        for key in ("name", "category", "tier", "sha256", "description"):
            if item.get(key) != record.get(key):
                errors.append(f"manifest {key} is stale: {path}")
        if sha256(source) != item.get("sha256"):
            errors.append(f"starter source hash changed: {path}")
    if errors:
        raise SystemExit("\n".join(f"ERROR: {error}" for error in errors))
    return skills


def build_readme(
    manifest: dict[str, object], skills: list[dict[str, object]], *, packaged: bool = False
) -> str:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for item in skills:
        grouped[str(item["group"])].append(item)

    lines = [
        "# 🎁 Agent 新手大礼包：100 项核心工作技能",
        "",
        "这是一个可以直接解压、离线阅读的基础组合。它收录 **恰好 100 项**本仓库本地可用的核心技能，覆盖技能发现、计划、实现、测试、研究、写作、设计、安全、产品与交付验证。机器清单见 [`manifest.json`](manifest.json)，可下载包为 [`newcomer-starter-pack.tar.gz`](newcomer-starter-pack.tar.gz)。",
        "",
        "> **强烈建议：频繁检索、明确点名、完整应用。** 对每项非琐碎任务，都应主动寻找匹配技能，并在工作记录中明确写出本轮调用了哪些技能、分别用在哪一步、如何按其完整流程执行、取得了什么验证证据。不要只说“参考过”，也不要只列名字而不落实。",
        "",
        "> **但不要一次吞下 100 项。** “完整应用”指完整执行**本轮选中技能**的关键步骤，不是把全部技能同时塞进上下文。通常使用 1 个主技能，并按需增加研究、制作、审查各 1 个，合计通常不超过 4 个。需要换阶段时再重新搜索和换组。",
        "",
        "## 解压与使用",
        "",
        "```bash",
        "tar -xzf bundles/newcomer-starter-pack/newcomer-starter-pack.tar.gz",
        "cd newcomer-starter-pack",
        "less START_HERE.md",
        "```",
        "",
        "解压目录中的 `skills/` 是 100 个独立包；`MANIFEST.json` 记录顺序、分类、来源路径、描述和 SHA-256，`LICENSE_AND_ATTRIBUTION.md` 与 `THIRD_PARTY_NOTICE.md` 说明许可核验边界。把该目录配置为 Agent 的技能搜索目录，或只复制当前任务需要的包。",
        "",
        "## 新会话必须先做的吸收报告",
        "",
        "把以下要求原样交给新会话中的工作者：",
        "",
        "```text",
        "请先阅读 START_HERE.md 与 MANIFEST.json，只扫描 100 项技能的元数据，不要一次加载全部正文。",
        "在开始实质工作前，请提交“技能吸收与调用报告”，必须回答：",
        "1. 你如何消化/吸收了现有技能：看了哪些入口和元数据，如何结合当前项目筛选，完整阅读了哪些 SKILL.md；",
        "2. 本轮你将明确调用哪些技能：逐项写出准确技能名、选择原因、负责阶段和预期制品；",
        "3. 后续你将如何完整应用：逐项列出会落实的关键步骤、质量门禁、验证命令/证据与失败回退；",
        "4. 哪些候选技能本轮不调用，以及为什么不需要，避免为了显得勤奋而堆叠上下文。",
        "后续每次任务阶段变化时重新检索；交付时报告实际调用结果，而不是只重复计划。",
        "```",
        "",
        "推荐报告格式：",
        "",
        "```markdown",
        "## 技能吸收与调用报告",
        "- 元数据吸收：已扫描 100/100；当前任务关键词：……",
        "- 完整阅读：`主技能`、`互补技能 A`、`互补技能 B`（仅列实际打开的正文）",
        "- 明确调用：",
        "  - `技能名` → 负责阶段 / 选择依据 / 预期制品",
        "- 完整应用计划：",
        "  - `技能名` → 关键步骤 / 质量门禁 / 验证证据 / 失败回退",
        "- 本轮未调用：候选技能及不调用原因",
        "- 交付回报：实际执行、验证结果、偏差与剩余风险",
        "```",
        "",
        "## 正确的高频使用节奏",
        "",
        "1. **任务进入时**：写清领域、交付物、方法与风险，先搜索再开工。",
        "2. **阶段切换时**：从研究转制作、从实现转审查时重新检索，明确换组。",
        "3. **执行过程中**：按选中 `SKILL.md` 的关键步骤产出制品，不跳过不方便的门禁。",
        "4. **遇到失败时**：调用调试、评审或风险技能，记录证据，不反复盲试。",
        "5. **交付之前**：调用验证技能，用真实命令、页面、数据或引用证明完成。",
        "6. **交付之后**：报告实际用了什么、没验证什么、下一会话应继续调用什么。",
        "",
        "## 精确收录清单（100/100）",
        "",
    ]
    for group, items in grouped.items():
        lines += [
            f"### {group}（{len(items)}）",
            "",
            "| # | 技能 | 分类 | 核心用途 |",
            "|---:|---|---|---|",
        ]
        for item in items:
            link = (
                f"skills/{item['name']}/SKILL.md"
                if packaged
                else f"../../{item['path']}"
            )
            lines.append(
                f"| {item['ordinal']} | [`{clean(item['name'])}`]({link}) | "
                f"{clean(item['category'])} | {clean(item['description'], 180)} |"
            )
        lines.append("")

    lines += [
        "## 选择与许可说明",
        "",
        "- 这 100 项全部来自已编目的本地紧凑层；包可在不初始化大型子模块的情况下阅读。",
        "- 清单是跨领域基础款，不代表所有项目都需要全部能力，也不替代目标项目自己的指令、事实和验收标准。",
        "- 每个技能仍受其上游许可证和使用边界约束；本包保留 canonical 路径、来源和哈希，不改变上游权利声明。",
        "- 安全、远控、凭据、网络、写入、个人数据、引用和高风险决策必须单独取得授权并执行相应门禁。",
        "",
        f"礼包版本：`{manifest['version']}`；生成日期：`{manifest['generatedAt']}`。",
        "",
    ]
    return "\n".join(lines)


def copy_package(record: dict[str, object], destination: Path) -> None:
    skill_file = REPO / str(record["path"])
    if skill_file == REPO / "SKILL.md":
        destination.mkdir(parents=True)
        shutil.copy2(skill_file, destination / "SKILL.md")
        return
    package_relative = record.get("sourcePackagePath")
    source_package = REPO / str(package_relative) if package_relative else skill_file.parent
    if not source_package.is_dir():
        raise SystemExit(f"package root is missing: {source_package}")
    shutil.copytree(
        source_package,
        destination,
        symlinks=True,
        ignore=shutil.ignore_patterns("__pycache__", "node_modules", ".DS_Store"),
    )
    if source_package / "SKILL.md" != skill_file:
        shutil.copy2(skill_file, destination / "SKILL.md")


def write_reproducible_archive(source_root: Path, output: Path) -> None:
    temporary = output.with_suffix(output.suffix + ".tmp")
    with temporary.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, compresslevel=9, mtime=0) as compressed:
            with tarfile.open(fileobj=compressed, mode="w", format=tarfile.PAX_FORMAT) as tar:
                paths = [source_root] + sorted(source_root.rglob("*"), key=lambda p: p.as_posix())
                for path in paths:
                    arcname = Path("newcomer-starter-pack") / path.relative_to(source_root)
                    info = tar.gettarinfo(str(path), arcname.as_posix())
                    info.uid = info.gid = 0
                    info.uname = info.gname = ""
                    info.mtime = 0
                    if info.isdir():
                        info.mode = 0o755
                    elif info.isfile():
                        info.mode = 0o755 if os.access(path, os.X_OK) else 0o644
                    if info.isfile():
                        with path.open("rb") as handle:
                            tar.addfile(info, handle)
                    else:
                        tar.addfile(info)
    temporary.replace(output)


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    skills = validate_manifest(manifest)
    readme = build_readme(manifest, skills)
    packaged_readme = build_readme(manifest, skills, packaged=True)
    (BUNDLE / "README.md").write_text(readme, encoding="utf-8")
    records = load_records()

    with tempfile.TemporaryDirectory(prefix="starter-bundle-") as temporary:
        package_root = Path(temporary) / "newcomer-starter-pack"
        (package_root / "skills").mkdir(parents=True)
        (package_root / "START_HERE.md").write_text(packaged_readme, encoding="utf-8")
        (package_root / "MANIFEST.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (package_root / "LICENSE_AND_ATTRIBUTION.md").write_text(
            "# License and attribution\n\n"
            "Each packaged skill retains the source path and source identifier recorded in "
            "MANIFEST.json. The bundle does not replace upstream licenses or grant additional "
            "rights. Consult THIRD_PARTY_NOTICE.md, the package-local legal files, and the "
            "identified source repository before redistribution or high-risk use.\n",
            encoding="utf-8",
        )
        shutil.copy2(REPO / "third_party/NOTICE.md", package_root / "THIRD_PARTY_NOTICE.md")
        for item in skills:
            copy_package(records[str(item["path"])], package_root / "skills" / str(item["name"]))
        write_reproducible_archive(package_root, ARCHIVE)

    digest = sha256(ARCHIVE)
    CHECKSUM.write_text(f"{digest}  {ARCHIVE.name}\n", encoding="utf-8")
    print(f"Packaged {len(skills)} skills: {ARCHIVE.relative_to(REPO)}")
    print(f"SHA-256 {digest}; {ARCHIVE.stat().st_size} bytes")


if __name__ == "__main__":
    main()
