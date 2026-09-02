#!/usr/bin/env python3
"""Build the repository-wide searchable skill catalog without dependencies."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUTPUT_JSON = REPO / "catalog" / "skills.json"
OUTPUT_MARKDOWN = REPO / "catalog" / "SKILLS.md"

# Deep, cross-disciplinary local Skills use reviewed semantic categories rather
# than whichever incidental keyword happens to score highest in a long description.
CATEGORY_OVERRIDES = {
    "book-systems-thinking-intervention": "business-strategy",
    "book-cointelligence-human-ai-collaboration": "agents-orchestration",
    "book-ai-mirror-agency": "business-strategy",
    "book-human-compatible-alignment": "security-compliance",
    "ml-dl-learning-router": "research-science",
    "d2l-lab-backbone": "research-science",
    "zhou-classical-ml-reasoning": "research-science",
    "goodfellow-deep-learning-theory": "research-science",
    "ai-futures-scenario-lab-2026": "business-strategy",
    "book-tools-of-titans-experiment-lab": "general",
    "book-fifth-discipline-learning-system": "business-strategy",
    "book-human-use-cybernetics": "security-compliance",
    "book-understanding-media-audit": "design-media",
    "book-cialdini-influence": "business-strategy",
    "book-dont-make-me-think": "design-media",
    "book-adler-community": "general",
    "book-hessler-documentary": "writing-content",
    "book-berger-contagious": "writing-content",
    "book-gladwell-tipping-point": "business-strategy",
    "book-tiny-habits-fogg": "general",
    "book-sapiens-claim-audit": "research-science",
    "book-noise-judgment-audit": "business-strategy",
    "book-naval-almanack-option-ledger": "business-strategy",
    "book-principles-decision-system": "business-strategy",
    "book-governing-commons-institution-design": "business-strategy",
    "book-privacy-context-flow-audit": "security-compliance",
    "book-safer-world-control-audit": "security-compliance",
    "book-what-if-causal-audit": "research-science",
    "book-applied-causal-ml-readiness": "research-science",
    "book-atlas-ai-stack-audit": "security-compliance",
    "book-ethical-algorithm-constraints": "security-compliance",
}

CATEGORY_RULES = [
    ("security-compliance", ("security", "compliance", "audit", "privacy", "threat", "安全", "合规", "审计")),
    ("research-science", ("research", "science", "academic", "paper", "literature", "statistics", "biology", "chemistry", "physics", "科研", "论文", "文献", "统计")),
    ("design-media", ("design", "ui", "ux", "visual", "poster", "slide", "image", "video", "animation", "设计", "海报", "视觉", "演示", "图像", "视频")),
    ("writing-content", ("writing", "writer", "content", "copy", "article", "story", "humaniz", "写作", "文案", "文章", "故事", "改稿")),
    ("documents-data", ("document", "pdf", "docx", "xlsx", "spreadsheet", "data", "database", "文档", "表格", "数据")),
    ("agents-orchestration", ("agent", "mcp", "orchestrat", "automation", "memory", "harness", "workflow", "智能体", "编排", "自动化", "记忆")),
    ("engineering-code", ("code", "developer", "engineering", "test", "debug", "api", "frontend", "backend", "python", "react", "deploy", "cloud", "azure", "kubernetes", "devops", "infrastructure", "sdk", ".net", "java", "typescript", "github", "git", "pull request", "ci", "cli", "代码", "开发", "测试", "调试", "部署", "云")),
    ("business-strategy", ("business", "product", "marketing", "sales", "strategy", "finance", "decision", "商业", "产品", "营销", "战略", "决策")),
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clean_scalar(value: str) -> str:
    value = value.strip().strip("\"'")
    return re.sub(r"\s+", " ", value)


def parse_frontmatter_text(text: str, fallback_name: str) -> tuple[str, str, bool]:
    """Parse the two portable Agent Skills fields without a YAML dependency."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.DOTALL)
    if not match:
        return fallback_name, "", False

    lines = match.group(1).splitlines()
    values: dict[str, str] = {}
    index = 0
    while index < len(lines):
        field_match = re.match(r"^(name|description):\s*(.*)$", lines[index])
        if not field_match:
            index += 1
            continue
        key, value = field_match.groups()
        if value in {"|", ">", "|-", ">-", "|+", ">+"}:
            block: list[str] = []
            index += 1
            while index < len(lines) and (not lines[index].strip() or lines[index][:1].isspace()):
                if lines[index].strip():
                    block.append(lines[index].strip())
                index += 1
            values[key] = " ".join(block)
            continue
        values[key] = clean_scalar(value)
        index += 1

    return values.get("name", fallback_name), values.get("description", ""), bool(values.get("name"))


