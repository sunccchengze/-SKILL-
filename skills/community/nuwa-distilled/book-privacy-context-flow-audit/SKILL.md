---
name: book-privacy-context-flow-audit
description: |
  基于 Helen Nissenbaum《Privacy in Context》把隐私问题编译为社会情境、subject/sender/recipient/attribute/transmission-principle 五参数信息流、entrenched norm、参数偏离、prima-facie 判断与道德政治/情境价值评价。
  当用户审计跨情境数据共享、公共记录、平台追踪、推断数据、AI memory/agent、隐私政策、notice-and-consent 或目的变更时使用。
  不把隐私等同保密/安全/控制，不把公开数据当自由取用，不把多数预期当正当规范或签署同意当适当性证明。高影响领域缺 owner、规则、真实影响、受影响群体、争议、stop/rollback 时受控失败；输出不是法律或部署批准。
---

# 《Privacy in Context》情境信息流审计 Skill

> **对象**：不先问“这是不是敏感 PII”，而先完整描述“谁以何种情境角色，在什么条件下，把关于谁的哪类信息流向谁；这与支撑该情境的规范、目的和价值如何相合”。

## 1. 使用 / 不使用

**使用于**：跨组织/供应商数据流、secondary use、public records、追踪与画像、推断属性、AI 记忆/工具调用、医疗/教育/雇佣/信用/执法信息、隐私政策模糊、context collapse。

**不可单独用于**：
- 替代 cybersecurity、保密分类、DPIA、数据保护法、合同或 threat modeling；
- 以调查多数票自动制造正当规范；
- 用“用户同意了”结束分析；
- 把 context 简化为 app/网页 URL；
- 让 LLM 自动决定能否披露真实个人信息；
- 数据泄露/人身危险正在发生时延迟 containment 与通知。

## 2. 版本与层级

| 层 | 内容 | 纪律 |
|---|---|---|
| A | 2009-11-24 首版（copyright 2010），ISBN `9780804752374` | 书中 CI、五参数、九步 heuristic |
| B | 2004 论文、online/privacy 与 2019 data-food-chain 后续 | 标时间；AI/推断扩展不倒灌 |
| C | 逻辑形式化、policy/crowd 研究、vulnerability 批评、NIST、LLM benchmark | 写样本/形式化范围/权力限制 |
| D | FLOW、CLI、高影响门 | 本 Skill 创建 |

“2009 发行/2010 版权”不是两本不同内容的书；本包不编译未持有版次页码。

## 3. 认识论与规范合同

1. **privacy ≠ no flow**：适当流动可维持医疗、教育、家庭与政治；问题是 flow 是否符合正当情境规范（PIC001）。
2. **public ≠ up for grabs**：公开可见不清除 recipient、规模、持久、搜索、用途与 transmission principle（PIC002、PIC013）。
3. **context ≠ place/platform**：情境由 roles、ends、values、practices 构成，可能嵌套/冲突（PIC003）。
4. **五参数缺一不可**：subject、sender、recipient 是角色；attribute 是有情境意义的信息类型；transmission principle 是流动条件（PIC005–PIC008）。
5. **consent 是一个 TP，不是万能许可**：还要看权力、理解、拒绝成本、用途与其他参数（PIC008、PIC014）。
6. **departure 是 prima facie，不是最终裁决**：旧规范有初步推定，但可能不公或技术变化有更强理由（PIC009–PIC012）。
7. **expectation ≠ legitimacy**：调查/政策/习惯是 norm evidence，需再问谁定规范、谁缺席、是否压迫（PIC020–PIC021）。
8. **security ≠ privacy**：授权、加密的数据流仍可能违反情境；隐私适当的流仍需安全保护（PIC022）。
9. **审计不是许可**：状态固定 `prima_facie_privacy_audit_not_legal_approval`（PIC027–PIC028）。

## 4. 六个核心模型（三重验证）

### M1 appropriate flow 而非 sensitive-data 容器
- **跨案例**：病历给医生适当，给广告商可能不适当；公开法庭记录批量可搜索会改变 flow。
- **生成力**：同一 attribute 随角色/TP 改变结论。
- **排他性**：不靠“敏感/公开”二分。
- **失败门**：只给 PII category 而无 flow，不作 CI 判断。

