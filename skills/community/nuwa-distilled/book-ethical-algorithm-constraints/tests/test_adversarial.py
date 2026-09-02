#!/usr/bin/env python3
"""Adversarial tests for the constrained-algorithm audit CLI."""

from __future__ import annotations

import ast
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/audit_constraint_system.py"
BASE = [
    "--system", "course support allocation", "--decision", "offer additional tutoring",
    "--affected-group", "students", "--protected-group", "students by disability and language",
    "--owner", "academic services lead", "--stakes", "low", "--legal-basis", "institutional support mandate",
    "--privacy-unit", "one student's participation", "--neighboring-relation", "datasets differ by one student record",
    "--epsilon", "1.0", "--delta", "0.000001", "--query-count", "4",
    "--fairness-goal", "calibration", "--base-rate-difference", "unknown",
    "--harm", "unequal access to support", "--appeal-path", "student services review",
    "--human-review", "advisor checks context", "--stop-condition", "appeal disparity exceeds threshold",
]


def run(*extra: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run([sys.executable, str(SCRIPT), *BASE, *extra], capture_output=True, check=check, timeout=10)


def payload(*extra: str) -> dict[str, object]:
    return json.loads(run(*extra).stdout)


class EthicalConstraintAdversarialTests(unittest.TestCase):
    def test_deterministic_normalized_groups(self) -> None:
        one = run("--affected-group", "  Students ", "--affected-group", "students").stdout
        two = run("--affected-group", "students").stdout
        self.assertEqual(one, two)

    def test_exact_claim_layer_is_operational_synthesis(self) -> None:
        self.assertEqual(payload()["claim_layer"], "D-Skill operational synthesis")

    def test_valid_spec_requires_governance_not_approval(self) -> None:
        result = payload()
        self.assertEqual(result["decision_gate"]["status"], "GOVERNANCE_REVIEW_REQUIRED")
        self.assertIn("deployment approval", result["decision_gate"]["does_not_mean"])

    def test_dp_without_neighboring_relation_blocks(self) -> None:
        removed = {"--neighboring-relation", "datasets differ by one student record"}
        args = [item for item in BASE if item not in removed]
        result = json.loads(subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, check=True).stdout)
        self.assertIn("privacy-neighboring-relation-unspecified", result["decision_gate"]["blocks"])

    def test_dp_without_composition_count_blocks(self) -> None:
        removed = {"--query-count", "4"}
        args = [item for item in BASE if item not in removed]
        result = json.loads(subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, check=True).stdout)
        self.assertIn("privacy-composition-count-missing", result["decision_gate"]["blocks"])

    def test_conflicting_fairness_goals_require_tradeoff(self) -> None:
        result = payload("--fairness-goal", "equalized-odds", "--base-rate-difference", "yes")
        self.assertEqual(result["decision_gate"]["status"], "TRADEOFF_DECISION_REQUIRED")

    def test_fairness_without_groups_blocks(self) -> None:
        removed = {"--protected-group", "students by disability and language"}
        args = [item for item in BASE if item not in removed]
        result = json.loads(subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, check=True).stdout)
        self.assertIn("fairness-groups-unspecified", result["decision_gate"]["blocks"])

    def test_high_stakes_without_due_process_blocks(self) -> None:
        removed = {"--appeal-path", "student services review", "--human-review", "advisor checks context", "--stop-condition", "appeal disparity exceeds threshold"}
        args = ["high" if item == "low" else item for item in BASE if item not in removed]
        result = json.loads(subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, check=True).stdout)
        self.assertIn("high-stakes-due-process-incomplete", result["decision_gate"]["blocks"])

    def test_medium_stakes_requires_dynamic_response_and_monitoring(self) -> None:
        args = ["medium" if item == "low" else item for item in BASE]
        result = json.loads(subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, check=True).stdout)
        self.assertIn("strategic-response-unmodeled", result["decision_gate"]["blocks"])
        self.assertIn("performative-feedback-unmonitored", result["decision_gate"]["blocks"])

    def test_adaptive_holdout_reuse_without_fresh_control_blocks(self) -> None:
        result = payload("--data-reuse-count", "5")
        self.assertIn("adaptive-holdout-validity-uncontrolled", result["decision_gate"]["blocks"])

    def test_invalid_privacy_parameters_fail_closed(self) -> None:
        completed = run("--epsilon", "-1", check=False)
        self.assertNotEqual(completed.returncode, 0)

    def test_source_is_dependency_free_and_help_works(self) -> None:
        source = SCRIPT.read_text(encoding="utf-8")
        ast.parse(source)
        self.assertNotIn("shell=True", source)
        self.assertIn(b"usage:", subprocess.run([sys.executable, str(SCRIPT), "--help"], check=True, capture_output=True).stdout)


if __name__ == "__main__":
    unittest.main()
