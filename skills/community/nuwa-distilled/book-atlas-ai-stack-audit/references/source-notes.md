# Source Notes — Atlas of AI Full-Stack Audit

检索基准日：**2026-08-16**。Crawford 的全栈/权力论点与具体系统事实必须分开；宏观叙事不自动证明任何供应商或部署有特定行为。

## 原作、目录与方法

### AT01 — Yale University Press official book record

- **类型**：出版社官方书页，一手书目来源。
- **支持**：Kate Crawford、书名、副标题、2021 出版信息，以及 AI 的物质/政治/地球成本定位。
- **限制**：营销摘要不代替章节论证或独立事实核查。
- **URL**：https://yalebooks.co.uk/book/9780300264630/atlas-of-ai/

### AT02 — JSTOR full book record

- **类型**：稳定学术平台的书目/全文记录。
- **支持**：Introduction、Earth、Labor、Data、Classification、Affect、State、Power、Space 的完整结构与章节定位。
- **限制**：访问权限可能变化；原书案例仍需按日期/地点读取。
- **URL**：https://www.jstor.org/stable/j.ctv1ghv45t

### AT03 — Anatomy of an AI System

- **类型**：Crawford/Joler 先导性项目与可视化，一手相关作品。
- **支持**：以 Amazon Echo 为对象，追踪资源、劳动、数据和网络基础设施，说明“设备/模型”边界过窄。
- **限制**：单一产品的概念性/调查性地图，不是完整 LCA，也不能直接迁移到任一系统。
- **URL**：https://anatomyof.ai/

## 数据、分类与 affect

### AT04 — Gebru et al., Datasheets for Datasets

- **类型**：同行评审数据文档研究。
- **支持**：记录 dataset motivation、composition、collection、preprocessing、uses、distribution、maintenance 等生命周期问题。
- **限制**：文档依赖提供者诚实与审查；datasheet 不能自动修复不合法/不正当数据。
- **URL**：https://doi.org/10.1145/3458723

### AT05 — Buolamwini & Gebru, Gender Shades

- **类型**：同行评审实证审计。
- **支持**：被测商业性别分类系统呈现显著 intersectional performance disparity；论文报告最深色女性最高 error 34.7%，最浅色男性最高 0.8%。
- **限制**：特定时间、系统、二元任务与 benchmark；不能机械外推到所有生物识别或社会类别。
- **URL**：https://proceedings.mlr.press/v81/buolamwini18a.html

### AT06 — Barrett et al., emotional expressions reconsidered

- **类型**：心理科学同行评审综述。
- **支持**：面部动作与情绪并非简单、可靠、特定、跨情境的一一映射；应区分 reliability、specificity、generalizability 与 validity。
- **限制**：不等于所有面部/行为信号在任何窄任务中都无信息；具体用途仍需验证。
- **URL**：https://doi.org/10.1177/1529100619832930

### AT07 — Model Cards for Model Reporting

- **类型**：同行评审模型文档方法。
- **支持**：按预期用途、群体、评价条件与限制报告模型，可补充 dataset/系统文档。
- **限制**：model card 仍以模型为中心，不能替代劳动、环境、国家或权力审计。
- **URL**：https://doi.org/10.1145/3287560.3287596

## 劳动、价值链与权利

### AT08 — ILO AI labour disclosure initiative

- **类型**：国际劳工组织官方倡议/会议材料。
- **支持**：提高 AI 背后社会成本与人类劳动可见度；指向 subcontractor disclosure、worker protection 与 social dialogue。
- **限制**：倡议不证明单一企业劳动条件，也不是强制审计完成证据。
- **URL**：https://www.ilo.org/meetings-and-events/ai-labour-disclosure-initiative-recognizing-social-cost-human-labour-behind

### AT09 — ILO Working Paper 144 on AI value chains

- **类型**：国际组织研究工作论文。
- **支持**：AI value chain、全球分工与 decent work 风险，强调 worker voice、human oversight 和供应链责任。
- **限制**：宏观/案例综合有地区和资料可得性限制；需本地劳动资料。
- **URL**：https://www.ilo.org/sites/default/files/2025-07/wp144_web.pdf

### AT10 — OECD Due Diligence Guidance for Responsible Business Conduct

