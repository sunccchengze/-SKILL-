import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "map_system.py"
spec = importlib.util.spec_from_file_location("map_system", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(module)


class MapSystemTests(unittest.TestCase):
    def test_valid_link_preserves_evidence_state(self):
        link = module.parse_link("A|+|B|measured-association|local time series")
        self.assertEqual(link["evidence_state"], "measured-association")
        self.assertEqual(link["rival_explanation"], "REQUIRED")

    def test_rejects_invented_evidence_state(self):
        with self.assertRaises(ValueError):
            module.parse_link("A|+|B|proven-cause|intuition")

    def test_cli_includes_causal_and_centrality_guards(self):
        run = subprocess.run(
            [sys.executable, str(SCRIPT), "--problem", "delay", "--outcome", "safe completion", "--horizon", "6 months", "--stakeholder", "worker"],
            check=True, capture_output=True, text=True,
        )
        self.assertIn("不是因果证明", run.stdout)
        self.assertIn("禁止按图中心性", run.stdout)
        self.assertIn("停止条件", run.stdout)

    def test_requires_stakeholder(self):
        run = subprocess.run(
            [sys.executable, str(SCRIPT), "--problem", "x", "--outcome", "y", "--horizon", "1 month"],
            capture_output=True, text=True,
        )
        self.assertNotEqual(run.returncode, 0)
        self.assertIn("stakeholder", run.stderr)


if __name__ == "__main__":
    unittest.main()
