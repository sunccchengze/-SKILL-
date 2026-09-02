#!/usr/bin/env python3
"""Repository-level deep-tier gates for three modern-application book packages."""

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
NUWA = REPO / "skills/community/nuwa-distilled"
PACKAGES = {
    "book-applied-causal-ml-readiness": {
        "workflow": "IDENTIFY-DML",
        "prefix": "CML",
        "source": "CM",
        "script": "audit_causal_ml.py",
        "category": "research-science",
        "research": (
            "01-version-scope-genre.md", "02-estimand-identification-controls.md",
            "03-overlap-dml-cross-fitting.md", "04-heterogeneity-sensitivity-transport.md",
            "05-independent-critique-policy.md", "06-operational-synthesis.md",
        ),
        "markers": (
            "online version 0.1.2", "2026-05-03", "预测", "DML",
            "post-treatment", "overlap", "interference", "transport", "不是银弹",
        ),
        "ready_args": (
            "--question", "Does outreach change retention?", "--treatment", "outreach offer",
            "--outcome", "six-month retention", "--unit", "eligible participant",
            "--time-zero", "eligibility date", "--estimand", "ate", "--design", "observational",
            "--identification-assumption", "exchangeability given baseline need",
            "--control", "baseline need", "--overlap-check", "propensity support by strata",
            "--split-plan", "five fold cross fitting", "--nuisance-evaluation", "out of fold loss",
            "--sensitivity", "negative control and robustness value", "--use-dml", "--owner", "evaluation lead",
        ),
        "status_key": ("decision", "status"),
        "ready_status": "READY_FOR_ESTIMATION_PLAN",
        "blocked_args": ("--post-treatment-control", "engagement after outreach"),
        "blocked_status": "BLOCKED_POST_TREATMENT_BIAS",
    },
    "book-atlas-ai-stack-audit": {
        "workflow": "ATLAS-STACK",
        "prefix": "ATL",
        "source": "AT",
        "script": "audit_ai_stack.py",
        "category": "security-compliance",
        "research": (
            "01-source-architecture.md", "02-earth-space-infrastructure.md",
            "03-labor-data-provenance.md", "04-classification-affect-validity.md",
            "05-state-power-rights-counterevidence.md", "06-operational-synthesis.md",
        ),
        "markers": (
            "Earth", "Labor", "Data", "Classification", "Affect", "State", "Power",
            "worker voice", "单提示", "构念效度",
        ),
        "ready_args": (
            "--system", "municipal triage", "--purpose", "route requests", "--geography", "Hong Kong",
            "--as-of", "2026-08-16", "--owner", "service director", "--lifecycle-stage", "proposal",
            "--supply-node", "cloud and disposal", "--worker-group", "contract annotators",
            "--data-source", "resident submissions", "--classification", "service taxonomy",
            "--affected-group", "residents and staff", "--state-linkage", "public procurement",
            "--material-evidence", "provider region inventory", "--labor-evidence", "contract and worker interviews",
            "--provenance-evidence", "lineage register", "--remedy", "appeal and reroute",
            "--claim-denominator", "annual workload", "--stop-condition", "untraceable component",
        ),
        "status_key": ("decision", "status"),
        "ready_status": "GOVERNANCE_REVIEW_REQUIRED",
        "blocked_args": ("--emotion-inference",),
        "blocked_status": "BLOCKED_SCIENTIFIC_VALIDITY_REVIEW",
    },
    "book-ethical-algorithm-constraints": {
        "workflow": "CONSTRAIN-ACT",
        "prefix": "ETH",
        "source": "EA",
        "script": "audit_constraint_system.py",
        "category": "security-compliance",
        "research": (
            "01-source-architecture.md", "02-privacy-dp-accounting.md",
            "03-fairness-impossibility-subgroups.md", "04-strategic-feedback-adaptivity.md",
            "05-interpretability-governance-critique.md", "06-operational-synthesis.md",
        ),
        "markers": (
            "differential privacy", "neighboring relation", "composition", "base rates",
            "subgroup", "performative", "reusable holdout", "形式保证不是道德完备性",
        ),
        "ready_args": (
            "--system", "course support allocation", "--decision", "offer tutoring",
            "--affected-group", "students", "--protected-group", "students by disability and language",
            "--owner", "services lead", "--stakes", "low", "--legal-basis", "support mandate",
            "--privacy-unit", "one student participation", "--neighboring-relation", "differ by one student",
            "--epsilon", "1.0", "--delta", "0.000001", "--query-count", "4",
            "--fairness-goal", "calibration", "--base-rate-difference", "unknown",
            "--harm", "unequal support", "--appeal-path", "services review",
            "--human-review", "advisor review", "--stop-condition", "appeal disparity threshold",
        ),
        "status_key": ("decision_gate", "status"),
        "ready_status": "GOVERNANCE_REVIEW_REQUIRED",
        "blocked_args": ("--fairness-goal", "equalized-odds", "--base-rate-difference", "yes"),
        "blocked_status": "TRADEOFF_DECISION_REQUIRED",
    },
}


