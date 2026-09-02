---
name: book-atlas-ai-stack-audit
description: |
  将 Kate Crawford《Atlas of AI》（2021）转化为 AI 全栈物质性、劳动、数据、分类、情感推断、国家与权力审计。
  当用户要评估 AI 采购、训练/标注供应链、数据来源、分类伤害、生物识别/情绪识别、数据中心环境声明、国家用途、补救与退出时使用。
  每项声明必须写系统边界、地域、日期、分母、来源与不确定性；禁止把企业/设施总量无依据地换算为单模型或单提示足迹，也不把一张“伦理清单”当完成正义。
---

# Atlas of AI Full-Stack Audit

> 基于 Kate Crawford, *Atlas of AI: Power, Politics, and the Planetary Costs of Artificial Intelligence*（Yale University Press, 2021）。原书从 Earth、Labor、Data、Classification、Affect、State 到 Power，并以 Space/基础设施视角贯穿。本包保持批判性视野，同时用独立证据校验、限定和操作化。

## 何时调用

- AI/LLM 采购、部署或退役前，需要看到云端接口背后的矿产、能源、水、硬件、废弃物与地点；
- 需要梳理直接员工、外包标注/审核、众包、内容生产者、受监控员工与补救；
- 需要审查 dataset 来源、同意/许可、代表性、分类 ontology、删除与维护；
- 用户声称可从脸、声音或行为“识别真实情绪/人格/意图”；
- 公共部门、警务、边境、福利、教育、医疗或雇佣系统需要国家—供应商—权利链条；
- 环境数字只有企业总量或设施总量，却要宣传“每次提示耗费 X”。

不用于：给公司做一张漂亮 ESG 图；从抽象批判直接推断某个具体供应商有违法或剥削；用本书代替当地工会、社群、原住民、环保或人权证据。

## 归因与方法纪律

- **原作**：Crawford 的综合论证是 AI 不是“云中无形智能”，而是嵌入资源提取、劳动、数据攫取、分类、国家机构与权力的产业/政治系统。
- **独立核查**：官方记录、同行评审实证、ILO、NIST、数据文档标准、人权/环境资料与受影响人陈述分开记录。
- **批评纳入**：原书跨度很广，个别机制、殖民/种族差异和“拒绝”政治的操作路径可能深度不足；本包不把宏观隐喻当本地事实。
- **本包综合**：`ATLAS-STACK`、八镜头、硬停止门与 CLI 是本 Skill 的审计设计，不伪称原书模板。

## 一、五个心智模型

### 模型1：AI is a situated stack, not a weightless model｜AI 是有地点的栈

系统边界至少覆盖提取/制造、数据生产、训练/推理、部署、维护与退役；列每个节点的地域、组织、合同、物质流和权力关系。

- **局限/失效**：全栈可无限扩张；必须公开 cut-off、分母和未知，不能以“尚未穷尽”拒绝任何决定。

### 模型2：Classification is an intervention into social order｜分类会介入社会秩序

标签、阈值和 benchmark 把历史制度与争议类别编码进系统；审计不仅问准确率，也问谁定义类别、谁被迫可见、谁能拒绝/申诉。

- **局限/失效**：并非所有分类都同等有害；具体效果依用途、错误成本、制度与补救，不能仅凭类别存在判罪。

### 模型3：Hidden labor is part of the technical system｜隐形劳动是技术组成

标注、清洗、内容审核、维护、客服和受系统管理的劳动不是外围“人类兜底”；合同层级、工资/安全、知识产权、申诉与 worker voice 是性能和正义条件。

- **局限/失效**：供应商披露不等于工人经验；个别访谈也不能自动代表全部地区/岗位，须防报复与抽样偏差。

### 模型4：A measurement needs construct validity before scale｜先问构念效度，再问规模

特别是 affect/情绪/人格推断：脸部动作、文化、语境与内在状态不是简单一一映射。准确率基准若标签本身无效，只会精确复制坏构念。

