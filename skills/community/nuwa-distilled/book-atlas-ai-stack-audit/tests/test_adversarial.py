#!/usr/bin/env python3
"""Adversarial tests for the Atlas full-stack audit CLI."""

from __future__ import annotations

import ast
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/audit_ai_stack.py"
BASE = [
    "--system", "municipal document triage", "--purpose", "route service requests",
    "--geography", "Hong Kong", "--as-of", "2026-08-16", "--owner", "service director",
    "--lifecycle-stage", "proposal", "--supply-node", "cloud region and device disposal chain",
    "--worker-group", "contract annotators", "--data-source", "resident submissions",
    "--classification", "service category taxonomy", "--affected-group", "residents and frontline staff",
    "--state-linkage", "public procurement and records retention", "--material-evidence", "provider region inventory",
    "--labor-evidence", "contract terms and worker interview protocol", "--provenance-evidence", "dataset lineage register",
    "--remedy", "human reroute and appeal", "--claim-denominator", "annual service workload",
    "--stop-condition", "material disparity or untraceable source",
]


def run(*extra: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run([sys.executable, str(SCRIPT), *BASE, *extra], capture_output=True, check=True, timeout=10)


def payload(*extra: str) -> dict[str, object]:
    return json.loads(run(*extra).stdout)


class AtlasStackAdversarialTests(unittest.TestCase):
    def test_deterministic_normalized_evidence(self) -> None:
        one = run("--data-source", "  Resident   Submissions ", "--data-source", "resident submissions").stdout
        two = run("--data-source", "resident submissions").stdout
        self.assertEqual(one, two)

    def test_exact_claim_layer_is_skill_synthesis(self) -> None:
        self.assertEqual(payload()["claim_layer"], "D-Skill operational synthesis")

    def test_complete_map_requires_governance_not_approval(self) -> None:
        result = payload()
        self.assertEqual(result["decision"]["status"], "GOVERNANCE_REVIEW_REQUIRED")
        self.assertIn("ethical approval", result["decision"]["does_not_mean"])

    def test_emotion_inference_blocks_on_construct_validity(self) -> None:
        result = payload("--emotion-inference")
        self.assertEqual(result["decision"]["status"], "BLOCKED_SCIENTIFIC_VALIDITY_REVIEW")

    def test_undocumented_third_party_blocks_provenance(self) -> None:
        self.assertEqual(payload("--undocumented-third-party")["decision"]["status"], "BLOCKED_PROVENANCE")

    def test_high_stakes_biometric_use_blocks_rights_review(self) -> None:
        result = payload("--biometric-classification", "--high-stakes")
        self.assertEqual(result["decision"]["status"], "BLOCKED_RIGHTS_REVIEW")

    def test_worker_voice_absence_is_not_completed_by_vendor_document(self) -> None:
        result = payload("--missing-worker-voice")
        self.assertIn("labor", result["decision"]["gaps"])
        self.assertIn("worker-voice-absent", result["decision"]["red_flags"])

    def test_missing_denominator_makes_earth_lens_incomplete(self) -> None:
        args = [item for item in BASE if item not in {"--claim-denominator", "annual service workload"}]
        result = json.loads(subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, check=True).stdout)
        self.assertIn("earth", result["decision"]["gaps"])

    def test_missing_appeal_and_stop_makes_power_lens_incomplete(self) -> None:
        removed = {"--remedy", "human reroute and appeal", "--stop-condition", "material disparity or untraceable source"}
        args = [item for item in BASE if item not in removed]
        result = json.loads(subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, check=True).stdout)
        self.assertIn("power", result["decision"]["gaps"])

    def test_lenses_cover_all_eight_book_views(self) -> None:
        names = {item["lens"] for item in payload()["lenses"]}
        self.assertEqual(names, {"earth", "labor", "data", "classification", "affect", "state", "power", "space"})

    def test_output_warns_against_per_prompt_allocation(self) -> None:
        self.assertIn("prompt", payload()["quantification_boundary"])

    def test_source_is_dependency_free_and_help_works(self) -> None:
        source = SCRIPT.read_text(encoding="utf-8")
        ast.parse(source)
        self.assertNotIn("shell=True", source)
        self.assertIn(b"usage:", subprocess.run([sys.executable, str(SCRIPT), "--help"], check=True, capture_output=True).stdout)


if __name__ == "__main__":
    unittest.main()
