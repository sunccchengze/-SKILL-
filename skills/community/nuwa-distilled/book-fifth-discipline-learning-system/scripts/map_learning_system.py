#!/usr/bin/env python3
"""Generate a deterministic, provenance-aware LOOPS systems-learning worksheet."""

from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path
from typing import Any, Iterable

SCHEMA_VERSION = "1.0"
GENERATOR = "book-fifth-discipline-learning-system/map_learning_system.py"
PACKAGE_PROVENANCE = [
    {
        "claim_ids": ["F001", "F002", "F003", "F004", "F005"],
        "layer": "A",
        "source_ids": ["FD-01", "FD-02"],
        "use": "five disciplines and Senge's integrative framing",
    },
    {
        "claim_ids": ["F006", "F007", "F008"],
        "layer": "C",
        "source_ids": ["FD-03", "FD-04", "FD-05", "FD-08", "FD-09"],
        "use": "systems-dynamics lineage, diagram syntax, and model boundaries",
    },
    {
        "claim_ids": ["F009", "F010", "F011", "F012"],
        "layer": "D",
        "source_ids": ["D1"],
        "use": "LOOPS workflow, evidence labels, power checks, and reversible probes",
    },
]


def _clean(value: str, field: str) -> str:
    normalized = " ".join(value.split())
    if not normalized:
        raise ValueError(f"{field} must not be blank")
    return normalized


def _clean_many(
    values: Iterable[str], field: str, *, minimum: int = 0, maximum: int = 12
) -> list[str]:
    cleaned = [_clean(value, field) for value in values]
    if len(cleaned) < minimum:
        raise ValueError(f"{field} requires at least {minimum} value(s)")
    if len(cleaned) > maximum:
        raise ValueError(f"{field} accepts at most {maximum} value(s)")
    folded = [value.casefold() for value in cleaned]
    if len(set(folded)) != len(folded):
        raise ValueError(f"{field} must not contain duplicate values")
    return cleaned


def _optional(value: str | None, field: str) -> str | None:
    return _clean(value, field) if value is not None else None


def _md(value: object) -> str:
    """Escape user-controlled text for a Markdown table or inline field."""
    return html.escape(str(value), quote=False).replace("\\", "\\\\").replace("|", "\\|")


