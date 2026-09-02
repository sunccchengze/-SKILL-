#!/usr/bin/env python3
"""Create an auditable human–AI collaboration plan."""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

LEVELS = {"low", "medium", "high"}
YES_NO = {"yes", "no"}
PRIVACY = {"public", "internal", "confidential", "restricted"}


def parse_subtask(raw: str) -> dict[str, str]:
    parts = [x.strip() for x in raw.split("|")]
    if len(parts) != 5:
        raise ValueError("--subtask must be NAME|IMPORTANCE|VERIFIABILITY|LEARNING_CRITICAL yes/no|PRIVACY")
    name, importance, verifiability, learning, privacy = parts
    if importance not in LEVELS or verifiability not in LEVELS:
        raise ValueError("importance and verifiability must be low, medium, or high")
    if learning not in YES_NO:
        raise ValueError("learning-critical must be yes or no")
    if privacy not in PRIVACY:
        raise ValueError("privacy must be public, internal, confidential, or restricted")
    return {"name": name, "importance": importance, "verifiability": verifiability, "learning_critical": learning, "privacy": privacy}


def route(item: dict[str, str], stakes: str) -> tuple[str, str]:
    if item["privacy"] in {"confidential", "restricted"}:
        return "just-me/expert-governed", "sensitive data; use only an approved controlled tool if policy permits"
    if stakes == "high" or (item["importance"] == "high" and item["verifiability"] == "low"):
        return "just-me/expert-governed", "high consequence or weak verifiability requires accountable expert control"
    if item["learning_critical"] == "yes":
        return "human-first learning", "preserve unaided attempt, then hints, retrieval, and an AI-off transfer check"
    if item["verifiability"] == "high" and item["importance"] == "low":
        return "AI-first delegation", "low consequence and cheap independent verification"
    if item["verifiability"] == "high":
        return "centaur", "clear handoff and independent acceptance test"
    return "cyborg", "low/medium-risk exploration benefits from iterative exchange; retain decision log"


def build(args: argparse.Namespace) -> dict:
    if not args.stakeholder:
        raise ValueError("at least one --stakeholder is required")
    if not args.subtask:
        raise ValueError("at least one --subtask is required")
    subtasks = []
    for raw in args.subtask:
        item = parse_subtask(raw)
        item["mode"], item["reason"] = route(item, args.stakes)
        item["human_accountability"] = "REQUIRED"
        item["verification"] = "REQUIRED before acceptance"
        subtasks.append(item)
    learning_required = args.goal in {"learning", "both"} or any(x["learning_critical"] == "yes" for x in subtasks)
    return {
        "method": "CO-LAB (Skill synthesis; not a Mollick-authored protocol)",
        "task": args.task,
        "goal": args.goal,
        "stakes": args.stakes,
        "stakeholders": args.stakeholder,
        "compliance_gate": {"data_policy": "VERIFY", "copyright_and_disclosure": "VERIFY", "stop_if": "unapproved data, unverifiable high-impact output, or missing accountable reviewer"},
        "human_baseline": {"unaided_attempt": "REQUIRED before AI", "quality_time_confidence": "RECORD"},
        "subtasks": subtasks,
        "model_log": {"date": args.date, "model_version_interface": args.model or "TO RECORD", "prompt_and_output_paths": "TO RECORD"},
        "ontology_notice": "AI 角色标签只是互动脚手架，不是真实人格，也不证明理解、资质或责任（interaction scaffolds, not evidence of personhood）。",
        "verification": ["open primary sources", "run independent tests or examples", "record corrections and reviewer", "model confidence is not verification"],
        "learning_check": {
            "required": learning_required,
            "sequence": "unaided attempt -> bounded hints -> retrieval/explanation -> AI-off transfer task -> delayed retest" if learning_required else "not required unless goal changes",
        },
        "dual_ledger": {"output_quality": "RECORD", "total_time_including_verification": "RECORD", "errors_and_omissions": "RECORD", "unaided_performance": "RECORD if learning", "distributional_costs": "RECORD"},
        "capability_ledger_scope": f"valid only for model/interface={args.model or 'TO RECORD'}, date={args.date}, and these exact subtasks",
        "decision": {"accountable_human": "NAME REQUIRED", "disclosure": "REQUIRED per context", "expand_modify_stop": "DECIDE after comparison with baseline"},
    }


def markdown(data: dict) -> str:
    lines = [
        "# CO-LAB 人机协作计划", "", f"- 任务：{data['task']}", f"- 目标：{data['goal']}", f"- 风险：{data['stakes']}",
        f"- 利益相关者：{', '.join(data['stakeholders'])}", "- 合规门：核验数据政策、版权与披露；缺责任人或高影响输出不可验证则停止。", "",
        "## 人类基线", "- AI 前无辅助尝试：REQUIRED", "- 基线质量、时间、信心：RECORD", "", "## 子任务路由", "",
        "| 子任务 | 重要性 | 可验证性 | 隐私 | 学习关键 | 模式 | 理由 |", "|---|---|---|---|---|---|---|",
    ]
    for item in data["subtasks"]:
        lines.append(f"| {item['name']} | {item['importance']} | {item['verifiability']} | {item['privacy']} | {item['learning_critical']} | {item['mode']} | {item['reason']} |")
    lines += [
        "", "## 模型与认识论声明", f"- 模型/日期：{data['model_log']['model_version_interface']} / {data['model_log']['date']}", f"- {data['ontology_notice']}",
        "", "## 验证", "- 打开原始来源；运行独立样例/测试；记录修正和具名验证人。", "- 模型自报置信度不是验证。",
        "", "## 学习保护", f"- 是否需要：{data['learning_check']['required']}", f"- 流程：{data['learning_check']['sequence']}",
        "", "## 双账本、责任与披露", "- 记录质量、含验证的总时间、错误/遗漏、撤 AI 表现和分配成本。", f"- 能力记录范围：{data['capability_ledger_scope']}", "- 具名责任人：NAME REQUIRED；扩展/修改/停止：比较基线后决定。", "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", required=True)
    parser.add_argument("--goal", choices=("performance", "learning", "both"), required=True)
    parser.add_argument("--stakes", choices=("low", "medium", "high"), required=True)
    parser.add_argument("--stakeholder", action="append")
    parser.add_argument("--subtask", action="append")
    parser.add_argument("--model")
    parser.add_argument("--date", default=date.today().isoformat())
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
