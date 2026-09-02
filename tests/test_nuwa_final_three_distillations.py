#!/usr/bin/env python3
"""Focused deep-tier gates for Sapiens, Noise, and the Naval Almanack."""

from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
import sys
import unittest
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
NUWA = REPO / "skills" / "community" / "nuwa-distilled"

PACKAGES = {
    "book-sapiens-claim-audit": {
        "workflow": "SCALE-AUDIT",
        "claim_prefix": "SAP",
        "source_prefix": "S",
        "script": "audit_historical_claim.py",
        "category": "research-science",
        "test_count": 11,
        "research": (
            "01-source-architecture.md", "02-cognition-symbolism.md",
            "03-agriculture-health.md", "04-extinction-cooperation.md",
            "05-presentism-rights.md", "06-operational-synthesis.md",
        ),
        "markers": (
            "Harari 原书", "认知革命", "古基因组", "替代解释",
            "自然主义", "受影响社群", "不用于祖源", "不是历史数据库",
        ),
        "ready_args": (
            "--claim", "agriculture improved every outcome",
            "--scale", "regional", "--period", "early farming",
            "--region", "multiple regions", "--evidence", "stature proxy",
            "--evidence", "  disease   proxy ", "--evidence", "stature proxy",
            "--alternative", "regional heterogeneity",
            "--uncertainty", "proxy is not total wellbeing",
            "--audience", "seminar", "--use-context", "education",
        ),
        "ready_status": "READY_FOR_AUDIT",
        "blocked_flag": "--rights-denial",
        "blocked_status": "BLOCKED",
    },
    "book-noise-judgment-audit": {
        "workflow": "NOISE-AUDIT",
        "claim_prefix": "NOI",
        "source_prefix": "N",
        "script": "audit_judgment_system.py",
        "category": "business-strategy",
        "test_count": 12,
        "research": (
            "01-source-architecture.md", "02-measurement-decomposition.md",
            "03-prediction-aggregation.md", "04-structured-interventions.md",
            "05-fairness-discretion.md", "06-operational-synthesis.md",
        ),
        "markers": (
            "三位作者", "水平噪音", "模式噪音", "场合噪音",
            "可辩护目标", "申诉", "移除所有裁量", "个案裁决",
        ),
        "ready_args": (
            "--system", "grant review", "--case-spec", "same round and rubric",
            "--equivalence-rule", "same evidence set", "--judge-count", "2",
            "--repeat-rounds", "1", "--target-type", "verified-outcome",
            "--outcome", "later milestone", "--intervention", "independent scoring",
            "--intervention", " independent   scoring ", "--cost-risk", "review time",
            "--owner", "program lead", "--use-context", "management",
        ),
        "ready_status": "READY_FOR_AUDIT",
        "blocked_flag": "--emergency",
        "blocked_status": "BLOCKED_FOR_EMERGENCY",
    },
    "book-naval-almanack-option-ledger": {
        "workflow": "NAVAL-OPTION",
        "claim_prefix": "NAV",
        "source_prefix": "V",
        "script": "build_option_experiment.py",
        "category": "business-strategy",
        "test_count": 12,
        "research": (
            "01-editorial-provenance.md", "02-wealth-model-primary.md",
            "03-base-rates-concentration.md", "04-autonomy-access.md",
            "05-happiness-mindfulness.md", "06-operational-synthesis.md",
        ),
        "markers": (
            "Jorgenson 编纂", "Naval primary", "superstar concentration",
            "准入约束", "ruin", "个性化投资", "不批准行动", "临床",
        ),
        "ready_args": (
            "--proposition", "test a reusable tool", "--attribution", "jorgenson-curation",
            "--source", "official almanack chapter", "--domain", "leverage",
            "--base-rate", "most tests do not scale", "--access-constraint", "weekly time",
            "--access-constraint", " weekly   time ", "--downside-cap", "six hours",
            "--reversible-test", "build one prototype", "--success-metric", "one user return",
            "--harm-metric", "sleep loss", "--stop-condition", "time cap exceeded",
            "--review-days", "14", "--stake", "low", "--owner", "experiment owner",
        ),
        "ready_status": "READY_FOR_REVERSIBLE_TEST",
        "blocked_flag": "--personalized-investment-advice",
        "blocked_status": "BLOCKED",
    },
}


def root(name: str) -> Path:
    return NUWA / name


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def instructional_sha256(path: Path) -> str:
    text = read(path).replace("\r\n", "\n").replace("\r", "\n")
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            text = text[end + 5 :]
    return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()


