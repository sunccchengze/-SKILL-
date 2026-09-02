---
name: book-ethical-algorithm-constraints
description: |
  将 Michael Kearns 与 Aaron Roth《The Ethical Algorithm》（2019）转化为隐私、公平、策略响应、自适应分析与可解释性约束审计。
  当用户要把 differential privacy、fairness metrics、subgroup audit、performative/strategic response、reusable holdout 或 explanation 用于真实决策时使用。
  形式保证不是道德完备性：隐私参数、群体指标和解释必须绑定具体人群/权利/制度/伤害；遇到不可能性、规范冲突或高风险无申诉时停止或升级，不以一个技术分数批准系统。
---

# The Ethical Algorithm Constraint Audit

> 基于 Michael Kearns & Aaron Roth, *The Ethical Algorithm: The Science of Socially Aware Algorithm Design*（Oxford University Press, 2019）。原书五个主题可概括为隐私、算法公平、策略性行为、适应性/可复用数据分析、伦理算法前景。作者亦承认隐私形式化比公平与可解释性更成熟。本包把形式工具置于制度、权利与可争辩价值之中。

## 何时调用

- 要设 differential privacy 的 unit、neighboring relation、epsilon/delta、composition 与 release policy；
- 要选 demographic parity、equalized odds、calibration、individual/subgroup fairness，却未说明伤害与权利；
- 用户要求“同时满足所有公平指标”或把一个 fairness score 当正义；
- 部署会改变人/机构行为，需要 strategic classification、gaming 或 performative prediction 分析；
- 同一 holdout 被反复查询/调参，或持续监控让验证集成为训练反馈；
- 用 feature importance、post-hoc explanation 或 interpretable model 作为高风险决定的全部正当性。

不用于：给系统盖“ethical”印章；替代受影响人参与、反歧视/隐私法律、正当程序、领域安全或组织问责。

## 原作与独立证据的角色

- **原作/作者议程**：展示社会价值的一部分可转成可计算约束/保证，并把 privacy、fairness、strategic response、adaptivity 连接起来。
- **独立数学结果**：DP 基础、fairness incompatibility、subgroup gerrymandering、adaptive holdout、performative prediction 说明工具能保证什么以及为什么会失败。
- **独立批评**：形式化会提高明确性和执行性，也会把 contestable target、institutional power、文化语境与 lived harm 压到模型外。
- **本包综合**：`CONSTRAIN-ACT`、多账本决议、CLI 和停止门属于本 Skill，不冒充作者逐字要求。

## 一、六个心智模型

### 模型1：A guarantee is conditional on its formal object｜保证只覆盖形式对象

DP 保证依赖 privacy unit、neighboring relation、mechanism、epsilon/delta 与 composition；fairness 保证依赖 group、outcome/label、threshold、metric 和 evaluation population。先写对象，再写数字。

- **局限/失效**：对象选错时，数学证明仍可完全正确却保护错的人、错的事件或错的权利。

### 模型2：Privacy is bounded participation influence, not secrecy｜隐私是参与影响界，不是保密万能罩

differential privacy 限制相邻数据集输出分布差异，并有 composition/post-processing 性质；它不保证数据库安全、不隐藏群体事实、不自动取得同意或提供情境适当性。

- **局限/失效**：epsilon 解释、delta、重复查询、辅助信息、unit 和 central/local trust model 都会改变实际保护。

### 模型3：Fairness metrics are harm proxies with incompatible commitments｜公平指标是带冲突承诺的伤害代理

calibration、error-rate parity、selection parity、individual/subgroup notions回答不同规范问题；当 base rates 不同时，某些组合除完美/退化情况外不能同时满足。

- **局限/失效**：不可能性定理不告诉组织该选哪个价值；group parity 也不保证个体正义、因果正义或所有交叉群体。

### 模型4：People and institutions respond to scores｜评分会改变被评分世界

人会投资、规避、申诉、退出，机构会改阈值与采集；部署分布因此不同于训练分布。策略响应可能是 gaming，也可能是有价值的适应或对不公制度的抵抗。

- **局限/失效**：响应模型常简化成本、信息和权力；把所有反应都叫操纵会惩罚最受约束者。