def build_map(args: argparse.Namespace) -> dict[str, Any]:
    problem = _clean(args.problem, "problem")
    horizon = _clean(args.horizon, "horizon")
    variables = _clean_many(args.variable, "variable", minimum=2, maximum=8)
    delays = _clean_many(args.delay or [], "delay", maximum=8)
    assumptions = _clean_many(args.assumption, "assumption", minimum=1, maximum=8)
    evidence = _clean_many(args.evidence or [], "evidence", maximum=12)
    stakeholders = _clean_many(args.stakeholder or [], "stakeholder", maximum=12)
    owner = _optional(args.owner, "owner")
    stop_condition = _optional(args.stop_condition, "stop-condition")
    source_locator = _clean(args.source_locator, "source-locator")

    if args.risk_level == "high":
        missing = []
        if owner is None:
            missing.append("--owner")
        if stop_condition is None:
            missing.append("--stop-condition")
        if missing:
            raise ValueError(
                "high-risk mapping requires " + " and ".join(missing)
            )

    safety_status = (
        "analysis_only"
        if args.risk_level == "high"
        else "bounded_probe_design"
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "generator": GENERATOR,
        "workflow": {
            "name": "LOOPS",
            "steps": ["Limit", "Locate", "Observe", "Outline", "Probe", "Select"],
            "created_by_skill": True,
            "claim_id": "F009",
        },
        "input": {
            "problem": problem,
            "horizon": horizon,
            "variables": variables,
            "delays": delays,
            "assumptions": assumptions,
            "evidence": evidence,
            "stakeholders": stakeholders,
        },
        "epistemic_contract": {
            "status": "hypothesis_map_not_causal_proof",
            "claim_layers": {
                "A": "The Fifth Discipline / Senge framing",
                "B": "adjacent Senge material",
                "C": "systems-dynamics and organizational-learning lineage",
                "D": "Skill-created operational synthesis",
            },
            "required_competing_explanations": 1,
            "required_out_of_boundary_variable": 1,
            "prohibited_inference": "A causal-loop arrow, archetype match, or workshop consensus does not establish causality or effect size.",
        },
        "source_context": {
            "declared_layer": args.source_layer,
            "locator": source_locator,
            "package_claim_map": "references/claim-layer-map.md",
            "package_source_notes": "references/source-notes.md",
        },
        "provenance": PACKAGE_PROVENANCE,
        "safety_gate": {
            "risk_level": args.risk_level,
            "status": safety_status,
            "owner": owner or "TODO before intervention",
            "stop_condition": stop_condition or "TODO before intervention",
            "rule": "Urgent safety, legal, safeguarding, or accountability duties precede systems mapping.",
            "non_delegation": "A systems explanation must not erase individual responsibility, rights, or applicable rules.",
        },
        "worksheets": {
            "limit": {
                "immediate_duties_checked": False,
                "analysis_boundary": f"Problem: {problem}; horizon: {horizon}",
                "out_of_scope": [],
            },
            "locate": {
                "repeating_outcome": problem,
                "affected_stakeholders": stakeholders,
                "event_only_explanation_rejected": True,
            },
            "observe": {
                "behavior_over_time": [
                    {
                        "variable": variable,
                        "baseline": "TODO",
                        "past_pattern": "TODO",
                        "current": "TODO",
                        "desired": "TODO",
                        "evidence": "TODO",
                    }
                    for variable in variables
                ],
                "evidence_inventory": evidence,
                "known_delays": delays,
            },
            "outline": {
                "candidate_edges": [],
                "edge_contract": [
                    "from_variable",
                    "polarity",
                    "to_variable",
                    "evidence_or_hypothesis",
                    "delay",
                    "falsifier",
                ],
                "loop_status": "TODO: label reinforcing/balancing only after closing a coherent loop",
            },
            "probe": {
                "candidate_archetype": "TODO",
                "archetype_mismatch": "TODO",
                "assumptions_to_test": assumptions,
                "competing_explanation": "TODO (required)",
                "out_of_boundary_variable": "TODO (required)",
                "power_questions": [
                    "Who defined the problem and desired outcome?",
                    "Whose knowledge can alter the map?",
                    "Who bears experiment costs and can refuse participation?",
                ],
            },
            "select": {
                "intervention": "TODO: one small, reversible structural change",
                "short_term_prediction": "TODO before action",
                "delayed_prediction": "TODO before action",
                "leading_indicator": "TODO",
                "lagging_indicator": "TODO",
                "harm_indicator": "TODO",
                "owner": owner or "TODO",
                "stop_condition": stop_condition or "TODO",
                "update_log": [],
            },
        },
    }