def parse_frontmatter(path: Path) -> tuple[str, str, bool]:
    return parse_frontmatter_text(
        path.read_text(encoding="utf-8", errors="replace"), path.parent.name
    )


def normalize_name(name: str) -> str:
    name = name.casefold().strip().replace("_", "-")
    name = re.sub(r"\s+", "-", name)
    return re.sub(r"-+", "-", name)


def tier_and_collection(relative: Path) -> tuple[str, str]:
    parts = relative.parts
    if relative == Path("SKILL.md"):
        return "router", "repository"
    if parts[:2] == ("skills", "community") and len(parts) > 2:
        return "community", parts[2]
    if parts[:2] == ("skills", "variants") and len(parts) > 2:
        return "variant", parts[2]
    if parts and parts[0] == "skills" and len(parts) > 1:
        return "maintained", parts[1]
    if parts[:3] == ("tools", "openwiki", "skills"):
        return "tool-bundled", "openwiki"
    return "bundled", parts[0] if parts else "repository"


def _keyword_matches(text: str, keyword: str) -> bool:
    """Avoid false positives such as ``ui`` in ``requires`` or ``api`` in ``rapid``."""
    if keyword.isascii() and keyword.isalnum() and len(keyword) <= 3:
        return bool(re.search(rf"(?<![a-z0-9]){re.escape(keyword)}(?![a-z0-9])", text))
    return keyword in text


def category_for(name: str, description: str, path: str) -> str:
    override = CATEGORY_OVERRIDES.get(normalize_name(name))
    if override:
        return override
    content = f"{name} {description}".casefold()
    source_path = path.casefold()
    best_category = "general"
    best_score = 0
    for category, keywords in CATEGORY_RULES:
        # Human-authored metadata is a stronger signal than a directory name.
        # Generic path components such as ``skills`` must not make every entry
        # look like an orchestration skill.
        content_score = sum(_keyword_matches(content, keyword) for keyword in keywords)
        path_score = sum(
            _keyword_matches(source_path, keyword)
            for keyword in keywords
            if keyword not in {"skill", "技能"}
        )
        score = content_score * 2 + path_score
        if score > best_score:
            best_category, best_score = category, score
    return best_category


def discover() -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for path in sorted(REPO.rglob("SKILL.md")):
        relative = path.relative_to(REPO)
        if ".git" in relative.parts or "node_modules" in relative.parts or relative.parts[:1] == ("full-sources",):
            continue
        name, description, valid_frontmatter = parse_frontmatter(path)
        tier, collection = tier_and_collection(relative)
        records.append(
            {
                "name": normalize_name(name),
                "displayName": name,
                "description": description,
                "category": category_for(name, description, str(relative)),
                "tier": tier,
                "collection": collection,
                "path": str(relative),
                "sha256": sha256(path),
                "frontmatter": "valid" if valid_frontmatter else "legacy",
            }
        )
    return records


def write_markdown(records: list[dict[str, object]]) -> None:
    visible = [record for record in records if record["tier"] != "variant"]
    category_counts = Counter(str(record["category"]) for record in visible)
    tier_counts = Counter(str(record["tier"]) for record in records)

    lines = [
        "# 技能目录",
        "",
        "> 此文件由 `python scripts/build_catalog.py` 生成。完整机器可读目录见 `skills.json`。",
        "",
        f"共发现 **{len(records)}** 个 `SKILL.md`，其中非变体入口 **{len(visible)}** 个。",
        "",
        "## 层级统计",
        "",
        "| 层级 | 数量 |",
        "|---|---:|",
    ]
    lines.extend(f"| `{tier}` | {count} |" for tier, count in sorted(tier_counts.items()))
    lines.extend(["", "## 分类统计", "", "| 分类 | 数量 |", "|---|---:|"])
    lines.extend(f"| `{category}` | {count} |" for category, count in sorted(category_counts.items()))
    lines.extend([
        "",
        "## 主入口",
        "",
        "| 名称 | 分类 | 层级 | 路径 | 说明 |",
        "|---|---|---|---|---|",
    ])
    for record in sorted(visible, key=lambda item: (str(item["category"]), str(item["name"]), str(item["path"]))):
        description = str(record["description"]).replace("|", "\\|").replace("\n", " ")
        if len(description) > 120:
            description = description[:117] + "..."
        lines.append(
            f"| `{record['name']}` | `{record['category']}` | `{record['tier']}` | "
            f"[`{record['path']}`](../{record['path']}) | {description} |"
        )
    OUTPUT_MARKDOWN.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    records = discover()
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    payload = {"formatVersion": 1, "count": len(records), "skills": records}
    OUTPUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(records)
    print(f"Cataloged {len(records)} skill entry points in {OUTPUT_JSON.relative_to(REPO)}")


if __name__ == "__main__":
    main()
