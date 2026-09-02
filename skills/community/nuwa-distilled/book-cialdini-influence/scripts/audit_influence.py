#!/usr/bin/env python3
"""Deterministic deep-tier worksheet generator. Standard library only."""
from __future__ import annotations
import argparse
import html
import json
import sys
from pathlib import Path
from typing import Any

CONFIG = {'package': 'book-cialdini-influence',
 'script': 'audit_influence.py',
 'workflow': 'PERSUADE',
 'description': 'Generate a bounded ethical-influence audit; never predict conversion or approve deployment.',
 'fields': [('artifact', {'required': True}),
            ('audience', {'required': True}),
            ('goal', {'required': True}),
            ('mechanism',
             {'action': 'append',
              'required': True,
              'choices': ['reciprocity',
                          'commitment',
                          'social-proof',
                          'authority',
                          'liking',
                          'scarcity',
                          'unity'],
              'min': 1,
              'max': 7}),
            ('evidence', {'action': 'append', 'required': True, 'min': 1, 'max': 12}),
            ('risk', {'choices': ['low', 'medium', 'high'], 'default': 'medium'}),
            ('owner', {}),
            ('disclosure', {}),
            ('exit_path', {}),
            ('harm', {'action': 'append', 'max': 12}),
            ('alternative', {'action': 'append', 'max': 8}),
            ('stop_condition', {})],
 'high': {'field': 'risk', 'value': 'high', 'requires': ['owner', 'disclosure', 'exit_path', 'harm']},
 'block_flags': [],
 'prohibited': 'No fabricated proof, authority, scarcity, covert sensitive profiling, coercion, or claim of '
               'ethical/legal approval.',
 'epistemic': {'A': 'Influence book principles and edition-specific claims',
               'B': 'later Cialdini material including unity',
               'C': 'independent evidence, dark-pattern and ethics boundaries',
               'D': 'Skill-created PERSUADE audit'},
 'provenance': [('A/B', ['CI-001', 'CI-002', 'CI-003'], ['CI-S01', 'CI-S02', 'CI-S03']),
                ('C', ['CI-004', 'CI-005', 'CI-012'], ['CI-S04', 'CI-S07', 'CI-S09']),
                ('D', ['CI-013', 'CI-018'], ['CI-S11'])],
 'sections': {'truthfulness': ['evidence', 'disclosure'],
              'autonomy': ['exit_path', 'alternative'],
              'mechanism_hypotheses': ['mechanism'],
              'harm_and_stop': ['harm', 'stop_condition', 'owner']}}
SCHEMA_VERSION = "1.0"
GENERATOR = "book-cialdini-influence/audit_influence.py"
MAX_TEXT = 4000


def _clean(value: str, field: str) -> str:
    normalized = " ".join(value.split())
    if not normalized:
        raise ValueError(f"{field} must not be blank")
    if len(normalized) > MAX_TEXT:
        raise ValueError(f"{field} exceeds {MAX_TEXT} characters")
    return normalized


def _clean_many(values: list[str] | None, field: str, minimum: int = 0, maximum: int = 12) -> list[str]:
    cleaned = [_clean(v, field) for v in (values or [])]
    if len(cleaned) < minimum:
        raise ValueError(f"{field} requires at least {minimum} value(s)")
    if len(cleaned) > maximum:
        raise ValueError(f"{field} accepts at most {maximum} value(s)")
    if len({v.casefold() for v in cleaned}) != len(cleaned):
        raise ValueError(f"{field} must not contain duplicate values")
    return cleaned


def _md(value: Any) -> str:
    return html.escape(str(value), quote=False).replace("\\", "\\\\").replace("|", "\\|")


def _is_high(data: dict[str, Any]) -> bool:
    rule = CONFIG.get("high")
    if not rule:
        return False
    if "field" in rule and "value" in rule:
        return data.get(rule["field"]) == rule["value"]
    if "field" in rule and "not_value" in rule:
        return data.get(rule["field"]) != rule["not_value"]
    return any(data.get(field) == expected for field, expected in rule.get("any", []))


