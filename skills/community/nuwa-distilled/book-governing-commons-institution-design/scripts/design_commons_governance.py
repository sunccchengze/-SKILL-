#!/usr/bin/env python3
"""Create a deterministic common-pool resource institutional diagnosis."""
from __future__ import annotations
import argparse, html, json, sys
from pathlib import Path
from typing import Any
SCHEMA_VERSION="1.0";GENERATOR="book-governing-commons-institution-design/design_commons_governance.py";HIGH={"personnel","labor","healthcare","education","credit","law-enforcement","content-governance"}
PRINCIPLES=["resource-and-user-boundaries","rules-fit-local-conditions-and-proportionality","affected-users-can-modify-operational-rules","monitors-accountable-to-users","graduated-sanctions","low-cost-conflict-resolution","external-recognition-of-right-to-organize","nested-enterprises-for-larger-systems"]
PROVENANCE=[{"claim_ids":["GTC001","GTC004","GTC006","GTC008","GTC010"],"layer":"A","source_ids":["GTC-01","GTC-02"],"use":"CPR problem, institutional diversity, and design principles"},{"claim_ids":["GTC019","GTC020","GTC021"],"layer":"C","source_ids":["GTC-07","GTC-08","GTC-09"],"use":"meta-analysis, scale, power, and digital transfer limits"},{"claim_ids":["GTC025","GTC026","GTC027","GTC028"],"layer":"D","source_ids":["D1"],"use":"COMMONS workflow and legitimacy gates"}]
def clean(v:str,f:str)->str:
 o=" ".join(v.split());
 if not o:raise ValueError(f"{f} must not be blank")
 return o
def many(v:list[str]|None,f:str,lo:int=0,hi:int=24)->list[str]:
 o=[clean(x,f) for x in (v or [])]
 if len(o)<lo:raise ValueError(f"{f} requires at least {lo} value(s)")
 if len(o)>hi:raise ValueError(f"{f} accepts at most {hi} value(s)")
 if len({x.casefold() for x in o})!=len(o):raise ValueError(f"{f} must not contain duplicate values")
 return o
def opt(v:str|None,f:str)->str|None:return clean(v,f) if v is not None else None
def build(a:argparse.Namespace)->dict[str,Any]:
 resource=clean(a.resource,"resource");unit=clean(a.resource_unit,"resource-unit");boundary=clean(a.boundary,"boundary");users=many(a.user_group,"user-group",1,16);rules=many(a.rule,"rule",1,20);monitor=clean(a.monitor,"monitor");conflict=clean(a.conflict_path,"conflict-path")
 high=a.risk_level=="high" or a.domain in HIGH
 gates={k:opt(getattr(a,k),k.replace("_","-")) for k in ["accountable_owner","applicable_rule","affected_group","legitimacy_evidence","appeal_path","rollback_trigger","stop_condition"]}
 if high:
  miss=["--"+k.replace("_","-") for k,v in gates.items() if v is None]
  if miss:raise ValueError("high-risk commons design requires "+", ".join(miss))
 return {"schema_version":SCHEMA_VERSION,"generator":GENERATOR,"workflow":{"name":"COMMONS","created_by_skill":True,"steps":["Characterize resource","Outline boundaries","Map rules-in-use","Monitor reciprocity","Organize collective choice","Navigate conflict","Scale by nesting"],"claim_id":"GTC025"},"epistemic_contract":{"status":"institutional_diagnosis_not_governance_legitimacy","design_principles_are_diagnostics_not_recipe":True,"prohibited_inference":"Open access is not common property; presence of eight labels neither proves durability nor justice."},"resource_system":{"resource":resource,"resource_units":unit,"subtractability":"TODO","cost_of_exclusion":"TODO","ecological_or_technical_dynamics":"TODO","boundary":boundary,"scale":"TODO","externalities":"TODO"},"participants":{"user_groups":users,"appropriators":"TODO","providers":"TODO","affected_nonusers":"TODO","rights_holders":"TODO","power_and_exclusion":"TODO"},"rules_in_use":[{"rule":x,"level":"operational/collective-choice/constitutional TODO","position":"TODO","action":"TODO","condition":"TODO","information":"TODO","payoff_or_sanction":"TODO","observed_or_formal":"TODO"} for x in rules],"collective_action":{"free_riding":"TODO","commitment":"TODO","institution_supply":"TODO","monitoring_cost":"TODO","trust_and_reciprocity":"TODO"},"principle_diagnostics":[{"principle":x,"evidence_for":"TODO","evidence_against":"TODO","mechanism":"TODO","failure_mode":"TODO","local_adaptation":"TODO"} for x in PRINCIPLES],"monitoring":{"monitor":monitor,"accountable_to":"TODO","resource_monitoring":"TODO","user_monitoring":"TODO","data_contestability":"TODO"},"enforcement":{"graduated_sanction_ladder":[],"due_process":"TODO","conflict_path":conflict,"low_cost_and_accessible":"TODO"},"polycentricity":{"external_recognition":"TODO","horizontal_coordination":"TODO","nested_levels":"TODO","cross_scale_feedback":"TODO"},"justice_checks":{"who_is_excluded":"TODO","distribution_of_benefits_and_burdens":"TODO","elite_capture":"TODO","coercion_mistaken_for_cooperation":"TODO","historical_and_legal_context":"TODO"},"safety_gate":{"high_risk":high,"domain":a.domain,"risk_level":a.risk_level,"status":"governance_review_required" if high else "diagnosis_only","submitted_not_verified":gates,"release_rule":"No institution is legitimate because a template is complete; affected people, law, evidence, due process, and revision remain required."},"provenance":PROVENANCE,"claim_map":"references/claim-layer-map.md","source_ledger":"references/source-notes.md"}
