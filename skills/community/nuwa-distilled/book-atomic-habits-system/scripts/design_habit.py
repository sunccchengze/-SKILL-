#!/usr/bin/env python3
"""Generate an evidence-bounded ATOM habit-system worksheet.

This dependency-free helper structures information supplied by the user. It does
not diagnose a disorder, predict success, or calculate when a habit will form.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence


def _bullets(values: Sequence[str], empty: str = "（待填写）") -> str:
    return "\n".join(f"- {value}" for value in values) if values else f"- {empty}"


def build_plan(
    *,
    behavior: str,
    value: str,
    identity: str,
    cue: str,
    location: str,
    tiny_start: str,
    standard: str,
    advanced: str = "",
    safety_cap: str = "不以熬夜、惩罚性补偿或健康风险换取连续记录",
    barriers: Sequence[str] = (),
    reward: str = "",
    observation_days: int = 14,
) -> dict[str, object]:
    """Build a transparent plan without promising automaticity or outcomes."""
    if not 1 <= observation_days <= 30:
        raise ValueError("observation_days must be between 1 and 30")
    required = {
        "behavior": behavior,
        "value": value,
        "identity": identity,
        "cue": cue,
        "location": location,
        "tiny_start": tiny_start,
        "standard": standard,
    }
    blank = [name for name, value_ in required.items() if not value_.strip()]
    if blank:
        raise ValueError(f"required fields cannot be blank: {', '.join(blank)}")

    return {
        "method": "ATOM 九步法（本 Skill 的现代综合，不是书中原章节）",
        "source_layers": {
            "author_framework": "行为循环、四定律、两分钟入口、系统/身份等教学框架",
            "acknowledged_predecessors": "BJ Fogg 相关锚点方法、David Allen 两分钟原则及作者明确提到的前作需保留归属",
            "independent_research": "实施意图、情境线索、重复与自动性研究用于限定，不证明个人必然成功",
            "skill_synthesis": "ATOM、四级行为、恢复和迁移模板",
        },
        "scientific_boundary": (
            "观察周期不是习惯形成期限；本计划不承诺 21/66 天、每天 1% 或任何结果，"
            "高频也不自动等于习惯。"
        ),
        "safety_boundary": (
            "若涉及依赖/危险戒断、进食障碍、强迫、自伤、医学风险或暴力风险，"
            "停止普通习惯建议并寻求合格专业支持；不自行改变药物或治疗。"
        ),
        "observation": {
            "days": observation_days,
            "label": "短周期观察与系统复盘，不是形成期限",
        },
        "assess": {
            "agency_and_constraints": [],
            "clinical_or_safety_screen": [],
            "professional_support_needed": [],
        },
        "target": {
            "behavior": behavior,
            "definition_of_done": standard,
            "outcomes_are_not_the_habit": True,
        },
        "observe_current_loop": {
            "cue": cue,
            "desired_state_or_craving": "",
            "current_response": "",
            "immediate_function_or_reward": reward,
            "delayed_effect": "",
            "barriers": list(barriers),
        },
        "map_identity": {
            "value": value,
            "revisable_identity": identity,
            "statement": f"我在练习成为{identity}，因为我重视{value}；一次漏做不作人格判决。",
        },
        "install_cue": {
            "cue": cue,
            "location": location,
            "implementation_intention": f"当{cue}，在{location}，我会{behavior}。",
            "migration_backup": "",
        },
        "optimize_four_laws": {
            "obvious": [],
            "attractive": [],
            "easy": [],
            "satisfying": [reward] if reward else [],
            "one_or_two_changes_only": True,
        },
        "behavior_levels": {
            "gateway_about_two_minutes": tiny_start,
            "standard_with_real_value": standard,
            "advanced_optional": advanced,
            "safety_cap_or_stop_condition": safety_cap,
        },
        "measure_and_recover": {
            "fields": [
                "预定线索是否出现",
                "是否开始",
                "最低/标准/进阶版",
                "启动难度 1–5",
                "真实产物或副作用",
            ],
            "recovery": "漏做后在下一个安全可用线索做最低版；不加倍、不惩罚、不作身份审判。",
            "diagnostic_rule": "若连续两次在同一步失败，只改一个线索、规模、摩擦或资源变量。",
        },
        "review": {
            "questions": [
                "线索是否稳定且可见？",
                "最低入口是否自然通向标准版？",
                "标准版是否产生真实价值？",
                "启动是否更少依赖额外提醒？",
                "是否出现健康、安全、强迫或指标游戏副作用？",
            ],
            "decision": "继续 / 缩小 / 扩展 / 换锚点 / 停止",
            "next_single_change": "",
        },
    }


def render_markdown(plan: dict[str, object]) -> str:
    target = plan["target"]
    loop = plan["observe_current_loop"]
    identity = plan["map_identity"]
    cue = plan["install_cue"]
    levels = plan["behavior_levels"]
    measure = plan["measure_and_recover"]
    observation = plan["observation"]
    assert isinstance(target, dict) and isinstance(loop, dict)
    assert isinstance(identity, dict) and isinstance(cue, dict)
    assert isinstance(levels, dict) and isinstance(measure, dict)
    assert isinstance(observation, dict)
    barriers = loop["barriers"]
    fields = measure["fields"]
    assert isinstance(barriers, list) and isinstance(fields, list)

    return f"""# ATOM 习惯系统工作表

