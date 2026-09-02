#!/usr/bin/env python3
"""Adversarial tests for the causal-ML readiness CLI."""

from __future__ import annotations

import ast
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/audit_causal_ml.py"
BASE = [
    "--question", "Does outreach change six-month retention?",
    "--treatment", "outreach offer", "--outcome", "six-month retention",
    "--unit", "eligible participant", "--time-zero", "eligibility date",
    "--estimand", "ate", "--design", "observational",
    "--identification-assumption", "conditional exchangeability given baseline need",
    "--control", "baseline need", "--overlap-check", "propensity distribution by outcome-blind strata",
    "--sensitivity", "robustness value and negative control", "--split-plan", "five-fold cross-fitting",
    "--nuisance-evaluation", "out-of-fold calibration and loss", "--use-dml", "--owner", "evaluation lead",
]


def run(*extra: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run([sys.executable, str(SCRIPT), *BASE, *extra], capture_output=True, check=check, timeout=10)


def payload(*extra: str) -> dict[str, object]:
    return json.loads(run(*extra).stdout)


class CausalReadinessAdversarialTests(unittest.TestCase):
    def test_deterministic_output_and_normalization(self) -> None:
        one = run("--control", "  Baseline   Need ", "--control", "baseline need").stdout
        two = run("--control", "baseline need").stdout
        self.assertEqual(one, two)

    def test_exact_claim_layer_marks_synthesis(self) -> None:
        self.assertEqual(payload()["claim_layer"], "D-Skill operational synthesis")

    def test_ready_is_only_estimation_plan(self) -> None:
        result = payload()
        self.assertEqual(result["decision"]["status"], "READY_FOR_ESTIMATION_PLAN")
        self.assertIn("not create identification", result["methods"]["dml_boundary"])

    def test_post_treatment_control_blocks(self) -> None:
        result = payload("--post-treatment-control", "engagement after outreach")
        self.assertEqual(result["decision"]["status"], "BLOCKED_POST_TREATMENT_BIAS")

    def test_hidden_confounding_concern_blocks_even_with_sensitivity(self) -> None:
        result = payload("--unobserved-confounding-concern")
        self.assertEqual(result["decision"]["status"], "BLOCKED_UNIDENTIFIED_CONFOUNDING")

    def test_interference_concern_blocks(self) -> None:
        self.assertEqual(payload("--interference-concern")["decision"]["status"], "BLOCKED_INTERFERENCE")

    def test_dml_without_split_and_nuisance_plan_blocks(self) -> None:
        args = [item for item in BASE if item not in {"--split-plan", "five-fold cross-fitting", "--nuisance-evaluation", "out-of-fold calibration and loss"}]
        result = json.loads(subprocess.run([sys.executable, str(SCRIPT), *args], check=True, capture_output=True).stdout)
        self.assertIn("dml-implementation", result["decision"]["blocking_gates"])

    def test_missing_overlap_blocks(self) -> None:
        args = [item for item in BASE if item not in {"--overlap-check", "propensity distribution by outcome-blind strata"}]
        result = json.loads(subprocess.run([sys.executable, str(SCRIPT), *args], check=True, capture_output=True).stdout)
        self.assertEqual(result["decision"]["status"], "BLOCKED_DESIGN")

    def test_cate_requires_heterogeneity_plan(self) -> None:
        args = ["cate" if item == "ate" else item for item in BASE]
        result = json.loads(subprocess.run([sys.executable, str(SCRIPT), *args], check=True, capture_output=True).stdout)
        self.assertIn("heterogeneity", result["decision"]["blocking_gates"])

    def test_transport_target_requires_transport_assumption(self) -> None:
        result = payload("--transport-target", "next-year regional population")
        self.assertIn("transport", result["decision"]["blocking_gates"])

    def test_high_stakes_never_auto_approves(self) -> None:
        result = payload("--high-stakes", "--policy-use", "benefit eligibility policy")
        self.assertEqual(result["decision"]["status"], "GOVERNANCE_REVIEW_REQUIRED")

    def test_source_has_no_unsafe_execution_and_help_works(self) -> None:
        source = SCRIPT.read_text(encoding="utf-8")
        ast.parse(source)
        self.assertNotIn("shell=True", source)
        self.assertIn(b"usage:", subprocess.run([sys.executable, str(SCRIPT), "--help"], check=True, capture_output=True).stdout)


if __name__ == "__main__":
    unittest.main()
