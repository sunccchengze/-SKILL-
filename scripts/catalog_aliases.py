#!/usr/bin/env python3
"""Shared helpers for provenance-preserving catalog alias suppression."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
POLICY_PATH = REPO / "catalog" / "overlap-policy.json"


def load_alias_index() -> dict[str, dict[str, str]]:
    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    return {str(alias["path"]): alias for alias in policy["aliases"]}


def annotate_alias(
    record: dict[str, Any], alias_index: dict[str, dict[str, str]]
) -> dict[str, Any]:
    """Return a record carrying alias metadata without mutating raw catalogs."""
    alias = alias_index.get(str(record["path"]))
    if not alias:
        return record
    annotated = dict(record)
    annotated["searchVisibility"] = "alias"
    annotated["aliasOf"] = alias["canonicalPath"]
    annotated["aliasReason"] = alias["reason"]
    annotated["aliasEvidence"] = alias["evidence"]
    return annotated


def is_alias(record: dict[str, Any]) -> bool:
    return record.get("searchVisibility") == "alias"
