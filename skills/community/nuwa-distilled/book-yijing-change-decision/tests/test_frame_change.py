from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "frame_change.py"
SPEC = importlib.util.spec_from_file_location("frame_change", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class FrameChangeTests(unittest.TestCase):
    def test_record_keeps_epistemic_categories_separate(self) -> None:
        record = MODULE.build_record(
            question="是否转项目？",
            horizon="三个月",
            facts=["两周后评审"],
            assumptions=["新项目成长更快"],
            unknowns=["是否有正式名额"],
            stakeholders=["导师"],
        )
        self.assertEqual(record["facts"], ["两周后评审"])
        self.assertEqual(record["assumptions"], ["新项目成长更快"])
        self.assertEqual(record["unknowns"], ["是否有正式名额"])
        self.assertIn("非古代筮法", record["method"])
        self.assertIn("不能充当外部事实证据", record["epistemic_boundary"])

    def test_markdown_contains_action_and_update_fields(self) -> None:
        record = MODULE.build_record(question="是否转项目？", horizon="三个月")
        output = MODULE.render_markdown(record)
        for expected in ("事实分栏", "时—位—应—势", "竞争情景", "72 小时可逆动作", "哪个经典类比已失效"):
            self.assertIn(expected, output)

    def test_script_does_not_cast_or_score_hexagrams(self) -> None:
        source = SCRIPT.read_text(encoding="utf-8")
        self.assertNotIn("random.", source)
        self.assertNotIn("吉凶评分", source)
        self.assertNotIn("predict_outcome", source)


if __name__ == "__main__":
    unittest.main()
