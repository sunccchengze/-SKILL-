#!/usr/bin/env python3
"""Create a deterministic contextual-integrity information-flow audit."""
from __future__ import annotations
import argparse, html, json, sys
from pathlib import Path
from typing import Any
SCHEMA_VERSION="1.0";GENERATOR="book-privacy-context-flow-audit/audit_contextual_flow.py";HIGH={"personnel","labor","healthcare","education","credit","law-enforcement","content-governance"}
PROVENANCE=[{"claim_ids":["PIC001","PIC004","PIC006","PIC008","PIC010"],"layer":"A","source_ids":["PIC-01","PIC-02","PIC-03"],"use":"contextual integrity, five parameters, norms, heuristic"},{"claim_ids":["PIC019","PIC020","PIC021"],"layer":"C","source_ids":["PIC-08","PIC-09","PIC-10"],"use":"formalization, empirical operationalization, and vulnerability critique"},{"claim_ids":["PIC025","PIC026","PIC027","PIC028"],"layer":"D","source_ids":["D1"],"use":"FLOW workflow and release gates"}]
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
 context=clean(a.context,"context");purpose=clean(a.context_purpose,"context-purpose");subjects=many(a.subject,"subject",1,12);senders=many(a.sender,"sender",1,12);recipients=many(a.recipient,"recipient",1,20);attributes=many(a.attribute,"attribute",1,24);principles=many(a.transmission_principle,"transmission-principle",1,20);norm=clean(a.baseline_norm,"baseline-norm");change=clean(a.proposed_change,"proposed-change");evidence=many(a.norm_evidence,"norm-evidence",1,20)
 high=a.risk_level=="high" or a.domain in HIGH
 gates={k:opt(getattr(a,k),k.replace("_","-")) for k in ["accountable_owner","applicable_rule","affected_group","impact_evidence","contest_path","rollback_trigger","stop_condition"]}
 if high:
  miss=["--"+k.replace("_","-") for k,v in gates.items() if v is None]
  if miss:raise ValueError("high-risk contextual-flow audit requires "+", ".join(miss))
 return {"schema_version":SCHEMA_VERSION,"generator":GENERATOR,"workflow":{"name":"FLOW","created_by_skill":True,"steps":["Frame social context","List five-parameter flows","Observe entrenched norms","Weigh legitimacy and controls"],"claim_id":"PIC025"},"epistemic_contract":{"status":"prima_facie_privacy_audit_not_legal_approval","security_is_not_privacy":True,"public_is_not_unrestricted":True,"consent_is_one_transmission_principle":True,"prohibited_inference":"Observed expectations do not automatically make a norm legitimate, and a signed notice does not automatically make a flow appropriate."},"context":{"name":context,"purpose":purpose,"values_ends":"TODO","nested_or_competing_contexts":"TODO"},"baseline_flow":{"subjects":subjects,"senders":senders,"recipients":recipients,"attributes":attributes,"transmission_principles":principles,"norm":norm,"norm_evidence":evidence},"proposed_practice":{"description":change,"derived_or_inferred_attributes":"TODO","downstream_recipients":"TODO","retention_and_linkage":"TODO","automated_decision_use":"TODO"},"parameter_delta":{"subject":"TODO changed/unchanged","sender":"TODO changed/unchanged","recipient":"TODO changed/unchanged","attribute":"TODO changed/unchanged","transmission_principle":"TODO changed/unchanged","scale_persistence_and_searchability":"TODO"},"decision_heuristic":{"steps_1_5_descriptive":{"practice":"recorded","context":"recorded","actors":"recorded","attributes_and_transmission_principles":"recorded","entrenched_norm_and_departures":"candidate_not_validated"},"step_6_prima_facie":"TODO: conforming / departure / contested / unknown","step_7_moral_political_factors":"TODO: power, autonomy, justice, rights, harms, benefits","step_8_contextual_values_ends":"TODO: supports or undermines context purposes and roles","step_9_recommendation":"TODO: allow / modify / pause / reject, with reasons"},"controls":{"recipient_limitation":"TODO","attribute_minimization":"TODO","purpose_and_use_binding":"TODO","retention_deletion":"TODO","access_and_audit_log":"TODO","inference_control":"TODO","notification_and_contestation":"TODO","vendor_and_model_flow_contract":"TODO"},"vulnerability_checks":{"missing_voice":"TODO","coerced_or_resigned_consent":"TODO","unequal_impact":"TODO","norm_set_by_dominant_actor":"TODO","multi_subject_or_group_privacy":"TODO"},"safety_gate":{"high_risk":high,"domain":a.domain,"risk_level":a.risk_level,"status":"governance_review_required" if high else "privacy_review_required","submitted_not_verified":gates,"release_rule":"A flow audit cannot waive law, rights, security, DPIA, procurement, affected-person participation, or independent review."},"provenance":PROVENANCE,"claim_map":"references/claim-layer-map.md","source_ledger":"references/source-notes.md"}
