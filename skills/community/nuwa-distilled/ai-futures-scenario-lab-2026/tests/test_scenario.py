import argparse
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_scenario.py"
spec = importlib.util.spec_from_file_location("build_scenario", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(module)


def args(**overrides):
    base = dict(
        focal="How should a university govern AI agents?", horizon=2032,
        stakeholder=["students", "staff"],
        uncertainty=["reliability|fragile|robust", "governance|concentrated|participatory"],
        action=["sandbox pilot"], claim=[], as_of="2026-08-16", format="json", output=None,
    )
    base.update(overrides)
    return argparse.Namespace(**base)


class ScenarioTests(unittest.TestCase):
    def test_builds_exactly_four_distinct_scenarios(self):
        data = module.build(args())
        self.assertEqual(4, len(data["scenarios"]))
        states = {tuple(x["state"] for x in card["critical_uncertainties"]) for card in data["scenarios"]}
        self.assertEqual(4, len(states))

    def test_cards_have_decision_and_epistemic_contract(self):
        card = module.build(args())["scenarios"][0]
        required = {"original_premises", "status_2026", "causal_pathway", "stakeholders", "distributional_effects", "indicators", "falsifiers", "reversible_actions", "lock_in_risks", "ethical_lenses", "review_date", "update_owner"}
        self.assertTrue(required.issubset(card))
        self.assertGreaterEqual(len(card["ethical_lenses"]), 5)

    def test_rejects_forbidden_label_and_misdated_observation(self):
        with self.assertRaises(ValueError):
            module.parse_claim("forecast-authority|certain|fiction|2021")
        with self.assertRaises(ValueError):
            module.parse_claim("observed-2026|claim|source|2025")

    def test_cli_writes_json_with_source_dates_and_no_probabilities(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "scenario.json"
            run = subprocess.run([
                sys.executable, str(SCRIPT), "--focal", "How should a university govern AI agents?", "--horizon", "2032",
                "--stakeholder", "students", "--stakeholder", "staff",
                "--uncertainty", "reliability|fragile|robust", "--uncertainty", "governance|concentrated|participatory",
                "--action", "sandbox pilot", "--as-of", "2026-08-16", "--format", "json", "--output", str(output),
            ], capture_output=True, text=True)
            self.assertEqual(0, run.returncode, run.stderr)
            data = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(2017, data["publication_baseline"]["Life 3.0"])
            self.assertIn("not forecast authority", data["epistemic_notice"])
            self.assertNotIn("probability", data["scenarios"][0])


if __name__ == "__main__":
    unittest.main()
