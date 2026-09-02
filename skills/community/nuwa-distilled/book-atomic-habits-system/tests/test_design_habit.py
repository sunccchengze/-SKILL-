from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "design_habit.py"
SPEC = importlib.util.spec_from_file_location("design_habit", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def sample_plan(**overrides: object) -> dict[str, object]:
    values: dict[str, object] = {
        "behavior": "读摘要并写一个问题",
        "value": "理解证据",
        "identity": "会留下阅读证据的研究者",
        "cue": "午饭后坐回工位",
        "location": "书桌",
        "tiny_start": "打开论文并读两分钟",
        "standard": "读完摘要并写一个问题",
    }
    values.update(overrides)
    return MODULE.build_plan(**values)


class DesignHabitTests(unittest.TestCase):
    def test_plan_keeps_gateway_standard_and_safety_cap(self) -> None:
        plan = sample_plan()
        levels = plan["behavior_levels"]
        self.assertEqual(levels["gateway_about_two_minutes"], "打开论文并读两分钟")
        self.assertEqual(levels["standard_with_real_value"], "读完摘要并写一个问题")
        self.assertIn("健康风险", levels["safety_cap_or_stop_condition"])
        self.assertNotEqual(levels["gateway_about_two_minutes"], levels["standard_with_real_value"])

    def test_observation_is_not_a_formation_deadline(self) -> None:
        plan = sample_plan(observation_days=7)
        self.assertEqual(plan["observation"]["days"], 7)
        self.assertIn("不是形成期限", plan["observation"]["label"])
        self.assertIn("不承诺 21/66 天", plan["scientific_boundary"])
        with self.assertRaises(ValueError):
            sample_plan(observation_days=66)

    def test_measurement_is_not_streak_only(self) -> None:
        plan = sample_plan()
        fields = plan["measure_and_recover"]["fields"]
        self.assertIn("预定线索是否出现", fields)
        self.assertIn("启动难度 1–5", fields)
        self.assertIn("真实产物或副作用", fields)
        self.assertIn("不加倍、不惩罚", plan["measure_and_recover"]["recovery"])

    def test_markdown_discloses_sources_and_safety_boundary(self) -> None:
        output = MODULE.render_markdown(sample_plan())
        for expected in ("作者框架", "被致谢前作", "独立研究", "本 Skill 综合", "危险戒断", "四定律是作者的实用分类"):
            self.assertIn(expected, output)

    def test_cli_can_write_structured_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "plan.json"
            code = MODULE.main(
                [
                    "--behavior", "读摘要并写一个问题",
                    "--value", "理解证据",
                    "--identity", "会留下阅读证据的研究者",
                    "--cue", "午饭后坐回工位",
                    "--location", "书桌",
                    "--tiny-start", "打开论文并读两分钟",
                    "--standard", "读完摘要并写一个问题",
                    "--json",
                    "--output", str(output),
                ]
            )
            self.assertEqual(code, 0)
            data = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(data["target"]["behavior"], "读摘要并写一个问题")
            self.assertIn("ATOM 九步法", data["method"])

    def test_source_contains_no_prediction_or_automatic_diagnosis(self) -> None:
        source = SCRIPT.read_text(encoding="utf-8")
        self.assertNotIn("predict_success", source)
        self.assertNotIn("random.", source)
        self.assertNotIn("diagnose_user", source)


if __name__ == "__main__":
    unittest.main()
