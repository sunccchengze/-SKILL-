---
name: research-workflow-orchestrator
description: 跨平台、人工在环的科研项目总控。用于识别科研阶段，选择少量专项技能，建立研究问题、检索、证据、方法、分析、写作、审查、披露与复现制品，并阻止从模糊想法直接跳到代写论文或自动投稿。
---

# Research Workflow Orchestrator

这是科研生命周期的薄路由器，不替代领域专家、伦理审批、统计顾问或专项 Skill。默认中文工作；题名、检索式、变量和引用保留原语言。

## 1. 启动时先做吸收报告

先扫描可用技能的名称、描述、来源和依赖，只完整阅读当前阶段需要的 1 个主技能及最多 3 个互补技能。开始实质工作前报告：

1. 扫描了哪些元数据，当前处于哪个研究阶段；
2. 明确调用哪些 Skill，各负责什么制品；
3. 每项 Skill 的关键步骤、门禁、验证证据和失败回退；
4. 哪些候选本轮不调用，为什么。

不得用“已经参考全部技能”代替真实调用记录。

## 2. 阶段路由

| 阶段 | 必要制品 | 推荐专项能力 | 人工门禁 |
|---|---|---|---|
| 0 章程 | `research-charter.md`、风险分类 | 本技能、academic-integrity-ai-disclosure | 负责人、权限、预算、数据边界确认 |
| 1 问题 | `research-question.md`、`protocol.md` | research-question-protocol、ideation | 问题可检验且范围获批 |
| 2 检索 | `search-strategy.md`、`search-log.csv` | systematic-evidence-synthesis、paper search | 数据库、检索式、日期、纳排标准获批 |
| 3 证据 | `evidence-table.csv`、`claim-source-map.jsonl` | PDF、citation、paper card | 关键来源已读且支持边界已核验 |
| 4 方法 | `analysis-plan.md`、预注册草案 | experimental design、statistics、qualitative-mixed-methods | 主要指标、排除规则、停止规则获批 |
| 5 执行 | Notebook、脚本、运行日志 | reproducible-research-analysis、领域工具 | 数据权限、成本和执行范围获批 |
| 6 写作 | outline、manuscript、图表 | scientific writing、paper spine | 只写已批准 claim；作者负责文本 |
| 7 审查 | citation audit、internal review | peer review、citation verification | 独立审查完成，缺陷有处置记录 |
| 8 发布 | reproducibility report、AI disclosure | venue template、data availability | 全体作者、机构和 venue 规则确认 |

一次只推进当前阶段及其直接依赖。用户只要求文献综述时，不擅自运行实验或生成投稿稿件。

## 3. 不可跳过的六道门

- **Gate A：问题。** 对象、范围、变量、结果和不能回答的内容清楚；“新颖性”仍是待检索假设。
- **Gate B：来源。** 查询、日期、数据库、版本和筛选理由可重放；引用存在性与论点支持关系分别核验。
- **Gate C：方案。** 在看最终结果前固定主要假设、指标、样本/材料、排除规则、模型和停止规则。
- **Gate D：执行。** 原始数据只读；环境、配置、种子、成本、失败运行和数据血缘保留。
- **Gate E：结论。** 每项 claim 指向数据、统计量、图表或已核验来源；报告不确定性、反例和限制。
- **Gate F：发布。** 独立评审、引用审计、复现检查、许可/隐私/伦理和 AI 披露均完成。

门禁未通过时标记 `BLOCKED`，说明缺什么以及谁有权批准，不用顺滑文字掩盖。

## 4. 工具与平台原则

- Skill 名称不是命令；只有当前平台真实支持时才使用斜杠命令、MCP、子 Agent 或插件。
- Markdown、CSV、JSONL、BibTeX/RIS 和 Notebook 是规范文件；Notion、Zotero、EndNote、SPSS、Word 是可选连接器或导出目标。
- 浏览器检索结果只是候选来源；关键结论回到原文、数据库记录、DOI 或权威机构页面。
- 外部 API、付费工具和云执行先说明密钥、费用、数据出境和许可要求；不得索取或保存凭证到项目。
- 自动循环必须设置目录、网络、轮数、时间、预算和停止条件，且不能自行投稿、公开发布或联系第三方。

## 5. 默认交付格式

每次阶段性交付包含：

```markdown
## 本轮技能调用
- skill → 实际执行步骤 → 产生制品 → 验证证据

## 阶段状态
- 当前阶段：
- 已通过门禁：
- BLOCKED：
- 需要负责人决定：

## 证据与限制
- 已核验：
- 尚未核验：
- 反例/冲突：
- 下一步最小动作：
```

严禁编造数据、引用、伦理审批、作者贡献或复现结果；严禁代替研究负责人作原创性、伦理和最终结论判断。
