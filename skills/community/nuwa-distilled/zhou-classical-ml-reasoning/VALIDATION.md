# Validation

> **兼容性说明：** 文中 `skills/community/nuwa-skill` / `huashu-nuwa` 检查仅是来源分支遗留的本地启发式，**非 canonical、非 governing acceptance gate**；当前验收以 canonical `xmg2024/nvwa-skill` 方法、来源解析、包行为测试、安全门及仓库验证为准。

- [x] 经典 ML 序列与南瓜书伴读边界
- [x] 六模型、九步 CLASSIC-TRACE、模型假设卡
- [x] 问题/标签/评估先于算法
- [x] split-before-fit、fold-local fit、final-test-once
- [x] 基线、指标历史、错误分析、不确定性、下一实验
- [x] post-2016 Transformer 连接单独标注
- [x] 来源/六轮研究、标准库 CLI、确定性测试、Nuwa 深层要素

运行：

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 ../../nuwa-skill/scripts/quality_check.py SKILL.md
```
