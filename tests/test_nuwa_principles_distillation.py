#!/usr/bin/env python3
"""Deep evidence, provenance, workflow, and safety gates for Principles."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PACKAGE = REPO / "skills" / "community" / "nuwa-distilled" / "book-principles-decision-system"
SCRIPT = PACKAGE / "scripts" / "apply_principles.py"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


BASE = [
    "--decision", "是否扩大试点",
    "--goal", "验证留存且限制伤害",
    "--reality", "四周有120名用户",
    "--reality", "退款率高于基线",
    "--principle", "留存改善且伤害不升才扩大",
    "--disagreement", "等待可能错过窗口",
    "--evidence", "试点周报 v3",
]


class PrinciplesDistillationTests(unittest.TestCase):
    def test_package_inventory_and_frontmatter(self) -> None:
        skill = read(PACKAGE / "SKILL.md")
        self.assertTrue(skill.startswith("---\n"))
        self.assertIn("name: book-principles-decision-system", skill.split("---\n", 2)[1])
        for relative in (
            "README.md",
            "SKILL.md",
            "VALIDATION.md",
            "references/README.md",
            "references/source-notes.md",
            "references/claim-layer-map.md",
            "references/templates.md",
            "scripts/apply_principles.py",
            "tests/test_apply_principles.py",
        ):
            self.assertTrue((PACKAGE / relative).is_file(), relative)
        passes = sorted((PACKAGE / "references" / "research").glob("*.md"))
        self.assertEqual([path.name[:2] for path in passes], ["01", "02", "03", "04", "05", "06"])

    def test_skill_uses_nvwa_triple_validation_and_book_specific_models(self) -> None:
        skill = read(PACKAGE / "SKILL.md")
        for marker in (
            "跨域复现",
            "生成力",
            "排他性",
            "原则编译循环",
            "目标—现实反馈",
            "五步个人演化",
            "Believability-weighted idea meritocracy",
            "组织/人生作为可重构机器",
            "BRIDGE 六步法",
            "透明度比例测试",
        ):
            self.assertIn(marker, skill)
        self.assertEqual(len(re.findall(r"(?m)^### M\d ", skill)), 6)
        self.assertIn("A. 2017 原书", skill)
        self.assertIn("B. 其他版本/后续材料", skill)
        self.assertIn("C. 独立研究/治理/批评", skill)
        self.assertIn("D. 本 Skill 综合", skill)

    def test_claim_map_has_36_ordered_traceable_single_layer_claims(self) -> None:
        text = read(PACKAGE / "references" / "claim-layer-map.md")
        sources = read(PACKAGE / "references" / "source-notes.md")
        rows = re.findall(
            r"(?m)^\| (P\d{3}) \| (.+?) \| ([ABCD]) \| (.+?) \| (.+?) \|$",
            text,
        )
        self.assertEqual([row[0] for row in rows], [f"P{number:03d}" for number in range(1, 37)])
        self.assertEqual({row[2] for row in rows}, {"A", "B", "C", "D"})
        known_sources = set(re.findall(r"(?m)^### (PD-\d{2})\b", sources)) | {"D1"}
        for claim_id, claim, _layer, source_field, limitation in rows:
            cited = set(re.findall(r"PD-\d{2}|D1", source_field))
            self.assertTrue(cited, claim_id)
            self.assertLessEqual(cited, known_sources, claim_id)
            self.assertGreater(len(claim), 18, claim_id)
            self.assertGreater(len(limitation), 12, claim_id)
        self.assertIn("明确否定的归因", text)
        self.assertIn("禁止坍缩", text)

    def test_source_ledger_has_23_complete_records_conflicts_and_questions(self) -> None:
        text = read(PACKAGE / "references" / "source-notes.md")
        for number in range(1, 24):
            self.assertRegex(text, rf"(?m)^### PD-{number:02d}\b")
        self.assertEqual(len(re.findall(r"(?m)^### PD-\d{2}\b", text)), 23)
        for marker, minimum in (
            ("- 支持：", 23),
            ("- 不支持：", 23),
            ("- 操作决定：", 23),
            ("版本/版次", 23),
            ("冲突/局限", 23),
        ):
            self.assertGreaterEqual(text.count(marker), minimum, marker)
        for section in (
            "## 证据分层",
            "## D1 — 本 Skill 创建",
            "## 证据冲突与决策",
            "## 未解决问题",
            "## 引用纪律",
        ):
            self.assertIn(section, text)
        self.assertRegex(text, r"PD-20\s*(?:↔|/)\s*PD-21")

    def test_each_research_round_changes_workflow_and_keeps_uncertainty(self) -> None:
        research = sorted((PACKAGE / "references" / "research").glob("*.md"))
        self.assertEqual(len(research), 6)
        aggregate = "\n".join(read(path) for path in research)
        for path in research:
            text = read(path)
            self.assertGreaterEqual(len(text.splitlines()), 60, path.name)
            self.assertIn("未解决问题", text, path.name)
            self.assertTrue(any(marker in text for marker in ("操作决定", "工作流决定", "工具决定", "维护决定")), path.name)
            self.assertRegex(text, r"## (?:失败门|失败方式)", path.name)
            self.assertTrue(any(marker in text for marker in ("不能支持", "边界", "不证明", "不可")), path.name)
        for source_id in ("PD-02", "PD-11", "PD-14", "PD-17", "PD-20", "PD-21"):
            self.assertIn(source_id, aggregate)
        self.assertIn("竞争解释", aggregate)

    def test_templates_encode_distinctive_decision_and_governance_artifacts(self) -> None:
        text = read(PACKAGE / "references" / "templates.md")
        self.assertGreaterEqual(len(text.splitlines()), 250)
        for marker in (
            "现实—解释—未知账本",
            "原书五步诊断卡",
            "Principle compiler",
            "深思异议卡",
            "任务特定可靠性矩阵",
            "决策模式与 Responsible Party",
            "比例透明与隐私区",
            "High-risk gate",
            "Real-impact evidence",
            "事前预测与结果分账",
            "调查争议并列卡",
            "Claim/source provenance",
            "Stop condition",
            "Rollback trigger",
        ):
            self.assertIn(marker, text)
        self.assertIn("不得写 deployment approved", text)

    def test_cli_provenance_is_subset_of_ledgers_and_created_by_skill(self) -> None:
        script = read(SCRIPT)
        claims = read(PACKAGE / "references" / "claim-layer-map.md")
        sources = read(PACKAGE / "references" / "source-notes.md")
        cli_claims = set(re.findall(r'"(P\d{3})"', script))
        cli_sources = set(re.findall(r'"(PD-\d{2})"', script))
        self.assertTrue(cli_claims)
        self.assertTrue(cli_sources)
        self.assertTrue(all(claim_id in claims for claim_id in cli_claims))
        self.assertTrue(all(source_id in sources for source_id in cli_sources))
        self.assertIn('"created_by_skill": True', script)
        self.assertIn("sort_keys=True", script)
        self.assertNotIn("shell=True", script)
        self.assertNotIn("os.system", script)
        self.assertNotIn("eval(", script)

    def test_sensitive_domain_gate_is_behavioral_not_keyword_only(self) -> None:
        incomplete = subprocess.run(
            [sys.executable, str(SCRIPT), *BASE, "--domain", "personnel", "--risk-level", "low", "--format", "json"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(incomplete.returncode, 2)
        for flag in (
            "--accountable-owner",
            "--applicable-rule",
            "--affected-group",
            "--impact-evidence",
            "--appeal-path",
            "--rollback-trigger",
            "--stop-condition",
        ):
            self.assertIn(flag, incomplete.stderr)

        complete = subprocess.run(
            [
                sys.executable, str(SCRIPT), *BASE,
                "--domain", "personnel", "--risk-level", "low",
                "--accountable-owner", "共同负责人",
                "--applicable-rule", "劳动与隐私规则",
                "--affected-group", "候选员工",
                "--impact-evidence", "真实流程分群报告",
                "--appeal-path", "独立人工复核",
                "--rollback-trigger", "差异伤害上升",
                "--stop-condition", "严重投诉一例",
                "--format", "json",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(complete.returncode, 0, complete.stderr)
        payload = json.loads(complete.stdout)
        self.assertEqual(payload["safety_gate"]["effective_risk"], "high")
        self.assertEqual(payload["safety_gate"]["status"], "governance_review_required")
        self.assertEqual(payload["safety_gate"]["impact_evidence_status"], "submitted_not_verified")
        self.assertEqual(payload["decision_governance"]["final_decision"], "TODO by the authorized and accountable process")

    def test_global_person_scores_and_causal_overstatement_are_rejected(self) -> None:
        combined = "\n".join(read(path) for path in PACKAGE.rglob("*.md"))
        for required in (
            "禁止全局",
            "任务特定可靠性",
            "因果未识别",
            "不是部署批准",
            "不构成法律/人事/投资/部署批准",
        ):
            self.assertIn(required, combined)
        for forbidden in (
            "BRIDGE 是 Dalio 原方法。",
            "Bridgewater 成功证明 radical transparency。",
            "可信度 = 82/100",
            "BRIDGE has been scientifically validated.",
            "deployment_status: approved",
        ):
            self.assertNotIn(forbidden, combined)

    def test_local_markdown_links_resolve(self) -> None:
        for path in PACKAGE.rglob("*.md"):
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", read(path)):
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                clean = target.split("#", 1)[0]
                if clean:
                    with self.subTest(path=path.relative_to(REPO), target=target):
                        self.assertTrue((path.parent / clean).resolve().exists())

    def test_validation_has_package_and_repository_commands_and_limits(self) -> None:
        text = read(PACKAGE / "VALIDATION.md")
        self.assertIn("从包根目录运行", text)
        self.assertIn("从仓库根目录运行", text)
        self.assertIn("14/14", text)
        self.assertIn("tests/test_nuwa_principles_distillation.py", text)
        self.assertIn("python3 scripts/validate_repository.py", text)
        self.assertIn("不证明", text)

    def test_catalog_and_reviewed_category_agree(self) -> None:
        build_script = read(REPO / "scripts" / "build_catalog.py")
        self.assertIn('"book-principles-decision-system": "business-strategy"', build_script)
        catalog = json.loads(read(REPO / "catalog" / "skills.json"))
        records = {record["name"]: record for record in catalog["skills"]}
        self.assertIn("book-principles-decision-system", records, "run scripts/build_catalog.py")
        record = records["book-principles-decision-system"]
        self.assertEqual(record["category"], "business-strategy")
        expected_path = "skills/community/nuwa-distilled/book-principles-decision-system/SKILL.md"
        tsv = read(REPO / "categories" / "business-strategy" / "skills.tsv")
        self.assertIn(
            f"book-principles-decision-system\tcommunity\tnuwa-distilled\tcurrent\tyes\t{expected_path}\t",
            tsv,
        )


if __name__ == "__main__":
    unittest.main()
