# Research track 05｜形式化、实证与 vulnerability 限制

- **研究问题**：形式化、实证与 vulnerability 限制
- **来源层**：见 `../source-notes.md`；本文件不创建新的 A 层归因。
- **方法**：版本核对 + 机制拆分 + 支持/反证并列 + 工作流落地。

## 主要发现

1. temporal logic 可表达部分 flow norms，不会自动选正当规范。
2. policy annotation 能暴露 missing/vague/bloated parameters。
3. crowd expectations 受样本/措辞/文化影响。
4. 弱势群体缺席会让 norm consensus 许可不平等。

## 归因与反证

- 原书主张、作者后续、独立证据和本包设计保持 A/B/C/D 分层。
- 发现支持机制候选，不把案例、报告完整度或专家一致当普遍因果证明。
- 与其他研究冲突时保留来源身份、方法和未决状态，不取无依据的中间值。

## 本轮造成的具体改变

- **workflow decision**：加入 norm evidence ledger 与 missing voice/power/unequal impact。
- **failure gate**：多数预期、企业 policy 或逻辑 entailment不得等于 legitimacy。
- 这项改变已经进入 `SKILL.md`、CLI schema、模板或验证契约；不是扩写背景散文。

## 仍未验证

- 如何给弱势证言制度权重。
- 本包的 D 层工作流尚无外部效度、可靠性或结果改善证明。
- 用户输入、领域法律和现实系统行为默认未核验。