> **科学边界**：{plan['scientific_boundary']}
>
> **安全边界**：{plan['safety_boundary']}

- **方法**：{plan['method']}
- **观察周期**：{observation['days']} 天（{observation['label']}）

## A｜安全与自主

- 用户可控范围与结构性约束：（待填写）
- 临床/安全筛查：（待填写）
- 所需专业支持或合理便利：（待填写）

## T｜一个可观察行为

- **行为**：{target['behavior']}
- **完成定义**：{target['definition_of_done']}
- 结果指标不直接冒充习惯。

## O｜当前循环

- **当前线索**：{loop['cue']}
- **期待的状态/渴求**：（待填写）
- **当前反应**：（待填写）
- **即时功能/奖励**：{loop['immediate_function_or_reward'] or '（待填写）'}
- **延迟影响**：（待填写）
- **已知摩擦**：
{_bullets(barriers)}

## M｜可修订身份

- **价值**：{identity['value']}
- **方向**：{identity['revisable_identity']}
- **非羞辱表述**：{identity['statement']}

## I｜安装线索

- **实施意图**：{cue['implementation_intention']}
- **情境迁移备选**：（待填写）

## O｜四定律

| 显而易见 | 有吸引力 | 容易做 | 令人满足 |
|---|---|---|---|
| （待填写） | （待填写） | （待填写） | {loop['immediate_function_or_reward'] or '（待填写）'} |

> 先选 1–2 个改动；四定律是作者的实用分类，不是完备自然定律。

## M｜最低入口、标准版、进阶版与封顶

- **最低入口（约两分钟）**：{levels['gateway_about_two_minutes']}
- **标准版（有真实价值）**：{levels['standard_with_real_value']}
- **进阶版（可选）**：{levels['advanced_optional'] or '（待填写）'}
- **封顶/停止条件**：{levels['safety_cap_or_stop_condition']}

## M｜测量与恢复

记录：
{_bullets(fields)}

- **恢复**：{measure['recovery']}
- **诊断规则**：{measure['diagnostic_rule']}

## R｜复盘系统

- 最低入口是否自然通向标准版？
- 标准版是否产生真实价值？
- 是否更少依赖额外提醒？
- 是否有安全、强迫、睡眠或指标游戏副作用？
- 决策：继续 / 缩小 / 扩展 / 换锚点 / 停止
- 下一周期只改一个变量：（待填写）

## 来源分层

- **作者框架**：行为循环、四定律、两分钟入口、系统/身份等教学框架；
- **被致谢前作**：BJ Fogg 相关锚点方法、David Allen 两分钟原则及作者明确提到的前作需保留归属；
- **独立研究**：实施意图、情境、重复和自动性只用于概率性限定；
- **本 Skill 综合**：ATOM、四级行为、恢复与迁移模板。
"""


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Generate an evidence-bounded ATOM habit plan.")
    p.add_argument("--behavior", required=True)
    p.add_argument("--value", required=True)
    p.add_argument("--identity", required=True)
    p.add_argument("--cue", required=True)
    p.add_argument("--location", required=True)
    p.add_argument("--tiny-start", required=True)
    p.add_argument("--standard", required=True)
    p.add_argument("--advanced", default="")
    p.add_argument("--safety-cap", default="不以熬夜、惩罚性补偿或健康风险换取连续记录")
    p.add_argument("--barrier", action="append", default=[])
    p.add_argument("--reward", default="")
    p.add_argument("--observation-days", type=int, default=14)
    p.add_argument("--json", action="store_true", help="Emit structured JSON instead of Markdown.")
    p.add_argument("--output", type=Path, help="Write to this path instead of stdout.")
    return p


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        plan = build_plan(
            behavior=args.behavior,
            value=args.value,
            identity=args.identity,
            cue=args.cue,
            location=args.location,
            tiny_start=args.tiny_start,
            standard=args.standard,
            advanced=args.advanced,
            safety_cap=args.safety_cap,
            barriers=args.barrier,
            reward=args.reward,
            observation_days=args.observation_days,
        )
    except ValueError as exc:
        parser().error(str(exc))
    text = json.dumps(plan, ensure_ascii=False, indent=2) + "\n" if args.json else render_markdown(plan)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="" if text.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
