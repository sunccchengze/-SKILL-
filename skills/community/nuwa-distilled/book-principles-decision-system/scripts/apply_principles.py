#!/usr/bin/env python3
"""Generate a deterministic, provenance-aware BRIDGE decision record.

The helper operationalizes a bounded reading of Ray Dalio's *Principles*.
It structures user-supplied material; it does not verify that material, score
people, make employment decisions, or authorize real-world deployment.
"""

from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path
from typing import Any, Iterable

SCHEMA_VERSION = "1.0"
GENERATOR = "book-principles-decision-system/apply_principles.py"
SENSITIVE_DOMAINS = {
    "personnel",
    "labor",
    "healthcare",
    "education",
    "credit",
    "law-enforcement",
    "content-governance",
}
PACKAGE_PROVENANCE = [
    {
        "claim_ids": ["P002", "P003", "P005", "P007", "P008", "P009", "P010", "P012", "P013", "P014", "P015"],
        "layer": "A",
        "source_ids": ["PD-01", "PD-02", "PD-03", "PD-04", "PD-05", "PD-06", "PD-07"],
        "use": "the 2017 book's principles, five-step loop, disagreement, responsibility, and systemization",
    },
    {
        "claim_ids": ["P018", "P019"],
        "layer": "B",
        "source_ids": ["PD-09", "PD-10"],
        "use": "edition lineage and Bridgewater's later, explicitly evolved culture statement",
    },
    {
        "claim_ids": ["P020", "P021", "P022", "P023", "P024", "P025", "P026", "P027", "P028"],
        "layer": "C",
        "source_ids": ["PD-11", "PD-12", "PD-13", "PD-14", "PD-15", "PD-16", "PD-17", "PD-18", "PD-19", "PD-20", "PD-21", "PD-22", "PD-23"],
        "use": "independent evidence, governance constraints, and contested implementation reports",
    },
    {
        "claim_ids": ["P029", "P030", "P031", "P032", "P033", "P034", "P035", "P036"],
        "layer": "D",
        "source_ids": ["D1"],
        "use": "BRIDGE workflow, principle cards, proportional transparency, and high-risk gates",
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
    """Escape user-controlled text for Markdown tables and inline fields."""
    return html.escape(str(value), quote=False).replace("\\", "\\\\").replace("|", "\\|")


def _effective_risk(declared: str, domain: str) -> tuple[str, str]:
    if domain in SENSITIVE_DOMAINS:
        return "high", "sensitive_domain_default"
    return declared, "declared_risk"


def build_record(args: argparse.Namespace) -> dict[str, Any]:
    decision = _clean(args.decision, "decision")
    goal = _clean(args.goal, "goal")
    realities = _clean_many(args.reality, "reality", minimum=2, maximum=12)
    principles = _clean_many(args.principle, "principle", minimum=1, maximum=8)
    disagreements = _clean_many(args.disagreement, "disagreement", minimum=1, maximum=8)
    evidence = _clean_many(args.evidence, "evidence", minimum=1, maximum=12)
    affected_groups = _clean_many(args.affected_group or [], "affected-group", maximum=12)
    impact_evidence = _clean_many(args.impact_evidence or [], "impact-evidence", maximum=12)
    accountable_owner = _optional(args.accountable_owner, "accountable-owner")
    applicable_rule = _optional(args.applicable_rule, "applicable-rule")
    appeal_path = _optional(args.appeal_path, "appeal-path")
    rollback_trigger = _optional(args.rollback_trigger, "rollback-trigger")
    stop_condition = _optional(args.stop_condition, "stop-condition")
    source_locator = _clean(args.source_locator, "source-locator")
    effective_risk, risk_basis = _effective_risk(args.risk_level, args.domain)

    if effective_risk == "high":
        missing: list[str] = []
        required_values = (
            (accountable_owner, "--accountable-owner"),
            (applicable_rule, "--applicable-rule"),
            (appeal_path, "--appeal-path"),
            (rollback_trigger, "--rollback-trigger"),
            (stop_condition, "--stop-condition"),
        )
        missing.extend(flag for value, flag in required_values if value is None)
        if not affected_groups:
            missing.append("--affected-group")
        if not impact_evidence:
            missing.append("--impact-evidence")
        if missing:
            raise ValueError("high-risk decision record requires " + ", ".join(missing))

    safety_status = (
        "governance_review_required"
        if effective_risk == "high"
        else "bounded_decision_design"
    )

    principle_cards = [
        {
            "candidate_principle": principle,
            "status": "hypothesis_to_test",
            "trigger": "TODO: recurring situation and boundary",
            "action": "TODO: behavior or decision rule",
            "prediction": "TODO before action",
            "exception": "TODO: when this principle should not fire",
            "falsifier": "TODO: outcome that would weaken the rule",
            "version": "0.1-draft",
        }
        for principle in principles
    ]

    return {
        "schema_version": SCHEMA_VERSION,
        "generator": GENERATOR,
        "workflow": {
            "name": "BRIDGE",
            "steps": ["Bound", "Record", "Identify", "Disagree", "Govern", "Evaluate"],
            "created_by_skill": True,
            "claim_id": "P029",
        },
        "input": {
            "decision_question": decision,
            "goal": goal,
            "realities": realities,
            "candidate_principles": principles,
            "disagreements": disagreements,
            "evidence": evidence,
            "affected_groups": affected_groups,
        },
        "epistemic_contract": {
            "status": "decision_record_not_decision_truth_or_deployment_approval",
            "input_treatment": "user_supplied_claims_not_independently_verified",
            "claim_layers": {
                "A": "2017 Principles: Life and Work",
                "B": "Dalio's other versions or later Bridgewater materials",
                "C": "independent research, reporting, and governance sources",
                "D": "Skill-created operational synthesis",
            },
            "prohibited_inference": (
                "A written principle, high-status opinion, weighted vote, personality label, "
                "or algorithmic score does not establish truth, fairness, causal impact, or authorization."
            ),
        },
        "source_context": {
            "declared_layer": args.source_layer,
            "locator": source_locator,
            "package_claim_map": "references/claim-layer-map.md",
            "package_source_notes": "references/source-notes.md",
        },
        "provenance": PACKAGE_PROVENANCE,
        "safety_gate": {
            "domain": args.domain,
            "declared_risk": args.risk_level,
            "effective_risk": effective_risk,
            "risk_basis": risk_basis,
            "status": safety_status,
            "accountable_owner": accountable_owner or "TODO before consequential action",
            "applicable_rule": applicable_rule or "TODO before consequential action",
            "affected_groups": affected_groups,
            "impact_evidence_submitted": impact_evidence,
            "impact_evidence_status": "submitted_not_verified" if impact_evidence else "not_supplied",
            "appeal_path": appeal_path or "TODO before consequential action",
            "rollback_trigger": rollback_trigger or "TODO before consequential action",
            "stop_condition": stop_condition or "TODO before consequential action",
            "non_approval": "Passing this generation gate is not legal, ethical, personnel, clinical, credit, or deployment approval.",
        },
        "decision_governance": {
            "mode": args.decision_mode,
            "final_decision": "TODO by the authorized and accountable process",
            "book_boundary": "Believability weighting can challenge a Responsible Party; it does not replace responsibility.",
            "person_rating_policy": (
                "Do not create a global worth, personality, or believability score. Any reliability claim must be "
                "task-specific, dated, based on comparable outcomes, uncertainty-aware, and contestable."
            ),
            "transparency_policy": (
                "Expose decision logic and material evidence proportionately; protect personal, privileged, "
                "security-sensitive, safeguarding, and legally restricted information."
            ),
        },
        "worksheets": {
            "bound": {
                "goal": goal,
                "decision_rights": "TODO: who advises, consents, decides, implements, and can halt",
                "rights_and_duties": [applicable_rule] if applicable_rule else [],
                "affected_groups": affected_groups,
                "out_of_scope": [],
            },
            "record": {
                "observations_or_claimed_realities": realities,
                "evidence_inventory": evidence,
                "interpretations": ["TODO: keep separate from observations"],
                "unknowns": ["TODO: what would materially change the choice"],
                "source_quality_review": "TODO: direct / external / inference, date, version, limitations",
            },
            "identify": {
                "decision_question": decision,
                "book_five_step_crosswalk": {
                    "goal": goal,
                    "problem": "TODO: observable gap blocking the goal",
                    "diagnosis": "TODO: competing root-cause hypotheses; do not diagnose a person from a label",
                    "design": "TODO: bounded plan linked to diagnosis",
                    "tasks": "TODO: owner, date, resources, dependencies",
                },
                "principle_cards": principle_cards,
            },
            "disagree": {
                "recorded_disagreements": disagreements,
                "strongest_alternative": "TODO: steelman a materially different choice",
                "disconfirming_evidence": "TODO",
                "reliability_matrix": [],
                "reliability_contract": [
                    "same decision domain",
                    "comparable and independently checkable outcomes",
                    "enough dated observations to estimate uncertainty",
                    "no circular weighting from prior status or self-confirming ratings",
                    "equal access to appeal and correction",
                ],
                "excluded_or_chilled_voice": "TODO: who may stay silent because of power, retaliation, access, or surveillance",
            },
            "govern": {
                "decision_mode": args.decision_mode,
                "accountable_owner": accountable_owner or "TODO",
                "applicable_rule": applicable_rule or "TODO",
                "decision_rationale": "TODO: include rejected alternatives and residual uncertainty",
                "appeal_path": appeal_path or "TODO",
                "rollback_trigger": rollback_trigger or "TODO",
                "stop_condition": stop_condition or "TODO",
                "privacy_zone": "TODO: what must not be exposed and why",
            },
            "evaluate": {
                "pre_action_prediction": "TODO before action",
                "baseline": "TODO",
                "decision_quality_metric": "TODO: process quality separate from lucky outcome",
                "outcome_and_harm_metrics": [],
                "review_date": "TODO",
                "principle_update_log": [],
                "choices": ["retain", "narrow", "revise", "retire"],
            },
        },
    }


def to_markdown(data: dict[str, Any]) -> str:
    inputs = data["input"]
    safety = data["safety_gate"]
    governance = data["decision_governance"]
    worksheets = data["worksheets"]
    lines = [
        "# BRIDGE 原则决策记录",
        "",
        f"- Schema：`{_md(data['schema_version'])}`",
        f"- 决策问题：{_md(inputs['decision_question'])}",
        f"- 目标：{_md(inputs['goal'])}",
        f"- 领域：`{_md(safety['domain'])}`",
        f"- 风险门：`{_md(safety['declared_risk'])}` → `{_md(safety['effective_risk'])}` / `{_md(safety['status'])}`",
        f"- 决策模式：`{_md(governance['mode'])}`",
        f"- 声明来源层：`{_md(data['source_context']['declared_layer'])}`",
        f"- 来源定位：{_md(data['source_context']['locator'])}",
        "",
        "> **认识论合同**：这是决策记录，不是真理证明、人员评分、因果证明或部署批准。输入被当作待核材料，而非已验证事实。",
        "",
        "## B — Bound｜目标、权利与边界",
        "",
        f"- Accountable owner：{_md(safety['accountable_owner'])}",
        f"- Applicable rule：{_md(safety['applicable_rule'])}",
        f"- 受影响群体：{_md('；'.join(inputs['affected_groups']) or 'TODO')}",
        f"- 真实影响证据（提交值）：{_md('；'.join(safety['impact_evidence_submitted']) or 'TODO')}",
        f"- 影响证据状态：`{_md(safety['impact_evidence_status'])}`（提交不等于核验）",
        f"- 申诉路径：{_md(safety['appeal_path'])}",
        f"- 回滚触发：{_md(safety['rollback_trigger'])}",
        f"- 停止条件：{_md(safety['stop_condition'])}",
        "",
        "## R — Record｜现实、证据、解释与未知",
        "",
        "| 用户提供的现实陈述 | 状态 | 需补定位/版本 |",
        "|---|---|---|",
    ]
    for reality in inputs["realities"]:
        lines.append(f"| {_md(reality)} | 待核 | TODO |")
    lines.extend([
        "",
        f"- 证据库存：{_md('；'.join(inputs['evidence']))}",
        "- 解释：TODO（不得与观察混写）",
        "- 未知：TODO（写会改变决策的未知）",
        "",
        "## I — Identify｜五步交叉检查与原则卡",
        "",
        "| 候选原则 | 触发 | 动作 | 事前预测 | 例外 | 推翻条件 | 版本 |",
        "|---|---|---|---|---|---|---|",
    ])
    for card in worksheets["identify"]["principle_cards"]:
        lines.append(
            "| {candidate} | {trigger} | {action} | {prediction} | {exception} | {falsifier} | {version} |".format(
                candidate=_md(card["candidate_principle"]),
                trigger=_md(card["trigger"]),
                action=_md(card["action"]),
                prediction=_md(card["prediction"]),
                exception=_md(card["exception"]),
                falsifier=_md(card["falsifier"]),
                version=_md(card["version"]),
            )
        )
    lines.extend([
        "",
        "- 原书五步：目标 → 问题 → 诊断 → 设计 → 执行；每一步必须与下一步分开记录。",
        "- 根因：至少保留两个竞争解释；不得用人格标签替代机制证据。",
        "",
        "## D — Disagree｜异议、三角校验与可信度边界",
        "",
        f"- 已记录异议：{_md('；'.join(inputs['disagreements']))}",
        "- 最强替代方案：TODO",
        "- 反证：TODO",
        "- 被权力、报复风险、访问限制或监控压低的声音：TODO",
        "",
        "| 人/来源 | 具体任务 | 可核结果与日期 | 样本/不确定性 | 利益冲突 | 可申诉修正 |",
        "|---|---|---|---|---|---|",
        "| TODO | TODO | TODO | TODO | TODO | TODO |",
        "",
        "> 禁止全局“可信度/人格/价值”评分；只允许与当前任务相关、可更新、可争议的可靠性记录。",
        "",
        "## G — Govern｜决策权、隐私、申诉与回滚",
        "",
        f"- 模式：{_md(governance['mode'])}",
        "- 最终决定：TODO，由有权且可问责的流程作出",
        f"- 透明边界：{_md(governance['transparency_policy'])}",
        "- 隐私区：TODO（个人、特权、安全、举报、保障或法律受限信息）",
        f"- 非批准声明：{_md(safety['non_approval'])}",
        "",
        "## E — Evaluate｜事前预测、结果与原则演化",
        "",
        "| 事前预测 | 基线 | 结果指标 | 伤害指标 | 复盘日 | 保留/收窄/修订/退役 |",
        "|---|---|---|---|---|---|",
        "| TODO | TODO | TODO | TODO | TODO | TODO |",
        "",
        "## Claim/source provenance",
        "",
        "| 层 | Claim IDs | Source IDs | 用途 |",
        "|---|---|---|---|",
    ])
    for record in data["provenance"]:
        lines.append(
            "| {layer} | {claims} | {sources} | {use} |".format(
                layer=_md(record["layer"]),
                claims=_md(", ".join(record["claim_ids"])),
                sources=_md(", ".join(record["source_ids"])),
                use=_md(record["use"]),
            )
        )
    lines.extend([
        "",
        "## 原则更新日志（不得覆盖旧版本）",
        "",
        "| 日期 | 原版本 | 观察 | 支持/削弱 | 新版本 | 决定人 |",
        "|---|---|---|---|---|---|",
        "| TODO | 0.1-draft | TODO | TODO | TODO | TODO |",
    ])
    return "\n".join(lines) + "\n"


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a bounded, provenance-aware BRIDGE decision record."
    )
    parser.add_argument("--decision", required=True)
    parser.add_argument("--goal", required=True)
    parser.add_argument("--reality", action="append", required=True)
    parser.add_argument("--principle", action="append", required=True)
    parser.add_argument("--disagreement", action="append", required=True)
    parser.add_argument("--evidence", action="append", required=True)
    parser.add_argument(
        "--domain",
        choices=["general", "business-strategy", *sorted(SENSITIVE_DOMAINS)],
        default="general",
    )
    parser.add_argument("--risk-level", choices=["low", "moderate", "high"], default="moderate")
    parser.add_argument(
        "--decision-mode",
        choices=["owner", "advice", "consent", "vote", "algorithm-assisted"],
        default="owner",
    )
    parser.add_argument("--affected-group", action="append")
    parser.add_argument("--accountable-owner")
    parser.add_argument("--applicable-rule")
    parser.add_argument("--impact-evidence", action="append")
    parser.add_argument("--appeal-path")
    parser.add_argument("--rollback-trigger")
    parser.add_argument("--stop-condition")
    parser.add_argument("--source-layer", choices=["A", "B", "C", "D"], default="D")
    parser.add_argument(
        "--source-locator",
        default="references/claim-layer-map.md#P029-P036",
    )
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    parser.add_argument("--output")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = make_parser().parse_args(argv)
    try:
        data = build_record(args)
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
