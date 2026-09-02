# Research Pass — 版本、范围与体裁

## 目标

锁定官方 online version 0.1.2（2026-05-03），并把项目首次公开、当前在线版本、出版社首版这些不同概念拆开。确认目录、受众、代码与练习定位，而不把教材定位当效果证据。

## 输入与方法

以 CM01 官网、CM02 官方 preface 和 CM03 arXiv 元数据三角校验。官网负责当前状态，preface 负责作者定位，arXiv 负责历史版本；没有用二手书评填作者主张。

## 主要发现

公开稿 first submitted 2024-03-04，而当前站点标 v0.1.2 dated 2026-05-03。目录覆盖 Chapter 0–17，面向 advanced undergraduate 至博士/应用研究者，并提供 R/Python notebooks 与练习。A-CML-01 至 A-CML-03 因而可定位。

## 反证与边界

在线出版会更新，页面日期不是传统纸本首版；notebook 可运行也不证明用户数据识别有效。后续版本可能改章节，引用必须锁版本、访问日和具体章节。

## 设计决议

将“书籍摘要”改为 IDENTIFY-DML readiness lab：原作只提供 A/B 层内容，独立论文承载 C 层，操作门留在 D 层。体裁声明进入 SKILL 顶部和 source notes。

## 纳入产物

本轮进入 `SKILL.md` 的 IDENTIFY-DML 步骤/停止门、`source-notes.md` 的来源卡、`claim-layer-map.md` 的对应 claim、`templates.md` 的强制字段，并至少由一个 adversarial test 或仓库集成断言约束。没有把研究日志当引用终点；最终输出仍须回链原始 source ID。

## 未解决

- 用户场景的本地数据、组织记录、受影响人证据和合法 authority 尚未知；不能由本轮桌面研究代填。
- 动态网页、软件、法律与在线书版本会变化；复用时重查基准日并记录差异。
- 形式字段可能被合规表演式填写；需要独立复核、反证、minority report 和可执行 stop/rollback。