- **局限/失效**：反对普遍一一映射不等于任何上下文辅助信号都无信息；必须按具体任务、群体和后果评估。

### 模型5：Power is who can set boundaries, refuse, and obtain remedy｜权力体现在定边界、拒绝与补救

最终问题不是“模型是否有偏见”一个分数，而是谁采购、谁定义目的、谁承担成本、谁有审计权、谁能退出、谁获补偿、谁能停止系统。

- **局限/失效**：权力图本身不重分配权力；若无合同权、预算、worker/community voice 与强制补救，只是描述性地图。

## 二、A/B/C/D 声明分层

- **A｜原作层**：Crawford 的章节架构、案例与提取/权力论点，定位 `AT01–AT03`。
- **B｜原作内部限定层**：原书的范围、案例性质和宏观综合限制；不把案例无条件泛化。
- **C｜独立证据层**：劳动、datasheet、面部分析差异、情绪构念、环境、治理与反方评论，定位 `AT04+`。
- **D｜Skill 推论层**：本 Skill 的边界字段、eight-lens gate、停止/补救规则；不可写成“Crawford 证明本系统……”。

完整 ledger：[`references/claim-layer-map.md`](references/claim-layer-map.md)。证据相冲突时保留冲突，不投票压成“伦理分”。

## 三、ATLAS-STACK 十二步审计

### 1. PURPOSE/DECISION｜冻结用途和决定

写系统、决策者、生命周期阶段、目标、非目标、受影响者、替代方案和“完全不用 AI”。用途漂移触发重审。

### 2. BOUNDARY｜声明系统边界

为每条声明绑定：**geography、as-of date、denominator、lifecycle、organizational boundary、cut-off、uncertainty**。缺一不能跨层换算。

### 3. SPACE/MAP｜画地点与价值链

从矿产/芯片/设备、云区/数据中心、网络、数据生产、标注、模型、集成商、前台、维修到电子废弃物；区分已证实节点与待核节点。

### 4. EARTH｜审物质与环境

记录能源 mix、water withdrawal/consumption、碳范围、硬件寿命、矿产、土地、废物、峰值负荷与社区影响。每个数字保留原分母和 allocation method。

### 5. LABOR｜审劳动与声音

列直接/外包/众包/内容审核/数据主体/受算法管理者；记录合同链、地域、报酬、工时、安全、监控、申诉、组织权和 worker voice。不能只问一级供应商。

### 6. DATA｜审来源与持续维护

使用 dataset card：motivation、composition、collection、permission/legal basis、preprocessing、recommended/non-use、distribution、maintenance、deletion/withdrawal、known gaps。`web available` 不等于可自由提取或伦理同意。

### 7. CLASSIFICATION｜审 ontology 与错误分配

列标签如何产生、谁定义、训练/部署人群、交叉群体分母、false positive/negative 的真实后果、contestability 与类别漂移。平均准确率不能掩盖最坏群体。

### 8. AFFECT｜先做构念效度门

若从脸/声/行为推断内在情绪、人格、可信度、痛苦或欺骗：先要求 construct definition、ground truth 机制、context/culture 证据、reliability、specificity 和下游权利；否则 `BLOCKED_SCIENTIFIC_VALIDITY_REVIEW`。

### 9. STATE｜查公共权力与供应商接口

记录采购、监管、警务、边境、福利、教育、医疗、军事/情报、数据共享、records retention、审计豁免和 vendor secrecy。政府采用不是“普通客户”关系。

### 10. POWER/DISTRIBUTION｜画决定权与损益

谁能改目的/阈值/分类？谁收益？谁承担物质、劳动、隐私、误判与机会成本？谁不在数据中？谁无真实退出？分歧不能被总分抵消。

### 11. REMEDY/REFUSAL｜把纠正权写进合同

要求 notice、可理解理由、人工复核、申诉时限、独立审计、工人/社群参与、纠错/删除、赔偿、暂停与退出；注明触发者和执行资金。

### 12. DECIDE/REVIEW｜输出带条件的决定

