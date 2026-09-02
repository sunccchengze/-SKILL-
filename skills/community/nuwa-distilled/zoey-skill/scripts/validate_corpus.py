#!/usr/bin/env python3
"""Validate Zoey source, coverage, and atomic-claim ledgers."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

SKILL_DIR = Path(__file__).resolve().parents[1]
SOURCE_INDEX = SKILL_DIR / "references" / "sources" / "content-index.jsonl"
COVERAGE = SKILL_DIR / "references" / "sources" / "coverage.csv"
CLAIMS = SKILL_DIR / "references" / "knowledge" / "claims.jsonl"

EVIDENCE_LEVELS = {"direct", "synthesis", "inference"}
CONFIDENCE_LEVELS = {"high", "medium", "low"}
SOURCE_LEVELS = {
    "first_party_complete",
    "first_party_partial",
    "first_party_metadata",
    "secondary",
    "inference",
}
CORPUS_MEMBERSHIPS = {"included_provisional", "excluded"}
URL_STATUSES = {"verified", "unverified_export_url", "unavailable"}
COVERAGE_STATUSES = {
    "discovered",
    "accessed",
    "extracted",
    "verified",
    "partial",
    "unavailable",
}
ELIGIBLE_DIRECT_LEVELS = {"first_party_complete", "first_party_partial"}
LIST_FIELDS = {
    "source_ids",
    "topics",
    "keywords",
    "audiences",
    "conditions",
    "actions",
    "warnings",
    "tools",
}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--require-content",
        action="store_true",
        help="fail unless the corpus has at least one source, claim, and eligible source",
    )
    return parser.parse_args(argv)


def load_jsonl(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    records: list[dict[str, Any]] = []
    errors: list[str] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, raw in enumerate(handle, 1):
            if not raw.strip():
                continue
            try:
                value = json.loads(raw)
            except json.JSONDecodeError as exc:
                errors.append(f"{path}:{line_number}: invalid JSON: {exc}")
                continue
            if not isinstance(value, dict):
                errors.append(f"{path}:{line_number}: expected object")
                continue
            records.append(value)
    return records, errors


def duplicate_errors(records: list[dict[str, Any]], field: str, label: str) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for position, record in enumerate(records, 1):
        value = record.get(field)
        if not isinstance(value, str) or not value:
            errors.append(f"{label} record {position}: missing {field}")
        elif value in seen:
            errors.append(f"{label} record {position}: duplicate {field} {value}")
        else:
            seen.add(value)
    return errors


def semantic_errors(
    sources: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    coverage_rows: list[dict[str, str]],
    require_content: bool = False,
) -> list[str]:
    """Return cross-ledger and evidence-eligibility errors."""
    errors: list[str] = []
    errors.extend(duplicate_errors(sources, "source_id", "source"))
    errors.extend(duplicate_errors(claims, "claim_id", "claim"))

    source_by_id = {
        record["source_id"]: record
        for record in sources
        if isinstance(record.get("source_id"), str) and record["source_id"]
    }
    source_ids = set(source_by_id)

    for record in sources:
        source_id = record.get("source_id", "<unknown>")
        if not record.get("url") or not record.get("title"):
            errors.append(f"source {source_id}: url and title are required")
        if record.get("source_level") not in SOURCE_LEVELS:
            errors.append(
                f"source {source_id}: invalid source_level {record.get('source_level')!r}"
            )
        membership = record.get("corpus_membership")
        if membership not in CORPUS_MEMBERSHIPS:
            errors.append(
                f"source {source_id}: invalid corpus_membership {membership!r}"
            )
        eligible = record.get("evidence_eligible")
        if not isinstance(eligible, bool):
            errors.append(f"source {source_id}: evidence_eligible must be boolean")
        if membership == "excluded" and eligible is not False:
            errors.append(f"source {source_id}: excluded source cannot be evidence eligible")
        if record.get("source_level") in {"first_party_metadata", "secondary", "inference"} and eligible is True:
            errors.append(
                f"source {source_id}: {record.get('source_level')} cannot be evidence eligible"
            )
        if record.get("url_status") not in URL_STATUSES:
            errors.append(
                f"source {source_id}: invalid url_status {record.get('url_status')!r}"
            )
        extraction = record.get("extraction")
        if not isinstance(extraction, dict):
            errors.append(f"source {source_id}: extraction must be an object")

    for record in claims:
        claim_id = record.get("claim_id", "<unknown>")
        if not record.get("statement"):
            errors.append(f"claim {claim_id}: statement is required")
        level = record.get("evidence_level")
        if level not in EVIDENCE_LEVELS:
            errors.append(f"claim {claim_id}: invalid evidence_level {level!r}")
        confidence = record.get("confidence")
        if confidence not in CONFIDENCE_LEVELS:
            errors.append(f"claim {claim_id}: invalid confidence {confidence!r}")
        if not record.get("verification_status"):
            errors.append(f"claim {claim_id}: verification_status is required")
        for field in LIST_FIELDS:
            value = record.get(field)
            if not isinstance(value, list):
                errors.append(f"claim {claim_id}: {field} must be a list")

        linked = record.get("source_ids")
        if not isinstance(linked, list) or not linked:
            errors.append(f"claim {claim_id}: source_ids must be a non-empty list")
            continue
        unknown = sorted(set(linked) - source_ids)
        if unknown:
            errors.append(f"claim {claim_id}: unknown sources {', '.join(unknown)}")
        if level == "synthesis" and len(set(linked)) < 2:
            errors.append(f"claim {claim_id}: synthesis requires at least two sources")

        linked_sources = [source_by_id[item] for item in set(linked) if item in source_by_id]
        for source in linked_sources:
            source_id = source["source_id"]
            if source.get("corpus_membership") != "included_provisional":
                errors.append(
                    f"claim {claim_id}: source {source_id} is not included_provisional"
                )
            if source.get("evidence_eligible") is not True:
                errors.append(f"claim {claim_id}: source {source_id} is not evidence eligible")
            if level == "direct" and source.get("source_level") not in ELIGIBLE_DIRECT_LEVELS:
                errors.append(
                    f"claim {claim_id}: direct claim cannot use {source.get('source_level')} "
                    f"source {source_id}"
                )
        if confidence == "high":
            for source in linked_sources:
                if source.get("source_level") != "first_party_complete" or source.get("url_status") != "verified":
                    errors.append(
                        f"claim {claim_id}: high confidence requires complete, verified sources"
                    )
                    break

    coverage_ids: set[str] = set()
    coverage_status_by_id: dict[str, str] = {}
    for position, row in enumerate(coverage_rows, 2):
        source_id = row.get("source_id", "")
        if not source_id:
            errors.append(f"coverage row {position}: missing source_id")
            continue
        if source_id in coverage_ids:
            errors.append(f"coverage row {position}: duplicate source_id {source_id}")
        coverage_ids.add(source_id)
        status = row.get("status", "")
        coverage_status_by_id[source_id] = status
        if status not in COVERAGE_STATUSES:
            errors.append(f"coverage row {position}: invalid status {status!r}")

    if source_ids != coverage_ids:
        missing_csv = sorted(source_ids - coverage_ids)
        missing_index = sorted(coverage_ids - source_ids)
        if missing_csv:
            errors.append(f"sources absent from coverage.csv: {', '.join(missing_csv)}")
        if missing_index:
            errors.append(
                f"coverage rows absent from content-index.jsonl: {', '.join(missing_index)}"
            )
    for source_id, source in source_by_id.items():
        if source_id in coverage_status_by_id and source.get("status") != coverage_status_by_id[source_id]:
            errors.append(
                f"source {source_id}: index status {source.get('status')!r} does not match "
                f"coverage status {coverage_status_by_id[source_id]!r}"
            )

    if require_content:
        if not sources:
            errors.append("--require-content: no sources")
        if not claims:
            errors.append("--require-content: no claims")
        if not any(record.get("evidence_eligible") is True for record in sources):
            errors.append("--require-content: no evidence-eligible sources")

    return errors


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    missing = [path for path in (SOURCE_INDEX, COVERAGE, CLAIMS) if not path.exists()]
    if missing:
        for path in missing:
            print(f"ERROR: missing required file: {path}", file=sys.stderr)
        return 1

    sources, source_errors = load_jsonl(SOURCE_INDEX)
    claims, claim_errors = load_jsonl(CLAIMS)
    with COVERAGE.open(newline="", encoding="utf-8") as handle:
        coverage_rows = list(csv.DictReader(handle))

    errors = source_errors + claim_errors
    errors.extend(semantic_errors(sources, claims, coverage_rows, args.require_content))
    if errors:
        print("\n".join(f"ERROR: {item}" for item in errors), file=sys.stderr)
        return 1

    eligible = sum(record.get("evidence_eligible") is True for record in sources)
    excluded = sum(record.get("corpus_membership") == "excluded" for record in sources)
    print(
        f"PASS: {len(sources)} sources ({eligible} eligible, {excluded} excluded), "
        f"{len(claims)} claims, {len(coverage_rows)} coverage rows"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
