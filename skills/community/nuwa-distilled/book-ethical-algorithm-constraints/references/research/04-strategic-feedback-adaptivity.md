# Research Pass — 策略响应、performative feedback 与适应性有效性

## 目标

将人/机构响应和反复验证纳入系统设计，避免静态 test-set accuracy 直接外推部署。

## 输入与方法

EA11 strategic classification、EA12 performative prediction 与 EA04 reusable holdout 分别覆盖行为响应、分布反馈和 adaptive data analysis。

## 主要发现

评分可改变行动成本与行为，部署又改变下一轮数据；performative stable 不等于 welfare/justice。反复查看 holdout 会把反馈用于下一版，受控机制只能在特定 query/assumption 下延长有效性。C-ETH-04/C-ETH-05 固化。

## 反证与边界

理论 response model 简化权力；受影响人适应可能是合理努力或抵抗，不应一概叫 gaming。reusable holdout 不解决 concept drift、pipeline change 或外部 validity。

## 设计决议

中高风险必须列 strategic responses、feedback monitor、lag 和 stop。data-reuse >1 无 fresh/controlled holdout 时阻断；记录每次 query 如何影响版本。

## 纳入产物

本轮进入 `SKILL.md` 的 CONSTRAIN-ACT 步骤/停止门、`source-notes.md` 的来源卡、`claim-layer-map.md` 的对应 claim、`templates.md` 的强制字段，并至少由一个 adversarial test 或仓库集成断言约束。没有把研究日志当引用终点；最终输出仍须回链原始 source ID。

## 未解决

- 用户场景的本地数据、组织记录、受影响人证据和合法 authority 尚未知；不能由本轮桌面研究代填。
- 动态网页、软件、法律与在线书版本会变化；复用时重查基准日并记录差异。
- 形式字段可能被合规表演式填写；需要独立复核、反证、minority report 和可执行 stop/rollback。
