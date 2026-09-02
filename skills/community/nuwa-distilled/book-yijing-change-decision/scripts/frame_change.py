#!/usr/bin/env python3
"""Generate a non-divinatory CHANGE decision worksheet.

The script deliberately does not cast hexagrams, score auspiciousness, or predict
outcomes. It keeps supplied facts, assumptions, and unknowns in separate fields.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence


def _bullets(values: Sequence[str], empty: str = "（待填写）") -> str:
    return "\n".join(f"- {value}" for value in values) if values else f"- {empty}"


def build_record(
    *,
    question: str,
    horizon: str,
    facts: Sequence[str] = (),
    assumptions: Sequence[str] = (),
    unknowns: Sequence[str] = (),
    stakeholders: Sequence[str] = (),
) -> dict[str, object]:
    """Build a structured record without interpreting or predicting the case."""
    return {
        "method": "CHANGE（本 Skill 的现代综合；非古代筮法）",
        "epistemic_boundary": (
            "经典或卦象只能进入解释/假设层，不能充当外部事实证据，"
            "也不能替代医学、法律、财务或安全专业判断。"
        ),
        "question": question,
        "horizon": horizon,
        "facts": list(facts),
        "assumptions": list(assumptions),
        "unknowns": list(unknowns),
        "stakeholders": list(stakeholders),
        "situation": {"timing": [], "position": [], "relationships": list(stakeholders), "momentum": []},
        "incipient_signals": [],
        "counter_frames": {"continue": [], "transform": [], "opposite": []},
        "action": {"reversible_72h": [], "evidence_needed": list(unknowns), "red_lines": [], "stop_or_escalate": []},
        "review": {"date": "", "supported_or_weakened_assumptions": [], "expired_analogies": []},
    }


def render_markdown(record: dict[str, object]) -> str:
    facts = record["facts"]
    assumptions = record["assumptions"]
    unknowns = record["unknowns"]
    stakeholders = record["stakeholders"]
    assert isinstance(facts, list) and isinstance(assumptions, list)
    assert isinstance(unknowns, list) and isinstance(stakeholders, list)

    return f"""# CHANGE 变化决策工作表

> {record['epistemic_boundary']}

- **方法**：{record['method']}
- **问题**：{record['question']}
- **时间范围**：{record['horizon']}

## 0. 边界检查

- 风险等级：低 / 中 / 高（待判断）
- 必须转向的专业证据：（待填写）
- 经典材料不得决定：（待填写）

## 1. 事实分栏

### 已知事实
{_bullets(facts)}

### 假设（不得混入事实）
{_bullets(assumptions)}

### 未知 / 待核
{_bullets(unknowns)}

## 2. 时—位—应—势

- **时**（阶段、窗口、截止日）：（待填写）
- **位**（权限、责任、能力、约束）：（待填写）
- **应**（协同、依赖、反对者）：
{_bullets(stakeholders)}
- **势**（增强/减弱且有数据支持的力量）：（待填写）

## 3. “几”与替代解释

| 弱信号 | 基线 | 替代解释 | 核验方式/日期 | 行动阈值 |
|---|---|---|---|---|
| （待填写） | | | | |

## 4. 经典层（可选，不是事实证据）

- 原典定位：（待核）
- 层级：古经 / 《十翼》 / 历史解释
- 本 Skill 的现代提示：（待填写）
- 另一种解释：（待填写）
- 不能推出的现实事实：（待填写）

## 5. 竞争情景

1. **继续**：若结构不变，什么会持续？（待填写）
2. **转化**：改变哪个结构变量？（待填写）
3. **反面**：核心假设若错，最早出现什么？（待填写）

## 6. 下一步

- 72 小时可逆动作：（待填写）
- 待补证据：
{_bullets(unknowns)}
- 红线：（待填写）
- 停止/升级条件：（待填写）

## 7. 更新

- 复盘日期：（待填写）
- 哪个假设被支持/削弱：（待填写）
- 时、位、应、势哪项改变：（待填写）
- 哪个经典类比已失效：（待填写）
"""


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Generate a non-divinatory CHANGE worksheet.")
    p.add_argument("--question", required=True)
    p.add_argument("--horizon", required=True)
    p.add_argument("--fact", action="append", default=[])
    p.add_argument("--assumption", action="append", default=[])
    p.add_argument("--unknown", action="append", default=[])
    p.add_argument("--stakeholder", action="append", default=[])
    p.add_argument("--json", action="store_true", help="Emit structured JSON instead of Markdown.")
    p.add_argument("--output", type=Path, help="Write to this path instead of stdout.")
    return p


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    record = build_record(
        question=args.question,
        horizon=args.horizon,
        facts=args.fact,
        assumptions=args.assumption,
        unknowns=args.unknown,
        stakeholders=args.stakeholder,
    )
    text = json.dumps(record, ensure_ascii=False, indent=2) + "\n" if args.json else render_markdown(record)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="" if text.endswith("\n") else "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
