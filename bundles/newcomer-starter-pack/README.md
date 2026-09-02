# 🎁 Agent 新手大礼包：100 项核心工作技能

这是一个可以直接解压、离线阅读的基础组合。它收录 **恰好 100 项**本仓库本地可用的核心技能，覆盖技能发现、计划、实现、测试、研究、写作、设计、安全、产品与交付验证。机器清单见 [`manifest.json`](manifest.json)，可下载包为 [`newcomer-starter-pack.tar.gz`](newcomer-starter-pack.tar.gz)。

> **强烈建议：频繁检索、明确点名、完整应用。** 对每项非琐碎任务，都应主动寻找匹配技能，并在工作记录中明确写出本轮调用了哪些技能、分别用在哪一步、如何按其完整流程执行、取得了什么验证证据。不要只说“参考过”，也不要只列名字而不落实。

> **但不要一次吞下 100 项。** “完整应用”指完整执行**本轮选中技能**的关键步骤，不是把全部技能同时塞进上下文。通常使用 1 个主技能，并按需增加研究、制作、审查各 1 个，合计通常不超过 4 个。需要换阶段时再重新搜索和换组。

## 解压与使用

```bash
tar -xzf bundles/newcomer-starter-pack/newcomer-starter-pack.tar.gz
cd newcomer-starter-pack
less START_HERE.md
```

解压目录中的 `skills/` 是 100 个独立包；`MANIFEST.json` 记录顺序、分类、来源路径、描述和 SHA-256，`LICENSE_AND_ATTRIBUTION.md` 与 `THIRD_PARTY_NOTICE.md` 说明许可核验边界。把该目录配置为 Agent 的技能搜索目录，或只复制当前任务需要的包。

## 新会话必须先做的吸收报告

把以下要求原样交给新会话中的工作者：

```text
请先阅读 START_HERE.md 与 MANIFEST.json，只扫描 100 项技能的元数据，不要一次加载全部正文。
在开始实质工作前，请提交“技能吸收与调用报告”，必须回答：
1. 你如何消化/吸收了现有技能：看了哪些入口和元数据，如何结合当前项目筛选，完整阅读了哪些 SKILL.md；
2. 本轮你将明确调用哪些技能：逐项写出准确技能名、选择原因、负责阶段和预期制品；
3. 后续你将如何完整应用：逐项列出会落实的关键步骤、质量门禁、验证命令/证据与失败回退；
4. 哪些候选技能本轮不调用，以及为什么不需要，避免为了显得勤奋而堆叠上下文。
后续每次任务阶段变化时重新检索；交付时报告实际调用结果，而不是只重复计划。
```

推荐报告格式：

```markdown
## 技能吸收与调用报告
- 元数据吸收：已扫描 100/100；当前任务关键词：……
- 完整阅读：`主技能`、`互补技能 A`、`互补技能 B`（仅列实际打开的正文）
- 明确调用：
  - `技能名` → 负责阶段 / 选择依据 / 预期制品
- 完整应用计划：
  - `技能名` → 关键步骤 / 质量门禁 / 验证证据 / 失败回退
- 本轮未调用：候选技能及不调用原因
- 交付回报：实际执行、验证结果、偏差与剩余风险
```

## 正确的高频使用节奏

1. **任务进入时**：写清领域、交付物、方法与风险，先搜索再开工。
2. **阶段切换时**：从研究转制作、从实现转审查时重新检索，明确换组。
3. **执行过程中**：按选中 `SKILL.md` 的关键步骤产出制品，不跳过不方便的门禁。
4. **遇到失败时**：调用调试、评审或风险技能，记录证据，不反复盲试。
5. **交付之前**：调用验证技能，用真实命令、页面、数据或引用证明完成。
6. **交付之后**：报告实际用了什么、没验证什么、下一会话应继续调用什么。

## 精确收录清单（100/100）

### Agent 基础与编排（15）

