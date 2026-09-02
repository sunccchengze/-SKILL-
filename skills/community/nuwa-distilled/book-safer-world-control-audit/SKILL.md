---
name: book-safer-world-control-audit
description: |
  基于 Nancy Leveson《Engineering a Safer World》把复杂社会技术系统的损失、危险、安全约束、层级控制结构、过程模型、反馈、不安全控制动作、loss scenarios 与运行风险迁移编译为可追踪审计。
  当用户需要 STAMP/STPA/CAST、软件与人机交互安全、组织/监管控制、四类 UCA、领先指标或 AI/agent 安全控制结构时使用。
  不把可靠性当安全，不把候选场景当已验证因果，不把 STPA 当概率风险量化、完整性证明或认证。高影响领域缺真实影响、owner、独立复核、申诉、stop/rollback 时受控失败；输出不是部署批准。
---

# 《Engineering a Safer World》社会技术安全控制 Skill

> **对象**：不是给部件列更多故障，而是问“哪些约束必须维持，谁有控制权，依据何种过程模型行动，得到什么反馈，系统为何仍会进入危险状态？”

## 1. 使用 / 禁用

**使用于**：复杂软件/AI/医疗/交通/运营系统；传统 FMEA/FTA 可能漏交互；安全责任跨团队/供应商/监管；自动化按设计运行也可能致险；事故后需 CAST 学习；上线后有迁移、压力和变更。

**不可单独用于**：
- 替代法规/标准认证、概率风险评估、FMEA/FTA/HAZOP 或安全 case；
- 从模板空白数宣称 completeness；
- 把“人是 controller”写成 blame；
- 让 LLM 自动签署 constraint、risk acceptance 或 go-live；
- 紧急事故时延迟 containment、救援、报告或证据保全。

## 2. 版本与层级

| 层 | 边界 | 纪律 |
|---|---|---|
| A | © 2011 首版文本（MIT Press 正式出版/OA eBook 2012；paperback 2016） | 写 Leveson 的系统理论主张，不冒充比较试验证明 |
| B | 2018 STPA Handbook、CAST Handbook、后续扩展 | 标后续版本，不倒灌为首版步骤版式 |
| C | 独立比较/验证、铁路/航空/LES/AI 案例和批评 | 并列收益、成本、主观性、V&V 限制 |
| D | CONTROL、CLI、发布门 | 明写本 Skill 创建 |

## 3. 认识论与安全合同

1. **safety ≠ reliability**：可靠部件可通过不安全交互制造损失；失效分析仍有价值但不充分（ESW001–ESW003）。
2. **hazard ≠ cause ≠ loss**：loss 是不可接受结果；hazard 是系统状态；cause/scenario 解释怎样到达（ESW011）。
3. **constraint 优先于 failure**：先写系统必须保持的行为边界，再找控制结构如何失败（ESW004、ESW012）。
4. **control 是广义影响**：设计、政策、激励、训练、监管、权限、自动化、反馈皆可构成控制（ESW005–ESW006）。
5. **过程模型会错**：人/软件依据不完整、过时或不一致的内部模型发动作；反馈延迟同样关键（ESW007）。
6. **UCA 必须情境化**：四类 guideword 不是四条风险；每项要 controller/action/context/hazard link（ESW009–ESW010）。
7. **没有 completeness guarantee**：分析范围、知识、人员和资源决定覆盖；独立验证不可省（ESW019–ESW022）。
8. **分析不是安全声明**：输出固定 `hazard_analysis_not_safety_certification`；高影响仍需真实 test/operation evidence（ESW027–ESW028）。

## 4. 六个核心模型（三重验证）

### M1 安全是受约束的控制问题
- **跨域**：技术系统、组织、监管、运营都通过约束维持非危险行为。
- **生成力**：从每个 loss 反推 hazard 与 system constraint。
- **排他性**：不是从 failure mode 开始。
- **失败门**：constraint 若不可观察/验证，只是愿望。

