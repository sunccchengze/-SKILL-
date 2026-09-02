# 来源账本｜《Don’t Make Me Think》任务可用性审计

> 复核日期：2026-08-16。`DM-S*` 为包内来源 ID。原书启发式、正式标准与经验研究不能互换。

## 原书与作者谱系

### DM-S01｜Krug, *Don't Make Me Think: A Common Sense Approach to Web Usability*

- 类型：一手书籍；New Riders，2000（首版）、2005（第 2 版）。
- 支持：自明/自解释、扫描、满意化选择、清楚导航、首页、goodwill reservoir 和轻量可用性测试。
- 不支持：正式国际标准、跨设备因果定律、普适点击上限。

### DM-S02｜Krug, *Don't Make Me Think, Revisited* (2014)

- 类型：一手修订书籍，New Riders。
- 支持：更新后的移动端讨论和作者持续主张；点击次数不如每次选择是否清楚重要。
- 不支持：只要选择“无思考”就不必测任务；以删字为由删掉知情披露或错误恢复信息。

### DM-S03｜Krug, *Rocket Surgery Made Easy* (2010)

- 类型：一手方法书。
- 支持：频繁、小规模、团队可执行的形成性测试与问题优先处理。
- 不支持：少量便利样本能估计人口问题发生率；替代代表性量化研究。

## 标准与政府指南

### DM-S04｜ISO 9241-11:2018, Usability: Definitions and Concepts

- URL：https://www.iso.org/standard/63500.html
- 类型：国际标准元数据/标准文本（正文可能需授权）。
- 支持：可用性与指定用户、目标、有效性、效率、满意度及使用情境相关。
- 不支持：一个与任务无关的通用“可用性分数”；本包已完成 ISO 合规认证。

### DM-S05｜W3C, Web Content Accessibility Guidelines (WCAG) 2.2

- URL：https://www.w3.org/TR/WCAG22/
- 类型：W3C Recommendation，2023。
- 支持：可感知、可操作、可理解、健壮及具体成功准则；键盘、焦点、目标尺寸、认证和认知可用性相关门。
- 不支持：仅人工走查即可声称完全符合；可用性测试取代技术无障碍评估。

### DM-S06｜W3C, Understanding WCAG 2.2

- URL：https://www.w3.org/WAI/WCAG22/Understanding/
- 类型：非规范性解释材料。
- 支持：成功准则意图、受益用户、示例和测试思路。
- 不支持：覆盖所有残障者体验；代替规范文本。

### DM-S07｜Digital.gov, Usability Testing

- URL：https://digital.gov/topics/usability/
- 类型：美国政府实践指南集合。
- 支持：以现实任务观察用户、迭代发现问题、选择适当研究方式。
- 不支持：某个固定样本数适用于所有决策；全球标准。

## 独立研究与反“三击”证据

### DM-S08｜Nielsen Norman Group, “The 3-Click Rule for Navigation Is False”

- URL：https://www.nngroup.com/articles/3-click-rule/
- 类型：行业研究综述/实践文章。
- 支持：用户不会仅因超过三次点击自动放弃；路径清楚和任务进展比固定点击数更有解释力。
- 不支持：点击成本永远无关；该文章本身等于同行评议元分析。

### DM-S09｜Pirolli & Card (1999), Information Foraging

- DOI：https://doi.org/10.1037/0033-295X.106.4.643
- 类型：理论论文，*Psychological Review* 106(4), 643–675。
- 支持：信息寻求可分析为线索价值、成本与路径选择；为 information scent 提供独立谱系。
- 不支持：Krug 独创 information scent；理论直接规定具体导航设计。

### DM-S10｜Sauro & Lewis, *Quantifying the User Experience*, 2nd ed. (2016)

- 类型：独立方法书，Morgan Kaufmann。
- 支持：任务成功、时间、错误、满意度、样本不确定性和可用性量化的设计原则。
- 不支持：形成性测试必须追求统计显著；任意小样本百分比可外推。

## 欺骗性设计边界

### DM-S11｜FTC (2022), *Bringing Dark Patterns to Light*

- URL：https://www.ftc.gov/reports/bringing-dark-patterns-light
- 类型：监管机构报告。
- 支持：难取消、隐藏条款、误导、未经充分理解的数据披露等设计边界。
- 不支持：全球法律判定；“容易完成购买”本身即欺骗。

### DM-S12｜Gray et al. (2018), “The Dark (Patterns) Side of UX Design”

- DOI：https://doi.org/10.1145/3173574.3174108
- 类型：CHI 同行评议研究。
- 支持：将用户价值与设计者/组织价值冲突操作化为 dark patterns 分类与专业伦理问题。
- 不支持：分类穷尽所有模式；仅凭标签证明法律违规。

## 本 Skill 创建物

### DM-S13｜SCENT 任务审计协议

- 类型：D 层综合，2026。
- 来源组合：DM-S01–DM-S12。
- 支持：任务、竞争假设、观察、严重度、无障碍/反欺骗门、修复复测的统一记录。
- 不支持：Krug 原方法、经验证量表、WCAG/ISO 认证。

## 更新与缺口

- WCAG、消费者保护规则和辅助技术会更新；真实项目需锁定版本与辖区。
- 小样本形成性测试的发现率取决于任务、参与者和问题分布；不保留“5 人发现 85%”等无条件说法。
- AI 界面的可解释性、生成错误与代理操作需要额外安全研究，不能只套网页启发式。
