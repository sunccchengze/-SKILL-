# Claim Layer Map — Applied Causal ML

固定分布：A=5、B=3、C=6、D=4，共 18 条。A/B/C 的来源 ID 必须存在于 [`source-notes.md`](source-notes.md)；D 明示本 Skill 推论。

| Claim ID | 层 | 声明 | 来源 | 关键限制 | 操作 |
|---|---|---|---|---|---|
| A-CML-01 | A | 官方项目当前标注 online version 0.1.2 dated May 3 2026 | CM01, CM02 | 在线版会更新且不是传统纸质首版 | 每次引用锁版本与访问日 |
| A-CML-02 | A | 项目公开稿的 arXiv 历史最迟可追溯至 2024-03-04 | CM03 | arXiv 日期不等于出版社首版 | 分列首次公开与当前版 |
| A-CML-03 | A | 原作面向高年级本科至博士和应用研究者并含 R/Python notebooks 与练习 | CM01, CM02 | 受众定位不证明读者已具识别能力 | 使用前检查先修与领域知识 |
| A-CML-04 | A | 原作把现代机器学习放入因果推断的识别和估计问题中 | CM01, CM02 | 教学组织不是用户场景的识别证明 | 先写 estimand 再选 learner |
| A-CML-05 | A | 官方目录覆盖基础因果问题与更高级的异质性和机器学习主题 | CM01 | 目录存在不等于所有主题同等成熟 | 按具体章节和版本定位 |
| B-CML-01 | B | 灵活 nuisance 学习仍须在因果识别条件下解释目标参数 | CM02, CM04 | 很多识别假设不可由数据完全检验 | 在报告中分列假设不确定性 |
| B-CML-02 | B | cross-fitting 与正交得分处理的是估计误差路径而不是所有偏差 | CM04, CM05 | 软件默认与理论条件可能不一致 | 冻结 split score 与实现版本 |
| B-CML-03 | B | 高级异质性或政策方法需要额外支持域和验证纪律 | CM01, CM02 | 示例成功不保证新人群或政策有效 | 探索与确认分离 |
| C-CML-01 | C | DML 的正交和 cross-fitting 可在条件下减少 nuisance 正则化和过拟合偏差 | CM04, CM06 | 不修复隐藏混杂 错 estimand 或无重叠 | 不把 DML 称识别策略 |
| C-CML-02 | C | 有限 overlap 会放大不稳定且修剪会改变目标人群 | CM07, CM09 | 有限样本诊断不能证明总体 positivity | 报告被排除群体和新 estimand |
| C-CML-03 | C | 未测混杂敏感性可量化脆弱性但不能证明偏差不存在 | CM08, CM14 | 方法依模型和有效 negative control | 将结果作为降级或重设计输入 |
| C-CML-04 | C | CATE 和 policy learning 需要 honesty 支持域及福利函数等额外条件 | CM10, CM11 | 群体估计不提供个体反事实真值 | 禁止事后最大组自动决策 |
| C-CML-05 | C | 迁移到目标域需要明确域差异和效应修饰结构 | CM12 | 结构图可信度和目标域数据仍有限 | 单独提交 transport memo |
| C-CML-06 | C | 干扰存在时必须重定义暴露单位和直接间接效应 | CM13, CM15 | 特定结构不能覆盖任意网络反馈 | no-interference 失败则停止普通解释 |
| D-CML-01 | D | 本 Skill 规定 IDENTIFY-DML 必须先冻结 estimand timeline 与 identification argument | 本 Skill 综合 A-CML-04, C-CML-01 | 操作顺序不能保证假设正确 | 用 estimand card 和识别表 |
| D-CML-02 | D | 本 Skill 将 post-treatment control hidden confounding interference 和无支持设为阻断门 | 本 Skill 综合 C-CML-02, C-CML-03, C-CML-06 | gate 依赖提交者如实披露 | 指定 owner 与独立复核 |
| D-CML-03 | D | 本 Skill 的 CLI 只输出估计计划准备度而不拟合或批准因果结论 | 本 Skill 的确定性安全设计 | readiness 不是 identification 或 validity | 状态最高为 READY_FOR_ESTIMATION_PLAN |
| D-CML-04 | D | 本 Skill 将高风险政策用途升级到治理 权利 申诉与迁移复核 | 本 Skill 综合 CM11, CM17 | 治理复核也可能遗漏受影响人 | 保留替代 停止与复审日期 |

## 使用规则

- 引用 claim ID 不代替阅读 source card；尤其 C 层需带 design/population/assumption。
- A 与 B 是“作者/原作说了什么”，不是自动真值；C 可支持、限定或反驳。
- D 只能作为本包操作协议，不得倒写成作者原话或行业共识。
