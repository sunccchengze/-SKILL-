# Research track 02｜安全、可靠性、约束与涌现

- **研究问题**：安全、可靠性、约束与涌现
- **来源层**：见 `../source-notes.md`；本文件不创建新的 A 层归因。
- **方法**：版本核对 + 机制拆分 + 支持/反证并列 + 工作流落地。

## 主要发现

1. 高可靠部件仍可不安全交互。
2. safety 是系统 emergent property；constraint 限制 mission 实现方式。
3. hazard 是系统状态，loss 是结果，scenario 是路径。
4. failure chains 可补充但不能穷尽复杂 causality。

## 归因与反证

- 原书主张、作者后续、独立证据和本包设计保持 A/B/C/D 分层。
- 发现支持机制候选，不把案例、报告完整度或专家一致当普遍因果证明。
- 与其他研究冲突时保留来源身份、方法和未决状态，不取无依据的中间值。

## 本轮造成的具体改变

- **workflow decision**：workflow 从 loss/hazard/constraint 开始，不从 components 开始。
- **failure gate**：hazard 写成 component failure 时拒绝进入 UCA。
- 这项改变已经进入 `SKILL.md`、CLI schema、模板或验证契约；不是扩写背景散文。

## 仍未验证

- 怎样与领域 PRA 接口由 assurance plan 决定。
- 本包的 D 层工作流尚无外部效度、可靠性或结果改善证明。
- 用户输入、领域法律和现实系统行为默认未核验。