| # | 技能 | 分类 | 核心用途 |
|---:|---|---|---|
| 1 | [`universal-skill-router`](../../SKILL.md) | agents-orchestration | 面向任意项目的技能检索、领域适配和最小专家组编排入口。用于在大型技能仓库中根据真实任务选择少量互补技能，建立制品契约与验证门禁，避免把历史项目假设带入新方向。 |
| 2 | [`using-agent-skills`](../../skills/community/agent-skills-main/skills/using-agent-skills/SKILL.md) | agents-orchestration | Discovers and invokes agent skills. Use when starting a session or when you need to discover which skill applies to the current task. This is the meta-skill that governs how all o… |
| 3 | [`planning-and-task-breakdown`](../../skills/community/agent-skills-main/skills/planning-and-task-breakdown/SKILL.md) | agents-orchestration | Breaks work into ordered tasks. Use when you have a spec or clear requirements and need to break work into implementable tasks. Use when a task feels too large to start, when you… |
| 4 | [`brainstorming`](../../skills/community/superpowers-main/skills/brainstorming/SKILL.md) | design-media | You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design bef… |
| 5 | [`writing-plans`](../../skills/community/superpowers-main/skills/writing-plans/SKILL.md) | writing-content | Use when you have a spec or requirements for a multi-step task, before touching code |
| 6 | [`executing-plans`](../../skills/community/superpowers-main/skills/executing-plans/SKILL.md) | general | Use when you have a written implementation plan to execute in a separate session with review checkpoints |
| 7 | [`verification-before-completion`](../../skills/community/superpowers-main/skills/verification-before-completion/SKILL.md) | general | Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any suc… |
| 8 | [`multi-agent-orchestration`](../../skills/core/multi-agent-orchestration/SKILL.md) | agents-orchestration | 为确实可并行、需要上下文隔离或独立红队的复杂任务设计最小多 Agent 团队，定义职责、文件边界、制品契约、合并顺序和验证门禁。 |
| 9 | [`dispatching-parallel-agents`](../../skills/community/superpowers-main/skills/dispatching-parallel-agents/SKILL.md) | agents-orchestration | Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies |
| 10 | [`subagent-driven-development`](../../skills/community/superpowers-main/skills/subagent-driven-development/SKILL.md) | agents-orchestration | Use when executing implementation plans with independent tasks in the current session |
| 11 | [`ai-cabinet-decision-making`](../../skills/core/ai-cabinet/SKILL.md) | business-strategy | 用五个独立席位对重要决策、方案比较、路线选择和高不确定性计划进行第一性原理追问、红队攻击、机会分析、外行清晰度审查与执行拆解，再由主席给出有条件建议。 |
| 12 | [`spec-driven-development`](../../skills/community/agent-skills-main/skills/spec-driven-development/SKILL.md) | agents-orchestration | Creates specs before coding. Use when starting a new project, feature, or significant change and no specification exists yet. Use when requirements are unclear, ambiguous, or only… |
| 13 | [`search-first`](../../skills/community/ECC/skills/search-first/SKILL.md) | agents-orchestration | Research-before-coding workflow. Search for existing tools, libraries, and patterns before writing custom code. Invokes the researcher agent. |
| 14 | [`official-source-router`](../../skills/official-source-router/SKILL.md) | agents-orchestration | Route product- and platform-specific work across 859 pinned skill entry paths from OpenAI, Vercel, and Microsoft official repositories. Use when selecting a first-party workflow,… |
| 15 | [`skill-creator`](../../skills/community/skills-main/skills/skill-creator/SKILL.md) | engineering-code | Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run… |

### 工程与代码（20）

