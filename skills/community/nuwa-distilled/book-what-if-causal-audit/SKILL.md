---
name: book-what-if-causal-audit
description: |
  基于 Hernán 与 Robins 的《Causal Inference: What If》（冻结 2025-05-27 版）把“X 是否有效”编译为可审计的因果问题、七项目标试验、识别假设、估计诊断与敏感性记录。
  当用户需要区分预测与因果、设计 observational target-trial emulation、检查 exchangeability/positivity/consistency、DAG 变量角色、time zero、g-methods 或 causal ML 误用时使用。
  不把关联、平衡、DAG、target-trial 表、p 值或 ML 当因果证明。人员、劳动、医疗、教育、信用、执法、内容治理默认高风险；缺真实影响证据、owner、规则、受影响群体、申诉、停止和回滚时受控失败，完整字段仍不是部署批准。
---

# 《Causal Inference: What If》因果设计审计 Skill

> **对象**：不是“跑一个因果模型”，而是把问题—试验—识别—估计—行动之间的每一座桥单独承重、单独标假设。

## 1. 使用 / 禁用

**使用于**：干预效果问题、RWE、政策评估、A/B 之外的观测比较、target-trial emulation、纵向策略、混杂/选择偏差、DAG 审查、g-formula/IPW/MSM/g-estimation、causal ML 前置审查。

**不要单独使用于**：
- 只需预测“谁会发生 Y”；
- 无法定义可比较策略、time zero 或结局窗口；
- 需要即时临床、法律、伦理、劳动或监管决定；
- 用户要求“把所有变量丢进模型自动消除偏差”；
- 将估计结果直接转成对人的高影响行动。

紧急保护/报告义务先行；研究设计不能拖延救治、停止伤害或证据保全。

## 2. 版本与四层

| 层 | 内容 | 输出纪律 |
|---|---|---|
| A | 2025-05-27 作者 PDF / 2025 CRC 成书，ISBN `9781420076165` | “书中定义/主张”；不称假设已成立 |
| B | 作者 2016 target trial 论文、TARGET 后续等 | 标作者、日期和后续身份 |
| C | 独立报告审查、DML/ICU 证据、方法争论、治理 | 写设计、范围、冲突和限制 |
| D | 本 Skill 的 TARGET 流程、CLI 与高影响门 | 明写本包创建，不冒充书中术语 |

该书是 living text。本包**冻结 2025-05-27**；更早/更晚 PDF 不混页码。完整声明见 [`claim-layer-map.md`](references/claim-layer-map.md)。

## 3. 认识论合同

1. **先定义 effect，后找数据。** 人群、两种策略、结局、窗口、contrast 任一缺失都不是完整 estimand（CIW001–CIW002）。
2. **识别先于估计。** 数据 + identifying assumptions 才可能连接到反事实；高级 estimator 只处理估计层（CIW004–CIW005、CIW014）。
3. **假设不是勾选。** exchangeability 不能仅由数据验证；positivity 与 target/method 相对；consistency 要求策略版本明确（CIW004–CIW007）。
4. **DAG 是假设图。** 图用于公开变量角色和路径，不是因果发现的真相输出（CIW008）。
5. **time zero 是设计约束。** eligibility、strategy assignment、follow-up 不对齐会制造 self-inflicted bias（CIW009–CIW010、CIW019）。
6. **预测质量不是干预效度。** DML/forest 可放松函数形式，不能修复未测混杂、坏控制或无重叠（CIW020）。
7. **诊断不证明。** balance/overlap/negative control/sensitivity 能暴露问题，不能认证不可检验假设（CIW022）。
8. **分析不是行动。** 高影响用途还需现实影响、权益、owner、stop/rollback/appeal；结果保持 `governance_review_required`（CIW027–CIW028）。

## 4. 六个不可替换心智模型（Nvwa 三重验证）

### M1 反事实对比：同一总体、两种世界、只能观察一个
- **跨章节复现**：trial、observational、standardization、g-methods 都估计策略下结局分布。
- **生成力**：迫使问题写成“谁、策略 A/B、什么结果、何时、何种 contrast”。
- **排他性**：区别于把回归系数或 feature importance 叫 effect。
- **失败门**：比较组实际接受的是不同且未定义版本，停止估计。

