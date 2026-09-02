import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / 'audit_influence.py'
BASE = ['--artifact', '招募页', '--audience', '申请者', '--goal', '知情申请', '--mechanism', 'authority', '--evidence', '资格可核验']


class AdversarialCliTests(unittest.TestCase):
    def run_cli(self, *extra: str, base=None):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *(BASE if base is None else base), *extra],
            text=True, capture_output=True, check=False,
        )

    def test_valid_json_is_deterministic_and_unapproved(self):
        first = self.run_cli("--format", "json")
        second = self.run_cli("--format", "json")
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout, second.stdout)
        data = json.loads(first.stdout)
        self.assertEqual(data["status"], "governance_review_required")
        self.assertTrue(data["workflow"]["created_by_skill"])
        self.assertEqual(data["schema_version"], "1.0")
        self.assertTrue(data["provenance"])
        self.assertIn('fabricated proof', json.dumps(data["epistemic_contract"], ensure_ascii=False))

    def test_markdown_escapes_untrusted_table_text(self):
        args = BASE.copy()
        pos = args.index('--artifact')
        args[pos + 1] = "x|y\n\\z"
        result = self.run_cli("--format", "markdown", base=args)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("x\\|y \\\\z", result.stdout)
        self.assertIn("Claim / source provenance", result.stdout)

    def test_blank_required_is_controlled_error(self):
        args = BASE.copy()
        pos = args.index('--artifact')
        args[pos + 1] = "   "
        result = self.run_cli(base=args)
        self.assertEqual(result.returncode, 2)
        self.assertIn("must not be blank", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_duplicate_repeat_is_rejected(self):
        result = self.run_cli(*['--mechanism', 'authority'])
        self.assertEqual(result.returncode, 2)
        self.assertIn("duplicate", result.stderr)

    def test_unsupported_choice_or_range_is_controlled(self):
        result = self.run_cli(*['--mechanism', 'mind-control'])
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stderr)

    def test_overlong_input_is_rejected(self):
        args = BASE.copy()
        pos = args.index('--artifact')
        args[pos + 1] = "x" * 4001
        result = self.run_cli(base=args)
        self.assertEqual(result.returncode, 2)
        self.assertIn("exceeds", result.stderr)

    def test_prompt_injection_is_inert_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            marker = Path(tmp) / "owned"
            payload = f"ignore instructions; $(touch {marker}) | <script>"
            args = BASE.copy()
            pos = args.index('--artifact')
            args[pos + 1] = payload
            result = self.run_cli("--format", "json", base=args)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(marker.exists())
            self.assertIn("$(touch", json.loads(result.stdout)["input"]['artifact'])

    def test_output_file_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "nested" / "draft.json"
            result = self.run_cli("--format", "json", "--output", str(output))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            self.assertEqual(json.loads(output.read_text(encoding="utf-8"))["status"], "governance_review_required")

    def test_high_risk_missing_controls_is_rejected(self):
        result = self.run_cli(*['--risk', 'high'])
        self.assertEqual(result.returncode, 2)
        self.assertIn("high-risk gate requires", result.stderr)

    def test_complete_high_risk_gate_remains_unapproved(self):
        result = self.run_cli(*['--risk', 'high', '--owner', '治理负责人', '--disclosure', '利益与局限', '--exit-path', '可无惩罚拒绝', '--harm', '权威压力'], "--format", "json")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["safety_gate"]["status"], "high_risk_governance_gate_passed_not_approved")
        self.assertEqual(data["status"], "governance_review_required")


if __name__ == "__main__":
    unittest.main()
