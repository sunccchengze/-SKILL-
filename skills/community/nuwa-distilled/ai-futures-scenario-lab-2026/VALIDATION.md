# Validation

> **兼容性说明：** 文中 `skills/community/nuwa-skill` / `huashu-nuwa` 检查仅是来源分支遗留的本地启发式，**非 canonical、非 governing acceptance gate**；当前验收以 canonical `xmg2024/nvwa-skill` 方法、来源解析、包行为测试、安全门及仓库验证为准。

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/build_scenario.py --focal "大学如何治理AI agents？" --horizon 2032 --stakeholder 学生 --stakeholder 教师 --uncertainty "可靠性|低|高" --uncertainty "治理参与|低|高" --action "可退出沙盒" --as-of 2026-08-16 --format json --output /tmp/scenario.json
python3 scripts/build_scenario.py --focal "x" --horizon 2032 --stakeholder students --uncertainty "a|l|h" --uncertainty "b|l|h" --claim "forecast-authority|certain|fiction|2021"  # 必须失败
python3 ../../nuwa-skill/scripts/quality_check.py SKILL.md
```

人工检查：四景恰好覆盖 2×2 且无概率；2017/2021/2026 日期、来源/类型/限制保留；每景有因果链、利益/权力/分配、指标/反证、可逆行动/停止/扩展/锁定、≥5 伦理镜头、复审日期/所有者；政策跨四景压力测试；fiction/speculation 未被写成 forecast authority。
