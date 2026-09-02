# Research track 05｜g-methods、估计与诊断

- **研究问题**：g-methods、估计与诊断
- **来源层**：见 `../source-notes.md`；本文件不创建新的 A 层归因。
- **方法**：版本核对 + 机制拆分 + 支持/反证并列 + 工作流落地。

## 主要发现

1. standardization/IPW/MSM/g-formula/g-estimation 回答不同结构。
2. time-varying confounding affected by prior treatment 不能机械普通调整。
3. overlap、balance、weights、ESS、missingness、negative controls 是诊断。
4. DML 放松 nuisance 函数形式，不放松识别。

## 归因与反证

- 原书主张、作者后续、独立证据和本包设计保持 A/B/C/D 分层。
- 发现支持机制候选，不把案例、报告完整度或专家一致当普遍因果证明。
- 与其他研究冲突时保留来源身份、方法和未决状态，不取无依据的中间值。

## 本轮造成的具体改变

- **workflow decision**：方法字段保持 TODO 直到 estimand/graph/assumptions 完成。
- **failure gate**：诊断通过不得改写为 causal proof。
- 这项改变已经进入 `SKILL.md`、CLI schema、模板或验证契约；不是扩写背景散文。

## 仍未验证

- 各 estimator 的小样本/高维性质需领域统计评审。
- 本包的 D 层工作流尚无外部效度、可靠性或结果改善证明。
- 用户输入、领域法律和现实系统行为默认未核验。
