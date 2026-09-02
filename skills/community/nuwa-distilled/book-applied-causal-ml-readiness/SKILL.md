---
name: book-applied-causal-ml-readiness
description: |
  将《Applied Causal Inference Powered by ML and AI》在线版本 0.1.2（2026-05-03）转化为因果识别、DML/双重稳健估计与异质性分析的可审计准备实验室。
  当用户要用机器学习估计处理效应、做 DML/cross-fitting、CATE、政策学习、敏感性分析或迁移判断时使用；先定义 estimand 和识别条件，再讨论估计器。
  预测不等于识别，DML 不能修复隐藏混杂、坏控制、无重叠、干扰、弱识别或迁移失败；本 Skill 只给分析合同与停止门，不自动宣称因果、部署或政策批准。
---

# Applied Causal ML Readiness Lab

> 基准：官方在线版 **v0.1.2，2026-05-03**。该项目早期公开稿可追溯至 2024-03-04；不得把在线版本日期写成传统纸质“首版”。本包不复制教材，而把其识别—估计—验证逻辑做成可审计分析合同。

## 何时调用

- 用户说“用 XGBoost/神经网络/随机森林控制协变量后就是因果吗”；
- 要估计 ATE、ATT、CATE、政策价值，或比较 DML、DR learner、causal forest；
- 要检查 DAG、bad controls、overlap、cross-fitting、nuisance loss、敏感性、外推；
- 需要在建模前冻结问题、数据切分、异质性和政策使用边界；
- 需要明确 **BLOCKED**、`READY_FOR_ESTIMATION_PLAN` 与治理复核，而不是让模型“算个因果结果”。

不用于：把相关预测包装成因果结论；替代随机化记录、领域知识、伦理审查、法律意见或参与式政策决策。

## 版本与归因纪律

- **原作层**：Victor Chernozhukov 等作者团队的在线教材；官网列出 Chapter 0–17、R/Python notebook 与练习，读者从高年级本科到博士/应用研究者。
- **版本层**：引用必须写“online version 0.1.2, May 3, 2026”；若引用 arXiv 历史，另写 first submitted 2024-03-04。
- **独立证据层**：DML 论文、重叠/敏感性/迁移/政策学习研究与治理标准，不当作作者自证。
- **本包推论层**：`IDENTIFY-DML` 门、模板和 CLI 是本 Skill 的操作综合，不冒充书中逐字方案。

## 一、五个心智模型

### 模型1：Identification before estimation｜先识别，后估计

先写单位、处理版本、对照、结果、time zero、时间窗与 estimand，再写使观察分布能回答该问题的交换性/随机化/工具变量等条件。算法性能不能提供缺失的反事实。

- **局限/失效**：明确假设仍不等于假设为真；DAG 也会漏变量、错方向或掩盖多种处理版本。

### 模型2：Orthogonality is a local robustness device, not a causal wand｜正交不是因果魔杖

DML 用正交得分降低目标估计对 nuisance 误差的一阶敏感性，并常用 sample splitting/cross-fitting 降低同样本过拟合偏差。这只在识别、重叠、矩条件、收敛和实现正确时有意义。

- **局限/失效**：隐藏混杂、post-treatment control、弱工具、极端 propensity、泄漏或错 estimand 不会被正交化修好。

### 模型3：Overlap defines the population you can learn about｜重叠定义可学习人群

positivity 不是一张“通过”截图；要看处理概率、协变量空间支持、极端权重、被修剪者及修剪后 estimand 如何改变。

- **局限/失效**：有限样本诊断不能证明总体 positivity；修剪改善稳定性却改变目标人群，不能悄悄仍称原 ATE。

### 模型4：Heterogeneity is a discovery-and-confirmation problem｜异质性须分发现与确认

CATE/forest 可探索效应差异，但 subgroup 选择、multiplicity、honesty、uncertainty 与最小样本都要预先约束；“某组点估计大”不是稳定政策规则。

- **局限/失效**：个体处理效应通常不可直接验证；高维分组会制造偶然赢家，平均校准不保证个体排序正确。

### 模型5：Transport and policy use are new causal problems｜迁移与政策使用是新问题

从 study sample 到 target population 要列选择机制、效应修饰、可比支持和目标期变化；从 effect estimate 到 policy 还要加入容量、成本、福利、权利、策略响应与反馈。

- **局限/失效**：历史可迁移不保证制度改变后仍成立；policy learner 的离线价值也可能在部署后因行为改变而失效。

## 二、A/B/C/D 声明防串层

任何高影响输出都在段首标层；完整逐条 ledger 在 [`references/claim-layer-map.md`](references/claim-layer-map.md)。

- **A｜原作层**：作者实际讲授的定义、章节结构、示例或限制；附 `CM01–CM03` 等定位。
- **B｜原作内部限定层**：作者自己承认的前提、有限样本、识别或高级内容边界；仍需原作来源。
- **C｜独立证据层**：独立论文、教材、标准的支持、反证、替代解释或非迁移条件；附来源与适用范围。
- **D｜Skill 推论层**：本包把 A/B/C 转成 gate、字段、模板与停止规则；必须写“本 Skill”，不能说“作者要求”。

