# Research track 02｜反事实 effect 与识别条件

- **研究问题**：反事实 effect 与识别条件
- **来源层**：见 `../source-notes.md`；本文件不创建新的 A 层归因。
- **方法**：版本核对 + 机制拆分 + 支持/反证并列 + 工作流落地。

## 主要发现

1. effect 必须绑定 target、strategies、outcome、time、contrast。
2. consistency 定义版本并连接 observed 与 counterfactual。
3. exchangeability 依赖实质知识，不能数据内验证。
4. positivity 相对 target、L 与方法；样本稀疏和结构零分开。

## 归因与反证

- 原书主张、作者后续、独立证据和本包设计保持 A/B/C/D 分层。
- 发现支持机制候选，不把案例、报告完整度或专家一致当普遍因果证明。
- 与其他研究冲突时保留来源身份、方法和未决状态，不取无依据的中间值。

## 本轮造成的具体改变

- **workflow decision**：CLI 强制 estimand 与至少三条 assumption。
- **failure gate**：不得把假设状态输出 verified；只能 asserted/challenged/incompatible。
- 这项改变已经进入 `SKILL.md`、CLI schema、模板或验证契约；不是扩写背景散文。

## 仍未验证

- 干扰、测量误差与 missingness 的领域化处理。
- 本包的 D 层工作流尚无外部效度、可靠性或结果改善证明。
- 用户输入、领域法律和现实系统行为默认未核验。
