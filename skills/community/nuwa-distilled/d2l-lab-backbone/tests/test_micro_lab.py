import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "run_micro_lab.py"
spec = importlib.util.spec_from_file_location("micro_lab", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(module)


class MicroLabTests(unittest.TestCase):
    def test_deterministic(self):
        self.assertEqual(module.run(7, 20, 0.05), module.run(7, 20, 0.05))

    def test_train_only_preprocessing_and_single_test_touch(self):
        data = module.run(7, 20, 0.05)
        self.assertEqual(data["preprocessing_fit"]["source"], "train only")
        self.assertEqual(data["final_test"]["touches"], 1)

    def test_contract_and_error_analysis_complete(self):
        data = module.run(7, 20, 0.05)
        for field in ("hypothesis", "configuration", "environment", "metric_history", "artifact_path", "error_analysis", "next_experiment"):
            self.assertIn(field, data)
        self.assertEqual(len(data["error_analysis"]["largest_test_residuals"]), 3)
        self.assertEqual(data["hypothesis_status"], "supported")

    def test_cli_json(self):
        run = subprocess.run([sys.executable, str(SCRIPT), "--seed", "7"], check=True, capture_output=True, text=True)
        self.assertEqual(json.loads(run.stdout)["configuration"]["seed"], 7)


if __name__ == "__main__":
    unittest.main()
