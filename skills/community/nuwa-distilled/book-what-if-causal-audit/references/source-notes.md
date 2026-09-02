# 来源账本：*Causal Inference: What If*

> 检索日期：2026-08-16。证据级：A=锁定原书/正式标准或原始研究；B=作者论文、系统综述/权威方法报告；C=评论/案例；D=本包综合。`supports` 与 `does not support` 同等强制。

## CIW-01｜锁定原书 PDF
- **身份/版本**：Hernán & Robins, *Causal Inference: What If*, PDF dated 2025-05-27；2025 同行书评将书目标为 2020（2025 revision）、ISBN `9781420076165`、350pp，但锁定 PDF 自身仍写明 print version “expected”。
- **URL**：https://miguelhernan.org/whatifbook （PDF 镜像文件名 `hernanrobins_WhatIf_27may25.pdf`）
- **证据级**：A；本包 A 层主锚。
- **supports**：反事实效应、随机/观测设计、exchangeability/positivity/consistency、DAG、偏差、标准化、IPW、g-formula、MSM、g-estimation、IV、target trial。
- **does not support**：任何具体用户问题已识别；ML 可弥补未测混杂；字段完成即行动许可；存在一个已核验的 2025 正式印刷版。
- **冲突/限制**：living text；书评的页数/ISBN 书目与锁定 PDF 的“即将印刷”说明不能合并成已出版事实；某些识别条件是特定方法下的充分条件，不能普遍化为一切框架的唯一必要条件。
- **未决**：ISBN 书目与 2025-05-27 PDF 的逐页/载体关系未校勘。

## CIW-02｜作者官方入口与版本身份
- **URL**：https://miguelhernan.org/whatifbook
- **证据级**：A（作者一方的书目/下载入口）。
- **supports**：作者、免费文本、数据/代码资源、持续修订身份。
- **does not support**：网页版本永不变化；第三方复现成功。
- **版本边界**：本包冻结 2025-05-27，不静默跟随未来更新。
- **限制/冲突**：未发现可直接裁定本条书目/范围事实的独立冲突；用途限于上述 supports 与版本边界。
- **未决**：网站未来重定向需锁文件哈希时另做归档。

## CIW-03｜目标试验七项与 observational emulation
- **身份**：Hernán & Robins (2016), “Using Big Data to Emulate a Target Trial When a Randomized Trial Is Not Available.”
- **URL/DOI**：https://pmc.ncbi.nlm.nih.gov/articles/PMC4832051/ ; doi:10.1093/aje/kwv254
- **证据级**：B（作者原始方法论文）。
- **supports**：资格、策略、分配、随访、结局、因果对比、分析计划；先写 trial 再映射数据。
- **does not support**：emulation 等同随机化；七项完整能消除混杂。
- **限制/冲突**：医学示例；跨领域须重新定义可干预策略与权利。
- **未决**：用户领域数据能否支持共同 time zero。

## CIW-04｜time-zero 与 immortal-time 偏差
- **身份**：Hernán et al. (2016), “Specifying a target trial prevents immortal time bias…”
- **URL**：https://pubmed.ncbi.nlm.nih.gov/27237061/
- **证据级**：B。
- **supports**：eligibility、assignment、follow-up 对齐可防可避免的时间偏差。
- **does not support**：对齐后结果即无偏。
- **限制**：重点是比较效果/安全研究的相对简单策略。
- **未决**：动态/宽限期策略需 cloning/censoring/weighting 或其他设计。

## CIW-05｜2025 修订版书评
- **URL**：https://gacetasanitaria.org/en-book-review-articulo-S021391112500041X
- **证据级**：C（同行期刊书评）。
- **supports**：2020/2025 修订身份、三部分结构、living book、ISBN 与方法范围。
- **does not support**：对每个方法的独立效度验证。
- **冲突**：书目数据库对 2020/2025、312/350/352 页并不一致；本包以标题页日期+ISBN 锁定而不混页码。
- **未决**：无。