### M2 社会情境作为规范结构
- **跨域**：healthcare、education、workplace、family、commerce、civic life。
- **生成力**：写 context purpose/values、角色职责、nested contexts 与侵入关系。
- **排他性**：不是设备地理位置、industry code 或“线上”总情境。
- **失败门**：无法说明该情境的社会 ends，只能给临时 scope 并标 contested。

### M3 五参数 flow tuple
`<subject, sender, recipient, attribute, transmission principle>`。
- **生成力**：每个实际 collection/disclosure/inference/tool call/retention flow 单列；复数角色拆行。
- **排他性**：TP 把 consent/confidence/reciprocity/warrant/sale/coercion/need-to-know 等独立出来。
- **失败门**：unknown 不填猜测；缺项状态 `incomplete_flow`。

### M4 entrenched norm 与 parameter delta
- **跨技术变化**：新 receiver、新 inferred attribute、新 purpose/TP、新规模/持久/搜索性揭示偏离。
- **生成力**：baseline tuple 与 proposed tuple 对照，不用“我们没改变数据”辩护。
- **排他性**：规范证据可来自 law、professional rules、practice、affected people；来源冲突并列。
- **失败门**：企业 policy 自己定义 norm 且无外部/受影响者证据时标 self-serving。

### M5 九步 decision heuristic 的描述—规范桥
1 描述实践；2 定 prevailing context；3 actors；4 attributes/TP；5 norms/points of departure；6 prima-facie；7 moral/political factors；8 contextual ends/values；9 recommendation。
- **生成力**：不止说“用户不舒服”，也不止服从旧惯例。
- **排他性**：最后判断同时看一般权利/正义与具体情境完整性。
- **失败门**：只做 1–5 不得输出 allow/reject。

### M6 vulnerability 与 downstream food chain 扩展
- **跨现代系统**：inference、data brokers、model memory、tool recipients、多主体信息。
- **生成力**：问看不见的 downstream recipients、derived attributes、共同 subjects、弱势群体、contestability。
- **排他性**：不把当前 UI 的 sender→recipient 当完整链。
- **失败门**：不能列 downstream/retention/inference 时，高影响 flow 暂停。

| 模型 | 跨域 | 生成 | 排他 | 保留 |
|---|---|---|---|---|
| appropriate flow | 多情境 | 关系判断 | 非 data label | 是 |
| context | 社会领域 | ends/roles | 非平台 | 是 |
| five tuple | 全链路 | 可审计 flow | 独立 TP | 是 |
| norm/delta | 技术变更 | 基线对照 | 非“same data” | 是 |
| nine steps | 描述/评价 | recommendation | 非现状主义 | 是 |
| vulnerability/downstream | AI/平台 | 隐形流与权力 | 非单主体 UI | 是 |

## 5. FLOW 主工作流（D 层）

### F — Frame social context
- 情境名不是产品名；写 purpose、values、roles、constitutive norms；
- 列 nested/competing contexts（例如 workplace health ↔ employment evaluation）；
- 写谁有权定义情境，受影响者是否认可；
- 紧急法律/保护义务先处理。

### L — List five-parameter flows
对每个 collection、generation/inference、disclosure、sale、tool call、memory retrieval、retention、deletion 分行：
- subject（可多主体/群体）；
- sender role；recipient role（含 processors/model/vendor）；
- attribute（observed/derived/inferred）；
- TP（consent/confidence/reciprocity/purpose-bound/legal duty/warrant/sale/coercion 等）；
- purpose、frequency、scale、persistence、searchability、jurisdiction。

不得写“系统把数据给第三方”这种角色/属性/TP 不完整句。

### O — Observe norms and departures
建立 baseline 与 proposed flow 对照。norm evidence ledger：来源、日期、样本/authority、支持/不支持、谁缺席、冲突。delta 对五参数逐项标 changed/unchanged/unknown，并另看 scale/linkage/inference。

**Prima-facie 规则**：显著 departure → review，不自动 reject；无 apparent departure 也继续检查隐形 downstream 与不公 norm。

