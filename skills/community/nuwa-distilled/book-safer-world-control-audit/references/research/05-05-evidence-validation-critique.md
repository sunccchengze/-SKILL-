# Research track 05｜比较证据、互补与验证限制

- **研究问题**：比较证据、互补与验证限制
- **来源层**：见 `../source-notes.md`；本文件不创建新的 A 层归因。
- **方法**：版本核对 + 机制拆分 + 支持/反证并列 + 工作流落地。

## 主要发现

1. 案例常报告 STPA 多找交互/软件/组织因素。
2. FMEA/STPA 个案也显示 focus 不同且互补。
3. 独立评估指出 completeness、requirement derivation、duplicate 与 V&V 问题。
4. 验证框架仍是发展中 formative practice。

## 归因与反证

- 原书主张、作者后续、独立证据和本包设计保持 A/B/C/D 分层。
- 发现支持机制候选，不把案例、报告完整度或专家一致当普遍因果证明。
- 与其他研究冲突时保留来源身份、方法和未决状态，不取无依据的中间值。

## 本轮造成的具体改变

- **workflow decision**：加入 independent challenge、verification evidence 与 no-completeness 声明。
- **failure gate**：不得用场景数量宣称 superiority/safety。
- 这项改变已经进入 `SKILL.md`、CLI schema、模板或验证契约；不是扩写背景散文。

## 仍未验证

- 缺少大规模受控效果比较。
- 本包的 D 层工作流尚无外部效度、可靠性或结果改善证明。
- 用户输入、领域法律和现实系统行为默认未核验。