def esc(v:object)->str:return html.escape(str(v),quote=False).replace("\\","\\\\").replace("|","\\|")
def md(d:dict[str,Any])->str:
 r=d["resource_system"];g=d["safety_gate"];lines=["# COMMONS 制度诊断","",f"- 资源系统：{esc(r['resource'])}",f"- 资源单位：{esc(r['resource_units'])}",f"- 边界：{esc(r['boundary'])}",f"- 状态：`{d['epistemic_contract']['status']}` / `{g['status']}`","","> 这是制度诊断，不是八项打勾即成功、正义或合法的证明。开放获取不等于共同财产制度。","","## 资源—参与者—规则","",f"- 用户群：{esc('；'.join(d['participants']['user_groups']))}","- 排他成本 / 减损性 / 外部性 / 受影响非用户 / 权力：TODO","","| Rules-in-use | 层级 | 条件/行动 | 信息 | 后果 |","|---|---|---|---|---|"]
 lines += [f"| {esc(x['rule'])} | TODO | TODO | TODO | TODO |" for x in d["rules_in_use"]]
 lines += ["","## 八项原则：机制诊断，不是配方","","| 原则 | 支持证据 | 反证 | 机制 | 失效/本地适配 |","|---|---|---|---|---|"]+[f"| `{x['principle']}` | TODO | TODO | TODO | TODO |" for x in d["principle_diagnostics"]]
 lines += ["","## 监督—制裁—冲突—嵌套","",f"- Monitor：{esc(d['monitoring']['monitor'])}",f"- Conflict path：{esc(d['enforcement']['conflict_path'])}","- 问责对象、监测数据可争议性、渐进制裁与正当程序：TODO","- 外部承认、横向协调、多层嵌套、跨尺度反馈：TODO","","## 权力与正义反证","","- 排除谁、收益/负担给谁、精英俘获、把强迫误作合作、历史/法律背景：TODO","","## 发布门","",f"- 提交但未核验：{esc(json.dumps(g['submitted_not_verified'],ensure_ascii=False,sort_keys=True))}",f"- 规则：{esc(g['release_rule'])}","","## Provenance","","| 层 | Claims | Sources |","|---|---|---|"]+[f"| {x['layer']} | {esc(', '.join(x['claim_ids']))} | {esc(', '.join(x['source_ids']))} |" for x in d["provenance"]]
 return "\n".join(lines)+"\n"
def parser()->argparse.ArgumentParser:
 p=argparse.ArgumentParser(description="Generate a common-pool-resource institutional diagnosis.")
 for x in ["resource","resource-unit","boundary","monitor","conflict-path"]:p.add_argument("--"+x,required=True,dest=x.replace("-","_"))
 p.add_argument("--user-group",action="append",required=True);p.add_argument("--rule",action="append",required=True)
 p.add_argument("--domain",default="natural-resource",choices=["natural-resource","digital","business","personnel","labor","healthcare","education","credit","law-enforcement","content-governance"]);p.add_argument("--risk-level",choices=["low","moderate","high"],default="moderate")
 for x in ["accountable-owner","applicable-rule","affected-group","legitimacy-evidence","appeal-path","rollback-trigger","stop-condition"]:p.add_argument("--"+x,dest=x.replace("-","_"))
 p.add_argument("--format",choices=["json","markdown"],default="markdown");p.add_argument("--output");return p
def main(argv:list[str]|None=None)->int:
 try:
  a=parser().parse_args(argv);d=build(a);text=json.dumps(d,ensure_ascii=False,indent=2,sort_keys=True)+"\n" if a.format=="json" else md(d)
  if a.output:o=Path(a.output);o.parent.mkdir(parents=True,exist_ok=True);o.write_text(text,encoding="utf-8")
  else:sys.stdout.write(text)
  return 0
 except (ValueError,OSError) as e:print(f"ERROR: {e}",file=sys.stderr);return 2
if __name__=="__main__":raise SystemExit(main())
