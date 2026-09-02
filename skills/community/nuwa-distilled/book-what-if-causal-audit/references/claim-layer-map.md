# Claim—layer—source map：*Causal Inference: What If*

**边界**：A = 锁定的 2025-05-27 作者 PDF / 2025 CRC 成书；B = 作者同主题其他论文/后续报告；C = 独立研究、报告规范与批评；D = 本 Skill 操作化。一个核心声明只占一层。

| ID | 可使用的声明 | 层 | 来源 | 限制 |
|---|---|---|---|---|
| CIW001 | 因果问题比较同一目标总体在不同策略下的反事实结局分布，而不只是观测组差异 | A | CIW-01 | 反事实定义不让个体两种结局同时可见 |
| CIW002 | 因果效应必须绑定总体、策略、结局、时间窗与效应尺度 | A | CIW-01 | “X 是否有效”尚不是可估计问题 |
| CIW003 | 随机化因预期产生可交换性而支持处理组比较 | A | CIW-01 | 实际试验仍受不依从、失访和测量影响 |
| CIW004 | 观测研究的标准化/IPW 识别通常需一致性、条件可交换性与正值性 | A | CIW-01 | 是给定方法下的充分条件，不宜写成所有因果推断的唯一必要条件 |
| CIW005 | 条件可交换性依赖实质知识且不能仅由观测数据验证 | A | CIW-01 | 平衡已测变量不证明无未测混杂 |
| CIW006 | 一致性要求策略/版本足够明确并把实际观察连接到相应反事实 | A | CIW-01 | 宽泛标签可能隐藏不同版本与机制 |
| CIW007 | 正值性只相对于为识别所需的调整变量与目标总体定义 | A | CIW-01 | 有限样本稀疏与结构零需分开 |
| CIW008 | 因果图编码假设并帮助识别混杂、选择和碰撞点偏差 | A | CIW-01 | 图本身不是从数据自动证明的事实 |
| CIW009 | 目标试验协议含资格、策略、分配、随访、结局、因果对比和分析计划七项 | A | CIW-01, CIW-02 | emulation 仍没有真正随机化 |
| CIW010 | eligibility、策略分配与随访起点应在 time zero 对齐 | A | CIW-01, CIW-02 | 对齐减少自致时间偏差，不消除混杂 |
| CIW011 | 混杂与效应修饰是逻辑不同的问题 | A | CIW-01 | 同一变量可在不同问题中扮演不同角色 |
| CIW012 | 选择偏差可由对共同结果选择变量条件化等结构产生 | A | CIW-01 | 不能以“代表性不足”涵盖全部选择偏差 |
| CIW013 | 时间变化处理与受既往处理影响的混杂常需 g-methods | A | CIW-01 | 方法正确仍依赖序贯识别与模型条件 |
| CIW014 | 估计方法选择应晚于问题、识别与数据结构 | A | CIW-01 | 高级估计器不是识别策略 |
| CIW015 | 2016 目标试验论文明确给出七项协议并示范观测映射 | B | CIW-03 | 是作者论文，不是锁定书内新增独立证据 |
| CIW016 | TARGET 2025 报告声明把目标试验与 emulation 的透明报告制度化 | B | CIW-07 | 报告完整不等于研究有效 |
| CIW017 | 作者网站把本书作为持续修订的 living book 发布 | B | CIW-02 | 因此本包冻结日期而非假称文本永不变化 |
| CIW018 | 对 202 项 TTE 的审查发现完整双协议与因果对比报告并不普遍 | C | CIW-08 | 报告审查不直接估计偏差大小 |
| CIW019 | target-trial 框架能减少 time-zero 错位造成的设计偏差 | C | CIW-03, CIW-07, CIW-08 | 不能消除残余混杂、测量误差和缺失 |
| CIW020 | 机器学习可放松函数形式假设，但不自动提供识别或识别坏控制变量 | C | CIW-09 | 某一 DML 评估不能代表所有 ML 因果方法 |
| CIW021 | ICU 因果研究审查显示识别假设及正值诊断经常报告不足 | C | CIW-10 | 限于 ICU 文献样本 |
| CIW022 | 负对照、重叠、平衡、权重和未测混杂敏感性是诊断而非证明 | C | CIW-07, CIW-10 | 通过诊断仍不验证不可检验假设 |
| CIW023 | 2026 争论提醒正值性不是脱离目标与方法的普遍口号 | C | CIW-11 | 该批评不否定书中对标准化/IPW 的条件表述 |
| CIW024 | 高风险决策需把估计与现实行动证据、权益和责任治理分开 | C | CIW-12 | 治理框架不替代法域专业审查 |
| CIW025 | TARGET 是本 Skill 创建的七步审计，不是书中命名法 | D | D1 | 未经外部效度验证 |
| CIW026 | CLI 只建立目标试验与假设账本，不运行估计或宣告因果 | D | D1 | 输入默认 submitted-not-verified |
| CIW027 | 高影响领域缺 owner/rule/impact/appeal/rollback/stop 时受控失败 | D | D1 | 填完仍是 governance_review_required |
| CIW028 | 输出必须显式写“设计审计 ≠ 因果证明 ≠ 部署批准” | D | D1 | 分析不能冒充决定 |

## 禁止坍缩

- association **≠** intervention effect；prediction **≠** causal effect；
- covariate balance **≠** no unmeasured confounding；DAG **≠** learned truth；
- identification **≠** estimation；precision **≠** validity；
- target-trial table **≠** randomized trial；diagnostic passed **≠** assumption proved；
- 2025 frozen PDF **≠** all earlier/later living versions；analysis **≠** action approval。
