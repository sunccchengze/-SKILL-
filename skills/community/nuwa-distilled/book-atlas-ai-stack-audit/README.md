# Atlas of AI Full-Stack Audit

这是对 **Kate Crawford《Atlas of AI》（Yale University Press, 2021）** 的 Nuwa deep-tier 操作化蒸馏，不是摘要、书评、作者模拟或自动决策器。

## 核心用途

把 AI 从模型/界面扩展到地点、物质、劳动、数据、分类、情感构念、国家与权力的全栈审计。

**不可越过的边界**：每条环境/劳动/性能声明须带边界、地域、日期、分母和不确定性；设施总量不得无依据换算到单模型/提示。

## 深层结构

- [`SKILL.md`](SKILL.md)：ATLAS-STACK 心智模型、逐步工作流、停止门、反证、内在张力与诚实边界；
- [`references/claim-layer-map.md`](references/claim-layer-map.md)：精确 18 条 A/B/C/D 声明，作者、作者限定、独立证据与本 Skill 推论不串层；
- [`references/source-notes.md`](references/source-notes.md)：书目版本、原始来源、独立证据、批评、适用范围和检索状态；
- [`references/templates.md`](references/templates.md)：可复制执行表，不是阅读笔记；
- [`references/research/`](references/research/)：六轮研究日志，包含取舍、反证和未解决项；
- [`scripts/audit_ai_stack.py`](scripts/audit_ai_stack.py)：只用 Python 标准库的确定性 JSON 审计 CLI；
- [`tests/test_adversarial.py`](tests/test_adversarial.py)：12 个包内红队测试；
- [`VALIDATION.md`](VALIDATION.md)：验证范围、命令、确定性与不声称事项。

## 快速开始

先读 `SKILL.md` 的适用场景与停止门，再复制对应模板；CLI 只检查输入合同：

```bash
python3 skills/community/nuwa-distilled/book-atlas-ai-stack-audit/scripts/audit_ai_stack.py --help
python3 skills/community/nuwa-distilled/book-atlas-ai-stack-audit/tests/test_adversarial.py
```

CLI 状态空间：`INCOMPLETE_STACK_MAP / BLOCKED_* / GOVERNANCE_REVIEW_REQUIRED`。不存在自动伦理/因果/部署批准。

## 最小使用协议

1. 记录用途、owner、版本/日期、受影响人和替代方案；
2. 所有重要声明标 A/B/C/D，并回链 source ID；
3. 同时提交支持证据、反证/替代解释、未知与非迁移条件；
4. 触发停止门时不以更多模型复杂度绕过；
5. 决议保留异议、补救、停止条件和复审日期。

## 研究入口

从 [`references/research/01-source-architecture.md`](references/research/01-source-architecture.md) 开始，再回到 [reference index](references/README.md)。