### M2 目标试验：让随机试验协议约束观测设计
- **跨域**：资格、策略、分配、随访、结局、contrast、analysis 七项贯穿药物/政策/组织干预。
- **生成力**：每项写 ideal 与 emulation 两列，差异就是偏差/可行性账本。
- **排他性**：先设计后建模；不是“像 RCT”营销标签。
- **失败门**：time zero 无法共同定义，改问题或放弃（CIW009–CIW010）。

### M3 三角识别条件：一致性—可交换性—正值性
- **跨方法**：支撑 standardization/IPW 等观测识别。
- **生成力**：每个条件写 statement、依据、可观测 implication、sensitivity、owner。
- **排他性**：把实质知识明写为数据之外的输入。
- **失败门**：不得用平衡、样本大或高预测准确率把状态改成 `verified`。

### M4 因果图是变量角色控制台
- **跨偏差**：confounder、mediator、collider、selection、instrument 的调整后果不同。
- **生成力**：同一变量必须相对于特定 estimand/时间位置分类；列竞争 DAG。
- **排他性**：拒绝按显著性/重要度机械选控制变量。
- **失败门**：处理后变量被当基线混杂无说明时停止总效应解释。

### M5 时间变化处理需要历史序列而非单次“暴露”
- **跨章节**：MSM、g-formula、g-estimation 处理 prior treatment 影响 future confounder 的结构。
- **生成力**：写 decision times、history、adherence、censoring 和 sequential assumptions。
- **排他性**：普通回归调 post-treatment confounder 可能同时挡机制、开偏差。
- **失败门**：时间戳粒度不能确定先后，不输出动态策略效应。

### M6 识别—估计—决定三层防火墙
- **跨应用**：识别回答“数据在假设下能否表达 effect”；估计回答“怎样算”；决定加入价值/效用/权利。
- **生成力**：让 ML 只进入 nuisance/heterogeneity 等明确位置。
- **排他性**：不会从置信区间直接跳到“应部署”。
- **失败门**：任何层借下一层词汇掩盖缺口即降级。

| 模型 | 跨域复现 | 生成力 | 排他性 | 保留 |
|---|---|---|---|---|
| 反事实 effect | trial/observational/longitudinal | 完整 estimand | 非关联 | 是 |
| target trial | RWE/政策/临床 | 双协议 | design-first | 是 |
| 三条件 | 多估计器 | 假设账本 | 数据外知识 | 是 |
| DAG 角色 | 混杂/选择/中介 | 调整策略 | 非特征选择 | 是 |
| longitudinal history | 动态策略 | 序贯设计 | 非单次 exposure | 是 |
| 三层防火墙 | 所有应用 | 防误用 | 非模型中心 | 是 |

## 5. 主工作流 TARGET（D 层）

### T — Target question
写：target population、strategy A/B、outcome、time horizon、measure、ITT/per-protocol/其他 contrast。区分 total/direct/controlled effect；不要用“AI 影响员工吗”。

**门**：策略不是可操作/可描述版本，或结局发生在处理之前，停止。

### A — Articulate the trial
双列表写七项：
1. eligibility；2. treatment strategies（开始/停止/切换/宽限）；3. assignment；4. follow-up/time zero；5. outcome ascertainment；6. causal contrast；7. analysis plan。

**门**：eligibility、assignment、follow-up 起点错位则先修设计，不用模型补。

### R — Register assumptions
最低槽：
- consistency / well-defined versions；
- exchangeability 或 IV/RD 等替代识别；
- positivity/overlap；
- measurement、missingness、censoring；
- interference（若 estimand 需要）。

每项必须含：why plausible / why not / observable diagnostic / sensitivity / falsifier / owner。状态只能 `asserted_not_verified`、`challenged`、`incompatible`。

### G — Graph structure
- 节点带时间索引；
- 每条箭头写实质依据与替代方向；
- 变量角色表：common cause / outcome predictor / mediator / collider / selection / instrument / proxy；
- 同时写未测 `U` 与数据捕获机制；
- 不以算法自动生成图替专家与受影响者知识。

