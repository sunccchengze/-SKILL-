# Claim—layer—source map：*Engineering a Safer World*

A = 锁定 MIT Press 原书；B = Leveson/Thomas 后续手册与 CAST；C = 独立比较、验证、应用和批评；D = 本 Skill 操作化。

| ID | 可使用的声明 | 层 | 来源 | 限制 |
|---|---|---|---|---|
| ESW001 | 复杂社会技术系统的安全是系统涌现属性，不可还原为部件可靠性 | A | ESW-01 | 不表示部件失效不重要 |
| ESW002 | 安全与可靠性可冲突，安全约束限制使命实现方式 | A | ESW-01 | 约束冲突仍需显式裁决 |
| ESW003 | 线性事件链偏重失效，难覆盖安全部件之间的不安全交互 | A | ESW-01 | 事件链仍可补充分析局部故障 |
| ESW004 | STAMP 把事故理解为控制结构未充分施加安全约束 | A | ESW-01 | 是事故模型，不是频率估计器 |
| ESW005 | 社会技术控制结构跨监管、管理、工程、运营与物理过程层级 | A | ESW-01 | 边界和层级由分析者建模，可能遗漏 |
| ESW006 | 控制回路含 controller、control action、controlled process、feedback 与 process model | A | ESW-01 | “control”不只指命令控制 |
| ESW007 | 错误/不完整过程模型、反馈延迟和协调缺口可在无部件失效时致险 | A | ESW-01 | 候选场景需验证 |
| ESW008 | 系统会随竞争压力、适应与变更向更高风险迁移 | A | ESW-01 | 不是任何漂移都必致事故 |
| ESW009 | STPA 从损失/危险/约束和控制结构推导不安全控制动作与场景 | A | ESW-01 | 原书步骤与 2018 手册表述需标版本 |
| ESW010 | UCA 四类为未提供、提供即危险、时序/顺序错误、持续时间错误 | A | ESW-01 | 每项需写实际危险情境与 hazard link |
| ESW011 | hazard 是在最坏环境条件下可导致损失的系统状态/条件 | A | ESW-01 | 不要把 cause 写成 hazard |
| ESW012 | constraint 应由危险反向形成可执行系统行为限制 | A | ESW-01 | 写出句子不等于被设计/验证/执行 |
| ESW013 | 安全须贯穿设计、运营、管理、监管与变更控制 | A | ESW-01 | 一次性工作坊不足 |
| ESW014 | CAST 用控制结构分析已发生损失，反对只归咎前线个体 | A | ESW-01 | 不取消个人违法/故意行为的独立责任 |
| ESW015 | 2018 STPA Handbook 将实践整理为四步并细化 loss scenario | B | ESW-02 | 后于 © 2011/正式出版 2012 的首版，不倒灌为原书版式 |
| ESW016 | CAST Handbook 提供事故学习的后续操作指南 | B | ESW-03 | CAST 与前瞻 STPA 不能互换 |
| ESW017 | STAMP 后续材料扩展到 security 与 learning-enabled systems | B | ESW-04 | 扩展不是原书对现代 AI 的预测 |
| ESW018 | 个案比较常见 STPA 找到传统方法外的交互/软件/人因场景 | C | ESW-05, ESW-06 | 个案数量不是普遍优效证明 |
| ESW019 | 独立 Lincoln Laboratory 审查肯定结构价值，也指出完整性、需求推导与验证不足 | C | ESW-07 | 2013 特定航空案例，不能定论所有版本 |
| ESW020 | FMEA/STPA 个案显示两者焦点不同且可能互补，STPA 不含内置风险优先级 | C | ESW-08 | 单一案例限制外推 |
| ESW021 | 2023 验证研究称形式化验证仍在发展，主观性和人员能力关键 | C | ESW-09 | 提议框架本身仍需实测 |
| ESW022 | 现场应用报告 STPA 可能劳动密集并依赖系统知识与多方参与 | C | ESW-10 | 资源成本随范围/熟练度变化 |
| ESW023 | learning-enabled systems 调查显示 STPA 已被扩展，但一般性与有效性仍不清楚 | C | ESW-11 | 扩展研究不是部署保证 |
| ESW024 | AI 场景应用应作为补充安全保证机制，不把 LLM 当安全分析权威 | C | ESW-12 | 新兴应用证据有限 |
| ESW025 | CONTROL 是本 Skill 创建的七步流程 | D | D1 | 不是 Leveson 原缩写 |
| ESW026 | CLI 对每个 control action 生成四类 UCA 槽并保持 candidate_not_validated | D | D1 | 自动枚举不保证情境正确/完整 |
| ESW027 | 高风险缺独立复核、真实影响、owner、appeal、stop/rollback 时失败 | D | D1 | 字段完整仍非认证 |
| ESW028 | 输出固定为 hazard_analysis_not_safety_certification | D | D1 | 不得用于证明“安全” |

## 禁止坍缩

reliability **≠** safety；hazard **≠** cause；loss **≠** hazard；controller **≠** only software；
STPA **≠** risk quantification；candidate scenario **≠** verified pathway；constraint text **≠** enforced control；
workshop complete **≠** complete hazard coverage；human contribution **≠** blame；analysis **≠** certification/deployment。
