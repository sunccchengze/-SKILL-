#!/usr/bin/env python3
"""Create a deterministic judgment-system audit plan, never an individual decision."""

from __future__ import annotations

import argparse
import json
from typing import Iterable

HIGH_IMPACT = {"hiring", "clinical", "legal", "benefits", "education-access"}


def clean(value: str) -> str:
    return " ".join(value.split())


def normalized(values: Iterable[str]) -> list[str]:
    return sorted({clean(value) for value in values if clean(value)})


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--system", required=True)
    p.add_argument("--case-spec", required=True)
    p.add_argument("--equivalence-rule", required=True)
    p.add_argument("--judge-count", type=int, required=True)
    p.add_argument("--repeat-rounds", type=int, required=True)
    p.add_argument("--target-type", choices=("verified-outcome", "expert-consensus", "policy-rule", "no-defensible-target"), required=True)
    p.add_argument("--outcome", required=True)
    p.add_argument("--intervention", action="append", default=[])
    p.add_argument("--cost-risk", required=True)
    p.add_argument("--owner", required=True)
    p.add_argument("--use-context", choices=("management", "forecasting", "hiring", "clinical", "legal", "benefits", "education-access"), required=True)
    p.add_argument("--qualified-reviewer", default="")
    p.add_argument("--subgroup-audit", default="")
    p.add_argument("--appeal-route", default="")
    p.add_argument("--stop-condition", default="")
    p.add_argument("--automation-review", default="")
    p.add_argument("--automate", action="store_true")
    p.add_argument("--remove-all-discretion", action="store_true")
    p.add_argument("--emergency", action="store_true")
    return p


def build(args: argparse.Namespace) -> dict[str, object]:
    interventions = normalized(args.intervention)
    reasons: list[str] = []
    status = "READY_FOR_AUDIT"

    if args.emergency:
        status = "BLOCKED_FOR_EMERGENCY"
        reasons.append("refer-to-local-emergency-and-qualified-services")
    elif args.remove_all_discretion:
        status = "STOP"
        reasons.append("blanket-discretion-removal-not-supported")
    else:
        if args.judge_count < 1 or args.repeat_rounds < 1:
            reasons.append("counts-must-be-positive")
        if args.judge_count < 2 and args.repeat_rounds < 2:
            reasons.append("cannot-estimate-inter-or-intra-judge-variation")
        if not interventions:
            reasons.append("no-testable-intervention")
        high_impact = args.use_context in HIGH_IMPACT
        gate = {
            "appeal_route": clean(args.appeal_route),
            "qualified_reviewer": clean(args.qualified_reviewer),
            "stop_condition": clean(args.stop_condition),
            "subgroup_audit": clean(args.subgroup_audit),
        }
        if high_impact:
            missing = sorted(key for key, value in gate.items() if not value)
            if missing:
                reasons.append("high-impact-gate-missing:" + ",".join(missing))
        if args.automate and not clean(args.automation_review):
            reasons.append("automation-review-missing")
        if reasons:
            status = "STOP"

    accuracy_claim = args.target_type == "verified-outcome"
    target_warnings = []
    if args.target_type == "no-defensible-target":
        target_warnings.append("accuracy claims are prohibited; audit reliability and procedure only")
    elif args.target_type in {"expert-consensus", "policy-rule"}:
        target_warnings.append("the selected target is a reference standard, not necessarily ground truth")

    identifiability = {
        "level_noise": args.judge_count >= 2,
        "occasion_noise": args.repeat_rounds >= 2,
        "pattern_noise": args.judge_count >= 2,
    }
    identifiability_notes = []
    if not identifiability["occasion_noise"]:
        identifiability_notes.append("occasion noise needs repeated judgments under controlled information")
    if args.judge_count < 2:
        identifiability_notes.append("level and pattern noise need multiple judges across comparable cases")

    return {
        "audit_design": {
            "case_spec": clean(args.case_spec),
            "equivalence_rule": clean(args.equivalence_rule),
            "judge_count": args.judge_count,
            "outcome": clean(args.outcome),
            "repeat_rounds": args.repeat_rounds,
            "system": clean(args.system),
        },
        "decision": {"reasons": sorted(reasons), "status": status},
        "disclaimer": "This plan does not decide any individual case and consistency is not proof of correctness.",
        "epistemic_layers": {
            "A": "Noise book claim",
            "B": "author follow-up and method context",
            "C": "independent evidence or counterevidence",
            "D": "NOISE-AUDIT inference, not an author quotation",
        },
        "governance": {
            "appeal_route": clean(args.appeal_route),
            "automation_review": clean(args.automation_review),
            "cost_risk": clean(args.cost_risk),
            "owner": clean(args.owner),
            "qualified_reviewer": clean(args.qualified_reviewer),
            "stop_condition": clean(args.stop_condition),
            "subgroup_audit": clean(args.subgroup_audit),
        },
        "identifiability": {"components": identifiability, "notes": sorted(identifiability_notes)},
        "intervention_trial": {
            "interventions": interventions,
            "required_metrics": ["reliability", "accuracy-if-defensible", "group-harms", "decision-change", "cost", "appeals"],
        },
        "target": {
            "accuracy_claim_permitted": accuracy_claim,
            "type": args.target_type,
            "warnings": sorted(target_warnings),
        },
        "use_context": args.use_context,
    }


def main() -> None:
    print(json.dumps(build(parser().parse_args()), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
