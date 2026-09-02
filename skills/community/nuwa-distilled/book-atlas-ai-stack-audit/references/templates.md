# Templates — ATLAS-STACK

先定义边界，再收证据。每项填写 source owner、geography、date、denominator、uncertainty；`unknown` 不能写成 zero。任何访谈/社群材料需同意、数据最小化和反报复安排。

## 1. Purpose、Affected Parties 与 Boundary Card

```yaml
audit_id:
system_and_version:
purpose_and_non_purpose:
lifecycle_stage:
decision_owner:
decision_to_make:
non_ai_alternative:
affected_and_absent_groups: []
geography:
as_of_date:
organizational_boundary:
lifecycle_boundary:
cut_off_rules:
claim_denominator:
known_unknowns: []
source_ids: []
stop_if: [purpose drifts, owner absent, boundary cannot be stated]
decision:
```

同一系统换用途/地点/人群后重开 audit；“AI platform”不是足够具体的审计对象。

## 2. Space 与 Supply-Chain Node Register

```yaml
nodes:
  - node_id:
    function: extraction | manufacture | data | annotation | compute | integration | deployment | maintenance | disposal
    organization:
    geography:
    contractual_tier:
    material_or_data_flow:
    workers:
    source:
    evidence_state: documented | corroborated | reported | estimated | unknown
    uncertainty:
    audit_access:
undocumented_components: []
owner:
stop_condition: [critical third party untraceable]
decision: BLOCKED_PROVENANCE | MAP_INCOMPLETE | CONTINUE
```

供应商列表不是 value chain；要标合同层、数据/物质流、谁可审计及处置节点。

## 3. Earth / Environmental Claim Card

```yaml
claim:
metric: energy | emissions | water-withdrawal | water-consumption | mineral | land | e-waste
value_and_unit:
source_owner:
source_record:
facility_or_system:
geography:
period:
scope_and_lifecycle:
denominator:
allocation_method:
energy_or_water_context:
uncertainty_interval_or_scenarios:
excluded_processes: []
community_distribution_effects: []
independent_check:
stop_if: [denominator absent, allocation unsupported]
decision: NOT_COMPARABLE | ESTIMATE_WITH_LIMITS | WITHDRAW_CLAIM
```

禁止把 company/facility total 直接除以 prompt/model/user；若只知总量，就以总量边界报告。

## 4. Labor Chain 与 Worker Voice Protocol

```yaml
worker_groups:
  - role:
    employer_and_contract_tier:
    geography:
    employment_status:
    pay_hours_and_targets:
    health_and_safety:
    surveillance_or_algorithmic_management:
    intellectual_property_or_content_exposure:
    grievance_and_organizing:
    evidence_sources: []
worker_voice_method:
consent_and_translation:
anti_retaliation:
secure_data_retention:
independent_worker_or_union_partner:
owner:
stop_if: [unsafe participation, worker voice absent, remedy unavailable]
decision:
```

vendor policy 只能是一项来源；“无投诉”不能证明无伤害。不得为审计再次提取创伤叙述。

## 5. Dataset Provenance 与 Authority Card

```yaml
dataset_or_source:
version_and_date:
motivation_and_creator:
composition_and_absences:
collection_context:
permission_legal_basis_and_dispute:
collective_or_indigenous_authority:
preprocessing_and_labels:
recommended_uses:
prohibited_or_unsupported_uses:
distribution_and_access:
maintenance_deletion_withdrawal:
known_bias_measurement_limits:
source_ids: []
owner:
stop_if: [lineage missing, authority unresolved, withdrawal impossible]
decision: BLOCKED_PROVENANCE | RESTRICT_USE | REVIEW
```

`publicly accessible` 不等于授权、同意或 context-preserving use；尤其区分个人 consent 与 collective authority。

## 6. Classification、Affect 与 Disparity Audit

```yaml
classification_or_construct:
who_defined_and_when:
social_history_and_contestation:
ground_truth_process:
reliability:
construct_validity:
context_and_culture:
deployment_population:
groups_and_denominators: []
false_positive_harms: []
false_negative_harms: []
intersectional_uncertainty:
threshold_and_abstention:
contest_and_correction:
source_ids: []
owner:
stop_if: [affect construct unsupported, high-risk disparity, category cannot be contested]
decision:
```

平均 accuracy 不得掩盖最坏群体、coverage 或 abstention。脸部动作不是内在情绪的普遍直接读数。

## 7. State、Procurement 与 Power Matrix

```yaml
public_authority_or_state_link:
statutory_or_contractual_authority:
procurement_path:
vendors_and_subprocessors: []
data_sharing_and_retention:
surveillance_or_enforcement_use:
secrecy_and_audit_exceptions:
rights_notice_and_due_process:
power_matrix:
  - actor:
    can_set_purpose:
    can_change_threshold:
    can_access_evidence:
    can_refuse:
    can_stop:
    bears_cost:
    receives_benefit:
source_ids: []
owner:
stop_if: [authority unclear, vendor secrecy defeats contest]
decision:
```

公共部门不是普通客户；保密条款不能自动胜过受影响人的 contestability 与公共问责。

## 8. Remedy、Refusal 与 Final Decision Record

```yaml
notices:
appeal_route_and_deadline:
human_review_authority:
correction_deletion_or_withdrawal:
worker_and_community_voice:
compensation_or_restoration:
independent_audit_access:
stop_pause_and_exit_power:
remedy_budget_and_owner:
non_ai_alternative:
unresolved_unknowns: []
minority_report:
source_ids: []
review_date:
retirement_and_disposal_duties:
stop_conditions: []
decision: BLOCKED_SCIENTIFIC_VALIDITY_REVIEW | BLOCKED_RIGHTS_REVIEW | BLOCKED_PROVENANCE | INCOMPLETE_STACK_MAP | GOVERNANCE_REVIEW_REQUIRED
```

不存在 `APPROVED`。决议说明谁不同意、成本如何分配、何时停止及退役后如何处理数据/硬件。