| # | 技能 | 分类 | 核心用途 |
|---:|---|---|---|
| 16 | [`daily-coding`](../../skills/community/claude-scholar/skills/daily-coding/SKILL.md) | writing-content | Use for everyday coding tasks that involve writing or modifying source code. |
| 17 | [`tdd-guide`](../../skills/community/alirezarezvani-claude-skills/engineering-team/skills/tdd-guide/SKILL.md) | engineering-code | Test-driven development skill for writing unit tests, generating test fixtures and mocks, analyzing coverage gaps, and guiding red-green-refactor workflows across Jest, Pytest, JU… |
| 18 | [`testing`](../../skills/community/buildwithclaude-hub/plugins/cc-best/skills/testing/SKILL.md) | engineering-code | Testing strategies and methodologies including TDD, E2E testing, and multi-framework support |
| 19 | [`systematic-debugging`](../../skills/community/superpowers-main/skills/systematic-debugging/SKILL.md) | engineering-code | Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes |
| 20 | [`browser-testing-with-devtools`](../../skills/community/agent-skills-main/skills/browser-testing-with-devtools/SKILL.md) | engineering-code | Tests in real browsers via Chrome DevTools MCP. Use when building or debugging anything that runs in a browser. Use when you need to inspect the DOM, capture console errors, analy… |
| 21 | [`code-review-excellence`](../../skills/community/claude-scholar/skills/code-review-excellence/SKILL.md) | engineering-code | This skill should be used when the user asks to review a diff or pull request, write review comments, audit code quality, establish review standards, or improve how a team perform… |
| 22 | [`requesting-code-review`](../../skills/community/superpowers-main/skills/requesting-code-review/SKILL.md) | engineering-code | Use when completing tasks, implementing major features, or before merging to verify work meets requirements |
| 23 | [`receiving-code-review`](../../skills/community/superpowers-main/skills/receiving-code-review/SKILL.md) | engineering-code | Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear or technically questionable - requires technical rigor and verificat… |
| 24 | [`code-simplification`](../../skills/community/agent-skills-main/skills/code-simplification/SKILL.md) | engineering-code | Simplifies code for clarity. Use when refactoring code for clarity without changing behavior. Use when code works but is harder to read, maintain, or extend than it should be. Use… |
| 25 | [`coding-standards`](../../skills/community/ECC/skills/coding-standards/SKILL.md) | engineering-code | Baseline cross-project coding conventions for naming, readability, immutability, and code-quality review. Use detailed frontend or backend skills for framework-specific patterns. |
| 26 | [`using-git-worktrees`](../../skills/community/superpowers-main/skills/using-git-worktrees/SKILL.md) | engineering-code | Use when starting feature work that needs isolation from current workspace or before executing implementation plans - ensures an isolated workspace exists via native tools or git… |
| 27 | [`git-workflow-and-versioning`](../../skills/community/agent-skills-main/skills/git-workflow-and-versioning/SKILL.md) | engineering-code | Structures git workflow practices. Use when making any code change. Use when committing, branching, resolving conflicts, or when you need to organize work across multiple parallel… |
| 28 | [`github-automation`](../../skills/community/buildwithclaude-hub/plugins/all-skills/skills/github-automation/SKILL.md) | engineering-code | Automate GitHub repositories, issues, pull requests, branches, CI/CD, and permissions via Rube MCP (Composio). Manage code workflows, review PRs, search code, and handle deploymen… |
| 29 | [`ci-cd-pipeline-builder`](../../skills/community/alirezarezvani-claude-skills/engineering/skills/ci-cd-pipeline-builder/SKILL.md) | engineering-code | Generate pragmatic CI/CD pipelines from detected project stack signals — fast baseline generation, repeatable checks, environment-aware deployment stages. Use when setting up CI f… |
| 30 | [`docker-patterns`](../../skills/community/ECC/skills/docker-patterns/SKILL.md) | agents-orchestration | Docker and Docker Compose patterns for local development, hardened CLI installer harnesses, container security, networking, volumes, and multi-service orchestration. Use when crea… |
| 31 | [`api-and-interface-design`](../../skills/community/agent-skills-main/skills/api-and-interface-design/SKILL.md) | engineering-code | Guides stable API and interface design. Use when designing APIs, module boundaries, or any public interface. Use when creating REST or GraphQL endpoints, defining type contracts b… |
| 32 | [`frontend-patterns`](../../skills/community/ECC/skills/frontend-patterns/SKILL.md) | engineering-code | Frontend development patterns for React, Next.js, state management, performance optimization, and UI best practices. |
| 33 | [`backend-patterns`](../../skills/community/ECC/skills/backend-patterns/SKILL.md) | engineering-code | Backend architecture patterns, API design, database optimization, and server-side best practices for Node.js, Express, and Next.js API routes. |
| 34 | [`python-patterns`](../../skills/community/ECC/skills/python-patterns/SKILL.md) | engineering-code | Pythonic idioms, PEP 8 standards, type hints, and best practices for building robust, efficient, and maintainable Python applications. |
| 35 | [`performance-optimization`](../../skills/community/agent-skills-main/skills/performance-optimization/SKILL.md) | documents-data | Optimizes application performance across frontend, backend, queries, and databases. Use when performance requirements exist, when you suspect performance regressions, when Core We… |