只允许：`BLOCKED_*`、`INCOMPLETE_STACK_MAP`、`GOVERNANCE_REVIEW_REQUIRED`。不存在 CLI `APPROVED`。记录 minority report、开放问题、下次复审和退役义务。

## 四、八镜头最小问题

| 镜头 | 必答问题 | 典型证据 | 常见假完成 |
|---|---|---|---|
| Earth | 哪些材料、能源、水、排放、土地与废物在边界内？ | 设施/供应链原始记录、方法 | 企业总量÷提示数 |
| Space | 提取、计算、标注、部署、处置在哪里？ | 供应商/地点/合同图 | “云端”一个节点 |
| Labor | 哪些工人、条件、声音与申诉使系统存在？ | 合同链+安全访谈+工人组织 | vendor code of conduct |
| Data | 谁产生、允许、维护、退出？ | datasheet、lineage、许可/法律依据 | “公开数据” |
| Classification | 谁定义类别，错误如何分配？ | ontology history、分群混淆矩阵 | aggregate accuracy |
| Affect | 构念与 ground truth 有效吗？ | 心理测量/跨文化/情境研究 | 厂商 benchmark |
| State | 哪些公共权力/采购/监控关系？ | 合同、法定权限、保留/共享规则 | 只写产品用途 |
| Power | 谁决定、受损、申诉、获补救、能停止？ | 权利矩阵、remedy SLA、预算 | ethics principles |

## 五、硬停止与升级规则

- **情绪/人格/欺骗从脸部直接推断** → `BLOCKED_SCIENTIFIC_VALIDITY_REVIEW`；高风险场景默认不部署。
- **未记录第三方模型、dataset、插件或劳务链** → `BLOCKED_PROVENANCE`。
- **高风险生物识别分类** → `BLOCKED_RIGHTS_REVIEW`，须合法性、必要性、替代、差异、正当程序与禁用判断。
- **无 worker voice，却声称劳动审计完成** → labor lens 不完整；供应商自报不能补齐。
- **环境数字无边界/地域/日期/分母** → 不得比较或宣传。
- **无法申诉/纠错/停止** → power lens 不完整，即使模型平均性能高。
- **公共用途依赖商业保密拒绝审计** → 升级采购/法律审查，不以 NDA 作为安全证据。

## 六、量化与证据协议

### 环境数字

保留：source owner、metric definition、scope、location、period、denominator、allocation、uncertainty、renewable matching 方法。设施年耗水不能直接成为某模型训练耗水；企业排放不能直接成为单提示碳排。

### 劳动证据

至少三角校验：合同/政策、工人安全陈述、现场/监管/工会或独立研究。访谈须同意、防报复、翻译与数据最小化；不把“没有投诉”当没有伤害。

### 数据与分类

每个 source/label 记录合法依据与伦理争议、collection context、代表/缺席群体、用途限制、维护与撤回。差异指标报告 numerator/denominator、样本量与 uncertainty。

### 声明强度

`documented`（直接记录）、`corroborated`（独立交叉）、`reported`（有主体报告）、`estimated`（有模型/分母）、`unknown`。不得把 `unknown` 写成零。

## 七、反方、替代解释与非迁移

- Crawford 的宏观地图能揭示被产品叙事遮蔽的成本，但广度可能牺牲具体机制深度；本地审计需新增原始证据。
- 同一云设施服务多个产品；总量变化可能来自区域扩张、冷却、能源结构或容量闲置，不可全归一模型。
- 群体性能差异可能受样本、标签、照明、设备、任务/阈值影响；这不消除伤害，要求更具体诊断。
- worker experience 跨国家、承包层、岗位差异巨大；一处证据不可自动迁移。
- 某用途的分类合法/有效不代表用途漂移后仍可接受；state context 会改变强制性和退出真实性。
- “去偏”“绿色”“human-in-the-loop”是待审声明，不是证据类别。

## 八、CLI：生成 stack gap register

