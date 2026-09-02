# Research track 04｜DAG、混杂、选择与坏控制

- **研究问题**：DAG、混杂、选择与坏控制
- **来源层**：见 `../source-notes.md`；本文件不创建新的 A 层归因。
- **方法**：版本核对 + 机制拆分 + 支持/反证并列 + 工作流落地。

## 主要发现

1. 图公开因果假设而不证明箭头。
2. confounder、mediator、collider、instrument、selection 的调整含义不同。
3. 同一变量角色随 estimand 与时间改变。
4. 只按预测重要度选择控制变量会打开/阻断错误路径。

## 归因与反证

- 原书主张、作者后续、独立证据和本包设计保持 A/B/C/D 分层。
- 发现支持机制候选，不把案例、报告完整度或专家一致当普遍因果证明。
- 与其他研究冲突时保留来源身份、方法和未决状态，不取无依据的中间值。

## 本轮造成的具体改变

- **workflow decision**：加入 time-indexed role table 与 competing DAG。
- **failure gate**：post-treatment 变量无说明不得作为 baseline confounder。
- 这项改变已经进入 `SKILL.md`、CLI schema、模板或验证契约；不是扩写背景散文。

## 仍未验证

- 自动 causal discovery 的适用边界未纳入 CLI。
- 本包的 D 层工作流尚无外部效度、可靠性或结果改善证明。
- 用户输入、领域法律和现实系统行为默认未核验。
