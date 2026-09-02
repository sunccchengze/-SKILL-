#!/usr/bin/env python3
"""Focused structural and epistemic tests for the two Nuwa book Skills."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
NUWA = REPO / "skills" / "community" / "nuwa-distilled"
YIJING = NUWA / "book-yijing-change-decision"
ATOMIC = NUWA / "book-atomic-habits-system"
BRIDGE = NUWA / "book-change-habit-bridge.md"

NEW_DEEP_PACKAGES = {
    "book-systems-thinking-intervention": "map_system.py",
    "book-cointelligence-human-ai-collaboration": "plan_collaboration.py",
    "book-ai-mirror-agency": "audit_agency.py",
    "book-human-compatible-alignment": "review_alignment.py",
    "ml-dl-learning-router": "diagnose_path.py",
    "d2l-lab-backbone": "run_micro_lab.py",
    "zhou-classical-ml-reasoning": "run_micro_experiment.py",
    "goodfellow-deep-learning-theory": "check_derivation.py",
    "ai-futures-scenario-lab-2026": "build_scenario.py",
    "book-tools-of-titans-experiment-lab": "build_experiment_card.py",
}
NEW_DEEP_PATHS = [NUWA / name for name in NEW_DEEP_PACKAGES]


class NuwaBookDistillationTests(unittest.TestCase):
    def test_skills_are_independently_invocable(self) -> None:
        expected = {
            YIJING: "book-yijing-change-decision",
            ATOMIC: "book-atomic-habits-system",
        }
        for package, name in expected.items():
            with self.subTest(name=name):
                text = (package / "SKILL.md").read_text(encoding="utf-8")
                self.assertTrue(text.startswith("---\n"))
                frontmatter = text.split("---\n", 2)[1]
                self.assertIn(f"name: {name}", frontmatter)
                self.assertIn("description:", frontmatter)
                self.assertNotIn("book-change-habit-bridge", frontmatter)

    def test_each_deep_package_has_navigation_templates_cli_tests_and_six_passes(self) -> None:
        expected_scripts = {
            YIJING: "frame_change.py",
            ATOMIC: "design_habit.py",
        }
        for package, script in expected_scripts.items():
            with self.subTest(package=package.name):
                for relative in (
                    "README.md",
                    "SKILL.md",
                    "VALIDATION.md",
                    "references/README.md",
                    "references/source-notes.md",
                    "references/claim-layer-map.md",
                    "references/templates.md",
                    f"scripts/{script}",
                ):
                    self.assertTrue((package / relative).is_file(), relative)
                passes = sorted((package / "references" / "research").glob("*.md"))
                tests = sorted((package / "tests").glob("test_*.py"))
                self.assertEqual(len(passes), 6)
                self.assertGreaterEqual(len(tests), 1)

    def test_yijing_preserves_layers_and_non_predictive_boundary(self) -> None:
        skill = (YIJING / "SKILL.md").read_text(encoding="utf-8")
        script = (YIJING / "scripts" / "frame_change.py").read_text(encoding="utf-8")
        for expected in ("《周易》古经", "《十翼》", "历史解释", "本 Skill 现代操作化", "CHANGE 七步法"):
            self.assertIn(expected, skill)
        self.assertIn("卦象不是事实证据", skill)
        self.assertIn("不自动把随机卦变成", skill)
        self.assertIn('"facts"', script)
        self.assertIn('"assumptions"', script)
        self.assertIn('"unknowns"', script)
        self.assertNotIn("predict_outcome", script)

    def test_atomic_preserves_claim_layers_and_scientific_limits(self) -> None:
        skill = (ATOMIC / "SKILL.md").read_text(encoding="utf-8")
        claims = (ATOMIC / "references" / "claim-layer-map.md").read_text(encoding="utf-8")
        for expected in ("A. 书/作者框架", "B. 明确借鉴", "C. 独立研究", "D. 本 Skill 综合", "ATOM 九步法"):
            self.assertIn(expected, skill)
        for expected in ("习惯", "不等于高频", "21/66", "1%", "可修订身份", "临床"):
            self.assertIn(expected, skill)
        self.assertEqual(len(re.findall(r"^\| A-C\d{2} \|", claims, flags=re.MULTILINE)), 16)
        self.assertIn("四级行为", claims)

    def test_bridge_is_optional_modern_and_does_not_merge_the_skills(self) -> None:
        text = BRIDGE.read_text(encoding="utf-8")
        for expected in (
            "层级：D，现代跨书操作化",
            "独立调用优先",
            "不要因为两包相邻就自动混用",
            "不声称 Clear 受《易经》影响",
            "观察周期：7–14 天（不是习惯形成期限）",
            "不得把古典类比放入“已确认的情境事实”",
        ):
            self.assertIn(expected, text)
        for package in (YIJING, ATOMIC):
            self.assertIn(
                "../book-change-habit-bridge.md",
                (package / "SKILL.md").read_text(encoding="utf-8"),
            )

    def test_known_dead_source_urls_are_absent(self) -> None:
        source_text = "\n".join(
            path.read_text(encoding="utf-8")
            for package in (YIJING, ATOMIC)
            for path in (package / "references").rglob("*.md")
        )
        for stale in (
            "https://iep.utm.edu/yijing/",
            "https://press.princeton.edu/books/paperback/9780691155669/the-i-ching",
            "https://ctext.org/wiki.pl?if=gb&res=303363",
            "https://ctext.org/wiki.pl?if=gb&res=568547",
            "https://discovery.ucl.ac.uk/id/eprint/10007063/",
        ):
            self.assertNotIn(stale, source_text)

    def test_local_markdown_links_resolve(self) -> None:
        for path in [BRIDGE, *YIJING.rglob("*.md"), *ATOMIC.rglob("*.md")]:
            text = path.read_text(encoding="utf-8")
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                clean = target.split("#", 1)[0]
                if not clean:
                    continue
                with self.subTest(path=path.relative_to(REPO), target=target):
                    self.assertTrue((path.parent / clean).resolve().exists())

    def test_new_deep_packages_are_independent_complete_and_research_backed(self) -> None:
        for name, script in NEW_DEEP_PACKAGES.items():
            package = NUWA / name
            with self.subTest(package=name):
                skill = (package / "SKILL.md").read_text(encoding="utf-8")
                frontmatter = skill.split("---\n", 2)[1]
                self.assertIn(f"name: {name}", frontmatter)
                self.assertIn("description:", frontmatter)
                for relative in (
                    "README.md", "SKILL.md", "VALIDATION.md",
                    "references/source-notes.md", "references/claim-layer-map.md",
                    "references/templates.md", f"scripts/{script}",
                ):
                    self.assertTrue((package / relative).is_file(), relative)
                self.assertEqual(6, len(list((package / "references" / "research").glob("*.md"))))
                self.assertGreaterEqual(len(list((package / "tests").glob("test_*.py"))), 1)
                validation = (package / "VALIDATION.md").read_text(encoding="utf-8")
                self.assertRegex(validation, r"unittest")
                self.assertIn("非 canonical", validation)

    def test_curriculum_has_router_artifacts_error_analysis_and_current_supplement(self) -> None:
        router = (NUWA / "ml-dl-learning-router" / "SKILL.md").read_text(encoding="utf-8")
        for module in ("d2l-lab-backbone", "zhou-classical-ml-reasoning", "goodfellow-deep-learning-theory"):
            self.assertIn(module, router)
        self.assertIn("先修", router)
        self.assertIn("错误分析", router)
        for name in ("d2l-lab-backbone", "zhou-classical-ml-reasoning", "goodfellow-deep-learning-theory"):
            text = (NUWA / name / "SKILL.md").read_text(encoding="utf-8")
            with self.subTest(package=name):
                self.assertRegex(text, r"Transformer|transformer")
                self.assertRegex(text, r"实验|experiment")
                self.assertIn("错误", text)
        theory = (NUWA / "goodfellow-deep-learning-theory" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("post-2016", theory)
        self.assertIn("Hugging Face", theory)

    def test_scenario_lab_preserves_dates_labels_and_non_forecast_boundary(self) -> None:
        package = NUWA / "ai-futures-scenario-lab-2026"
        skill = (package / "SKILL.md").read_text(encoding="utf-8")
        script = (package / "scripts" / "build_scenario.py").read_text(encoding="utf-8")
        status = (package / "references" / "assumption-status-2026.md").read_text(encoding="utf-8")
        for expected in ("2017", "2021", "2026", "指标", "反证", "利益相关者", "可逆", "伦理"):
            self.assertIn(expected, skill + status)
        self.assertIn('LABELS = {"observed-2026", "book-premise", "extrapolation", "scenario-choice", "wildcard"}', script)
        self.assertIn("not forecast authority", script)
        self.assertIn("No scenario receives an implied probability", script)
        self.assertNotIn('"forecast-authority"}', script)

    def test_new_package_local_markdown_links_resolve(self) -> None:
        for package in NEW_DEEP_PATHS:
            for path in package.rglob("*.md"):
                text = path.read_text(encoding="utf-8")
                for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
                    if target.startswith(("http://", "https://", "mailto:", "#")):
                        continue
                    clean = target.split("#", 1)[0]
                    if not clean:
                        continue
                    with self.subTest(path=path.relative_to(REPO), target=target):
                        self.assertTrue((path.parent / clean).resolve().exists())

    def test_new_packages_are_registered_in_reviewed_categories(self) -> None:
        catalog = json.loads((REPO / "catalog" / "skills.json").read_text(encoding="utf-8"))
        actual = {
            record["name"]: record["category"]
            for record in catalog["skills"]
            if record["name"] in NEW_DEEP_PACKAGES
        }
        expected = {
            "book-systems-thinking-intervention": "business-strategy",
            "book-cointelligence-human-ai-collaboration": "agents-orchestration",
            "book-ai-mirror-agency": "business-strategy",
            "book-human-compatible-alignment": "security-compliance",
            "ml-dl-learning-router": "research-science",
            "d2l-lab-backbone": "research-science",
            "zhou-classical-ml-reasoning": "research-science",
            "goodfellow-deep-learning-theory": "research-science",
            "ai-futures-scenario-lab-2026": "business-strategy",
            "book-tools-of-titans-experiment-lab": "general",
        }
        self.assertEqual(expected, actual)

    def test_tools_of_titans_is_an_experiment_lab_not_a_celebrity_catalog(self) -> None:
        package = NUWA / "book-tools-of-titans-experiment-lab"
        skill = (package / "SKILL.md").read_text(encoding="utf-8")
        claims = (package / "references" / "claim-layer-map.md").read_text(encoding="utf-8")
        copyright_text = (package / "references" / "copyright-boundaries.md").read_text(encoding="utf-8")
        script = (package / "scripts" / "build_experiment_card.py").read_text(encoding="utf-8")
        for expected in (
            "TITAN-TRACE 十步法", "source_provenance", "claim_type", "empirical_support",
            "transferability", "safety_gate", "COM-B", "幸存者", "事后因果", "权威",
            "情境错配", "Healthy / Wealthy / Wise", "宽定义", "小的表现细节",
            "从强项学习", "模式与离群者", "选择性浏览", "publication-era drift",
            "基线", "伤害指标", "停止规则", "竞争解释",
            "continue / change / stop", "professional-review", "no-self-experiment",
        ):
            self.assertIn(expected, skill)
        for prohibited_substitute in ("逐章", "逐人物", "补剂清单", "完整索引"):
            self.assertIn(prohibited_substitute, skill + copyright_text)
        self.assertGreaterEqual(len(re.findall(r"^\| TOT-C\d{2} \|", claims, flags=re.MULTILINE)), 26)
        for domain in (
            "medical-treatment", "medication-change", "supplement-change", "extreme-fasting-diet",
            "psychedelic-or-controlled-substance", "acute-mental-health",
            "dangerous-physical-practice", "high-stakes-finance", "unlawful-conduct",
        ):
            self.assertIn(f'"{domain}"', script)
        self.assertIn('"not_proof_of_causality": True', script)
        self.assertIn('"no_population_generalization": True', script)
        self.assertNotIn("celebrity_ranking", script)

    def test_deferred_time_management_skill_was_not_added(self) -> None:
        self.assertFalse((NUWA / "book-ai-powered-time-management").exists())


if __name__ == "__main__":
    unittest.main()
