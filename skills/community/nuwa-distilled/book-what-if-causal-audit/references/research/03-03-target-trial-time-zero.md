# Research track 03｜七项协议与 time-zero 对齐

- **研究问题**：七项协议与 time-zero 对齐
- **来源层**：见 `../source-notes.md`；本文件不创建新的 A 层归因。
- **方法**：版本核对 + 机制拆分 + 支持/反证并列 + 工作流落地。

## 主要发现

1. 协议七项逐一对应 emulation。
2. eligibility、assignment、follow-up 对齐可防 immortal-time 等 self-inflicted bias。
3. active-comparator/new-user 是常见设计工具，不是普适要求。
4. TTE 不修复 residual confounding 或 measurement error。

## 归因与反证

- 原书主张、作者后续、独立证据和本包设计保持 A/B/C/D 分层。
- 发现支持机制候选，不把案例、报告完整度或专家一致当普遍因果证明。
- 与其他研究冲突时保留来源身份、方法和未决状态，不取无依据的中间值。

## 本轮造成的具体改变

- **workflow decision**：输出固定 ideal target trial + emulation 两层。
- **failure gate**：共同 time zero 不可定义则改问题或停止。
- 这项改变已经进入 `SKILL.md`、CLI schema、模板或验证契约；不是扩写背景散文。

## 仍未验证

- 动态宽限期/克隆策略需专项统计设计。
- 本包的 D 层工作流尚无外部效度、可靠性或结果改善证明。
- 用户输入、领域法律和现实系统行为默认未核验。
