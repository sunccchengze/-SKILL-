#!/usr/bin/env python3
"""Focused deep-tier gates for the seven upgraded Nuwa book packages."""

from __future__ import annotations

import ast
import hashlib
import json
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
NUWA = REPO / "skills" / "community" / "nuwa-distilled"

PACKAGES = {
    "book-cialdini-influence": {
        "workflow": "PERSUADE", "script": "audit_influence.py", "test": "test_audit_influence.py",
        "claim": "CI", "source": "CI", "category": "business-strategy", "tests": 10,
        "markers": ("虚假评价", "unity", "退出路径", "完整披露"),
        "template_markers": ("owner", "证据", "停止", "决定"),
    },
    "book-dont-make-me-think": {
        "workflow": "SCENT", "script": "audit_usability.py", "test": "test_audit_usability.py",
        "claim": "DM", "source": "DM", "category": "design-media", "tests": 10,
        "markers": ("三次点击", "WCAG 2.2", "小样本", "欺骗性设计"),
        "template_markers": ("owner", "观察", "停止", "决定"),
    },
    "book-adler-community": {
        "workflow": "BOUNDARY", "script": "reflect_adler.py", "test": "test_reflect_adler.py",
        "claim": "AD", "source": "AD", "category": "general", "tests": 10,
        "markers": ("岸见", "Adler", "创伤", "共同任务"),
        "template_markers": ("来源 ID", "可观察事实", "停止条件", "我自主选择"),
    },
    "book-hessler-documentary": {
        "workflow": "LEDGERS", "script": "build_field_ledger.py", "test": "test_build_field_ledger.py",
        "claim": "HE", "source": "HE", "category": "writing-content", "tests": 10,
        "markers": ("RT ledger", "CD ledger", "INFERRED", "再识别"),
        "template_markers": ("来源", "同意", "停止", "owner"),
    },
    "book-berger-contagious": {
        "workflow": "STEPPED", "script": "design_diffusion_test.py", "test": "test_design_diffusion_test.py",
        "claim": "BE", "source": "BE", "category": "writing-content", "tests": 10,
        "markers": ("STEPPS", "分享", "长期留存", "错误信息"),
        "template_markers": ("数据源", "竞争解释", "停止阈值", "决定"),
    },
    "book-gladwell-tipping-point": {
        "workflow": "SIX-WAY", "script": "compare_diffusion_models.py", "test": "test_compare_diffusion_models.py",
        "claim": "TP", "source": "TP", "category": "business-strategy", "tests": 9,
        "markers": ("Law of the Few", "同质", "platform", "临界点"),
        "template_markers": ("证据", "六路解释", "停止", "决定"),
    },
    "book-tiny-habits-fogg": {
        "workflow": "MAP-IT", "script": "design_tiny_habit.py", "test": "test_design_tiny_habit.py",
        "claim": "TH", "source": "TH", "category": "general", "tests": 9,
        "markers": ("B=MAT", "B=MAP", "Stephen Guise", "66 天"),
        "template_markers": ("定性证据", "自愿", "停止", "决定"),
    },
}


