# 研究与科学

检索、综述、引用、实验、统计、科学计算、论文、同行评审与复现。

- 默认可见技能：**806**
- 新手大礼包入选：**9**
- 完整机器索引：[`skills.tsv`](skills.tsv)
- 可迁移离线包：[`科研大礼包 · Research Workflow Kit`](../../bundles/research-workflow-kit/README.md)

## 如何找技能

```bash
python scripts/search_skills.py "literature review citation statistics" --category research-science --limit 12
```

先看搜索元数据，只打开当前任务真正命中的 1 个主技能和至多 3 个互补技能；不要把本分类全部载入上下文。

## 新手大礼包中的代表技能

| 技能 | 层级 | 用途 |
|---|---|---|
| [`research-expert-system`](../../skills/core/research-expert-system/SKILL.md) | maintained | 世界级通用科研能力路由器。用于从选题、文献检索、系统综述、研究设计、实验执行、数据分析、科研绘图、论文写作、引用核验、同行评审、rebuttal、复现归档到学术汇报的完整研究生命周期；根据任务选择 ARS、Nature Skills、Scientific Agent Skills、ARIS、AI Research Skills、PaperSpine、Paper Craft、Hermes 和 Jupyter live kernel，并强制执行人类决策、证据追踪、统计严谨性和研究诚信门禁。 |
| [`citation-management`](../../skills/community/scientific-agent-skills/skills/citation-management/SKILL.md) | community | Comprehensive citation management for academic research. Search OpenAlex, PubMed, and Google Scholar for papers, extract accurate metadata, validate citations, and generate properly formatted BibTeX entries. This skill should be used when you need to find papers, verify citation information, convert DOIs to BibTeX, or ensure reference accuracy in scientific writing. |
| [`citation-verification`](../../skills/community/claude-scholar/skills/citation-verification/SKILL.md) | community | This skill provides reference guidance for citation verification in academic writing. Use when the user asks about "citation verification best practices", "how to verify references", "preventing fake citations", or needs guidance on citation accuracy. This skill supports ml-paper-writing by providing detailed verification principles and common error patterns. |
| [`deep-research`](../../skills/community/ECC/skills/deep-research/SKILL.md) | community | Multi-source deep research using firecrawl and exa MCPs. Searches the web, synthesizes findings, and delivers cited reports with source attribution. Use when the user wants thorough research on any topic with evidence and citations. |
| [`literature-review`](../../skills/community/scientific-agent-skills/skills/literature-review/SKILL.md) | community | Conduct comprehensive, systematic literature reviews using multiple academic databases (PubMed, arXiv, bioRxiv, Semantic Scholar, etc.). This skill should be used when conducting systematic literature reviews, meta-analyses, research synthesis, or comprehensive literature searches across biomedical, scientific, and technical domains. Creates professionally formatted markdown documents and PDFs with verified citations in multiple citation styles (APA, Nature, Vancouver, etc.). |
| [`planning-with-files`](../../skills/community/claude-scholar/skills/planning-with-files/SKILL.md) | community | Use this by default for non-trivial multi-step work that needs persistent planning, progress tracking, or durable notes on disk. Trigger when a task will likely span multiple tool calls, research steps, verification loops, or enough context that the plan should not live only in transient chat memory. |
| [`research-ideation`](../../skills/community/claude-scholar/skills/research-ideation/SKILL.md) | community | This skill should be used when the user asks to "brainstorm research ideas", "use 5W1H framework", "identify research gaps", "conduct gap analysis", "start research project", "conduct literature review", "define research question", "select research method", "plan research", or mentions research project initiation phase. Provides comprehensive guidance for research startup workflow from idea generation to planning. |
| [`research-paper-writing`](../../skills/community/Research-Paper-Writing-Skills-main/research-paper-writing/SKILL.md) | community | Improve academic paper writing quality for ML/CV/NLP-style papers with clear section structure, paragraph flow, and reviewer-facing presentation. Use when drafting or revising Abstract, Introduction, Related Work, Method, Experiments, or Conclusion; polishing figures/tables; checking claim-support alignment; or performing self-review before submission. |
| [`statistical-analysis`](../../skills/community/scientific-agent-skills/skills/statistical-analysis/SKILL.md) | community | Guided statistical analysis for research data - test selection, assumption checking, effect sizes, power analysis, Bayesian alternatives, and APA-formatted reporting. Use whenever a user wants to compare groups, test a hypothesis, analyze experimental or survey data, check statistical assumptions, compute required sample sizes, or write up results - even if they never name a specific test. Covers t-tests, ANOVA, chi-square, correlation, regression, non-parametric and Bayesian methods. For low-level model APIs, see the statsmodels and pymc skills. |

返回[全部分类](../README.md)或查看[新手大礼包](../../bundles/newcomer-starter-pack/README.md)。