### 模型5：Adaptive analysis spends validity｜自适应分析会消耗有效性

反复查看 holdout 后调参会把它变成训练信号。可复用 holdout/DP-inspired 方法能在特定查询模型下控制过拟合，但不是无限次免检。

- **局限/失效**：理论假设、查询类型和实现边界不匹配时，形式有效性不迁移；现实分布漂移又是另一问题。

### 模型6：Interpretability is a relation among model, person, task, and institution｜解释是关系，不是图

解释要问给谁、为哪项权利/任务、是否 faithful/stable/actionable、能否支持 contest 与 remedy。高风险场景应优先可验证机制与流程，而非事后故事。

- **局限/失效**：可解释模型也可建在不正当目标上；复杂模型的忠实解释可能仍不被人理解或不能纠正决定。

## 二、A/B/C/D 声明分层

- **A｜原作层**：五章结构与作者 formalization 议程，定位 `EA01–EA02`。
- **B｜原作内部限定层**：作者承认 privacy 比 fairness/explainability 更成熟，形式工具仍有 scope。
- **C｜独立证据层**：DP、fairness 不可能性、subgroup audit、adaptive/performative 研究和 institutional critique，定位 `EA03+`。
- **D｜Skill 推论层**：本 Skill 的 constraint canvas、trade-off minute、停止门和 CLI；不能写“作者证明系统 ethical”。

完整 18 条 ledger：[`references/claim-layer-map.md`](references/claim-layer-map.md)。A/B/C 可有冲突；D 必须显示冲突如何进入决议。

## 三、CONSTRAIN-ACT 十四步工作流

### 1. CONTEXT｜冻结决定与制度

写 system、decision、owner、legal/organizational authority、stakes、时间、替代、非自动化方案。若目标本身不可接受，优化约束没有意义。

### 2. AFFECTED｜列权利主体而非只列“用户”

列被决定者、数据主体、非用户、代理人、工作人员、交叉群体与未来受影响人；记录哪些群体没有数据/代表，谁可真正退出。

### 3. HARMS/RIGHTS｜先做不可抵消账本

分列 privacy、歧视、物质机会、尊严/污名、表达、身体/安全、正当程序、集体/群体伤害。高严重伤害不得被平均 utility 抵消。

### 4. FORMAL OBJECT｜把价值翻译成可争辩对象

每项约束写：对象、单位、人群、标签/结果、metric、threshold/budget、时间窗、assumption、证明/测试方法、owner、失败意义。记录翻译丢失了什么。

### 5. PRIVACY｜建立 release ledger

定义 privacy unit 与 neighboring relation；选择 central/local model、epsilon/delta、mechanism、sensitivity、query/release 次数、composition accountant、访问/删除/安全/consent 的非 DP 控制。不得只填 epsilon。

### 6. FAIRNESS｜从伤害选指标，不从工具箱选

把 harm pathway 映射到 selection、error、calibration、ranking、allocation、individual/subgroup 目标；报告 numerator/denominator、uncertainty、base rates 与 label validity。

### 7. IMPOSSIBILITY｜显式跑冲突门

若 calibration 与 equalized odds 等目标在 differing base rates 下冲突，提交 feasibility 证据与 trade-off memo；不能暗改阈值后声称“都公平”。

### 8. SUBGROUP｜防 fairness gerrymandering

预声明保护组与交叉组，同时设置可搜索 subgroup class、样本量、multiplicity、privacy、解释责任与发现后 remedy。更丰富审计会增加计算与统计负担。

### 9. STRATEGY｜模拟响应与反制反馈

列谁看到分数、可采取何行动、成本由谁承担、响应是否 desirable、是否转移伤害、机构会怎么改规则。不要把受影响人合理适应一概称作弊。

### 10. PERFORMATIVITY｜把 deployment 当干预

画预测→决定→资源/行为→新数据→再训练链；定义稳定性假设、monitor、lag、counterfactual/causal 评估和停止条件。offline accuracy 不等于长期系统表现。

### 11. ADAPTIVITY｜管理验证预算

