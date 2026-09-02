# 来源账本：*Privacy in Context*

> 检索日期 2026-08-16。A=原书/作者原始论文；B=同行形式化/实证研究或正式治理框架；C=批评/新兴 AI 评估；D=Skill 综合。

## PIC-01｜锁定原书
- **身份**：Helen Nissenbaum, *Privacy in Context: Technology, Policy, and the Integrity of Social Life*, Stanford University Press；published 2009-11-24，copyright 2010，paperback ISBN `9780804752374`, 304pp。
- **URL**：https://books.google.com/books/about/Privacy_in_Context.html?id=_NN1uGn1Jd8C
- **证据级**：A；A 层主锚。
- **supports**：反对 privacy=control/secrecy/public-private 二分；情境、角色、属性、传输原则、规范、偏离与九步评价。
- **does not support**：任何观察到的规范都正当；同意无作用；作者预测 LLM；CI 单独满足法律。
- **版本边界**：2009 发布/2010 版权是同一首版书目差异，不伪造两个内容版本。
- **限制/冲突**：未发现可直接裁定本条书目/范围事实的独立冲突；用途限于上述 supports 与版本边界。
- **未决**：不同电子/精装 ISBN 页码不用于本包定位。

## PIC-02｜2004 “Privacy as Contextual Integrity”
- **URL**：https://digitalcommons.law.uw.edu/wlr/vol79/iss1/10/
- **证据级**：A（作者早期原始论文）。
- **supports**：公开监控/公开记录问题；appropriateness 与 distribution norms；情境规范具有初步推定但需 justice 评价。
- **does not support**：早期两类规范表述等同书中所有五参数细节。
- **冲突/限制**：早期框架；本包层 B 处理版本发展。
- **未决**：无。

## PIC-03｜2019 data food chain
- **URL**：https://nissenbaum.tech.cornell.edu/papers/Contextual%20Integrity%20Up%20and%20Down.pdf
- **证据级**：A/B（作者后续论文）。
- **supports**：五参数必须全写；CI 不反对 flow 本身；“public is public”忽略 recipient/transmission changes；推断/下游加工责任。
- **does not support**：2010 原书已讨论当前 LLM 架构；任何数据处理都违法。
- **限制**：后续阐释，不能倒灌为原书预测。
- **未决**：复杂多主体推断的参数模型。

## PIC-04｜online privacy contextual approach
- **URL**：https://www.amacad.org/publication/daedalus/contextual-approach-privacy-online
- **证据级**：A/B（作者后续论文）。
- **supports**：notice-and-consent 弱点；线上生活嵌入多个社会情境；规范而非统一线上空间。
- **does not support**：consent 从不正当；线下规范原样支配所有线上新实践。
- **限制**：规范论证。
- **未决**：平台跨情境的制度执行。

## PIC-05｜逻辑形式化
- **身份**：Barth, Datta, Mitchell & Nissenbaum (2006), “Privacy and Contextual Integrity.”
- **URL**：https://theory.stanford.edu/people/jcm/papers/barth-datta-mitchell-nissenbaum-2006.pdf
- **证据级**：B。
- **supports**：角色、subject/sender/recipient、attribute、过去/未来 transmission condition 可用 temporal logic 表达；示例映射 HIPAA/COPPA/GLBA。
- **does not support**：逻辑自动发现正当规范；覆盖群体信息/所有法律；实现即合规。
- **限制**：简化 agent、single subject 与 information type 假设。
- **未决**：动态/冲突规范与机器推断。

## PIC-06｜隐私政策 CI 标注
- **身份**：Shvartzshnaider et al. (2019), “Going Against the (Appropriate) Flow.”
- **URL**：https://nissenbaum.tech.cornell.edu/papers/Going%20Against%20the%20(Appropriate)%20Flow.pdf
- **证据级**：B。
- **supports**：缺参数、模糊语言、参数膨胀会使政策中的数据流难理解/评价；五元组可做系统审计。
- **does not support**：政策陈述等于实际系统行为；NLP 可独自裁决隐私。
- **限制**：文本分析样本和标注判断。
- **未决**：运行时 flow 与政策对账。

