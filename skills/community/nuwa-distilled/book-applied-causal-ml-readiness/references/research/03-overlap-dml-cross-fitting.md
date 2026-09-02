# Research Pass — Overlap、DML 与 cross-fitting

## 目标

把 DML 的有效作用范围与常见“因果魔杖”误解分开，同时确定 overlap、split、nuisance evaluation 和 estimator specification 的顺序。

## 输入与方法

读取 CM04 DML 原始论文、CM05 实施文档、CM06 独立比较与 CM07 limited-overlap 方法。理论、软件与比较研究分别负责机制、实现和反例。

## 主要发现

orthogonal score 降低目标对 nuisance 误差的一阶敏感性，cross-fitting 减少同样本过拟合路径；两者仍需识别、支持域、矩条件与 learner 质量。有限 overlap 会产生极端权重；trim 后目标 population 已变化。C-CML-01 与 C-CML-02 因而绑定。

## 反证与边界

in-sample AUC 高不保证 OOF nuisance 适用，更不保证效应无偏。默认 fold 会破坏时间/cluster 独立性；固定 clipping 可藏支持失败。CM06 的场景比较不能证明一个 learner 普遍最优。

## 设计决议

IDENTIFY-DML 把 overlap 放在 estimator 前，并要求 outcome-blind diagnostics、split manifest、OOF nuisance scorecard、baseline estimator 和实现版本。CLI 的 --use-dml 同时要求 split-plan 与 nuisance-evaluation。

## 纳入产物

本轮进入 `SKILL.md` 的 IDENTIFY-DML 步骤/停止门、`source-notes.md` 的来源卡、`claim-layer-map.md` 的对应 claim、`templates.md` 的强制字段，并至少由一个 adversarial test 或仓库集成断言约束。没有把研究日志当引用终点；最终输出仍须回链原始 source ID。

## 未解决

- 用户场景的本地数据、组织记录、受影响人证据和合法 authority 尚未知；不能由本轮桌面研究代填。
- 动态网页、软件、法律与在线书版本会变化；复用时重查基准日并记录差异。
- 形式字段可能被合规表演式填写；需要独立复核、反证、minority report 和可执行 stop/rollback。
