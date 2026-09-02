# Research track 06｜AI/LES 应用与运营风险迁移

- **研究问题**：AI/LES 应用与运营风险迁移
- **来源层**：见 `../source-notes.md`；本文件不创建新的 A 层归因。
- **方法**：版本核对 + 机制拆分 + 支持/反证并列 + 工作流落地。

## 主要发现

1. LES/AI 扩展是后续研究，不是 © 2011/正式出版 2012 原书的预测。
2. AI 系统仍含人、组织、供应商、评估、工具与监管 controllers。
3. LLM 可辅助枚举但会幻觉、遗漏和格式服从失败。
4. 上线后压力、更新和反馈时滞需 leading indicators/CAST。

## 归因与反证

- 原书主张、作者后续、独立证据和本包设计保持 A/B/C/D 分层。
- 发现支持机制候选，不把案例、报告完整度或专家一致当普遍因果证明。
- 与其他研究冲突时保留来源身份、方法和未决状态，不取无依据的中间值。

## 本轮造成的具体改变

- **workflow decision**：高风险强制真实影响、独立复核、owner、appeal、stop/rollback。
- **failure gate**：LLM 不可签 safety requirement、risk acceptance 或 certification。
- 这项改变已经进入 `SKILL.md`、CLI schema、模板或验证契约；不是扩写背景散文。

## 仍未验证

- AI STPA 的外部效度与监管接受仍有限。
- 本包的 D 层工作流尚无外部效度、可靠性或结果改善证明。
- 用户输入、领域法律和现实系统行为默认未核验。
