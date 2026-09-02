from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "retrieve_knowledge.py"
SPEC = importlib.util.spec_from_file_location("retrieve_knowledge_integration", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class CorpusIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.claims = MODULE.load_jsonl(
            ROOT / "references" / "knowledge" / "claims.jsonl"
        )
        cls.sources = MODULE.load_source_map(
            ROOT / "references" / "sources" / "content-index.jsonl"
        )

    def test_ai_reading_retrieves_repeated_three_step_method(self) -> None:
        ranked = MODULE.rank_records("怎么用AI阅读文献并做论文矩阵", self.claims, 5)
        self.assertTrue(ranked)
        self.assertEqual(ranked[0]["claim_id"], "ZC-0032")
        self.assertEqual(ranked[0]["evidence_level"], "synthesis")

    def test_uncovered_group_meeting_question_returns_no_evidence(self) -> None:
        ranked = MODULE.rank_records("组会汇报PPT怎么做", self.claims, 8)
        self.assertEqual(ranked, [])

    def test_uncovered_grant_budget_question_returns_no_evidence(self) -> None:
        ranked = MODULE.rank_records("国自然基金预算怎么编", self.claims, 8)
        self.assertEqual(ranked, [])

    def test_every_current_claim_keeps_provisional_provenance(self) -> None:
        self.assertTrue(self.claims)
        self.assertTrue(
            all(
                item.get("verification_status") == "provisional_diandian_mediated"
                for item in self.claims
            )
        )

    def test_unverified_export_url_is_not_rendered_as_canonical_link(self) -> None:
        ranked = MODULE.rank_records("怎么用AI阅读文献并做论文矩阵", self.claims, 1)
        rendered = MODULE.render_text(ranked, Path("claims.jsonl"), self.sources)
        self.assertIn("canonical source URL pending", rendered)
        self.assertNotIn("https://www.xiaohongshu.com/explore/N264", rendered)


if __name__ == "__main__":
    unittest.main()
