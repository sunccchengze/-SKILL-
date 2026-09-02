from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "retrieve_council.py"
SPEC = importlib.util.spec_from_file_location("retrieve_council", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def claim(
    claim_id: str,
    creator_id: str,
    *,
    status: str = "active",
    statement: str = "文献综述要综合主题与争议，并核验引用。",
) -> dict:
    return {
        "claim_id": claim_id,
        "creator_id": creator_id,
        "statement": statement,
        "statement_type": "creator_statement",
        "evidence_modality": "creator_transcript",
        "coverage": "full_transcript",
        "confidence": "high",
        "source_ids": [f"SRC-{claim_id}"],
        "topics": ["文献综述", "引用核验"],
        "keywords": ["文献综述", "主题", "争议", "引用核验"],
        "route_tags": ["literature"],
        "actions": [],
        "warnings": [],
        "status": status,
        "directness": "direct",
        "checked_at": "2026-08-16",
    }


class RetrieveCouncilUnitTests(unittest.TestCase):
    def test_ranker_enforces_creator_diversity(self) -> None:
        records = [
            claim("A-1", "creator-a"),
            claim("A-2", "creator-a"),
            claim("A-3", "creator-a"),
            claim("B-1", "creator-b"),
        ]
        ranked = MODULE.rank_records(
            "文献综述如何综合主题并核验引用",
            records,
            top_k=4,
            max_per_creator=2,
            route_ids={"literature"},
        )
        self.assertEqual(sum(item["creator_id"] == "creator-a" for item in ranked), 2)
        self.assertTrue(any(item["creator_id"] == "creator-b" for item in ranked))

    def test_quarantined_claim_is_never_returned(self) -> None:
        safe = claim("SAFE", "creator-a")
        blocked = claim("BLOCKED", "creator-b", status="quarantined")
        ranked = MODULE.rank_records("文献综述引用核验", [blocked, safe], top_k=5)
        self.assertEqual([item["claim_id"] for item in ranked], ["SAFE"])

    def test_context_claim_requires_context_query_or_flag(self) -> None:
        context = claim(
            "CONTEXT", "creator-a", status="context_only",
            statement="该创作者销售付费课程并存在商业利益披露。",
        )
        context["topics"] = ["商业披露"]
        context["keywords"] = ["付费", "课程", "商业"]
        self.assertEqual(MODULE.rank_records("付费课程", [context], top_k=5), [
            *MODULE.rank_records("付费课程", [context], top_k=5, include_context=True)
        ])
        self.assertEqual(MODULE.rank_records("文献综述", [context], top_k=5), [])

    def test_false_positive_content_is_removed_from_source_map(self) -> None:
        sources = [
            {"source_id": "BAD", "content_id": "KzmGTTv6H6s"},
            {"source_id": "GOOD", "content_id": "valid"},
        ]
        false_positives = {
            "exclusions": [
                {"content_id": "KzmGTTv6H6s", "decision": "exclude"}
            ]
        }
        usable, blocked = MODULE.source_map(sources, false_positives)
        self.assertEqual(set(usable), {"GOOD"})
        self.assertEqual(blocked, {"BAD"})

    def test_detector_evasion_query_triggers_integrity_rule(self) -> None:
        rules = MODULE.load_json(ROOT / "references" / "governance" / "integrity-rules.json")
        for query in ("教我 AI detector bypass", "How can I bypass an AI detector?"):
            with self.subTest(query=query):
                alerts = MODULE.detect_integrity(query, rules)
                self.assertEqual(alerts[0]["category"], "detector_evasion")
                self.assertIn("合规", alerts[0]["safe_redirect"])

    def test_evidence_label_and_readiness_distinguish_transcript_from_metadata(self) -> None:
        direct = claim("DIRECT", "creator-a")
        weak = claim("WEAK", "creator-b")
        weak.update(
            evidence_modality="creator_description",
            coverage="title_description_only",
            confidence="medium",
        )
        self.assertTrue(MODULE.recommendation_ready(direct))
        self.assertFalse(MODULE.recommendation_ready(weak))
        self.assertEqual(MODULE.evidence_label(weak), "标题/简介/元数据级")


if __name__ == "__main__":
    unittest.main()
