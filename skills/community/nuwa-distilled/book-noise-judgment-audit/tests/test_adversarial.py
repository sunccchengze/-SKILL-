#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit_judgment_system.py"
SPEC = importlib.util.spec_from_file_location("noise_audit", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class NoiseAdversarialTests(unittest.TestCase):
    def args(self, *extra: str):
        base = ["--system", "grant review", "--case-spec", "same dossier", "--equivalence-rule", "same track and stage", "--judge-count", "3", "--repeat-rounds", "1", "--target-type", "policy-rule", "--outcome", "ordinal rating", "--intervention", "independent criterion scores", "--cost-risk", "false rejection", "--owner", "director", "--use-context", "management"]
        return MODULE.parser().parse_args(base + list(extra))

    def test_ready_plan_is_not_case_decision(self):
        payload = MODULE.build(self.args())
        self.assertEqual(payload["decision"]["status"], "READY_FOR_AUDIT")
        self.assertIn("does not decide any individual case", payload["disclaimer"])

    def test_single_judge_single_round_stops(self):
        args = self.args()
        args.judge_count = 1
        self.assertEqual(MODULE.build(args)["decision"]["status"], "STOP")

    def test_no_target_prohibits_accuracy_claim(self):
        args = self.args()
        args.target_type = "no-defensible-target"
        target = MODULE.build(args)["target"]
        self.assertFalse(target["accuracy_claim_permitted"])
        self.assertTrue(any("prohibited" in item for item in target["warnings"]))

    def test_policy_rule_not_ground_truth(self):
        target = MODULE.build(self.args())["target"]
        self.assertFalse(target["accuracy_claim_permitted"])
        self.assertTrue(any("not necessarily ground truth" in item for item in target["warnings"]))

    def test_remove_all_discretion_stops(self):
        self.assertEqual(MODULE.build(self.args("--remove-all-discretion"))["decision"]["status"], "STOP")

    def test_no_intervention_stops(self):
        args = self.args()
        args.intervention = []
        self.assertEqual(MODULE.build(args)["decision"]["status"], "STOP")

    def test_clinical_context_requires_rights_gates(self):
        args = self.args()
        args.use_context = "clinical"
        self.assertEqual(MODULE.build(args)["decision"]["status"], "STOP")
        args.qualified_reviewer = "licensed clinician"
        args.subgroup_audit = "error and missingness by relevant groups"
        args.appeal_route = "human second review"
        args.stop_condition = "rollback on harm threshold"
        self.assertEqual(MODULE.build(args)["decision"]["status"], "READY_FOR_AUDIT")

    def test_automation_requires_review(self):
        args = self.args("--automate")
        self.assertEqual(MODULE.build(args)["decision"]["status"], "STOP")
        args.automation_review = "data coverage drift access and audit log"
        self.assertEqual(MODULE.build(args)["decision"]["status"], "READY_FOR_AUDIT")

    def test_emergency_blocks(self):
        self.assertEqual(MODULE.build(self.args("--emergency"))["decision"]["status"], "BLOCKED_FOR_EMERGENCY")

    def test_component_identifiability_is_design_dependent(self):
        payload = MODULE.build(self.args())
        self.assertFalse(payload["identifiability"]["components"]["occasion_noise"])
        self.assertTrue(any("repeated" in item for item in payload["identifiability"]["notes"]))

    def test_deterministic_normalized_output(self):
        cmd = [sys.executable, str(SCRIPT), "--system", "  test  system ", "--case-spec", "same", "--equivalence-rule", "same rule", "--judge-count", "2", "--repeat-rounds", "1", "--target-type", "verified-outcome", "--outcome", "y", "--intervention", "b", "--intervention", "a", "--intervention", "a", "--cost-risk", "c", "--owner", "o", "--use-context", "forecasting"]
        first = subprocess.check_output(cmd, text=True)
        self.assertEqual(first, subprocess.check_output(cmd, text=True))
        payload = json.loads(first)
        self.assertEqual(payload["audit_design"]["system"], "test system")
        self.assertEqual(payload["intervention_trial"]["interventions"], ["a", "b"])

    def test_exact_claim_count(self):
        text = (ROOT / "references" / "claim-layer-map.md").read_text(encoding="utf-8")
        ids = [line.split("|")[1].strip() for line in text.splitlines() if line.startswith("| ") and "-NOI-" in line]
        self.assertEqual(len(ids), 18)
        self.assertEqual(len(set(ids)), 18)
        self.assertEqual({item[0] for item in ids}, {"A", "B", "C", "D"})


if __name__ == "__main__":
    unittest.main()