### E — Estimate with diagnostics
方法必须匹配 estimand 与结构：standardization/outcome model、IPW/MSM、g-formula、g-estimation、IV 等。先冻结 analysis plan，再检查：
- overlap 与 extreme weights；
- weighted/unweighted balance；
- influential units 与 effective sample size；
- censoring/missing mechanisms；
- outcome/treatment misclassification；
- model specification；
- subgroup harm，不只平均 effect。

### T — Test robustness
至少：negative-control rationale、未测混杂 quantitative sensitivity、替代策略版本、time-zero/lag、missingness、estimators、target population、placebo/falsification。敏感性分析只显示脆弱性，不“修复”假设。

### T — Transmit limits
发布表必须并列：estimate、uncertainty、identification assumptions、failed diagnostics、unmeasured threats、target、transport boundary、decision owner。高影响只输出 review packet。

## 6. 快速规则与常见误用

| 误用 | 诊断 | 修复 |
|---|---|---|
| “控制了很多变量” | 未给变量角色 | DAG + time index + bad-control review |
| treatment 是标签 | 版本混杂 | 写策略开始/持续/切换 |
| 先看到数据再定义人群 | data-driven estimand | 冻结 target trial |
| users 比 nonusers | prevalent-user bias | active comparator/new user 或解释不可行 |
| 从入组后才判资格 | immortal/selection bias | 对齐 time zero |
| 平衡好=无混杂 | 只平衡 measured L | 保留 unmeasured U 与 sensitivity |
| overlap 差就删人 | target 偷换 | 显式重定义 target/estimand |
| ML AUC 高 | prediction | 独立识别策略后才用 ML |
| 显著=应采取 | value jump | 风险、效用、权益、owner 与实地影响门 |
| target trial=RCT | randomization laundering | 明写 observational analogue |

## 7. 高影响门

人员、劳动、医疗、教育、信用、执法、内容治理强制：
`accountable-owner / applicable-rule / affected-group / impact-evidence / appeal-path / rollback-trigger / stop-condition`。

`impact-evidence` 必须指真实流程/真实影响与分群伤害；CLI 只记录并标 `submitted_not_verified`。字段缺失返回 code 2；字段齐全仍保持 `governance_review_required`。

## 8. CLI

```bash
python3 scripts/emulate_target_trial.py \
  --question "启动项目提醒是否降低30日流失" \
  --population "首次完成注册且尚未收到提醒的客户" \
  --treatment "注册日发送一次提醒" --comparator "注册日不发送提醒" \
  --outcome "30日内停止使用" --time-zero "注册完成时" --follow-up "30日" \
  --estimand "目标总体30日风险差" \
  --assumption "提醒版本足够明确" \
  --assumption "给定基线活跃度与渠道后条件可交换" \
  --assumption "各协变量层两策略均有正概率" \
  --confounder "基线活跃度" --evidence "消息日志v2与事件字典v4" \
  --domain research --format markdown
```

CLI 不读取个体数据、不拟合模型、不计算 effect。高风险参数见 `--help`。

## 9. 张力与诚实边界

- **理想 trial ↔ 可行数据**：数据不能支持协议时改问题，不把缺失藏进模型。
- **明确干预 ↔ 现实多版本**：精确定义提高可解释性，也可能缩小外部效度。
- **exchangeability ↔ 不可检验**：专业判断不可省略，也不可伪装为验证。
- **positivity ↔ target relevance**：保留真实人群与稳定估计可能冲突，须公开 target 改变。
- **ITT ↔ adherence**：回答分配与遵循是不同 effects。
- **平均 effect ↔ 分布伤害**：总体收益不能清除小群体严重损害。
- **方法灵活 ↔ researcher degrees of freedom**：预注册和版本日志优先。
- **因果证据 ↔ 行动正当性**：即使内部效度强，也不自动合法、公平或值得做。

本包不替代原书、统计顾问、领域专家、IRB/伦理、法律或监管审查；也不声称公开资料验证任何用户数据与假设。

## 10. 深入资料

- [`references/source-notes.md`](references/source-notes.md) — supports / does-not-support / conflicts / unresolved
- [`references/templates.md`](references/templates.md) — 书特定制品
- `references/research/01`–`06` — 版本、模型、设计、估计、批评与 AI 治理研究轨
- [`VALIDATION.md`](VALIDATION.md) — 行为、来源和失败门验证