def esc(v:object)->str:return html.escape(str(v),quote=False).replace("\\","\\\\").replace("|","\\|")
def md(d:dict[str,Any])->str:
 b=d["baseline_flow"];g=d["safety_gate"];c=d["context"];lines=["# FLOW 情境完整性审计","",f"- 社会情境 / 目的：{esc(c['name'])} / {esc(c['purpose'])}",f"- 状态：`{d['epistemic_contract']['status']}` / `{g['status']}`","","> 安全、保密、同意或“公开可见”都不自动等于情境适当；本输出不是法律或部署批准。","","## 基线五参数信息流","","| Subject | Sender | Recipient | Attribute | Transmission principle |","|---|---|---|---|---|",f"| {esc('；'.join(b['subjects']))} | {esc('；'.join(b['senders']))} | {esc('；'.join(b['recipients']))} | {esc('；'.join(b['attributes']))} | {esc('；'.join(b['transmission_principles']))} |",f"- 基线规范：{esc(b['norm'])}",f"- 规范证据：{esc('；'.join(b['norm_evidence']))}","","## 新实践与参数差异","",f"- 实践：{esc(d['proposed_practice']['description'])}","- subject / sender / recipient / attribute / transmission principle：TODO changed/unchanged","- 推断属性、下游接收者、留存/链接、自动决定用途、规模/持久/可搜索性：TODO","","## 九步启发式的判断段","","1–5. 描述实践、情境、角色、属性/传输原则、规范与偏离：已建候选，需核验","6. Prima facie violation：TODO","7. 道德政治因素（权力、自治、正义、权利、伤害、收益）：TODO","8. 对情境价值/目的/角色的影响：TODO","9. allow / modify / pause / reject：TODO","","## 控制与脆弱性","","- 限定 recipient/attribute/purpose/retention；日志；推断控制；通知/争议；供应商/模型流合同：TODO","- 缺席声音、被迫/放弃式同意、差异影响、强者定规范、多主体/群体隐私：TODO","","## 发布门","",f"- 提交但未核验：{esc(json.dumps(g['submitted_not_verified'],ensure_ascii=False,sort_keys=True))}",f"- 规则：{esc(g['release_rule'])}","","## Provenance","","| 层 | Claims | Sources |","|---|---|---|"]+[f"| {x['layer']} | {esc(', '.join(x['claim_ids']))} | {esc(', '.join(x['source_ids']))} |" for x in d["provenance"]]
 return "\n".join(lines)+"\n"
def parser()->argparse.ArgumentParser:
 p=argparse.ArgumentParser(description="Generate a contextual-integrity information-flow audit.")
 p.add_argument("--context",required=True);p.add_argument("--context-purpose",required=True)
 for x in ["subject","sender","recipient","attribute","transmission-principle","norm-evidence"]:p.add_argument("--"+x,action="append",required=True,dest=x.replace("-","_"))
 p.add_argument("--baseline-norm",required=True);p.add_argument("--proposed-change",required=True)
 p.add_argument("--domain",default="general",choices=["general","personnel","labor","healthcare","education","credit","law-enforcement","content-governance"]);p.add_argument("--risk-level",choices=["low","moderate","high"],default="moderate")
 for x in ["accountable-owner","applicable-rule","affected-group","impact-evidence","contest-path","rollback-trigger","stop-condition"]:p.add_argument("--"+x,dest=x.replace("-","_"))
 p.add_argument("--format",choices=["json","markdown"],default="markdown");p.add_argument("--output");return p
def main(argv:list[str]|None=None)->int:
 try:
  a=parser().parse_args(argv);d=build(a);text=json.dumps(d,ensure_ascii=False,indent=2,sort_keys=True)+"\n" if a.format=="json" else md(d)
  if a.output:o=Path(a.output);o.parent.mkdir(parents=True,exist_ok=True);o.write_text(text,encoding="utf-8")
  else:sys.stdout.write(text)
  return 0
 except (ValueError,OSError) as e:print(f"ERROR: {e}",file=sys.stderr);return 2
if __name__=="__main__":raise SystemExit(main())
