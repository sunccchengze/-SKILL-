import argparse
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "map_learning_system.py"
sys.path.insert(0, str(SCRIPT.parent))

from map_learning_system import build_map, to_markdown  # noqa: E402


BASE = [
    "--problem", "发布越赶返工越多",
    "--horizon", "12周",
    "--variable", "发布压力",
    "--variable", "返工量",
    "--assumption", "加快发布能追回进度",
    "--stakeholder", "测试团队",
]


class LearningSystemTests(unittest.TestCase):
    def run_cli(self, *extra: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *BASE, *extra],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_direct_builder_preserves_epistemic_contract(self):
        args = argparse.Namespace(
            problem="发布越赶返工越多",
            horizon="12周",
            variable=["发布压力", "返工量"],
            delay=["缺陷两周后出现"],
            assumption=["加快发布能追回进度"],
            evidence=["每周返工记录"],
            stakeholder=["测试团队"],
            risk_level="moderate",
            owner=None,
            stop_condition=None,
            source_layer="D",
            source_locator="references/claim-layer-map.md#F009-F012",
            format="json",
            output=None,
        )
        data = build_map(args)
        self.assertEqual(data["workflow"]["name"], "LOOPS")
        self.assertEqual(data["epistemic_contract"]["status"], "hypothesis_map_not_causal_proof")
        self.assertIn("F009", data["provenance"][2]["claim_ids"])
        self.assertIn("competing_explanation", data["worksheets"]["probe"])
        self.assertEqual(data["worksheets"]["probe"]["competing_explanation"], "TODO (required)")

    def test_json_subprocess_is_valid_and_deterministic(self):
        first = self.run_cli("--format", "json")
        second = self.run_cli("--format", "json")
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout, second.stdout)
        payload = json.loads(first.stdout)
        self.assertEqual(payload["schema_version"], "1.0")
        self.assertEqual(payload["input"]["variables"], ["发布压力", "返工量"])

    def test_markdown_escapes_table_metacharacters(self):
        args = BASE.copy()
        index = args.index("返工量")
        args[index] = "返工|量"
        result = subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("返工\\|量", result.stdout)
        self.assertIn("Claim / source provenance", result.stdout)

    def test_blank_required_value_is_controlled_error(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), *BASE[:-1], "   "],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertTrue(result.stderr.startswith("ERROR:"), result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_one_variable_is_rejected(self):
        args = BASE.copy()
        del args[args.index("--variable", args.index("--variable") + 1):args.index("--variable", args.index("--variable") + 1) + 2]
        result = subprocess.run([sys.executable, str(SCRIPT), *args], text=True, capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("at least 2", result.stderr)

    def test_duplicate_variables_are_rejected(self):
        result = self.run_cli("--variable", "返工量")
        self.assertEqual(result.returncode, 2)
        self.assertIn("duplicate", result.stderr)

    def test_high_risk_requires_owner_and_stop_condition(self):
        result = self.run_cli("--risk-level", "high", "--format", "json")
        self.assertEqual(result.returncode, 2)
        self.assertIn("--owner", result.stderr)
        self.assertIn("--stop-condition", result.stderr)

    def test_high_risk_output_remains_analysis_only(self):
        result = self.run_cli(
            "--risk-level", "high",
            "--owner", "安全负责人",
            "--stop-condition", "事故指标上升",
            "--format", "json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["safety_gate"]["status"], "analysis_only")
        self.assertIn("must not erase", payload["safety_gate"]["non_delegation"])

    def test_output_file_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "nested" / "worksheet.json"
            result = self.run_cli("--format", "json", "--output", str(output))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, "")
            self.assertEqual(json.loads(output.read_text(encoding="utf-8"))["workflow"]["name"], "LOOPS")

    def test_renderer_is_stable(self):
        result = self.run_cli("--format", "json")
        data = json.loads(result.stdout)
        self.assertEqual(to_markdown(data), to_markdown(data))


if __name__ == "__main__":
    unittest.main()
