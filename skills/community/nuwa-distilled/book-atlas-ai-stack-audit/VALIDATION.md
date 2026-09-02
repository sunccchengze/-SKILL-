# Validation — Atlas of AI Full-Stack Audit

> **兼容性说明：** 文中 `skills/community/nuwa-skill` / `huashu-nuwa` 检查仅是来源分支遗留的本地启发式，**非 canonical、非 governing acceptance gate**；当前验收以 canonical `xmg2024/nvwa-skill` 方法、来源解析、包行为测试、安全门及仓库验证为准。

## Scope

验证对象是文件完整性、A/B/C/D 可追溯、模板可执行、CLI 语法/确定性/安全停止与包内链接。验证**不表示**书中主张全部真实，不代表用户场景满足假设，也不确认法律、伦理、因果、环境、劳动或部署结论。

## Commands

```bash
python3 skills/community/nuwa-distilled/book-atlas-ai-stack-audit/tests/test_adversarial.py
python3 skills/community/nuwa-skill/scripts/quality_check.py skills/community/nuwa-distilled/book-atlas-ai-stack-audit/SKILL.md
python3 skills/community/nuwa-distilled/book-atlas-ai-stack-audit/scripts/audit_ai_stack.py --help
```

仓库集成另由：

```bash
python3 tests/test_nuwa_modern_application_distillations.py
python3 scripts/validate_repository.py
```

## Determinism contract

CLI 仅使用 Python 标准库；文本压缩空白，重复 list 以 case-insensitive key 去重并稳定排序；JSON 使用 UTF-8、`sort_keys=True`、固定 schema/version。相同语义输入产生逐字节相同 stdout，不输出时间、随机数、绝对仓库路径，不联网、不读用户数据、不拟合或调用外部模型。

## Adversarial coverage

包内 `skills/community/nuwa-distilled/book-atlas-ai-stack-audit/tests/test_adversarial.py` 含 **12** 个测试，覆盖 deterministic/normalized 输出、精确 D 层标记、正常门、包特定阻断、危险参数、无自动批准、help 和无 shell execution。

## Validation limits

- markdown 来源卡是研究记录，不是对网页未来可用性的保证；
- 单元测试确认编码 gate，不证明输入证据真实、充分或代表性；
- quality checker 是结构性最低门，不评估每个规范选择；
- CLI 状态 `INCOMPLETE_STACK_MAP / BLOCKED_* / GOVERNANCE_REVIEW_REQUIRED` 只描述规格准备度；
- 真正使用仍需领域专家、受影响人、独立证据、法律/权利与组织 owner。

## Reproduction record

基准日：2026-08-16。交付前实际命令、通过数量、catalog hash 与仓库总量以版本控制中的最终运行结果为准；本文件不预先伪造结果。
