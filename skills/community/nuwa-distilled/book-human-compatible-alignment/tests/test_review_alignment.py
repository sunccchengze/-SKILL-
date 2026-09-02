import importlib.util
import subprocess
import sys
import unittest
from argparse import Namespace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "review_alignment.py"
spec = importlib.util.spec_from_file_location("review_alignment", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(module)


class AlignmentReviewTests(unittest.TestCase):
    def args(self, **overrides):
        values = dict(objective="support learning", action=["rank"], stakeholder=["students"], stakes="medium", reversible="yes")
        values.update(overrides)
        return Namespace(**values)

    def test_high_irreversible_blocks_autonomy(self):
        data = module.build(self.args(stakes="high", reversible="no"))
        self.assertIn("BLOCK AUTONOMOUS", data["consequence_gate"]["decision"])

    def test_six_evidence_types_are_distinct(self):
        data = module.build(self.args())
        row = data["preference_evidence_register"][0]
        for kind in module.PREFERENCE_EVIDENCE:
            self.assertIn(kind, row)
        self.assertEqual(row["conflicts"], "PRESERVE")

    def test_cli_refuses_behavior_authorization_and_safety_shortcut(self):
        run = subprocess.run([
            sys.executable, str(SCRIPT), "--objective", "help", "--action", "recommend", "--stakeholder", "users", "--stakes", "medium", "--reversible", "yes",
        ], check=True, capture_output=True, text=True)
        self.assertIn("not preference truth, consent, authorization", run.stdout)
        self.assertIn("not a deployment safety guarantee", run.stdout)
        self.assertIn("权利是约束", run.stdout)

    def test_corrigibility_has_three_layers(self):
        data = module.build(self.args())
        self.assertEqual([x["layer"] for x in data["corrigibility_layers"]], ["model/policy", "execution infrastructure", "organization/labor"])


if __name__ == "__main__":
    unittest.main()
