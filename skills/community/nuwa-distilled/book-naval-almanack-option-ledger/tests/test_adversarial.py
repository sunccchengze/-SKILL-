#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_option_experiment.py"
SPEC = importlib.util.spec_from_file_location("naval_option", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class NavalAdversarialTests(unittest.TestCase):
    def args(self, *extra: str):
        base = ["--proposition", "publish one technical note", "--attribution", "jorgenson-curation", "--source", "official almanack", "--domain", "leverage", "--base-rate", "audience outcomes are skewed", "--access-constraint", "two hours weekly", "--downside-cap", "one draft", "--reversible-test", "publish once", "--success-metric", "three qualified replies", "--harm-metric", "no confidential material", "--stop-condition", "stop on employer conflict", "--review-days", "30", "--stake", "low", "--owner", "experimenter"]
        return MODULE.parser().parse_args(base + list(extra))

    def test_ready_is_reversible_not_promise(self):
        payload = MODULE.build(self.args())
        self.assertEqual(payload["decision"]["status"], "READY_FOR_REVERSIBLE_TEST")
        self.assertIn("No wealth", payload["disclaimer"])

    def test_jorgenson_maps_to_a_layer(self):
        self.assertEqual(MODULE.build(self.args())["attribution"]["layer"], "A")

    def test_naval_primary_requires_primary_check(self):
        args = self.args()
        args.attribution = "naval-primary"
        self.assertEqual(MODULE.build(args)["decision"]["status"], "STOP")
        args.primary_text_checked = True
        self.assertEqual(MODULE.build(args)["decision"]["status"], "READY_FOR_REVERSIBLE_TEST")
        self.assertEqual(MODULE.build(args)["attribution"]["layer"], "B")

    def test_missing_access_constraint_stops(self):
        args = self.args()
        args.access_constraint = []
        self.assertEqual(MODULE.build(args)["decision"]["status"], "STOP")

    def test_invalid_review_window_stops(self):
        args = self.args()
        args.review_days = 0
        self.assertEqual(MODULE.build(args)["decision"]["status"], "STOP")

    def test_high_risk_requires_three_gates_and_never_approves(self):
        args = self.args()
        args.stake = "high"
        self.assertEqual(MODULE.build(args)["decision"]["status"], "STOP")
        args.runway = "documented living and insurance runway"
        args.qualified_reviewer = "qualified local adviser"
        args.dependents_plan = "joint written plan"
        payload = MODULE.build(args)
        self.assertEqual(payload["decision"]["status"], "REVIEW_ONLY")
        self.assertTrue(any("not-approved" in item for item in payload["decision"]["reasons"]))

    def test_personalized_investment_blocks(self):
        self.assertEqual(MODULE.build(self.args("--personalized-investment-advice"))["decision"]["status"], "BLOCKED")

    def test_clinical_substitution_blocks(self):
        self.assertEqual(MODULE.build(self.args("--clinical-treatment"))["decision"]["status"], "BLOCKED")

    def test_crisis_unlawful_and_exploitation_block(self):
        for flag in ("--crisis", "--unlawful", "--exploitative"):
            with self.subTest(flag=flag):
                self.assertEqual(MODULE.build(self.args(flag))["decision"]["status"], "BLOCKED")

    def test_warnings_include_superstar_concentration(self):
        warnings = MODULE.build(self.args())["risk_ledger"]["warnings"]
        self.assertTrue(any("superstar concentration" in item for item in warnings))

    def test_deterministic_and_normalized(self):
        cmd = [sys.executable, str(SCRIPT), "--proposition", " test   option ", "--attribution", "skill-inference", "--source", "ledger", "--domain", "specific-knowledge", "--base-rate", "unknown", "--access-constraint", "b", "--access-constraint", "a", "--access-constraint", "a", "--downside-cap", "one hour", "--reversible-test", "interview", "--success-metric", "learning", "--harm-metric", "none", "--stop-condition", "deadline", "--review-days", "7", "--stake", "low", "--owner", "me"]
        first = subprocess.check_output(cmd, text=True)
        self.assertEqual(first, subprocess.check_output(cmd, text=True))
        payload = json.loads(first)
        self.assertEqual(payload["experiment"]["proposition"], "test option")
        self.assertEqual(payload["risk_ledger"]["access_constraints"], ["a", "b"])

    def test_exact_claim_count(self):
        text = (ROOT / "references" / "claim-layer-map.md").read_text(encoding="utf-8")
        ids = [line.split("|")[1].strip() for line in text.splitlines() if line.startswith("| ") and "-NAV-" in line]
        self.assertEqual(len(ids), 18)
        self.assertEqual(len(set(ids)), 18)
        self.assertEqual({item[0] for item in ids}, {"A", "B", "C", "D"})


if __name__ == "__main__":
    unittest.main()
