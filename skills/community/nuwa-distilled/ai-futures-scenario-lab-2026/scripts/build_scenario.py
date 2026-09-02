#!/usr/bin/env python3
"""Build four dated, non-predictive AI scenario cards with strict claim labels."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

LABELS = {"observed-2026", "book-premise", "extrapolation", "scenario-choice", "wildcard"}


def parse_uncertainty(raw: str) -> dict[str, str]:
    parts = [x.strip() for x in raw.split("|")]
    if len(parts) != 3 or not all(parts):
        raise ValueError("--uncertainty must be NAME|LOW_END|HIGH_END")
    return {"name": parts[0], "low": parts[1], "high": parts[2]}


def parse_claim(raw: str) -> dict[str, str]:
    parts = [x.strip() for x in raw.split("|")]
    if len(parts) != 4:
        raise ValueError("--claim must be LABEL|TEXT|SOURCE|DATE")
    label, text, source, publication_date = parts
    if label not in LABELS:
        raise ValueError(f"invalid claim label '{label}'; allowed: {', '.join(sorted(LABELS))}")
    if not text or not source or not publication_date:
        raise ValueError("claim text, source, and date are required")
    if label == "observed-2026" and not publication_date.startswith("2026"):
        raise ValueError("observed-2026 claims require a 2026 source/as-of date")
    if label == "book-premise" and not (publication_date.startswith("2017") or publication_date.startswith("2021")):
        raise ValueError("book-premise must preserve the 2017 or 2021 publication date")
    return {"label": label, "text": text, "source": source, "publication_date": publication_date, "scope_and_limit": "REQUIRED"}


def build(args: argparse.Namespace) -> dict:
    if not args.stakeholder:
        raise ValueError("at least one --stakeholder is required")
    if len(args.uncertainty or []) != 2:
        raise ValueError("exactly two --uncertainty axes are required")
    axes = [parse_uncertainty(raw) for raw in args.uncertainty]
    claims = [
        {"label": "book-premise", "text": "Multiple long-run AI futures should be considered across goals, control, power, work, conflict, and human meaning.", "source": "Life 3.0", "publication_date": "2017", "type": "philosophical scenario lens", "scope_and_limit": "not a probability forecast"},
        {"label": "book-premise", "text": "Ten 2041 fictional stories plus technical analysis provide social and technical scenario seeds.", "source": "AI 2041", "publication_date": "2021", "type": "fiction + analysis", "scope_and_limit": "visions are not forecast authority"},
        {"label": "observed-2026", "text": "Rapid benchmark progress coexists with evaluation reliability problems and uneven long-horizon agent performance.", "source": "Stanford AI Index 2026, Technical Performance", "publication_date": "2026", "type": "current evidence summary", "scope_and_limit": "benchmark/deployment coverage is partial; no 2041 inference"},
        {"label": "observed-2026", "text": "Adoption, investment, and some task productivity evidence coexist with uneven benefits and early, mixed labor-market evidence.", "source": "Stanford AI Index 2026, Economy", "publication_date": "2026", "type": "current evidence summary", "scope_and_limit": "regions/tasks differ; no long-run net employment conclusion"},
    ]
    claims.extend(parse_claim(raw) for raw in (args.claim or []))
    combos = [
        (axes[0]["low"], axes[1]["low"]),
        (axes[0]["low"], axes[1]["high"]),
        (axes[0]["high"], axes[1]["low"]),
        (axes[0]["high"], axes[1]["high"]),
    ]
    scenarios = []
    for index, (axis1, axis2) in enumerate(combos, start=1):
        scenarios.append({
            "id": chr(64 + index),
            "name": f"Scenario {chr(64 + index)}: {axis1} × {axis2}",
            "focal_question": args.focal,
            "horizon": args.horizon,
            "version_as_of": args.as_of,
            "drivers": [axis["name"] for axis in axes] + ["compute/energy", "adoption and institutions", "public legitimacy"],
            "critical_uncertainties": [{"name": axes[0]["name"], "state": axis1}, {"name": axes[1]["name"], "state": axis2}],
            "scenario_choice": {"label": "scenario-choice", "text": f"Explore the conjunction {axis1} and {axis2} without assigning probability.", "alternatives_not_selected": "RECORD"},
            "original_premises": [claim for claim in claims if claim["label"] == "book-premise"],
            "status_2026": [claim for claim in claims if claim["label"] == "observed-2026"],
            "causal_pathway": [
                {"label": "scenario-choice", "node": f"Axis state: {axis1} + {axis2}", "source_or_assumption": "workshop choice"},
                {"label": "extrapolation", "node": "Mechanism and intermediate state TO DEFINE", "source_or_assumption": "state assumptions and rival mechanism"},
                {"label": "extrapolation", "node": "Outcome TO DEFINE", "source_or_assumption": "must link to indicators and falsifiers"},
            ],
            "stakeholders": [{"group": name, "power": "ASSESS", "benefit_harm": "ASSESS", "voice_exit_appeal": "ASSESS"} for name in args.stakeholder],
            "distributional_effects": {"winners": "REQUIRED", "burdened": "REQUIRED", "non_users": "REQUIRED", "future_generations": "REQUIRED"},
            "indicators": [
                {"indicator": "capability/reliability signal TO DEFINE", "source": "REQUIRED", "frequency": "REQUIRED", "threshold": "REQUIRED", "interpreter": "NAME"},
                {"indicator": "adoption/distribution signal TO DEFINE", "source": "REQUIRED", "frequency": "REQUIRED", "threshold": "REQUIRED", "interpreter": "NAME"},
                {"indicator": "governance/rights signal TO DEFINE", "source": "REQUIRED", "frequency": "REQUIRED", "threshold": "REQUIRED", "interpreter": "NAME"},
            ],
            "falsifiers": ["Observation that weakens the capability-to-deployment mechanism: REQUIRED", "Observation that weakens the governance/distribution mechanism: REQUIRED"],
            "reversible_actions": [{"action": action, "reversibility": "ASSESS", "stop_condition": "SET", "scale_condition": "SET"} for action in (args.action or ["TO PROPOSE"])],
            "lock_in_risks": ["infrastructure/contract", "data/model dependence", "rights or workforce role erosion"],
            "ethical_lenses": ["rights/due process", "justice/distribution", "capability/agency", "care/relationships", "safety/robustness", "democracy/power", "ecology/intergenerational"],
            "ethical_conflicts_and_dissent": "RECORD; do not collapse to one score",
            "review_date": "SET",
            "update_owner": "NAME",
        })
    return {
        "method": "SCENARIO-TRACE (Skill synthesis; scenarios are not forecasts)",
        "as_of": args.as_of,
        "focal_question": args.focal,
        "horizon": args.horizon,
        "claim_labels": sorted(LABELS),
        "publication_baseline": {"Life 3.0": 2017, "AI 2041": 2021, "current_status": 2026},
        "claims": claims,
        "axes": axes,
        "scenarios": scenarios,
        "policy_stress_test": [{"action": action, "scenario_A": "ASSESS", "scenario_B": "ASSESS", "scenario_C": "ASSESS", "scenario_D": "ASSESS", "abuse_failure": "ASSESS", "distribution": "ASSESS", "reversibility_stop": "SET"} for action in (args.action or ["TO PROPOSE"])],
        "backcast": {"90_days": "SET", "1_year": "SET", "3_years": "SET", "scenario_rebuild_triggers": ["new major driver", "contradictory evidence", "affected stakeholder challenge", "indicator gaming or measurement change"]},
        "epistemic_notice": "Fiction and philosophical scenarios are imagination resources, not forecast authority. No scenario receives an implied probability.",
    }


def markdown(data: dict) -> str:
    lines = ["# AI 未来情景实验室", "", f"- as-of：{data['as_of']}", f"- focal question：{data['focal_question']}", f"- horizon：{data['horizon']}", "- **小说/哲学情景不是预测权威；四景不含隐含概率。**", "", "## 声明登记", "", "| 标签 | 声明 | 来源 | 日期 | 边界 |", "|---|---|---|---|---|"]
    for claim in data["claims"]:
        lines.append(f"| {claim['label']} | {claim['text']} | {claim['source']} | {claim['publication_date']} | {claim['scope_and_limit']} |")
    for scenario in data["scenarios"]:
        lines += ["", f"## {scenario['name']}", f"- focal/horizon/version：{scenario['focal_question']} / {scenario['horizon']} / {scenario['version_as_of']}", f"- critical uncertainties：{scenario['critical_uncertainties']}", "- original premises：见声明登记（保留 2017/2021 与类型）", "- 2026 status：见 observed-2026（保留来源和限制）", "- causal pathway：scenario-choice → extrapolation mechanism REQUIRED → outcome REQUIRED", f"- stakeholders：{', '.join(x['group'] for x in scenario['stakeholders'])}；权力/收益/伤害/退出申诉=ASSESS", "- distribution：winners / burdened / non-users / future generations = REQUIRED", "- indicators：能力可靠性、采用分配、治理权利；各需来源/频率/阈值/解释者", "- falsifiers：能力→部署机制与治理→分配机制各至少一个", "- reversible actions：停止/扩展条件 REQUIRED；lock-in：合同/基础设施、依赖、权利/角色侵蚀", "- ethical lenses：rights, justice, capability, care, safety, democracy, ecology；冲突不总分化", "- review date / update owner：SET / NAME"]
    lines += ["", "## 政策压力测试", "- 每个行动跨 A/B/C/D 评估收益、失败/滥用、分配、锁定、可逆与停止。", "", "## 回溯", "- 90 天 / 1 年 / 3 年：SET", "- 重建触发：新驱动、矛盾证据、受影响者质疑、指标投机/口径变化。", ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--focal", required=True)
    parser.add_argument("--horizon", type=int, required=True)
    parser.add_argument("--stakeholder", action="append")
    parser.add_argument("--uncertainty", action="append")
    parser.add_argument("--action", action="append")
    parser.add_argument("--claim", action="append")
    parser.add_argument("--as-of", default="2026-08-16", help="dated evidence baseline; defaults to this package's reviewed 2026 baseline")
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