- **类型**：政府间组织正式尽责指南。
- **支持**：识别、预防/减缓、跟踪、沟通与补救 adverse impacts，覆盖商业关系而非只看一级组织。
- **限制**：通用业务指南，不是 AI 专属技术测试；法律地位因地区而异。
- **URL**：https://mneguidelines.oecd.org/due-diligence-guidance-for-responsible-business-conduct.htm

### AT11 — CARE Principles for Indigenous Data Governance

- **类型**：Global Indigenous Data Alliance 原则。
- **支持**：Collective Benefit、Authority to Control、Responsibility、Ethics，纠正仅以开放/可重用为中心的数据治理。
- **限制**：原则实施须由具体 Indigenous peoples/institutions 主导；不能被一般组织自我认证。
- **URL**：https://www.gida-global.org/care

## 环境、基础设施与量化边界

### AT12 — NIST AI 600-1 Generative AI Profile

- **类型**：NIST 官方 GenAI 风险管理 profile。
- **支持**：生命周期风险包括 environmental impacts、data provenance、harmful bias、human-AI configuration 与 value-chain/component integration。
- **限制**：风险框架不提供某模型的 LCA 数字或法律批准。
- **URL**：https://airc.nist.gov/docs/NIST.AI.600-1.GenAI-Profile.ipd.pdf

### AT13 — Patterson et al., Carbon Emissions and Large Neural Network Training

- **类型**：产业作者的实证/方法论文。
- **支持**：训练排放高度依赖模型、硬件、数据中心效率与能源位置；报告边界会显著影响比较。
- **限制**：作者/设施可得数据与训练环节范围有限；不能代表完整生命周期或所有供应商。
- **URL**：https://arxiv.org/abs/2104.10350

### AT14 — Li et al., Making AI Less “Thirsty”

- **类型**：预印本环境估算研究。
- **支持**：AI/data-center water footprint 需要考虑 onsite 与 offsite water、地点/时间和调度；水不是单一全球常数。
- **限制**：估算依赖假设和非公开运营数据；预印本结论不可变成无区间的单提示事实。
- **URL**：https://arxiv.org/abs/2304.03271

### AT15 — Green Algorithms

- **类型**：同行评审计算碳估算方法/工具。
- **支持**：硬件、运行时间、location carbon intensity、PUE 等字段使计算 footprint 声明更透明。
- **限制**：估算边界通常不含完整硬件供应链、water 或社会分配；默认值需披露。
- **URL**：https://doi.org/10.1002/advs.202100707

## 国家、治理与批评

### AT16 — EU AI Act official legal text portal

- **类型**：欧盟官方法规入口。
- **支持**：按用途/风险设置禁止、义务、透明度、治理与执法要求，说明 state/regulatory context 改变系统可接受性。
- **限制**：适用范围、实施日期与后续 guidance 需按具体日期核对；不能迁移为全球规则。
- **URL**：https://eur-lex.europa.eu/eli/reg/2024/1689/oj

### AT17 — UNESCO Recommendation on the Ethics of AI

- **类型**：政府间组织规范文件。
- **支持**：人权、环境、文化多样性、数据治理、劳动、审计与多方参与的广义生命周期框架。
- **限制**：软法/国家实施不一；原则承诺不等于本地执行证据。
- **URL**：https://www.unesco.org/en/artificial-intelligence/recommendation-ethics

### AT18 — Kafer, critical review of Atlas of AI

- **类型**：独立学术评论/反方阅读。
- **支持**：指出全书广度可能牺牲种族/殖民机制深度，且 refusal/political alternatives 的操作路径不足。
- **限制**：评论者解释不是对所有章节的定论；用来保留争议而非“驳倒”原书。
- **URL**：https://www.ejumpcut.org/archive/JC62.2024/GaryKafer/index.html

## 使用边界汇总

- 宏观全栈视野用于发现问题，不直接证明具体组织事实。
- 生命周期数字必须保留 boundary、geography、date、denominator、allocation 与 uncertainty。
- 个别 benchmark/案例不自动迁移到新系统；也不能因范围有限而忽略已显示的伤害机制。
- worker/community/Indigenous evidence 不是可任意提取的数据；参与方式本身需权利与安全设计。
