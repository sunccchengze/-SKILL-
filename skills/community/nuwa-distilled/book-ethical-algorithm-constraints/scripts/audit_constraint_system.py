#!/usr/bin/env python3
"""Build a deterministic algorithmic-constraint audit without claiming moral completeness."""

from __future__ import annotations

import argparse
import json
import re
from typing import Iterable

FAIRNESS_CONFLICT_SET = {"calibration", "equalized-odds"}


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def normalized(values: Iterable[str] | None) -> list[str]:
    found: dict[str, str] = {}
    for raw in values or []:
        value = clean(raw)
        if value:
            found.setdefault(value.casefold(), value)
    return sorted(found.values(), key=lambda item: (item.casefold(), item))


def parser() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(
        description="Audit privacy, fairness, strategic response, adaptivity, and interpretability constraints."
    )
    cli.add_argument("--system", required=True)
    cli.add_argument("--decision", required=True)
    cli.add_argument("--affected-group", action="append", default=[])
    cli.add_argument("--protected-group", action="append", default=[])
    cli.add_argument("--owner", required=True)
    cli.add_argument("--stakes", required=True, choices=("low", "medium", "high"))
    cli.add_argument("--legal-basis", default="")
    cli.add_argument("--privacy-unit", default="")
    cli.add_argument("--neighboring-relation", default="")
    cli.add_argument("--epsilon", type=float)
    cli.add_argument("--delta", type=float)
    cli.add_argument("--query-count", type=int, default=0)
    cli.add_argument("--fairness-goal", action="append", default=[], choices=("demographic-parity", "equalized-odds", "calibration", "individual", "subgroup"))
    cli.add_argument("--base-rate-difference", default="unknown", choices=("yes", "no", "unknown"))
    cli.add_argument("--harm", action="append", default=[])
    cli.add_argument("--strategic-response", action="append", default=[])
    cli.add_argument("--feedback-monitor", action="append", default=[])
    cli.add_argument("--fresh-holdout", default="")
    cli.add_argument("--data-reuse-count", type=int, default=0)
    cli.add_argument("--explanation-method", default="")
    cli.add_argument("--appeal-path", default="")
    cli.add_argument("--human-review", default="")
    cli.add_argument("--stop-condition", action="append", default=[])
    cli.add_argument("--request-deployment", action="store_true")
    return cli


def build(args: argparse.Namespace) -> dict[str, object]:
    if args.epsilon is not None and args.epsilon < 0:
        raise SystemExit("--epsilon must be non-negative")
    if args.delta is not None and not (0 <= args.delta < 1):
        raise SystemExit("--delta must satisfy 0 <= delta < 1")
    if args.query_count < 0 or args.data_reuse_count < 0:
        raise SystemExit("query and reuse counts must be non-negative")

    affected = normalized(args.affected_group)
    protected = normalized(args.protected_group)
    fairness = normalized(args.fairness_goal)
    harms = normalized(args.harm)
    responses = normalized(args.strategic_response)
    monitors = normalized(args.feedback_monitor)
    stops = normalized(args.stop_condition)
    blocks: list[str] = []
    tradeoffs: list[str] = []
    reviews: list[str] = []

    dp_requested = args.epsilon is not None or args.delta is not None
    if dp_requested and not (clean(args.privacy_unit) and clean(args.neighboring_relation)):
        blocks.append("privacy-neighboring-relation-unspecified")
    if dp_requested and args.query_count <= 0:
        blocks.append("privacy-composition-count-missing")
    if fairness and not protected:
        blocks.append("fairness-groups-unspecified")
    if FAIRNESS_CONFLICT_SET.issubset(set(fairness)) and args.base_rate_difference != "no":
        tradeoffs.append("calibration-versus-equalized-odds-under-differing-or-unknown-base-rates")
    if "subgroup" in fairness:
        reviews.append("subgroup-search-capacity-multiplicity-and-sample-size")
    if args.stakes == "high" and not (clean(args.appeal_path) and clean(args.human_review) and stops):
        blocks.append("high-stakes-due-process-incomplete")
    if args.stakes in {"medium", "high"} and not responses:
        blocks.append("strategic-response-unmodeled")
    if args.stakes in {"medium", "high"} and not monitors:
        blocks.append("performative-feedback-unmonitored")
    if args.data_reuse_count > 1 and not clean(args.fresh_holdout):
        blocks.append("adaptive-holdout-validity-uncontrolled")
    if not affected or not harms:
        blocks.append("affected-parties-or-harms-unspecified")
    if not clean(args.legal_basis):
        reviews.append("legal-and-institutional-authority")
    if clean(args.explanation_method):
        reviews.append("explanation-fidelity-stability-and-human-meaning")

    if blocks:
        status = "BLOCKED_CONSTRAINT_SPECIFICATION"
    elif tradeoffs:
        status = "TRADEOFF_DECISION_REQUIRED"
    else:
        status = "GOVERNANCE_REVIEW_REQUIRED"

    return {
        "claim_layer": "D-Skill operational synthesis",
        "context": {
            "affected_groups": affected,
            "decision": clean(args.decision),
            "harms": harms,
            "owner": clean(args.owner),
            "protected_groups": protected,
            "stakes": args.stakes,
            "system": clean(args.system),
        },
        "decision_gate": {
            "blocks": sorted(blocks),
            "does_not_mean": "moral completeness, legal compliance, justice, causal fairness, or deployment approval",
            "deployment_requested": bool(args.request_deployment),
            "status": status,
            "tradeoffs": sorted(tradeoffs),
        },
        "dynamics": {
            "feedback_monitors": monitors,
            "strategic_responses": responses,
        },
        "fairness": {
            "base_rate_difference": args.base_rate_difference,
            "goals": fairness,
            "warning": "metrics encode distinct normative choices and may be jointly infeasible; report harms and denominators, not one fairness score",
        },
        "interpretability": {
            "appeal_path": clean(args.appeal_path),
            "explanation_method": clean(args.explanation_method),
            "human_review": clean(args.human_review),
            "review_questions": sorted(reviews),
        },
        "normalized": True,
        "privacy": {
            "delta": args.delta,
            "epsilon": args.epsilon,
            "neighboring_relation": clean(args.neighboring_relation),
            "privacy_unit": clean(args.privacy_unit),
            "query_count": args.query_count,
            "warning": "a differential-privacy guarantee bounds a specified participation effect under composition; it is not secrecy, security, consent, or protection from population facts",
        },
        "validity": {
            "data_reuse_count": args.data_reuse_count,
            "fresh_holdout": clean(args.fresh_holdout),
            "stop_conditions": stops,
        },
        "version": "1.0.0",
    }


def main() -> None:
    args = parser().parse_args()
    print(json.dumps(build(args), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