登记每次 holdout 查询、谁看到结果、如何影响下一版本、fresh lockbox、可复用机制与外部复制。频繁 dashboard 也可能成为适应性泄漏。

### 12. INTERPRETABILITY/DUE PROCESS｜把解释接到权利

为 affected person、operator、auditor、court/regulator 分别写解释需求；测试 fidelity、stability、comprehension、contestability。必须有 notice、人工复核、申诉和 correction trail。

### 13. RESIDUAL/INSTITUTION｜列形式化外部

记录没被 metric 表达的制度权力、文化语境、历史分类、worker discretion、资源限制、法律争议和 lived harm；邀请受影响代表并保留 minority report。

### 14. ACT/REVIEW｜做可逆决定

状态只允许 `BLOCKED_CONSTRAINT_SPECIFICATION`、`TRADEOFF_DECISION_REQUIRED`、`GOVERNANCE_REVIEW_REQUIRED`。指定 owner、stop/rollback、remedy budget、复审日与退役。

## 四、三本不可合并的账

### Privacy ledger

记录 unit、neighbors、epsilon/delta、mechanism、sensitivity、composition、release、access/security、consent/context。DP 账不能用公平改善抵消。

### Fairness/harm ledger

逐群体记录 harm、metric、label validity、base rate、threshold、errors、uncertainty、impossibility 与 remedy。不得合并成一个 fairness score。

### Institutional rights ledger

记录 authority、purpose limitation、notice、appeal、human authority、worker/community voice、audit access、compensation、stop power。形式准确率不能替代此账。

## 五、硬停止与升级门

| 触发 | 状态/动作 |
|---|---|
| 写 epsilon 却无 privacy unit/neighboring relation/composition | `BLOCKED_CONSTRAINT_SPECIFICATION` |
| 公平目标无群体、伤害、label validity 或分母 | `BLOCKED_CONSTRAINT_SPECIFICATION` |
| differing/unknown base rates 下要求兼得相冲突指标 | `TRADEOFF_DECISION_REQUIRED` |
| 中高风险却未建 strategic/performative monitor | `BLOCKED_CONSTRAINT_SPECIFICATION` |
| 重复使用 holdout 却无 query ledger/fresh control | `BLOCKED_CONSTRAINT_SPECIFICATION` |
| 高风险无 notice、人工复核、申诉、停止 | `BLOCKED_CONSTRAINT_SPECIFICATION` |
| 只给 post-hoc explanation 便要求部署 | 阻止；先做 fidelity、正当程序与目标合法性 |
| 规格完整 | 仍仅 `GOVERNANCE_REVIEW_REQUIRED`，不自动批准 |

## 六、关键不可能性与非银弹边界

- **Fairness incompatibility**：当群体 base rates 不同且预测非完美时，calibration 与某些 error-rate parity 通常无法同时满足。数学不替你选择权利与伤害优先级。
- **Fairness gerrymandering**：大组 parity 可隐藏交叉 subgroup 违规；扩大 subgroup class 又带来 sample、multiplicity、privacy 和计算难题。
- **DP boundary**：DP 控制指定相邻关系的边际参与泄漏；不防数据库入侵、不保证 secrecy/consent、不抹除群体推断，composition 会累积。
- **Adaptive validity**：可复用 holdout 处理特定适应性查询，不保证 concept drift、数据管道变化或无界探索。
- **Strategic/performative boundary**：部署会改变数据，稳定点依赖响应假设；模型均衡不等于社会正义。
- **Interpretability boundary**：解释可帮助诊断/申诉，却不能把非法目标、不可靠数据或无权机构变正当。

## 七、反证、替代解释与非迁移

- disparity 可能由 label bias、measurement、selection、threshold、资源分配或上游制度共同产生；这要求因果调查，不是为伤害开脱。
- metric 改善可能来自拒绝为某群体作决定、改变 denominator 或牺牲 calibration；报告 coverage 与 abstention。
- gaming 可能是合理努力、规避不公或信息不对称；政策反应要区分社会价值。
- explanation stability 在局部样本好，不代表真实运行分布或另一角色理解。
- 一个 jurisdiction 的 protected groups、legal basis、appeal rights 不能直接迁移。
- 实验 benchmark 的形式保证不自动迁移到 data pipeline、vendor components 和组织执行。

