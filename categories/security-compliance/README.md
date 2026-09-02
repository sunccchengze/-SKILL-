# 安全、隐私与合规

安全评审、威胁与风险、隐私、无障碍、依赖、审计和合规治理。

- 默认可见技能：**147**
- 新手大礼包入选：**7**
- 完整机器索引：[`skills.tsv`](skills.tsv)

## 如何找技能

```bash
python scripts/search_skills.py "security privacy compliance audit" --category security-compliance --limit 12
```

先看搜索元数据，只打开当前任务真正命中的 1 个主技能和至多 3 个互补技能；不要把本分类全部载入上下文。

## 新手大礼包中的代表技能

| 技能 | 层级 | 用途 |
|---|---|---|
| [`accessibility`](../../skills/community/ECC/skills/accessibility/SKILL.md) | community | Design, implement, and audit inclusive digital products using WCAG 2.2 Level AA |
| [`ai-security`](../../skills/community/alirezarezvani-claude-skills/engineering-team/skills/ai-security/SKILL.md) | community | Use when assessing AI/ML systems for prompt injection, jailbreak vulnerabilities, model inversion risk, data poisoning exposure, or agent tool abuse. Covers MITRE ATLAS technique mapping, injection signature detection, and adversarial robustness scoring. |
| [`dependency-auditor`](../../skills/community/alirezarezvani-claude-skills/engineering/skills/dependency-auditor/SKILL.md) | community | Audit and manage dependencies across multi-language projects. Identifies vulnerabilities, license conflicts, transitive dependency risks, and safe-upgrade paths. Use when auditing third-party packages before release, investigating a CVE, planning a major version bump, or running a license-compliance review. Examples: 'audit our npm dependencies', 'do we have GPL contamination', 'plan the upgrade to React 19'. |
| [`incident-response`](../../skills/community/alirezarezvani-claude-skills/engineering-team/skills/incident-response/SKILL.md) | community | Use when a security incident has been detected or declared and needs classification, triage, escalation path determination, and forensic evidence collection. Covers SEV1-SEV4 classification, false positive filtering, incident taxonomy, and NIST SP 800-61 lifecycle. |
| [`security-and-hardening`](../../skills/community/agent-skills-main/skills/security-and-hardening/SKILL.md) | community | Hardens code against vulnerabilities. Use when handling user input, authentication, data storage, or external integrations. Use when building any feature that accepts untrusted data, manages user sessions, or interacts with third-party services. |
| [`security-audit`](../../skills/community/buildwithclaude-hub/plugins/agent-triforce/skills/security-audit/SKILL.md) | community | Deep security audit covering OWASP Top 10, authentication, authorization, data protection, dependency vulnerabilities, and secrets scanning. Delegates to the Centinela (QA) agent. |
| [`security-review`](../../skills/community/ECC/skills/security-review/SKILL.md) | community | Use this skill when adding authentication, handling user input, working with secrets, creating API endpoints, or implementing payment/sensitive features. Provides comprehensive security checklist and patterns. |

返回[全部分类](../README.md)或查看[新手大礼包](../../bundles/newcomer-starter-pack/README.md)。
