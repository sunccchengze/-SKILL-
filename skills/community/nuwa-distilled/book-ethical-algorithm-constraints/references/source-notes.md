# Source Notes — The Ethical Algorithm Constraint Audit

检索基准日：**2026-08-16**。定理、实证、规范选择和治理要求分开；“可形式化”不等于“该形式对象在制度上正确”。

## 原作与作者议程

### EA01 — Oxford University Press official book record

- **类型**：出版社官方书页，一手书目来源。
- **支持**：Michael Kearns、Aaron Roth、2019 出版信息，以及 Privacy、Fairness、Games/strategic behavior、Lost Data/adaptivity、The Ethical Algorithm 五章结构。
- **限制**：出版社简介不独立证明技术/规范主张；具体引文需回原书。
- **URL**：https://global.oup.com/academic/product/the-ethical-algorithm-9780190948207

### EA02 — Kearns & Roth, ACM SIGecom agenda article

- **类型**：作者对“ethical algorithm design”研究议程的一手概述。
- **支持**：把社会属性形式化为算法约束/保证的项目；作者明确 privacy 技术比 fairness 或 explainability 更成熟。
- **限制**：研究议程不是所有价值可形式化的证明，也不是部署批准标准。
- **URL**：https://mail.sigecom.hosting.acm.org/exchanges/volume_18/1/KEARNS.pdf

## 隐私与自适应有效性

### EA03 — Dwork & Roth, Algorithmic Foundations of Differential Privacy

- **类型**：基础专著/一手理论综合。
- **支持**：neighboring datasets、epsilon/delta、composition、post-processing、mechanisms 与 reconstruction 风险基础。
- **限制**：形式保护取决于 unit/relation/mechanism；不提供 secrecy、security、consent 或 population-fact protection。
- **URL**：https://www.cis.upenn.edu/~aaroth/Papers/privacybook.pdf

### EA04 — Dwork et al., reusable holdout

- **类型**：同行评审理论/方法研究。
- **支持**：适应性重用 holdout 会过拟合；DP-inspired limited feedback 可在陈明条件下提高可复用性。
- **限制**：不是无限查询许可；query class、implementation、distribution 与外部复制仍有限。
- **URL**：https://www.science.org/doi/10.1126/science.aaa9375

### EA05 — NIST Privacy Framework

- **类型**：美国官方隐私风险治理框架。
- **支持**：隐私是组织/系统生命周期风险管理，涉及 data processing、roles、communication 与 controls，不等于一个 epsilon。
- **限制**：自愿框架、法域限定；不替代具体隐私法或 DP 证明。
- **URL**：https://www.nist.gov/privacy-framework

## 公平、不可能性与 subgroup

### EA06 — Kleinberg, Mullainathan & Raghavan, inherent trade-offs

- **类型**：同行评审理论论文。
- **支持**：当群体 base rates 不同，calibration/balance 类条件除完美或退化情形外通常不能同时满足。
- **限制**：定理基于特定定义；不决定社会应选何指标，也不涵盖全部公平概念。
- **URL**：https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITCS.2017.43

### EA07 — Chouldechova, fair prediction with disparate impact

- **类型**：同行评审统计分析。
- **支持**：差异 base rates 下 predictive parity 与 error-rate balance 的张力，并以风险评估说明政策意义。
- **限制**：特定二元分类/指标结构；不能当作所有公平目标的统一不可能性。
- **URL**：https://doi.org/10.1089/big.2016.0047

### EA08 — Kearns et al., Preventing Fairness Gerrymandering

- **类型**：同行评审方法论文。
- **支持**：少数粗粒度组 parity 可隐藏 intersectional subgroup 违规；丰富 subgroup audit 与学习存在计算问题。
- **限制**：subgroup class、样本、可计算性与统计不确定性限制覆盖；不保证个体/因果公平。
- **URL**：https://proceedings.mlr.press/v80/kearns18a.html

### EA09 — Barocas & Selbst, Big Data's Disparate Impact

