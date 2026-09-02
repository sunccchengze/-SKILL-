# 写作与内容

中文与英文写作、编辑、内容研究、技术表达、营销文案与去模板化。

- 默认可见技能：**88**
- 新手大礼包入选：**15**
- 完整机器索引：[`skills.tsv`](skills.tsv)

## 如何找技能

```bash
python scripts/search_skills.py "writing editing content audience" --category writing-content --limit 12
```

先看搜索元数据，只打开当前任务真正命中的 1 个主技能和至多 3 个互补技能；不要把本分类全部载入上下文。

## 新手大礼包中的代表技能

| 技能 | 层级 | 用途 |
|---|---|---|
| [`human-writing`](../../skills/community/human-writing/SKILL.md) | maintained | 通用中文创作与改稿 Skill。用于知乎回答、论坛长帖、公众号文章、博客、评论、人物故事、历史叙事、新闻与行业解读、科普、教程、评测、个人叙事、小说、故事、对白、口播和演讲稿。默认写成一个见过事、查过材料、愿意把来龙去脉讲清楚的人在说话，重点保留中文互联网长回答与长帖的活人感和自然中文韵律，避免空泛的机构腔、喊口号式演说腔、营销腔和模型腔。非虚构长文先检查材料够不够，材料不足时研究、追问或缩短，绝不用重复解释灌字数。现实内容额外核验事实、引语、数据与用户亲历，虚构内容可以创造人物、场景、对白、心理与情节。成稿正文严禁冒号、破折号、“不是……而是……”及同类翻案句，并清除商业黑话和模型惯用黑话。不创建作者画像、个人规则库或个人写作 Skill。 |
| [`humanizer-zh`](../../skills/core/humanizer-zh/SKILL.md) | maintained | 去除文本中的 AI 生成痕迹。适用于编辑或审阅文本，使其听起来更自然、更像人类书写。 基于维基百科的"AI 写作特征"综合指南。检测并修复以下模式：夸大的象征意义、 宣传性语言、以 -ing 结尾的肤浅分析、模糊的归因、破折号过度使用、三段式法则、 AI 词汇、否定式排比、过多的连接性短语。 |
| [`article-writing`](../../skills/community/ECC/skills/article-writing/SKILL.md) | community | Write articles, guides, blog posts, tutorials, newsletter issues, and other long-form content in a distinctive voice derived from supplied examples or brand guidance. Use when the user wants polished written content longer than a paragraph, especially when voice consistency, structure, and credibility matter. |
| [`content-research-writer`](../../skills/community/buildwithclaude-hub/plugins/all-skills/skills/content-research-writer/SKILL.md) | community | Assists in writing high-quality content by conducting research, adding citations, improving hooks, iterating on outlines, and providing real-time feedback on each section. Transforms your writing process from solo effort to collaborative partnership. |
| [`content-strategy`](../../skills/community/boraoztunc-skills/content-strategy/SKILL.md) | community | When the user wants to plan a content strategy, decide what content to create, or figure out what topics to cover. Also use when the user mentions "content strategy," "what should I write about," "content ideas," "blog strategy," "topic clusters," or "content planning." For writing individual pieces, see copywriting. For SEO-specific audits, see seo-audit. |
| [`copy-editing`](../../skills/community/boraoztunc-skills/copy-editing/SKILL.md) | community | When the user wants to edit, review, or improve existing marketing copy. Also use when the user mentions 'edit this copy,' 'review my copy,' 'copy feedback,' 'proofread,' 'polish this,' 'make this better,' or 'copy sweep.' This skill provides a systematic approach to editing marketing copy through multiple focused passes. |
| [`copywriting`](../../skills/community/boraoztunc-skills/copywriting/SKILL.md) | community | When the user wants to write, rewrite, or improve marketing copy for any page — including homepage, landing pages, pricing pages, feature pages, about pages, or product pages. Also use when the user says "write copy for," "improve this copy," "rewrite this page," "marketing copy," "headline help," or "CTA copy." For email copy, see email-sequence. For popup copy, see popup-cro. |
| [`daily-coding`](../../skills/community/claude-scholar/skills/daily-coding/SKILL.md) | community | Use for everyday coding tasks that involve writing or modifying source code. |
| [`doc-coauthoring`](../../skills/community/skills-main/skills/doc-coauthoring/SKILL.md) | community | Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, technical specs, decision docs, or similar structured content. This workflow helps users efficiently transfer context, refine content through iteration, and verify the doc works for readers. Trigger when user mentions writing docs, creating proposals, drafting specs, or similar documentation tasks. |
| [`markdown-mermaid-writing`](../../skills/community/scientific-agent-skills/skills/markdown-mermaid-writing/SKILL.md) | community | Comprehensive markdown and Mermaid diagram writing skill. Use when creating any scientific document, report, analysis, or visualization. Establishes text-based diagrams as the default documentation standard with full style guides (markdown + mermaid), 24 diagram type references, and 9 document templates. |
| [`scientific-writing`](../../skills/community/scientific-agent-skills/skills/scientific-writing/SKILL.md) | community | Draft, revise, and audit scientific manuscripts or reports with explicit evidence provenance, reporting-guideline coverage, authorship accountability, confidentiality controls, and local consistency checks. Use for manuscript sections, references, declarations, tables, figures, or submission preparation when scientific accuracy and traceability matter. |
| [`user-story`](../../skills/community/alirezarezvani-claude-skills/.gemini/skills/user-story/SKILL.md) | community | Generate user stories with acceptance criteria and sprint planning. Usage: /user-story <generate|sprint> [options] |
| [`writing`](../../skills/community/WRITING.md-main/skills/writing/SKILL.md) | community | Draft, revise, audit, or transform human-facing prose: articles, blogs, documentation, criticism, essays, email, marketing and SEO copy, summaries, scripts, application materials, and UI text. Excludes code comments, commit messages, and private notes. |
| [`writing-anti-ai`](../../skills/community/claude-scholar/skills/writing-anti-ai/SKILL.md) | community | This skill should be used when the user asks to "remove AI writing patterns", "humanize this text", "make this sound more natural", "remove AI-generated traces", "fix robotic writing", or needs to eliminate AI writing patterns from prose. Supports both English and Chinese text. Based on Wikipedia's "Signs of AI writing" guide, detects and fixes inflated symbolism, promotional language, superficial -ing analyses, vague attributions, AI vocabulary, negative parallelisms, and excessive conjunctive phrases. |
| [`writing-plans`](../../skills/community/superpowers-main/skills/writing-plans/SKILL.md) | community | Use when you have a spec or requirements for a multi-step task, before touching code |

返回[全部分类](../README.md)或查看[新手大礼包](../../bundles/newcomer-starter-pack/README.md)。