def root(name: str) -> Path:
    return NUWA / name


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def nested(payload: dict[str, object], path: tuple[str, str]) -> object:
    node = payload[path[0]]
    assert isinstance(node, dict)
    return node[path[1]]


class ModernApplicationDeepTierTests(unittest.TestCase):
    maxDiff = None

    def test_exact_fifteen_file_contract_and_frontmatter(self) -> None:
        for name, meta in PACKAGES.items():
            expected = {
                "README.md", "SKILL.md", "VALIDATION.md", "references/README.md",
                "references/claim-layer-map.md", "references/source-notes.md", "references/templates.md",
                f"scripts/{meta['script']}", "tests/test_adversarial.py",
                *(f"references/research/{item}" for item in meta["research"]),
            }
            actual = {
                str(path.relative_to(root(name))) for path in root(name).rglob("*")
                if path.is_file() and "__pycache__" not in path.parts
            }
            skill = read(root(name) / "SKILL.md")
            with self.subTest(package=name):
                self.assertEqual(actual, expected)
                self.assertEqual(len(actual), 15)
                self.assertTrue(skill.startswith("---\n"))
                self.assertIn(f"name: {name}\n", skill.split("---\n", 2)[1])
                self.assertIn(str(meta["workflow"]), skill)

    def test_claim_ledger_is_exact_layered_and_traceable(self) -> None:
        for name, meta in PACKAGES.items():
            prefix, source_prefix = str(meta["prefix"]), str(meta["source"])
            claims = read(root(name) / "references/claim-layer-map.md")
            sources = read(root(name) / "references/source-notes.md")
            rows = re.findall(
                rf"^\| ([ABCD]-{prefix}-\d{{2}}) \| ([ABCD]) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|$",
                claims, re.MULTILINE,
            )
            known = set(re.findall(rf"(?m)^### ({source_prefix}\d{{2}})\b", sources))
            with self.subTest(package=name):
                self.assertEqual(len(rows), 18)
                self.assertEqual(Counter(row[1] for row in rows), {"A": 5, "B": 3, "C": 6, "D": 4})
                self.assertGreaterEqual(len(known), 18)
                for claim_id, layer, claim, cited, limitation, operation in rows:
                    self.assertTrue(claim.strip() and limitation.strip() and operation.strip(), claim_id)
                    if layer in "ABC":
                        cited_ids = set(re.findall(rf"{source_prefix}\d{{2}}", cited))
                        self.assertTrue(cited_ids, claim_id)
                        self.assertLessEqual(cited_ids, known, claim_id)
                    else:
                        self.assertIn("本 Skill", cited, claim_id)

    def test_source_notes_have_version_scope_counterevidence_and_urls(self) -> None:
        for name in PACKAGES:
            text = read(root(name) / "references/source-notes.md")
            urls = re.findall(r"(?m)^- \*\*URL\*\*：(https://\S+)$", text)
            with self.subTest(package=name):
                self.assertGreaterEqual(len(urls), 18)
                self.assertIn("限制", text)
                self.assertRegex(text, r"反方|批评|边界|不能|不等于")
                self.assertIn("2026-08-16", text)

    def test_six_research_passes_are_substantive_and_bound_to_outputs(self) -> None:
        for name, meta in PACKAGES.items():
            paths = sorted((root(name) / "references/research").glob("*.md"))
            with self.subTest(package=name):
                self.assertEqual(tuple(path.name for path in paths), meta["research"])
                for path in paths:
                    text = read(path)
                    self.assertGreaterEqual(len(text), 600, path.name)
                    self.assertGreaterEqual(len(re.findall(r"(?m)^## ", text)), 7, path.name)
                    for heading in ("## 目标", "## 纳入产物", "## 未解决", "## 反证与边界"):
                        self.assertIn(heading, text, path.name)
                    self.assertIn(str(meta["workflow"]), text)

    def test_package_specific_workflows_and_boundaries(self) -> None:
        for name, meta in PACKAGES.items():
            skill = read(root(name) / "SKILL.md")
            with self.subTest(package=name):
                for marker in meta["markers"]:
                    self.assertIn(str(marker), skill)
                for heading in ("心智模型", "诚实边界", "内在张力", "表达DNA"):
                    self.assertIn(heading, skill)
                for layer in "ABCD":
                    self.assertRegex(skill, rf"\*\*{layer}｜")
                self.assertRegex(skill, r"BLOCKED|停止")
                self.assertRegex(skill, r"反证|替代解释|非迁移")
                validation = read(root(name) / "VALIDATION.md")
                self.assertIn("非 canonical", validation)
        self.assertNotIn("book-human-compatible-alignment", "\n".join(read(root(name) / "SKILL.md") for name in PACKAGES))

    def test_templates_are_executable_not_summary_sheets(self) -> None:
        for name in PACKAGES:
            text = read(root(name) / "references/templates.md")
            with self.subTest(package=name):
                self.assertGreaterEqual(len(re.findall(r"(?m)^## \d+\. ", text)), 8)
                self.assertGreaterEqual(text.count("```"), 16)
                for marker in ("owner", "source", "stop", "decision"):
                    self.assertIn(marker, text)

    def test_scripts_and_package_adversarial_suites_are_real(self) -> None:
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
                self.assertEqual(tests.count("    def test_"), 12)
                self.assertIn("deterministic", tests)
                self.assertIn("exact_claim", tests)
                subprocess.run([sys.executable, str(root(name) / "tests/test_adversarial.py")], check=True, capture_output=True, timeout=20)

    def test_clis_are_deterministic_and_fail_closed(self) -> None:
        for name, meta in PACKAGES.items():
            command = [sys.executable, str(root(name) / "scripts" / str(meta["script"])), *meta["ready_args"]]
            first = subprocess.run(command, check=True, capture_output=True, timeout=10)
            second = subprocess.run(command, check=True, capture_output=True, timeout=10)
            ready = json.loads(first.stdout)
            blocked = json.loads(subprocess.run([*command, *meta["blocked_args"]], check=True, capture_output=True, timeout=10).stdout)
            with self.subTest(package=name):
                self.assertEqual(first.stdout, second.stdout)
                self.assertEqual(nested(ready, meta["status_key"]), meta["ready_status"])
                self.assertEqual(nested(blocked, meta["status_key"]), meta["blocked_status"])
                self.assertTrue(ready["normalized"])
                self.assertNotIn(str(REPO), first.stdout.decode("utf-8"))

    def test_validation_records_scope_limits_and_determinism(self) -> None:
        for name in PACKAGES:
            text = read(root(name) / "VALIDATION.md")
            with self.subTest(package=name):
                for heading in ("## Scope", "## Commands", "## Determinism contract", "## Validation limits"):
                    self.assertIn(heading, text)
                self.assertRegex(text, r"不表示|不代表|不确认")
                self.assertIn(f"{name}/tests/test_adversarial.py", text)

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

    def test_catalog_categories_and_hashes_agree(self) -> None:
        build_script = read(REPO / "scripts/build_catalog.py")
        catalog = json.loads(read(REPO / "catalog/skills.json"))
        records = {record["name"]: record for record in catalog["skills"]}
        for name, meta in PACKAGES.items():
            category = str(meta["category"])
            expected_path = f"skills/community/nuwa-distilled/{name}/SKILL.md"
            with self.subTest(package=name):
                self.assertIn(f'"{name}": "{category}"', build_script)
                self.assertIn(name, records)
                self.assertEqual(records[name]["category"], category)
                self.assertEqual(records[name]["path"], expected_path)
                self.assertEqual(records[name]["sha256"], hashlib.sha256((REPO / expected_path).read_bytes()).hexdigest())
                self.assertIn(expected_path, read(REPO / "categories" / category / "skills.tsv"))


if __name__ == "__main__":
    unittest.main()