### W — Weigh legitimacy and controls
依九步后半：
- 一般 moral/political：自治、尊严、非歧视、权力、权利、伤害/收益、公平；
- 情境：实践促进还是破坏该 context 的 ends、roles、trust；
- alternatives：限制 recipient、attribute、TP、purpose、retention，而非只有 all/none；
- controls：purpose binding、access/log、minimization、inference limits、notification、contest/correction/deletion、vendor/model contracts；
- recommendation：allow / modify / pause / reject，附 owner、evidence、review/stop/rollback。

## 6. Flow 与 norm 卡

```text
FLOW-ID / version:
Context / purpose / values:
Subject role(s):
Sender role:
Recipient role(s):
Attribute: observed | derived | inferred
Transmission principle:
Purpose / scale / frequency / retention / linkage:
Baseline norm + evidence for/against + missing voices:
Parameter delta:
Prima-facie status: conforming | departure | contested | unknown
Moral/political + contextual evaluation:
Control / owner / contest / stop / rollback:
```

## 7. 失败模式

| 失败 | 表现 | 修复 |
|---|---|---|
| security substitution | 加密所以无隐私问题 | 审计授权但不适当 flow |
| consent laundering | TOS 勾选即允许 | consent 作为一个 TP + power/refusal cost |
| public-is-public | 可见即可批抓/画像 | receiver/scale/searchability/purpose delta |
| context=platform | “在 App 内” | social ends/roles/norms |
| role erasure | Google/医院/用户 | advertiser/processor/clinician/employer 等 capacity |
| attribute flattening | 统称 PII | 情境信息类型+inference |
| policy=practice | 文本承诺即真实 flow | runtime logs/vendor lineage |
| norm=majority | 调查 60% 即正当 | minority/vulnerability/rights |
| status quo lock | 旧规范不可改 | steps 7–9 正当化评价 |
| novelty waiver | 没旧规范所以自由 | analog contexts + values + precaution |
| single-subject | 忽略家人/群体推断 | multi-subject/group map |
| binary control | 全收或全禁 | 调 receiver/attribute/TP/retention |
| LLM privacy judge | 模型说可以披露 | benchmark 显示失误；人类/制度 gate |
| legal approval | CI 通过即合规 | law/DPIA/security/contract 另审 |

## 8. 高影响门与 CLI

人员、劳动、医疗、教育、信用、执法、内容治理强制：`accountable-owner / applicable-rule / affected-group / impact-evidence / contest-path / rollback-trigger / stop-condition`。`contest-path` 必须允许更正、反对和非原决定者复核。

```bash
python3 scripts/audit_contextual_flow.py \
  --context "大学教学" --context-purpose "支持学习与公平评估" \
  --subject "学生" --sender "课程教师" --recipient "助教" \
  --attribute "课程成绩" --transmission-principle "履职所需且保密" \
  --baseline-norm "教师可为课程反馈将成绩给该课程助教，助教须保密" \
  --proposed-change "把成绩发送给外部模型供应商生成学习建议" \
  --norm-evidence "课程政策v3" --domain general --format markdown
```

CLI 不连接数据系统、不判法律、不决定 norm，只保存候选 flow 与 delta。

## 9. 内在张力与边界

- **稳定规范 ↔ 技术/道德进步**：旧规范给初步推定，但不能锁定歧视或阻止更好实践。
- **context specificity ↔ universal rights**：情境解释细节，一般权利防地方规范压迫。
- **flow benefit ↔ privacy**：隐私不是停流；优化 recipient/attribute/TP 可保社会功能。
- **consent ↔ power/resignation**：形式选择在高拒绝成本下可能失真。
- **empirical expectation ↔ legitimacy**：可测预期不等于应然；分歧必须保留。
- **semantic richness ↔ scalability**：五参数具体化提高意义，却增加维护；用 ontology/versioning，不删语义。
- **individual ↔ interdependent/group privacy**：一个 flow 可同时关于多人/群体。
- **privacy ↔ safety/legal duties**：保密可与救援/报告冲突；用明确 TP、最小必要和审计，不绝对化。

本包不声称 CI 自动解决所有隐私问题，不替代 security/法律/伦理/受影响者 deliberation，也不把后续 LLM 研究冒充原书预测。

## 10. 深入资料

[`references/source-notes.md`](references/source-notes.md) · [`references/claim-layer-map.md`](references/claim-layer-map.md) · [`references/templates.md`](references/templates.md) · `references/research/01`–`06` · [`VALIDATION.md`](VALIDATION.md)
