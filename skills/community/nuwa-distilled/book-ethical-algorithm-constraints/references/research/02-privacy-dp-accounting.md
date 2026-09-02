# Research Pass — Differential Privacy 与 release accounting

## 目标

明确 DP 保证对象、composition 与 non-DP controls，阻止“给一个 epsilon 就隐私合规”的错误。

## 输入与方法

以 EA03 DP 基础专著为 theorem 主体，EA05 NIST Privacy Framework 补组织生命周期。区分 mathematical guarantee 与 security/consent/purpose limitation。

## 主要发现

必须定义 privacy unit、neighboring relation、central/local trust、epsilon/delta、mechanism、sensitivity/clipping、release/query count 与 accountant。composition 累积，post-processing 只在输入已受 DP 保护时适用。C-ETH-01 固化。

## 反证与边界

DP 不阻止数据库入侵、不抹除 population fact、不自动保护 household/group、不建立 consent。epsilon 实际意义依场景；小群体 utility 和公平测量可能受噪声更大影响。

## 设计决议

建立 privacy release ledger 和硬门：有 epsilon/delta 却无 unit/neighbor/composition 即 BLOCKED_CONSTRAINT_SPECIFICATION；同时保留 access/security/deletion/context 账。

## 纳入产物

本轮进入 `SKILL.md` 的 CONSTRAIN-ACT 步骤/停止门、`source-notes.md` 的来源卡、`claim-layer-map.md` 的对应 claim、`templates.md` 的强制字段，并至少由一个 adversarial test 或仓库集成断言约束。没有把研究日志当引用终点；最终输出仍须回链原始 source ID。

## 未解决

- 用户场景的本地数据、组织记录、受影响人证据和合法 authority 尚未知；不能由本轮桌面研究代填。
- 动态网页、软件、法律与在线书版本会变化；复用时重查基准日并记录差异。
- 形式字段可能被合规表演式填写；需要独立复核、反证、minority report 和可执行 stop/rollback。
