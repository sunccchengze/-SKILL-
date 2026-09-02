#!/usr/bin/env python3
"""Generate a deterministic STAMP/STPA control-and-constraint audit scaffold."""
from __future__ import annotations
import argparse, html, json, sys
from pathlib import Path
from typing import Any
SCHEMA_VERSION="1.0"; GENERATOR="book-safer-world-control-audit/analyze_safety_control.py"
HIGH={"personnel","labor","healthcare","education","credit","law-enforcement","content-governance"}
PROVENANCE=[{"claim_ids":["ESW001","ESW004","ESW006","ESW009","ESW010"],"layer":"A","source_ids":["ESW-01","ESW-02"],"use":"STAMP control model and STPA structure"},{"claim_ids":["ESW019","ESW020","ESW021"],"layer":"C","source_ids":["ESW-08","ESW-09","ESW-10"],"use":"comparative evidence and validation limits"},{"claim_ids":["ESW025","ESW026","ESW027","ESW028"],"layer":"D","source_ids":["D1"],"use":"CONTROL workflow and deployment gates"}]
def clean(v:str,f:str)->str:
 o=" ".join(v.split());
 if not o: raise ValueError(f"{f} must not be blank")
 return o
def many(v:list[str]|None,f:str,lo:int=0,hi:int=24)->list[str]:
 o=[clean(x,f) for x in (v or [])]
 if len(o)<lo: raise ValueError(f"{f} requires at least {lo} value(s)")
 if len(o)>hi: raise ValueError(f"{f} accepts at most {hi} value(s)")
 if len({x.casefold() for x in o})!=len(o): raise ValueError(f"{f} must not contain duplicate values")
 return o
def opt(v:str|None,f:str)->str|None:return clean(v,f) if v is not None else None
def build(a:argparse.Namespace)->dict[str,Any]:
 system=clean(a.system,"system"); boundary=clean(a.boundary,"boundary"); losses=many(a.loss,"loss",1,12); hazards=many(a.hazard,"hazard",1,20); controllers=many(a.controller,"controller",1,20); actions=many(a.control_action,"control-action",1,20); feedback=many(a.feedback,"feedback",1,20)
 high=a.risk_level=="high" or a.domain in HIGH
 gates={k:opt(getattr(a,k),k.replace("_","-")) for k in ["accountable_owner","applicable_rule","affected_group","real_impact_evidence","independent_review","appeal_path","rollback_trigger","stop_condition"]}
 if high:
  missing=["--"+k.replace("_","-") for k,v in gates.items() if v is None]
  if missing: raise ValueError("high-risk safety audit requires "+", ".join(missing))
 ucas=[]
 for ca in actions:
  for kind in ["not-provided-when-required","provided-when-unsafe","wrong-timing-or-order","wrong-duration"]:
   ucas.append({"control_action":ca,"type":kind,"unsafe_context":"TODO","hazard_links":[],"controller_constraint":"TODO","status":"candidate_not_validated"})
 return {"schema_version":SCHEMA_VERSION,"generator":GENERATOR,"workflow":{"name":"CONTROL","created_by_skill":True,"steps":["Consequences","Operational boundary","Name hazards","Trace control structure","Requirements","Observe unsafe actions","Learn in operation"],"claim_id":"ESW025"},"epistemic_contract":{"status":"hazard_analysis_not_safety_certification","safety_not_reliability":True,"no_completeness_guarantee":True,"prohibited_inference":"Component reliability, a completed worksheet, or an absence of found scenarios does not prove system safety."},"scope":{"system":system,"boundary":boundary,"external_environment":"TODO","losses":[{"id":f"L-{i+1}","text":x} for i,x in enumerate(losses)],"hazards":[{"id":f"H-{i+1}","state":x,"loss_links":[],"system_constraint":"TODO"} for i,x in enumerate(hazards)]},"control_structure":{"controllers":[{"name":x,"authority":"TODO","responsibility":"TODO","process_model":"TODO"} for x in controllers],"control_actions":actions,"feedback":feedback,"missing_feedback_check":"TODO","coordination_check":"TODO","development_operation_interfaces":"TODO"},"unsafe_control_actions":ucas,"loss_scenarios":[{"uca_id":"TODO","controller_or_path":"TODO","process_model_flaw":"TODO","feedback_or_delay":"TODO","organizational_pressure":"TODO","environmental_condition":"TODO","hazard":"TODO","constraint_and_verification":"TODO"}],"operations":{"leading_indicators":[],"migration_toward_risk":"TODO","change_control":"TODO","incident_path":"TODO","CAST_required_after_loss":True},"safety_gate":{"high_risk":high,"domain":a.domain,"risk_level":a.risk_level,"status":"governance_review_required" if high else "analysis_only","submitted_not_verified":gates,"release_rule":"STPA output must be independently challenged, verified in design/test/operation, owned, stoppable, and never treated as certification."},"provenance":PROVENANCE,"claim_map":"references/claim-layer-map.md","source_ledger":"references/source-notes.md"}
