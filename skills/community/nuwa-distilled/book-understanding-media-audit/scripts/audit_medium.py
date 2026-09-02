#!/usr/bin/env python3
"""Generate a deterministic, provenance-aware MEDIUM configuration audit."""

from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path
from typing import Any, Iterable

SCHEMA_VERSION = "1.0"
GENERATOR = "book-understanding-media-audit/audit_medium.py"
PACKAGE_PROVENANCE = [
    {
        "claim_ids": ["M001", "M002", "M003", "M004", "M005"],
        "layer": "A",
        "source_ids": ["UM-01", "UM-02", "UM-03"],
        "use": "1964 medium/message, extension, content nesting, and hot/cool probes",
    },
    {
        "claim_ids": ["M006"],
        "layer": "B",
        "source_ids": ["UM-05"],
        "use": "later tetrad attribution",
    },
    {
        "claim_ids": ["M007", "M008"],
        "layer": "C",
        "source_ids": ["UM-04", "UM-06", "UM-07", "UM-08", "UM-09"],
        "use": "media ecology, political-economy critique, and differentiated effects",
    },
    {
        "claim_ids": ["M009", "M010", "M011", "M012"],
        "layer": "D",
        "source_ids": ["D1"],
        "use": "MEDIUM workflow, configuration ledger, dual-layer audit, and falsifiable probes",
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
    medium = _clean(args.medium, "medium")
    use = _clean(args.use, "use")
    content = _clean(args.content, "content")
    actors = _clean_many(args.actor, "actor", minimum=1, maximum=12)
    affordances = _clean_many(args.affordance, "affordance", minimum=1, maximum=12)
    constraints = _clean_many(args.constraint, "constraint", minimum=1, maximum=12)
    harms = _clean_many(args.harm or [], "harm", maximum=12)
    owner = _optional(args.owner, "owner")
    stop_condition = _optional(args.stop_condition, "stop-condition")
    source_locator = _clean(args.source_locator, "source-locator")

    if args.stakes == "high":
        required = {
            "--owner": owner,
            "--stop-condition": stop_condition,
            "--harm": harms[0] if harms else None,
        }
        missing = [flag for flag, value in required.items() if value is None]
        if missing:
            raise ValueError("high-stakes audit requires " + ", ".join(missing))

    gate_status = (
        "analysis_and_probe_design_only"
        if args.stakes == "high"
        else "probe_requires_real_world_validation"
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "generator": GENERATOR,
        "workflow": {
            "name": "MEDIUM",
            "steps": [
                "Map configuration",
                "Examine scale-speed-pattern",
                "Detect extensions and amputations",
                "Inspect figure-ground and power",
                "Use tetrad as hypotheses",
                "Make falsifiable probes",
            ],
            "created_by_skill": True,
            "claim_id": "M009",
        },
        "input": {
            "medium": medium,
            "use": use,
            "content": content,
            "actors": actors,
            "affordances": affordances,
            "constraints": constraints,
            "harms": harms,
        },
        "epistemic_contract": {
            "status": "configuration_hypotheses_not_media_effect_proof",
            "claim_layers": {
                "A": "Understanding Media (1964)",
                "B": "later McLuhan / Laws of Media",
                "C": "later scholarship and critiques",
                "D": "Skill-created operational synthesis",
            },
            "prohibited_inferences": [
                "Changing scale, speed, or pattern is a question generator, not proof of a specific effect.",
                "Hot/cool is not a permanent platform score or ethical ranking.",
                "A tetrad reversal is not a dated forecast.",
                "Technology does not act independently of institutions, ownership, culture, or users.",
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
            "stakes": args.stakes,
            "status": gate_status,
            "owner": owner or "TODO before high-impact test",
            "known_harms": harms,
            "stop_condition": stop_condition or "TODO before high-impact test",
            "rule": "Health, safety, legal, educational, employment, or civic effects require domain review and applicable safeguards.",
            "not_a_launch_decision": True,
        },
        "audit": {
            "configuration": {
                "named_configuration": medium,
                "use_context": use,
                "device_and_interface": "TODO",
                "inputs_and_outputs": "TODO",
                "generation_ranking_recommendation": "TODO",
                "defaults": "TODO",
                "synchronous_or_asynchronous": "TODO",
                "owner_and_business_model": "TODO",
                "users_nonusers_and_represented_people": actors,
                "version_and_observation_date": "TODO",
            },
            "content_layer": {
                "content": content,
                "accuracy_sources_omissions": "TODO",
                "nested_media_chain": [],
                "constant_content_comparison": "TODO",
            },
            "medium_layer": {
                "before_configuration": "TODO",
                "after_configuration": medium,
                "scale_change": "TODO hypothesis",
                "speed_change": "TODO hypothesis",
                "pattern_change": "TODO hypothesis",
                "attention_and_visibility": "TODO hypothesis",
                "participation_and_completion_labor": "TODO hypothesis",
            },
            "extension_amputation_recovery": [
                {
                    "affordance": affordance,
                    "extended_capability": "TODO",
                    "underused_or_outsourced_capability": "TODO",
                    "hidden_labor": "TODO",
                    "failure_consequence": "TODO",
                    "recovery_or_alternative": "TODO",
                }
                for affordance in affordances
            ],
            "constraints": [
                {"constraint": constraint, "who_encounters_it": "TODO", "evidence": "TODO"}
                for constraint in constraints
            ],
            "figure_ground_and_power": {
                "visible_figure": content,
                "ground_defaults_infrastructure_costs": "TODO",
                "who_owns_and_governs": "TODO",
                "who_can_change_rules": "TODO",
                "benefit_and_burden_distribution": actors,
                "offline_accessibility_or_nonprofiled_alternative": "TODO",
            },
            "tetrad_hypotheses": {
                "layer": "B",
                "enhances": "TODO with evidence and counterexample",
                "obsolesces_from_dominance": "TODO with evidence and counterexample",
                "retrieves": "TODO with evidence and counterexample",
                "reverses_at_extreme": "TODO with evidence and counterexample",
                "forecast_warning": "No tetrad cell is a dated prediction.",
            },
            "falsifiable_probes": [
                {
                    "claim": "Because [configuration feature], [group] will show [change] over [window].",
                    "measure": "TODO: logs, task outcome, interview, or observation",
                    "comparison_configuration": "TODO",
                    "alternative_explanation": "TODO",
                    "disconfirming_observation": "TODO",
                    "continue_modify_pause": "TODO before test",
                }
            ],
        },
    }


def to_markdown(data: dict[str, Any]) -> str:
    inputs = data["input"]
    safety = data["safety_gate"]
    lines = [
        "# MEDIUM 媒介配置审计",
        "",
        f"- Schema：`{_md(data['schema_version'])}`",
        f"- 媒介配置：{_md(inputs['medium'])}",
        f"- 使用情境：{_md(inputs['use'])}",
        f"- 风险门：`{_md(safety['stakes'])}` / `{_md(safety['status'])}`",
        f"- 声明来源层 / 定位：`{_md(data['source_context']['declared_layer'])}` / {_md(data['source_context']['locator'])}",
        "",
        "> **认识论边界**：这是配置假设与探针，不证明媒介效应，不给平台贴永久标签，也不批准上线。",
        "",
        "## M — Map configuration",
        "",
        f"- 配置 / 用途 / 内容：{_md(inputs['medium'])} / {_md(inputs['use'])} / {_md(inputs['content'])}",
        f"- 用户、非用户、被代表者：{_md('；'.join(inputs['actors']))}",
        "- 设备、接口、模型/检索、默认、排序、版本、商业模式：TODO",
        "",
        "## E — Examine content and medium separately",
        "",
        "| 层 | 当前观察 | 待核证据 |",
        "|---|---|---|",
        f"| 内容 | {_md(inputs['content'])} | 准确、来源、遗漏、可验证性：TODO |",
        f"| 媒介 | {_md(inputs['medium'])} | 默认、节奏、排序、可见性、角色：TODO |",
        "",
        "| 维度 | Before | After | 假设效应 | 受益/受损 | 如何观察 |",
        "|---|---|---|---|---|---|",
        "| 尺度 | TODO | TODO | TODO | TODO | TODO |",
        "| 速度 | TODO | TODO | TODO | TODO | TODO |",
        "| 模式 | TODO | TODO | TODO | TODO | TODO |",
        "| 注意/可见性 | TODO | TODO | TODO | TODO | TODO |",
        "| 参与/补全劳动 | TODO | TODO | TODO | TODO | TODO |",
        "",
        "## D — Detect extension, amputation, recovery",
        "",
        "| Affordance | 延伸 | 少用/外包 | 隐形劳动 | 失效后果 | 恢复/替代 |",
        "|---|---|---|---|---|---|",
    ]
    for affordance in inputs["affordances"]:
        lines.append(f"| {_md(affordance)} | TODO | TODO | TODO | TODO | TODO |")
    lines.extend(
        [
            "",
            f"- 已知约束：{_md('；'.join(inputs['constraints']))}",
            "",
            "## I — Inspect figure, ground, and power",
            "",
            f"- Figure：{_md(inputs['content'])}",
            "- Ground（默认、协议、基础设施、成本、节奏）：TODO",
            "- 所有权 / 规则改变权 / 商业激励：TODO / TODO / TODO",
            "- 分群收益与负担、离线/无障碍/非画像替代：TODO",
            "",
            "## U — Use tetrad as B-layer hypotheses",
            "",
            "- 增强 / 退出主导 / 复归 / 极端反转：TODO / TODO / TODO / TODO",
            "- 每格证据、反例和替代解释：TODO",
            "- 注意：反转不是带日期的预测。",
            "",
            "## M — Make falsifiable probes",
            "",
            "- 因为 [配置特征]，预计 [群体] 在 [窗口] 出现 [变化]：TODO",
            "- 日志 / 行为任务 / 访谈 / 观察：TODO",
            "- 对照配置 / 替代解释 / 推翻观察：TODO / TODO / TODO",
            f"- owner / 停止条件：{_md(safety['owner'])} / {_md(safety['stop_condition'])}",
            f"- 已知伤害：{_md('；'.join(safety['known_harms']) or 'TODO')}",
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
            "## 配置与判断更新日志",
            "",
            "| 日期 | 配置版本 | 证据变化 | 被削弱的假设 | 决定 |",
            "|---|---|---|---|---|",
            "| TODO | TODO | TODO | TODO | TODO |",
        ]
    )
    return "\n".join(lines) + "\n"


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a bounded, provenance-aware MEDIUM configuration audit."
    )
    parser.add_argument("--medium", required=True)
    parser.add_argument("--use", required=True)
    parser.add_argument("--content", required=True)
    parser.add_argument("--actor", action="append", required=True)
    parser.add_argument("--affordance", action="append", required=True)
    parser.add_argument("--constraint", action="append", required=True)
    parser.add_argument("--harm", action="append")
    parser.add_argument("--stakes", choices=["low", "moderate", "high"], default="moderate")
    parser.add_argument("--owner")
    parser.add_argument("--stop-condition")
    parser.add_argument("--source-layer", choices=["A", "B", "C", "D"], default="D")
    parser.add_argument(
        "--source-locator",
        default="references/claim-layer-map.md#M009-M012",
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
