#!/usr/bin/env python3
"""Retrieve source-grounded council claims with routing and integrity controls.

This dependency-free utility retrieves evidence; it does not invent a council answer.
Quarantined claims and known false-positive sources are never returned as advice.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

SKILL_DIR = Path(__file__).resolve().parents[1]
CLAIMS_PATH = SKILL_DIR / "references" / "knowledge" / "claims.jsonl"
CREATORS_PATH = SKILL_DIR / "references" / "knowledge" / "creators.json"
SOURCES_PATH = SKILL_DIR / "references" / "sources" / "sources.jsonl"
FALSE_POSITIVES_PATH = SKILL_DIR / "references" / "sources" / "false-positives.json"
ROUTING_PATH = SKILL_DIR / "references" / "governance" / "routing.json"
DISAGREEMENTS_PATH = SKILL_DIR / "references" / "governance" / "disagreements.jsonl"
COMMERCIAL_PATH = SKILL_DIR / "references" / "governance" / "commercial-conflicts.jsonl"
INTEGRITY_PATH = SKILL_DIR / "references" / "governance" / "integrity-rules.json"

ASCII_WORD = re.compile(r"[a-z0-9][a-z0-9_.+-]*", re.IGNORECASE)
CJK_RUN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]+")
QUESTION_FILLER = {
    "一个", "一下", "什么", "怎么", "如何", "应该", "可以", "能否", "能够",
    "使用", "进行", "这个", "那个", "关于", "是否", "想要", "请问", "帮我",
    "科研", "研究", "论文", "问题", "建议", "方法",
}
CONTEXT_QUERY_TERMS = {"商业", "利益冲突", "付费", "广告", "销售", "披露", "身份", "证据层级", "来源质量"}


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def load_jsonl(path: Path, required: tuple[str, ...] = ()) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, raw in enumerate(handle, 1):
            if not raw.strip():
                continue
            try:
                record = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
            if not isinstance(record, dict):
                raise ValueError(f"{path}:{line_number}: expected an object")
            missing = [field for field in required if not record.get(field)]
            if missing:
                raise ValueError(f"{path}:{line_number}: missing {', '.join(missing)}")
            records.append(record)
    return records


def text_of(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return " ".join(text_of(item) for item in value)
    if isinstance(value, dict):
        return " ".join(f"{key} {text_of(item)}" for key, item in value.items())
    return str(value)


def tokenize(text: str) -> list[str]:
    lowered = text.casefold()
    tokens = ASCII_WORD.findall(lowered)
    for run in CJK_RUN.findall(lowered):
        tokens.append(run)
        tokens.extend(run[index : index + 2] for index in range(len(run) - 1))
    return tokens


def semantic_terms(text: str) -> set[str]:
    lowered = text.casefold()
    terms = {token for token in ASCII_WORD.findall(lowered) if len(token) >= 2}
    for run in CJK_RUN.findall(lowered):
        if len(run) <= 4 and run not in QUESTION_FILLER:
            terms.add(run)
        terms.update(
            pair
            for pair in (run[index : index + 2] for index in range(len(run) - 1))
            if pair not in QUESTION_FILLER
        )
    return terms


def query_requests_context(query: str) -> bool:
    lowered = query.casefold()
    return any(term.casefold() in lowered for term in CONTEXT_QUERY_TERMS)


def detect_routes(query: str, routing: dict[str, Any], limit: int = 2) -> list[dict[str, Any]]:
    query_terms = semantic_terms(query)
    lowered = query.casefold()
    scored: list[tuple[float, dict[str, Any]]] = []
    for route in routing.get("routes", []):
        phrases = [str(item) for item in route.get("intents", [])]
        terms = semantic_terms(" ".join(phrases) + " " + str(route.get("route_id", "")))
        exact = sum(1 for phrase in phrases if len(phrase) >= 2 and phrase.casefold() in lowered)
        overlap = len(query_terms & terms)
        score = exact * 5.0 + overlap
        if score:
            scored.append((score, route))
    scored.sort(key=lambda item: (-item[0], str(item[1].get("route_id", ""))))
    return [dict(route, route_score=score) for score, route in scored[:limit]]


def excluded_content_ids(false_positives: dict[str, Any]) -> set[str]:
    return {
        str(item["content_id"])
        for item in false_positives.get("exclusions", [])
        if item.get("decision") in {"exclude", "metadata_only_not_claim_evidence"}
        and item.get("content_id")
    }


def source_map(
    sources: Iterable[dict[str, Any]], false_positives: dict[str, Any]
) -> tuple[dict[str, dict[str, Any]], set[str]]:
    blocked_ids = excluded_content_ids(false_positives)
    usable: dict[str, dict[str, Any]] = {}
    blocked_source_ids: set[str] = set()
    for source in sources:
        source_id = str(source.get("source_id", ""))
        if str(source.get("content_id", "")) in blocked_ids:
            blocked_source_ids.add(source_id)
            continue
        usable[source_id] = source
    return usable, blocked_source_ids


def passes_precision_gate(query: str, record: dict[str, Any]) -> bool:
    query_terms = semantic_terms(query)
    if not query_terms:
        return False
    anchors = semantic_terms(
        " ".join(text_of(record.get(field)) for field in ("topics", "keywords", "route_tags"))
    )
    details = semantic_terms(
        " ".join(text_of(record.get(field)) for field in ("statement", "actions", "warnings"))
    )
    anchor_overlap = query_terms & anchors
    detail_overlap = query_terms & details
    return (
        len(anchor_overlap) >= 2
        or len(anchor_overlap | detail_overlap) >= 2
        or len(detail_overlap) >= 2
        or any(len(term) >= 4 and term in (anchors | details) for term in query_terms)
    )


def document_frequency(records: Iterable[dict[str, Any]]) -> Counter[str]:
    frequencies: Counter[str] = Counter()
    for record in records:
        searchable = " ".join(
            text_of(record.get(field))
            for field in ("statement", "topics", "keywords", "route_tags", "actions", "warnings")
        )
        frequencies.update(set(tokenize(searchable)))
    return frequencies


def evidence_adjustment(record: dict[str, Any]) -> float:
    confidence = {"high": 1.4, "medium": 0.5, "low": -0.8}.get(str(record.get("confidence")), -1.0)
    modality = {
        "creator_transcript": 1.7,
        "creator_authored_outline": 1.4,
        "institutional_profile": 1.0,
        "creator_description": 0.2,
        "mediated_export": -0.6,
        "secondary_summary": -1.0,
        "related_video_metadata": -1.5,
    }.get(str(record.get("evidence_modality")), 0.0)
    directness = {"direct": 0.7, "indirect": -0.4, "secondary": -0.8}.get(
        str(record.get("directness")), -0.5
    )
    return confidence + modality + directness


def score_record(
    query: str,
    query_counts: Counter[str],
    record: dict[str, Any],
    frequencies: Counter[str],
    document_count: int,
    route_ids: set[str],
) -> float:
    weights = {
        "statement": 5.0,
        "topics": 4.5,
        "keywords": 4.0,
        "route_tags": 2.5,
        "actions": 1.5,
        "warnings": 0.6,
    }
    score = 0.0
    for field, weight in weights.items():
        field_counts = Counter(tokenize(text_of(record.get(field))))
        for token, query_frequency in query_counts.items():
            if token not in field_counts:
                continue
            inverse_frequency = math.log(1.0 + (document_count + 1.0) / (frequencies[token] + 1.0))
            score += weight * inverse_frequency * min(query_frequency, field_counts[token])
    normalized_query = "".join(query.casefold().split())
    normalized_statement = "".join(text_of(record.get("statement")).casefold().split())
    if normalized_query and normalized_query in normalized_statement:
        score += 10.0
    if route_ids & set(record.get("route_tags", [])):
        score += 3.0
    return score + evidence_adjustment(record)


def evidence_label(record: dict[str, Any]) -> str:
    modality = record.get("evidence_modality")
    coverage = record.get("coverage")
    if modality == "creator_transcript" and coverage == "full_transcript":
        return "完整逐字稿直接证据"
    if modality == "creator_authored_outline":
        return "创作者提纲直接证据"
    if modality == "mediated_export":
        return "暂定介导证据"
    if modality == "secondary_summary":
        return "二手摘要"
    if coverage in {"title_description_only", "related_collection_metadata", "channel_metadata_only"}:
        return "标题/简介/元数据级"
    return "有限直接证据"


def recommendation_ready(record: dict[str, Any]) -> bool:
    return (
        record.get("status") == "active"
        and record.get("confidence") in {"high", "medium"}
        and record.get("evidence_modality") in {"creator_transcript", "creator_authored_outline"}
        and record.get("directness") == "direct"
    )


def rank_records(
    query: str,
    claims: list[dict[str, Any]],
    sources: dict[str, dict[str, Any]] | None = None,
    *,
    top_k: int = 8,
    max_per_creator: int = 2,
    include_context: bool = False,
    route_ids: set[str] | None = None,
) -> list[dict[str, Any]]:
    """Rank claims while enforcing quarantine, provenance, and creator diversity."""
    route_ids = route_ids or set()
    sources = sources or {}
    allow_context = include_context or query_requests_context(query)
    eligible: list[dict[str, Any]] = []
    for record in claims:
        status = record.get("status")
        if status == "quarantined" or (status == "context_only" and not allow_context):
            continue
        linked = record.get("source_ids", [])
        if sources and (not linked or any(source_id not in sources for source_id in linked)):
            continue
        if passes_precision_gate(query, record):
            eligible.append(record)
    if not eligible:
        return []

    query_counts = Counter(tokenize(query))
    frequencies = document_frequency(eligible)
    scored = [
        (
            score_record(query, query_counts, record, frequencies, len(eligible), route_ids),
            record,
        )
        for record in eligible
    ]
    scored = [item for item in scored if item[0] >= 8.0]
    scored.sort(
        key=lambda item: (
            -int(recommendation_ready(item[1])),
            -item[0],
            str(item[1].get("claim_id", "")),
        )
    )

    selected: list[dict[str, Any]] = []
    creator_counts: defaultdict[str, int] = defaultdict(int)
    for score, record in scored:
        creator_id = str(record.get("creator_id", ""))
        if creator_counts[creator_id] >= max_per_creator:
            continue
        enriched = dict(record)
        enriched["retrieval_score"] = round(score, 4)
        enriched["evidence_label"] = evidence_label(record)
        enriched["recommendation_ready"] = recommendation_ready(record)
        if sources:
            enriched["sources"] = [
                {
                    key: sources[source_id].get(key)
                    for key in (
                        "source_id", "title", "url", "platform", "published_at", "modality",
                        "extraction_coverage", "directness", "commercial_disclosure",
                    )
                }
                for source_id in record.get("source_ids", [])
            ]
        selected.append(enriched)
        creator_counts[creator_id] += 1
        if len(selected) >= top_k:
            break
    return selected


def detect_integrity(query: str, rules: dict[str, Any]) -> list[dict[str, Any]]:
    lowered = query.casefold()
    alerts: list[dict[str, Any]] = []
    for rule in rules.get("forbidden", []):
        matched = [pattern for pattern in rule.get("patterns", []) if str(pattern).casefold() in lowered]
        if matched:
            alerts.append(
                {
                    "rule_id": rule.get("rule_id"),
                    "category": rule.get("category"),
                    "matched_patterns": matched,
                    "action": rule.get("action"),
                    "safe_redirect": rules.get("safe_redirects", {}).get(rule.get("category")),
                }
            )
    return alerts


def relevant_disagreements(query: str, disagreements: list[dict[str, Any]], limit: int = 3) -> list[dict[str, Any]]:
    query_terms = semantic_terms(query)
    ranked: list[tuple[int, dict[str, Any]]] = []
    for item in disagreements:
        topic = str(item.get("topic", ""))
        overlap = len(query_terms & semantic_terms(topic + " " + text_of(item.get("positions", []))))
        if topic and topic in query:
            overlap += 4
        if overlap >= 2:
            ranked.append((overlap, item))
    ranked.sort(key=lambda entry: (-entry[0], str(entry[1].get("disagreement_id", ""))))
    return [item for _, item in ranked[:limit]]


def build_payload(query: str, top_k: int = 8, include_context: bool = False) -> dict[str, Any]:
    creators_data = load_json(CREATORS_PATH)
    creators = {item["creator_id"]: item for item in creators_data.get("creators", [])}
    claims = load_jsonl(CLAIMS_PATH, ("claim_id", "creator_id", "statement"))
    source_records = load_jsonl(SOURCES_PATH, ("source_id", "creator_id", "url"))
    usable_sources, blocked_source_ids = source_map(source_records, load_json(FALSE_POSITIVES_PATH))
    routing = load_json(ROUTING_PATH)
    routes = detect_routes(query, routing)
    route_ids = {str(item.get("route_id")) for item in routes}
    results = rank_records(
        query,
        claims,
        usable_sources,
        top_k=top_k,
        max_per_creator=2,
        include_context=include_context,
        route_ids=route_ids,
    )
    commercial = {
        item["creator_id"]: item
        for item in load_jsonl(COMMERCIAL_PATH, ("conflict_id", "creator_id"))
    }
    advisors: list[dict[str, Any]] = []
    seen: set[str] = set()
    for result in results:
        creator_id = str(result["creator_id"])
        if creator_id in seen:
            continue
        seen.add(creator_id)
        creator = creators.get(creator_id, {})
        advisors.append(
            {
                "creator_id": creator_id,
                "display_name": creator.get("display_name", creator_id),
                "role": creator.get("council_role"),
                "evidence_profile": creator.get("evidence_profile"),
                "commercial_conflict": commercial.get(creator_id),
            }
        )

    integrity_rules = load_json(INTEGRITY_PATH)
    alerts = detect_integrity(query, integrity_rules)
    disagreements = relevant_disagreements(
        query, load_jsonl(DISAGREEMENTS_PATH, ("disagreement_id", "topic"))
    )
    if not results:
        evidence_status = "abstain"
        abstention = "联合体语料没有足够匹配的创作者证据。若继续，请把后续内容标为“通用科研建议”，不要归因给成员。"
    elif any(item["recommendation_ready"] for item in results):
        evidence_status = "grounded"
        abstention = None
    else:
        evidence_status = "weak_only"
        abstention = "只找到标题、简介、二手摘要或暂定介导证据；不得据此补写步骤。需要时另列通用科研建议。"

    return {
        "query": query,
        "default_response_language": routing.get("default_language", "zh-CN"),
        "evidence_status": evidence_status,
        "abstention": abstention,
        "integrity_alerts": alerts,
        "detected_routes": routes,
        "advisors": advisors,
        "commercial_disclosures": (
            list(commercial.values()) if query_requests_context(query) else []
        ),
        "results": results,
        "disagreements": disagreements,
        "retrieval_policy": {
            "quarantined_claims_returned": False,
            "false_positive_source_ids_blocked": sorted(blocked_source_ids),
            "max_claims_per_creator": 2,
            "commercial_disclosures_attached": True,
        },
    }


def render_text(payload: dict[str, Any]) -> str:
    lines = ["AI科研学长姐联合体 · 证据检索", f"查询：{payload['query']}"]
    alerts = payload.get("integrity_alerts", [])
    if alerts:
        lines.extend(["", "## 学术诚信提示"])
        for alert in alerts:
            lines.append(f"- [{alert['rule_id']}] {alert['action']}")
            if alert.get("safe_redirect"):
                lines.append(f"  合规替代：{alert['safe_redirect']}")
    routes = payload.get("detected_routes", [])
    if routes:
        lines.extend(["", "## 路由", "、".join(str(item["route_id"]) for item in routes)])
    if payload.get("abstention"):
        lines.extend(["", "## 证据边界", str(payload["abstention"])])
    results = payload.get("results", [])
    if results:
        creator_names = {
            item["creator_id"]: item.get("display_name", item["creator_id"])
            for item in payload.get("advisors", [])
        }
        lines.extend(["", "## 命中的创作者证据"])
        for position, result in enumerate(results, 1):
            lines.append(
                f"{position}. [{result['claim_id']}] {creator_names.get(result['creator_id'], result['creator_id'])}：{result['statement']}"
            )
            lines.append(
                "   证据："
                f"{result['evidence_label']} / {result['confidence']} / "
                f"{result['directness']} / {result['coverage']}"
            )
            if result.get("warnings"):
                lines.append("   警告：" + "；".join(result["warnings"]))
            for source in result.get("sources", []):
                lines.append(
                    f"   来源：[{source['source_id']}] {source['title']} — {source['url']}"
                )
        disclosures = [
            advisor for advisor in payload.get("advisors", [])
            if advisor.get("commercial_conflict", {}).get("level") not in {None, "low_or_unknown"}
        ]
        if disclosures:
            lines.extend(["", "## 商业与利益披露"])
            for advisor in disclosures:
                conflict = advisor["commercial_conflict"]
                lines.append(f"- {advisor['display_name']}：{conflict['summary']} {conflict['response_action']}")
    if payload.get("commercial_disclosures"):
        lines.extend(["", "## 商业披露总表"] )
        creator_names = {
            item["creator_id"]: item.get("display_name", item["creator_id"])
            for item in payload.get("advisors", [])
        }
        for item in payload["commercial_disclosures"]:
            lines.append(
                f"- {creator_names.get(item['creator_id'], item['creator_id'])} "
                f"({item['level']})：{item['summary']}"
            )
    if payload.get("disagreements"):
        lines.extend(["", "## 相关分歧/张力"])
        for item in payload["disagreements"]:
            lines.append(f"- [{item['disagreement_id']}] {item['topic']}：{item['resolution']}")
    lines.extend([
        "",
        "## 使用约束",
        "先按成员逐条归因，再做条件化综合；不能把检索结果直接拼成虚构共识。",
        "工具、政策、价格与投稿规则属于时效信息，执行前应重新核验。",
    ])
    return "\n".join(lines)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", required=True, help="Chinese or English research question")
    parser.add_argument("--top-k", type=int, default=8)
    parser.add_argument("--include-context", action="store_true", help="include non-advisory context records")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.top_k < 1:
        print("ERROR: --top-k must be positive", file=sys.stderr)
        return 2
    try:
        payload = build_payload(args.query, args.top_k, args.include_context)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(render_text(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
