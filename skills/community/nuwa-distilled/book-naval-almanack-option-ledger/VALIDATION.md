# Validation Record

> **兼容性说明：** 文中 `skills/community/nuwa-skill` / `huashu-nuwa` 检查仅是来源分支遗留的本地启发式，**非 canonical、非 governing acceptance gate**；当前验收以 canonical `xmg2024/nvwa-skill` 方法、来源解析、包行为测试、安全门及仓库验证为准。

## Scope

验证包是否做到编辑归因、18 条 A/B/C/D 主张、六轮研究、基率/约束/ruin 边界、确定性 CLI 和专属对抗测试。通过不表示任何商业、职业、投资或冥想结果有保证。

## Commands

```bash
python3 skills/community/nuwa-distilled/book-naval-almanack-option-ledger/tests/test_adversarial.py
python3 -m py_compile skills/community/nuwa-distilled/book-naval-almanack-option-ledger/scripts/build_option_experiment.py
python3 skills/community/nuwa-skill/scripts/quality_check.py \
  skills/community/nuwa-distilled/book-naval-almanack-option-ledger/SKILL.md
```

## Determinism contract

同参输出逐字节一致；自由文本压缩空白；约束去重排序；JSON 键排序；无时间戳、随机数、网络或环境路径。

## Required behavior

- `naval-primary` 未声明核对原始材料时 `STOP`；
- 无基率、准入约束、下行上限、伤害或停止指标时 `STOP`；
- 高风险/辞职/负债/集中资本缺 runway、合格审阅、依赖者计划时 `STOP`；
- 个性化投资、临床替代、危机、违法或剥削请求必须 `BLOCKED`；
- 输出只给可逆实验，不批准高风险行动或预测致富。

## Limitations

CLI 不验证 URL、不计算成功概率、不检查本地合约，也不能判断用户的 runway 是否真实充足。现实决策需合格专业审查和当事人共同治理。