def build_record(args: argparse.Namespace) -> dict[str, Any]:
    data: dict[str, Any] = {}
    for field, opts in CONFIG["fields"]:
        value = getattr(args, field)
        if opts.get("flag"):
            data[field] = bool(value)
        elif opts.get("action") == "append":
            data[field] = _clean_many(value, field, opts.get("min", 0), opts.get("max", 12))
        elif opts.get("type") == "int":
            if value < opts.get("min_value", value) or value > opts.get("max_value", value):
                raise ValueError(f"{field} must be between {opts['min_value']} and {opts['max_value']}")
            data[field] = value
        elif value is None:
            data[field] = None
        else:
            data[field] = _clean(value, field)

    blocked_reasons = [field for field in CONFIG.get("block_flags", []) if data.get(field)]
    blocked = bool(blocked_reasons)
    if not blocked:
        missing_normal = [field for field in CONFIG.get("normal_requires", []) if not data.get(field)]
        if missing_normal:
            raise ValueError("ordinary workflow requires " + " and ".join("--" + f.replace("_", "-") for f in missing_normal))
    high = _is_high(data)
    if high:
        missing = [field for field in CONFIG["high"]["requires"] if not data.get(field)]
        if missing:
            raise ValueError("high-risk gate requires " + " and ".join("--" + f.replace("_", "-") for f in missing))

    if blocked:
        worksheets: dict[str, Any] = {
            "scope_block": {
                "triggered_flags": blocked_reasons,
                "ordinary_workflow_withheld": True,
                "routing": CONFIG.get("blocked_message", "Stop ordinary analysis and seek appropriate qualified support or governance."),
            }
        }
        safety = "blocked_scope_and_support_required"
    else:
        worksheets = {
            section: {field: data.get(field) if data.get(field) not in (None, [], "") else "TODO" for field in fields}
            for section, fields in CONFIG["sections"].items()
        }
        safety = "high_risk_governance_gate_passed_not_approved" if high else "bounded_draft_not_approved"

    return {
        "schema_version": SCHEMA_VERSION,
        "generator": GENERATOR,
        "workflow": {"name": CONFIG["workflow"], "created_by_skill": True},
        "status": "governance_review_required",
        "input": data,
        "safety_gate": {
            "status": safety,
            "blocked": blocked,
            "high_risk": high,
            "rule": "A passed data-completeness gate is not ethical, legal, clinical, editorial, accessibility, safety, or deployment approval.",
        },
        "epistemic_contract": {
            "layers": CONFIG["epistemic"],
            "prohibited_inference": CONFIG["prohibited"],
            "package_claim_map": "references/claim-layer-map.md",
            "source_notes": "references/source-notes.md",
        },
        "provenance": [
            {"layer": layer, "claim_ids": claims, "source_ids": sources}
            for layer, claims, sources in CONFIG["provenance"]
        ],
        "static_boundaries": CONFIG.get("static", {}),
        "worksheets": worksheets,
    }


def to_markdown(record: dict[str, Any]) -> str:
    lines = [
        f"# {_md(record['workflow']['name'])} 工作底稿",
        "",
        f"- 状态：`{_md(record['status'])}`",
        f"- 安全门：`{_md(record['safety_gate']['status'])}`",
        f"- 生成器：`{_md(record['generator'])}`",
        "",
        "> 本输出是未批准的结构化工作底稿；不构成效果预测、事实核验或专业批准。",
        "",
        "## 输入记录",
        "",
        "| 字段 | 值 |",
        "|---|---|",
    ]
    for key, value in record["input"].items():
        shown = "；".join(str(v) for v in value) if isinstance(value, list) else value
        lines.append(f"| {_md(key)} | {_md(shown if shown not in (None, '') else 'TODO')} |")
    lines += ["", "## 工作表", ""]
    for section, body in record["worksheets"].items():
        lines += [f"### {_md(section)}", ""]
        for key, value in body.items():
            shown = "；".join(str(v) for v in value) if isinstance(value, list) else value
            lines.append(f"- **{_md(key)}**：{_md(shown)}")
        lines.append("")
    if record["static_boundaries"]:
        lines += ["## 固定边界", ""]
        for key, value in record["static_boundaries"].items():
            lines.append(f"- **{_md(key)}**：{_md(value)}")
        lines.append("")
    lines += ["## Claim / source provenance", "", "| 层 | Claim IDs | Source IDs |", "|---|---|---|"]
    for item in record["provenance"]:
        lines.append(f"| {_md(item['layer'])} | {_md(', '.join(item['claim_ids']))} | {_md(', '.join(item['source_ids']))} |")
    lines += ["", "## 禁止推断", "", _md(record["epistemic_contract"]["prohibited_inference"]), ""]
    return "\n".join(lines) + "\n"


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=CONFIG["description"])
    for field, opts in CONFIG["fields"]:
        flags = "--" + field.replace("_", "-")
        kwargs: dict[str, Any] = {}
        if opts.get("flag"):
            kwargs["action"] = "store_true"
        else:
            if opts.get("required"):
                kwargs["required"] = True
            if "choices" in opts:
                kwargs["choices"] = opts["choices"]
            if opts.get("action") == "append":
                kwargs["action"] = "append"
            if opts.get("type") == "int":
                kwargs["type"] = int
            if "default" in opts:
                kwargs["default"] = opts["default"]
        p.add_argument(flags, dest=field, **kwargs)
    p.add_argument("--format", choices=["json", "markdown"], default="markdown")
    p.add_argument("--output")
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        record = build_record(args)
        text = json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n" if args.format == "json" else to_markdown(record)
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