### M2 层级社会技术控制结构
- **跨域**：government/regulator → company management → engineering/operations → automation/humans → process。
- **生成力**：标 authority、responsibility、control action、feedback、coordination、development-operation interface。
- **排他性**：把组织与技术放在同一因果模型，不用“文化”作残余桶。
- **失败门**：责任无 authority/resources 或反馈不回到 controller 时标 structural gap。

### M3 controller process model
- **跨域**：飞控软件、临床人员、运营经理和监管者均依内部状态估计行动。
- **生成力**：问 model variables、更新来源、延迟、假设、错配条件。
- **排他性**：解释“按程序做仍错”而不只找故障。
- **失败门**：只写“human error”不写当时信息/目标/压力，退回重做。

### M4 四类 Unsafe Control Action
- not provided when required；provided when unsafe；wrong timing/order；stopped too soon/applied too long。
- **生成力**：对每个 control action 全遍历，写 actual hazardous context。
- **排他性**：遗漏、发出、时序、持续时间都纳入。
- **失败门**：把原因写进 UCA 会过早缩小搜索；原因留到 loss scenario。

### M5 loss scenario 穿过完整控制回路
- **跨域**：controller algorithm/process model、input、sensor/feedback、actuator/path、controlled process、environment、coordination。
- **生成力**：既找导致 UCA 的情境，也找 action 已正确给出但未正确执行的路径。
- **排他性**：不把单一部件 failure 列表冒充 scenario。
- **失败门**：scenario 不能追到 hazard/constraint/verification 就不进入 safety requirement。

### M6 动态迁移与运营学习
- **跨域**：绩效压力、预算、人员、维护、软件更新、环境变化让系统漂移。
- **生成力**：leading indicator、assumption monitor、management of change、stop/rollback、CAST loop。
- **排他性**：安全不是设计评审一次完成。
- **失败门**：没有 owner 与触发阈值的“持续监测”不算控制。

| 模型 | 跨域 | 生成 | 排他 | 保留 |
|---|---|---|---|---|
| constraint control | 全生命周期 | loss→constraint | 非 failure-first | 是 |
| hierarchy | 技术/组织/监管 | authority/feedback | 社会技术同模 | 是 |
| process model | 人/自动化 | 错配机制 | 非 blame | 是 |
| four UCA | 每个 action | 情境矩阵 | 时序/持续 | 是 |
| loss scenario | 完整 loop | 可验证约束 | 非单因列表 | 是 |
| migration | operations/change | leading controls | 非一次审计 | 是 |

## 5. CONTROL 主工作流（D 层）

### C — Consequences
列 losses（生命/健康/权利/环境/资产/使命/信任），由受影响方参与定义；不要只列公司损失。写严重度但不伪造概率。

### O — Operational boundary
画系统边界、环境、生命周期、决策层、供应商、监管、开发/运营接口。边界外因素必须有接口与 owner，不能用“out of scope”删除实际控制。

### N — Name hazards
hazard 写系统状态/条件 + worst-case environment；每个 link 到 loss。由 hazard 反写 system constraint：`System must [behavior] when [context]`。

**反例**：“模型 hallucination”常是 cause/behavior，须写它使系统进入什么危险状态。

### T — Trace control structure
每个 controller 记录：responsibility、authority、process model、control algorithm、inputs、control actions、feedback、delay。检查：
- 下行 constraint 与上行 feedback 是否闭合；
- 多 controller 谁协调；
- 目标/激励冲突；
- 谁能 halt；
- 变更如何同步到训练/程序/模型。

### R — Requirements / constraints
保持 trace：`L → H → SC → controller responsibility → CA/UCA → LS → requirement → verification → operational indicator`。重复/冲突 constraints 需合并或裁决；不能从模糊 scenario 直接生成 requirement。

### O — Observe unsafe actions
对每个 CA 遍历四类 UCA。模板：
`[Controller] [not/provides/timing/duration] [CA] when [actual context], leading to [H-ID].`

再写 controller constraint；**不要**在 UCA 中塞 process-model 原因。

