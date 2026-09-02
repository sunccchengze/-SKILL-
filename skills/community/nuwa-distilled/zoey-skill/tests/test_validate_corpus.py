from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_corpus.py"
SPEC = importlib.util.spec_from_file_location("validate_corpus", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def source(
    source_id: str = "ZS-0001",
    *,
    level: str = "first_party_partial",
    membership: str = "included_provisional",
    eligible: bool = True,
) -> dict:
    return {
        "source_id": source_id,
        "url": "https://example.invalid/export-locator",
        "url_status": "unverified_export_url",
        "title": "test",
        "source_level": level,
        "corpus_membership": membership,
        "evidence_eligible": eligible,
        "status": "partial",
        "extraction": {},
    }


def claim(source_ids: list[str] | None = None, level: str = "direct") -> dict:
    return {
        "claim_id": "ZC-0001",
        "statement": "test statement",
        "evidence_level": level,
        "confidence": "medium",
        "verification_status": "provisional_diandian_mediated",
        "source_ids": source_ids or ["ZS-0001"],
        "topics": [],
        "keywords": [],
        "audiences": [],
        "conditions": [],
        "actions": [],
        "warnings": [],
        "tools": [],
    }


def coverage(source_id: str = "ZS-0001") -> dict[str, str]:
    return {"source_id": source_id, "status": "partial"}


class ValidateCorpusTests(unittest.TestCase):
    def test_valid_provisional_direct_claim_passes(self) -> None:
        errors = MODULE.semantic_errors([source()], [claim()], [coverage()], True)
        self.assertEqual(errors, [])

    def test_metadata_source_cannot_support_direct_claim(self) -> None:
        errors = MODULE.semantic_errors(
            [source(level="first_party_metadata", eligible=False)],
            [claim()],
            [coverage()],
        )
        self.assertTrue(any("not evidence eligible" in item for item in errors))
        self.assertTrue(any("direct claim cannot use" in item for item in errors))

    def test_excluded_source_cannot_support_claim(self) -> None:
        errors = MODULE.semantic_errors(
            [source(membership="excluded", eligible=False)],
            [claim()],
            [coverage()],
        )
        self.assertTrue(any("not included_provisional" in item for item in errors))

    def test_synthesis_requires_two_sources(self) -> None:
        errors = MODULE.semantic_errors(
            [source()], [claim(level="synthesis")], [coverage()]
        )
        self.assertTrue(any("requires at least two sources" in item for item in errors))


if __name__ == "__main__":
    unittest.main()
