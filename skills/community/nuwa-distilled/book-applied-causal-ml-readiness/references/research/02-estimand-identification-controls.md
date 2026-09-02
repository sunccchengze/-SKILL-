# Research Pass — Estimand、识别与控制变量

## 目标

研究为何 prediction 不能替代 counterfactual identification，并把 treatment versions、time zero、exchangeability、consistency、positivity、interference 与 variable timing 转成分析合同。

## 输入与方法

对照 CM09 的系统因果定义、CM15 的 target-trial 设计纪律与 CM13 的 interference 结果；用原作框架定位，而不从 feature importance 或自动 DAG 学习推断因果方向。

## 主要发现

estimand 必须包含 population、unit、treatment、comparator、outcome、time zero/horizon 和 aggregation。post-treatment mediator/collider 作为控制会改问题或造偏；randomized 标签也要核实际分配。C-CML-06 说明有 spillover 时应重定义暴露和效应。

## 反证与边界

DAG 是可争辩模型，很多关键假设不可完全检验。target-trial emulation 能避免部分 immortal-time/设计错位，却不消除隐藏混杂；cluster standard errors 也不能自动解决 interference 定义。

## 设计决议

D-CML-01 决定先写 estimand card、timeline 与 identification table；post-treatment control、可信 hidden confounding 与未建模 interference 分别触发硬阻断。

## 纳入产物

本轮进入 `SKILL.md` 的 IDENTIFY-DML 步骤/停止门、`source-notes.md` 的来源卡、`claim-layer-map.md` 的对应 claim、`templates.md` 的强制字段，并至少由一个 adversarial test 或仓库集成断言约束。没有把研究日志当引用终点；最终输出仍须回链原始 source ID。

## 未解决

- 用户场景的本地数据、组织记录、受影响人证据和合法 authority 尚未知；不能由本轮桌面研究代填。
- 动态网页、软件、法律与在线书版本会变化；复用时重查基准日并记录差异。
- 形式字段可能被合规表演式填写；需要独立复核、反证、minority report 和可执行 stop/rollback。
