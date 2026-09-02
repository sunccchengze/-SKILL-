import argparse
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit_medium.py"
sys.path.insert(0, str(SCRIPT.parent))

from audit_medium import build_audit, to_markdown  # noqa: E402


BASE = [
    "--medium", "生成式搜索界面",
    "--use", "研究选题初筛",
    "--content", "论文摘要",
    "--actor", "研究生",
    "--affordance", "对话式追问",
    "--constraint", "引用不可见",
]


class MediumAuditTests(unittest.TestCase):
    def run_cli(self, *extra: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *BASE, *extra],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_direct_builder_preserves_claim_layers(self):
        args = argparse.Namespace(
            medium="生成式搜索界面",
            use="研究选题初筛",
            content="论文摘要",
            actor=["研究生"],
            affordance=["对话式追问"],
            constraint=["引用不可见"],
            harm=[],
            stakes="moderate",
            owner=None,
            stop_condition=None,
            source_layer="D",
            source_locator="references/claim-layer-map.md#M009-M012",
            format="json",
            output=None,
        )
        data = build_audit(args)
        self.assertEqual(data["workflow"]["name"], "MEDIUM")
        self.assertEqual(data["audit"]["tetrad_hypotheses"]["layer"], "B")
        self.assertIn("M007", data["provenance"][2]["claim_ids"])
        self.assertTrue(data["safety_gate"]["not_a_launch_decision"])

    def test_json_subprocess_is_deterministic(self):
        first = self.run_cli("--format", "json")
        second = self.run_cli("--format", "json")
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout, second.stdout)
        payload = json.loads(first.stdout)
        self.assertEqual(payload["schema_version"], "1.0")
        self.assertEqual(payload["input"]["medium"], "生成式搜索界面")

    def test_markdown_escapes_table_input(self):
        args = BASE.copy()
        args[args.index("对话式追问")] = "追问|改写"
        result = subprocess.run([sys.executable, str(SCRIPT), *args], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("追问\\|改写", result.stdout)
        self.assertIn("认识论边界", result.stdout)

    def test_blank_input_has_controlled_error(self):
        args = BASE.copy()
        args[args.index("生成式搜索界面")] = "  "
        result = subprocess.run([sys.executable, str(SCRIPT), *args], text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertTrue(result.stderr.startswith("ERROR:"), result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_duplicate_actor_is_rejected(self):
        result = self.run_cli("--actor", "研究生")
        self.assertEqual(result.returncode, 2)
        self.assertIn("duplicate", result.stderr)

    def test_high_stakes_requires_owner_harm_and_stop(self):
        result = self.run_cli("--stakes", "high", "--format", "json")
        self.assertEqual(result.returncode, 2)
        self.assertIn("--owner", result.stderr)
        self.assertIn("--stop-condition", result.stderr)
        self.assertIn("--harm", result.stderr)

    def test_high_stakes_output_remains_analysis_only(self):
        result = self.run_cli(
            "--stakes", "high",
            "--owner", "研究平台主管",
            "--harm", "错误引用进入决策",
            "--stop-condition", "引用核验失败率超过基线",
            "--format", "json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["safety_gate"]["status"], "analysis_and_probe_design_only")
        self.assertEqual(payload["epistemic_contract"]["status"], "configuration_hypotheses_not_media_effect_proof")

    def test_output_file_is_created_without_stdout(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "reports" / "medium.json"
            result = self.run_cli("--format", "json", "--output", str(output))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            self.assertEqual(json.loads(output.read_text(encoding="utf-8"))["workflow"]["name"], "MEDIUM")

    def test_adversarial_text_is_not_executed(self):
        with tempfile.TemporaryDirectory() as tmp:
            marker = Path(tmp) / "executed"
            result = self.run_cli("--actor", f"$(touch {marker})", "--format", "json")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(marker.exists())
            self.assertIn(f"$(touch {marker})", json.loads(result.stdout)["input"]["actors"])

    def test_renderer_is_stable(self):
        data = json.loads(self.run_cli("--format", "json").stdout)
        self.assertEqual(to_markdown(data), to_markdown(data))


if __name__ == "__main__":
    unittest.main()
