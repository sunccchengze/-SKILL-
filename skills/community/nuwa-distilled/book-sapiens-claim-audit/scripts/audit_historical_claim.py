#!/usr/bin/env python3
"""Build a deterministic SCALE-AUDIT plan; never adjudicate historical truth."""

from __future__ import annotations

import argparse
import json
from typing import Iterable

HIGH_RISK_CONTEXTS = {"policy", "ancestry", "territorial"}


def normalized(values: Iterable[str]) -> list[str]:
    return sorted({" ".join(value.split()) for value in values if " ".join(value.split())})


def clean(value: str) -> str:
    return " ".join(value.split())


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--claim", required=True)
    p.add_argument("--scale", choices=("site", "local", "regional", "continental", "global"), required=True)
    p.add_argument("--period", required=True)
    p.add_argument("--region", required=True)
    p.add_argument("--evidence", action="append", default=[], help="Repeatable evidence or proxy item")
    p.add_argument("--alternative", action="append", default=[], help="Repeatable competing explanation")
    p.add_argument("--uncertainty", action="append", default=[], help="Repeatable uncertainty or limitation")
    p.add_argument("--audience", required=True)
    p.add_argument("--use-context", choices=("research", "education", "exhibition", "policy", "ancestry", "territorial"), required=True)
    p.add_argument("--owner", default="")
    p.add_argument("--domain-reviewer", default="")
    p.add_argument("--community-consultation", default="")
    p.add_argument("--appeal-channel", default="")
    p.add_argument("--stop-condition", default="")
    p.add_argument("--dehumanizing-use", action="store_true")
    p.add_argument("--rights-denial", action="store_true")
    p.add_argument("--atrocity-denial", action="store_true")
    return p


def build(args: argparse.Namespace) -> dict[str, object]:
    evidence = normalized(args.evidence)
    alternatives = normalized(args.alternative)
    uncertainties = normalized(args.uncertainty)
    block_reasons = []
    if args.dehumanizing_use:
        block_reasons.append("dehumanizing-use")
    if args.rights_denial:
        block_reasons.append("rights-denial")
    if args.atrocity_denial:
        block_reasons.append("atrocity-denial")

    status = "READY_FOR_AUDIT"
    reasons: list[str] = []
    if block_reasons:
        status = "BLOCKED"
        reasons.extend(block_reasons)
    elif not evidence or not alternatives or not uncertainties:
        status = "STOP"
        if not evidence:
            reasons.append("no-evidence-ledger")
        if not alternatives:
            reasons.append("no-competing-explanation")
        if not uncertainties:
            reasons.append("no-uncertainty-record")
    elif args.use_context in HIGH_RISK_CONTEXTS:
        gate = {
            "owner": clean(args.owner),
            "domain_reviewer": clean(args.domain_reviewer),
            "community_consultation": clean(args.community_consultation),
            "appeal_channel": clean(args.appeal_channel),
            "stop_condition": clean(args.stop_condition),
        }
        missing = sorted(key for key, value in gate.items() if not value)
        if missing:
            status = "STOP"
            reasons.append("high-risk-gate-missing:" + ",".join(missing))

    scale_warnings = []
    if args.scale in {"continental", "global"} and len(evidence) < 2:
        scale_warnings.append("broad-scale claim has fewer than two evidence entries")
    if args.scale == "global":
        scale_warnings.append("global claims require multi-region coverage; entries are not automatically independent")

    return {
        "claim": clean(args.claim),
        "decision": {"reasons": sorted(reasons), "status": status},
        "disclaimer": "This is an audit plan, not a historical truth verdict or a rights determination.",
        "epistemic_layers": {
            "A": "book attribution must be edition-checked",
            "B": "genre, translation, and concept context",
            "C": "independent evidence and counterevidence",
            "D": "SCALE-AUDIT inference; not Harari's words",
        },
        "evidence_plan": {
            "alternatives": alternatives,
            "evidence": evidence,
            "uncertainties": uncertainties,
            "required_uncertainty_vector": ["observation", "construct", "causal", "extrapolation", "counterfactual"],
        },
        "rights_gate": {
            "appeal_channel": clean(args.appeal_channel),
            "community_consultation": clean(args.community_consultation),
            "domain_reviewer": clean(args.domain_reviewer),
            "owner": clean(args.owner),
            "stop_condition": clean(args.stop_condition),
        },
        "scale_card": {
            "audience": clean(args.audience),
            "period": clean(args.period),
            "region": clean(args.region),
            "scale": args.scale,
            "warnings": sorted(scale_warnings),
        },
        "use_context": args.use_context,
        "valid_dispositions": ["retain", "split", "downgrade", "stop"],
    }


def main() -> None:
    args = parser().parse_args()
    print(json.dumps(build(args), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
