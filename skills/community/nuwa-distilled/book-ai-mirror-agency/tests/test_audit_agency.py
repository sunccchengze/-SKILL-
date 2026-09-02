import importlib.util
import subprocess
import sys
import unittest
from argparse import Namespace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit_agency.py"
spec = importlib.util.spec_from_file_location("audit_agency", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(module)


class AgencyAuditTests(unittest.TestCase):
    def test_high_irreversible_blocks_automation(self):
        data = module.build(Namespace(decision="rank", stakes="high", irreversible="yes", affected=["applicants"], ai_role="score"))
        self.assertIn("DO NOT AUTOMATE", data["rights_gate"]["status"])

    def test_non_delegable_core_includes_purpose_and_appeal(self):
        data = module.build(Namespace(decision="rank", stakes="medium", irreversible="no", affected=["applicants"], ai_role="summarize"))
        self.assertIn("purpose", data["non_delegable_core"])
        self.assertIn("appeal adjudication", data["non_delegable_core"])
        self.assertTrue(any(x["path"] == "no-AI/low-tech" for x in data["counterfutures"]))

    def test_cli_preserves_epistemic_and_human_fallibility_boundaries(self):
        run = subprocess.run([
            sys.executable, str(SCRIPT), "--decision", "rank proposals", "--stakes", "medium", "--affected", "applicants",
            "--irreversible", "no", "--ai-role", "summarize",
        ], check=True, capture_output=True, text=True)
        self.assertIn("不是完整技术模型或因果效应", run.stdout)
        self.assertIn("人类判断也不天然智慧或公平", run.stdout)
        self.assertIn("无 AI/低技术路径", run.stdout)

    def test_requires_affected_group(self):
        run = subprocess.run([sys.executable, str(SCRIPT), "--decision", "x", "--stakes", "low", "--irreversible", "no", "--ai-role", "draft"], capture_output=True, text=True)
        self.assertNotEqual(run.returncode, 0)


if __name__ == "__main__":
    unittest.main()
