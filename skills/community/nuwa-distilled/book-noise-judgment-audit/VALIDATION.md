# Validation Record

> **兼容性说明：** 文中 `skills/community/nuwa-skill` / `huashu-nuwa` 检查仅是来源分支遗留的本地启发式，**非 canonical、非 governing acceptance gate**；当前验收以 canonical `xmg2024/nvwa-skill` 方法、来源解析、包行为测试、安全门及仓库验证为准。

## Scope

验证对象是 Nuwa deep-tier 包的结构、18 条分层主张、六轮研究、确定性 CLI、判断资格门、公平/申诉门和专属红队行为。验证不代表任一现实判断系统已被证明准确、公平或合法。

## Commands

```bash
python3 skills/community/nuwa-distilled/book-noise-judgment-audit/tests/test_adversarial.py
python3 -m py_compile skills/community/nuwa-distilled/book-noise-judgment-audit/scripts/audit_judgment_system.py
python3 skills/community/nuwa-skill/scripts/quality_check.py \
  skills/community/nuwa-distilled/book-noise-judgment-audit/SKILL.md
```

## Determinism contract

同参输出逐字节一致。自由文本压缩空白；重复干预去重排序；JSON 键排序；无时间戳、随机数、网络访问或环境路径。

## Required behavior

- 只有一名判断者且无重复测量时 `STOP`；
- 没有可辩护目标时输出可靠性审计并禁止准确性声明；
- 要求移除全部裁量时 `STOP`；
- 高影响场景缺领域审阅、群体审计、申诉或停止条件时 `STOP`；
- 紧急场景 `BLOCKED_FOR_EMERGENCY`；
- 输出不得给个案诊疗、量刑、录用或福利资格决定。

## Limitations

CLI 不摄入个人数据、不计算 ICC/MSE、不训练模型，也不验证公平性。它只生成测量和治理计划，现实实施仍需统计、领域、法务、隐私及受影响者参与。