禁止：用 DML 软件成功运行证明 ATE 已识别；用作者例子证明用户场景；用 sensitivity 数字消除 hidden confounding；把 CATE 排名变成个体事实。

## 三、IDENTIFY-DML 十三步工作流

### 1. DECISION｜先冻结决策，不先碰模型

写清：谁在何时因何决定需要这个估计；如果只是预测、描述或资源排序，就不要强迫它成为因果问题。记录“不估计”的替代方案。

### 2. ESTIMAND｜把反事实问题写成合同

最低字段：population、unit、treatment versions、comparator、outcome、time zero、horizon、aggregation、ATE/ATT/CATE/policy value。处理定义不一致时停止。

### 3. TIMELINE｜画时间与数据生成过程

按 treatment 前/同时/后标变量；将 post-treatment mediator、collider、measurement after assignment 与 baseline confounder 分开。不要从 feature importance 推断 DAG。

### 4. IDENTIFICATION｜写可争辩的识别论证

为 randomized、observational、natural experiment 分别提交：分配机制、exchangeability/exclusion、consistency、positivity、no interference 或其放宽。每项要有 owner、证据、反例和可证伪部分。

### 5. DATA AUDIT｜审数据不是只审缺失率

检查资格、纳入、处理记录、结果定义、删失、measurement error、缺失机制、泄漏、重复单位、cluster、选择进入样本和 privacy。数据不可追溯则 `BLOCKED_DESIGN`。

### 6. OVERLAP｜声明支持域和 estimand 变化

按 outcome-blind 方案检查 propensity/support；报告尾部、权重、被排除群体。若修剪，重命名目标为 trimmed estimand 并讨论公平/迁移影响。

### 7. SPLIT｜冻结 cross-fitting 与调参边界

写 folds、cluster-aware split、time-aware split、seed、nuisance tuning 的训练域和最终评估域。严禁 outcome/target fold 泄漏；重复切分应预声明聚合方式。

### 8. NUISANCE｜先评价 nuisance 任务

分别评估 outcome model、propensity/instrument 等 out-of-fold 表现、校准和极端预测；不以单一 ML 排行代替估计量诊断。复杂模型不是默认更好。

### 9. ESTIMATION｜再选 DML/DR/forest

说明 score、learner、cross-fitting、standard error、cluster、weight 与软件版本。DML 是候选估计器，不是识别策略名称；同时保留朴素/设计导向基线。

### 10. ROBUSTNESS｜反证优先

至少做：替代 adjustment set/learner、重叠限制、negative control 或 placebo（可行时）、未测混杂敏感性、measurement error/attrition 分析。结果变化要更新结论，不得只放附录。

### 11. HETEROGENEITY｜发现与验证分离

预声明 subgroup、honesty/holdout、multiplicity、minimum support、uncertainty；探索性组必须标探索。禁止按事后最大 CATE 自动推荐行动。

### 12. TRANSPORT/POLICY｜重开一轮识别

列 target population 与 study 差异、效应修饰、支持域、制度变化、成本/容量、策略响应、福利和权利。高风险用途至少转 `GOVERNANCE_REVIEW_REQUIRED`。

### 13. REPORT/REVIEW｜四层报告与复审

同时报告：估计、uncertainty、识别假设、诊断失败、未解决威胁、非迁移人群、停止条件、复审日期。结论只到证据可承载的强度。

## 四、硬停止门

| 触发 | 状态 | 不能用什么“补救” | 下一步 |
|---|---|---|---|
| treatment/outcome/time zero 或 estimand 含糊 | `BLOCKED_DESIGN` | 更多算力 | 与领域方重定义 |
| 明确把处理后变量当控制 | `BLOCKED_POST_TREATMENT_BIAS` | DML/正则化 | 重画时间线与因果图 |
| 有可信未测混杂且无新设计 | `BLOCKED_UNIDENTIFIED_CONFOUNDING` | sensitivity 当识别 | 改设计/降级为关联 |
| 干扰/溢出存在却仍解释为 SUTVA 单位效应 | `BLOCKED_INTERFERENCE` | cluster SE 单独解决 | 重定义暴露/单位/estimand |
| 无支持或极端权重 | `BLOCKED_DESIGN` | 默认 clipping | 改人群、收集数据或报告不可识别区 |
| DML 无独立 split 与 OOF nuisance 评价 | `BLOCKED_DESIGN` | in-sample AUC | 冻结 cross-fitting 计划 |
| CATE 无 honesty/multiplicity/support | `BLOCKED_DESIGN` | 漂亮热图 | 降为探索或建立确认集 |
| 高风险政策/个体行动 | `GOVERNANCE_REVIEW_REQUIRED` | 高置信度点估计 | 权利、申诉、容量、参与、法律复核 |

