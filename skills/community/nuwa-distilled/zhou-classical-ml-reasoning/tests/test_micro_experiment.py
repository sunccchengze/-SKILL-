import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "run_micro_experiment.py"
spec = importlib.util.spec_from_file_location("micro_classic", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(module)


class ClassicExperimentTests(unittest.TestCase):
    def test_deterministic_and_supported(self):
        first = module.run(11, 80, 0.1)
        self.assertEqual(first, module.run(11, 80, 0.1))
        self.assertEqual(first["hypothesis_status"], "supported")

    def test_leakage_guards(self):
        data = module.run(11, 80, 0.1)
        self.assertEqual(data["preprocessing_fit"]["source"], "train only")
        self.assertEqual(data["final_test"]["touches"], 1)
        self.assertIn("Do not tune", data["error_analysis"]["warning"])

    def test_contract_has_baseline_history_errors_and_next(self):
        data = module.run(11, 80, 0.1)
        for key in ("problem_card", "model_assumption_card", "baseline", "metric_history", "artifact_path", "error_analysis", "next_experiment"):
            self.assertIn(key, data)
        self.assertEqual(len(data["error_analysis"]["hardest_test_examples"]), 3)

    def test_cli(self):
        run = subprocess.run([sys.executable, str(SCRIPT), "--exercise", "split-baseline", "--seed", "11"], check=True, capture_output=True, text=True)
        self.assertEqual(json.loads(run.stdout)["exercise"], "split-baseline")


if __name__ == "__main__":
    unittest.main()