def to_markdown(data: dict[str, Any]) -> str:
    inputs = data["input"]
    safety = data["safety_gate"]
    lines = [
        "# LOOPS 学习系统工作表",
        "",
        f"- Schema：`{_md(data['schema_version'])}`",
        f"- 问题：{_md(inputs['problem'])}",
        f"- 时间范围：{_md(inputs['horizon'])}",
        f"- 风险门：`{_md(safety['risk_level'])}` / `{_md(safety['status'])}`",
        f"- 声明来源层：`{_md(data['source_context']['declared_layer'])}`",
        f"- 来源定位：{_md(data['source_context']['locator'])}",
        "",
        "> **认识论边界**：本工作表生成待反驳的系统假设，不生成因果证明、效应量或部署许可。高风险输出仅供分析。",
        "",
        "## L — Limit",
        "",
        f"- 紧急义务：待检查；规则：{_md(safety['rule'])}",
        f"- 责任 owner：{_md(safety['owner'])}",
        f"- 停止条件：{_md(safety['stop_condition'])}",
        "",
        "## L — Locate",
        "",
        f"- 重复结果：{_md(inputs['problem'])}",
        f"- 受影响者：{_md('；'.join(inputs['stakeholders']) or 'TODO')}",
        "",
        "## O — Observe：行为随时间",
        "",
        "| 变量 | 基线 | 过去模式 | 当前 | 期望 | 证据 |",
        "|---|---|---|---|---|---|",
    ]
    for variable in inputs["variables"]:
        lines.append(f"| {_md(variable)} | TODO | TODO | TODO | TODO | TODO |")
    lines.extend(
        [
            "",
            f"- 已知时滞：{_md('；'.join(inputs['delays']) or 'TODO')}",
            f"- 证据库存：{_md('；'.join(inputs['evidence']) or 'TODO')}",
            "",
            "## O — Outline：回路声明",
            "",
            "| From | 极性 | To | 证据/假设 | 时滞 | 推翻观察 |",
            "|---|---|---|---|---|---|",
            "| TODO | TODO | TODO | TODO | TODO | TODO |",
            "",
            "## P — Probe",
            "",
            f"- 待检验假设：{_md('；'.join(inputs['assumptions']))}",
            "- 候选基模及不匹配点：TODO",
            "- 竞争解释：TODO（必填）",
            "- 图外变量：TODO（必填）",
            "- 权力检查：谁定义问题、谁能改图、谁承担成本、谁能拒绝？",
            "",
            "## S — Select：可逆探针",
            "",
            "- 一个小规模结构改变：TODO",
            "- 事前短期 / 延迟预测：TODO / TODO",
            "- 领先 / 滞后 / 伤害指标：TODO / TODO / TODO",
            f"- owner / 停止条件：{_md(safety['owner'])} / {_md(safety['stop_condition'])}",
            "",
            "## Claim / source provenance",
            "",
            "| 层 | Claim IDs | Source IDs | 用途 |",
            "|---|---|---|---|",
        ]
    )
    for record in data["provenance"]:
        lines.append(
            "| {layer} | {claims} | {sources} | {use} |".format(
                layer=_md(record["layer"]),
                claims=_md(", ".join(record["claim_ids"])),
                sources=_md(", ".join(record["source_ids"])),
                use=_md(record["use"]),
            )
        )
    lines.extend(
        [
            "",
            "## 更新日志（不得覆盖原假设）",
            "",
            "| 日期 | 观察 | 被削弱/增强的箭头 | 决定 |",
            "|---|---|---|---|",
            "| TODO | TODO | TODO | TODO |",
        ]
    )
    return "\n".join(lines) + "\n"


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a bounded, provenance-aware LOOPS worksheet."
    )
    parser.add_argument("--problem", required=True)
    parser.add_argument("--horizon", required=True)
    parser.add_argument("--variable", action="append", required=True)
    parser.add_argument("--delay", action="append")
    parser.add_argument("--assumption", action="append", required=True)
    parser.add_argument("--evidence", action="append")
    parser.add_argument("--stakeholder", action="append")
    parser.add_argument("--risk-level", choices=["low", "moderate", "high"], default="moderate")
    parser.add_argument("--owner")
    parser.add_argument("--stop-condition")
    parser.add_argument("--source-layer", choices=["A", "B", "C", "D"], default="D")
    parser.add_argument(
        "--source-locator",
        default="references/claim-layer-map.md#F009-F012",
    )
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    parser.add_argument("--output")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = make_parser()
    args = parser.parse_args(argv)
    try:
        data = build_map(args)
        text = (
            json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
            if args.format == "json"
            else to_markdown(data)
        )
        if args.output:
            output = Path(args.output)
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(text, encoding="utf-8")
        else:
            sys.stdout.write(text)
        return 0
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
