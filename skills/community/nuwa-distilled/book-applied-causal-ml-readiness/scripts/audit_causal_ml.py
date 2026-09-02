#!/usr/bin/env python3
"""Build a deterministic causal-ML readiness contract; never estimate an effect."""

from __future__ import annotations

import argparse
import json
import re
from typing import Iterable


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def normalized(values: Iterable[str] | None) -> list[str]:
    """Normalize, de-duplicate case-insensitively, and sort user-supplied lists."""
    found: dict[str, str] = {}
    for raw in values or []:
        value = clean(raw)
        if value:
            found.setdefault(value.casefold(), value)
    return sorted(found.values(), key=lambda item: (item.casefold(), item))


def parser() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(
        description="Audit whether a causal question is ready for an estimation plan. No data are loaded and no effect is estimated."
    )
    cli.add_argument("--question", required=True)
    cli.add_argument("--treatment", required=True)
    cli.add_argument("--outcome", required=True)
    cli.add_argument("--unit", required=True)
    cli.add_argument("--time-zero", required=True)
    cli.add_argument("--estimand", required=True, choices=("ate", "att", "cate", "policy-value"))
    cli.add_argument("--design", required=True, choices=("randomized", "observational", "natural-experiment"))
    cli.add_argument("--identification-assumption", action="append", default=[])
    cli.add_argument("--control", action="append", default=[])
    cli.add_argument("--post-treatment-control", action="append", default=[])
    cli.add_argument("--overlap-check", default="")
    cli.add_argument("--split-plan", default="")
    cli.add_argument("--nuisance-evaluation", default="")
    cli.add_argument("--sensitivity", default="")
    cli.add_argument("--heterogeneity-plan", default="")
    cli.add_argument("--transport-target", default="")
    cli.add_argument("--transport-assumption", action="append", default=[])
    cli.add_argument("--policy-use", default="analysis only")
    cli.add_argument("--owner", required=True)
    cli.add_argument("--use-dml", action="store_true")
    cli.add_argument("--unobserved-confounding-concern", action="store_true")
    cli.add_argument("--interference-concern", action="store_true")
    cli.add_argument("--high-stakes", action="store_true")
    return cli


def build(args: argparse.Namespace) -> dict[str, object]:
    assumptions = normalized(args.identification_assumption)
    controls = normalized(args.control)
    post_controls = normalized(args.post_treatment_control)
    transport_assumptions = normalized(args.transport_assumption)
    gates: list[dict[str, str]] = []

    def gate(name: str, state: str, reason: str) -> None:
        gates.append({"gate": name, "reason": reason, "state": state})

    gate(
        "estimand-definition",
        "pass",
        f"target is {args.estimand}; effect interpretation still requires a treatment version and time horizon",
    )
    gate(
        "identification-argument",
        "pass" if assumptions else "block",
        "assumptions are explicit but not empirically proven" if assumptions else "no identification assumption was supplied",
    )
    gate(
        "temporal-order",
        "block" if post_controls else "pass",
        "post-treatment variables were proposed as controls" if post_controls else "no declared post-treatment control",
    )
    gate(
        "overlap-positivity",
        "pass" if clean(args.overlap_check) else "block",
        "a diagnostic is planned; its result remains unknown" if clean(args.overlap_check) else "no overlap/positivity diagnostic was supplied",
    )
    gate(
        "unobserved-confounding",
        "block" if args.unobserved_confounding_concern else "review",
        "a credible hidden-confounding concern cannot be repaired by DML or sensitivity analysis"
        if args.unobserved_confounding_concern
        else "absence of a declared concern does not prove exchangeability",
    )
    gate(
        "interference",
        "block" if args.interference_concern else "review",
        "declared spillovers conflict with a no-interference interpretation"
        if args.interference_concern
        else "interference still requires domain review",
    )
    if args.design == "observational":
        gate(
            "observational-sensitivity",
            "pass" if clean(args.sensitivity) else "block",
            "sensitivity analysis is planned but does not identify hidden bias"
            if clean(args.sensitivity)
            else "observational design lacks a sensitivity plan",
        )
        gate(
            "pre-treatment-controls",
            "pass" if controls else "block",
            "candidate controls require DAG/timing review" if controls else "no pre-treatment adjustment set was supplied",
        )
    else:
        gate("design-specific-validity", "review", "randomization or instrument validity must be checked from design records")
    if args.use_dml:
        gate(
            "dml-implementation",
            "pass" if clean(args.split_plan) and clean(args.nuisance_evaluation) else "block",
            "cross-fitting/splitting and nuisance evaluation are planned"
            if clean(args.split_plan) and clean(args.nuisance_evaluation)
            else "DML was requested without both a split plan and out-of-fold nuisance evaluation",
        )
    else:
        gate("estimator-selection", "review", "DML is not mandatory; choose an estimator only after identification")
    if args.estimand == "cate":
        gate(
            "heterogeneity",
            "pass" if clean(args.heterogeneity_plan) else "block",
            "heterogeneity plan is predeclared" if clean(args.heterogeneity_plan) else "CATE lacks subgroup multiplicity/honesty plan",
        )
    if clean(args.transport_target):
        gate(
            "transport",
            "pass" if transport_assumptions else "block",
            "transport assumptions are explicit but unverified" if transport_assumptions else "target differs from study population without transport assumptions",
        )

    blocking = [item["gate"] for item in gates if item["state"] == "block"]
    if post_controls:
        status = "BLOCKED_POST_TREATMENT_BIAS"
    elif args.unobserved_confounding_concern:
        status = "BLOCKED_UNIDENTIFIED_CONFOUNDING"
    elif args.interference_concern:
        status = "BLOCKED_INTERFERENCE"
    elif blocking:
        status = "BLOCKED_DESIGN"
    elif args.high_stakes or clean(args.policy_use).casefold() != "analysis only":
        status = "GOVERNANCE_REVIEW_REQUIRED"
    else:
        status = "READY_FOR_ESTIMATION_PLAN"

    return {
        "claim_layer": "D-Skill operational synthesis",
        "decision": {
            "blocking_gates": sorted(blocking),
            "does_not_mean": "identified effect, unbiased estimate, transportability, or deployment approval",
            "status": status,
        },
        "estimand_contract": {
            "design": args.design,
            "estimand": args.estimand,
            "outcome": clean(args.outcome),
            "question": clean(args.question),
            "time_zero": clean(args.time_zero),
            "treatment": clean(args.treatment),
            "unit": clean(args.unit),
        },
        "gates": sorted(gates, key=lambda item: item["gate"]),
        "methods": {
            "controls": controls,
            "dml_requested": bool(args.use_dml),
            "dml_boundary": "orthogonality and cross-fitting address nuisance-estimation bias under assumptions; they do not create identification",
            "heterogeneity_plan": clean(args.heterogeneity_plan),
            "nuisance_evaluation": clean(args.nuisance_evaluation),
            "overlap_check": clean(args.overlap_check),
            "post_treatment_controls": post_controls,
            "sensitivity": clean(args.sensitivity),
            "split_plan": clean(args.split_plan),
        },
        "normalized": True,
        "ownership": {"owner": clean(args.owner), "policy_use": clean(args.policy_use)},
        "transport": {
            "assumptions": transport_assumptions,
            "target": clean(args.transport_target),
        },
        "version": "1.0.0",
    }


def main() -> None:
    args = parser().parse_args()
    print(json.dumps(build(args), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
