# 2026 AI 时代四本核心经典：非互换组合协议

> 本文只说明四套系统怎样交接，不把一个作者的概念归给另一个作者，也不制造“统一超级理论”。每个结论仍回到各包 claim/source map。

## 四个不同对象

| 包 | 首要问题 | 分析对象 | 不能替代 |
|---|---|---|---|
| [*Causal Inference: What If*](book-what-if-causal-audit/) | 若总体采用策略 A 而非 B，结局会怎样？ | target、strategies、counterfactual estimand、识别假设、估计 | 不能判断系统所有危险、制度正当性或信息流规范 |
| [*Engineering a Safer World*](book-safer-world-control-audit/) | 哪些不充分控制/反馈会让系统进入危险状态？ | loss、hazard、constraint、control structure、UCA、scenario | 不能识别平均干预效应、证明频率或决定 privacy norm |
| [*Governing the Commons*](book-governing-commons-institution-design/) | 相互依赖的资源使用者怎样形成和维持规则？ | CPR、rules-in-use、commitment、monitoring、sanctions、conflict、nesting | 不能把任何共享资产自动变 commons，也不能证明制度正义 |
| [*Privacy in Context*](book-privacy-context-flow-audit/) | 某信息流是否符合正当的情境规范？ | context、roles、five-parameter flow、norm、departure、evaluation | 不能以安全/同意/公开标签替代适当性，也不能认证法律合规 |

## 组合顺序（D 层 portfolio 设计）

对一个 AI 系统可按以下接口运行，但四份输出分别保存：

1. **FLOW 先画信息流与情境权利**：避免后续数据/监控方案先侵犯不可牺牲边界。
2. **CONTROL 定损失、危险与控制结构**：把模型、人、组织、供应商、监管与反馈放在同一社会技术边界。
3. **COMMONS 仅在真正存在 CPR/维护稀缺与共同治理问题时诊断制度**：明确谁定规则、监督谁、怎样争议和嵌套。
4. **TARGET 只对可定义干预效果的问题设计证据**：例如某 safety constraint 或治理变更是否降低指定结局；先识别，后估计。
5. **发布门合并但不抵销**：最严格的 rights/safety/legitimacy/evidence gate 优先；一套通过不能覆盖另一套失败。

该顺序是本 portfolio 的 **D 层操作化**，不是四位作者共同提出。

## 接口制品

| From → To | 传递内容 | 禁止传递的伪结论 |
|---|---|---|
| FLOW → CONTROL | 不可接受隐私损失、情境角色、允许/禁止的 flow constraints | “有同意所以安全” |
| CONTROL → TARGET | 候选 safety intervention、harm outcomes、time-varying feedback | “STPA 找到 scenario 所以干预有效” |
| COMMONS → CONTROL | 实际 authority、monitoring、sanction/appeal control loops | “社区规则所以不会失败” |
| TARGET → COMMONS | 规则变更的条件性结果与不确定性 | “平均 effect 为正所以制度正当” |
| FLOW → COMMONS | 信息边界、monitor data 的 TP、contest/correction rights | “共同资源所以可全面监控” |
| CONTROL → FLOW | telemetry/incident flows、recipients、retention 与 emergency TP | “安全目的允许任意数据流” |

## 四重发布门

任何涉及人员、劳动、医疗、教育、信用、执法、内容治理的现实动作，至少同时回答：

- **Causal**：effect 是否明确定义/识别？现实 impact evidence 和分群伤害是什么？
- **Safety**：loss/hazard/constraint/owner/feedback/stop/rollback 是否可验证？
- **Institution**：谁有合法制订/修改/监督/制裁权？谁被排除？有何低成本 conflict/appeal？
- **Privacy**：完整五参数 flow、正当 norm、downstream/inference、contest 与 deletion 是什么？

缺任一项只输出 gap list；全部字段齐全也只到 `governance_review_required`，不是部署批准。

## 不可坍缩清单

- counterfactual assumption **≠** STAMP loss scenario；
- causal DAG **≠** safety control structure；
- positivity/overlap **≠** commons participation；
- safety monitoring **≠** 无边界 surveillance；
- common-property boundary **≠** privacy-appropriate recipient；
- contextual norm **≠** rule-in-use 的长期有效性；
- durable institution **≠** safe system **≠** causal effectiveness **≠** legitimate information flow；
- diagnosis **≠** legitimacy；institutional diagnosis **≠** governance legitimacy；
- 四份 analysis **≠** 一份 deployment approval。
