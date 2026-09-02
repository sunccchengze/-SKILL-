# Research track 06｜causal ML、高影响与发布边界

- **研究问题**：causal ML、高影响与发布边界
- **来源层**：见 `../source-notes.md`；本文件不创建新的 A 层归因。
- **方法**：版本核对 + 机制拆分 + 支持/反证并列 + 工作流落地。

## 主要发现

1. prediction P(Y|X) 与 intervention distribution 不同。
2. 模型异质性结果也依识别/多重探索。
3. 真实影响、分群伤害、owner、rule、appeal、stop/rollback 属决定层。
4. 报告清单改善透明度但不保证效度。

## 归因与反证

- 原书主张、作者后续、独立证据和本包设计保持 A/B/C/D 分层。
- 发现支持机制候选，不把案例、报告完整度或专家一致当普遍因果证明。
- 与其他研究冲突时保留来源身份、方法和未决状态，不取无依据的中间值。

## 本轮造成的具体改变

- **workflow decision**：高影响门字段缺失 code 2；齐全仍 governance_review_required。
- **failure gate**：任何结果不得自动触发人员/临床/信用/执法行动。
- 这项改变已经进入 `SKILL.md`、CLI schema、模板或验证契约；不是扩写背景散文。

## 仍未验证

- 需现实使用者测试 TARGET 制品的可理解性。
- 本包的 D 层工作流尚无外部效度、可靠性或结果改善证明。
- 用户输入、领域法律和现实系统行为默认未核验。
