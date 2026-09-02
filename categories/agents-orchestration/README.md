# Agent 与编排

路由、计划、上下文、记忆、评估、多 Agent 协作与工作流治理。

- 默认可见技能：**384**
- 新手大礼包入选：**11**
- 完整机器索引：[`skills.tsv`](skills.tsv)

## 如何找技能

```bash
python scripts/search_skills.py "task planning orchestration verification" --category agents-orchestration --limit 12
```

先看搜索元数据，只打开当前任务真正命中的 1 个主技能和至多 3 个互补技能；不要把本分类全部载入上下文。

## 新手大礼包中的代表技能

| 技能 | 层级 | 用途 |
|---|---|---|
| [`multi-agent-orchestration`](../../skills/core/multi-agent-orchestration/SKILL.md) | maintained | 为确实可并行、需要上下文隔离或独立红队的复杂任务设计最小多 Agent 团队，定义职责、文件边界、制品契约、合并顺序和验证门禁。 |
| [`official-source-router`](../../skills/core/official-source-router/SKILL.md) | maintained | Route product- and platform-specific work across 859 pinned skill entry paths from OpenAI, Vercel, and Microsoft official repositories. Use when selecting a first-party workflow, resolving duplicate skill names, initializing an official source, checking provenance or license boundaries, or combining official skills with the repository's maintained workflows. |
| [`universal-skill-router`](../../SKILL.md) | router | 面向任意项目的技能检索、领域适配和最小专家组编排入口。用于在大型技能仓库中根据真实任务选择少量互补技能，建立制品契约与验证门禁，避免把历史项目假设带入新方向。 |
| [`dispatching-parallel-agents`](../../skills/community/superpowers-main/skills/dispatching-parallel-agents/SKILL.md) | community | Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies |
| [`docker-patterns`](../../skills/community/ECC/skills/docker-patterns/SKILL.md) | community | Docker and Docker Compose patterns for local development, hardened CLI installer harnesses, container security, networking, volumes, and multi-service orchestration. Use when creating or reviewing Dockerfiles and Compose services, testing installers across Linux distributions, or planning accurate native macOS and Windows validation. |
| [`planning-and-task-breakdown`](../../skills/community/agent-skills-main/skills/planning-and-task-breakdown/SKILL.md) | community | Breaks work into ordered tasks. Use when you have a spec or clear requirements and need to break work into implementable tasks. Use when a task feels too large to start, when you need to estimate scope, or when parallel work is possible. |
| [`search-first`](../../skills/community/ECC/skills/search-first/SKILL.md) | community | Research-before-coding workflow. Search for existing tools, libraries, and patterns before writing custom code. Invokes the researcher agent. |
| [`spec-driven-development`](../../skills/community/agent-skills-main/skills/spec-driven-development/SKILL.md) | community | Creates specs before coding. Use when starting a new project, feature, or significant change and no specification exists yet. Use when requirements are unclear, ambiguous, or only exist as a vague idea. |
| [`subagent-driven-development`](../../skills/community/superpowers-main/skills/subagent-driven-development/SKILL.md) | community | Use when executing implementation plans with independent tasks in the current session |
| [`using-agent-skills`](../../skills/community/agent-skills-main/skills/using-agent-skills/SKILL.md) | community | Discovers and invokes agent skills. Use when starting a session or when you need to discover which skill applies to the current task. This is the meta-skill that governs how all other skills are discovered and invoked. |
| [`websearch`](../../skills/community/prime-agent/packages/coding-agent/skills/websearch/SKILL.md) | community | Search Google via the Serper API. Configure access via /login, then MCP Connections, then Serper (web search). Takes one query and returns titles, URLs, snippets, and knowledge-graph data. |

返回[全部分类](../README.md)或查看[新手大礼包](../../bundles/newcomer-starter-pack/README.md)。
