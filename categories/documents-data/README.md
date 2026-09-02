# 文档与数据

PDF、结构化文档、表格、数据库、数据清洗、分析与可追踪交付。

- 默认可见技能：**175**
- 新手大礼包入选：**6**
- 完整机器索引：[`skills.tsv`](skills.tsv)

## 如何找技能

```bash
python scripts/search_skills.py "document data spreadsheet database" --category documents-data --limit 12
```

先看搜索元数据，只打开当前任务真正命中的 1 个主技能和至多 3 个互补技能；不要把本分类全部载入上下文。

## 新手大礼包中的代表技能

| 技能 | 层级 | 用途 |
|---|---|---|
| [`convert-documents-to-markdown`](../../skills/community/anydoc-main/skills/convert-documents-to-markdown/SKILL.md) | community | Convert Word (.doc, .docx), PowerPoint (.ppt, .pptx), Excel (.xls, .xlsx), OpenDocument (.odt, .ods, .odp), RTF, EPUB, CSV, and PDF files to GitHub-Flavored Markdown. Use when a task needs the contents of an office document, spreadsheet, presentation, ebook, or PDF you cannot read directly. |
| [`document-generate`](../../skills/community/gstack/document-generate/SKILL.md) | community | Generate missing documentation from scratch for a feature, module, or entire project. (gstack) |
| [`exploratory-data-analysis`](../../skills/community/scientific-agent-skills/skills/exploratory-data-analysis/SKILL.md) | community | Perform bounded, local exploratory analysis of explicitly supported scientific files. Use for redacted CSV/TSV/JSON profiles; optional NumPy, HDF5, FASTA/FASTQ, and basic image metadata inspection; missingness/leakage audits; outlier and transformation sensitivity; and rigorous EDA report scaffolds. Other domain formats are reference-only and unknown formats fail closed. |
| [`make-pdf`](../../skills/community/gstack/make-pdf/SKILL.md) | community | Turn any markdown file into a publication-quality PDF. (gstack) |
| [`performance-optimization`](../../skills/community/agent-skills-main/skills/performance-optimization/SKILL.md) | community | Optimizes application performance across frontend, backend, queries, and databases. Use when performance requirements exist, when you suspect performance regressions, when Core Web Vitals or load times need improvement, when N+1 query patterns need fixing, or when profiling reveals bottlenecks. |
| [`sql-database-assistant`](../../skills/community/alirezarezvani-claude-skills/engineering/skills/sql-database-assistant/SKILL.md) | community | Use when the user asks to write SQL queries, optimize database performance, generate migrations, explore database schemas, or work with ORMs like Prisma, Drizzle, TypeORM, or SQLAlchemy. |

返回[全部分类](../README.md)或查看[新手大礼包](../../bundles/newcomer-starter-pack/README.md)。