```bash
python3 scripts/audit_ai_stack.py \
  --system "市政文档分流" --purpose "路由服务请求" \
  --geography "Hong Kong" --as-of "2026-08-16" \
  --owner "服务负责人" --lifecycle-stage proposal \
  --supply-node "云区与设备处置链" --worker-group "外包标注员" \
  --data-source "居民提交" --classification "服务类别 taxonomy" \
  --affected-group "居民与一线员工" --state-linkage "公共采购与档案保留" \
  --material-evidence "provider region inventory" \
  --labor-evidence "合同与安全工人访谈计划" \
  --provenance-evidence "dataset lineage register" \
  --claim-denominator "年度服务工作量" \
  --remedy "人工改路由与申诉" --stop-condition "来源不可追溯"
```

CLI 不抓取供应链、不算足迹、不验证厂商陈述。它只标准化缺口并从不输出批准。

## 九、十组内在张力

1. **张力 1｜全栈广度 vs 可执行边界**：看得过窄会漏成本，看得无限宽则无法负责。
2. **张力 2｜量化可比 vs 分母诚实**：统一数字易比较，却可能掩盖地点、时期和 allocation 假设。
3. **张力 3｜供应商披露 vs 工人安全声音**：合同可查但被管理，访谈真实却有报复/抽样风险。
4. **张力 4｜分类一致 vs 社会类别争议**：稳定标签利于建模，也可能把制度历史自然化。
5. **张力 5｜性能提升 vs 构念无效**：benchmark 可涨，所测“情绪/可信度”仍可能不成立。
6. **张力 6｜个性化便利 vs 强制可见**：服务更精准，弱势群体也可能更难退出或保持模糊。
7. **张力 7｜国家能力 vs 正当程序**：公共效率可能增加，也扩大监控和无申诉决定。
8. **张力 8｜全球 AI 叙事 vs 地方差异**：产业链全球相连，劳动/环境/法律后果高度地方化。
9. **张力 9｜拒绝/暂停 vs 服务机会成本**：停止可防伤害，也可能延误可及服务；必须比较非 AI 替代。
10. **张力 10｜透明地图 vs 实质权力**：披露能见度不是补偿、谈判权或停止权。

## 十、表达DNA

- **句式**：先“这个数字/类别在哪个边界成立”，再说影响；不从抽象“AI”直接跳到结论。
- **词汇**：stack、site、supply chain、worker voice、ontology、construct validity、state、remedy。
- **语气**：批判但可核查；不用宏大隐喻替代具体主体、合同和分母。
- **节奏**：目的 → 边界 → 地点 → 物质 → 劳动 → 数据 → 分类/情感 → 国家 → 权力/补救。
- **确定性**：区分 documented、corroborated、reported、estimated、unknown。
- **引用**：Crawford 原作、独立实证、受影响人证词、本 Skill 推论分层标注。

## 十一、诚实边界

- 本 Skill 不证明某具体公司/政府违法、剥削或歧视；具体指控需要本地可核证材料与回应权。
- 生命周期地图永不天然完整；必须公开 cut-off、缺失供应商和未知，而不是称“全盘透明”。
- 数据中心、公司或电网总量不能无 allocation method 变成模型/用户/提示数字。
- 工人访谈和社群材料需安全、同意、翻译与反报复；不可为了审计再提取他们。
- Gender Shades 等实证说明被测系统/任务中的差异，不自动代表所有生物识别系统。
- 情绪构念的科学争议不能仅靠工程准确率解决；也不能把争议简化成“任何行为信号都没信息”。
- 本包不替代环境 LCA、劳动监察、法律/人权评估、原住民数据治理或民主采购程序。

## 十二、来源与执行导航

- [包说明](README.md)
- [参考导航](references/README.md)
- [18 条 A/B/C/D 声明](references/claim-layer-map.md)
- [来源与批评卡](references/source-notes.md)
- [八类审计模板](references/templates.md)
- [六轮研究日志](references/research/01-source-architecture.md)
- [验证记录](VALIDATION.md)
