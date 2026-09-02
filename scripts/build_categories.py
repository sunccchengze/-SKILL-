#!/usr/bin/env python3
"""Build additive category indexes without moving canonical skill packages."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CATALOGS = (
    "catalog/skills.json",
    "catalog/official-skills.json",
    "catalog/research-skills.json",
    "catalog/curated-skills.json",
)
CATEGORIES = {
    "agents-orchestration": (
        "Agent 与编排",
        "路由、计划、上下文、记忆、评估、多 Agent 协作与工作流治理。",
        "task planning orchestration verification",
    ),
    "engineering-code": (
        "工程与代码",
        "架构、编码、测试、调试、评审、Git、CI/CD、API、前后端与性能。",
        "code test debug review architecture",
    ),
    "documents-data": (
        "文档与数据",
        "PDF、结构化文档、表格、数据库、数据清洗、分析与可追踪交付。",
        "document data spreadsheet database",
    ),
    "research-science": (
        "研究与科学",
        "检索、综述、引用、实验、统计、科学计算、论文、同行评审与复现。",
        "literature review citation statistics",
    ),
    "writing-content": (
        "写作与内容",
        "中文与英文写作、编辑、内容研究、技术表达、营销文案与去模板化。",
        "writing editing content audience",
    ),
    "design-media": (
        "设计与媒体",
        "产品/UI/UX、视觉系统、网页、演示、图像、视频、动效与媒体生产。",
        "design ui ux visual media",
    ),
    "business-strategy": (
        "商业与战略",
        "产品、市场、营销、定价、竞争、运营、决策、发布与组织协作。",
        "product strategy market decision",
    ),
    "security-compliance": (
        "安全、隐私与合规",
        "安全评审、威胁与风险、隐私、无障碍、依赖、审计和合规治理。",
        "security privacy compliance audit",
    ),
    "general": (
        "通用生产力",
        "跨领域计划、沟通、会议、通用工具、个人效率与难以单归一域的能力。",
        "plan communicate productivity",
    ),
}
TIER_RANK = {
    "maintained": 0,
    "router": 1,
    "official-source": 2,
    "curated-source": 3,
    "community": 4,
    "tool-bundled": 5,
    "full-source": 6,
    "bundled": 7,
}


def load_visible_records() -> tuple[int, list[dict[str, object]]]:
    aliases = {
        str(item["path"])
        for item in json.loads((REPO / "catalog/overlap-policy.json").read_text())["aliases"]
    }
    records: list[dict[str, object]] = []
    raw_count = 0
    for relative in CATALOGS:
        catalog = json.loads((REPO / relative).read_text(encoding="utf-8"))
        for record in catalog["skills"]:
            raw_count += 1
            if record.get("tier") == "variant" or record.get("path") in aliases:
                continue
            records.append(record)
    return raw_count, records


def clean(value: object) -> str:
    return " ".join(str(value or "").replace("\t", " ").split())


def starter_paths() -> set[str]:
    path = REPO / "bundles/newcomer-starter-pack/manifest.json"
    if not path.is_file():
        return set()
    return {str(item["path"]) for item in json.loads(path.read_text())["skills"]}


def main() -> None:
    raw_count, records = load_visible_records()
    unknown = sorted({str(record["category"]) for record in records} - set(CATEGORIES))
    if unknown:
        raise SystemExit(f"unknown categories: {', '.join(unknown)}")

    starters = starter_paths()
    root = REPO / "categories"
    root.mkdir(exist_ok=True)
    summary = []

    for slug, (title, description, example_query) in CATEGORIES.items():
        selected = [record for record in records if record["category"] == slug]
        selected.sort(
            key=lambda record: (
                TIER_RANK.get(str(record.get("tier")), 8),
                clean(record.get("name")).casefold(),
                clean(record.get("path")),
            )
        )
        category_root = root / slug
        category_root.mkdir(exist_ok=True)
        with (category_root / "skills.tsv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
            writer.writerow(
                ("name", "tier", "source", "status", "available_locally", "path", "description")
            )
            for record in selected:
                path = clean(record["path"])
                writer.writerow(
                    (
                        clean(record["name"]),
                        clean(record.get("tier")),
                        clean(record.get("sourceId", record.get("collection", "repository"))),
                        clean(record.get("sourceStatus", "current")),
                        (
                            "requires-submodule-init"
                            if record.get("requiresSubmoduleInit")
                            else ("yes" if (REPO / path).is_file() else "requires-submodule-init")
                        ),
                        path,
                        clean(record.get("description")) or "—",
                    )
                )

        starter_selected = [record for record in selected if record["path"] in starters]
        featured = starter_selected[:20] or selected[:20]
        lines = [
            f"# {title}",
            "",
            description,
            "",
            f"- 默认可见技能：**{len(selected)}**",
            f"- 新手大礼包入选：**{len(starter_selected)}**",
            "- 完整机器索引：[`skills.tsv`](skills.tsv)",
            "",
            "## 如何找技能",
            "",
            "```bash",
            f'python scripts/search_skills.py "{example_query}" --category {slug} --limit 12',
            "```",
            "",
            "先看搜索元数据，只打开当前任务真正命中的 1 个主技能和至多 3 个互补技能；不要把本分类全部载入上下文。",
            "",
            "## 新手大礼包中的代表技能" if starter_selected else "## 首批可浏览入口",
            "",
            "| 技能 | 层级 | 用途 |",
            "|---|---|---|",
        ]
        if slug == "research-science":
            lines.insert(
                7,
                "- 可迁移离线包：[`科研大礼包 · Research Workflow Kit`](../../bundles/research-workflow-kit/README.md)",
            )
        for record in featured:
            path = clean(record["path"])
            lines.append(
                f"| [`{clean(record['name'])}`](../../{path}) | {clean(record.get('tier'))} | "
                f"{clean(record.get('description'))} |"
            )
        lines += [
            "",
            "返回[全部分类](../README.md)或查看[新手大礼包](../../bundles/newcomer-starter-pack/README.md)。",
            "",
        ]
        (category_root / "README.md").write_text("\n".join(lines), encoding="utf-8")
        summary.append(
            {
                "id": slug,
                "displayName": title,
                "description": description,
                "count": len(selected),
                "starterCount": len(starter_selected),
                "index": f"categories/{slug}/skills.tsv",
            }
        )

    by_tier = Counter(str(record.get("tier")) for record in records)
    payload = {
        "formatVersion": 1,
        "generatedAt": "2026-08-16",
        "rawCatalogEntries": raw_count,
        "defaultVisibleEntries": len(records),
        "starterBundleEntries": len(starters),
        "byTier": dict(sorted(by_tier.items())),
        "categories": summary,
    }
    (REPO / "catalog/category-summary.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    root_lines = [
        "# 技能分类导航",
        "",
        "这里是**不移动 canonical 包路径**的加法式导航层。技能仍由 `catalog/`、`skills/` 和固定的 `full-sources/` 管理；分类目录提供人类 README 与完整 TSV，因此不会破坏既有搜索、安装、来源锁和引用。",
        "",
        f"四个机器目录共有 **{raw_count}** 个原始入口；隐藏内容变体与已审计别名后，默认呈现 **{len(records)}** 个候选。",
        "",
        "| 分类 | 技能数 | 新手大礼包 | 主要范围 |",
        "|---|---:|---:|---|",
    ]
    for item in summary:
        root_lines.append(
            f"| [{item['displayName']}]({item['id']}/README.md) | {item['count']} | "
            f"{item['starterCount']} | {item['description']} |"
        )
    root_lines += [
        "",
        "## 选择原则",
        "",
        "1. 先把任务写成“领域 + 交付物 + 方法 + 风险”关键词。",
        "2. 用 `search_skills.py` 搜索；分类只用于缩小范围，不是强制边界。",
        "3. 通常选择 1 个主技能，加研究、制作、审查各至多 1 个互补技能。",
        "4. 明确说出本轮调用了哪些技能、用在哪一步、用什么证据验证；不要只列名字不执行。",
        "5. 需要完整 references/assets 时初始化相应 `full-sources/`；不要把快索引缺文件误判为上游没有。",
        "",
        "机器摘要见 [`catalog/category-summary.json`](../catalog/category-summary.json)，100 项基础组合见[新手大礼包](../bundles/newcomer-starter-pack/README.md)。",
        "",
    ]
    (root / "README.md").write_text("\n".join(root_lines), encoding="utf-8")
    print(f"Classified {len(records)} default-visible entries into {len(CATEGORIES)} categories.")


if __name__ == "__main__":
    main()
