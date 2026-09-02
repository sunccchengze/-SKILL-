# Research Pass — IDENTIFY-DML 操作综合

## 目标

把前五轮研究压成可复现工作流、模板、状态机和 adversarial tests，同时检查 D 层没有倒灌成作者主张。

## 输入与方法

逐条审 A-CML/B-CML/C-CML 到 D-CML 的依赖；把每个硬边界变成字段、状态或测试。对 ready case、post-treatment、hidden confounding、interference、CATE、transport 和 high-stakes 分别红队。

## 主要发现

最终形成十三步 IDENTIFY-DML、八类模板、确定性 JSON CLI。最高 READY_FOR_ESTIMATION_PLAN 只表示可以写估计计划；阻断状态具体指出设计失败；high-stakes 进入 GOVERNANCE_REVIEW_REQUIRED。

## 反证与边界

CLI 不读数据，无法识别提交者隐瞒的混杂或变量时序；测试只验证代码 gate，不验证证据真实性。任何 checklist 也可能被形式主义使用。

## 设计决议

纳入 exact 18-claim ledger、source cards、六轮日志和 12 个包内测试。复审触发包括原作版本更新、新外推场景、数据生成变化或政策用途变化。

## 纳入产物

本轮进入 `SKILL.md` 的 IDENTIFY-DML 步骤/停止门、`source-notes.md` 的来源卡、`claim-layer-map.md` 的对应 claim、`templates.md` 的强制字段，并至少由一个 adversarial test 或仓库集成断言约束。没有把研究日志当引用终点；最终输出仍须回链原始 source ID。

## 未解决

- 用户场景的本地数据、组织记录、受影响人证据和合法 authority 尚未知；不能由本轮桌面研究代填。
- 动态网页、软件、法律与在线书版本会变化；复用时重查基准日并记录差异。
- 形式字段可能被合规表演式填写；需要独立复核、反证、minority report 和可执行 stop/rollback。