### 文档与数据（8）

| # | 技能 | 分类 | 核心用途 |
|---:|---|---|---|
| 36 | [`doc-coauthoring`](../../skills/community/skills-main/skills/doc-coauthoring/SKILL.md) | writing-content | Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, technical specs, decision docs, or similar structu… |
| 37 | [`make-pdf`](../../skills/community/gstack/make-pdf/SKILL.md) | documents-data | Turn any markdown file into a publication-quality PDF. (gstack) |
| 38 | [`document-generate`](../../skills/community/gstack/document-generate/SKILL.md) | documents-data | Generate missing documentation from scratch for a feature, module, or entire project. (gstack) |
| 39 | [`convert-documents-to-markdown`](../../skills/community/anydoc-main/skills/convert-documents-to-markdown/SKILL.md) | documents-data | Convert Word (.doc, .docx), PowerPoint (.ppt, .pptx), Excel (.xls, .xlsx), OpenDocument (.odt, .ods, .odp), RTF, EPUB, CSV, and PDF files to GitHub-Flavored Markdown. Use when a t… |
| 40 | [`markdown-mermaid-writing`](../../skills/community/scientific-agent-skills/skills/markdown-mermaid-writing/SKILL.md) | writing-content | Comprehensive markdown and Mermaid diagram writing skill. Use when creating any scientific document, report, analysis, or visualization. Establishes text-based diagrams as the def… |
| 41 | [`slides`](../../skills/community/ui-ux-pro-max/cli/assets/skills/slides/SKILL.md) | design-media | Create strategic HTML presentations with Chart.js, design tokens, responsive layouts, copywriting formulas, and contextual slide strategies. |
| 42 | [`exploratory-data-analysis`](../../skills/community/scientific-agent-skills/skills/exploratory-data-analysis/SKILL.md) | documents-data | Perform bounded, local exploratory analysis of explicitly supported scientific files. Use for redacted CSV/TSV/JSON profiles; optional NumPy, HDF5, FASTA/FASTQ, and basic image me… |
| 43 | [`sql-database-assistant`](../../skills/community/alirezarezvani-claude-skills/engineering/skills/sql-database-assistant/SKILL.md) | documents-data | Use when the user asks to write SQL queries, optimize database performance, generate migrations, explore database schemas, or work with ORMs like Prisma, Drizzle, TypeORM, or SQLA… |

### 研究与科学（10）

| # | 技能 | 分类 | 核心用途 |
|---:|---|---|---|
| 44 | [`research-expert-system`](../../skills/research-expert-system/SKILL.md) | research-science | 世界级通用科研能力路由器。用于从选题、文献检索、系统综述、研究设计、实验执行、数据分析、科研绘图、论文写作、引用核验、同行评审、rebuttal、复现归档到学术汇报的完整研究生命周期；根据任务选择 ARS、Nature Skills、Scientific Agent Skills、ARIS、AI Research Skills、PaperSpine、Pap… |
| 45 | [`research-ideation`](../../skills/community/claude-scholar/skills/research-ideation/SKILL.md) | research-science | This skill should be used when the user asks to "brainstorm research ideas", "use 5W1H framework", "identify research gaps", "conduct gap analysis", "start research project", "con… |
| 46 | [`deep-research`](../../skills/community/ECC/skills/deep-research/SKILL.md) | research-science | Multi-source deep research using firecrawl and exa MCPs. Searches the web, synthesizes findings, and delivers cited reports with source attribution. Use when the user wants thorou… |
| 47 | [`literature-review`](../../skills/community/scientific-agent-skills/skills/literature-review/SKILL.md) | research-science | Conduct comprehensive, systematic literature reviews using multiple academic databases (PubMed, arXiv, bioRxiv, Semantic Scholar, etc.). This skill should be used when conducting… |
| 48 | [`citation-management`](../../skills/community/scientific-agent-skills/skills/citation-management/SKILL.md) | research-science | Comprehensive citation management for academic research. Search OpenAlex, PubMed, and Google Scholar for papers, extract accurate metadata, validate citations, and generate proper… |
| 49 | [`citation-verification`](../../skills/community/claude-scholar/skills/citation-verification/SKILL.md) | research-science | This skill provides reference guidance for citation verification in academic writing. Use when the user asks about "citation verification best practices", "how to verify reference… |
| 50 | [`scientific-writing`](../../skills/community/scientific-agent-skills/skills/scientific-writing/SKILL.md) | writing-content | Draft, revise, and audit scientific manuscripts or reports with explicit evidence provenance, reporting-guideline coverage, authorship accountability, confidentiality controls, an… |
| 51 | [`statistical-analysis`](../../skills/community/scientific-agent-skills/skills/statistical-analysis/SKILL.md) | research-science | Guided statistical analysis for research data - test selection, assumption checking, effect sizes, power analysis, Bayesian alternatives, and APA-formatted reporting. Use whenever… |
| 52 | [`experimental-design`](../../skills/community/scientific-agent-skills/skills/experimental-design/SKILL.md) | design-media | Design experiments and studies BEFORE data is collected — choosing a design, randomizing, blocking, and laying out treatment combinations so results are interpretable. Use wheneve… |
| 53 | [`research-paper-writing`](../../skills/community/Research-Paper-Writing-Skills-main/research-paper-writing/SKILL.md) | research-science | Improve academic paper writing quality for ML/CV/NLP-style papers with clear section structure, paragraph flow, and reviewer-facing presentation. Use when drafting or revising Abs… |

