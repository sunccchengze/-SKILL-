# Validation Record

> **兼容性说明：** 文中 `skills/community/nuwa-skill` / `huashu-nuwa` 检查仅是来源分支遗留的本地启发式，**非 canonical、非 governing acceptance gate**；当前验收以 canonical `xmg2024/nvwa-skill` 方法、来源解析、包行为测试、安全门及仓库验证为准。

## Scope

该验证确认包具备 18 条 A/B/C/D 主张、六轮研究、可执行模板、确定性 CLI、权利/停止门和包专属对抗测试。它不确认《Sapiens》的每个历史陈述为真。

## Commands

```bash
python3 skills/community/nuwa-distilled/book-sapiens-claim-audit/tests/test_adversarial.py
python3 -m py_compile skills/community/nuwa-distilled/book-sapiens-claim-audit/scripts/audit_historical_claim.py
python3 skills/community/nuwa-distilled/book-sapiens-claim-audit/scripts/audit_historical_claim.py \
  --claim "agriculture always improved individual health" \
  --scale regional --period "10000-5000 BP" --region "multiple regions" \
  --evidence "stature proxy" --alternative "regional heterogeneity" \
  --uncertainty "proxy is not total wellbeing" --audience "seminar" --use-context education
python3 skills/community/nuwa-skill/scripts/quality_check.py \
  skills/community/nuwa-distilled/book-sapiens-claim-audit/SKILL.md
```

## Determinism contract

同一参数必须产生逐字节一致 JSON。JSON 必须排序键；列表做空白清理、去重和排序；不得写入时间戳、随机数、网络结果或环境路径。

## Required adversarial behavior

- 缺少证据、替代解释或不确定性时拒绝生成“通过”计划；
- 全局主张只有一个局部证据时标记尺度缺口；
- `--dehumanizing-use`、`--rights-denial` 或 `--atrocity-denial` 必须返回 `BLOCKED`；
- `policy`、`ancestry`、`territorial` 使用必须有责任人、领域审阅、社群咨询、异议渠道和停止条件，否则 `STOP`；
- 输出必须明确“计划不是历史真值裁决”。

## Known limitations

- CLI 不读取论文、不计算年代模型、不做因果推断；
- 包中页码会随语言和版本变化；
- 来源清单是定向证据集，不是系统综述；
- 文本测试能检测门是否存在，不能保证现实治理质量。
