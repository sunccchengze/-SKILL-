# Source Notes — Applied Causal ML Readiness

检索基准日：**2026-08-16**。版本、作者主张与独立证据分开。`A/B` 优先回到原作；`C` 必须写设计、适用范围和限制。URL 可定位，不代表页面永不变化。

## 原作与版本

### CM01 — Official project homepage

- **类型**：作者/项目官方网页，一手；版本与目录权威。
- **状态**：页面列出 Chapter 0–17；online version **0.1.2, May 3, 2026**；有 R/Python notebook 与 exercises 入口。
- **支持**：书的公开形态、当前在线版本、章节架构。
- **限制**：动态在线出版物；以后引用需重查版本。不能据此称 2026 传统首版。
- **URL**：https://causalml-book.org/

### CM02 — Official preface (version 0.1.2)

- **类型**：原作前言 PDF，一手。
- **支持**：目标读者从 advanced undergraduate 到 graduate/applied researchers；核心与高级主题、代码/练习安排和先修定位。
- **限制**：前言陈述教学意图，不独立验证方法表现。
- **URL**：https://causalml-book.org/chapters/CausalML_preface.pdf

### CM03 — arXiv historical record 2403.02467

- **类型**：作者公开稿元数据/版本史，一手。
- **状态**：first submitted **2024-03-04**；后续版本可能变更。
- **支持**：防止把 2026 在线版本日期伪造成项目首次公开日期。
- **限制**：arXiv 时间不等于出版社版首版；使用内容需写具体版本。
- **URL**：https://arxiv.org/abs/2403.02467

## DML、识别与实现

### CM04 — Chernozhukov et al., Double/debiased machine learning

- **类型**：同行评审方法论文，一手研究。
- **支持**：orthogonal scores 与 cross-fitting 用于降低高维 nuisance 学习中的正则化/过拟合偏差，并在条件下支持推断。
- **限制**：定理依赖识别、矩条件、收敛率和实现；不保证无隐藏混杂、重叠或正确 estimand。
- **URL**：https://doi.org/10.1111/ectj.12097

### CM05 — DoubleML documentation: basic methodology

- **类型**：开源方法/软件官方文档，实施参考。
- **支持**：sample splitting、cross-fitting、score 与 nuisance learner 的实现概念。
- **限制**：文档/软件成功运行不是识别证据；版本与默认设置需记录。
- **URL**：https://docs.doubleml.org/stable/guide/basics.html

### CM06 — Evaluation study of DML methods (2024 preprint)

- **类型**：独立比较/评价预印本。
- **支持**：DML 实际表现依赖 causal structure、controls、learner 与具体 data-generating process；没有普遍最佳 learner。
- **限制**：模拟/选定场景不穷尽现实；预印本状态需保留。
- **URL**：https://arxiv.org/html/2403.14385v1

### CM07 — Crump et al., dealing with limited overlap

- **类型**：同行评审方法论文。
- **支持**：有限 overlap 会损害估计；可为特定目标定义更有支持的子总体。
- **限制**：修剪会改变 estimand/population；阈值不是普适伦理规则。
- **URL**：https://doi.org/10.1093/biomet/asn055

### CM08 — Cinelli & Hazlett, omitted-variable sensitivity

- **类型**：同行评审方法论文。
- **支持**：可用可解释量度分析线性回归结论对未观测混杂的敏感性。
- **限制**：量化 robustness 不证明无混杂；模型、尺度与线性结构限定迁移。
- **URL**：https://doi.org/10.1111/rssb.12348

### CM09 — Hernán & Robins, What If

- **类型**：开放教材/综合方法来源。
- **支持**：明确因果 estimand、exchangeability、positivity、consistency、时间顺序与目标试验思维。
- **限制**：综合教材不是用户数据的识别证明；具体设计仍需领域证据。
- **URL**：https://miguelhernan.org/whatifbook

### CM10 — Wager & Athey, causal forests

- **类型**：同行评审方法论文。
- **支持**：在明示条件下用随机森林框架估计异质处理效应并做推断。
- **限制**：估计 CATE 不等于观测个体反事实；有限样本、支持域与 honesty 很关键。
- **URL**：https://doi.org/10.1080/01621459.2017.1319839

### CM11 — Athey & Wager, policy learning

- **类型**：同行评审方法论文。
- **支持**：可在约束 policy class 与识别条件下学习福利导向政策并讨论 regret。
- **限制**：福利函数、成本、容量、权利、策略响应和迁移是额外规范/因果问题。
- **URL**：https://doi.org/10.3982/ECTA15732

## 迁移、干扰、测量与治理

### CM12 — Bareinboim & Pearl, external validity/transportability

- **类型**：同行评审理论论文。
- **支持**：从实验/研究域向目标域迁移需要明确域差异与结构条件，而非只比较平均特征。
- **限制**：图结构与选择机制需可信；可识别公式不保证数据质量。
- **URL**：https://doi.org/10.1073/pnas.1510507113

### CM13 — Hudgens & Halloran, causal inference with interference

- **类型**：同行评审方法论文。
- **支持**：有干扰时需要重新定义暴露与直接/间接等效应，普通 no-interference 解释会失效。
- **限制**：特定干扰结构与设计假设；不能覆盖任意网络扩散。
- **URL**：https://doi.org/10.1198/016214508000000292

### CM14 — Lipsitch et al., negative controls

- **类型**：同行评审流行病学方法论文。
- **支持**：negative control exposure/outcome 可帮助探测部分混杂、选择或测量偏差。
- **限制**：阴性结果不证明完全无偏；control 自身需要有效性论证。
- **URL**：https://doi.org/10.1097/EDE.0b013e3181d61eeb

### CM15 — Hernán & Robins, target trial emulation

- **类型**：同行评审方法论文章。
- **支持**：观察研究可通过明确 eligibility、assignment、time zero、follow-up、outcome 与 analysis 来避免若干设计偏差。
- **限制**：模拟规范不能消除未测混杂或测量失败。
- **URL**：https://doi.org/10.1093/aje/kwv254

### CM16 — STROBE statement

- **类型**：观察研究报告规范。
- **支持**：透明报告设计、变量、偏差、样本、分析与限制。
- **限制**：报告完整不等于因果有效；不是估计器选择指南。
- **URL**：https://www.strobe-statement.org/

### CM17 — NIST AI Risk Management Framework 1.0

- **类型**：官方风险治理框架。
- **支持**：高影响 AI 需要持续 Govern/Map/Measure/Manage、角色责任、情境与监测，而非一次模型验证。
- **限制**：自愿框架，不替代领域法律；不提供因果识别保证。
- **URL**：https://www.nist.gov/itl/ai-risk-management-framework

### CM18 — CONSORT 2025 statement

- **类型**：随机试验报告规范的当前官方入口。
- **支持**：随机化、分配、分析、人群与 harms 等透明报告提醒；随机化有效性依赖实际执行。
- **限制**：报告标准不是具体试验批准，也不覆盖所有观察/自然实验设计。
- **URL**：https://www.consort-statement.org/

## 使用边界汇总

- 原作在线版本会变；必须锁版本与访问日。
- DML 结果只在 estimand、识别、支持域、数据生成过程与实现条件下可解释。
- simulation、software documentation、reporting checklist 各自只能支持有限层面。
- “未被诊断发现”不等于“偏差不存在”；C 层反证必须进入最终结论。
