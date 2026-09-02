# 来源账本：*Engineering a Safer World*

> 检索日期 2026-08-16。A=原书/正式手册；B=独立同行研究或权威评估；C=案例/新兴应用；D=Skill 综合。

## ESW-01｜MIT Press 原书
- **身份**：Nancy G. Leveson, *Engineering a Safer World: Systems Thinking Applied to Safety*；首版文本 © 2011、MIT Press 正式出版 2012（hardcover ISBN `9780262016629`），2016 paperback ISBN `9780262533690`，560pp；MIT 产品页与 MIT Direct 分别记录 electronic ISBN `9780262297301` / `9780262298247`。
- **URL**：https://mitpress.mit.edu/9780262533690/engineering-a-safer-world/ ; https://doi.org/10.7551/mitpress/8179.001.0001
- **证据级**：A；A 层主锚。
- **supports**：安全/可靠性区分、系统理论、约束、层级控制结构、过程模型、STAMP、STPA、CAST、运营与风险迁移。
- **does not support**：STAMP 已穷尽所有事故因果；STPA 是概率风险量化；2026 AI 实践已由原书验证。
- **版本边界**：概念锁 © 2011/正式出版 2012 的首版文本；后续手册分 B。
- **限制/未决**：首版 front matter 标 © 2011 且 LoC/当前 MIT 元数据标 2012；MIT 两个官方入口的 electronic ISBN 也不同。本包显式保留这些书目差异，不把版权年、正式出版年或载体 ISBN 混为一谈。

## ESW-02｜STPA Handbook
- **身份**：Leveson & Thomas (2018), *STPA Handbook*。
- **URL**：http://psas.scripts.mit.edu/home/get_file.php?name=STPA_handbook.pdf ；可访问的未改动版镜像：https://www.flighttestsafety.org/images/STPA_Handbook.pdf
- **证据级**：A/B（作者后续操作指南）。
- **supports**：四步：定义目的、建控制结构、识别 UCA、识别 loss scenarios；四类 UCA。
- **does not support**：这是首版原书逐字步骤；应用必完整。
- **限制**：依赖分析者范围、知识和审查；2026-08-16 检查时原 MIT scripts 入口返回 service unavailable，镜像内容的作者、日期、目录与引用记录一致，但镜像托管方不是作者机构。
- **未决**：原入口恢复时间及未来修订版差异。

## ESW-03｜CAST Handbook
- **URL**：http://sunnyday.mit.edu/CAST-Handbook.pdf
- **证据级**：A/B。
- **supports**：用控制结构、约束和反馈调查已发生损失；找系统改进而非 root-cause blame。
- **does not support**：取消法律/个人问责；CAST 与 STPA 可互换。
- **限制**：作者团队指南，需独立调查程序。
- **未决**：事故证据保全和法域要求另查。

## ESW-04｜STAMP 早期事故模型论文
- **URL**：http://sunnyday.mit.edu/accidents/safetyscience-single.pdf
- **证据级**：A（作者理论原始论文）。
- **supports**：约束而非事件为基本单元；层级社会技术控制和动态反馈。
- **does not support**：事件链永无用；一张图能代表全部组织现实。
- **冲突/限制**：是理论主张与案例，不是随机比较。
- **未决**：不同安全学派的因果本体争议。

## ESW-05｜STAMP 官方出版清单/比较案例
- **URL**：http://sunnyday.mit.edu/STAMP-publications.html
- **证据级**：C（作者维护索引及案例摘要）。
- **supports**：航空、制造、医疗等案例报告发现传统方法外的交互、软件、人因/组织场景。
- **does not support**：案例选择无偏；所有比较独立；STPA 普遍优效。
- **限制**：成功发表/作者参与偏差。
- **未决**：需预注册/盲评比较。

## ESW-06｜FMEA 与 STPA 同案比较
- **URL/DOI**：https://link.springer.com/article/10.1007/s11219-017-9396-0
- **证据级**：B（同行个案）。
- **supports**：两法焦点不同；STPA 强于 causal factors/软件交互，FMEA 可能找到更多部件失效且有风险优先级；互补。
- **does not support**：STPA 支配 FMEA；单案证明统计优势。
- **冲突**：比一些倡导性“全包含”叙述更保守；本包保留两面。
- **未决**：领域与团队效应。

## ESW-07｜Lincoln Laboratory 独立审查
- **URL**：https://www.ll.mit.edu/sites/default/files/publication/doc/2018-12/Harkleroad_2013_ATC-427.pdf
- **证据级**：B（独立政府资助评估）。
- **supports**：结构化 UCA/场景是价值；完整性无法保证；需求推导较 ad hoc、可能重复；需 SME、训练与 V&V。
- **does not support**：STPA 无价值或已被证伪。
- **限制**：2013 航空应用和当时方法版本。
- **未决**：2018 handbook 是否解决多少问题。

## ESW-08｜ISO 26262 兼容性研究
- **URL**：https://www.cas.mcmaster.ca/~lawford/papers/UsingSTPAinISO26262proces.pdf
- **证据级**：B/C。
- **supports**：STPA 能补交互/反馈/软件原因，但不含某些传统风险分析组件；可在标准流程中补充使用。
- **does not support**：使用 STPA 自动满足 ISO 26262。
- **限制**：标准解释需认证机构确认。
- **未决**：标准新版映射。

## ESW-09｜STPA 验证框架研究
- **URL/DOI**：https://www.sciencedirect.com/science/article/abs/pii/S092575352300022X
- **证据级**：B（2023 同行方法研究）。
- **supports**：文献验证不足；主观性、信息/分析者依赖、时间和抽象管理是限制；提出 comprehensiveness/accuracy/credibility 检查。
- **does not support**：所提框架已经证明提高事故预防。
- **限制**：formative framework 仍需实测。
- **未决**：何时停止验证、独立性门槛。

## ESW-10｜UK rail 实地案例
- **URL**：https://www.sciencedirect.com/science/article/pii/S0925753523002175
- **证据级**：B/C。
- **supports**：报告更广系统边界和非显见因素；也报告耗时、依赖主持者技能与合适参与者。
- **does not support**：铁路结论直接转 AI/医疗；更多场景等于更好控制。
- **限制**：仅深析部分 control loops。
- **未决**：全系统资源成本和运营效果。

## ESW-11｜Learning-enabled systems survey
- **URL**：https://arxiv.org/abs/2302.10588
- **证据级**：C（31 篇预印本调查）。
- **supports**：STPA 已扩展至 ML 生命周期；有效性与一般性仍有改进空间。
- **does not support**：DeepSTPA 或任一扩展获监管认可；AI 已安全。
- **限制**：预印本、异质案例。
- **未决**：独立复现和终版。

## ESW-12｜Frontier AI STPA 演示
- **URL**：https://arxiv.org/html/2506.01782
- **证据级**：C（新兴案例/预印本）。
- **supports**：可把 AI 公司、模型、评估、监控和组织过程画为控制结构并补安全 case 覆盖。
- **does not support**：原书预测 frontier AI；该案例证明 AGI 可控；LLM 可替代专家。
- **限制**：单一 threat-model 演示，作者也列资源、主观性与证据限制。
- **未决**：独立实证和 regulator 接受。

## D1｜本 Skill 综合
- **位置**：`SKILL.md`、CLI、模板。
- **证据级**：D。
- **supports**：CONTROL 流程、四类 UCA 自动槽、traceability 字段、高风险门。
- **does not support**：Leveson 提出 CONTROL 缩写；分析完整；认证或部署批准。
- **未决**：需安全工程师、领域 SME、受影响者和独立 assurance 共同验证。
