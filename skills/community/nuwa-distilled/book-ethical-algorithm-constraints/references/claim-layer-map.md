# Claim Layer Map — The Ethical Algorithm

固定分布：A=5、B=3、C=6、D=4，共 18 条。定理、实证、规范选择和本 Skill gate 不互相冒充。

| Claim ID | 层 | 声明 | 来源 | 关键限制 | 操作 |
|---|---|---|---|---|---|
| A-ETH-01 | A | 原书以 privacy fairness strategic behavior adaptive analysis 与 ethical algorithm 前景组织五章 | EA01 | 章节范围不等于伦理问题全集 | 建立形式化外部残余风险账 |
| A-ETH-02 | A | 作者议程主张部分社会价值可转化为算法约束和保证 | EA02 | 可形式化不说明形式对象选得正确 | 记录翻译丢失和决策权 |
| A-ETH-03 | A | 原书用 differential privacy 说明可证明隐私保证 | EA01, EA02 | 保证依 unit relation mechanism 和 composition | 禁止只报 epsilon |
| A-ETH-04 | A | 原书把策略性行为视为算法设计必须预期的反馈 | EA01 | 理论响应模型会简化权力和行动成本 | 区分 gaming 合理适应和抵抗 |
| A-ETH-05 | A | 原书把重复数据分析的过拟合纳入伦理算法讨论 | EA01 | 统计有效性不是社会正当性 | 单独维护 holdout query ledger |
| B-ETH-01 | B | 作者明确 privacy 的形式化成熟度高于 fairness 或 explainability | EA02 | 成熟度比较不等于 DP 解决全部隐私 | privacy 与 institutional rights 分账 |
| B-ETH-02 | B | 形式工具只能对定义好的对象和假设给保证 | EA02, EA03 | 定义过程本身包含规范权力 | 每项约束写 owner 和异议 |
| B-ETH-03 | B | 伦理算法研究议程仍是开放方向而非完成的道德编译器 | EA01, EA02 | 出版后的理论 法律与实践继续发展 | 使用 2026 独立证据更新 |
| C-ETH-01 | C | differential privacy 有 composition 和 post-processing 性质但不保护所有推断 | EA03, EA05 | 不等于安全 同意 情境适当或群体隐私 | 维护 release ledger 和非 DP 控制 |
| C-ETH-02 | C | differing base rates 下 calibration 与部分 error parity 目标通常不可兼得 | EA06, EA07 | 特定定义和非完美预测条件下成立 | 提交 trade-off decision 而非伪全通过 |
| C-ETH-03 | C | 粗群体 parity 可隐藏 intersectional subgroup 违规 | EA08 | 丰富审计受样本 计算 multiplicity 与隐私限制 | 预声明 subgroup class 与 remedy |
| C-ETH-04 | C | strategic 与 performative response 会使部署分布偏离训练分布 | EA11, EA12 | 响应和稳定性假设可能不现实 | 建 feedback monitor 和 stop trigger |
| C-ETH-05 | C | 适应性重复查询 holdout 会过拟合且受控机制仅在条件下延长有效性 | EA04 | 不是无限查询也不解决 drift | 登记查询并保留 fresh lockbox |
| C-ETH-06 | C | post-hoc explanation 与技术抽象可能掩盖 fidelity 制度权力和 lived harm | EA10, EA13, EA15, EA16 | 批评不否定所有形式工具 | 连接解释到申诉和制度审查 |
| D-ETH-01 | D | 本 Skill 规定 CONSTRAIN-ACT 先列权利伤害再选择 formal property | 本 Skill 综合 A-ETH-02, C-ETH-06 | 流程仍受参与代表性限制 | 保留 minority report 和无 AI 替代 |
| D-ETH-02 | D | 本 Skill 将 DP 缺 unit 邻接关系 composition 与公平缺群体伤害设为阻断 | 本 Skill 综合 C-ETH-01, C-ETH-02 | 字段完整不证明参数合理 | 由隐私权利领域专家复核 |
| D-ETH-03 | D | 本 Skill 将 fairness 不可能性转成显式 trade-off 决议而非单一总分 | 本 Skill 综合 C-ETH-02, C-ETH-03 | 决议主体仍可能缺乏合法性 | 记录 authority dissent remedy 与复审 |
| D-ETH-04 | D | 本 Skill 的 CLI 最高只到 GOVERNANCE_REVIEW_REQUIRED 不输出 ethical approval | 本 Skill 的确定性安全设计 | gate 不验证输入证据真实性 | 结合独立审计 法律与受影响人参与 |

## 使用规则

- theorem 行必须保留定义、假设和例外，禁止传播为“公平不可能”。
- metric 变化不等于 harm 变化；报告 coverage、abstention、label validity 和真实后果。
- D 层状态只检查 specification，不判断系统是否应存在。
