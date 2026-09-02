# Research track 03｜五参数与 transmission principle

- **研究问题**：五参数与 transmission principle
- **来源层**：见 `../source-notes.md`；本文件不创建新的 A 层归因。
- **方法**：版本核对 + 机制拆分 + 支持/反证并列 + 工作流落地。

## 主要发现

1. subject/sender/recipient 均需 context-relative role。
2. attribute 是有意义的信息类型，含 inferred data。
3. TP 是 consent/confidence/reciprocity/sale/coercion/warrant 等条件。
4. 缺参数会导致政策/判断含混。

## 归因与反证

- 原书主张、作者后续、独立证据和本包设计保持 A/B/C/D 分层。
- 发现支持机制候选，不把案例、报告完整度或专家一致当普遍因果证明。
- 与其他研究冲突时保留来源身份、方法和未决状态，不取无依据的中间值。

## 本轮造成的具体改变

- **workflow decision**：CLI 强制全部五参数且允许复数角色。
- **failure gate**：unknown 不猜；不完整 flow 标 incomplete。
- 这项改变已经进入 `SKILL.md`、CLI schema、模板或验证契约；不是扩写背景散文。

## 仍未验证

- 复杂多主体/group subject 本体。
- 本包的 D 层工作流尚无外部效度、可靠性或结果改善证明。
- 用户输入、领域法律和现实系统行为默认未核验。