class FinalThreeDeepTierTests(unittest.TestCase):
    maxDiff = None

    def test_exact_fifteen_file_inventory_and_frontmatter(self) -> None:
        for name, meta in PACKAGES.items():
            expected = {
                "README.md", "SKILL.md", "VALIDATION.md", "references/README.md",
                "references/claim-layer-map.md", "references/source-notes.md",
                "references/templates.md", f"scripts/{meta['script']}",
                "tests/test_adversarial.py",
                *(f"references/research/{item}" for item in meta["research"]),
            }
            actual = {
                str(path.relative_to(root(name)))
                for path in root(name).rglob("*")
                if path.is_file() and "__pycache__" not in path.parts
            }
            skill = read(root(name) / "SKILL.md")
            with self.subTest(package=name):
                self.assertEqual(actual, expected)
                self.assertEqual(len(actual), 15)
                self.assertTrue(skill.startswith("---\n"))
                self.assertIn(f"name: {name}\n", skill.split("---\n", 2)[1])
                self.assertIn(str(meta["workflow"]), skill)

    def test_exact_claim_ledger_has_required_layers_and_traceability(self) -> None:
        for name, meta in PACKAGES.items():
            prefix = str(meta["claim_prefix"])
            source_prefix = str(meta["source_prefix"])
            claims = read(root(name) / "references/claim-layer-map.md")
            sources = read(root(name) / "references/source-notes.md")
            rows = re.findall(
                rf"^\| ([ABCD]-{prefix}-\d{{2}}) \| ([ABCD]) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|$",
                claims,
                re.MULTILINE,
            )
            known = set(re.findall(rf"(?m)^### ({source_prefix}\d{{2}})\b", sources))
            with self.subTest(package=name):
                self.assertEqual(len(rows), 18)
                self.assertEqual(Counter(row[1] for row in rows), {"A": 5, "B": 3, "C": 6, "D": 4})
                for claim_id, layer, claim, cited_text, limitation, operation in rows:
                    self.assertTrue(claim_id.startswith(f"{layer}-{prefix}-"), claim_id)
                    self.assertGreater(len(claim.strip()), 8, claim_id)
                    self.assertGreater(len(limitation.strip()), 5, claim_id)
                    self.assertGreater(len(operation.strip()), 3, claim_id)
                    if layer in {"A", "B", "C"}:
                        cited = set(re.findall(rf"{source_prefix}\d{{2}}", cited_text))
                        self.assertTrue(cited, claim_id)
                        self.assertLessEqual(cited, known, claim_id)
                    else:
                        self.assertIn("本 Skill", cited_text, claim_id)

    def test_six_research_passes_are_numbered_substantive_and_bound_to_outputs(self) -> None:
        for name, meta in PACKAGES.items():
            paths = sorted((root(name) / "references/research").glob("*.md"))
            with self.subTest(package=name):
                self.assertEqual(tuple(path.name for path in paths), meta["research"])
                for path in paths:
                    text = read(path)
                    self.assertGreaterEqual(len(text), 600, path.name)
                    self.assertGreaterEqual(len(re.findall(r"(?m)^## ", text)), 6, path.name)
                    self.assertIn("## 目标", text, path.name)
                    self.assertIn("## 纳入产物", text, path.name)
                    self.assertIn("## 未解决", text, path.name)
                    self.assertRegex(text, rf"[ABCD]-{meta['claim_prefix']}-\d{{2}}|{meta['workflow']}")

    def test_package_specific_attribution_counterevidence_and_boundaries(self) -> None:
        for name, meta in PACKAGES.items():
            skill = read(root(name) / "SKILL.md")
            with self.subTest(package=name):
                for marker in meta["markers"]:
                    self.assertIn(str(marker), skill)
                for heading in ("心智模型", "诚实边界", "内在张力", "表达DNA"):
                    self.assertIn(heading, skill)
                for layer in "ABCD":
                    self.assertRegex(skill, rf"\*\*{layer}｜")
                self.assertRegex(skill, r"停止|STOP|BLOCKED")
                self.assertRegex(skill, r"伤害|权利|风险|危机")
                self.assertRegex(skill, r"反证|反方|替代")

    def test_templates_are_executable_and_not_summary_only(self) -> None:
        for name in PACKAGES:
            text = read(root(name) / "references/templates.md")
            with self.subTest(package=name):
                self.assertGreaterEqual(len(re.findall(r"(?m)^## \d+\. ", text)), 6)
                self.assertGreaterEqual(text.count("```"), 12)
                self.assertRegex(text, r"责任人|owner")
                self.assertRegex(text, r"来源|source")
                self.assertRegex(text, r"停止|stop")
                self.assertRegex(text, r"决定|决议|结论|decision")

    def test_scripts_and_package_specific_adversarial_suites_are_real(self) -> None:
        for name, meta in PACKAGES.items():
            script = read(root(name) / "scripts" / str(meta["script"]))
            tests = read(root(name) / "tests/test_adversarial.py")
            with self.subTest(package=name):
                ast.parse(script)
                ast.parse(tests)
                self.assertIn("sort_keys=True", script)
                self.assertIn("normalized", script)
                self.assertNotIn("shell=True", script)
                self.assertNotIn("os.system", script)
                self.assertNotIn("eval(", script)
                self.assertGreaterEqual(tests.count("    def test_"), int(meta["test_count"]))
                for marker in ("deterministic", "exact_claim"):
                    self.assertIn(marker, tests)

    def test_cli_output_is_json_deterministic_normalized_and_safely_gated(self) -> None:
        for name, meta in PACKAGES.items():
            script = root(name) / "scripts" / str(meta["script"])
            command = [sys.executable, str(script), *meta["ready_args"]]
            first = subprocess.run(command, cwd=REPO, check=True, capture_output=True, timeout=10)
            second = subprocess.run(command, cwd=REPO, check=True, capture_output=True, timeout=10)
            payload = json.loads(first.stdout)
            blocked = subprocess.run(
                [*command, str(meta["blocked_flag"])],
                cwd=REPO,
                check=True,
                capture_output=True,
                timeout=10,
            )
            blocked_payload = json.loads(blocked.stdout)
            help_run = subprocess.run(
                [sys.executable, str(script), "--help"],
                cwd=REPO,
                check=True,
                capture_output=True,
                timeout=10,
            )
            with self.subTest(package=name):
                self.assertEqual(first.stdout, second.stdout)
                self.assertEqual(payload["decision"]["status"], meta["ready_status"])
                self.assertEqual(blocked_payload["decision"]["status"], meta["blocked_status"])
                self.assertIn("usage:", help_run.stdout.decode("utf-8"))
                self.assertNotIn(str(REPO), first.stdout.decode("utf-8"))

    def test_validation_records_state_limits_and_actual_test_counts(self) -> None:
        for name, meta in PACKAGES.items():
            text = read(root(name) / "VALIDATION.md")
            with self.subTest(package=name):
                self.assertIn("## Scope", text)
                self.assertIn("## Commands", text)
                self.assertIn("## Determinism contract", text)
                self.assertRegex(text, r"不表示|不代表|不确认")
                self.assertIn(f"{name}/tests/test_adversarial.py", text)
                self.assertEqual(
                    read(root(name) / "tests/test_adversarial.py").count("    def test_"),
                    int(meta["test_count"]),
                )

    def test_all_relative_markdown_links_resolve(self) -> None:
        for name in PACKAGES:
            for path in root(name).rglob("*.md"):
                for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", read(path)):
                    if target.startswith(("http://", "https://", "mailto:", "#")):
                        continue
                    clean = target.split("#", 1)[0]
                    if clean:
                        with self.subTest(path=path.relative_to(REPO), target=target):
                            self.assertTrue((path.parent / clean).resolve().exists())

    def test_local_creation_provenance_hashes_sources_and_uniqueness(self) -> None:
        report = json.loads(read(REPO / "catalog/import-report.json"))
        records = {record["name"]: record for record in report["localNuwaCreations"]}
        self.assertEqual(set(records), set(PACKAGES))
        self.assertEqual(len(records), len(report["localNuwaCreations"]))
        for name, record in records.items():
            skill = root(name) / "SKILL.md"
            with self.subTest(package=name):
                self.assertEqual(record["status"], "nuwa-deep-tier-original")
                self.assertEqual(record["outputPath"], str(skill.relative_to(REPO)))
                self.assertEqual(record["sha256"], hashlib.sha256(skill.read_bytes()).hexdigest())
                self.assertEqual(record["instructionSha256"], instructional_sha256(skill))
                self.assertTrue((REPO / record["validationPath"]).is_file())
                self.assertGreaterEqual(len(record["sourceURLs"]), 5)
                self.assertTrue(all(url.startswith("https://") for url in record["sourceURLs"]))

    def test_01a0095c_receives_explicit_non_repetition_standard(self) -> None:
        note = read(NUWA / "NOTE-TO-01A0095C-ON-NUWA-DEEP-TIER.md")
        for marker in (
            "01A0095C", "请不要重复", "不是摘要加长", "A｜原作层",
            "C｜证据层", "D｜Skill 推论层", "六轮实质研究", "专属红队测试",
            "确定性 CLI", "仓库集成纪律", "不要再做的事",
        ):
            self.assertIn(marker, note)

    def test_catalog_override_generated_catalog_and_category_indexes_agree(self) -> None:
        build_script = read(REPO / "scripts/build_catalog.py")
        catalog = json.loads(read(REPO / "catalog/skills.json"))
        by_name = {record["name"]: record for record in catalog["skills"]}
        for name, meta in PACKAGES.items():
            category = str(meta["category"])
            expected_path = f"skills/community/nuwa-distilled/{name}/SKILL.md"
            with self.subTest(package=name):
                self.assertIn(f'"{name}": "{category}"', build_script)
                self.assertEqual(by_name[name]["category"], category)
                self.assertEqual(by_name[name]["path"], expected_path)
                self.assertEqual(by_name[name]["sha256"], hashlib.sha256((REPO / expected_path).read_bytes()).hexdigest())
                self.assertIn(expected_path, read(REPO / "categories" / category / "skills.tsv"))


if __name__ == "__main__":
    unittest.main()
