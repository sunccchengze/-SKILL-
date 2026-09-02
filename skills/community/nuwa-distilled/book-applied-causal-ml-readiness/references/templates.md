# Templates — IDENTIFY-DML

复制后填写；`unknown` 不是空白的委婉说法。每份产物都需 owner、source/证据、反证、stop 与 decision。触发阻断时保留记录，不删行“过关”。

## 1. 决策与 Estimand Card

```yaml
analysis_id:
version_as_of:
decision_owner:
decision_to_inform:
why_causal_not_predictive:
no_estimate_alternative:
population:
unit:
treatment_versions:
comparator:
outcome_definition:
time_zero:
follow_up_horizon:
estimand: ATE | ATT | CATE | policy-value
aggregation_and_scale:
interference_unit:
source_ids: []
unknowns: []
stop_if: [treatment versions conflict, time zero cannot be aligned]
decision: BLOCKED_DESIGN | CONTINUE_TO_IDENTIFICATION
```

检查：结果是否可能受处理定义改变？同一“处理”是否含多版本？目标是 sample 还是 target population？若改人群/时间窗，必须新建版本。

## 2. 时间线、DAG 与变量角色表

```yaml
variables:
  - name:
    measured_at:
    role_proposed: baseline-confounder | instrument | mediator | outcome | collider | selection | proxy
    causal_rationale:
    source_or_domain_owner:
    alternative_role:
    measurement_error:
    included_in_adjustment: yes | no | disputed
post_treatment_controls: []
selection_into_dataset:
anticipation_or_spillover:
reviewers: []
stop_if: [declared control occurs after treatment, role dispute unresolved]
decision:
```

不要从 feature importance 自动定箭头。DAG 是待争辩模型；提交至少一个替代图及它会改变的 adjustment/estimand。

## 3. Identification Argument Table

```yaml
design: randomized | observational | natural-experiment
assumptions:
  - name: exchangeability | exclusion | consistency | positivity | no-interference | other
    precise_statement:
    why_needed:
    evidence_for:
    evidence_against:
    empirically_checkable_part:
    untestable_part:
    owner:
    failure_consequence:
    redesign_option:
identification_formula_or_logic:
source_ids: []
stop_condition:
decision: BLOCKED_UNIDENTIFIED_CONFOUNDING | PROVISIONAL_ARGUMENT
```

“控制了很多变量”不是 argument；“随机”要有分配与执行记录；工具变量要列 exclusion/monotonicity 等具体前提。

## 4. Overlap 与支持域报告

```yaml
estimand_before_check:
propensity_or_support_method:
outcome_blind_protocol:
strata_and_denominators: []
extreme_region_definition:
weight_distribution:
groups_with_no_support: []
proposed_action: collect-data | restrict-population | trim | no-estimate
estimand_after_action:
people_excluded_and_equity_effect:
uncertainty:
source_artifacts: []
owner:
stop_if:
decision:
```

修剪后不得继续写原总体 ATE；写新 population、coverage 与被排除群体。默认 clipping 不是理由。

## 5. Split Manifest 与 Nuisance Scorecard

```yaml
random_seed:
fold_count:
unit_or_cluster_kept_together:
time_or_site_constraints:
hyperparameter_tuning_domain:
features_frozen_at:
leakage_checks: []
nuisance_models:
  - task: outcome | propensity | instrument
    learner_and_version:
    out_of_fold_metrics:
    calibration:
    failure_slices:
    alternative_learner:
score_function:
cross_fit_repetitions:
owner:
stop_if: [target-fold leakage, no out-of-fold evaluation]
decision:
```

最终 effect estimate 好看不能覆盖 nuisance/overlap 失败。模型复杂度要与样本、支持和复现成本一起决定。

## 6. Estimator 与 Robustness Matrix

```yaml
primary_estimator:
score_and_software_version:
standard_error_and_cluster:
baseline_estimator:
checks:
  - check: alternative-adjustment | learner | split | trim | placebo | negative-control | sensitivity | attrition
    claim_tested:
    preregistered_threshold:
    result:
    interpretation:
    conclusion_change:
source_ids: []
unresolved_threats: []
owner:
stop_or_downgrade_if:
decision:
```

statistical interval 与 identification uncertainty 分开。未做的检查写 `not feasible + reason`，不能静默删除。

## 7. Heterogeneity Preregistration

```yaml
heterogeneity_question:
prespecified_subgroups: []
exploratory_search_space:
minimum_support_per_group:
honesty_or_confirmation_split:
multiplicity_control:
uncertainty_method:
calibration_or_ranking_check:
protected_or_vulnerable_groups:
individual_action_prohibited: yes
non_transfer_conditions: []
owner:
source_ids: []
stop_if: [post-hoc winner only, insufficient support]
decision: EXPLORATORY_ONLY | READY_FOR_CONFIRMATION
```

CATE 是条件平均，不是个人真实反事实。任何政策规则另开 policy/rights review。

## 8. Transport、政策与最终 Decision Memo

```yaml
study_population:
target_population:
differences:
  - factor:
    effect_modifier_rationale:
    support_evidence:
    transport_assumption:
implementation_version_change:
capacity_and_cost:
strategic_or_equilibrium_response:
welfare_definition_and_dissent:
rights_appeal_and_remedy:
non_ai_alternative:
source_ids: []
unknowns: []
owner:
review_date:
stop_and_rollback:
decision: BLOCKED | GOVERNANCE_REVIEW_REQUIRED | ANALYSIS_ONLY
```

最终 memo 附 A/B/C/D claim ledger、minority report 和“此结果不表示什么”。不得用模型置信度替代政策合法性。
