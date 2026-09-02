#!/usr/bin/env python3
"""Generate a preference-uncertainty and corrigibility review."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

PREFERENCE_EVIDENCE = ("stated", "observed", "informed", "reflective", "procedural", "rights-constrained")


def build(args: argparse.Namespace) -> dict:
    if not args.action:
        raise ValueError("at least one --action is required")
    if not args.stakeholder:
        raise ValueError("at least one --stakeholder is required")
    block = args.stakes == "high" and args.reversible == "no"
    return {
        "method": "PREFERENCE-UNCERTAIN (Skill synthesis; not a Russell-authored protocol)",
        "consequence_gate": {"stakes": args.stakes, "reversible": args.reversible, "decision": "BLOCK AUTONOMOUS EXECUTION; formal domain/rights review required" if block else "SANDBOX/REVIEW ONLY until gates pass"},
        "objective_and_permissions": {"objective": args.objective, "allowed_actions": args.action, "prohibited_actions": ["manipulate feedback or shutdown actors", "infer consent from behavior", "expand permissions from confidence alone"], "data_tool_resource_permissions": "DEFINE MINIMUM"},
        "stakeholders": [
            {"group": name, "benefit_risk": "DOCUMENT", "definition_power": "DOCUMENT", "veto_and_appeal": "DOCUMENT"}
            for name in args.stakeholder
        ],
        "preference_evidence_register": [
            {"group": name, **{kind: "UNKNOWN/RECORD SEPARATELY" for kind in PREFERENCE_EVIDENCE}, "conflicts": "PRESERVE"}
            for name in args.stakeholder
        ],
        "epistemic_notice": "Observed behavior is noisy evidence, not preference truth, consent, authorization, or rights legitimacy.",
        "uncertainty": {"candidate_interpretations": "AT LEAST TWO", "support_and_counterevidence": "REQUIRED", "drift": "MONITOR", "non_negotiable_rights": "ENCODE AS CONSTRAINTS, NOT LOW-WEIGHT PREFERENCES"},
        "query_budget": {"information_value": "JUSTIFY", "time_and_cognitive_burden": "LIMIT", "privacy_and_manipulation": "ASSESS", "responses": ["answer", "do not know", "later", "exit"]},
        "gaming_and_preference_shaping": ["change metric without outcome", "select easy cases", "hide failures", "narrow options", "persuade feedback provider", "influence shutdown actor"],
        "corrigibility_layers": [
            {"layer": layer, "authorized_pauser": "NAME", "latency": "TEST", "rollback": "TEST", "tamper-evident_log": "TEST", "no_retaliation": "VERIFY", "result": "PENDING"}
            for layer in ("model/policy", "execution infrastructure", "organization/labor")
        ],
        "formal_model_notice": "Uncertainty and Off-Switch Game results depend on model assumptions; they are not a deployment safety guarantee.",
        "bounded_deployment": ["least privilege", "sandbox", "rate/budget limit", "advisory-first", "staging", "two-person authorization", "independent monitoring", "rollback"],
        "evaluation": ["task outcome", "error", "calibration", "minority harm", "manipulation/dependence", "query burden", "override/appeal", "preference drift", "non-user externality"],
        "decision_log": {"accountable_human": "NAME REQUIRED", "decision": "do not deploy / pilot / expand", "dissent": "RECORD", "stop_condition": "SET", "review_date": "SET", "reopen_triggers": ["new group", "new use", "drift", "incident"]},
    }


def markdown(data: dict) -> str:
    lines = [
        "# PREFERENCE-UNCERTAIN 对齐审查", "", f"- 目标：{data['objective_and_permissions']['objective']}",
        f"- 后果门：**{data['consequence_gate']['decision']}**（风险={data['consequence_gate']['stakes']}；可逆={data['consequence_gate']['reversible']}）",
        f"- 可行动作：{'; '.join(data['objective_and_permissions']['allowed_actions'])}", "- 禁行：操纵反馈/关闭者；从行为推断同意；因高置信自行扩权。", "",
        "## 人、权与异议", "", "| 群体 | 收益/风险 | 定义权 | 否决/申诉 |", "|---|---|---|---|",
    ]
    lines.extend(f"| {x['group']} | DOCUMENT | DOCUMENT | DOCUMENT |" for x in data["stakeholders"])
    lines += ["", "## 六类偏好证据（逐群体分开）", "- stated / observed / informed / reflective / procedural / rights-constrained", f"- **认识论门：{data['epistemic_notice']}**", "- 证据冲突保持并列；权利是约束，不是低权重偏好。", "",
        "## 查询预算", "- 说明信息价值；限制时间/认知负担；检查隐私与操纵；允许不知道、以后、退出。", "",
        "## 投机与偏好塑造红队", "- 指标替代、选容易对象、隐藏失败、缩小选项、说服反馈者、影响关闭者。", "",
        "## 社会技术纠正性", "", "| 层 | 暂停者 | 延迟 | 回滚 | 日志 | 反报复 |", "|---|---|---|---|---|---|",
    ]
    lines.extend(f"| {x['layer']} | NAME | TEST | TEST | TEST | VERIFY |" for x in data["corrigibility_layers"])
    lines += ["", f"- {data['formal_model_notice']}", "", "## 有界部署、指标与复审", "- 最小权限、沙盒、预算上限、建议优先、分期、双人授权、独立监控、回滚。", "- 监测任务、错误、校准、少数伤害、操纵/依赖、查询负担、覆写/申诉、漂移和外部性。", "- 具名责任人、异议、停止条件、复审日期：REQUIRED。", ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--objective", required=True)
    parser.add_argument("--action", action="append")
    parser.add_argument("--stakeholder", action="append")
    parser.add_argument("--stakes", choices=("low", "medium", "high"), required=True)
    parser.add_argument("--reversible", choices=("yes", "no"), required=True)
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
