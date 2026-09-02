#!/usr/bin/env python3
"""Generate a deterministic, provenance-aware HUMAN automation audit."""

from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path
from typing import Any, Iterable

SCHEMA_VERSION = "1.0"
GENERATOR = "book-human-use-cybernetics/audit_automation.py"
PACKAGE_PROVENANCE = [
    {
        "claim_ids": ["H001", "H002", "H003", "H004", "H005"],
        "layer": "A",
        "source_ids": ["HU-01", "HU-02", "HU-03", "HU-04"],
        "use": "Wiener's feedback, communication, automation, and human-purpose framing",
    },
    {
        "claim_ids": ["H006", "H007", "H008"],
        "layer": "C",
        "source_ids": ["HU-05", "HU-06", "HU-07", "HU-08"],
        "use": "modern ethics, reduction critique, and governance translation",
    },
    {
        "claim_ids": ["H009", "H010", "H011", "H012"],
        "layer": "D",
        "source_ids": ["D1"],
        "use": "HUMAN workflow, proxy checks, meaningful review, and exit contract",
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
    return html.escape(str(value), quote=False).replace("\\", "\\\\").replace("|", "\\|")


def build_audit(args: argparse.Namespace) -> dict[str, Any]:
    system = _clean(args.system, "system")
    purpose = _clean(args.purpose, "purpose")
    metrics = _clean_many(args.metric, "metric", minimum=1, maximum=8)
    affected = _clean_many(args.affected, "affected", minimum=1, maximum=12)
    decisions = _clean_many(args.decision, "decision", minimum=1, maximum=8)
    harms = _clean_many(args.harm, "harm", minimum=1, maximum=12)
    accountable_owner = _optional(args.accountable_owner, "accountable-owner")
    applicable_rule = _optional(args.applicable_rule, "applicable-rule")
    appeal_path = _optional(args.appeal_path, "appeal-path")
    rollback_trigger = _optional(args.rollback_trigger, "rollback-trigger")
    source_locator = _clean(args.source_locator, "source-locator")

    if args.risk_level == "high":
        required = {
            "--accountable-owner": accountable_owner,
            "--applicable-rule": applicable_rule,
            "--appeal-path": appeal_path,
            "--rollback-trigger": rollback_trigger,
        }
        missing = [flag for flag, value in required.items() if value is None]
        if missing:
            raise ValueError(
                "high-risk audit requires " + ", ".join(missing)
            )

    gate_status = (
        "governance_review_required"
        if args.risk_level == "high"
        else "incomplete_until_human_review_contract_is_verified"
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "generator": GENERATOR,
        "workflow": {
            "name": "HUMAN",
            "steps": [
                "Human ends",
                "Understand system",
                "Map feedback",
                "Assign agency",
                "Negotiate test and exit",
            ],
            "created_by_skill": True,
            "claim_id": "H009",
        },
        "input": {
            "system": system,
            "purpose": purpose,
            "metrics": metrics,
            "affected_groups": affected,
            "decisions": decisions,
            "harms": harms,
        },
        "epistemic_contract": {
            "status": "governance_worksheet_not_deployment_approval",
            "claim_layers": {
                "A": "The Human Use of Human Beings",
                "B": "other Wiener works / adjacent author material",
                "C": "later scholarship and modern governance",
                "D": "Skill-created operational synthesis",
            },
            "prohibited_inferences": [
                "Feedback does not prove that a system serves legitimate human ends.",
                "A human-in-the-loop label does not establish meaningful authority or review quality.",
                "A classic text cannot establish present system performance, legality, or safety.",
            ],
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
            "status": gate_status,
            "accountable_owner": accountable_owner or "TODO before pilot",
            "applicable_rule": applicable_rule or "TODO before pilot",
            "appeal_path": appeal_path or "TODO before pilot",
            "rollback_trigger": rollback_trigger or "TODO before pilot",
            "rule": "High-stakes health, legal, credit, employment, education, safety, or rights decisions require domain experts and applicable-law review.",
            "not_a_go_decision": True,
        },
        "audit": {
            "human_ends": {
                "intended_human_outcome": purpose,
                "affected_groups": affected,
                "non_sacrifice_boundaries": [f"Prevent or bound: {harm}" for harm in harms],
                "who_defined_purpose": "TODO",
                "who_can_refuse": "TODO",
            },
            "system_boundary": {
                "automated_decisions": decisions,
                "data_inputs": [],
                "model_or_rules": "TODO",
                "downstream_human_actions": [],
                "externalities": [],
                "vendors_and_dependencies": [],
            },
            "feedback": {
                "proxies": [
                    {
                        "proxy": metric,
                        "human_outcome": purpose,
                        "gaming_path": "TODO",
                        "missing_group_or_signal": "TODO",
                        "guardrail": "TODO",
                    }
                    for metric in metrics
                ],
                "observed_real_world_outcome": "TODO",
                "signal_delay": "TODO",
                "noise_and_missingness": "TODO",
                "who_can_change_goal_or_rule": "TODO",
            },
            "agency": {
                "automation_scope": decisions,
                "reviewer_can_see_original_facts": False,
                "reviewer_can_see_basis_and_uncertainty": False,
                "reviewer_has_time_and_training": False,
                "reviewer_can_override_without_penalty": False,
                "override_is_logged_and_learned_from": False,
                "affected_person_can_reach_review": False,
                "final_accountability": accountable_owner or "TODO",
            },
            "test_and_exit": {
                "pilot_scope": "TODO: limited population, function, and duration",
                "baseline": "TODO",
                "direct_human_outcome": purpose,
                "harm_metrics": harms,
                "disaggregated_results": affected,
                "pass_threshold": "TODO before pilot",
                "pause_threshold": "TODO before pilot",
                "rollback_trigger": rollback_trigger or "TODO before pilot",
                "appeal_path": appeal_path or "TODO before pilot",
                "decision_log": [],
            },
            "labor_and_distribution": {
                "removed_tasks": [],
                "new_exception_or_emotional_labor": [],
                "skill_and_autonomy_effects": "TODO",
                "benefit_recipients": [],
                "risk_bearers": affected,
                "worker_participation": "TODO",
            },
        },
    }


def to_markdown(data: dict[str, Any]) -> str:
    inputs = data["input"]
    safety = data["safety_gate"]
    lines = [
        "# HUMAN 人本自动化审计",
        "",
        f"- Schema：`{_md(data['schema_version'])}`",
        f"- 系统：{_md(inputs['system'])}",
        f"- 人本目的：{_md(inputs['purpose'])}",
        f"- 风险门：`{_md(safety['risk_level'])}` / `{_md(safety['status'])}`",
        f"- 声明来源层 / 定位：`{_md(data['source_context']['declared_layer'])}` / {_md(data['source_context']['locator'])}",
        "",
        "> **非批准声明**：此输出是待核验治理工作表，不证明系统合法、安全、公平、有效，也不批准部署。",
        "",
        "## H — Human ends",
        "",
        f"- 目的：{_md(inputs['purpose'])}",
        f"- 受影响群体：{_md('；'.join(inputs['affected_groups']))}",
        f"- 不可牺牲边界：{_md('；'.join(inputs['harms']))}",
        "- 谁定义目的 / 谁能拒绝：TODO / TODO",
        "",
        "## U — Understand the system",
        "",
        f"- 自动化决定：{_md('；'.join(inputs['decisions']))}",
        "- 输入 → 模型/规则 → 输出 → 人类动作 → 现实后果：TODO",
        "- 供应商、依赖和外部性：TODO",
        "",
        "## M — Map feedback and proxies",
        "",
        "| 代理指标 | 真正的人类结果 | 游戏化路径 | 漏项/群体 | 护栏 |",
        "|---|---|---|---|---|",
    ]
    for metric in inputs["metrics"]:
        lines.append(
            f"| {_md(metric)} | {_md(inputs['purpose'])} | TODO | TODO | TODO |"
        )
    lines.extend(
        [
            "",
            "- 结果信号 / 时滞 / 噪声 / 修正规则权限：TODO / TODO / TODO / TODO",
            "",
            "## A — Assign agency",
            "",
            f"- 最终责任：{_md(safety['accountable_owner'])}",
            "- [ ] 复核者可见原始事实、依据与不确定性",
            "- [ ] 复核者有时间、训练、覆盖权且不会因覆盖受惩罚",
            "- [ ] 覆盖被记录并进入规则改进",
            f"- [ ] 受影响者可到达申诉路径：{_md(safety['appeal_path'])}",
            "",
            "## N — Negotiate test and exit",
            "",
            f"- 适用规则：{_md(safety['applicable_rule'])}",
            "- 基线 / 范围 / 周期：TODO / TODO / TODO",
            f"- 伤害指标：{_md('；'.join(inputs['harms']))}",
            "- 分群结果：TODO",
            f"- 回滚触发：{_md(safety['rollback_trigger'])}",
            "- 通过 / 暂停 / 终止阈值：TODO / TODO / TODO",
            "",
            "## 劳动与分配",
            "",
            "| 被移除任务 | 新增异常/情绪劳动 | 技能/自主性 | 收益方 | 风险承担者 |",
            "|---|---|---|---|---|",
            f"| TODO | TODO | TODO | TODO | {_md('；'.join(inputs['affected_groups']))} |",
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
            "## 决策日志",
            "",
            "| 日期 | 证据变化 | 申诉/事件 | 决定 | 责任人 |",
            "|---|---|---|---|---|",
            "| TODO | TODO | TODO | TODO | TODO |",
        ]
    )
    return "\n".join(lines) + "\n"


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a bounded, provenance-aware HUMAN automation audit."
    )
    parser.add_argument("--system", required=True)
    parser.add_argument("--purpose", required=True)
    parser.add_argument("--metric", action="append", required=True)
    parser.add_argument("--affected", action="append", required=True)
    parser.add_argument("--decision", action="append", required=True)
    parser.add_argument("--harm", action="append", required=True)
    parser.add_argument("--risk-level", choices=["low", "moderate", "high"], default="moderate")
    parser.add_argument("--accountable-owner")
    parser.add_argument("--applicable-rule")
    parser.add_argument("--appeal-path")
    parser.add_argument("--rollback-trigger")
    parser.add_argument("--source-layer", choices=["A", "B", "C", "D"], default="D")
    parser.add_argument(
        "--source-locator",
        default="references/claim-layer-map.md#H009-H012",
    )
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    parser.add_argument("--output")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = make_parser()
    args = parser.parse_args(argv)
    try:
        data = build_audit(args)
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
