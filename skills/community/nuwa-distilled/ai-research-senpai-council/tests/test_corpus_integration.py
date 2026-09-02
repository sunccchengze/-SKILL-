from __future__ import annotations

import importlib.util
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "retrieve_council.py"
SPEC = importlib.util.spec_from_file_location("retrieve_council_integration", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class CorpusIntegrationTests(unittest.TestCase):
    def test_literature_review_has_direct_multicreator_evidence(self) -> None:
        payload = MODULE.build_payload("怎么用AI做文献综述并核验引用？", top_k=8)
        self.assertEqual(payload["default_response_language"], "zh-CN")
        self.assertEqual(payload["evidence_status"], "grounded")
        creators = {item["creator_id"] for item in payload["results"]}
        self.assertIn("amina-yonis", creators)
        self.assertIn("james-hayton", creators)
        self.assertTrue(any(item["recommendation_ready"] for item in payload["results"]))
        self.assertTrue(all(item["status"] != "quarantined" for item in payload["results"]))
        self.assertTrue(all(item.get("sources") for item in payload["results"]))
        self.assertIn("DIS-001", {item["disagreement_id"] for item in payload["disagreements"]})

    def test_results_never_exceed_two_claims_per_creator(self) -> None:
        payload = MODULE.build_payload("文献综述检索阅读写作引用怎么做", top_k=12)
        counts = Counter(item["creator_id"] for item in payload["results"])
        self.assertTrue(counts)
        self.assertLessEqual(max(counts.values()), 2)

    def test_uncovered_grant_budget_abstains(self) -> None:
        payload = MODULE.build_payload("国自然基金预算怎么编？", top_k=8)
        self.assertEqual(payload["evidence_status"], "abstain")
        self.assertEqual(payload["results"], [])
        self.assertIn("通用科研建议", payload["abstention"])

    def test_detector_evasion_is_flagged_and_quarantine_is_not_routed(self) -> None:
        payload = MODULE.build_payload("怎么用AI detector bypass让学校查不出来？")
        self.assertEqual(payload["integrity_alerts"][0]["category"], "detector_evasion")
        self.assertNotIn(
            "ARC-0035", {item["claim_id"] for item in payload["results"]}
        )
        self.assertNotIn(
            "ARC-0057", {item["claim_id"] for item in payload["results"]}
        )

    def test_commercial_query_returns_complete_disclosure_ledger(self) -> None:
        payload = MODULE.build_payload("哪些成员有付费课程或商业利益冲突？", top_k=12)
        self.assertEqual(len(payload["commercial_disclosures"]), 12)
        by_creator = {item["creator_id"]: item for item in payload["commercial_disclosures"]}
        self.assertEqual(by_creator["amina-yonis"]["level"], "high")
        self.assertEqual(by_creator["andy-stapleton"]["level"], "high")

    def test_qualitative_contradiction_routes_to_kriukow(self) -> None:
        payload = MODULE.build_payload("质性访谈里参与者前后矛盾怎么办？", top_k=6)
        self.assertEqual(payload["results"][0]["creator_id"], "kriukow")
        self.assertTrue(payload["results"][0]["recommendation_ready"])


if __name__ == "__main__":
    unittest.main()
