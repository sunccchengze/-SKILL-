#!/usr/bin/env python3
"""Deep-tier structural, provenance, safety, and evidence gates for three classics."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
NUWA = REPO / "skills" / "community" / "nuwa-distilled"
PORTFOLIO = NUWA / "PRE2000_CLASSICS_PORTFOLIO.md"
PACKAGES = {
    "book-fifth-discipline-learning-system": {
        "script": "map_learning_system.py",
        "test": "test_map_learning_system.py",
        "workflow": "LOOPS",
        "claim_prefix": "F",
        "source_prefix": "FD",
        "source_count": 14,
        "category": "business-strategy",
        "safety_status": "analysis_only",
        "high_risk_flags": ("--owner", "--stop-condition"),
        "skill_markers": (
            "图是理论，不是真相",
            "竞争解释",
            "图外变量",
            "结构不取消能动性",
            "共同愿景",
        ),
        "template_markers": (
            "安全、责任与范围门",
            "行为随时间（BOT）",
            "箭头与回路证据账",
            "竞争解释",
            "停止条件",
            "更新日志",
        ),
    },
    "book-human-use-cybernetics": {
        "script": "audit_automation.py",
        "test": "test_audit_automation.py",
        "workflow": "HUMAN",
        "claim_prefix": "H",
        "source_prefix": "HU",
        "source_count": 13,
        "category": "security-compliance",
        "safety_status": "governance_review_required",
        "high_risk_flags": (
            "--accountable-owner",
            "--applicable-rule",
            "--appeal-path",
            "--rollback-trigger",
        ),
        "skill_markers": (
            "反馈不是价值",
            "目的先于指标",
            "功能类比不等于人机伦理等同",
            "社会熵不作为可直接计算的 KPI",
            "人工覆盖、申诉、退出、回滚",
        ),
        "template_markers": (
            "高风险治理门",
            "Meaningful human review",
            "申诉、退出、事故与退役协议",
            "劳动、技能与分配账",
            "rollback",
            "决策与版本日志",
        ),
    },
    "book-understanding-media-audit": {
        "script": "audit_medium.py",
        "test": "test_audit_medium.py",
        "workflow": "MEDIUM",
        "claim_prefix": "M",
        "source_prefix": "UM",
        "source_count": 13,
        "category": "design-media",
        "safety_status": "analysis_and_probe_design_only",
        "high_risk_flags": ("--owner", "--harm", "--stop-condition"),
        "skill_markers": (
            "内容与媒介双层",
            "尺度、速度或模式变化",
            "hot/cool 依清晰度、感官和参与方式而变化",
            "技术决定论",
            "可反驳",
        ),
        "template_markers": (
            "媒介配置与版本卡",
            "内容与嵌套媒介链",
            "Feature → Affordance → Outcome",
            "Figure/Ground、权力与差异影响",
            "Tetrad 假设卡（B 层）",
            "可反驳配置探针",
            "stop condition",
        ),
    },
}


def package_path(name: str) -> Path:
    return NUWA / name


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class NuwaClassicsDistillationTests(unittest.TestCase):
    def test_portfolio_selects_instead_of_mechanically_distilling_ten(self) -> None:
        text = read(PORTFOLIO)
        for expected in (
            "不应“一书一 Skill”机械铺开",
            "第一批独立深蒸馏",
            "保留为阅读镜片",
            "不做 Nuwa 书籍蒸馏；改走课程/技术路由",
            "复合认知架构",
            "注意力—优先级",
        ):
            self.assertIn(expected, text)
        self.assertEqual(text.count("**第一批独立深蒸馏**"), 3)

    def test_package_inventory_and_frontmatter(self) -> None:
        for name, meta in PACKAGES.items():
            package = package_path(name)
            with self.subTest(package=name):
                skill = read(package / "SKILL.md")
                self.assertTrue(skill.startswith("---\n"))
                frontmatter = skill.split("---\n", 2)[1]
                self.assertIn(f"name: {name}", frontmatter)
                self.assertIn("description:", frontmatter)
                self.assertIn(str(meta["workflow"]), skill)
                for relative in (
                    "README.md",
                    "SKILL.md",
                    "VALIDATION.md",
                    "references/README.md",
                    "references/source-notes.md",
                    "references/claim-layer-map.md",
                    "references/templates.md",
                    f"scripts/{meta['script']}",
                    f"tests/{meta['test']}",
                ):
                    self.assertTrue((package / relative).is_file(), f"{name}/{relative}")
                passes = sorted((package / "references" / "research").glob("*.md"))
                self.assertEqual([path.name[:2] for path in passes], ["01", "02", "03", "04", "05", "06"])

    def test_skill_contracts_keep_attribution_and_safety_boundaries(self) -> None:
        for name, meta in PACKAGES.items():
            package = package_path(name)
            skill = read(package / "SKILL.md")
            readme = read(package / "README.md")
            with self.subTest(package=name):
                for layer in ("A.", "B.", "C.", "D."):
                    self.assertIn(layer, skill)
                for marker in meta["skill_markers"]:
                    self.assertIn(str(marker), skill)
                self.assertIn(str(meta["safety_status"]), skill)
                self.assertIn(f"scripts/{meta['script']} --help", skill)
                self.assertIn(f"scripts/{meta['script']}", readme)
                self.assertIn("认识论合同", readme)
                self.assertIn("输入仅作为数据", readme)
                for flag in meta["high_risk_flags"]:
                    self.assertIn(str(flag), skill)
                    self.assertIn(str(flag), readme)

    def test_claim_maps_have_exactly_24_traceable_claims(self) -> None:
        row_pattern = re.compile(r"^\| ([FHM]\d{3}) \| (.+?) \| ([ABCD/]+) \| (.+?) \| (.+?) \|$", re.MULTILINE)
        for name, meta in PACKAGES.items():
            text = read(package_path(name) / "references" / "claim-layer-map.md")
            source_notes = read(package_path(name) / "references" / "source-notes.md")
            rows = row_pattern.findall(text)
            prefix = str(meta["claim_prefix"])
            source_prefix = str(meta["source_prefix"])
            known_sources = set(
                re.findall(rf"(?m)^### ({source_prefix}-\d{{2}})\b", source_notes)
            ) | {"D1"}
            expected = [f"{prefix}{number:03d}" for number in range(1, 25)]
            with self.subTest(package=name):
                self.assertEqual([row[0] for row in rows], expected)
                self.assertEqual({layer for row in rows for layer in row[2].split("/")}, {"A", "B", "C", "D"})
                for claim_id, claim, _layer, sources, limitation in rows:
                    cited_sources = set(
                        re.findall(rf"{source_prefix}-\d{{2}}|D1", sources)
                    )
                    self.assertGreater(len(claim), 12, claim_id)
                    self.assertTrue(cited_sources, claim_id)
                    self.assertLessEqual(cited_sources, known_sources, claim_id)
                    self.assertGreater(len(limitation), 10, claim_id)
                self.assertIn("明确否定的归因", text)
                self.assertTrue(any(section in text for section in ("禁止坍缩", "不能互相替代")))

    def test_source_ledgers_state_support_non_support_and_unresolved_questions(self) -> None:
        for name, meta in PACKAGES.items():
            text = read(package_path(name) / "references" / "source-notes.md")
            source_prefix = str(meta["source_prefix"])
            with self.subTest(package=name):
                for number in range(1, int(meta["source_count"]) + 1):
                    self.assertRegex(text, rf"(?m)^### {source_prefix}-{number:02d}\b", f"missing {source_prefix}-{number:02d}")
                self.assertGreaterEqual(text.count("- 支持："), 12)
                self.assertGreaterEqual(text.count("- 不支持："), 12)
                self.assertGreaterEqual(text.count("- 操作决定："), 12)
                for section in ("## 证据分层", "## D1 — 本 Skill 创建", "## 证据冲突与决策", "## 未解决问题", "## 引用纪律"):
                    self.assertIn(section, text)

    def test_research_passes_are_evidence_bound_and_operational(self) -> None:
        for name, meta in PACKAGES.items():
            research = sorted((package_path(name) / "references" / "research").glob("*.md"))
            aggregate = "\n".join(read(path) for path in research)
            with self.subTest(package=name):
                self.assertEqual(len(research), 6)
                for path in research:
                    text = read(path)
                    self.assertGreaterEqual(len(text.splitlines()), 50, path.name)
                    self.assertIn("未解决问题", text, path.name)
                    self.assertTrue(
                        any(marker in text for marker in ("边界", "不能", "不可", "不等于")),
                        f"{path.name} lacks an evidence boundary",
                    )
                self.assertIn(str(meta["source_prefix"]), aggregate)
                self.assertTrue(any(marker in aggregate for marker in ("竞争解释", "替代解释", "反例")))
                self.assertTrue(any(marker in aggregate for marker in ("操作决定", "操作化", "工作流")))

    def test_templates_are_executable_workflow_artifacts(self) -> None:
        for name, meta in PACKAGES.items():
            text = read(package_path(name) / "references" / "templates.md")
            with self.subTest(package=name):
                self.assertGreaterEqual(len(text.splitlines()), 100)
                for common in ("安全", "owner", "证据", "版本", "Claim/source provenance"):
                    self.assertIn(common, text)
                for marker in meta["template_markers"]:
                    self.assertIn(str(marker), text)

    def test_cli_provenance_is_a_subset_of_claim_and_source_ledgers(self) -> None:
        for name, meta in PACKAGES.items():
            package = package_path(name)
            script = read(package / "scripts" / str(meta["script"]))
            claims = read(package / "references" / "claim-layer-map.md")
            sources = read(package / "references" / "source-notes.md")
            cli_claim_ids = set(re.findall(rf'"({meta["claim_prefix"]}\d{{3}})"', script))
            cli_source_ids = set(re.findall(rf'"({meta["source_prefix"]}-\d{{2}})"', script))
            with self.subTest(package=name):
                self.assertTrue(cli_claim_ids)
                self.assertTrue(cli_source_ids)
                self.assertTrue(all(claim_id in claims for claim_id in cli_claim_ids))
                self.assertTrue(all(source_id in sources for source_id in cli_source_ids))
                self.assertIn('"created_by_skill": True', script)
                self.assertIn(str(meta["safety_status"]), script)
                self.assertIn("sort_keys=True", script)
                self.assertNotIn("shell=True", script)
                self.assertNotIn("os.system", script)
                self.assertNotIn("eval(", script)

    def test_validation_docs_give_package_and_repository_root_commands(self) -> None:
        for name, meta in PACKAGES.items():
            text = read(package_path(name) / "VALIDATION.md")
            with self.subTest(package=name):
                self.assertIn("从包根目录运行", text)
                self.assertIn("从仓库根目录运行", text)
                self.assertIn("10/10 通过", text)
                self.assertIn(f"{name}/tests", text)
                self.assertIn("python3 tests/test_nuwa_classics_distillations.py", text)
                self.assertIn("python3 scripts/validate_repository.py", text)
                self.assertTrue(any(marker in text for marker in ("不证明", "不构成", "不是")))

    def test_category_overrides_and_generated_catalog_agree(self) -> None:
        build_script = read(REPO / "scripts" / "build_catalog.py")
        catalog = json.loads(read(REPO / "catalog" / "skills.json"))
        by_name = {record["name"]: record for record in catalog["skills"]}
        for name, meta in PACKAGES.items():
            with self.subTest(package=name):
                category = str(meta["category"])
                self.assertIn(f'"{name}": "{category}"', build_script)
                self.assertIn(name, by_name, "run scripts/build_catalog.py")
                self.assertEqual(by_name[name]["category"], category)
                category_tsv = read(REPO / "categories" / category / "skills.tsv")
                expected_path = f"skills/community/nuwa-distilled/{name}/SKILL.md"
                self.assertIn(
                    f"{name}\tcommunity\tnuwa-distilled\tcurrent\tyes\t{expected_path}\t",
                    category_tsv,
                )

    def test_local_markdown_links_resolve(self) -> None:
        paths = [PORTFOLIO]
        for name in PACKAGES:
            paths.extend(package_path(name).rglob("*.md"))
        for path in paths:
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", read(path)):
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                clean = target.split("#", 1)[0]
                if not clean:
                    continue
                with self.subTest(path=path.relative_to(REPO), target=target):
                    self.assertTrue((path.parent / clean).resolve().exists())

    def test_distillations_do_not_claim_external_validation_or_author_prediction(self) -> None:
        text = "\n".join(
            read(path)
            for name in PACKAGES
            for path in package_path(name).rglob("*.md")
        )
        for forbidden in (
            "已被科学证明的普适定律",
            "McLuhan 精确预言了生成式 AI。",
            "Senge 独自发明系统动力学。",
            "社会熵可以直接计算",
            "HUMAN 是 Wiener 原方法",
            "LOOPS 是 Senge 原方法",
        ):
            self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
