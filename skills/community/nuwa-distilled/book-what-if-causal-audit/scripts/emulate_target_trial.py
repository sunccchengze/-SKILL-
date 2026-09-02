#!/usr/bin/env python3
"""Create a deterministic, assumption-explicit target-trial emulation record."""
from __future__ import annotations
import argparse, html, json, sys
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1.0"
GENERATOR = "book-what-if-causal-audit/emulate_target_trial.py"
HIGH_RISK = {"personnel", "labor", "healthcare", "education", "credit", "law-enforcement", "content-governance"}
PROVENANCE = [
    {"claim_ids":["CIW001","CIW004","CIW006","CIW009"],"layer":"A","source_ids":["CIW-01","CIW-02"],"use":"question, counterfactual effect, assumptions, target trial"},
    {"claim_ids":["CIW019","CIW020","CIW021"],"layer":"C","source_ids":["CIW-07","CIW-08","CIW-10"],"use":"reporting, design bias, and ML limits"},
    {"claim_ids":["CIW025","CIW026","CIW027","CIW028"],"layer":"D","source_ids":["D1"],"use":"TARGET workflow and release gates"},
]

def clean(value: str, field: str) -> str:
    out = " ".join(value.split())
    if not out: raise ValueError(f"{field} must not be blank")
    return out

def many(values: list[str] | None, field: str, minimum: int=0, maximum: int=20) -> list[str]:
    out=[clean(v,field) for v in (values or [])]
    if len(out)<minimum: raise ValueError(f"{field} requires at least {minimum} value(s)")
    if len(out)>maximum: raise ValueError(f"{field} accepts at most {maximum} value(s)")
    if len({v.casefold() for v in out}) != len(out): raise ValueError(f"{field} must not contain duplicate values")
    return out

def opt(value: str|None, field: str) -> str|None: return clean(value,field) if value is not None else None

def build(args: argparse.Namespace) -> dict[str,Any]:
    vals={k:clean(getattr(args,k),k.replace("_","-")) for k in ["question","population","treatment","comparator","outcome","time_zero","follow_up","estimand"]}
    assumptions=many(args.assumption,"assumption",3,12); confounders=many(args.confounder,"confounder",0,20); evidence=many(args.evidence,"evidence",1,20)
    high=args.risk_level=="high" or args.domain in HIGH_RISK
    gates={k:opt(getattr(args,k),k.replace("_","-")) for k in ["accountable_owner","applicable_rule","affected_group","impact_evidence","appeal_path","rollback_trigger","stop_condition"]}
    if high:
        missing=["--"+k.replace("_","-") for k,v in gates.items() if v is None]
        if missing: raise ValueError("high-risk causal audit requires " + ", ".join(missing))
    return {
      "schema_version":SCHEMA_VERSION,"generator":GENERATOR,
      "workflow":{"name":"TARGET","created_by_skill":True,"steps":["Target question","Articulate trial","Register assumptions","Graph structure","Estimate diagnostics","Robustness","Transmit limits"],"claim_id":"CIW025"},
      "epistemic_contract":{"status":"design_and_assumption_audit_not_causal_proof","identification_precedes_estimation":True,"prediction_is_not_intervention":True,"prohibited_inference":"No estimator, p-value, predictive score, or ML flexibility repairs an unidentified effect."},
      "question":vals["question"],
      "target_trial":{
        "eligibility_criteria":vals["population"],"treatment_strategies":[vals["treatment"],vals["comparator"]],"assignment_procedure":"Hypothetical random assignment; observational emulation requires an explicit identification strategy.","follow_up":{"time_zero":vals["time_zero"],"period":vals["follow_up"]},"outcome":vals["outcome"],"causal_contrast":vals["estimand"],"analysis_plan":"TODO only after identification and data diagnostics"
      },
      "emulation":{
        "mapping_status":"not_yet_mapped","time_zero_alignment":"TODO: eligibility, strategy assignment, and follow-up must align","available_evidence":evidence,"candidate_confounders":confounders,"covariate_role_table":[],"method":"TODO: choose only after estimand, graph, and assumptions"
      },
      "assumption_register":[{"statement":a,"status":"asserted_not_verified","diagnostic":"TODO","falsifier_or_sensitivity":"TODO","owner":"TODO"} for a in assumptions],
      "required_assumption_slots":["consistency/well-defined strategies","conditional exchangeability or alternative identification","positivity/overlap for chosen target and method","measurement and missingness","no interference if required by estimand"],
      "diagnostics":{"overlap":"TODO","covariate_balance":"TODO","weights_and_influence":"TODO","missingness":"TODO","negative_controls":"TODO","model_specification":"TODO","sensitivity_to_unmeasured_confounding":"TODO"},
      "safety_gate":{"high_risk":high,"risk_level":args.risk_level,"domain":args.domain,"status":"governance_review_required" if high else "analysis_only","submitted_not_verified":gates,"release_rule":"Even complete submitted fields do not verify evidence or authorize intervention."},
      "provenance":PROVENANCE,"claim_map":"references/claim-layer-map.md","source_ledger":"references/source-notes.md"
    }

