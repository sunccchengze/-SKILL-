# Research track 03｜层级控制结构与过程模型

- **研究问题**：层级控制结构与过程模型
- **来源层**：见 `../source-notes.md`；本文件不创建新的 A 层归因。
- **方法**：版本核对 + 机制拆分 + 支持/反证并列 + 工作流落地。

## 主要发现

1. controller 可为监管、管理、人、自动化；control 是广义约束影响。
2. loop 需 action、feedback、process model、algorithm、delay。
3. development 与 operations 控制结构相互作用。
4. 协调缺口、错误反馈和模型错配可在无 failure 时致险。

## 归因与反证

- 原书主张、作者后续、独立证据和本包设计保持 A/B/C/D 分层。
- 发现支持机制候选，不把案例、报告完整度或专家一致当普遍因果证明。
- 与其他研究冲突时保留来源身份、方法和未决状态，不取无依据的中间值。

## 本轮造成的具体改变

- **workflow decision**：CLI 要求 controller/action/feedback 并保留 authority/model TODO。
- **failure gate**：无 feedback/authority 的责任声明标 structural gap。
- 这项改变已经进入 `SKILL.md`、CLI schema、模板或验证契约；不是扩写背景散文。

## 仍未验证

- 复杂组织的真实 informal influence 难完整建模。
- 本包的 D 层工作流尚无外部效度、可靠性或结果改善证明。
- 用户输入、领域法律和现实系统行为默认未核验。
