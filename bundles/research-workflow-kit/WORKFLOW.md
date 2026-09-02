# 人工在环科研工作流

## 阶段与出口标准

| # | 阶段 | 必要输入 | 必要输出 | 出口门禁 |
|---:|---|---|---|---|
| 0 | Research Charter | 目标、角色、资源、风险 | 章程、决策权、伦理/隐私初筛 | 负责人批准范围和权限 |
| 1 | Question & Scope | 模糊问题、已有材料 | 可检验问题、边界、协议草案 | 问题和不能回答内容获批 |
| 2 | Search Protocol | 问题、概念块 | 数据库、查询、日期、纳排/去重规则 | 正式检索前冻结协议 |
| 3 | Acquisition & Evidence | 导出记录、合法全文 | search/screening log、证据表、claim-source map | 关键来源与位置已核验 |
| 4 | Methods & Analysis Plan | 证据、数据条件 | 设计、样本/材料、指标、模型、停止规则 | 看最终结果前批准 |
| 5 | Execution | 合法输入、锁定环境 | Notebook/脚本、配置、运行日志、原始输出 | 血缘完整，失败保留 |
| 6 | Manuscript | 已批准 claim-evidence | 大纲、文稿、图表、披露草案 | 无无证据核心 claim |
| 7 | Internal Review | 文稿和复现材料 | 引用审计、模拟评审、修订矩阵 | 缺陷处置或明确阻塞 |
| 8 | Release | 全部已审制品 | 复现报告、限制、release checklist | 作者/机构/venue 最终确认 |

## 推荐组队

通常使用 1 个主 Skill + 1–3 个互补 Skill：

- 文献：orchestrator + systematic-evidence-synthesis + paper search + citation verification；
- 定量：question-protocol + experimental-design + statistical-analysis + reproducible-analysis；
- 质性：question-protocol + qualitative-mixed-methods + evidence-synthesis + integrity-disclosure；
- 写作：orchestrator + scientific-writing/paper-spine + peer-review + integrity-disclosure；
- ML：orchestrator + experiment plan/run + reproducible-analysis + independent review。

同一 Agent 可以承担多个低风险角色，但高影响结论应由没有参与原始分析的独立 Reviewer 检查。

## 规范文件

- Markdown：章程、协议、解释、决策、评审、限制；
- CSV/TSV：检索、筛选、证据、数据字典、引用审计；
- JSONL：逐 claim/逐来源映射和机器日志；
- BibTeX/RIS：引用库交换；
- Notebook + 脚本：分析与展示；
- 环境锁：requirements/uv/conda/renv/container 等按项目选择。

Notion、Obsidian、Zotero、EndNote、SPSS、Word 和 LaTeX 可以同步或导出，但不可成为唯一审计副本。

## Claim–Evidence 门禁

每项核心结论记录：claim ID、原文、类型（背景/主要/次要/探索）、数据或来源、精确位置、统计证据、反例、限制、核验者、状态。只有 `verified` 的核心 claim 才能进入摘要和结论。

## 自动化边界示例

```yaml
max_rounds: 3
max_wall_time_hours: 4
max_compute_cost_usd: 20
allowed_directories: [05-analysis]
allowed_network: [arxiv.org, api.crossref.org, api.openalex.org]
human_approval_required_for:
  - changing_primary_question
  - purchasing_compute
  - processing_sensitive_data
  - external_publication
  - deleting_raw_data
stop_on:
  - evidence_integrity_failure
  - repeated_failure_twice
  - budget_exceeded
```

这是需按项目修改的示例，不是对网络、预算或数据的默认授权。
