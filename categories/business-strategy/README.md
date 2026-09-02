# 商业与战略

产品、市场、营销、定价、竞争、运营、决策、发布与组织协作。

- 默认可见技能：**165**
- 新手大礼包入选：**11**
- 完整机器索引：[`skills.tsv`](skills.tsv)

## 如何找技能

```bash
python scripts/search_skills.py "product strategy market decision" --category business-strategy --limit 12
```

先看搜索元数据，只打开当前任务真正命中的 1 个主技能和至多 3 个互补技能；不要把本分类全部载入上下文。

## 新手大礼包中的代表技能

| 技能 | 层级 | 用途 |
|---|---|---|
| [`ai-cabinet-decision-making`](../../skills/core/ai-cabinet/SKILL.md) | maintained | 用五个独立席位对重要决策、方案比较、路线选择和高不确定性计划进行第一性原理追问、红队攻击、机会分析、外行清晰度审查与执行拆解，再由主席给出有条件建议。 |
| [`competitive-intel`](../../skills/community/alirezarezvani-claude-skills/c-level-advisor/skills/competitive-intel/SKILL.md) | community | Systematic competitor tracking that feeds CMO positioning, CRO battlecards, and CPO roadmap decisions. Use when analyzing competitors, building sales battlecards, tracking market moves, positioning against alternatives, or when user mentions competitive intelligence, competitive analysis, competitor research, battlecards, win/loss, or market positioning. |
| [`launch-strategy`](../../skills/community/alirezarezvani-claude-skills/marketing-skill/skills/launch-strategy/SKILL.md) | community | When the user wants to plan a product launch, feature announcement, or release strategy. Also use when the user mentions 'launch,' 'Product Hunt,' 'feature release,' 'announcement,' 'go-to-market,' 'beta launch,' 'early access,' 'waitlist,' 'product update,' 'GTM plan,' 'launch checklist,' or 'launch momentum.' This skill covers phased launches, channel strategy, and ongoing launch momentum. |
| [`market-research`](../../skills/community/ECC/skills/market-research/SKILL.md) | community | Conduct market research, competitive analysis, investor due diligence, and industry intelligence with source attribution and decision-oriented summaries. Use when the user wants market sizing, competitor comparisons, fund research, technology scans, or research that informs business decisions. |
| [`marketing-campaign`](../../skills/community/ECC/skills/marketing-campaign/SKILL.md) | community | End-to-end marketing campaign planning and execution. Covers audience research, positioning, campaign angle definition, landing page copy, email sequences, social posts, ad copy, short-form video scripts, and content calendars. Use as the orchestration layer for multi-channel product launches. |
| [`marketing-strategy-pmm`](../../skills/community/alirezarezvani-claude-skills/marketing-skill/skills/marketing-strategy-pmm/SKILL.md) | community | Product marketing skill for positioning, GTM strategy, competitive intelligence, and product launches. Use when the user asks about product positioning, go-to-market planning, competitive analysis, target audience definition, ICP definition, market research, launch plans, or sales enablement. Covers April Dunford positioning, ICP definition, competitive battlecards, launch playbooks, and international market entry. Produces deliverables including positioning statements, battlecard documents, launch plans, and go-to-market strategies. |
| [`meetings`](../../skills/community/alirezarezvani-claude-skills/productivity/meetings/skills/meetings/SKILL.md) | community | Use when someone wants to decide whether a meeting is worth calling, price a meeting in dollars, build a timeboxed agenda with desired outcomes, or turn messy meeting notes into owned action items — or says "should this be a meeting", "/cs:meeting-prep", or "/cs:meeting-actions". Runs a cost gate (ASYNC / NOT-READY / MEET), builds a decision-first agenda, and extracts an owner + due-date checklist that flags every orphan. |
| [`pricing-strategy`](../../skills/community/alirezarezvani-claude-skills/marketing-skill/skills/pricing-strategy/SKILL.md) | community | Design, optimize, and communicate SaaS pricing — tier structure, value metrics, pricing pages, and price increase strategy. Use when building a pricing model from scratch, redesigning existing pricing, planning a price increase, or improving a pricing page. Trigger keywords: pricing tiers, pricing page, price increase, packaging, value metric, per seat pricing, usage-based pricing, freemium, good-better-best, pricing strategy, monetization, pricing page conversion, Van Westendorp. NOT for broader product strategy — use product-strategist for that. NOT for customer success or renewals — use customer-success-manager for expansion revenue. |
| [`product-analytics`](../../skills/community/alirezarezvani-claude-skills/product-team/skills/product-analytics/SKILL.md) | community | Use when defining product KPIs, building metric dashboards, running cohort or retention analysis, or interpreting feature adoption trends across product stages. |
| [`product-discovery`](../../skills/community/alirezarezvani-claude-skills/product-team/skills/product-discovery/SKILL.md) | community | Use when validating product opportunities, mapping assumptions, planning discovery sprints, or testing problem-solution fit before committing delivery resources. |
| [`product-manager`](../../skills/community/alirezarezvani-claude-skills/.gemini/skills/product-manager/SKILL.md) | community | Ships outcomes, not features. Writes specs engineers actually read. Prioritizes ruthlessly. Kills darlings when the data says so. Operates at the intersection of user needs, business goals, and engineering reality. Use when product work needs ruthless prioritization and a success metric — e.g., turning vague stakeholder asks into a 2-page spec, or deciding which of three competing roadmap bets to fund this quarter. (For framework-heavy RICE/PRD tooling, see cs-product-manager.) |

返回[全部分类](../README.md)或查看[新手大礼包](../../bundles/newcomer-starter-pack/README.md)。
