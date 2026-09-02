# Research Pass — CONSTRAIN-ACT 操作综合

## 目标

把五轮研究变成多账本约束审计、确定性 CLI、模板和红队测试，并确保形式保证不被包装成道德完备性。

## 输入与方法

逐条检查 A-ETH/B-ETH/C-ETH 到 D-ETH 的依赖。红队 DP 缺 neighbor/composition、公平冲突/缺群体、高风险无 due process、动态缺口、holdout reuse 和非法参数。

## 主要发现

形成十四步 CONSTRAIN-ACT、八类模板与状态机。blocks 优先于 tradeoff；完整规格仍只到 GOVERNANCE_REVIEW_REQUIRED。privacy、fairness/harm、institutional rights 三账不可互相抵消。

## 反证与边界

CLI 只检查字段，不能评判 epsilon 合理性、证明 fairness 数据、预测 equilibrium 或验证 explanation。参与代表性和机构合法性仍可能失败。

## 设计决议

纳入 exact 18-claim ledger、18 source cards、六轮日志和 12 个测试。复审触发包括 law/purpose/group/label/base-rate/query budget/response 或 vendor change。

## 纳入产物

本轮进入 `SKILL.md` 的 CONSTRAIN-ACT 步骤/停止门、`source-notes.md` 的来源卡、`claim-layer-map.md` 的对应 claim、`templates.md` 的强制字段，并至少由一个 adversarial test 或仓库集成断言约束。没有把研究日志当引用终点；最终输出仍须回链原始 source ID。

## 未解决

- 用户场景的本地数据、组织记录、受影响人证据和合法 authority 尚未知；不能由本轮桌面研究代填。
- 动态网页、软件、法律与在线书版本会变化；复用时重查基准日并记录差异。
- 形式字段可能被合规表演式填写；需要独立复核、反证、minority report 和可执行 stop/rollback。
