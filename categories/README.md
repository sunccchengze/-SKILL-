# 技能分类导航

这里是**不移动 canonical 包路径**的加法式导航层。技能仍由 `catalog/`、`skills/` 和固定的 `full-sources/` 管理；分类目录提供人类 README 与完整 TSV，因此不会破坏既有搜索、安装、来源锁和引用。

四个机器目录共有 **3784** 个原始入口；隐藏内容变体与已审计别名后，默认呈现 **3126** 个候选。

| 分类 | 技能数 | 新手大礼包 | 主要范围 |
|---|---:|---:|---|
| [Agent 与编排](agents-orchestration/README.md) | 384 | 11 | 路由、计划、上下文、记忆、评估、多 Agent 协作与工作流治理。 |
| [工程与代码](engineering-code/README.md) | 767 | 24 | 架构、编码、测试、调试、评审、Git、CI/CD、API、前后端与性能。 |
| [文档与数据](documents-data/README.md) | 175 | 6 | PDF、结构化文档、表格、数据库、数据清洗、分析与可追踪交付。 |
| [研究与科学](research-science/README.md) | 806 | 9 | 检索、综述、引用、实验、统计、科学计算、论文、同行评审与复现。 |
| [写作与内容](writing-content/README.md) | 88 | 15 | 中文与英文写作、编辑、内容研究、技术表达、营销文案与去模板化。 |
| [设计与媒体](design-media/README.md) | 308 | 12 | 产品/UI/UX、视觉系统、网页、演示、图像、视频、动效与媒体生产。 |
| [商业与战略](business-strategy/README.md) | 165 | 11 | 产品、市场、营销、定价、竞争、运营、决策、发布与组织协作。 |
| [安全、隐私与合规](security-compliance/README.md) | 147 | 7 | 安全评审、威胁与风险、隐私、无障碍、依赖、审计和合规治理。 |
| [通用生产力](general/README.md) | 286 | 5 | 跨领域计划、沟通、会议、通用工具、个人效率与难以单归一域的能力。 |

## 选择原则

1. 先把任务写成“领域 + 交付物 + 方法 + 风险”关键词。
2. 用 `search_skills.py` 搜索；分类只用于缩小范围，不是强制边界。
3. 通常选择 1 个主技能，加研究、制作、审查各至多 1 个互补技能。
4. 明确说出本轮调用了哪些技能、用在哪一步、用什么证据验证；不要只列名字不执行。
5. 需要完整 references/assets 时初始化相应 `full-sources/`；不要把快索引缺文件误判为上游没有。

机器摘要见 [`catalog/category-summary.json`](../catalog/category-summary.json)，100 项基础组合见[新手大礼包](../bundles/newcomer-starter-pack/README.md)。
