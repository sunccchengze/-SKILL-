#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit_historical_claim.py"
SPEC = importlib.util.spec_from_file_location("sapiens_audit", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class SapiensAdversarialTests(unittest.TestCase):
    def args(self, *extra: str):
        base = [
            "--claim", "a global historical claim",
            "--scale", "regional",
            "--period", "10000-5000 BP",
            "--region", "West Eurasia",
            "--evidence", "skeletal proxy",
            "--alternative", "migration and regional heterogeneity",
            "--uncertainty", "proxy does not equal total wellbeing",
            "--audience", "seminar",
            "--use-context", "education",
        ]
        return MODULE.parser().parse_args(base + list(extra))

    def test_ready_is_not_truth_verdict(self):
        payload = MODULE.build(self.args())
        self.assertEqual(payload["decision"]["status"], "READY_FOR_AUDIT")
        self.assertIn("not a historical truth verdict", payload["disclaimer"])

    def test_missing_alternative_stops(self):
        args = self.args()
        args.alternative = []
        self.assertEqual(MODULE.build(args)["decision"]["status"], "STOP")

    def test_missing_uncertainty_stops(self):
        args = self.args()
        args.uncertainty = []
        self.assertEqual(MODULE.build(args)["decision"]["status"], "STOP")

    def test_missing_evidence_stops(self):
        args = self.args()
        args.evidence = []
        self.assertEqual(MODULE.build(args)["decision"]["status"], "STOP")

    def test_dehumanizing_use_blocks(self):
        self.assertEqual(MODULE.build(self.args("--dehumanizing-use"))["decision"]["status"], "BLOCKED")

    def test_rights_denial_blocks(self):
        self.assertEqual(MODULE.build(self.args("--rights-denial"))["decision"]["status"], "BLOCKED")

    def test_atrocity_denial_blocks(self):
        self.assertEqual(MODULE.build(self.args("--atrocity-denial"))["decision"]["status"], "BLOCKED")

    def test_high_risk_context_requires_all_gates(self):
        args = self.args()
        args.use_context = "ancestry"
        self.assertEqual(MODULE.build(args)["decision"]["status"], "STOP")
        args.owner = "curator"
        args.domain_reviewer = "archaeologist"
        args.community_consultation = "named community process"
        args.appeal_channel = "public correction form"
        args.stop_condition = "pause on contested identity claim"
        self.assertEqual(MODULE.build(args)["decision"]["status"], "READY_FOR_AUDIT")

    def test_global_scale_warns(self):
        args = self.args()
        args.scale = "global"
        warnings = MODULE.build(args)["scale_card"]["warnings"]
        self.assertTrue(any("multi-region" in item for item in warnings))

    def test_deterministic_cli_and_normalized_lists(self):
        cmd = [sys.executable, str(SCRIPT), "--claim", "  test   claim ", "--scale", "regional", "--period", "x", "--region", "y", "--evidence", "b", "--evidence", "a", "--evidence", "a", "--alternative", "z", "--uncertainty", "u", "--audience", "class", "--use-context", "education"]
        first = subprocess.check_output(cmd, text=True)
        second = subprocess.check_output(cmd, text=True)
        self.assertEqual(first, second)
        payload = json.loads(first)
        self.assertEqual(payload["claim"], "test claim")
        self.assertEqual(payload["evidence_plan"]["evidence"], ["a", "b"])

    def test_exact_claim_ledger_and_layers(self):
        text = (ROOT / "references" / "claim-layer-map.md").read_text(encoding="utf-8")
        ids = []
        for line in text.splitlines():
            if line.startswith("| ") and "-SAP-" in line:
                ids.append(line.split("|")[1].strip())
        self.assertEqual(len(ids), 18)
        self.assertEqual(len(set(ids)), 18)
        self.assertEqual({item[0] for item in ids}, {"A", "B", "C", "D"})


if __name__ == "__main__":
    unittest.main()
