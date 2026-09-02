# Claim—layer—source map：*Privacy in Context*

A = 2009 首版/2010 版权文本；B = Nissenbaum 其他论文与后续阐释；C = 独立形式化、实证、治理与批评；D = 本 Skill 操作化。

| ID | 可使用的声明 | 层 | 来源 | 限制 |
|---|---|---|---|---|
| PIC001 | 隐私不等于停止信息流，而关乎信息流是否适当 | A | PIC-01 | 不表示数据最小化/保密不重要 |
| PIC002 | public/private 二分不能充分解释公开场所与公共记录中的隐私 | A | PIC-01 | “公开”不取消角色、规模与用途约束 |
| PIC003 | 社会情境由角色、目的、价值与实践构成，不只是地点或平台 | A | PIC-01 | context 边界可能重叠、争议和变化 |
| PIC004 | 情境信息规范规定适当的信息流 | A | PIC-01 | 观察到的习惯不自动是正当规范 |
| PIC005 | 信息流至少需明确 subject、sender、recipient、attribute、transmission principle | A | PIC-01 | 任一缺失会使规范判断含混 |
| PIC006 | actors 必须按情境角色/能力描述，而非仅公司或个人名 | A | PIC-01 | 同一主体可同时承担多角色 |
| PIC007 | attribute 是情境有意义的信息类型，包括推断结果 | A | PIC-01 | “敏感/非敏感”不能替代具体属性 |
| PIC008 | transmission principle 是流动条件，如保密、互惠、授权、购买、强制或依法要求 | A | PIC-01 | consent 只是其中之一 |
| PIC009 | 新实践改变任一参数会触发对规范偏离的 prima-facie 审查 | A | PIC-01 | 偏离不自动等于最终禁止 |
| PIC010 | 九步启发式先描述实践/情境/参数/规范，再评估道德政治因素、情境目的并建议 | A | PIC-01 | heuristic 不是机械算法 |
| PIC011 | 维护旧规范有初步推定，但可为更好的道德政治理由而改变 | A | PIC-01 | status quo 可能不公，需正当性评价 |
| PIC012 | 评价应考虑一般道德政治因素与情境的目的、价值和功能 | A | PIC-01 | 多价值冲突不能由多数预期自动解决 |
| PIC013 | 规模、聚合、持久性、可搜索性与跨情境流会改变原本“相同”公开数据的意义 | A | PIC-01 | 技术差异需映射到参数/规范变化 |
| PIC014 | notice-and-consent 不能独自承担所有隐私判断 | A | PIC-01 | 同意仍可作为具体 transmission principle |
| PIC015 | 2004 论文先以 appropriateness 与 distribution norms 阐明 CI | B | PIC-02 | 早期表述与书中五参数框架标版本 |
| PIC016 | 2019 data food chain 论文明确强调全五参数和推断/下游责任 | B | PIC-03 | 后续发展不冒充 2009 原书 AI 预测 |
| PIC017 | Nissenbaum 后续论述把 CI 用于在线追踪及反对纯 notice/choice | B | PIC-04 | 作者延展仍与独立验证分层 |
| PIC018 | temporal-logic 工作证明 CI 参数可形式表达一些传输规范 | C | PIC-05 | 形式化覆盖有限，不自动选择正当规范 |
| PIC019 | 隐私政策标注研究发现缺参数、模糊与参数膨胀会阻碍理解 | C | PIC-06 | 文本可读性不验证实践符合声明 |
| PIC020 | crowd/实证研究可测规范预期，但结果依赖样本、措辞、文化与权力 | C | PIC-07 | 多数意见不是道德真理 |
| PIC021 | vulnerability 批评指出规范分析可能漏掉未在场/无权发言群体与差异伤害 | C | PIC-08 | 这是增强而非完全取代 CI 的理由 |
| PIC022 | NIST Privacy Framework 提供数据流库存、用途、推断限制、可见性与治理控制 | C | PIC-09 | 自愿框架不是法律合规证明 |
| PIC023 | LLM benchmark 显示模型在情境隐私推理/实际保密行为上会失败 | C | PIC-10 | benchmark 不能代表所有模型/真实部署 |
| PIC024 | 多主体、群体信息与推断会超出单一 subject 的简化模型 | C | PIC-10, PIC-11 | 新扩展证据不属于原书 A 层 |
| PIC025 | FLOW 是本 Skill 创建的 Frame—List—Observe—Weigh 审计 | D | D1 | 不是 Nissenbaum 原缩写 |
| PIC026 | CLI 保存基线五元组、新实践和参数 delta，不自动裁决规范 | D | D1 | 用户输入为 submitted-not-verified |
| PIC027 | 高影响信息流缺 owner/rule/impact/contest/rollback/stop 时失败 | D | D1 | 字段齐全仍需 DPIA/法律/安全等审查 |
| PIC028 | 输出固定为 prima_facie_privacy_audit_not_legal_approval | D | D1 | 不批准数据处理或部署 |

## 禁止坍缩

privacy **≠** secrecy/security/control；public **≠** free for all；consent **≠** appropriateness；
expectation **≠** legitimate norm；parameter change **≠** final violation；no parameter change **≠** no harm；
platform **≠** social context；company name **≠** actor role；PII label **≠** attribute analysis；
policy text **≠** actual flow；majority norm **≠** justice；FLOW audit **≠** legal/deployment approval。
