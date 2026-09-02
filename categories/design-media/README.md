# 设计与媒体

产品/UI/UX、视觉系统、网页、演示、图像、视频、动效与媒体生产。

- 默认可见技能：**308**
- 新手大礼包入选：**12**
- 完整机器索引：[`skills.tsv`](skills.tsv)

## 如何找技能

```bash
python scripts/search_skills.py "design ui ux visual media" --category design-media --limit 12
```

先看搜索元数据，只打开当前任务真正命中的 1 个主技能和至多 3 个互补技能；不要把本分类全部载入上下文。

## 新手大礼包中的代表技能

| 技能 | 层级 | 用途 |
|---|---|---|
| [`victor-design-system`](../../skills/community/victor-design/SKILL.md) | maintained | 证据驱动的跨载体视觉设计与交付系统。用于海报、图文/社交内容、PPT/演示和产品 UI：理解主题与情绪，学习优秀人工参考，选择有依据且足够丰富的设计手法，制作 HTML 母版并完成可编辑交付与审查。 |
| [`anti-ui-slop`](../../skills/community/buildwithclaude-hub/plugins/all-skills/skills/anti-ui-slop/SKILL.md) | community | Stop coding agents from shipping generic UI. Use UIZZE's 800,000+ real web and iOS screens to build product-specific interfaces, define a design contract, cover required states, and run a hard finish gate. Use for web or iOS UI design, implementation, redesign, critique, and pre-ship review in Codex, Claude Code, Cursor, Copilot, and other coding agents. |
| [`brainstorming`](../../skills/community/superpowers-main/skills/brainstorming/SKILL.md) | community | You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation. |
| [`canvas-design`](../../skills/community/skills-main/skills/canvas-design/SKILL.md) | community | Create beautiful visual art in .png and .pdf documents using design philosophy. You should use this skill when the user asks to create a poster, piece of art, design, or other static piece. Create original visual designs, never copying existing artists' work to avoid copyright violations. |
| [`design-review`](../../skills/community/gstack/design-review/SKILL.md) | community | Designer's eye QA: finds visual inconsistency, spacing issues, hierarchy problems, AI slop patterns, and slow interactions — then fixes them. (gstack) |
| [`design-system`](../../skills/community/ECC/skills/design-system/SKILL.md) | community | Use this skill to generate or audit design systems, check visual consistency, and review PRs that touch styling. |
| [`experimental-design`](../../skills/community/scientific-agent-skills/skills/experimental-design/SKILL.md) | community | Design experiments and studies BEFORE data is collected — choosing a design, randomizing, blocking, and laying out treatment combinations so results are interpretable. Use whenever someone is planning a study, asks how to assign subjects/samples to groups, mentions randomization, blocking, stratification, controls, factorial or fractional-factorial designs, design of experiments (DOE), screening many factors, response-surface optimization, crossover or repeated-measures or split-plot designs, cluster/group randomization, Latin squares, plate layouts, batch/run-order effects, replication vs. pseudoreplication, or sequential/adaptive/group-sequential designs. Trigger even for informal phrasings like "how should I set up this experiment", "how do I avoid confounding", "what's the best way to test these 6 factors", or "assign these mice to conditions". For computing the sample size or power once the design is chosen, use statistical-power; for analyzing data already collected, use statistical-analysis. |
| [`frontend-design`](../../skills/community/skills-main/skills/frontend-design/SKILL.md) | community | Guidance for distinctive, intentional visual design when building new UI or reshaping an existing one. Helps with aesthetic direction, typography, and making choices that don't read as templated defaults. |
| [`generate-image`](../../skills/community/scientific-agent-skills/skills/generate-image/SKILL.md) | community | Generate or edit images with AI models through the OpenRouter Image API (Gemini, Seedream, Recraft, GPT-Image, Riverflow). Use for photos, illustrations, artwork, concept art, visual assets, logos, and image editing or compositing from reference images. For flowcharts, circuits, pathways, and other technical diagrams, use the scientific-schematics skill instead. |
| [`slides`](../../skills/community/ui-ux-pro-max/cli/assets/skills/slides/SKILL.md) | community | Create strategic HTML presentations with Chart.js, design tokens, responsive layouts, copywriting formulas, and contextual slide strategies. |
| [`ui-ux-pro-max`](../../skills/community/claude-scholar/skills/ui-ux-pro-max/SKILL.md) | community | This skill should be used when the user asks to design or review a UI, create a landing page or dashboard, choose colors or typography, improve accessibility, or implement polished frontend interfaces with a clear design system. |
| [`web-design-guidelines`](../../skills/community/boraoztunc-skills/web-design-guidelines/SKILL.md) | community | Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility", "audit design", "review UX", or "check my site against best practices". |

返回[全部分类](../README.md)或查看[新手大礼包](../../bundles/newcomer-starter-pack/README.md)。
