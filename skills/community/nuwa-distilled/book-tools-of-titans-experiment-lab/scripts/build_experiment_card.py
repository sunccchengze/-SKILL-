#!/usr/bin/env python3
"""Build a deterministic, low-risk TITAN-TRACE personal experiment card.

The CLI fails closed for clinical, substance, dangerous physical, high-stakes
financial, and unlawful domains. It does not unlock them with an approval flag.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import NoReturn

SCHEMA_VERSION = "titan-trace/1.0"

SOURCE_PROVENANCE = (
    "user-owned-book-passage",
    "official-author-publication",
    "original-interview-or-show-notes",
    "independent-primary-research",
    "independent-guideline-or-review",
    "user-observation",
)

CLAIM_TYPES = (
    "reported-practice",
    "interviewee-belief",
    "author-synthesis",
    "question-prompt",
    "resource-recommendation",
    "anecdote",
    "independent-evidence",
)

SUPPORT_LEVELS = (
    "not-checked",
    "mechanistic-only",
    "observational",
    "controlled-study",
    "evidence-synthesis",
    "guideline",
)

TRANSFERABILITY_LEVELS = (
    "low",
    "uncertain",
    "conditional",
    "plausible-context-match",
)

SAFE_DOMAINS = (
    "general-behavior",
    "sleep-hygiene",
    "light-activity",
    "work-process",
    "learning",
    "creative-practice",
    "low-stakes-business",
)

BLOCKED_DOMAINS = {
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

ALL_DOMAINS = SAFE_DOMAINS + tuple(BLOCKED_DOMAINS)

# A second fail-closed layer catches obvious domain laundering. Patterns are
# intentionally narrow; the user can rephrase genuinely safe work-process text.
RISK_PATTERNS = {
    "professional-review": (
        r"\b(?:dose|dosage|milligrams?|prescription|medication|supplements?|fasting)\b",
        r"剂量|处方|停药|换药|药物|补剂|极端禁食|断食超过",
    ),
    "no-self-experiment": (
        r"\b(?:psychedelic|psilocybin|controlled substance|self-harm|suicid|psychosis|mania|"
        r"underwater breath[- ]?hold|financial leverage|borrow to invest|insider trading)\b",
        r"致幻|受控物质|自伤|自杀|精神病性|躁狂|水下闭气|借贷投资|金融杠杆|内幕交易|违法",
    ),
}

DEFAULT_BIAS_FLAGS = (
    "survivorship-and-selection-on-success",
    "post-hoc-causal-story",
    "authority-and-halo-effect",
    "context-and-resource-mismatch",
    "recall-editorial-and-social-desirability-bias",
    "optimization-theater-and-multiple-comparisons",
)


def fail(message: str, *, gate: str = "invalid-input") -> NoReturn:
    print(f"ERROR [{gate}]: {message}", file=sys.stderr)
    raise SystemExit(2)


def nonblank(value: str, field: str) -> str:
    cleaned = " ".join(value.split())
    if not cleaned:
        fail(f"{field} must not be blank")
    return cleaned


def risk_from_text(*values: str) -> str | None:
    text = " ".join(values).casefold()
    for gate in ("no-self-experiment", "professional-review"):
        if any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in RISK_PATTERNS[gate]):
            return gate
    return None


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description=(
            "Create a deterministic low-risk TITAN-TRACE JSON card. "
            "Unsafe and professional-review domains are rejected, not unlocked."
        )
    )
    result.add_argument("--target", required=True)
    result.add_argument("--candidate", required=True)
    result.add_argument("--source-provenance", required=True, choices=SOURCE_PROVENANCE)
    result.add_argument("--source-locator", required=True)
    result.add_argument("--claim-type", required=True, choices=CLAIM_TYPES)
    result.add_argument("--support", required=True, choices=SUPPORT_LEVELS)
    result.add_argument("--evidence-locator")
    result.add_argument("--transferability", required=True, choices=TRANSFERABILITY_LEVELS)
    result.add_argument("--domain", required=True, choices=ALL_DOMAINS)
    result.add_argument("--mechanism", required=True)
    result.add_argument("--barrier", required=True, choices=("capability", "opportunity", "motivation", "unclear"))
    result.add_argument("--barrier-note", required=True)
    result.add_argument("--baseline-days", required=True, type=int)
    result.add_argument("--baseline-measure", required=True)
    result.add_argument("--comparison", required=True)
    result.add_argument("--prediction", required=True)
    result.add_argument("--duration-days", required=True, type=int)
    result.add_argument("--primary-outcome", required=True)
    result.add_argument("--outcome-unit", required=True)
    result.add_argument("--desired-direction", required=True, choices=("higher", "lower"))
    result.add_argument("--meaningful-change", required=True, type=float)
    result.add_argument("--harm-metric", action="append", default=[])
    result.add_argument("--stop-rule", action="append", default=[])
    result.add_argument("--rival-explanation", action="append", default=[])
    result.add_argument("--bias-flag", action="append", default=[])
    result.add_argument("--max-burden-minutes", required=True, type=int)
    result.add_argument("--measurement-schedule", default="daily-at-a-fixed-time")
    result.add_argument("--output", help="JSON output path; omit to print to stdout")
    return result


def validate(args: argparse.Namespace) -> None:
    text_fields = {
        "target": args.target,
        "candidate": args.candidate,
        "source-locator": args.source_locator,
        "mechanism": args.mechanism,
        "barrier-note": args.barrier_note,
        "baseline-measure": args.baseline_measure,
        "comparison": args.comparison,
        "prediction": args.prediction,
        "primary-outcome": args.primary_outcome,
        "outcome-unit": args.outcome_unit,
        "measurement-schedule": args.measurement_schedule,
    }
    for field, value in text_fields.items():
        setattr(args, field.replace("-", "_"), nonblank(value, field))

    if args.domain in BLOCKED_DOMAINS:
        gate = BLOCKED_DOMAINS[args.domain]
        fail(
            f"domain '{args.domain}' requires {gate}; this tool only builds green low-risk cards",
            gate=gate,
        )

    inferred_gate = risk_from_text(args.target, args.candidate, args.mechanism)
    if inferred_gate:
        fail(
            "the target/candidate/mechanism contains a high-risk signal that conflicts with the selected safe domain",
            gate=inferred_gate,
        )

    if args.support != "not-checked" and not (args.evidence_locator or "").strip():
        fail("--evidence-locator is required when --support is not 'not-checked'")
    if args.support == "not-checked" and args.evidence_locator:
        fail("do not provide --evidence-locator while support is 'not-checked'; classify the support first")

    if not 7 <= args.baseline_days <= 42:
        fail("--baseline-days must be between 7 and 42")
    if not 7 <= args.duration_days <= 42:
        fail("--duration-days must be between 7 and 42")
    if not 1 <= args.max_burden_minutes <= 10:
        fail("--max-burden-minutes must be between 1 and 10")
    if args.meaningful_change <= 0:
        fail("--meaningful-change must be greater than zero")
    if len(args.harm_metric) < 1:
        fail("provide at least one --harm-metric")
    if len(args.stop_rule) < 2:
        fail("provide at least two prespecified --stop-rule values")
    if len(args.rival_explanation) < 2:
        fail("provide at least two --rival-explanation values")

    args.harm_metric = [nonblank(item, "harm-metric") for item in args.harm_metric]
    args.stop_rule = [nonblank(item, "stop-rule") for item in args.stop_rule]
    args.rival_explanation = [nonblank(item, "rival-explanation") for item in args.rival_explanation]
    args.bias_flag = [nonblank(item, "bias-flag") for item in args.bias_flag]

    if len(set(args.stop_rule)) != len(args.stop_rule):
        fail("--stop-rule values must be distinct")
    if len(set(args.rival_explanation)) != len(args.rival_explanation):
        fail("--rival-explanation values must be distinct")


def build_card(args: argparse.Namespace) -> dict[str, object]:
    direction_word = "improves upward" if args.desired_direction == "higher" else "improves downward"
    bias_flags = list(DEFAULT_BIAS_FLAGS)
    for item in args.bias_flag:
        if item not in bias_flags:
            bias_flags.append(item)

    support_locator = None
    if args.support != "not-checked":
        support_locator = nonblank(args.evidence_locator, "evidence-locator")

    return {
        "schema_version": SCHEMA_VERSION,
        "card_type": "low-risk-personal-experiment",
        "status": "draft-not-proof",
        "workflow": "TITAN-TRACE",
        "target": args.target,
        "claim_ledger": {
            "candidate_behavior": args.candidate,
            "source_provenance": args.source_provenance,
            "source_locator": args.source_locator,
            "claim_type": args.claim_type,
            "empirical_support": args.support,
            "independent_evidence_locator": support_locator,
            "transferability": args.transferability,
            "safety_gate": "green",
            "domain": args.domain,
        },
        "bias_red_team": [
            {"flag": item, "status": "must-check-not-resolved-by-celebrity-frequency"}
            for item in bias_flags
        ],
        "barrier_diagnosis": {
            "framework": "COM-B",
            "primary_barrier": args.barrier,
            "observation": args.barrier_note,
            "warning": "COM-B diagnosis does not itself prove the intervention is appropriate.",
        },
        "mechanism_hypothesis": {
            "statement": args.mechanism,
            "prediction": args.prediction,
            "falsification_prompt": (
                "Name an observation that would favor a rival explanation over this mechanism before starting."
            ),
        },
        "experiment": {
            "one_primary_change": args.candidate,
            "baseline": {
                "days": args.baseline_days,
                "measure": args.baseline_measure,
            },
            "comparison": args.comparison,
            "duration_days": args.duration_days,
            "measurement_schedule": args.measurement_schedule,
            "primary_outcome": {
                "name": args.primary_outcome,
                "unit": args.outcome_unit,
                "desired_direction": args.desired_direction,
                "minimum_meaningful_change": args.meaningful_change,
            },
            "harm_metrics": args.harm_metric,
            "stop_rules": args.stop_rule,
            "daily_recording_budget_minutes": args.max_burden_minutes,
            "rival_explanations": args.rival_explanation,
            "missing_data_rule": "Record the reason; never encode missing as no harm or no effect.",
            "protocol_change_rule": "Stop and open a new card; never rewrite thresholds after seeing results.",
        },
        "decision_rule": {
            "continue": (
                f"Primary outcome {direction_word} by at least {args.meaningful_change:g} "
                f"{args.outcome_unit} versus the comparison, with no stop rule triggered and sustainable burden."
            ),
            "change": (
                "Only after stopping this card, if one specific, testable COM-B design defect explains low adherence; "
                "re-baseline and preregister a new card."
            ),
            "stop": "Any stop rule, elevated risk, unsustainable burden, uninterpretable data, or failure to reach the meaningful-change threshold.",
        },
        "bounded_inference": {
            "not_proof_of_causality": True,
            "no_population_generalization": True,
            "allowed_wording": (
                "For me, during this period, under these recorded conditions, the observation was ...; "
                "rival explanations remain ..."
            ),
            "cannot_establish": [
                "that the reported high performer succeeded because of this behavior",
                "that the mechanism is uniquely correct",
                "that the result applies to other people",
                "medical, psychological, nutritional, training, legal, or financial efficacy",
            ],
        },
    }


def emit(card: dict[str, object], output: str | None) -> None:
    rendered = json.dumps(card, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if not output:
        sys.stdout.write(rendered)
        return
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(rendered, encoding="utf-8")
    print(f"Wrote TITAN-TRACE card to {path}")


def main() -> None:
    args = parser().parse_args()
    validate(args)
    emit(build_card(args), args.output)


if __name__ == "__main__":
    main()
