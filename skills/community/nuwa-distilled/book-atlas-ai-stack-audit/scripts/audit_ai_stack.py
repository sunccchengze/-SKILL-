#!/usr/bin/env python3
"""Create a deterministic, evidence-bounded AI stack audit; never approve deployment."""

from __future__ import annotations

import argparse
import json
import re
from typing import Iterable


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
        description="Audit material, labor, data, classification, affect, state, and power dependencies."
    )
    cli.add_argument("--system", required=True)
    cli.add_argument("--purpose", required=True)
    cli.add_argument("--geography", required=True)
    cli.add_argument("--as-of", required=True)
    cli.add_argument("--owner", required=True)
    cli.add_argument("--lifecycle-stage", required=True, choices=("proposal", "procurement", "training", "deployment", "retirement"))
    cli.add_argument("--supply-node", action="append", default=[])
    cli.add_argument("--worker-group", action="append", default=[])
    cli.add_argument("--data-source", action="append", default=[])
    cli.add_argument("--classification", action="append", default=[])
    cli.add_argument("--affected-group", action="append", default=[])
    cli.add_argument("--state-linkage", action="append", default=[])
    cli.add_argument("--material-evidence", action="append", default=[])
    cli.add_argument("--labor-evidence", action="append", default=[])
    cli.add_argument("--provenance-evidence", action="append", default=[])
    cli.add_argument("--remedy", action="append", default=[])
    cli.add_argument("--uncertainty", action="append", default=[])
    cli.add_argument("--claim-denominator", default="")
    cli.add_argument("--stop-condition", action="append", default=[])
    cli.add_argument("--emotion-inference", action="store_true")
    cli.add_argument("--biometric-classification", action="store_true")
    cli.add_argument("--undocumented-third-party", action="store_true")
    cli.add_argument("--missing-worker-voice", action="store_true")
    cli.add_argument("--high-stakes", action="store_true")
    return cli


def build(args: argparse.Namespace) -> dict[str, object]:
    lists = {
        "affected_groups": normalized(args.affected_group),
        "classifications": normalized(args.classification),
        "data_sources": normalized(args.data_source),
        "labor_evidence": normalized(args.labor_evidence),
        "material_evidence": normalized(args.material_evidence),
        "provenance_evidence": normalized(args.provenance_evidence),
        "remedies": normalized(args.remedy),
        "state_linkages": normalized(args.state_linkage),
        "stop_conditions": normalized(args.stop_condition),
        "supply_nodes": normalized(args.supply_node),
        "uncertainties": normalized(args.uncertainty),
        "worker_groups": normalized(args.worker_group),
    }
    lens_requirements = {
        "affect": bool(lists["classifications"]),
        "classification": bool(lists["classifications"] and lists["affected_groups"]),
        "data": bool(lists["data_sources"] and lists["provenance_evidence"]),
        "earth": bool(lists["supply_nodes"] and lists["material_evidence"] and clean(args.claim_denominator)),
        "labor": bool(lists["worker_groups"] and lists["labor_evidence"] and not args.missing_worker_voice),
        "power": bool(lists["affected_groups"] and lists["remedies"] and lists["stop_conditions"]),
        "space": bool(lists["supply_nodes"]),
        "state": bool(lists["state_linkages"]),
    }
    gaps = sorted(name for name, complete in lens_requirements.items() if not complete)
    red_flags: list[str] = []
    if args.emotion_inference:
        red_flags.append("emotion-inference-construct-validity")
    if args.biometric_classification:
        red_flags.append("biometric-rights-and-disparity")
    if args.undocumented_third_party:
        red_flags.append("undocumented-value-chain-component")
    if args.missing_worker_voice:
        red_flags.append("worker-voice-absent")

    if args.emotion_inference:
        status = "BLOCKED_SCIENTIFIC_VALIDITY_REVIEW"
    elif args.undocumented_third_party:
        status = "BLOCKED_PROVENANCE"
    elif args.biometric_classification and args.high_stakes:
        status = "BLOCKED_RIGHTS_REVIEW"
    elif gaps:
        status = "INCOMPLETE_STACK_MAP"
    else:
        status = "GOVERNANCE_REVIEW_REQUIRED"

    lenses = [
        {
            "complete": lens_requirements[name],
            "lens": name,
            "question": {
                "earth": "Which materials, energy, water, emissions, land, and waste are inside the declared boundary?",
                "labor": "Which direct and subcontracted workers make the system possible, under what conditions and voice?",
                "data": "Who produced and documented the data, permissions, exclusions, maintenance, and withdrawal?",
                "classification": "Which ontology turns contested social categories into labels, and who can contest it?",
                "affect": "Does the measured construct have contextual validity rather than a face-to-inner-state shortcut?",
                "state": "Which procurement, surveillance, policing, military, benefit, or regulatory relationships shape use?",
                "power": "Who decides, benefits, bears cost, audits, appeals, obtains remedy, and can stop the system?",
                "space": "Where are extraction, computation, annotation, deployment, and disposal physically situated?",
            }[name],
        }
        for name in sorted(lens_requirements)
    ]
    return {
        "audit_boundary": {
            "as_of": clean(args.as_of),
            "claim_denominator": clean(args.claim_denominator),
            "geography": clean(args.geography),
            "lifecycle_stage": args.lifecycle_stage,
            "purpose": clean(args.purpose),
            "system": clean(args.system),
        },
        "claim_layer": "D-Skill operational synthesis",
        "decision": {
            "does_not_mean": "ethical approval, legal compliance, complete lifecycle accounting, or a per-model/per-prompt footprint",
            "gaps": gaps,
            "red_flags": sorted(red_flags),
            "status": status,
        },
        "evidence_register": lists,
        "lenses": lenses,
        "normalized": True,
        "owner": clean(args.owner),
        "quantification_boundary": "Do not allocate facility or corporate totals to a model, user, or prompt without an auditable allocation method and uncertainty interval.",
        "version": "1.0.0",
    }


def main() -> None:
    args = parser().parse_args()
    print(json.dumps(build(args), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
