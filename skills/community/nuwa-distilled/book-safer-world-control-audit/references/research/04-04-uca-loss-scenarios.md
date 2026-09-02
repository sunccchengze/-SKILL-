# Research track 04｜四类 UCA 与 loss scenarios

- **研究问题**：四类 UCA 与 loss scenarios
- **来源层**：见 `../source-notes.md`；本文件不创建新的 A 层归因。
- **方法**：版本核对 + 机制拆分 + 支持/反证并列 + 工作流落地。

## 主要发现

1. 每个 CA 检查 omission/provision/timing/duration。
2. UCA 写 actual context + hazard，而非原因。
3. scenario 再绕 controller/input/model/feedback/path/process/environment。
4. 正确 action 也可能因执行路径/controlled process 失效而致险。

## 归因与反证

- 原书主张、作者后续、独立证据和本包设计保持 A/B/C/D 分层。
- 发现支持机制候选，不把案例、报告完整度或专家一致当普遍因果证明。
- 与其他研究冲突时保留来源身份、方法和未决状态，不取无依据的中间值。

## 本轮造成的具体改变

- **workflow decision**：CLI 对每个 CA 确定性生成四类候选槽。
- **failure gate**：候选永远 candidate_not_validated；无 trace 不转 requirement。
- 这项改变已经进入 `SKILL.md`、CLI schema、模板或验证契约；不是扩写背景散文。

## 仍未验证

- 多 action 组合与级联需补充方法。
- 本包的 D 层工作流尚无外部效度、可靠性或结果改善证明。
- 用户输入、领域法律和现实系统行为默认未核验。