### L — Learn in operation
对 UCA 建 loss scenarios：错误 input、算法、process model、反馈、delay、execution path、process/environment、coordination、组织压力。为每项指定：prevention/detection/recovery、verification evidence、owner、leading indicator、stop/rollback。事故后走 CAST，不用“root cause=operator”。

## 6. 安全 requirement 验证卡

| 字段 | 必填问题 |
|---|---|
| trace | 对应哪些 L/H/UCA/LS？ |
| controller | 谁有 authority/resources？ |
| behavior | 可观测、可测试吗？ |
| context | 何时必须/禁止？ |
| feedback | controller 如何知道执行与效果？ |
| degraded mode | sensor/模型/人不可用时怎样？ |
| verification | analysis/test/simulation/field evidence 各是什么？ |
| operation | leading indicator、threshold、owner、response？ |
| change | 更新、供应商、组织变化怎样回归？ |
| recovery | stop、safe state、rollback、incident/appeal？ |

## 7. 常见失败模式

| 失败 | 表现 | 修复 |
|---|---|---|
| reliability laundering | 冗余高所以安全 | 加交互/constraint 分析 |
| hazard/cause 混写 | “传感器失败”作 hazard | 改为危险系统状态 |
| box-only diagram | 有方框无 authority/feedback | 每条边标 action/feedback/delay |
| UCA 无 context | “系统不应错误输出” | actual state + hazard link |
| scenario=单故障 | 只列 sensor fails | 绕完整 loop 与组织接口 |
| human error stop | 前线归责 | process model、反馈、目标、工作条件 |
| requirement leap | “加强培训” | trace + behavior + verify |
| more hazards=better | 数量竞赛 | severity/relevance/duplicates/verification |
| STPA replaces all | 删除 FMEA/FTA/PRA | 说明互补接口 |
| static safety | 上线即结束 | migration/indicator/change/CAST |
| LLM authority | 自动场景直接签核 | candidate_not_validated + SME/independent challenge |
| certification laundering | 报告完整=安全 | status 固定非认证 |

## 8. 高影响门与 CLI

强制字段：`accountable-owner / applicable-rule / affected-group / real-impact-evidence / independent-review / appeal-path / rollback-trigger / stop-condition`。CLI 记录但不核实。

```bash
python3 scripts/analyze_safety_control.py \
  --system "工具调用型AI客服" --boundary "用户请求到工具执行与人工接管" \
  --loss "错误退款造成客户财务损失" \
  --hazard "未经授权的退款指令可到达支付系统" \
  --controller "AI编排器" --controller "人工主管" \
  --control-action "批准退款" --feedback "支付执行状态与权限校验结果" \
  --domain engineering --risk-level moderate --format markdown
```

输出会为每项 CA 创建四类候选槽，全部 `candidate_not_validated`；不计算 risk score。

## 9. 内在张力与边界

- **广边界 ↔ 可执行范围**：边界过窄漏系统因果，过宽让分析失控；用分层/接口而非删除。
- **系统责任 ↔ 个体责任**：系统解释不取消故意、违法或专业义务；也不以个体责任终止系统学习。
- **全面枚举 ↔ prioritization**：STPA 无内置概率优先级，须另接严重度/证据/法规/PRA。
- **定性洞察 ↔ V&V**：专家一致不是验证；simulation/test/operation 与独立 challenge 必须另留。
- **早期分析 ↔ 设计细节不足**：假设显式版本化，随设计迭代。
- **安全约束 ↔ mission pressure**：冲突须交授权 owner，不能静默让吞吐覆盖安全。
- **自动化扩展 ↔ 分析者风险**：LLM 可辅助枚举，但自身需版本、日志、validator 和人类责任。

本包不声称 STPA 优于所有传统方法、不提供认证、不验证任何用户系统安全，也不把 2025/2026 AI 应用归给 © 2011/正式出版 2012 的原书。

## 10. 深入资料

[`references/source-notes.md`](references/source-notes.md) · [`references/claim-layer-map.md`](references/claim-layer-map.md) · [`references/templates.md`](references/templates.md) · `references/research/01`–`06` · [`VALIDATION.md`](VALIDATION.md)