## CIW-06｜识别条件原始章节镜像核对
- **URL**：https://static1.squarespace.com/static/675db8b0dd37046447128f5f/t/6835bdb7dc9e482163d8712d/1748352541538/hernanrobins_WhatIf_27may25.pdf
- **证据级**：A（锁定 PDF 的可检索镜像）。
- **supports**：书中明确称观测识别条件常“heroic”，无论测多少变量都不能仅凭数据验证无未测混杂。
- **does not support**：所有观测研究均无意义。
- **限制**：镜像稳定性不如作者入口。
- **未决**：长期保存应记录哈希，本轮未纳入整本文件以避免版权/体积问题。

## CIW-07｜TARGET 报告声明
- **身份**：2025 TARGET Statement, JAMA。
- **URL**：https://jamanetwork.com/journals/jama/fullarticle/2837724
- **证据级**：A/B（正式报告指南；方法后续）。
- **supports**：target trial 与 emulation 双写、识别假设、设计偏差、残余混杂/测量限制透明报告。
- **does not support**：报告清单评分即内部效度；本书作者已在 2025-05-27 版逐条采纳。
- **限制**：报告规范，不是效果验证。
- **未决**：不同领域报告扩展。

## CIW-08｜TTE 报告审查
- **身份**：Matthews et al. (2023), 202 项研究审查。
- **URL**：https://pmc.ncbi.nlm.nih.gov/articles/PMC10534275/
- **证据级**：B（系统抽取）。
- **supports**：42% 未完整描述 emulation；仅 44% 同时明确写 target protocol 与 emulation；因果对比报告 73%。
- **does not support**：缺项必然造成某个方向/大小的偏差。
- **限制**：截止当时文献与编码规则。
- **未决**：2025 TARGET 后是否改善。

## CIW-09｜DML 方法评估
- **URL**：https://arxiv.org/html/2403.14385v1
- **证据级**：B/C（方法综述+模拟，预印本）。
- **supports**：DML 可改善非线性 nuisance 估计，却不能发现未测混杂或坏控制；识别须先独立成立。
- **does not support**：DML 总优于参数模型；所有 causal ML 都相同。
- **限制**：模拟设计和特定实现；非同行终版锁定。
- **未决**：正式发表版本差异。

## CIW-10｜ICU 因果研究 scoping review
- **URL**：https://www.nature.com/articles/s41746-023-00961-1
- **证据级**：B。
- **supports**：真实应用中 exchangeability/positivity/consistency 报告和诊断不足；RL 与 g-methods 共享强因果假设。
- **does not support**：结果外推所有行业；任何 RL 动态策略无效。
- **限制**：ICU 文献与纳入标准。
- **未决**：不同风险领域的审查。

## CIW-11｜2026 positivity/consistency 批评
- **URL**：https://academic.oup.com/aje/advance-article/doi/10.1093/aje/kwag093/8663866
- **证据级**：C（方法争论文章，2026）。
- **supports**：positivity 的必要性依赖 estimand、target 与识别/建模路线；盲目限制样本可能伤害目标。
- **does not support**：标准化/IPW 不需要重叠；书中陈述错误。
- **冲突**：对“基础条件”口号提出限定；本包保留书中“for standardization/IPW”语境。
- **未决**：争论后续回应。

## CIW-12｜NIST AI RMF
- **URL**：https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf
- **证据级**：B（治理框架）。
- **supports**：高影响 AI 需治理、测量、管理、owner、影响与持续监控；技术分析不是部署批准。
- **does not support**：NIST 验证本书任何估计量；自愿框架满足所有法律。
- **限制**：后于本书且独立，必须 C 层。
- **未决**：法域和行业专门义务。

## D1｜本 Skill 综合
- **位置**：`SKILL.md`、`scripts/emulate_target_trial.py`、`references/templates.md`。
- **证据级**：D；作者为本包。
- **supports**：TARGET 工作流、假设账本、受控失败、高风险发布门、机器可读 provenance。
- **does not support**：Hernán/Robins 提出 TARGET 缩写；外部效度；因果/法律/部署结论。
- **未决**：需领域专家、受影响者与独立统计审查验证。
