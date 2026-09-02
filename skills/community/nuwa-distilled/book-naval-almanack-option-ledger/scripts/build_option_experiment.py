#!/usr/bin/env python3
"""Build a deterministic attributed option experiment; never promise success."""

from __future__ import annotations

import argparse
import json
from typing import Iterable


def clean(value: str) -> str:
    return " ".join(value.split())


def normalized(values: Iterable[str]) -> list[str]:
    return sorted({clean(value) for value in values if clean(value)})


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--proposition", required=True)
    p.add_argument("--attribution", choices=("naval-primary", "jorgenson-curation", "external-evidence", "skill-inference"), required=True)
    p.add_argument("--primary-text-checked", action="store_true")
    p.add_argument("--source", required=True)
    p.add_argument("--domain", choices=("specific-knowledge", "accountability", "leverage", "ownership", "judgment", "compounding", "wealth", "happiness", "mindfulness"), required=True)
    p.add_argument("--base-rate", required=True)
    p.add_argument("--access-constraint", action="append", default=[])
    p.add_argument("--downside-cap", required=True)
    p.add_argument("--reversible-test", required=True)
    p.add_argument("--success-metric", required=True)
    p.add_argument("--harm-metric", required=True)
    p.add_argument("--stop-condition", required=True)
    p.add_argument("--review-days", type=int, required=True)
    p.add_argument("--stake", choices=("low", "medium", "high"), required=True)
    p.add_argument("--owner", required=True)
    p.add_argument("--career-exit", action="store_true")
    p.add_argument("--debt", action="store_true")
    p.add_argument("--concentrated-capital", action="store_true")
    p.add_argument("--runway", default="")
    p.add_argument("--qualified-reviewer", default="")
    p.add_argument("--dependents-plan", default="")
    p.add_argument("--personalized-investment-advice", action="store_true")
    p.add_argument("--clinical-treatment", action="store_true")
    p.add_argument("--crisis", action="store_true")
    p.add_argument("--unlawful", action="store_true")
    p.add_argument("--exploitative", action="store_true")
    return p


def build(args: argparse.Namespace) -> dict[str, object]:
    constraints = normalized(args.access_constraint)
    blocked = []
    for flag, reason in (
        (args.personalized_investment_advice, "personalized-investment-advice"),
        (args.clinical_treatment, "clinical-treatment-substitution"),
        (args.crisis, "crisis-needs-local-qualified-support"),
        (args.unlawful, "unlawful-action"),
        (args.exploitative, "exploitative-use"),
    ):
        if flag:
            blocked.append(reason)

    reasons: list[str] = []
    status = "READY_FOR_REVERSIBLE_TEST"
    if blocked:
        status = "BLOCKED"
        reasons.extend(blocked)
    else:
        if args.attribution == "naval-primary" and not args.primary_text_checked:
            reasons.append("naval-primary-source-not-checked")
        if not constraints:
            reasons.append("no-access-constraint-recorded")
        if args.review_days < 1:
            reasons.append("review-days-must-be-positive")
        high_risk = args.stake == "high" or args.career_exit or args.debt or args.concentrated_capital
        if high_risk:
            gate = {
                "dependents_plan": clean(args.dependents_plan),
                "qualified_reviewer": clean(args.qualified_reviewer),
                "runway": clean(args.runway),
            }
            missing = sorted(key for key, value in gate.items() if not value)
            if missing:
                reasons.append("high-risk-gate-missing:" + ",".join(missing))
            else:
                reasons.append("high-risk-action-not-approved; review only")
        if reasons:
            status = "STOP" if any(not item.startswith("high-risk-action-not-approved") for item in reasons) else "REVIEW_ONLY"

    return {
        "attribution": {
            "layer": {
                "external-evidence": "C",
                "jorgenson-curation": "A",
                "naval-primary": "B",
                "skill-inference": "D",
            }[args.attribution],
            "primary_text_checked": bool(args.primary_text_checked),
            "source": clean(args.source),
            "type": args.attribution,
        },
        "decision": {"reasons": sorted(reasons), "status": status},
        "disclaimer": "No wealth, business, career, investment, or wellbeing outcome is promised; this is not personalized financial, legal, tax, or clinical advice.",
        "experiment": {
            "domain": args.domain,
            "harm_metric": clean(args.harm_metric),
            "owner": clean(args.owner),
            "proposition": clean(args.proposition),
            "reversible_test": clean(args.reversible_test),
            "review_days": args.review_days,
            "stop_condition": clean(args.stop_condition),
            "success_metric": clean(args.success_metric),
        },
        "risk_ledger": {
            "access_constraints": constraints,
            "base_rate": clean(args.base_rate),
            "dependents_plan": clean(args.dependents_plan),
            "downside_cap": clean(args.downside_cap),
            "qualified_reviewer": clean(args.qualified_reviewer),
            "runway": clean(args.runway),
            "stake": args.stake,
            "warnings": [
                "base rates constrain belief but do not predict an individual result",
                "permissionless reach can coexist with superstar concentration and platform dependence",
                "accountability and ownership do not justify ruin or shifting harm to others",
            ],
        },
        "valid_review_outcomes": ["stop", "modify", "repeat", "scale-one-step"],
    }


def main() -> None:
    print(json.dumps(build(parser().parse_args()), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
