#!/usr/bin/env python3
"""Deterministically select one next ML/DL learning module."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

DIMENSIONS = ("python", "algebra", "calculus", "probability", "evaluation", "neural_networks")
LABELS = {"python": "Python", "algebra": "线性代数", "calculus": "微积分", "probability": "概率统计", "evaluation": "划分/评估", "neural_networks": "神经网络"}
PATCHES = {
    "python": "写一个只用标准库读取小型 CSV、计算均值并为函数加断言的脚本",
    "algebra": "手算并用标准库核对二维点积、矩阵-向量乘法和形状",
    "calculus": "推导平方损失的一维导数并用有限差分核对",
    "probability": "从硬币样本计算频率、期望和一个 bootstrap 区间",
    "evaluation": "先切 train/validation/test；只用 train 拟合均值并展示全数据拟合的泄漏",
    "neural_networks": "手算单神经元前向、损失与一轮梯度更新",
}
COMMANDS = {
    "zhou-classical-ml-reasoning": "python3 ../zhou-classical-ml-reasoning/scripts/run_micro_experiment.py --exercise split-baseline --output experiment.json",
    "d2l-lab-backbone": "python3 ../d2l-lab-backbone/scripts/new_experiment.py --title 'first D2L lab' --hypothesis 'baseline beats chance' --output experiment.md",
    "goodfellow-deep-learning-theory": "python3 ../goodfellow-deep-learning-theory/scripts/check_derivation.py --exercise finite-difference --output derivation.json",
}


def select(scores: dict[str, int], goal: str) -> tuple[str, str]:
    if scores["evaluation"] < 2 or scores["probability"] < 2:
        return "zhou-classical-ml-reasoning", "先建立问题设定、概率/评估和泄漏纪律"
    if goal == "theory" and min(scores["algebra"], scores["calculus"], scores["probability"]) >= 2:
        return "goodfellow-deep-learning-theory", "理论目标且数学阻塞已达最小门槛"
    if goal == "classical":
        return "zhou-classical-ml-reasoning", "目标是经典机器学习推理"
    if goal == "transformers" and scores["neural_networks"] < 2:
        return "d2l-lab-backbone", "先用可运行实验补神经网络与注意力桥"
    return "d2l-lab-backbone", "以可执行实验建立深度学习主循环"


def build(args: argparse.Namespace) -> dict:
    scores = {name: getattr(args, name) for name in DIMENSIONS}
    module, reason = select(scores, args.goal)
    low = sorted((name for name, score in scores.items() if score < 2), key=lambda name: (scores[name], DIMENSIONS.index(name)))[:3]
    patches = [{"dimension": LABELS[name], "task": PATCHES[name], "timebox_minutes": 60, "pass": "保存可运行产物并能无辅助解释"} for name in low]
    return {
        "method": "ROUTE-ONE (Skill heuristic; not a validated psychometric assessment)",
        "goal": args.goal,
        "diagnostics": {**scores, "compute": args.compute},
        "next_module": module,
        "reason": reason,
        "prerequisite_patches": patches,
        "first_command": COMMANDS[module],
        "artifact_contract": ["hypothesis/prediction", "configuration", "seed", "environment", "metric history", "artifact path", "error analysis", "next experiment"],
        "leakage_invariant": "split first; learn preprocessing/feature selection/tuning inside training folds; touch final test once after selection",
        "exit_ticket": ["explain assumptions", "run from a clean start", "analyze at least three errors", "solve one unaided transfer variant"],
        "scope_notice": "Exactly one next module. Scores are provisional and must be updated from artifacts, not credentials.",
    }


def markdown(data: dict) -> str:
    lines = ["# ROUTE-ONE 下一站", "", f"## 下一模块：`{data['next_module']}`", f"理由：{data['reason']}。", "", "## 七维诊断", "", "| 维度 | 分数/资源 |", "|---|---|" ]
    for key, value in data["diagnostics"].items():
        lines.append(f"| {LABELS.get(key, '算力')} | {value} |")
    lines += ["", "## 阻塞补丁（最多三项）"]
    if data["prerequisite_patches"]:
        lines.extend(f"- {x['dimension']}（{x['timebox_minutes']} 分钟）：{x['task']}；通过={x['pass']}" for x in data["prerequisite_patches"])
    else:
        lines.append("- 无当前阻塞；从模块首个合同开始。")
    lines += ["", "## 首个运行命令", "```bash", data["first_command"], "```", "", "## 产物合同", "- " + "；".join(data["artifact_contract"]), "", "## 泄漏不变量", f"- {data['leakage_invariant']}", "", "## 退出票", *[f"- {x}" for x in data["exit_ticket"]], "", f"> {data['scope_notice']}", ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--goal", choices=("classical", "deep-practice", "theory", "transformers"), required=True)
    for name in DIMENSIONS:
        parser.add_argument("--" + name.replace("_", "-"), type=int, choices=range(4), required=True)
    parser.add_argument("--compute", choices=("unknown", "cpu", "gpu"), required=True)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output")
    args = parser.parse_args()
    data = build(args)
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n" if args.format == "json" else markdown(data)
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