### 写作与内容（10）

| # | 技能 | 分类 | 核心用途 |
|---:|---|---|---|
| 54 | [`human-writing`](../../skills/community/human-writing/SKILL.md) | writing-content | 通用中文创作与改稿 Skill。用于知乎回答、论坛长帖、公众号文章、博客、评论、人物故事、历史叙事、新闻与行业解读、科普、教程、评测、个人叙事、小说、故事、对白、口播和演讲稿。默认写成一个见过事、查过材料、愿意把来龙去脉讲清楚的人在说话，重点保留中文互联网长回答与长帖的活人感和自然中文韵律，避免空泛的机构腔、喊口号式演说腔、营销腔和模型腔。非虚构长文先检查… |
| 55 | [`humanizer-zh`](../../skills/humanizer-zh/SKILL.md) | writing-content | 去除文本中的 AI 生成痕迹。适用于编辑或审阅文本，使其听起来更自然、更像人类书写。 基于维基百科的"AI 写作特征"综合指南。检测并修复以下模式：夸大的象征意义、 宣传性语言、以 -ing 结尾的肤浅分析、模糊的归因、破折号过度使用、三段式法则、 AI 词汇、否定式排比、过多的连接性短语。 |
| 56 | [`stop-slop`](../../skills/stop-slop/SKILL.md) | general | 起草、编辑或审阅散文时识别并删除常见 AI 模板腔，包括空泛开场、公式结构、虚假深度、模糊归因、节奏单一、过度修辞和可删内容，同时保留事实、含义与目标语气。 |
| 57 | [`copywriting`](../../skills/community/boraoztunc-skills/copywriting/SKILL.md) | writing-content | When the user wants to write, rewrite, or improve marketing copy for any page — including homepage, landing pages, pricing pages, feature pages, about pages, or product pages. Als… |
| 58 | [`copy-editing`](../../skills/community/boraoztunc-skills/copy-editing/SKILL.md) | writing-content | When the user wants to edit, review, or improve existing marketing copy. Also use when the user mentions 'edit this copy,' 'review my copy,' 'copy feedback,' 'proofread,' 'polish… |
| 59 | [`content-research-writer`](../../skills/community/buildwithclaude-hub/plugins/all-skills/skills/content-research-writer/SKILL.md) | writing-content | Assists in writing high-quality content by conducting research, adding citations, improving hooks, iterating on outlines, and providing real-time feedback on each section. Transfo… |
| 60 | [`article-writing`](../../skills/community/ECC/skills/article-writing/SKILL.md) | writing-content | Write articles, guides, blog posts, tutorials, newsletter issues, and other long-form content in a distinctive voice derived from supplied examples or brand guidance. Use when the… |
| 61 | [`writing`](../../skills/community/WRITING.md-main/skills/writing/SKILL.md) | writing-content | Draft, revise, audit, or transform human-facing prose: articles, blogs, documentation, criticism, essays, email, marketing and SEO copy, summaries, scripts, application materials,… |
| 62 | [`writing-anti-ai`](../../skills/community/claude-scholar/skills/writing-anti-ai/SKILL.md) | writing-content | This skill should be used when the user asks to "remove AI writing patterns", "humanize this text", "make this sound more natural", "remove AI-generated traces", "fix robotic writ… |
| 63 | [`content-strategy`](../../skills/community/boraoztunc-skills/content-strategy/SKILL.md) | writing-content | When the user wants to plan a content strategy, decide what content to create, or figure out what topics to cover. Also use when the user mentions "content strategy," "what should… |