## 五、最小产物包

1. estimand card；2. timeline/DAG register；3. identification table；4. data lineage；5. overlap report；6. split manifest；7. nuisance scorecard；8. estimator spec；9. robustness matrix；10. heterogeneity preregistration；11. transport/policy memo；12. decision log。

若只交模型和一张 effect plot，不能称因果 ML 审计。

## 六、反证与非迁移检查

- **反证 1**：同一估计对合理 adjustment set、trim 或 split 极不稳定；降级结论。
- **反证 2**：negative control 显示残余结构；调查偏差，不把它称“一个额外特征”。
- **反证 3**：nuisance 表现差、propensity 极端、fold 间漂移；不因最终标准误小而忽略。
- **替代解释**：选择进入处理、测量改变、同时政策、spillover、anticipation、attrition。
- **非迁移条件**：目标人群无 covariate support、实施版本变化、关键 effect modifier 缺失、制度/价格/激励改变。
- **不确定性**：统计区间不含 identification uncertainty；二者分列，不能做一个“总置信度”。

## 七、CLI：只生成 readiness contract

```bash
python3 scripts/audit_causal_ml.py \
  --question "外展邀请是否改变六个月留存？" \
  --treatment "收到外展邀请" --outcome "六个月留存" \
  --unit "符合资格的参与者" --time-zero "资格确认日" \
  --estimand ate --design observational \
  --identification-assumption "给定处理前需求后条件交换性" \
  --control "处理前需求" \
  --overlap-check "按预声明分层检查 propensity 支持" \
  --split-plan "五折 cross-fitting；同一人不跨折" \
  --nuisance-evaluation "OOF calibration 与 loss" \
  --sensitivity "未测混杂 robustness value 与 negative control" \
  --use-dml --owner "评估负责人"
```

输出为稳定、`sort_keys=True` JSON。`READY_FOR_ESTIMATION_PLAN` 仅表示“可写估计计划”，不表示 effect 已识别/估出/可迁移；CLI 不读数据、不拟合模型、不批准行动。

## 八、十组内在张力

1. **张力 1｜灵活学习器 vs 可识别反事实**：ML 可拟合复杂函数，却不能观察未发生结果。
2. **张力 2｜正交稳健 vs 假设脆弱**：对 nuisance 局部稳健，不对隐藏混杂稳健。
3. **张力 3｜重叠稳定 vs 目标完整**：修剪可稳定权重，也排除最缺少选择的人。
4. **张力 4｜预测分数 vs 因果参数**：高 AUC 可与错误因果结论共存。
5. **张力 5｜模型复杂度 vs 可审计实现**：更强 learner 可能带来调参泄漏与运维不可复现。
6. **张力 6｜异质性发现 vs 多重比较**：发现越自由，偶然“赢家”越多。
7. **张力 7｜平均效应 vs 个体决策**：群体均值不提供某个人的反事实真值。
8. **张力 8｜敏感性量化 vs 识别修复**：可描述需多大隐藏偏差，却不能证明偏差不存在。
9. **张力 9｜迁移效率 vs 地方机制**：复用估计省时，但制度、实施和支持域会变。
10. **张力 10｜政策价值 vs 权利边界**：总福利优化可能掩盖申诉、分配和不可接受伤害。

## 九、表达DNA

- **句式**：先“目标参数与识别条件”，再“估计器与结果”；不要先报一个数。
- **词汇**：estimand、time zero、exchangeability、overlap、orthogonal score、cross-fitting、non-transfer。
- **语气**：技术精确但不炫技；明确“在这些假设下”而不是“AI 发现因果”。
- **节奏**：问题 → 时间线 → 识别 → 支持域 → split → nuisance → estimator → 反证 → 决策。
- **确定性**：区分已观察诊断、不可检验假设、外部证据与本 Skill 门槛。
- **引用**：作者主张、独立证据和操作推论分别标 A/C/D；不用二手营销替代原始论文。

## 十、诚实边界

- 本 Skill 不从观察数据自动发现真实 DAG，也不证明无未测混杂。
- DML、双重稳健或 causal forest 不是银弹；模型名称不能替代识别论证。
- sensitivity analysis 描述结论对偏差的脆弱度，不消除偏差。
- 置信区间通常条件于模型/识别前提，不覆盖全部结构、迁移或测量不确定性。
- CATE 不等于可验证的个体 treatment effect，不应用于无申诉的高风险个体分配。
- 数据外 transport、制度改变后的 performative feedback 和 equilibrium effect 需新证据。
- 本包不是统计、医学、法律或政策批准，也不替代领域专家与受影响人群参与。

## 十一、来源与执行导航

- [包说明](README.md)
- [参考导航](references/README.md)
- [18 条 A/B/C/D 声明](references/claim-layer-map.md)
- [来源卡与版本状态](references/source-notes.md)
- [可复制模板](references/templates.md)
- [六轮研究日志](references/research/01-version-scope-genre.md)
- [验证记录](VALIDATION.md)
