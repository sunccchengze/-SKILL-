#!/usr/bin/env python3
"""Retrieve source-grounded Zoey knowledge records without external dependencies."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_INDEX = SKILL_DIR / "references" / "knowledge" / "claims.jsonl"
DEFAULT_SOURCE_INDEX = SKILL_DIR / "references" / "sources" / "content-index.jsonl"
ASCII_WORD = re.compile(r"[a-z0-9][a-z0-9_.+-]*", re.IGNORECASE)
CJK_RUN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]+")
RETRIEVAL_STOPWORDS = {
    "一个",
    "一下",
    "什么",
    "怎么",
    "如何",
    "应该",
    "可以",
    "能够",
    "使用",
    "进行",
    "这个",
    "那个",
    "关于",
    "是否",
    "想要",
    "请问",
    "帮我",
}


def tokenize(text: str) -> list[str]:
    """Tokenize English words plus Chinese unigrams and bigrams."""
    lowered = text.casefold()
    tokens = ASCII_WORD.findall(lowered)
    for run in CJK_RUN.findall(lowered):
        tokens.extend(run)
        tokens.extend(run[i : i + 2] for i in range(len(run) - 1))
    return tokens


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


def semantic_terms(text: str) -> set[str]:
    """Return English tokens and informative CJK bigrams for a precision gate."""
    lowered = text.casefold()
    terms = {token for token in ASCII_WORD.findall(lowered) if len(token) >= 2}
    for run in CJK_RUN.findall(lowered):
        terms.update(
            token
            for token in (run[i : i + 2] for i in range(len(run) - 1))
            if token not in RETRIEVAL_STOPWORDS
        )
    return terms


def passes_precision_gate(query: str, record: dict[str, Any]) -> bool:
    """Reject matches caused only by generic Chinese characters or question phrasing."""
    query_terms = semantic_terms(query)
    if not query_terms:
        return False
    anchor_terms = semantic_terms(
        " ".join(
            text_of(record.get(field))
            for field in ("topics", "keywords", "tools", "audiences")
        )
    )
    detail_terms = semantic_terms(
        " ".join(
            text_of(record.get(field))
            for field in ("statement", "conditions", "actions", "warnings")
        )
    )
    anchor_overlap = query_terms & anchor_terms
    detail_overlap = query_terms & detail_terms
    return (
        len(anchor_overlap) >= 2
        or (bool(anchor_overlap) and bool(detail_overlap))
        or len(detail_overlap) >= 2
    )


def load_jsonl(
    path: Path, required_fields: tuple[str, ...] = ("claim_id", "statement")
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    if not path.exists():
        raise FileNotFoundError(f"JSONL index not found: {path}")
    with path.open(encoding="utf-8") as handle:
        for line_number, raw in enumerate(handle, 1):
            line = raw.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
            if not isinstance(record, dict):
                raise ValueError(f"{path}:{line_number}: each line must be a JSON object")
            missing = [field for field in required_fields if not record.get(field)]
            if missing:
                raise ValueError(
                    f"{path}:{line_number}: {', '.join(missing)} required"
                )
            records.append(record)
    return records


def load_source_map(path: Path) -> dict[str, dict[str, Any]]:
    records = load_jsonl(path, required_fields=("source_id",))
    sources: dict[str, dict[str, Any]] = {}
    for position, record in enumerate(records, 1):
        source_id = record.get("source_id")
        if not isinstance(source_id, str) or not source_id:
            raise ValueError(f"{path}:{position}: source_id is required")
        if source_id in sources:
            raise ValueError(f"{path}:{position}: duplicate source_id {source_id}")
        sources[source_id] = record
    return sources


def source_label(source_id: str, sources: dict[str, dict[str, Any]]) -> str:
    record = sources.get(source_id)
    if not record:
        return f"{source_id} | source metadata missing"
    parts = [
        source_id,
        str(record.get("title", "untitled")),
        str(record.get("published_at", "unknown date")),
    ]
    locator = record.get("export_locator")
    if locator:
        parts.append(f"export locator={locator}")
    if record.get("url_status") == "verified" and record.get("url"):
        parts.append(str(record["url"]))
    else:
        parts.append("canonical source URL pending")
    return " | ".join(parts)


def document_frequency(records: Iterable[dict[str, Any]]) -> Counter[str]:
    frequencies: Counter[str] = Counter()
    for record in records:
        searchable = " ".join(
            text_of(record.get(field))
            for field in (
                "statement",
                "topics",
                "keywords",
                "audiences",
                "conditions",
                "actions",
                "warnings",
                "tools",
            )
        )
        frequencies.update(set(tokenize(searchable)))
    return frequencies


def score_record(
    query: str,
    query_counts: Counter[str],
    record: dict[str, Any],
    frequencies: Counter[str],
    document_count: int,
) -> float:
    weights = {
        "statement": 5.0,
        "topics": 4.0,
        "keywords": 3.5,
        "tools": 3.0,
        "actions": 2.0,
        "audiences": 1.5,
        "conditions": 1.25,
        "warnings": 1.0,
    }
    score = 0.0
    for field, weight in weights.items():
        field_counts = Counter(tokenize(text_of(record.get(field))))
        for token, query_frequency in query_counts.items():
            if token not in field_counts:
                continue
            inverse_frequency = math.log(
                1.0 + (document_count + 1.0) / (frequencies[token] + 1.0)
            )
            score += weight * inverse_frequency * min(query_frequency, field_counts[token])

    normalized_query = "".join(query.casefold().split())
    normalized_statement = "".join(text_of(record.get("statement")).casefold().split())
    if normalized_query and normalized_query in normalized_statement:
        score += 12.0

    evidence_bonus = {"direct": 1.0, "synthesis": 0.6, "inference": 0.0}
    confidence_bonus = {"high": 0.4, "medium": 0.2, "low": 0.0}
    score += evidence_bonus.get(str(record.get("evidence_level", "")), 0.0)
    score += confidence_bonus.get(str(record.get("confidence", "")), 0.0)
    return score


def rank_records(
    query: str, records: list[dict[str, Any]], top_k: int
) -> list[dict[str, Any]]:
    query_counts = Counter(tokenize(query))
    if not query_counts:
        return []
    frequencies = document_frequency(records)
    scored: list[tuple[float, dict[str, Any]]] = []
    for record in records:
        if not passes_precision_gate(query, record):
            continue
        score = score_record(query, query_counts, record, frequencies, len(records))
        if score > 0:
            scored.append((score, record))
    scored.sort(key=lambda item: (-item[0], str(item[1].get("claim_id", ""))))
    return [dict(record, retrieval_score=round(score, 4)) for score, record in scored[:top_k]]


def render_text(
    results: list[dict[str, Any]],
    index: Path,
    sources: dict[str, dict[str, Any]] | None = None,
) -> str:
    if not results:
        return (
            "NO_ZOEY_EVIDENCE\n"
            f"No matching source-grounded record was found in {index}.\n"
            "Do not present model memory or general academic advice as Zoey's view."
        )
    sources = sources or {}
    lines: list[str] = [
        "PROVENANCE_NOTICE: current records are provisional and mediated by a user-supplied Xiaohongshu Diandian export.",
        "No canonical note URL or raw transcript has yet been verified.",
        "",
    ]
    for position, record in enumerate(results, 1):
        source_ids = record.get("source_ids", [])
        lines.extend(
            [
                f"[{position}] {record['claim_id']} | score={record['retrieval_score']}",
                f"evidence={record.get('evidence_level', 'unknown')} | confidence={record.get('confidence', 'unknown')} | verification={record.get('verification_status', 'unknown')}",
                f"statement: {record['statement']}",
                "sources:",
            ]
        )
        if source_ids:
            lines.extend(f"  - {source_label(item, sources)}" for item in source_ids)
        else:
            lines.append("  - missing")
        lines.extend(
            [
                f"conditions: {text_of(record.get('conditions')) or '—'}",
                f"actions: {text_of(record.get('actions')) or '—'}",
                f"warnings: {text_of(record.get('warnings')) or '—'}",
                "",
            ]
        )
    return "\n".join(lines).rstrip()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", required=True, help="User question or retrieval query")
    parser.add_argument("--top-k", type=int, default=8, help="Maximum records to return")
    parser.add_argument("--index", type=Path, default=DEFAULT_INDEX, help="claims.jsonl path")
    parser.add_argument(
        "--source-index",
        type=Path,
        default=DEFAULT_SOURCE_INDEX,
        help="content-index.jsonl path used to render source titles and provenance",
    )
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = parser.parse_args(argv)
    if args.top_k < 1 or args.top_k > 100:
        parser.error("--top-k must be between 1 and 100")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        records = load_jsonl(args.index)
        sources = load_source_map(args.source_index)
        results = rank_records(args.query, records, args.top_k)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    referenced_ids = {
        source_id
        for record in results
        for source_id in record.get("source_ids", [])
        if source_id in sources
    }
    if args.json:
        print(
            json.dumps(
                {
                    "query": args.query,
                    "index": str(args.index),
                    "source_index": str(args.source_index),
                    "record_count": len(records),
                    "provenance_notice": (
                        "Current records are provisional and mediated by a user-supplied "
                        "Xiaohongshu Diandian export; canonical note URLs and raw transcripts "
                        "have not been verified."
                    ),
                    "matches": results,
                    "source_records": {
                        source_id: sources[source_id]
                        for source_id in sorted(referenced_ids)
                    },
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(render_text(results, args.index, sources))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