### 设计与媒体（10）

| # | 技能 | 分类 | 核心用途 |
|---:|---|---|---|
| 64 | [`victor-design-system`](../../skills/community/victor-design/SKILL.md) | design-media | 证据驱动的跨载体视觉设计与交付系统。用于海报、图文/社交内容、PPT/演示和产品 UI：理解主题与情绪，学习优秀人工参考，选择有依据且足够丰富的设计手法，制作 HTML 母版并完成可编辑交付与审查。 |
| 65 | [`frontend-design`](../../skills/community/skills-main/skills/frontend-design/SKILL.md) | design-media | Guidance for distinctive, intentional visual design when building new UI or reshaping an existing one. Helps with aesthetic direction, typography, and making choices that don't re… |
| 66 | [`web-design-guidelines`](../../skills/community/boraoztunc-skills/web-design-guidelines/SKILL.md) | design-media | Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility", "audit design", "review UX", or "check my site against best practi… |
| 67 | [`accessibility`](../../skills/community/ECC/skills/accessibility/SKILL.md) | security-compliance | Design, implement, and audit inclusive digital products using WCAG 2.2 Level AA |
| 68 | [`ui-ux-pro-max`](../../skills/community/claude-scholar/skills/ui-ux-pro-max/SKILL.md) | design-media | This skill should be used when the user asks to design or review a UI, create a landing page or dashboard, choose colors or typography, improve accessibility, or implement polishe… |
| 69 | [`canvas-design`](../../skills/community/skills-main/skills/canvas-design/SKILL.md) | design-media | Create beautiful visual art in .png and .pdf documents using design philosophy. You should use this skill when the user asks to create a poster, piece of art, design, or other sta… |
| 70 | [`design-system`](../../skills/community/ECC/skills/design-system/SKILL.md) | design-media | Use this skill to generate or audit design systems, check visual consistency, and review PRs that touch styling. |
| 71 | [`generate-image`](../../skills/community/scientific-agent-skills/skills/generate-image/SKILL.md) | design-media | Generate or edit images with AI models through the OpenRouter Image API (Gemini, Seedream, Recraft, GPT-Image, Riverflow). Use for photos, illustrations, artwork, concept art, vis… |
| 72 | [`design-review`](../../skills/community/gstack/design-review/SKILL.md) | design-media | Designer's eye QA: finds visual inconsistency, spacing issues, hierarchy problems, AI slop patterns, and slow interactions — then fixes them. (gstack) |
| 73 | [`anti-ui-slop`](../../skills/community/buildwithclaude-hub/plugins/all-skills/skills/anti-ui-slop/SKILL.md) | design-media | Stop coding agents from shipping generic UI. Use UIZZE's 800,000+ real web and iOS screens to build product-specific interfaces, define a design contract, cover required states, a… |

### 安全与合规（8）

