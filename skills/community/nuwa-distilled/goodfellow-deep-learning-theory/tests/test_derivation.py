import importlib.util
import json
import math
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_derivation.py"
spec = importlib.util.spec_from_file_location("derivation", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(module)


class DerivationTests(unittest.TestCase):
    def test_gradient_matches_finite_difference(self):
        data = module.run(0.7, 1, 1e-5)
        self.assertEqual(data["status"], "consistent_at_tested_point")
        self.assertLess(data["best_check"]["relative_error"], 1e-7)

    def test_stable_extreme_loss(self):
        data = module.run(0.7, 1, 1e-5)
        self.assertTrue(all(row["finite"] and math.isfinite(row["loss"]) for row in data["extreme_cases"]))

    def test_contract_has_assumptions_errors_and_next(self):
        data = module.run(0.7, 1, 1e-5)
        for key in ("assumptions", "notation_and_shapes", "equation_steps", "configuration", "environment", "error_analysis", "artifact_path", "next_experiment"):
            self.assertIn(key, data)
        self.assertIn("does not validate", data["error_analysis"]["scope"])

    def test_cli(self):
        run = subprocess.run([sys.executable, str(SCRIPT), "--exercise", "finite-difference", "--x", "0.7", "--target", "1"], check=True, capture_output=True, text=True)
        self.assertEqual(json.loads(run.stdout)["exercise"], "finite-difference")


if __name__ == "__main__":
    unittest.main()
