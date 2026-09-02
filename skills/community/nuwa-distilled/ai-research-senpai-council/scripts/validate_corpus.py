#!/usr/bin/env python3
"""Validate the council's creator, source, claim, and governance ledgers."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

SKILL_DIR = Path(__file__).resolve().parents[1]
CREATORS = SKILL_DIR / "references" / "knowledge" / "creators.json"
CLAIMS = SKILL_DIR / "references" / "knowledge" / "claims.jsonl"
SOURCES = SKILL_DIR / "references" / "sources" / "sources.jsonl"
FALSE_POSITIVES = SKILL_DIR / "references" / "sources" / "false-positives.json"
ROUTING = SKILL_DIR / "references" / "governance" / "routing.json"
DISAGREEMENTS = SKILL_DIR / "references" / "governance" / "disagreements.jsonl"
COMMERCIAL = SKILL_DIR / "references" / "governance" / "commercial-conflicts.jsonl"
INTEGRITY = SKILL_DIR / "references" / "governance" / "integrity-rules.json"

FIXED_ROSTER = {
    "zoey", "yang-shixiong", "mai-xiaozhe", "simin", "he-jing", "li-mu",
    "andy-stapleton", "amina-yonis", "tara-brabazon", "james-hayton",
    "kriukow", "academic-english-now",
}
CONFIDENCE = {"high", "medium", "low"}
CLAIM_STATUS = {"active", "context_only", "quarantined"}
DIRECTNESS = {"direct", "indirect", "secondary"}
STATEMENT_TYPES = {
    "creator_statement", "description_level_summary", "title_level_theme",
    "commercial_disclosure", "institutional_fact", "secondary_summary", "risk_notice",
}
MODALITIES = {
    "mediated_export", "creator_description", "creator_authored_outline",
    "institutional_profile", "secondary_summary", "creator_transcript",
    "related_video_metadata",
}
COVERAGE = {
    "partial_mediated_export", "title_description_only", "related_collection_metadata",
    "creator_outline", "institutional_page", "secondary_article", "full_transcript",
    "creator_page_and_description", "channel_metadata_only",
}
SOURCE_STATUS = {"live", "unknown", "unlisted", "private", "unavailable"}
REQUIRED_CLAIM_LISTS = {"source_ids", "topics", "keywords", "route_tags", "actions", "warnings"}
CLAIM_SOURCE_METADATA_FIELDS = {"url", "source_url", "source_title", "platform", "published_at"}


def load_json(path: Path, errors: list[str]) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path}: expected an object")
        return {}
    return value


def load_jsonl(path: Path, errors: list[str]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    try:
        handle = path.open(encoding="utf-8")
    except OSError as exc:
        errors.append(f"{path}: {exc}")
        return records
    with handle:
        for line_number, raw in enumerate(handle, 1):
            if not raw.strip():
                continue
            try:
                value = json.loads(raw)
            except json.JSONDecodeError as exc:
                errors.append(f"{path}:{line_number}: invalid JSON: {exc}")
                continue
            if not isinstance(value, dict):
                errors.append(f"{path}:{line_number}: expected an object")
                continue
            records.append(value)
    return records


def unique_index(records: list[dict[str, Any]], field: str, label: str, errors: list[str]) -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for position, record in enumerate(records, 1):
        value = record.get(field)
        if not isinstance(value, str) or not value:
            errors.append(f"{label} record {position}: missing {field}")
        elif value in index:
            errors.append(f"{label} record {position}: duplicate {field} {value}")
        else:
            index[value] = record
    return index


def validate_creators(data: dict[str, Any], errors: list[str]) -> dict[str, dict[str, Any]]:
    records = data.get("creators")
    if not isinstance(records, list):
        errors.append("creators.json: creators must be a list")
        return {}
    index = unique_index(records, "creator_id", "creator", errors)
    if set(index) != FIXED_ROSTER:
        errors.append(
            "creators.json: roster must equal fixed 12-member set; "
            f"missing={sorted(FIXED_ROSTER - set(index))}, extra={sorted(set(index) - FIXED_ROSTER)}"
        )
    for creator_id, creator in index.items():
        for field in (
            "display_name", "canonical_name", "council_role", "evidence_profile",
            "commercial_disclosure", "identity_note",
        ):
            if not isinstance(creator.get(field), str) or not creator[field].strip():
                errors.append(f"creator {creator_id}: {field} is required")
        for field in ("platforms", "languages", "strengths", "integrity_flags"):
            if not isinstance(creator.get(field), list):
                errors.append(f"creator {creator_id}: {field} must be a list")
    return index


def validate_sources(
    records: list[dict[str, Any]], creators: dict[str, dict[str, Any]],
    false_positives: dict[str, Any], errors: list[str],
) -> dict[str, dict[str, Any]]:
    index = unique_index(records, "source_id", "source", errors)
    blocked = {
        str(item.get("content_id"))
        for item in false_positives.get("exclusions", [])
        if item.get("decision") in {"exclude", "metadata_only_not_claim_evidence"}
    }
    for source_id, source in index.items():
        for field in ("creator_id", "platform", "content_id", "title", "url", "fetched_at", "notes"):
            if not isinstance(source.get(field), str) or not source[field].strip():
                errors.append(f"source {source_id}: {field} is required")
        if source.get("creator_id") not in creators:
            errors.append(f"source {source_id}: unknown creator {source.get('creator_id')!r}")
        if source.get("modality") not in MODALITIES:
            errors.append(f"source {source_id}: invalid modality {source.get('modality')!r}")
        if source.get("directness") not in DIRECTNESS:
            errors.append(f"source {source_id}: invalid directness {source.get('directness')!r}")
        if source.get("status") not in SOURCE_STATUS:
            errors.append(f"source {source_id}: invalid status {source.get('status')!r}")
        if not isinstance(source.get("original_uploader"), bool) and not (
            source.get("modality") == "mediated_export" and source.get("original_uploader") == "unknown"
        ):
            errors.append(f"source {source_id}: original_uploader must be boolean (or unknown for mediated export)")
        if str(source.get("content_id")) in blocked:
            errors.append(f"source {source_id}: false-positive or metadata-only content_id re-entered ledger")
    return index


def validate_claims(
    records: list[dict[str, Any]], creators: dict[str, dict[str, Any]],
    sources: dict[str, dict[str, Any]], errors: list[str],
) -> dict[str, dict[str, Any]]:
    index = unique_index(records, "claim_id", "claim", errors)
    active_by_creator: Counter[str] = Counter()
    for claim_id, claim in index.items():
        for field in ("creator_id", "statement", "checked_at"):
            if not isinstance(claim.get(field), str) or not claim[field].strip():
                errors.append(f"claim {claim_id}: {field} is required")
        creator_id = claim.get("creator_id")
        if creator_id not in creators:
            errors.append(f"claim {claim_id}: unknown creator {creator_id!r}")
        if claim.get("statement_type") not in STATEMENT_TYPES:
            errors.append(f"claim {claim_id}: invalid statement_type {claim.get('statement_type')!r}")
        if claim.get("evidence_modality") not in MODALITIES:
            errors.append(f"claim {claim_id}: invalid evidence_modality {claim.get('evidence_modality')!r}")
        if claim.get("coverage") not in COVERAGE:
            errors.append(f"claim {claim_id}: invalid coverage {claim.get('coverage')!r}")
        if claim.get("confidence") not in CONFIDENCE:
            errors.append(f"claim {claim_id}: invalid confidence {claim.get('confidence')!r}")
        if claim.get("status") not in CLAIM_STATUS:
            errors.append(f"claim {claim_id}: invalid status {claim.get('status')!r}")
        if claim.get("directness") not in DIRECTNESS:
            errors.append(f"claim {claim_id}: invalid directness {claim.get('directness')!r}")
        for field in REQUIRED_CLAIM_LISTS:
            if not isinstance(claim.get(field), list):
                errors.append(f"claim {claim_id}: {field} must be a list")
        linked = claim.get("source_ids")
        if not isinstance(linked, list) or not linked:
            errors.append(f"claim {claim_id}: source_ids must be non-empty")
            linked = []
        for source_id in linked:
            source = sources.get(source_id)
            if not source:
                errors.append(f"claim {claim_id}: unknown source {source_id}")
            elif source.get("creator_id") != creator_id:
                errors.append(
                    f"claim {claim_id}: source {source_id} belongs to {source.get('creator_id')}, not {creator_id}"
                )
        if set(claim) & CLAIM_SOURCE_METADATA_FIELDS:
            errors.append(
                f"claim {claim_id}: duplicates canonical source metadata fields {sorted(set(claim) & CLAIM_SOURCE_METADATA_FIELDS)}"
            )
        if claim.get("status") == "quarantined" and not claim.get("warnings"):
            errors.append(f"claim {claim_id}: quarantined claim requires warnings")
        if claim.get("statement_type") == "secondary_summary" and claim.get("directness") != "secondary":
            errors.append(f"claim {claim_id}: secondary summary must use secondary directness")
        if claim.get("evidence_modality") == "secondary_summary" and claim.get("confidence") == "high":
            errors.append(f"claim {claim_id}: secondary summary cannot be high confidence")
        if claim.get("coverage") in {"title_description_only", "related_collection_metadata", "channel_metadata_only"} and not claim.get("warnings"):
            errors.append(f"claim {claim_id}: metadata-level claim requires an evidence warning")
        if claim.get("status") == "active":
            active_by_creator[str(creator_id)] += 1
    missing_active = sorted(FIXED_ROSTER - set(active_by_creator))
    if missing_active:
        errors.append(f"claims: creators without an active claim: {', '.join(missing_active)}")
    return index


def validate_governance(
    routing: dict[str, Any], disagreements: list[dict[str, Any]],
    commercial: list[dict[str, Any]], integrity: dict[str, Any],
    creators: dict[str, dict[str, Any]], sources: dict[str, dict[str, Any]],
    claims: dict[str, dict[str, Any]], errors: list[str],
) -> None:
    route_ids: set[str] = set()
    for position, route in enumerate(routing.get("routes", []), 1):
        route_id = route.get("route_id")
        if not isinstance(route_id, str) or not route_id:
            errors.append(f"routing record {position}: route_id required")
            continue
        if route_id in route_ids:
            errors.append(f"routing: duplicate route_id {route_id}")
        route_ids.add(route_id)
        for field in ("primary", "secondary"):
            values = route.get(field)
            if not isinstance(values, list):
                errors.append(f"route {route_id}: {field} must be a list")
                continue
            unknown = sorted(set(values) - set(creators))
            if unknown:
                errors.append(f"route {route_id}: unknown {field} creators {unknown}")
    if routing.get("default_language") != "zh-CN":
        errors.append("routing: default_language must be zh-CN")

    disagreement_index = unique_index(disagreements, "disagreement_id", "disagreement", errors)
    for disagreement_id, item in disagreement_index.items():
        positions = item.get("positions")
        if not isinstance(positions, list) or len(positions) < 2:
            errors.append(f"disagreement {disagreement_id}: at least two positions required")
            continue
        for position in positions:
            for claim_id in position.get("claim_ids", []):
                if claim_id not in claims:
                    errors.append(f"disagreement {disagreement_id}: unknown claim {claim_id}")

    commercial_index = unique_index(commercial, "conflict_id", "commercial conflict", errors)
    commercial_creators: list[str] = []
    for conflict_id, item in commercial_index.items():
        creator_id = item.get("creator_id")
        commercial_creators.append(str(creator_id))
        if creator_id not in creators:
            errors.append(f"commercial conflict {conflict_id}: unknown creator {creator_id!r}")
        for source_id in item.get("source_ids", []):
            if source_id not in sources:
                errors.append(f"commercial conflict {conflict_id}: unknown source {source_id}")
    if set(commercial_creators) != set(creators) or len(commercial_creators) != len(creators):
        errors.append("commercial conflicts: require exactly one record per creator")

    for rule in integrity.get("forbidden", []):
        for claim_id in rule.get("quarantined_claim_ids", []):
            if claim_id not in claims:
                errors.append(f"integrity rule {rule.get('rule_id')}: unknown claim {claim_id}")
            elif claims[claim_id].get("status") != "quarantined":
                errors.append(f"integrity rule {rule.get('rule_id')}: {claim_id} is not quarantined")


def semantic_errors(require_content: bool = False) -> tuple[list[str], dict[str, int]]:
    errors: list[str] = []
    creators_data = load_json(CREATORS, errors)
    false_positives = load_json(FALSE_POSITIVES, errors)
    routing = load_json(ROUTING, errors)
    integrity = load_json(INTEGRITY, errors)
    source_records = load_jsonl(SOURCES, errors)
    claim_records = load_jsonl(CLAIMS, errors)
    disagreement_records = load_jsonl(DISAGREEMENTS, errors)
    commercial_records = load_jsonl(COMMERCIAL, errors)

    creators = validate_creators(creators_data, errors)
    sources = validate_sources(source_records, creators, false_positives, errors)
    claims = validate_claims(claim_records, creators, sources, errors)
    validate_governance(
        routing, disagreement_records, commercial_records, integrity,
        creators, sources, claims, errors,
    )
    if require_content:
        if len(creators) != 12:
            errors.append(f"--require-content: expected 12 creators, got {len(creators)}")
        if not sources:
            errors.append("--require-content: no sources")
        if not claims:
            errors.append("--require-content: no claims")
        if not any(item.get("evidence_modality") == "creator_transcript" and item.get("status") == "active" for item in claims.values()):
            errors.append("--require-content: no active transcript-grounded claim")
    stats = {
        "creators": len(creators), "sources": len(sources), "claims": len(claims),
        "active": sum(item.get("status") == "active" for item in claims.values()),
        "context_only": sum(item.get("status") == "context_only" for item in claims.values()),
        "quarantined": sum(item.get("status") == "quarantined" for item in claims.values()),
        "disagreements": len(disagreement_records), "commercial_conflicts": len(commercial_records),
    }
    return errors, stats


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-content", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    errors, stats = semantic_errors(args.require_content)
    if errors:
        print("\n".join(f"ERROR: {item}" for item in errors), file=sys.stderr)
        return 1
    print(
        "PASS: "
        f"{stats['creators']} creators, {stats['sources']} sources, {stats['claims']} claims "
        f"({stats['active']} active, {stats['context_only']} context, {stats['quarantined']} quarantined), "
        f"{stats['disagreements']} disagreement records, {stats['commercial_conflicts']} disclosures"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
