# Research Pass — 异质性、敏感性与迁移

## 目标

研究平均效应之后最容易过度声称的三处：CATE 事后发现、未测混杂敏感性被当修复、study-to-target 外推被当默认。

## 输入与方法

使用 CM08 sensitivity、CM10 causal forest、CM11 policy learning 与 CM12 transportability。分别记录 theorem/estimand 条件、经验不可验证部分和规范福利选择。

## 主要发现

CATE 是条件平均而非观测个体反事实；honesty、support、multiplicity 与 confirmation 必须预声明。sensitivity 可表达需要多强 omitted confounding 才改结论，却不能证明它不存在。transport 要列 selection/effect modifiers 与 target support。C-CML-03 至 C-CML-05 承载这些边界。

## 反证与边界

policy value 依 welfare、cost、capacity 与 rights；离线表现不能覆盖战略反馈。敏感性数字会受模型尺度影响；target 域只匹配平均协变量不保证机制相同。

## 设计决议

CATE 缺计划触发阻断；transport target 缺 assumption 触发阻断；政策用途只能升级治理复核。模板强制区分 exploratory/confirmatory 和 study/target population。

## 纳入产物

本轮进入 `SKILL.md` 的 IDENTIFY-DML 步骤/停止门、`source-notes.md` 的来源卡、`claim-layer-map.md` 的对应 claim、`templates.md` 的强制字段，并至少由一个 adversarial test 或仓库集成断言约束。没有把研究日志当引用终点；最终输出仍须回链原始 source ID。

## 未解决

- 用户场景的本地数据、组织记录、受影响人证据和合法 authority 尚未知；不能由本轮桌面研究代填。
- 动态网页、软件、法律与在线书版本会变化；复用时重查基准日并记录差异。
- 形式字段可能被合规表演式填写；需要独立复核、反证、minority report 和可执行 stop/rollback。
