#!/usr/bin/env python3
"""Generate a systems-intervention worksheet without treating a CLD as causal proof."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

EVIDENCE_STATES = {
    "stakeholder-hypothesis",
    "literature-supported-link",
    "measured-association",
    "identified-causal-effect",
}


def parse_link(raw: str) -> dict[str, str]:
    parts = [part.strip() for part in raw.split("|")]
    if len(parts) != 5:
        raise ValueError("--link must be FROM|POLARITY|TO|EVIDENCE_STATE|SOURCE")
    source, polarity, target, evidence, citation = parts
    if not source or not target or not citation:
        raise ValueError("link endpoints and source must be non-empty")
    if polarity not in {"+", "-"}:
        raise ValueError("link polarity must be + or -")
    if evidence not in EVIDENCE_STATES:
        raise ValueError("invalid evidence state: " + evidence)
    return {
        "from": source,
        "polarity": polarity,
        "to": target,
        "evidence_state": evidence,
        "source_or_design": citation,
        "mechanism": "TO VERIFY",
        "delay": "UNKNOWN",
        "rival_explanation": "REQUIRED",
        "falsifier": "REQUIRED",
    }


def build(args: argparse.Namespace) -> dict:
    if not args.stakeholder:
        raise ValueError("at least one --stakeholder is required")
    return {
        "method": "SYSTEM-TRACE (Skill synthesis; not a Meadows-authored method)",
        "focus": {
            "problem": args.problem,
            "desired_outcome": args.outcome,
            "horizon": args.horizon,
            "boundary": args.boundary or "TO DEFINE",
            "emergency_gate": "Run emergency/professional protocol first if immediate harm exists.",
            "boundary_omissions": ["TO IDENTIFY"],
        },
        "stakeholders": [
            {"name": name, "benefits_costs_power_exit": "TO DOCUMENT", "dissent": "OPEN"}
            for name in args.stakeholder
        ],
        "behavior_over_time": [
            {"variable": args.outcome, "unit_or_proxy": "TO DEFINE", "baseline": "TO MEASURE", "turning_points": []}
        ],
        "stock_flow_ledger": [
            {"stock": "TO DEFINE", "unit_or_proxy": "TO DEFINE", "inflows": [], "outflows": [], "data_source": "TO DEFINE"}
        ],
        "links": [parse_link(item) for item in (args.link or [])],
        "epistemic_notice": [
            "A causal-loop diagram is a testable model, not causal proof.",
            "Measured association is not an identified causal effect.",
            "Graph centrality must not determine leverage priority.",
        ],
        "rival_structures": [
            {"label": "A", "explanation": "REQUIRED", "discriminating_observation": "REQUIRED"},
            {"label": "B", "explanation": "REQUIRED", "discriminating_observation": "REQUIRED"},
        ],
        "leverage_hypotheses": [
            {
                "candidate": "TO PROPOSE",
                "mechanism": "TO VERIFY",
                "evidence": "TO CITE",
                "distributional_effects": "TO ASSESS",
                "reversibility": "REQUIRED",
                "stop_condition": "REQUIRED",
                "priority_rule": "mechanism + evidence + controllability + equity + reversibility; never centrality alone",
            }
        ],
        "bounded_experiment": {
            "baseline": "TO MEASURE",
            "comparison_or_staging": "TO DESIGN",
            "process_metric": "TO DEFINE",
            "outcome_metric": args.outcome,
            "distribution_metric": "TO DEFINE",
            "side_effect_metric": "TO DEFINE",
            "review_date": "TO SET",
            "stop_condition": "TO SET",
            "evidence_return": "Update link states while preserving prior versions.",
        },
    }


def markdown(data: dict) -> str:
    focus = data["focus"]
    lines = [
        "# SYSTEM-TRACE 系统干预工作表",
        "",
        f"- 问题：{focus['problem']}",
        f"- 期望结果：{focus['desired_outcome']}",
        f"- 时限：{focus['horizon']}",
        f"- 边界：{focus['boundary']}",
        f"- 应急门：{focus['emergency_gate']}",
        "",
        "## 利益相关者",
    ]
    lines.extend(f"- {x['name']}：{x['benefits_costs_power_exit']}；异议={x['dissent']}" for x in data["stakeholders"])
    lines += ["", "## 连接登记（图是待检验模型，不是因果证明）", "", "| From | ± | To | 证据状态 | 来源/设计 | 机制 | 竞争解释 | 反证 |", "|---|---|---|---|---|---|---|---|"]
    if data["links"]:
        for link in data["links"]:
            lines.append("| {from} | {polarity} | {to} | {evidence_state} | {source_or_design} | {mechanism} | {rival_explanation} | {falsifier} |".format(**link))
    else:
        lines.append("| TO DEFINE | | TO DEFINE | stakeholder-hypothesis | REQUIRED | TO VERIFY | REQUIRED | REQUIRED |")
    lines += [
        "", "## 竞争结构", "- A：REQUIRED；区分观测：REQUIRED", "- B：REQUIRED；区分观测：REQUIRED",
        "", "## 杠杆假设", "- 机制、证据、可控性、权益与可逆性共同排序；**禁止按图中心性直接排序**。",
        "- 候选：TO PROPOSE；可逆性：REQUIRED；停止条件：REQUIRED",
        "", "## 有界试点与证据回传", f"- 基线：{data['bounded_experiment']['baseline']}",
        f"- 结果指标：{data['bounded_experiment']['outcome_metric']}", "- 分配/副作用指标：TO DEFINE", "- 检查日期与停止条件：TO SET",
        "- 回传：保留版本并更新连接证据状态；相关不得直接升级为已识别因果效应。", "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--problem", required=True)
    parser.add_argument("--outcome", required=True)
    parser.add_argument("--horizon", required=True)
    parser.add_argument("--boundary")
    parser.add_argument("--stakeholder", action="append")
    parser.add_argument("--link", action="append")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        data = build(args)
    except ValueError as exc:
        parser.error(str(exc))
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n" if args.format == "json" else markdown(data)
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
