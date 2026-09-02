from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
SCRIPT = PACKAGE / "scripts" / "build_experiment_card.py"


def base_args() -> list[str]:
    return [
        sys.executable,
        str(SCRIPT),
        "--target", "reduce afternoon writing start delay",
        "--candidate", "write an unedited draft for ten minutes after lunch",
        "--source-provenance", "official-author-publication",
        "--source-locator", "https://example.org/original#section",
        "--claim-type", "question-prompt",
        "--support", "not-checked",
        "--transferability", "conditional",
        "--domain", "creative-practice",
        "--mechanism", "a stable cue may reduce start friction",
        "--barrier", "motivation",
        "--barrier-note", "time and skill are present, but starting is avoided",
        "--baseline-days", "7",
        "--baseline-measure", "minutes from lunch to first paragraph",
        "--comparison", "baseline week at the same location",
        "--prediction", "median delay falls by at least five minutes",
        "--duration-days", "14",
        "--primary-outcome", "start delay",
        "--outcome-unit", "minutes",
        "--desired-direction", "lower",
        "--meaningful-change", "5",
        "--harm-metric", "subjective stress 0-10",
        "--stop-rule", "stress is at least 8 on two consecutive days",
        "--stop-rule", "one required meeting is missed",
        "--rival-explanation", "the deadline is getting closer",
        "--rival-explanation", "recording itself acts as a reminder",
        "--max-burden-minutes", "5",
    ]


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, capture_output=True, text=True, check=False)


def replace_flag(args: list[str], flag: str, value: str) -> list[str]:
    changed = list(args)
    index = changed.index(flag)
    changed[index + 1] = value
    return changed


class ExperimentCardTests(unittest.TestCase):
    def test_valid_card_is_parseable_and_preserves_epistemic_fields(self) -> None:
        result = run(base_args())
        self.assertEqual(0, result.returncode, result.stderr)
        card = json.loads(result.stdout)
        self.assertEqual("titan-trace/1.0", card["schema_version"])
        self.assertEqual("TITAN-TRACE", card["workflow"])
        ledger = card["claim_ledger"]
        self.assertEqual("official-author-publication", ledger["source_provenance"])
        self.assertEqual("question-prompt", ledger["claim_type"])
        self.assertEqual("not-checked", ledger["empirical_support"])
        self.assertEqual("conditional", ledger["transferability"])
        self.assertEqual("green", ledger["safety_gate"])
        self.assertTrue(card["bounded_inference"]["not_proof_of_causality"])
        self.assertTrue(card["bounded_inference"]["no_population_generalization"])

    def test_output_is_deterministic(self) -> None:
        first = run(base_args())
        second = run(base_args())
        self.assertEqual(0, first.returncode, first.stderr)
        self.assertEqual(first.stdout, second.stdout)

    def test_output_file_is_written_only_for_valid_card(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "nested" / "card.json"
            result = run(base_args() + ["--output", str(path)])
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertTrue(path.is_file())
            card = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual("low-risk-personal-experiment", card["card_type"])

    def test_every_blocked_domain_fails_closed(self) -> None:
        expected = {
            "medical-treatment": "professional-review",
            "medication-change": "professional-review",
            "supplement-change": "professional-review",
            "extreme-fasting-diet": "professional-review",
            "psychedelic-or-controlled-substance": "no-self-experiment",
            "acute-mental-health": "no-self-experiment",
            "dangerous-physical-practice": "no-self-experiment",
            "high-stakes-finance": "no-self-experiment",
            "unlawful-conduct": "no-self-experiment",
        }
        for domain, gate in expected.items():
            with self.subTest(domain=domain):
                result = run(replace_flag(base_args(), "--domain", domain))
                self.assertNotEqual(0, result.returncode)
                self.assertIn(gate, result.stderr)
                self.assertEqual("", result.stdout)

    def test_safe_domain_cannot_launder_supplement_or_controlled_substance(self) -> None:
        for candidate, gate in (
            ("start a supplement dose after lunch", "professional-review"),
            ("try a psychedelic after lunch", "no-self-experiment"),
        ):
            with self.subTest(candidate=candidate):
                result = run(replace_flag(base_args(), "--candidate", candidate))
                self.assertNotEqual(0, result.returncode)
                self.assertIn(gate, result.stderr)

    def test_speed_word_fast_is_not_mistaken_for_fasting(self) -> None:
        args = replace_flag(base_args(), "--candidate", "draft fast for ten minutes after lunch")
        result = run(args)
        self.assertEqual(0, result.returncode, result.stderr)

    def test_nontrivial_support_requires_independent_evidence_locator(self) -> None:
        result = run(replace_flag(base_args(), "--support", "controlled-study"))
        self.assertNotEqual(0, result.returncode)
        self.assertIn("--evidence-locator is required", result.stderr)

        args = replace_flag(base_args(), "--support", "controlled-study")
        args += ["--evidence-locator", "https://doi.org/10.0000/example"]
        accepted = run(args)
        self.assertEqual(0, accepted.returncode, accepted.stderr)
        card = json.loads(accepted.stdout)
        self.assertEqual("https://doi.org/10.0000/example", card["claim_ledger"]["independent_evidence_locator"])

    def test_not_checked_rejects_an_evidence_locator(self) -> None:
        result = run(base_args() + ["--evidence-locator", "https://example.org/evidence"])
        self.assertNotEqual(0, result.returncode)
        self.assertIn("classify the support first", result.stderr)

    def test_baseline_duration_and_burden_are_bounded(self) -> None:
        cases = (
            ("--baseline-days", "6", "between 7 and 42"),
            ("--duration-days", "43", "between 7 and 42"),
            ("--max-burden-minutes", "11", "between 1 and 10"),
            ("--meaningful-change", "0", "greater than zero"),
        )
        for flag, value, message in cases:
            with self.subTest(flag=flag):
                result = run(replace_flag(base_args(), flag, value))
                self.assertNotEqual(0, result.returncode)
                self.assertIn(message, result.stderr)

    def test_two_distinct_stop_rules_are_required(self) -> None:
        args = base_args()
        first = args.index("--stop-rule")
        del args[first:first + 2]
        result = run(args)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("at least two", result.stderr)

        duplicate = base_args() + ["--stop-rule", "one required meeting is missed"]
        result = run(duplicate)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("must be distinct", result.stderr)

    def test_two_distinct_rival_explanations_are_required(self) -> None:
        args = base_args()
        first = args.index("--rival-explanation")
        del args[first:first + 2]
        result = run(args)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("at least two", result.stderr)

    def test_bias_flags_always_include_selection_and_authority(self) -> None:
        result = run(base_args() + ["--bias-flag", "seasonality"])
        self.assertEqual(0, result.returncode, result.stderr)
        flags = [item["flag"] for item in json.loads(result.stdout)["bias_red_team"]]
        self.assertIn("survivorship-and-selection-on-success", flags)
        self.assertIn("authority-and-halo-effect", flags)
        self.assertIn("seasonality", flags)


if __name__ == "__main__":
    unittest.main()
