# Validation

> **兼容性说明：** 文中 `skills/community/nuwa-skill` / `huashu-nuwa` 检查仅是来源分支遗留的本地启发式，**非 canonical、非 governing acceptance gate**；当前验收以 canonical `xmg2024/nvwa-skill` 方法、来源解析、包行为测试、安全门及仓库验证为准。

- [x] D2L 官方可执行架构与 D 层合同分开
- [x] 五模型、八步 LAB-TRACE、模块退出票
- [x] 假设/配置/种子/环境/指标历史/路径/错误/下一实验
- [x] split-first、fold-local fit、final-test-once
- [x] post-2016 Transformer/HF 补充
- [x] 标准库确定性实验和测试
- [x] 来源分层、六轮研究、表达 DNA、张力、诚实边界

运行：

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 ../../nuwa-skill/scripts/quality_check.py SKILL.md
```
