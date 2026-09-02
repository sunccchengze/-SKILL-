from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_corpus.py"
SPEC = importlib.util.spec_from_file_location("validate_corpus", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ValidateCorpusTests(unittest.TestCase):
    def test_real_corpus_passes_deep_validation(self) -> None:
        errors, stats = MODULE.semantic_errors(require_content=True)
        self.assertEqual(errors, [])
        self.assertEqual(stats["creators"], 12)
        self.assertGreater(stats["claims"], 0)
        self.assertGreater(stats["sources"], 0)
        self.assertGreater(stats["quarantined"], 0)

    def test_false_positive_content_id_is_rejected(self) -> None:
        errors: list[str] = []
        creators = {"creator": {"creator_id": "creator"}}
        false_positives = {
            "exclusions": [
                {"content_id": "bad-video", "decision": "exclude"}
            ]
        }
        source = {
            "source_id": "SRC-BAD",
            "creator_id": "creator",
            "platform": "youtube",
            "content_id": "bad-video",
            "title": "bad",
            "url": "https://example.invalid/bad",
            "fetched_at": "2026-08-16",
            "notes": "test",
            "modality": "creator_transcript",
            "directness": "direct",
            "status": "live",
            "original_uploader": True,
        }
        MODULE.validate_sources([source], creators, false_positives, errors)
        self.assertTrue(any("re-entered ledger" in item for item in errors))

    def test_claim_cannot_duplicate_source_url(self) -> None:
        errors: list[str] = []
        creators = {"creator": {"creator_id": "creator"}}
        sources = {"SRC-1": {"source_id": "SRC-1", "creator_id": "creator"}}
        record = {
            "claim_id": "CLAIM-1",
            "creator_id": "creator",
            "statement": "test",
            "checked_at": "2026-08-16",
            "statement_type": "creator_statement",
            "evidence_modality": "creator_transcript",
            "coverage": "full_transcript",
            "confidence": "high",
            "status": "active",
            "directness": "direct",
            "source_ids": ["SRC-1"],
            "topics": [],
            "keywords": [],
            "route_tags": [],
            "actions": [],
            "warnings": [],
            "url": "https://example.invalid/duplicated",
        }
        MODULE.validate_claims([record], creators, sources, errors)
        self.assertTrue(any("duplicates canonical source metadata" in item for item in errors))

    def test_integrity_rule_requires_quarantined_claim(self) -> None:
        errors: list[str] = []
        MODULE.validate_governance(
            {"default_language": "zh-CN", "routes": []},
            [],
            [],
            {"forbidden": [{"rule_id": "INT-X", "quarantined_claim_ids": ["C-1"]}]},
            {},
            {},
            {"C-1": {"status": "active"}},
            errors,
        )
        self.assertTrue(any("is not quarantined" in item for item in errors))


if __name__ == "__main__":
    unittest.main()
