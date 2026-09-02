# AI Futures Scenario Lab 2026

> **兼容性说明：** 文中 `skills/community/nuwa-skill` / `huashu-nuwa` 检查仅是来源分支遗留的本地启发式，**非 canonical、非 governing acceptance gate**；当前验收以 canonical `xmg2024/nvwa-skill` 方法、来源解析、包行为测试、安全门及仓库验证为准。

把 *Life 3.0*（2017）与 *AI 2041*（2021）作为有日期的想象资源，以 2026 证据基线构造四个可监测、可反证、可复审的决策情景。小说和哲学情景不是预测权威。

```bash
python3 scripts/build_scenario.py \
  --focal "2032年前大学如何治理AI agents？" --horizon 2032 \
  --stakeholder 学生 --stakeholder 教师 --stakeholder 行政人员 \
  --uncertainty "代理可靠性|脆弱|稳健" \
  --uncertainty "治理分布|集中|参与式" \
  --action "可退出的沙盒试点" --as-of 2026-08-16 \
  --format json --output scenario.json
python3 -m unittest discover -s tests -p 'test_*.py'
python3 ../../nuwa-skill/scripts/quality_check.py SKILL.md
```

自定义声明：`--claim 'LABEL|TEXT|SOURCE|DATE'`；仅允许五标签。输出是待研究者补全/质询的实验骨架，不是自动预测器。
