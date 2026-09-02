# Applied Causal ML Readiness Lab

这是对 **《Applied Causal Inference Powered by ML and AI》在线版 v0.1.2（2026-05-03）** 的 Nuwa deep-tier 操作化蒸馏，不是摘要、书评、作者模拟或自动决策器。

## 核心用途

把因果 ML 项目从“先选算法”改造成 estimand、识别、重叠、cross-fitting、敏感性、异质性与迁移的分析合同。

**不可越过的边界**：DML 只降低满足前提时的 nuisance/regularization bias；不修复隐藏混杂、坏控制、无重叠、干扰或迁移失败。

## 深层结构

- [`SKILL.md`](SKILL.md)：IDENTIFY-DML 心智模型、逐步工作流、停止门、反证、内在张力与诚实边界；
- [`references/claim-layer-map.md`](references/claim-layer-map.md)：精确 18 条 A/B/C/D 声明，作者、作者限定、独立证据与本 Skill 推论不串层；
- [`references/source-notes.md`](references/source-notes.md)：书目版本、原始来源、独立证据、批评、适用范围和检索状态；
- [`references/templates.md`](references/templates.md)：可复制执行表，不是阅读笔记；
- [`references/research/`](references/research/)：六轮研究日志，包含取舍、反证和未解决项；
- [`scripts/audit_causal_ml.py`](scripts/audit_causal_ml.py)：只用 Python 标准库的确定性 JSON 审计 CLI；
- [`tests/test_adversarial.py`](tests/test_adversarial.py)：12 个包内红队测试；
- [`VALIDATION.md`](VALIDATION.md)：验证范围、命令、确定性与不声称事项。

## 快速开始

先读 `SKILL.md` 的适用场景与停止门，再复制对应模板；CLI 只检查输入合同：

```bash
python3 skills/community/nuwa-distilled/book-applied-causal-ml-readiness/scripts/audit_causal_ml.py --help
python3 skills/community/nuwa-distilled/book-applied-causal-ml-readiness/tests/test_adversarial.py
```

CLI 状态空间：`READY_FOR_ESTIMATION_PLAN / BLOCKED_* / GOVERNANCE_REVIEW_REQUIRED`。不存在自动伦理/因果/部署批准。

## 最小使用协议

1. 记录用途、owner、版本/日期、受影响人和替代方案；
2. 所有重要声明标 A/B/C/D，并回链 source ID；
3. 同时提交支持证据、反证/替代解释、未知与非迁移条件；
4. 触发停止门时不以更多模型复杂度绕过；
5. 决议保留异议、补救、停止条件和复审日期。

## 研究入口

从 [`references/research/01-version-scope-genre.md`](references/research/01-version-scope-genre.md) 开始，再回到 [reference index](references/README.md)。
