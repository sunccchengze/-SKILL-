import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "diagnose_path.py"
spec = importlib.util.spec_from_file_location("diagnose_path", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(module)


class RouterTests(unittest.TestCase):
    def test_evaluation_gap_routes_classical(self):
        scores = dict(python=2, algebra=3, calculus=3, probability=3, evaluation=1, neural_networks=3)
        self.assertEqual(module.select(scores, "theory")[0], "zhou-classical-ml-reasoning")

    def test_theory_route_when_prereqs_ready(self):
        scores = dict(python=2, algebra=2, calculus=2, probability=2, evaluation=2, neural_networks=1)
        self.assertEqual(module.select(scores, "theory")[0], "goodfellow-deep-learning-theory")

    def test_transformer_novice_routes_d2l(self):
        scores = dict(python=2, algebra=2, calculus=2, probability=2, evaluation=2, neural_networks=1)
        self.assertEqual(module.select(scores, "transformers")[0], "d2l-lab-backbone")

    def test_cli_outputs_exactly_one_module_and_contract(self):
        run = subprocess.run([
            sys.executable, str(SCRIPT), "--goal", "deep-practice", "--python", "1", "--algebra", "1", "--calculus", "1",
            "--probability", "2", "--evaluation", "2", "--neural-networks", "0", "--compute", "cpu", "--format", "json",
        ], check=True, capture_output=True, text=True)
        import json
        data = json.loads(run.stdout)
        self.assertIsInstance(data["next_module"], str)
        self.assertLessEqual(len(data["prerequisite_patches"]), 3)
        self.assertIn("error analysis", data["artifact_contract"])
        self.assertIn("final test once", data["leakage_invariant"])


if __name__ == "__main__":
    unittest.main()