## 八、CLI：约束规格审计

```bash
python3 scripts/audit_constraint_system.py \
  --system "课程支持分配" --decision "提供额外辅导" \
  --affected-group "学生" --protected-group "按残障与语言交叉的学生" \
  --owner "学生服务负责人" --stakes low \
  --legal-basis "机构支持职责" --harm "支持机会不平等" \
  --privacy-unit "一名学生是否参与" \
  --neighboring-relation "数据集相差一名学生记录" \
  --epsilon 1.0 --delta 0.000001 --query-count 4 \
  --fairness-goal calibration --base-rate-difference unknown \
  --appeal-path "学生服务复核" --human-review "顾问检查语境" \
  --stop-condition "申诉差异超过预声明阈值"
```

CLI 不计算 epsilon 合理性、不测 fairness、不拟合 equilibrium、不验证解释；只检查规格缺口。任何完整输出仍非 moral/legal/deployment approval。

## 九、十组内在张力

1. **张力 1｜形式精确 vs 对象选择**：证明可严谨，保护对象仍可能由权力错误定义。
2. **张力 2｜隐私强度 vs 数据效用**：更强噪声可减参与泄漏，也会伤害小群体测量与服务。
3. **张力 3｜群体 parity vs calibration**：不同规范承诺在 base rates 不同时可能不可兼得。
4. **张力 4｜大组稳定 vs 交叉群体可见**：细分揭示伤害，也增加不确定性与隐私风险。
5. **张力 5｜策略稳健 vs 人的能动性**：防操纵可提升稳定，却可能压制合理适应/抗议。
6. **张力 6｜自适应创新 vs holdout 有效性**：迭代越多，验证信号越容易被学习。
7. **张力 7｜透明解释 vs 安全/隐私/可操纵**：更多披露可助申诉，也可能暴露他人或系统漏洞。
8. **张力 8｜可解释模型 vs 预测性能**：实际并非总有固定 trade-off，必须按任务实证而非口号。
9. **张力 9｜优化福利 vs 不可抵消权利**：平均收益不能买断尊严、歧视或正当程序。
10. **张力 10｜统一标准 vs 地方合法性**：通用 metric 便于工程，法律、文化和历史伤害却不可移植。

## 十、表达DNA

- **句式**：先说“这个保证对哪个 formal object、在什么 assumption 下成立”，再说社会意义。
- **词汇**：neighboring relation、composition、harm pathway、base rate、impossibility、subgroup、performative、remedy。
- **语气**：不反数学，也不以数学消除规范争议；把 unresolved value choice 写出来。
- **节奏**：制度目的 → 权利/伤害 → 形式对象 → 可行/冲突 → 动态 → 有效性 → 正当程序 → 决议。
- **确定性**：区分 theorem、empirical result、normative choice、institutional fact 与本 Skill gate。
- **引用**：作者 agenda、独立 theorem/实证、批评与 D 层操作不混写。

## 十一、诚实边界

- 形式保证不是道德完备性；constraint satisfied 不等于 system just、合法或值得部署。
- differential privacy 不等于 secrecy、security、consent、purpose limitation 或群体隐私。
- fairness metric 不能独立决定“公平”的正确含义；冲突须由可问责制度决议。
- subgroup audit 会受样本量、multiple testing、privacy 和搜索 class 限制，不能保证发现所有伤害。
- strategic/performative 模型是对响应的简化，不应把弱势人的合理行为污名化为 gaming。
- reusable holdout 不提供无限验证预算，也不解决未来 drift。
- explanation 不能修复非法目标、坏标签、隐藏供应链或无申诉权。
- 本包不替代法律、人权、领域安全、劳动/公众参与、采购问责或独立审计。

## 十二、来源与执行导航

- [包说明](README.md)
- [参考导航](references/README.md)
- [18 条 A/B/C/D 声明](references/claim-layer-map.md)
- [来源卡与不可能性](references/source-notes.md)
- [约束、权利与决议模板](references/templates.md)
- [六轮研究日志](references/research/01-source-architecture.md)
- [验证记录](VALIDATION.md)
