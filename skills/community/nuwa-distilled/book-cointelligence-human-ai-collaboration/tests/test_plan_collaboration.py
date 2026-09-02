import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "plan_collaboration.py"
spec = importlib.util.spec_from_file_location("plan_collaboration", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(module)


class CollaborationPlanTests(unittest.TestCase):
    def test_learning_critical_routes_human_first(self):
        item = module.parse_subtask("derive result|high|high|yes|public")
        mode, reason = module.route(item, "medium")
        self.assertEqual(mode, "human-first learning")
        self.assertIn("AI-off", reason)

    def test_sensitive_data_routes_expert_governed(self):
        item = module.parse_subtask("review records|high|high|no|confidential")
        self.assertEqual(module.route(item, "low")[0], "just-me/expert-governed")

    def test_high_stakes_not_delegated(self):
        item = module.parse_subtask("recommend action|high|high|no|public")
        self.assertEqual(module.route(item, "high")[0], "just-me/expert-governed")

    def test_cli_has_baseline_ontology_and_dual_ledger(self):
        run = subprocess.run([
            sys.executable, str(SCRIPT), "--task", "learn", "--goal", "learning", "--stakes", "medium",
            "--stakeholder", "student", "--subtask", "solve|high|high|yes|public", "--date", "2026-08-16",
        ], check=True, capture_output=True, text=True)
        self.assertIn("AI 前无辅助尝试", run.stdout)
        self.assertIn("不是真实人格", run.stdout)
        self.assertIn("撤 AI 表现", run.stdout)
        self.assertIn("含验证的总时间", run.stdout)


if __name__ == "__main__":
    unittest.main()