- **类型**：法律学术研究。
- **支持**：数据挖掘中的 target、labels、features、training data 与 proxies 可产生/延续 disparate impact；形式性能不是法律结论。
- **限制**：美国反歧视法语境；法律发展和其他法域需更新。
- **URL**：https://www.californialawreview.org/print/big-datas-disparate-impact

### EA10 — Selbst et al., Fairness and Abstraction

- **类型**：同行评审社会技术批评。
- **支持**：把公平问题从社会系统抽象成技术对象会产生 framing、portability、formalism、ripple effect 与 solutionism traps。
- **限制**：诊断性框架不提供单一 metric/实现；需结合具体机构实证。
- **URL**：https://doi.org/10.1145/3287560.3287598

## 策略响应、反馈与解释

### EA11 — Hardt et al., Strategic Classification

- **类型**：同行评审理论研究。
- **支持**：受评分者会响应规则，分类器设计与行动成本/信息会共同改变结果。
- **限制**：响应模型与效用假设简化现实；“策略”不等于道德上的作弊。
- **URL**：https://doi.org/10.1145/3097983.3098087

### EA12 — Perdomo et al., Performative Prediction

- **类型**：同行评审理论研究。
- **支持**：部署预测会改变未来数据分布；定义 performative stability 并分析迭代再训练条件。
- **限制**：稳定点依赖响应/平滑等假设；稳定不等于因果最优或社会正义。
- **URL**：https://proceedings.mlr.press/v119/perdomo20a.html

### EA13 — Rudin, stop explaining black-box models for high stakes

- **类型**：同行评审立场/综合论文。
- **支持**：高风险场景中 post-hoc explanation 可能不忠实；应认真比较 inherently interpretable model，而非假定精度必降。
- **限制**：不是所有复杂任务都有简单同等性能模型；interpretability 也不解决目标合法性。
- **URL**：https://doi.org/10.1038/s42256-019-0048-x

### EA14 — Model Cards for Model Reporting

- **类型**：同行评审模型文档方法。
- **支持**：按用途、人群、指标和限制披露模型结果，有助于角色化解释/问责。
- **限制**：自我文档不能验证 fidelity、权利、供应链或 remedy。
- **URL**：https://doi.org/10.1145/3287560.3287596

## 治理与形式化批评

### EA15 — Formalising ethical values in AI systems

- **类型**：同行评审哲学/技术伦理研究。
- **支持**：technical 与 normative alignment 相互依赖；instructions、preferences、interests、values 不可互换。
- **限制**：概念分析不是具体系统验收测试。
- **URL**：https://link.springer.com/article/10.1007/s11023-020-09539-2

### EA16 — 2026 comparative review of formal approaches to AI ethics

- **类型**：截至基准日的同行评审批评/综合。
- **支持**：形式化提高 precision/enforceability，也可能抽象掉 institutional power、cultural context 与 lived harms。
- **限制**：2026 新文献，结论和分类需随讨论更新；不是对所有形式方法的否定。
- **URL**：https://link.springer.com/article/10.1007/s00146-026-03032-7

### EA17 — NIST AI Risk Management Framework 1.0

- **类型**：官方 AI 生命周期治理框架。
- **支持**：Govern/Map/Measure/Manage、roles、context、affected parties、monitoring 与 risk tolerance，补足单一 metric 视角。
- **限制**：自愿且非行业专属；不自动满足法律或公平定理。
- **URL**：https://www.nist.gov/itl/ai-risk-management-framework

### EA18 — EU AI Act official legal text

- **类型**：欧盟官方法规。
- **支持**：按用途/风险设置禁止与义务；技术 metric 之外还有 authority、documentation、human oversight、rights 与 enforcement。
- **限制**：适用范围和实施时间需按系统/日期核对；不能当全球统一伦理定义。
- **URL**：https://eur-lex.europa.eu/eli/reg/2024/1689/oj

## 使用边界汇总

- theorem 只在其定义与假设内成立；normative choice 不会由 theorem 自动给出。
- privacy、fairness、validity、interpretability 和 institutional rights 分账，不做可互相抵消的总分。
- 高风险系统的“metric pass”不能取代合法目的、正当程序、受影响人参与、补救与停止权。
- 新法、动态部署和反馈会改变结论；使用时重新核对日期、法域与运行分布。