def esc(v:object)->str:return html.escape(str(v),quote=False).replace("\\","\\\\").replace("|","\\|")
def md(d:dict[str,Any])->str:
 s=d["scope"];g=d["safety_gate"]; lines=["# CONTROL 系统安全审计","",f"- 系统：{esc(s['system'])}",f"- 边界：{esc(s['boundary'])}",f"- 状态：`{d['epistemic_contract']['status']}` / `{g['status']}`","","> 本输出是候选危险与约束的分析脚手架，不是完整性证明、风险量化、认证或部署批准。","","## 损失—危险—约束","","| ID | 项目 | 链接/约束 |","|---|---|---|"]
 for x in s["losses"]: lines.append(f"| {x['id']} | {esc(x['text'])} | TODO |")
 for x in s["hazards"]: lines.append(f"| {x['id']} | {esc(x['state'])} | TODO |")
 lines += ["","## 控制结构","",f"- Controllers：{esc('；'.join(x['name'] for x in d['control_structure']['controllers']))}",f"- Control actions：{esc('；'.join(d['control_structure']['control_actions']))}",f"- Feedback：{esc('；'.join(d['control_structure']['feedback']))}","","## 四类 UCA 候选","","| Control action | 类型 | 危险情境 | Hazard | Constraint |","|---|---|---|---|---|"]
 lines += [f"| {esc(x['control_action'])} | `{x['type']}` | TODO | TODO | TODO |" for x in d["unsafe_control_actions"]]
 lines += ["","## Loss scenario / 运行控制","","- 控制算法、过程模型、反馈/延迟、执行路径、协调、组织压力、环境扰动：TODO","- 领先指标、风险迁移、变更控制、事故 CAST：TODO","","## 发布门","",f"- 提交但未核验：{esc(json.dumps(g['submitted_not_verified'],ensure_ascii=False,sort_keys=True))}",f"- 规则：{esc(g['release_rule'])}","","## Provenance","","| 层 | Claims | Sources |","|---|---|---|"]+[f"| {x['layer']} | {esc(', '.join(x['claim_ids']))} | {esc(', '.join(x['source_ids']))} |" for x in d["provenance"]]
 return "\n".join(lines)+"\n"
def parser()->argparse.ArgumentParser:
 p=argparse.ArgumentParser(description="Generate a STAMP/STPA safety control audit scaffold.")
 p.add_argument("--system",required=True);p.add_argument("--boundary",required=True)
 for x in ["loss","hazard","controller","control-action","feedback"]:p.add_argument("--"+x,action="append",required=True,dest=x.replace("-","_"))
 p.add_argument("--domain",default="engineering",choices=["engineering","business","personnel","labor","healthcare","education","credit","law-enforcement","content-governance"]);p.add_argument("--risk-level",choices=["low","moderate","high"],default="moderate")
 for x in ["accountable-owner","applicable-rule","affected-group","real-impact-evidence","independent-review","appeal-path","rollback-trigger","stop-condition"]:p.add_argument("--"+x,dest=x.replace("-","_"))
 p.add_argument("--format",choices=["json","markdown"],default="markdown");p.add_argument("--output");return p
def main(argv:list[str]|None=None)->int:
 try:
  a=parser().parse_args(argv);d=build(a);text=json.dumps(d,ensure_ascii=False,indent=2,sort_keys=True)+"\n" if a.format=="json" else md(d)
  if a.output:o=Path(a.output);o.parent.mkdir(parents=True,exist_ok=True);o.write_text(text,encoding="utf-8")
  else:sys.stdout.write(text)
  return 0
 except (ValueError,OSError) as e:print(f"ERROR: {e}",file=sys.stderr);return 2
if __name__=="__main__":raise SystemExit(main())
