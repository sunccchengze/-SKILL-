import argparse
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit_automation.py"
sys.path.insert(0, str(SCRIPT.parent))

from audit_automation import build_audit, to_markdown  # noqa: E402


BASE = [
    "--system", "AI客服分流",
    "--purpose", "让用户及时获得正确帮助",
    "--metric", "平均处理时长",
    "--affected", "紧急问题用户",
    "--decision", "是否转人工",
    "--harm", "错拒或延迟人工支持",
]


class AutomationAuditTests(unittest.TestCase):
    def run_cli(self, *extra: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *BASE, *extra],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_direct_builder_has_real_governance_contract(self):
        args = argparse.Namespace(
            system="AI客服分流",
            purpose="让用户及时获得正确帮助",
            metric=["平均处理时长"],
            affected=["紧急问题用户"],
            decision=["是否转人工"],
            harm=["错拒或延迟人工支持"],
            risk_level="moderate",
            accountable_owner=None,
            applicable_rule=None,
            appeal_path=None,
            rollback_trigger=None,
            source_layer="D",
            source_locator="references/claim-layer-map.md#H009-H012",
            format="json",
            output=None,
        )
        data = build_audit(args)
        self.assertEqual(data["workflow"]["name"], "HUMAN")
        self.assertTrue(data["safety_gate"]["not_a_go_decision"])
        self.assertIn("H009", data["provenance"][2]["claim_ids"])
        self.assertFalse(data["audit"]["agency"]["reviewer_can_override_without_penalty"])

    def test_json_subprocess_is_valid_and_deterministic(self):
        first = self.run_cli("--format", "json")
        second = self.run_cli("--format", "json")
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout, second.stdout)
        payload = json.loads(first.stdout)
        self.assertEqual(payload["schema_version"], "1.0")
        self.assertEqual(payload["input"]["system"], "AI客服分流")

    def test_markdown_escapes_untrusted_table_text(self):
        args = BASE.copy()
        args[args.index("平均处理时长")] = "速度|吞吐"
        result = subprocess.run([sys.executable, str(SCRIPT), *args], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("速度\\|吞吐", result.stdout)
        self.assertIn("非批准声明", result.stdout)

    def test_blank_input_has_controlled_error(self):
        args = BASE.copy()
        args[args.index("AI客服分流")] = "   "
        result = subprocess.run([sys.executable, str(SCRIPT), *args], text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertTrue(result.stderr.startswith("ERROR:"), result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_duplicate_harms_are_rejected(self):
        result = self.run_cli("--harm", "错拒或延迟人工支持")
        self.assertEqual(result.returncode, 2)
        self.assertIn("duplicate", result.stderr)

    def test_high_risk_requires_complete_governance_fields(self):
        result = self.run_cli("--risk-level", "high", "--format", "json")
        self.assertEqual(result.returncode, 2)
        for flag in ("--accountable-owner", "--applicable-rule", "--appeal-path", "--rollback-trigger"):
            self.assertIn(flag, result.stderr)

    def test_high_risk_never_becomes_deployment_approval(self):
        result = self.run_cli(
            "--risk-level", "high",
            "--accountable-owner", "客服治理负责人",
            "--applicable-rule", "适用消费者保护与隐私规则，待法务核验",
            "--appeal-path", "人工热线",
            "--rollback-trigger", "紧急用户错拒率超过基线",
            "--format", "json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["safety_gate"]["status"], "governance_review_required")
        self.assertEqual(payload["epistemic_contract"]["status"], "governance_worksheet_not_deployment_approval")

    def test_output_file_is_created_without_stdout(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "reports" / "audit.json"
            result = self.run_cli("--format", "json", "--output", str(output))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            self.assertEqual(json.loads(output.read_text(encoding="utf-8"))["workflow"]["name"], "HUMAN")

    def test_adversarial_text_is_data_not_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            marker = Path(tmp) / "executed"
            token = f"$(touch {marker})"
            result = self.run_cli("--affected", token, "--format", "json")
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertIn(token, payload["input"]["affected_groups"])
            self.assertFalse(marker.exists())

    def test_renderer_is_stable(self):
        data = json.loads(self.run_cli("--format", "json").stdout)
        self.assertEqual(to_markdown(data), to_markdown(data))


if __name__ == "__main__":
    unittest.main()