## PIC-07｜crowdsourcing privacy expectations
- **URL**：https://www.princeton.edu/~pmittal/publications/privacy-expectations-hcomp16
- **证据级**：B（实证/形式化）。
- **supports**：CI 五元组可转 vignette/逻辑以测教育情境规范；规范发现与正式表达困难。
- **does not support**：crowd majority 是合法规范；一个文化样本适用于全球。
- **限制**：场景、措辞、样本与时间影响回答。
- **未决**：弱势群体权重与分歧记录。

## PIC-08｜norms-to-vulnerabilities 批评
- **身份**：McDonald & Forte (2020), CHI, “The Politics of Privacy Theories.”
- **URL/DOI**：https://dl.acm.org/doi/fullHtml/10.1145/3313831.3376167
- **证据级**：B/C。
- **supports**：CI/规范框架若缺席脆弱群体声音、假定影响均等，会许可不平等；需显式 vulnerability 分析。
- **does not support**：CI 毫无价值；所有共识无效。
- **限制**：理论批评+案例，不给通用计算规则。
- **未决**：制度化代表与反报复机制。

## PIC-09｜NIST Privacy Framework 1.0
- **URL**：https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.01162020.pdf
- **证据级**：A/B（正式自愿框架）。
- **supports**：data processing inventory/ecosystem、contextual factors、purpose、lineage、inference limitation、visibility、govern/control/protect。
- **does not support**：NIST 采用 CI 为唯一理论；自愿 profile 满足 GDPR/法域法。
- **限制**：C 层现代治理；不是原书。
- **未决**：2.0 更新与行业 profile。

## PIC-10｜ConfAIde LLM benchmark
- **URL**：https://proceedings.iclr.cc/paper_files/paper/2024/file/08305d8b2ddab98932c163ea73df065f-Paper-Conference.pdf
- **证据级**：B/C（ICLR 2024）。
- **supports**：模型在 contextual privacy/theory-of-mind/secret-keeping 上会与人类判断偏离；简单“保持隐私”提示不足。
- **does not support**：benchmark 是隐私真理仲裁者；所有模型/部署同一失败率；CI 自动修复模型。
- **限制**：合成 tiers、特定模型、文化判断。
- **未决**：真实 agent 工具行为与长期记忆。

## PIC-11｜多主体 interdependent privacy benchmark
- **URL**：https://arxiv.org/html/2606.09908v1
- **证据级**：C（2026 预印本）。
- **supports**：单一 subject 五元组需扩展以表示共同/相关他人；LLM 在 context switching/多主体上困难。
- **does not support**：2026 扩展属于原书；合成 judge 足以证明真实安全。
- **限制**：预印本、LLM judges、synthetic pipeline。
- **未决**：人工复核与现实数据。

## PIC-12｜九步 heuristic 现代路线图
- **身份**：Kumar et al. (2024), CSCW, “A Roadmap for Applying the Contextual Integrity Framework…”
- **URL**：https://pearl.umd.edu/wp-content/uploads/2024/04/Kumar_etal-2024-CSCW-CI.pdf
- **证据级**：B（独立操作化）。
- **supports**：1–5 描述实践/情境/参数/规范，6 prima facie，7 moral-political，8 contextual ends，9 recommendation；指出许多研究只做描述半程。
- **does not support**：路线图是 Nissenbaum 原文逐字替代；完成九步即正确。
- **限制**：定性研究导向。
- **未决**：组织级 stop/appeal 的实证。

## D1｜本 Skill 综合
- **位置**：`SKILL.md`、CLI、模板。
- **证据级**：D。
- **supports**：FLOW 缩写、baseline/new/delta 制品、vulnerability gate、高风险受控失败。
- **does not support**：Nissenbaum 提出 FLOW；自动规范裁决；法律/部署批准。
- **未决**：需情境参与者、隐私/安全/法律与独立评估共同验证。
