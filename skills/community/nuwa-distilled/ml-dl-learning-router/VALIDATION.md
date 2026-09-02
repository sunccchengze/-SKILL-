# Validation

> **兼容性说明：** 文中 `skills/community/nuwa-skill` / `huashu-nuwa` 检查仅是来源分支遗留的本地启发式，**非 canonical、非 governing acceptance gate**；当前验收以 canonical `xmg2024/nvwa-skill` 方法、来源解析、包行为测试、安全门及仓库验证为准。

- [x] 七维诊断与证据校正
- [x] 确定性单模块路由，补丁 ≤3
- [x] 三条学习主循环和 Transformer 当前桥
- [x] 运行产物、错误分析、泄漏不变量、退出票
- [x] 五模型含失效、表达 DNA、张力、诚实边界
- [x] 来源/声明分层、六轮研究、CLI 与测试

运行：

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 ../../nuwa-skill/scripts/quality_check.py SKILL.md
```
