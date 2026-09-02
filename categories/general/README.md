# 通用生产力

跨领域计划、沟通、会议、通用工具、个人效率与难以单归一域的能力。

- 默认可见技能：**286**
- 新手大礼包入选：**5**
- 完整机器索引：[`skills.tsv`](skills.tsv)

## 如何找技能

```bash
python scripts/search_skills.py "plan communicate productivity" --category general --limit 12
```

先看搜索元数据，只打开当前任务真正命中的 1 个主技能和至多 3 个互补技能；不要把本分类全部载入上下文。

## 新手大礼包中的代表技能

| 技能 | 层级 | 用途 |
|---|---|---|
| [`stop-slop`](../../skills/core/stop-slop/SKILL.md) | maintained | 起草、编辑或审阅散文时识别并删除常见 AI 模板腔，包括空泛开场、公式结构、虚假深度、模糊归因、节奏单一、过度修辞和可删内容，同时保留事实、含义与目标语气。 |
| [`executing-plans`](../../skills/community/superpowers-main/skills/executing-plans/SKILL.md) | community | Use when you have a written implementation plan to execute in a separate session with review checkpoints |
| [`project-health`](../../skills/community/alirezarezvani-claude-skills/.gemini/skills/project-health/SKILL.md) | community | Portfolio health dashboard and risk matrix analysis. Usage: /project-health <dashboard|risk> [options] |
| [`sprint-plan`](../../skills/community/alirezarezvani-claude-skills/.gemini/skills/sprint-plan/SKILL.md) | community | Capacity-gated sprint planning — runs capacity math, carry-over check, and a definition-of-ready gate before committing scope. Usage: /sprint-plan <goal> [capacity] |
| [`verification-before-completion`](../../skills/community/superpowers-main/skills/verification-before-completion/SKILL.md) | community | Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any success claims; evidence before assertions always |

返回[全部分类](../README.md)或查看[新手大礼包](../../bundles/newcomer-starter-pack/README.md)。
