from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "retrieve_knowledge.py"
SPEC = importlib.util.spec_from_file_location("retrieve_knowledge", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class RetrieveKnowledgeTests(unittest.TestCase):
    def test_empty_index_has_no_results(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            index = Path(directory) / "claims.jsonl"
            index.write_text("", encoding="utf-8")
            self.assertEqual(MODULE.rank_records("文献阅读", MODULE.load_jsonl(index), 8), [])

    def test_relevant_direct_claim_ranks_first(self) -> None:
        records = [
            {
                "claim_id": "ZC-0001",
                "statement": "先按研究问题筛选文献，再做精读。",
                "evidence_level": "direct",
                "source_ids": ["ZS-0001"],
                "topics": ["文献阅读"],
                "actions": ["筛选", "精读"],
            },
            {
                "claim_id": "ZC-0002",
                "statement": "汇报前检查幻灯片结构。",
                "evidence_level": "direct",
                "source_ids": ["ZS-0002"],
                "topics": ["组会"],
                "actions": ["检查PPT"],
            },
        ]
        ranked = MODULE.rank_records("文献应该怎么阅读", records, 2)
        self.assertEqual(ranked[0]["claim_id"], "ZC-0001")

    def test_uncovered_query_does_not_match_question_filler(self) -> None:
        records = [
            {
                "claim_id": "ZC-0001",
                "statement": "怎么写文献综述并综合研究争议。",
                "evidence_level": "direct",
                "source_ids": ["ZS-0001"],
                "topics": ["文献综述"],
                "actions": ["综合证据"],
            }
        ]
        self.assertEqual(MODULE.rank_records("组会汇报PPT怎么做", records, 8), [])

    def test_invalid_json_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            index = Path(directory) / "claims.jsonl"
            index.write_text(json.dumps(["not an object"]) + "\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                MODULE.load_jsonl(index)


if __name__ == "__main__":
    unittest.main()
