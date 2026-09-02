from __future__ import annotations

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "skills" / "community" / "nuwa-distilled"
PACKAGES = {
    "book-what-if-causal-audit": {
        "prefix": "CIW", "workflow": "TARGET",
        "status": "design_and_assumption_audit_not_causal_proof",
        "script": "emulate_target_trial.py", "shape": "target_trial",
        "markers": ["七项目标试验", "exchangeability", "positivity", "time zero", "DAG"],
        "args": ["--question","Does A change Y?","--population","adults","--treatment","A","--comparator","B","--outcome","Y","--time-zero","baseline","--follow-up","30 days","--estimand","risk difference","--assumption","consistency","--assumption","exchangeability","--assumption","positivity","--evidence","registry v1"],
    },
    "book-safer-world-control-audit": {
        "prefix": "ESW", "workflow": "CONTROL",
        "status": "hazard_analysis_not_safety_certification",
        "script": "analyze_safety_control.py", "shape": "unsafe_control_actions",
        "markers": ["safety ≠ reliability", "control structure", "process model", "Unsafe Control Action", "CAST"],
        "args": ["--system","agent","--boundary","request to tool","--loss","harm","--hazard","unsafe action reaches tool","--controller","orchestrator","--control-action","approve","--feedback","tool state"],
    },
    "book-governing-commons-institution-design": {
        "prefix": "GTC", "workflow": "COMMONS",
        "status": "institutional_diagnosis_not_governance_legitimacy",
        "script": "design_commons_governance.py", "shape": "principle_diagnostics",
        "markers": ["CPR", "rules-in-use", "graduated sanctions", "conflict", "nested"],
        "args": ["--resource","cluster","--resource-unit","GPU hour","--boundary","members","--user-group","researchers","--rule","base quota","--monitor","operations","--conflict-path","mediation"],
    },
    "book-privacy-context-flow-audit": {
        "prefix": "PIC", "workflow": "FLOW",
        "status": "prima_facie_privacy_audit_not_legal_approval",
        "script": "audit_contextual_flow.py", "shape": "decision_heuristic",
        "markers": ["subject", "sender", "recipient", "attribute", "transmission principle", "prima-facie"],
        "args": ["--context","teaching","--context-purpose","learning","--subject","student","--sender","teacher","--recipient","assistant","--attribute","grade","--transmission-principle","confidential","--baseline-norm","course-only sharing","--proposed-change","send to vendor","--norm-evidence","policy v1"],
    },
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def claim_rows(path: Path, prefix: str) -> list[tuple[str, str, list[str]]]:
    rows = []
    for line in read(path).splitlines():
        if not line.startswith(f"| {prefix}"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        claim_id, layer, source_cell = cells[0], cells[2], cells[3]
        sources = re.findall(rf"(?:{prefix}-\d{{2}}|D1)", source_cell)
        rows.append((claim_id, layer, sources))
    return rows


def run_cli(package: str, extra: list[str] | None = None) -> subprocess.CompletedProcess[str]:
    cfg = PACKAGES[package]
    script = BASE / package / "scripts" / cfg["script"]
    return subprocess.run(
        [sys.executable, str(script), *cfg["args"], *(extra or []), "--format", "json"],
        text=True, capture_output=True,
    )


class CoreClassicsRepositoryTests(unittest.TestCase):
    def test_four_packages_have_complete_structure(self) -> None:
        required = ["README.md", "SKILL.md", "VALIDATION.md", "references/README.md",
                    "references/claim-layer-map.md", "references/source-notes.md",
                    "references/templates.md"]
        for package, cfg in PACKAGES.items():
            base = BASE / package
            with self.subTest(package=package):
                for rel in required:
                    self.assertTrue((base / rel).is_file(), rel)
                self.assertTrue((base / "scripts" / cfg["script"]).is_file())
                self.assertEqual(len(list((base / "references" / "research").glob("*.md"))), 6)

    def test_claim_ids_are_complete_unique_and_layered(self) -> None:
        for package, cfg in PACKAGES.items():
            rows = claim_rows(BASE / package / "references" / "claim-layer-map.md", cfg["prefix"])
            ids = [row[0] for row in rows]
            with self.subTest(package=package):
                self.assertEqual(ids, [f"{cfg['prefix']}{i:03d}" for i in range(1, 29)])
                self.assertEqual(len(ids), len(set(ids)))
                self.assertEqual(set(row[1] for row in rows), {"A", "B", "C", "D"})
                self.assertTrue(all(row[2] for row in rows))

    def test_every_claim_source_resolves_to_a_real_ledger_entry(self) -> None:
        for package, cfg in PACKAGES.items():
            base = BASE / package / "references"
            ledger = read(base / "source-notes.md")
            headings = set(re.findall(rf"^## ({cfg['prefix']}-\d{{2}}|D1)｜", ledger, re.MULTILINE))
            used = {source for _, _, sources in claim_rows(base / "claim-layer-map.md", cfg["prefix"]) for source in sources}
            with self.subTest(package=package):
                self.assertEqual(used - headings, set())
                self.assertIn("D1", headings)
                for source in headings - {"D1"}:
                    section = ledger.split(f"## {source}｜", 1)[1].split("\n## ", 1)[0]
                    self.assertIn("**supports**", section)
                    self.assertIn("**does not support**", section)
                    self.assertIn("**证据级**", section)
                    self.assertRegex(section, r"限制|冲突")
                    self.assertIn("未决", section)
                    self.assertRegex(section, r"https?://")

    def test_research_rounds_make_decisions_not_prose_only(self) -> None:
        for package in PACKAGES:
            for path in sorted((BASE / package / "references" / "research").glob("*.md")):
                text = read(path)
                with self.subTest(package=package, track=path.name):
                    self.assertIn("workflow decision", text)
                    self.assertIn("failure gate", text)
                    self.assertIn("本轮造成的具体改变", text)
                    self.assertIn("仍未验证", text)
                    self.assertNotIn("workflow decision**：无", text)

    def test_skills_keep_non_interchangeable_mechanisms(self) -> None:
        for package, cfg in PACKAGES.items():
            text = read(BASE / package / "SKILL.md")
            with self.subTest(package=package):
                self.assertIn(cfg["workflow"], text)
                for marker in cfg["markers"]:
                    self.assertIn(marker, text)
                self.assertIn("A", text)
                self.assertIn("B", text)
                self.assertIn("C", text)
                self.assertIn("D", text)

    def test_cli_outputs_are_deterministic_and_book_specific(self) -> None:
        outputs: dict[str, dict[str, object]] = {}
        for package, cfg in PACKAGES.items():
            first, second = run_cli(package), run_cli(package)
            with self.subTest(package=package):
                self.assertEqual(first.returncode, 0, first.stderr)
                self.assertEqual(first.stdout, second.stdout)
                data = json.loads(first.stdout)
                outputs[package] = data
                self.assertEqual(data["workflow"]["name"], cfg["workflow"])
                self.assertEqual(data["epistemic_contract"]["status"], cfg["status"])
                self.assertIn(cfg["shape"], data)
        self.assertEqual(len({json.dumps(value.get("workflow"), sort_keys=True) for value in outputs.values()}), 4)

    def test_safety_specific_uca_cross_product_is_not_generic(self) -> None:
        data = json.loads(run_cli("book-safer-world-control-audit").stdout)
        self.assertEqual(len(data["unsafe_control_actions"]), 4)
        self.assertEqual({x["type"] for x in data["unsafe_control_actions"]},
                         {"not-provided-when-required", "provided-when-unsafe", "wrong-timing-or-order", "wrong-duration"})
        self.assertTrue(all(x["status"] == "candidate_not_validated" for x in data["unsafe_control_actions"]))

    def test_causal_and_privacy_epistemic_distinctions_survive_rendering(self) -> None:
        causal = json.loads(run_cli("book-what-if-causal-audit").stdout)
        privacy = json.loads(run_cli("book-privacy-context-flow-audit").stdout)
        self.assertTrue(causal["epistemic_contract"]["identification_precedes_estimation"])
        self.assertEqual(causal["target_trial"]["analysis_plan"], "TODO only after identification and data diagnostics")
        self.assertTrue(privacy["epistemic_contract"]["consent_is_one_transmission_principle"])
        self.assertIn("step_6_prima_facie", privacy["decision_heuristic"])

    def test_commons_does_not_turn_principles_into_a_score(self) -> None:
        data = json.loads(run_cli("book-governing-commons-institution-design").stdout)
        self.assertEqual(len(data["principle_diagnostics"]), 8)
        self.assertNotIn("score", json.dumps(data).lower())
        self.assertIn("coercion_mistaken_for_cooperation", data["justice_checks"])

    def test_portfolio_preserves_separate_attribution_and_gates(self) -> None:
        text = read(BASE / "AI_ERA_CORE_CLASSICS_PORTFOLIO.md")
        for term in ["counterfactual assumption **≠** STAMP loss scenario",
                     "causal DAG **≠** safety control structure",
                     "diagnosis **≠** legitimacy", "governance_review_required"]:
            self.assertIn(term, text)
        self.assertIn("D 层操作化", text)

    def test_templates_are_book_specific(self) -> None:
        expected = {
            "book-what-if-causal-audit": ["七项目标试验", "Time-indexed variable role", "Longitudinal strategy"],
            "book-safer-world-control-audit": ["Four-category", "Loss scenario walk", "CAST learning"],
            "book-governing-commons-institution-design": ["Rule-in-use grammar", "Graduated sanction", "Digital transfer test"],
            "book-privacy-context-flow-audit": ["Five-parameter flow", "Nine-step decision", "Policy—runtime"],
        }
        for package, markers in expected.items():
            text = read(BASE / package / "references" / "templates.md")
            with self.subTest(package=package):
                for marker in markers:
                    self.assertIn(marker, text)

    def test_existing_and_complete_high_risk_behavior_covered_by_package_suites(self) -> None:
        for package in PACKAGES:
            tests = list((BASE / package / "tests").glob("test_*.py"))
            self.assertEqual(len(tests), 1)
            text = read(tests[0])
            for marker in ["test_high_risk_missing_gates_fails", "test_high_risk_complete_is_review_not_approval",
                           "test_markdown_escapes_adversarial_text", "test_file_write", "test_duplicate_repeat_rejected"]:
                self.assertIn(marker, text)


if __name__ == "__main__":
    unittest.main()
