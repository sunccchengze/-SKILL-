---
name: multi-agent-orchestration
description: 为确实可并行、需要上下文隔离或独立红队的复杂任务设计最小多 Agent 团队，定义职责、文件边界、制品契约、合并顺序和验证门禁。
---

# 多 Agent 编排

读取并执行 [`../../governance/MULTI_AGENT_ORCHESTRATION.md`](../../governance/MULTI_AGENT_ORCHESTRATION.md)。

先证明拆分有价值，再创建角色。每个 Worker 必须有明确输入、允许修改范围、输出路径和验证方法。并行 Worker 不写同一文件；Reviewer 针对真实合并制品审查。
