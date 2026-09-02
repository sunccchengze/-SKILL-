# Templates — CONSTRAIN-ACT

形式属性、实际伤害、制度权利分账。模板完整只表示可审查，不表示 ethical/legal/deployment approval。每张卡需 source、owner、stop 和 decision。

## 1. Decision Context 与 Authority Card

```yaml
audit_id:
system_and_version:
decision:
purpose_and_non_purpose:
stakes: low | medium | high
owner:
legal_or_institutional_authority:
lifecycle_stage:
non_automated_alternative:
who_can_refuse:
review_date:
source_ids: []
unknowns: []
stop_if: [purpose illegitimate, authority missing, no accountable owner]
decision:
```

先判断“是否应做这个决定”，再判断如何优化；合法 authority 与伦理正当性分开记录。

## 2. Affected Parties、Rights 与 Harm Pathway

```yaml
parties:
  - group:
    role: decision-subject | data-subject | non-user | worker | proxy | future-group
    representation_or_absence:
    real_exit:
    rights_at_stake: []
harms:
  - harm:
    causal_pathway:
    severity_and_reversibility:
    numerator_denominator:
    evidence_and_source:
    uncertainty:
    cannot_be_offset_by: []
owner:
remedy_required:
stop_condition:
decision:
```

不要把所有伤害乘权重压成一个总 utility；保留不可抵消权利和 minority report。

## 3. Formal Property Translation Card

```yaml
value_or_right:
formal_property:
object_and_unit:
population_and_time_window:
label_or_outcome:
metric_or_guarantee:
threshold_or_budget:
assumptions:
proof_or_test_method:
what_translation_preserves:
what_translation_loses:
who_selected_it:
dissent_and_alternatives:
source_ids: []
owner:
stop_if: [object undefined, translation loss unacceptable]
decision:
```

技术团队不能隐式拥有规范选择权；每项 property 都要有受影响人可争辩的翻译记录。

## 4. Differential Privacy Release Ledger

```yaml
privacy_unit:
neighboring_relation:
central_or_local_model:
mechanism_and_version:
epsilon:
delta:
sensitivity_or_clipping:
releases:
  - release_id:
    query_or_artifact:
    budget_spent:
    date:
    recipient:
composition_accountant:
post_processing_boundary:
auxiliary_information_review:
non_dp_controls: [security, access, consent, purpose-limitation, deletion]
population_or_group_inference_limit:
owner:
source_ids: []
stop_if: [unit missing, composition unknown, budget exceeded]
decision:
```

epsilon 不可脱离 neighbor、delta、composition 和任务解释；DP 不替代数据库安全或 context/consent。

## 5. Fairness、Impossibility 与 Subgroup Audit

```yaml
harm_to_metric_mapping:
protected_and_intersectional_groups: []
label_validity_and_history:
base_rates_by_group: []
goals: [demographic-parity, equalized-odds, calibration, individual, subgroup]
metric_definitions_and_denominators:
coverage_and_abstention:
uncertainty_and_sample_size:
incompatibility_result:
perfect_or_degenerate_exception_applicable:
subgroup_search_class:
multiplicity_and_privacy:
tradeoff_decision_authority:
dissent:
remedy:
owner:
source_ids: []
stop_if: [groups absent, label invalid, conflict hidden]
decision: BLOCKED_CONSTRAINT_SPECIFICATION | TRADEOFF_DECISION_REQUIRED | REVIEW
```

“公平不可能”不是结论；写清哪些定义为何冲突、谁有权选择、真实 harm 和补救如何变化。

## 6. Strategic / Performative Response Map

```yaml
score_or_decision_visible_to:
actions_available_by_actor:
  - actor:
    action:
    information_available:
    private_cost:
    structural_constraint:
    desirable_adaptation_or_harmful_gaming:
institutional_response:
prediction_to_decision_to_new_data_chain:
response_model_assumptions:
feedback_monitors: []
lag_and_threshold:
causal_or_counterfactual_evaluation:
owner:
source_ids: []
stop_if: [high-impact response unmodeled, harm shifts to constrained group]
decision:
```

不要把受影响人的合理努力、规避不公或抗议都写成 gaming；机构也会策略性改规则。

## 7. Adaptive Validity 与 Holdout Query Ledger

```yaml
training_and_tuning_data:
holdout_or_lockbox:
queries:
  - query_id:
    requester:
    statistic_or_feedback:
    answer_precision:
    how_answer_changed_next_version:
    date:
reusable_mechanism_and_assumptions:
query_budget:
fresh_external_replication:
distribution_drift_monitor:
owner:
source_ids: []
stop_if: [unlogged query, budget exceeded, holdout becomes training signal]
decision:
```

dashboard、错误切片和人类查看结果都可能构成 adaptive feedback；可复用机制不是无限验证。

## 8. Interpretability、Due Process 与 Final Decision

```yaml
audiences:
  - role: affected-person | operator | auditor | regulator
    question_they_need_answered:
    explanation_method:
    fidelity_test:
    stability_test:
    comprehension_test:
    actionability_and_contest:
notice:
appeal_path_and_deadline:
human_review_authority:
correction_and_audit_trail:
residual_institutional_risks: []
minority_report:
remedy_budget_and_owner:
stop_and_rollback: []
review_date:
source_ids: []
decision: BLOCKED_CONSTRAINT_SPECIFICATION | TRADEOFF_DECISION_REQUIRED | GOVERNANCE_REVIEW_REQUIRED
```

post-hoc 图不是正当程序。最终决议须写形式保证“不涵盖什么”，且不存在自动 `ETHICAL` 或 `APPROVED` 状态。
