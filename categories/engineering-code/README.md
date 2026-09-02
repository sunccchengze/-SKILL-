# 工程与代码

架构、编码、测试、调试、评审、Git、CI/CD、API、前后端与性能。

- 默认可见技能：**767**
- 新手大礼包入选：**24**
- 完整机器索引：[`skills.tsv`](skills.tsv)

## 如何找技能

```bash
python scripts/search_skills.py "code test debug review architecture" --category engineering-code --limit 12
```

先看搜索元数据，只打开当前任务真正命中的 1 个主技能和至多 3 个互补技能；不要把本分类全部载入上下文。

## 新手大礼包中的代表技能

| 技能 | 层级 | 用途 |
|---|---|---|
| [`openwiki`](../../tools/openwiki/SKILL.md) | maintained | 使用仓库内固定版本的 LangChain OpenWiki CLI，为代码库生成和持续维护面向 Agent 的 Markdown Wiki、AGENTS/CLAUDE 入口、Mermaid 图与 OKF 文档。适用于代码库理解、架构文档、持续文档更新和 CI 文档任务。 |
| [`spec-kit`](../../tools/spec-kit/SKILL.md) | maintained | Apply GitHub Spec Kit's pinned specification-driven workflow to define principles, requirements, plans, tasks, implementation, and convergence checks. Use when starting or restructuring non-trivial product or software work that benefits from traceable specs before code. |
| [`api-and-interface-design`](../../skills/community/agent-skills-main/skills/api-and-interface-design/SKILL.md) | community | Guides stable API and interface design. Use when designing APIs, module boundaries, or any public interface. Use when creating REST or GraphQL endpoints, defining type contracts between modules, or establishing boundaries between frontend and backend. |
| [`architecture-decision-records`](../../skills/community/ECC/skills/architecture-decision-records/SKILL.md) | community | Capture architectural decisions made during Claude Code sessions as structured ADRs. Auto-detects decision moments, records context, alternatives considered, and rationale. Maintains an ADR log so future developers understand why the codebase is shaped the way it is. |
| [`backend-patterns`](../../skills/community/ECC/skills/backend-patterns/SKILL.md) | community | Backend architecture patterns, API design, database optimization, and server-side best practices for Node.js, Express, and Next.js API routes. |
| [`browser-testing-with-devtools`](../../skills/community/agent-skills-main/skills/browser-testing-with-devtools/SKILL.md) | community | Tests in real browsers via Chrome DevTools MCP. Use when building or debugging anything that runs in a browser. Use when you need to inspect the DOM, capture console errors, analyze network requests, profile performance, or verify visual output with real runtime data. Requires the chrome-devtools MCP server to be configured. |
| [`ci-cd-pipeline-builder`](../../skills/community/alirezarezvani-claude-skills/engineering/skills/ci-cd-pipeline-builder/SKILL.md) | community | Generate pragmatic CI/CD pipelines from detected project stack signals — fast baseline generation, repeatable checks, environment-aware deployment stages. Use when setting up CI for a new project, refactoring existing pipelines, or standardizing deployment workflows across multiple repos. |
| [`code-review-excellence`](../../skills/community/claude-scholar/skills/code-review-excellence/SKILL.md) | community | This skill should be used when the user asks to review a diff or pull request, write review comments, audit code quality, establish review standards, or improve how a team performs code review. |
| [`code-simplification`](../../skills/community/agent-skills-main/skills/code-simplification/SKILL.md) | community | Simplifies code for clarity. Use when refactoring code for clarity without changing behavior. Use when code works but is harder to read, maintain, or extend than it should be. Use when reviewing code that has accumulated unnecessary complexity. |
| [`codebase-onboarding`](../../skills/community/ECC/skills/codebase-onboarding/SKILL.md) | community | Analyze an unfamiliar codebase and generate a structured onboarding guide with architecture map, key entry points, conventions, and a starter CLAUDE.md. Use when joining a new project or setting up Claude Code for the first time in a repo. |
| [`coding-standards`](../../skills/community/ECC/skills/coding-standards/SKILL.md) | community | Baseline cross-project coding conventions for naming, readability, immutability, and code-quality review. Use detailed frontend or backend skills for framework-specific patterns. |
| [`frontend-patterns`](../../skills/community/ECC/skills/frontend-patterns/SKILL.md) | community | Frontend development patterns for React, Next.js, state management, performance optimization, and UI best practices. |
| [`git-workflow-and-versioning`](../../skills/community/agent-skills-main/skills/git-workflow-and-versioning/SKILL.md) | community | Structures git workflow practices. Use when making any code change. Use when committing, branching, resolving conflicts, or when you need to organize work across multiple parallel streams. Use when cutting a release, choosing a semantic version bump, tagging, or writing a changelog. |
| [`github-automation`](../../skills/community/buildwithclaude-hub/plugins/all-skills/skills/github-automation/SKILL.md) | community | Automate GitHub repositories, issues, pull requests, branches, CI/CD, and permissions via Rube MCP (Composio). Manage code workflows, review PRs, search code, and handle deployments programmatically. |
| [`python-patterns`](../../skills/community/ECC/skills/python-patterns/SKILL.md) | community | Pythonic idioms, PEP 8 standards, type hints, and best practices for building robust, efficient, and maintainable Python applications. |
| [`receiving-code-review`](../../skills/community/superpowers-main/skills/receiving-code-review/SKILL.md) | community | Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear or technically questionable - requires technical rigor and verification, not performative agreement or blind implementation |
| [`requesting-code-review`](../../skills/community/superpowers-main/skills/requesting-code-review/SKILL.md) | community | Use when completing tasks, implementing major features, or before merging to verify work meets requirements |
| [`security-guidance`](../../skills/community/alirezarezvani-claude-skills/engineering/security-guidance/skills/security-guidance/SKILL.md) | community | PreToolUse security-anti-pattern hook for Claude Code. Catches 12 common security risks (command injection, XSS, SQL injection, unsafe deserialization, GitHub Actions workflow injection, eval/new Function code injection) BEFORE the Edit/Write/MultiEdit operation completes. Session-state caching prevents duplicate warnings on the same file+rule combo. Stdlib only — no dependencies. Use when you want a safety net during Claude Code sessions that touch security-sensitive code (auth, payments, user input handling, IaC). Disable with ENABLE_SECURITY_REMINDER=0 if you need to perform a verified-safe operation that would otherwise trip a pattern. Triggers — "add security hook", "block unsafe code", "detect command injection before write", "prevent SQL injection patterns", "security warning hook". |
| [`skill-creator`](../../skills/community/skills-main/skills/skill-creator/SKILL.md) | community | Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy. |
| [`skill-security-auditor`](../../skills/community/alirezarezvani-claude-skills/engineering/skills/skill-security-auditor/SKILL.md) | community | Security audit and vulnerability scanner for AI agent skills before installation. Use when: (1) evaluating a skill from an untrusted source, (2) auditing a skill directory or git repo URL for malicious code, (3) pre-install security gate for Claude Code plugins, OpenClaw skills, or Codex skills, (4) scanning Python scripts for dangerous patterns like os.system, eval, subprocess, network exfiltration, (5) detecting prompt injection in SKILL.md files, (6) checking dependency supply chain risks, (7) verifying file system access stays within skill boundaries. Triggers: "audit this skill", "is this skill safe", "scan skill for security", "check skill before install", "skill security check", "skill vulnerability scan". |

返回[全部分类](../README.md)或查看[新手大礼包](../../bundles/newcomer-starter-pack/README.md)。
