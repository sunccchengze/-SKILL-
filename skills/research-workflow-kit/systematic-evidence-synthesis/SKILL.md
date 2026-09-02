---
name: systematic-evidence-synthesis
description: 可审计的文献检索、筛选、PDF 处理、引用图谱探索、证据提取与综合流程。用于叙述综述、范围综述、系统综述、证据地图和研究缺口分析，强制记录查询、日期、数据库、去重、纳排理由和 claim-source 映射。
---

# Systematic Evidence Synthesis

本技能不会把普通网页搜索包装成系统综述。采用何种报告规范（如 PRISMA、PRISMA-ScR、领域专门指南）由研究类型和当前版本决定，并记录核验日期。

## 1. 预先写检索协议

记录：研究问题、概念块及同义词、数据库、灰色文献范围、语言和日期限制、完整查询式、检索日期、纳排标准、去重键、筛选人数/冲突处理、停止条件和更新计划。

至少区分：

- **发现检索**：扩大词表、找关键作者/综述；
- **正式检索**：按冻结查询运行并保存数量；
- **补充检索**：向前/向后引文、相关论文、作者追踪；
- **更新检索**：在明确日期重跑。

若平台没有引文图谱 API，只能使用实际可访问的 Crossref、OpenAlex、Semantic Scholar、PubMed、出版社或参考文献列表；不得声称完成了图遍历。

## 2. 来源台账

`search-log.csv` 至少含：database、query、executed_at、filters、result_count、export_file、notes。

`screening-log.csv` 至少含：record_id、title、doi_or_url、stage、decision、reason、reviewer、decided_at。

保留检索导出原件；DOI、PMID、arXiv ID、规范化题名和年份用于去重，但自动去重结果要抽查。

## 3. PDF 与全文

- 只通过开放获取、机构授权、作者稿或用户合法提供的文件取得全文；不绕过付费墙或访问控制。
- 保存原始文件哈希、来源 URL、访问日期和版本（preprint/AAM/version of record）。
- OCR、版面解析和表格抽取均记录工具与失败页；关键数字回看渲染页、图、表或补充材料。
- 摘要能支持的结论有限；未读全文不得标记为全文核验。

## 4. 证据提取

`evidence-table.csv` 建议字段：

```text
record_id,citation,study_type,population_or_corpus,setting,sample,
exposure_or_method,comparator,outcomes,estimate,uncertainty,limitations,
risk_of_bias,source_location,extractor,verified,status
```

逐项区分作者报告、提取者解释和本项目推断。`source_location` 精确到页/段/图/表。双重提取或抽查规则在协议中确定。

## 5. 综合

先按问题和研究设计分层，再决定叙述、表格、meta-analysis 或不合并。异质性过高时不强行给一个总效应。缺口分为：

- 没有研究；
- 有研究但样本/场景有限；
- 结果冲突；
- 测量或方法不足；
- 报告不完整；
- 已有证据但转化/实施不足。

“没搜到”不是“从未有人研究”。缺口陈述必须附检索边界和日期。

## 6. 引用核验

分别验证：

1. 记录真实存在且元数据一致；
2. 当前引用版本正确；
3. 原文确实支持附近命题；
4. 语气强度没有超过研究设计；
5. 撤稿、更正和勘误已检查；
6. 二手引用尽量回到原始来源。

无法核验的引文状态为 `UNVERIFIED`，不得进入投稿稿件的关键论证。
