#!/usr/bin/env python3
"""Generate an AGENCY-MIRROR audit that preserves human authorship and contestability."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def build(args: argparse.Namespace) -> dict:
    if not args.affected:
        raise ValueError("at least one --affected group is required")
    block = args.stakes == "high" and args.irreversible == "yes"
    return {
        "method": "AGENCY-MIRROR (Skill synthesis; not a Vallor-authored protocol)",
        "decision": args.decision,
        "stakes": args.stakes,
        "irreversible": args.irreversible,
        "affected_groups": args.affected,
        "ai_role": args.ai_role,
        "rights_gate": {
            "status": "DO NOT AUTOMATE; require formal rights/domain review" if block else "REVIEW REQUIRED",
            "accountable_human": "NAME REQUIRED",
            "pause_and_prohibition_conditions": "REQUIRED",
        },
        "human_authored_purpose": {"desired_future": "WRITE BEFORE QUERYING AI", "non_tradeable_values": ["TO DEFINE"], "whose_success": args.affected},
        "mirror_inspection": {"training_or_input_period": "UNKNOWN/VERIFY", "represented_groups": "UNKNOWN/VERIFY", "omitted_groups_and_futures": ["REQUIRED"], "proxy_and_default_risks": ["REQUIRED"]},
        "claim_types": [
            {"type": kind, "claim": "TO CLASSIFY", "source_or_human_author": "REQUIRED"}
            for kind in ("observation", "prediction", "causal claim", "value judgment", "institutional constraint", "decision")
        ],
        "non_delegable_core": ["purpose", "rights trade-offs", "who bears risk", "final authorization", "appeal adjudication", "accountability"],
        "counterfutures": [
            {"path": "AI-assisted", "description": "TO DESIGN"},
            {"path": "affected-group-authored", "description": "REQUIRED"},
            {"path": "no-AI/low-tech", "description": "REQUIRED"},
            {"path": "not represented by historical default", "description": "REQUIRED"},
        ],
        "judgment_rehearsal": {"conflicting_values": "REQUIRED", "least_heard_group": "REQUIRED", "unaided_variant": "REQUIRED", "responsibility_statement": "REQUIRED"},
        "contestability": {"notice": "REQUIRED", "understandable_reason": "REQUIRED", "challenge_data_and_goal": "REQUIRED", "human_review": "REQUIRED", "exit_or_alternative": "REQUIRED", "no_retaliation": "REQUIRED", "accessibility_test": "language, time, cost, disability, and power"},
        "design_comparison": ["no use", "advisory only", "overridable", "two-person review", "sandbox", "automatic execution"],
        "evaluation": ["value alignment", "error", "reversibility", "human capability", "distribution", "fairness", "exit", "total cost"],
        "authorship_log": {"purpose_author": "NAME REQUIRED", "dissenters": "RECORD", "final_decider": "NAME REQUIRED", "AI contribution": args.ai_role, "review_date": "SET", "withdrawal_trigger": "SET"},
        "epistemic_notice": "The mirror is a philosophical diagnostic, not a complete technical model or causal estimate. Human judgment is not automatically wise or fair.",
    }


def markdown(data: dict) -> str:
    gate = data["rights_gate"]
    lines = [
        "# AGENCY-MIRROR 能动性审计", "", f"- 决定：{data['decision']}", f"- 风险/不可逆：{data['stakes']} / {data['irreversible']}",
        f"- 受影响群体：{', '.join(data['affected_groups'])}", f"- AI 作用：{data['ai_role']}", f"- 权利门：**{gate['status']}**；具名责任人：NAME REQUIRED", "",
        "## 人写目的（查询 AI 前）", "- 希望共同创造的未来：WRITE BEFORE QUERYING AI", "- 不可交换底线：TO DEFINE", "- 成功由受影响群体共同定义。", "",
        "## 检查历史镜面", "- 训练/输入时段与代表群体：UNKNOWN/VERIFY", "- 被遗漏、被平均和历史中尚未充分表示的未来：REQUIRED", "- 镜子是哲学诊断隐喻，不是完整技术模型或因果效应。", "",
        "## 分开 is 与 ought", "- 将声明逐项标为：观察 / 预测 / 因果 / 价值判断 / 制度约束 / 决定。", "- 事实需来源；价值与决定需人署名。", "",
        "## 不可委托核心", "- " + "；".join(data["non_delegable_core"]), "- AI 的拟人流畅不证明理解、人格、资质或责任。", "",
        "## 反事实未来", "- AI 辅助路径：TO DESIGN", "- 受影响者提出路径：REQUIRED", "- 无 AI/低技术路径：REQUIRED", "- 不从历史默认直接延伸的新可能性：REQUIRED", "",
        "## 实践判断练习", "- 冲突价值、最少被听见者、无 AI 变式和责任声明：REQUIRED", "- 人类判断也不天然智慧或公平，需证据、质询与程序。", "",
        "## 可争议性与真实选项", "- 通知、可理解理由、质疑数据/目标、人工复审、退出/替代、不报复：REQUIRED", "- 用语言、时间、成本、残障与权力测试这些选项是否真实。", "",
        "## 作者性与复审", "- 目的作者、异议者、最终决定者：NAME/RECORD REQUIRED", "- 复审日期与撤回触发器：SET", "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--decision", required=True)
    parser.add_argument("--stakes", choices=("low", "medium", "high"), required=True)
    parser.add_argument("--affected", action="append")
    parser.add_argument("--irreversible", choices=("yes", "no"), required=True)
    parser.add_argument("--ai-role", required=True)
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