def package(name: str) -> Path:
    return NUWA / name


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class SevenBookUpgradeTests(unittest.TestCase):
    def test_complete_inventory_and_frontmatter(self) -> None:
        for name, meta in PACKAGES.items():
            root = package(name)
            skill = read(root / "SKILL.md")
            with self.subTest(package=name):
                self.assertTrue(skill.startswith("---\n"))
                self.assertIn(f"name: {name}", skill.split("---\n", 2)[1])
                self.assertIn(str(meta["workflow"]), skill)
                for relative in (
                    "README.md", "VALIDATION.md", "references/README.md",
                    "references/source-notes.md", "references/claim-layer-map.md",
                    "references/templates.md", f"scripts/{meta['script']}", f"tests/{meta['test']}",
                ):
                    self.assertTrue((root / relative).is_file(), f"missing {name}/{relative}")
                self.assertEqual(len(list((root / "references/research").glob("*.md"))), 6)

    def test_package_contract_markers_and_honest_boundaries(self) -> None:
        for name, meta in PACKAGES.items():
            skill = read(package(name) / "SKILL.md")
            with self.subTest(package=name):
                for marker in meta["markers"]:
                    self.assertIn(str(marker), skill)
                for heading in ("心智模型", "诚实边界", "表达DNA"):
                    self.assertIn(heading, skill)
                self.assertIn("A", skill)
                self.assertIn("B", skill)
                self.assertIn("C", skill)
                self.assertIn("D", skill)
                self.assertIn(f"scripts/{meta['script']} --help", skill)

    def test_exactly_18_claims_are_traceable_to_known_sources(self) -> None:
        for name, meta in PACKAGES.items():
            root = package(name)
            claim_text = read(root / "references/claim-layer-map.md")
            source_text = read(root / "references/source-notes.md")
            prefix = str(meta["claim"])
            source_prefix = str(meta["source"])
            rows = re.findall(rf"^\| ({prefix}-\d{{3}}) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|$", claim_text, re.MULTILINE)
            known_sources = set(re.findall(rf"(?m)^### ({source_prefix}-S\d{{2}})\b", source_text))
            with self.subTest(package=name):
                self.assertEqual([row[0] for row in rows], [f"{prefix}-{i:03d}" for i in range(1, 19)])
                layers = {
                    layer.strip().split("-", 1)[0]
                    for row in rows
                    for layer in row[1].split("/")
                }
                self.assertEqual(layers, {"A", "B", "C", "D"})
                for claim_id, _layer, allowed, sources, prohibited, consequence in rows:
                    cited = set(re.findall(rf"{source_prefix}-S\d{{2}}", sources))
                    self.assertTrue(cited, claim_id)
                    self.assertLessEqual(cited, known_sources, claim_id)
                    self.assertGreater(len(allowed.strip()), 4, claim_id)
                    self.assertGreater(len(prohibited.strip()), 2, claim_id)
                    self.assertGreater(len(consequence.strip()), 1, claim_id)

    def test_six_research_passes_are_substantive_and_source_bound(self) -> None:
        for name, meta in PACKAGES.items():
            paths = sorted((package(name) / "references/research").glob("*.md"))
            with self.subTest(package=name):
                self.assertEqual([p.name[:2] for p in paths], ["01", "02", "03", "04", "05", "06"])
                for path in paths:
                    text = read(path)
                    self.assertGreaterEqual(len(text.splitlines()), 55, path.name)
                    self.assertIn("## 发现与证据判决", text, path.name)
                    self.assertIn("## 张力与反例", text, path.name)
                    self.assertIn("## 对工作流的操作含义", text, path.name)
                    self.assertIn("## 尚未解决与更新触发", text, path.name)
                    self.assertRegex(text, rf"{meta['source']}-S\d{{2}}")
                    self.assertIn("working_evidence_note_not_approval", text)

    def test_templates_are_executable_not_summary_only(self) -> None:
        for name, meta in PACKAGES.items():
            text = read(package(name) / "references/templates.md")
            with self.subTest(package=name):
                self.assertGreaterEqual(len(text.splitlines()), 45)
                self.assertGreaterEqual(len(re.findall(r"(?m)^## T\d", text)), 5)
                for marker in meta["template_markers"]:
                    self.assertIn(str(marker), text)

    def test_cli_provenance_and_adversarial_suite_contract(self) -> None:
        for name, meta in PACKAGES.items():
            root = package(name)
            script = read(root / "scripts" / str(meta["script"]))
            test_text = read(root / "tests" / str(meta["test"]))
            claims = read(root / "references" / "claim-layer-map.md")
            sources = read(root / "references" / "source-notes.md")
            with self.subTest(package=name):
                ast.parse(script)
                ast.parse(test_text)
                cli_claims = set(re.findall(rf"['\"]({meta['claim']}-\d{{3}})['\"]", script))
                cli_sources = set(re.findall(rf"['\"]({meta['source']}-S\d{{2}})['\"]", script))
                self.assertTrue(cli_claims)
                self.assertTrue(cli_sources)
                self.assertTrue(all(item in claims for item in cli_claims))
                self.assertTrue(all(item in sources for item in cli_sources))
                self.assertIn("sort_keys=True", script)
                self.assertIn('"governance_review_required"', script)
                self.assertNotIn("shell=True", script)
                self.assertNotIn("os.system", script)
                self.assertNotIn("eval(", script)
                self.assertGreaterEqual(test_text.count("    def test_"), int(meta["tests"]))
                for marker in ("deterministic", "injection", "overlong", "duplicate", "output_file"):
                    self.assertIn(marker, test_text)

    def test_validation_records_match_actual_package_contract(self) -> None:
        for name, meta in PACKAGES.items():
            text = read(package(name) / "VALIDATION.md")
            with self.subTest(package=name):
                self.assertIn(f"`{meta['tests']}/{meta['tests']}` 通过", text)
                self.assertIn("`6/6` 通过", text)
                self.assertIn("governance_review_required", text)
                self.assertIn(f"{name}/tests", text)
                self.assertIn("不证明", text)

    def test_reference_navigation_links_resolve(self) -> None:
        for name in PACKAGES:
            for path in package(name).rglob("*.md"):
                for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", read(path)):
                    if target.startswith(("http://", "https://", "mailto:", "#")):
                        continue
                    clean = target.split("#", 1)[0]
                    if clean:
                        with self.subTest(path=path.relative_to(REPO), target=target):
                            self.assertTrue((path.parent / clean).resolve().exists())

    def test_catalog_override_and_generated_category_agree(self) -> None:
        build_script = read(REPO / "scripts/build_catalog.py")
        catalog = json.loads(read(REPO / "catalog/skills.json"))
        by_name = {record["name"]: record for record in catalog["skills"]}
        for name, meta in PACKAGES.items():
            category = str(meta["category"])
            with self.subTest(package=name):
                self.assertIn(f'"{name}": "{category}"', build_script)
                self.assertEqual(by_name[name]["category"], category)
                tsv = read(REPO / "categories" / category / "skills.tsv")
                self.assertIn(f"skills/community/nuwa-distilled/{name}/SKILL.md", tsv)

    def test_import_provenance_registers_local_deep_tier_adaptations(self) -> None:
        report = json.loads(read(REPO / "catalog/import-report.json"))
        records = {
            record["outputPath"]: record
            for record in report["canonical"] + report["variants"]
        }
        groups = {group["canonicalSourcePath"]: group for group in report["aliases"]}
        for name in PACKAGES:
            output = f"skills/community/nuwa-distilled/{name}/SKILL.md"
            record = records[output]
            digest = hashlib.sha256((REPO / output).read_bytes()).hexdigest()
            with self.subTest(package=name):
                self.assertEqual(record["sha256"], digest)
                self.assertEqual(record["localAdaptation"]["status"], "nuwa-deep-tier-upgrade")
                self.assertRegex(record["localAdaptation"]["basedOnSourceSha256"], r"^[0-9a-f]{64}$")
                self.assertEqual(
                    groups[record["sourcePath"]]["instructionSha256"],
                    record["instructionSha256"],
                )

    def test_each_package_has_explicit_safety_and_stop_gates(self) -> None:
        headings = {
            "book-cialdini-influence": "## 硬门与安全边界",
            "book-dont-make-me-think": "## 安全与停止门",
            "book-adler-community": "## 红线与停止条件",
            "book-hessler-documentary": "## 同意、隐私与伤害门",
            "book-berger-contagious": "## 安全与停止门",
            "book-gladwell-tipping-point": "## 安全与伦理门",
            "book-tiny-habits-fogg": "## 安全与停止门",
        }
        for name, heading in headings.items():
            skill = read(package(name) / "SKILL.md")
            with self.subTest(package=name):
                self.assertIn(heading, skill)
                self.assertRegex(skill, r"停止|阻断|暂停")
                self.assertRegex(skill, r"伤害|危机|风险")


if __name__ == "__main__":
    unittest.main()
