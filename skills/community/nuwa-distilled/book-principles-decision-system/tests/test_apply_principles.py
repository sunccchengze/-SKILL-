import argparse
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "apply_principles.py"
sys.path.insert(0, str(SCRIPT.parent))

from apply_principles import build_record, to_markdown  # noqa: E402

BASE = [
    "--decision", "是否把新产品试点扩大到两个市场",
    "--goal", "验证留存而不制造不可逆客户伤害",
    "--reality", "四周试点有120名活跃用户",
    "--reality", "退款率为基线的1.3倍",
    "--principle", "只有留存改善且伤害不升高时才扩大",
    "--disagreement", "销售团队认为四周样本太小但窗口会关闭",
    "--evidence", "试点周报 v3",
]


class PrinciplesDecisionTests(unittest.TestCase):
    def run_cli(self, *extra: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *BASE, *extra],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_builder_preserves_workflow_and_epistemic_contract(self):
        args = argparse.Namespace(
            decision="是否扩大试点",
            goal="验证留存",
            reality=["四周120名用户", "退款率上升三成"],
            principle=["收益改善且伤害不升高才扩大"],
            disagreement=["窗口成本可能高于等待成本"],
            evidence=["试点周报 v3"],
            domain="business-strategy",
            risk_level="moderate",
            decision_mode="owner",
            affected_group=[],
            accountable_owner=None,
            applicable_rule=None,
            impact_evidence=[],
            appeal_path=None,
            rollback_trigger=None,
            stop_condition=None,
            source_layer="D",
            source_locator="references/claim-layer-map.md#P029-P036",
            format="json",
            output=None,
        )
        data = build_record(args)
        self.assertEqual(data["workflow"]["name"], "BRIDGE")
        self.assertTrue(data["workflow"]["created_by_skill"])
        self.assertEqual(data["epistemic_contract"]["status"], "decision_record_not_decision_truth_or_deployment_approval")
        self.assertEqual(data["decision_governance"]["final_decision"], "TODO by the authorized and accountable process")

    def test_json_is_valid_and_deterministic(self):
        first = self.run_cli("--format", "json")
        second = self.run_cli("--format", "json")
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout, second.stdout)
        payload = json.loads(first.stdout)
        self.assertEqual(payload["schema_version"], "1.0")
        self.assertEqual(payload["input"]["realities"][0], "四周试点有120名活跃用户")

    def test_markdown_escapes_adversarial_table_input(self):
        args = BASE.copy()
        args[args.index("退款率为基线的1.3倍")] = "退款|率 <script>alert(1)</script>"
        result = subprocess.run([sys.executable, str(SCRIPT), *args], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("退款\\|率 &lt;script&gt;alert(1)&lt;/script&gt;", result.stdout)
        self.assertNotIn("<script>", result.stdout)
        self.assertIn("Claim/source provenance", result.stdout)

    def test_blank_value_is_controlled_error(self):
        args = BASE.copy()
        args[args.index("试点周报 v3")] = "   "
        result = subprocess.run([sys.executable, str(SCRIPT), *args], text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertTrue(result.stderr.startswith("ERROR:"), result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_one_reality_is_rejected(self):
        args = BASE.copy()
        first = args.index("--reality")
        second = args.index("--reality", first + 1)
        del args[second:second + 2]
        result = subprocess.run([sys.executable, str(SCRIPT), *args], text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("at least 2", result.stderr)

    def test_duplicate_values_are_rejected_case_insensitively(self):
        result = self.run_cli("--evidence", "试点周报 V3")
        self.assertEqual(result.returncode, 2)
        self.assertIn("duplicate", result.stderr)

    def test_sensitive_domain_cannot_downgrade_high_risk(self):
        result = self.run_cli("--domain", "personnel", "--risk-level", "low", "--format", "json")
        self.assertEqual(result.returncode, 2)
        self.assertIn("--accountable-owner", result.stderr)
        self.assertIn("--impact-evidence", result.stderr)
        self.assertIn("--appeal-path", result.stderr)
        self.assertIn("--rollback-trigger", result.stderr)
        self.assertIn("--stop-condition", result.stderr)

    def test_high_risk_requires_affected_group(self):
        result = self.run_cli(
            "--risk-level", "high",
            "--accountable-owner", "风控负责人",
            "--applicable-rule", "适用劳动与隐私规则",
            "--impact-evidence", "分群试点结果",
            "--appeal-path", "独立复核邮箱",
            "--rollback-trigger", "任一群体伤害率上升",
            "--stop-condition", "严重事件一例",
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("--affected-group", result.stderr)

    def test_high_risk_output_remains_review_not_approval(self):
        result = self.run_cli(
            "--domain", "personnel",
            "--risk-level", "low",
            "--accountable-owner", "人力与业务共同负责人",
            "--applicable-rule", "适用劳动、反歧视与隐私规则",
            "--affected-group", "候选人",
            "--impact-evidence", "真实流程分群验证报告 v1",
            "--appeal-path", "非原决策人的人工复核",
            "--rollback-trigger", "任一受保护群体选择率显著恶化",
            "--stop-condition", "投诉或伤害指标超过基线",
            "--format", "json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        gate = payload["safety_gate"]
        self.assertEqual(gate["effective_risk"], "high")
        self.assertEqual(gate["risk_basis"], "sensitive_domain_default")
        self.assertEqual(gate["status"], "governance_review_required")
        self.assertIn("not legal", gate["non_approval"])
        self.assertEqual(gate["impact_evidence_status"], "submitted_not_verified")
        markdown = to_markdown(payload)
        self.assertIn("真实流程分群验证报告 v1", markdown)
        self.assertIn("submitted_not_verified", markdown)
        self.assertIn("提交不等于核验", markdown)

    def test_person_policy_forbids_global_score(self):
        result = self.run_cli("--format", "json")
        payload = json.loads(result.stdout)
        policy = payload["decision_governance"]["person_rating_policy"]
        self.assertIn("Do not create a global", policy)
        self.assertIn("task-specific", policy)
        self.assertIn("contestable", policy)

    def test_principle_cards_have_version_exception_and_falsifier(self):
        payload = json.loads(self.run_cli("--format", "json").stdout)
        card = payload["worksheets"]["identify"]["principle_cards"][0]
        self.assertEqual(card["version"], "0.1-draft")
        self.assertIn("exception", card)
        self.assertIn("falsifier", card)
        self.assertEqual(card["status"], "hypothesis_to_test")

    def test_output_file_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "nested" / "record.json"
            result = self.run_cli("--format", "json", "--output", str(output))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            self.assertEqual(json.loads(output.read_text(encoding="utf-8"))["workflow"]["name"], "BRIDGE")

    def test_renderer_is_stable(self):
        data = json.loads(self.run_cli("--format", "json").stdout)
        self.assertEqual(to_markdown(data), to_markdown(data))
        self.assertIn("禁止全局", to_markdown(data))

    def test_source_avoids_unsafe_execution(self):
        source = SCRIPT.read_text(encoding="utf-8")
        self.assertNotIn("shell=True", source)
        self.assertNotIn("os.system", source)
        self.assertNotIn("eval(", source)
        self.assertIn("sort_keys=True", source)


if __name__ == "__main__":
    unittest.main()
