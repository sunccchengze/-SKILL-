# Research Pass — Earth、Space 与基础设施量化

## 目标

研究如何记录 energy、emissions、water、hardware、minerals 与 e-waste，又不制造单 prompt/model 的伪精确足迹。

## 输入与方法

比较 AT12 NIST 生命周期风险、AT13 训练排放、AT14 water 估算与 AT15 Green Algorithms。每个来源记录 scope、location、period、denominator 和 excluded lifecycle。

## 主要发现

环境结果高度依赖硬件、运行时间、PUE、能源/水地点与时间。facility/corporate total 与 product/model/prompt 是不同 analysis unit；跨层需要可审计 allocation method 和 uncertainty。C-ATL-05 由此形成。

## 反证与边界

论文常缺完整硬件供应链、运营商原始数据或退役；arXiv 水估算受假设限制。renewable matching 也不等于实时无边际影响。unknown 不能当 zero。

## 设计决议

建立 Earth claim card 和 Space node register；无 geography/date/denominator/allocation 的数字标 NOT_COMPARABLE 或 WITHDRAW_CLAIM。CLI 要求 claim-denominator 才完成 Earth lens。

## 纳入产物

本轮进入 `SKILL.md` 的 ATLAS-STACK 步骤/停止门、`source-notes.md` 的来源卡、`claim-layer-map.md` 的对应 claim、`templates.md` 的强制字段，并至少由一个 adversarial test 或仓库集成断言约束。没有把研究日志当引用终点；最终输出仍须回链原始 source ID。

## 未解决

- 用户场景的本地数据、组织记录、受影响人证据和合法 authority 尚未知；不能由本轮桌面研究代填。
- 动态网页、软件、法律与在线书版本会变化；复用时重查基准日并记录差异。
- 形式字段可能被合规表演式填写；需要独立复核、反证、minority report 和可执行 stop/rollback。