| # | 技能 | 分类 | 核心用途 |
|---:|---|---|---|
| 74 | [`security-review`](../../skills/community/ECC/skills/security-review/SKILL.md) | security-compliance | Use this skill when adding authentication, handling user input, working with secrets, creating API endpoints, or implementing payment/sensitive features. Provides comprehensive se… |
| 75 | [`security-and-hardening`](../../skills/community/agent-skills-main/skills/security-and-hardening/SKILL.md) | security-compliance | Hardens code against vulnerabilities. Use when handling user input, authentication, data storage, or external integrations. Use when building any feature that accepts untrusted da… |
| 76 | [`security-audit`](../../skills/community/buildwithclaude-hub/plugins/agent-triforce/skills/security-audit/SKILL.md) | security-compliance | Deep security audit covering OWASP Top 10, authentication, authorization, data protection, dependency vulnerabilities, and secrets scanning. Delegates to the Centinela (QA) agent. |
| 77 | [`security-guidance`](../../skills/community/alirezarezvani-claude-skills/engineering/security-guidance/skills/security-guidance/SKILL.md) | engineering-code | PreToolUse security-anti-pattern hook for Claude Code. Catches 12 common security risks (command injection, XSS, SQL injection, unsafe deserialization, GitHub Actions workflow inj… |
| 78 | [`skill-security-auditor`](../../skills/community/alirezarezvani-claude-skills/engineering/skills/skill-security-auditor/SKILL.md) | engineering-code | Security audit and vulnerability scanner for AI agent skills before installation. Use when: (1) evaluating a skill from an untrusted source, (2) auditing a skill directory or git… |
| 79 | [`ai-security`](../../skills/community/alirezarezvani-claude-skills/engineering-team/skills/ai-security/SKILL.md) | security-compliance | Use when assessing AI/ML systems for prompt injection, jailbreak vulnerabilities, model inversion risk, data poisoning exposure, or agent tool abuse. Covers MITRE ATLAS technique… |
| 80 | [`dependency-auditor`](../../skills/community/alirezarezvani-claude-skills/engineering/skills/dependency-auditor/SKILL.md) | security-compliance | Audit and manage dependencies across multi-language projects. Identifies vulnerabilities, license conflicts, transitive dependency risks, and safe-upgrade paths. Use when auditing… |
| 81 | [`incident-response`](../../skills/community/alirezarezvani-claude-skills/engineering-team/skills/incident-response/SKILL.md) | security-compliance | Use when a security incident has been detected or declared and needs classification, triage, escalation path determination, and forensic evidence collection. Covers SEV1-SEV4 clas… |

### 商业与协作（12）

| # | 技能 | 分类 | 核心用途 |
|---:|---|---|---|
| 82 | [`product-manager`](../../skills/community/alirezarezvani-claude-skills/.gemini/skills/product-manager/SKILL.md) | business-strategy | Ships outcomes, not features. Writes specs engineers actually read. Prioritizes ruthlessly. Kills darlings when the data says so. Operates at the intersection of user needs, busin… |
| 83 | [`product-discovery`](../../skills/community/alirezarezvani-claude-skills/product-team/skills/product-discovery/SKILL.md) | business-strategy | Use when validating product opportunities, mapping assumptions, planning discovery sprints, or testing problem-solution fit before committing delivery resources. |
| 84 | [`user-story`](../../skills/community/alirezarezvani-claude-skills/.gemini/skills/user-story/SKILL.md) | writing-content | Generate user stories with acceptance criteria and sprint planning. Usage: /user-story <generate\|sprint> [options] |
| 85 | [`sprint-plan`](../../skills/community/alirezarezvani-claude-skills/.gemini/skills/sprint-plan/SKILL.md) | general | Capacity-gated sprint planning — runs capacity math, carry-over check, and a definition-of-ready gate before committing scope. Usage: /sprint-plan <goal> [capacity] |
| 86 | [`marketing-campaign`](../../skills/community/ECC/skills/marketing-campaign/SKILL.md) | business-strategy | End-to-end marketing campaign planning and execution. Covers audience research, positioning, campaign angle definition, landing page copy, email sequences, social posts, ad copy,… |
| 87 | [`competitive-intel`](../../skills/community/alirezarezvani-claude-skills/c-level-advisor/skills/competitive-intel/SKILL.md) | business-strategy | Systematic competitor tracking that feeds CMO positioning, CRO battlecards, and CPO roadmap decisions. Use when analyzing competitors, building sales battlecards, tracking market… |
| 88 | [`market-research`](../../skills/community/ECC/skills/market-research/SKILL.md) | business-strategy | Conduct market research, competitive analysis, investor due diligence, and industry intelligence with source attribution and decision-oriented summaries. Use when the user wants m… |
| 89 | [`launch-strategy`](../../skills/community/alirezarezvani-claude-skills/marketing-skill/skills/launch-strategy/SKILL.md) | business-strategy | When the user wants to plan a product launch, feature announcement, or release strategy. Also use when the user mentions 'launch,' 'Product Hunt,' 'feature release,' 'announcement… |
| 90 | [`pricing-strategy`](../../skills/community/alirezarezvani-claude-skills/marketing-skill/skills/pricing-strategy/SKILL.md) | business-strategy | Design, optimize, and communicate SaaS pricing — tier structure, value metrics, pricing pages, and price increase strategy. Use when building a pricing model from scratch, redesig… |
| 91 | [`product-analytics`](../../skills/community/alirezarezvani-claude-skills/product-team/skills/product-analytics/SKILL.md) | business-strategy | Use when defining product KPIs, building metric dashboards, running cohort or retention analysis, or interpreting feature adoption trends across product stages. |
| 92 | [`marketing-strategy-pmm`](../../skills/community/alirezarezvani-claude-skills/marketing-skill/skills/marketing-strategy-pmm/SKILL.md) | business-strategy | Product marketing skill for positioning, GTM strategy, competitive intelligence, and product launches. Use when the user asks about product positioning, go-to-market planning, com… |
| 93 | [`meetings`](../../skills/community/alirezarezvani-claude-skills/productivity/meetings/skills/meetings/SKILL.md) | business-strategy | Use when someone wants to decide whether a meeting is worth calling, price a meeting in dollars, build a timeboxed agenda with desired outcomes, or turn messy meeting notes into o… |

### 通用工具与项目卫生（7）

| # | 技能 | 分类 | 核心用途 |
|---:|---|---|---|
| 94 | [`spec-kit`](../../tools/spec-kit/SKILL.md) | engineering-code | Apply GitHub Spec Kit's pinned specification-driven workflow to define principles, requirements, plans, tasks, implementation, and convergence checks. Use when starting or restruc… |
| 95 | [`openwiki`](../../skills/openwiki/SKILL.md) | engineering-code | 使用仓库内固定版本的 LangChain OpenWiki CLI，为代码库生成和持续维护面向 Agent 的 Markdown Wiki、AGENTS/CLAUDE 入口、Mermaid 图与 OKF 文档。适用于代码库理解、架构文档、持续文档更新和 CI 文档任务。 |
| 96 | [`project-health`](../../skills/community/alirezarezvani-claude-skills/.gemini/skills/project-health/SKILL.md) | general | Portfolio health dashboard and risk matrix analysis. Usage: /project-health <dashboard\|risk> [options] |
| 97 | [`architecture-decision-records`](../../skills/community/ECC/skills/architecture-decision-records/SKILL.md) | engineering-code | Capture architectural decisions made during Claude Code sessions as structured ADRs. Auto-detects decision moments, records context, alternatives considered, and rationale. Mainta… |
| 98 | [`codebase-onboarding`](../../skills/community/ECC/skills/codebase-onboarding/SKILL.md) | engineering-code | Analyze an unfamiliar codebase and generate a structured onboarding guide with architecture map, key entry points, conventions, and a starter CLAUDE.md. Use when joining a new pro… |
| 99 | [`websearch`](../../skills/community/prime-agent/packages/coding-agent/skills/websearch/SKILL.md) | agents-orchestration | Search Google via the Serper API. Configure access via /login, then MCP Connections, then Serper (web search). Takes one query and returns titles, URLs, snippets, and knowledge-gr… |
| 100 | [`planning-with-files`](../../skills/community/claude-scholar/skills/planning-with-files/SKILL.md) | research-science | Use this by default for non-trivial multi-step work that needs persistent planning, progress tracking, or durable notes on disk. Trigger when a task will likely span multiple tool… |

## 选择与许可说明

- 这 100 项全部来自已编目的本地紧凑层；包可在不初始化大型子模块的情况下阅读。
- 清单是跨领域基础款，不代表所有项目都需要全部能力，也不替代目标项目自己的指令、事实和验收标准。
- 每个技能仍受其上游许可证和使用边界约束；本包保留 canonical 路径、来源和哈希，不改变上游权利声明。
- 安全、远控、凭据、网络、写入、个人数据、引用和高风险决策必须单独取得授权并执行相应门禁。

礼包版本：`2026.08.15`；生成日期：`2026-08-15`。