def esc(v:object)->str: return html.escape(str(v),quote=False).replace("\\","\\\\").replace("|","\\|")
def markdown(d:dict[str,Any])->str:
    t=d["target_trial"]; g=d["safety_gate"]
    lines=["# TARGET 因果设计记录","",f"- 问题：{esc(d['question'])}",f"- 状态：`{esc(d['epistemic_contract']['status'])}`",f"- 风险：`{esc(g['domain'])}` / `{esc(g['status'])}`","","> 本输出是设计与假设审计，不是因果证明、效应估计、临床/人事/政策建议或部署批准。","","## 七项目标试验协议","","| 项目 | 规格 |","|---|---|",f"| 资格 | {esc(t['eligibility_criteria'])} |",f"| 策略 | {esc(' vs '.join(t['treatment_strategies']))} |",f"| 分配 | {esc(t['assignment_procedure'])} |",f"| 随访 | time zero={esc(t['follow_up']['time_zero'])}; {esc(t['follow_up']['period'])} |",f"| 结局 | {esc(t['outcome'])} |",f"| 因果对比 | {esc(t['causal_contrast'])} |",f"| 分析 | {esc(t['analysis_plan'])} |","","## 识别假设账本","","| 假设 | 当前状态 | 可观测诊断 | 敏感性/推翻 |","|---|---|---|---|"]
    lines += [f"| {esc(x['statement'])} | asserted_not_verified | TODO | TODO |" for x in d["assumption_register"]]
    lines += ["","## 数据与诊断","",f"- 证据：{esc('；'.join(d['emulation']['available_evidence']))}",f"- 候选混杂：{esc('；'.join(d['emulation']['candidate_confounders']) or 'TODO')}","- time-zero 对齐 / 重叠 / 平衡 / 权重 / 缺失 / 负对照 / 模型 / 未测混杂敏感性：TODO","","## 高影响发布门","",f"- 提交但未核验：{esc(json.dumps(g['submitted_not_verified'],ensure_ascii=False,sort_keys=True))}",f"- 规则：{esc(g['release_rule'])}","","## Provenance","","| 层 | Claims | Sources |","|---|---|---|"]
    lines += [f"| {x['layer']} | {esc(', '.join(x['claim_ids']))} | {esc(', '.join(x['source_ids']))} |" for x in d["provenance"]]
    return "\n".join(lines)+"\n"
def parser()->argparse.ArgumentParser:
    p=argparse.ArgumentParser(description="Generate an assumption-explicit target-trial emulation record.")
    for x in ["question","population","treatment","comparator","outcome","time-zero","follow-up","estimand"]: p.add_argument("--"+x,required=True,dest=x.replace("-","_"))
    p.add_argument("--assumption",action="append",required=True); p.add_argument("--confounder",action="append"); p.add_argument("--evidence",action="append",required=True)
    p.add_argument("--domain",default="research",choices=["research","business","personnel","labor","healthcare","education","credit","law-enforcement","content-governance"]); p.add_argument("--risk-level",choices=["low","moderate","high"],default="moderate")
    for x in ["accountable-owner","applicable-rule","affected-group","impact-evidence","appeal-path","rollback-trigger","stop-condition"]: p.add_argument("--"+x,dest=x.replace("-","_"))
    p.add_argument("--format",choices=["json","markdown"],default="markdown"); p.add_argument("--output"); return p
def main(argv:list[str]|None=None)->int:
    try:
        a=parser().parse_args(argv); d=build(a); text=json.dumps(d,ensure_ascii=False,indent=2,sort_keys=True)+"\n" if a.format=="json" else markdown(d)
        if a.output: out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(text,encoding="utf-8")
        else: sys.stdout.write(text)
        return 0
    except (ValueError,OSError) as e: print(f"ERROR: {e}",file=sys.stderr); return 2
if __name__=="__main__": raise SystemExit(main())
