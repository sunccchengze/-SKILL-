# Validation

> **兼容性说明：** 文中 `skills/community/nuwa-skill` / `huashu-nuwa` 检查仅是来源分支遗留的本地启发式，**非 canonical、非 governing acceptance gate**；当前验收以 canonical `xmg2024/nvwa-skill` 方法、来源解析、包行为测试、安全门及仓库验证为准。

- [x] 七模型、十步 CO-LAB 与失效条件
- [x] A/B/C/D 分层、六轮研究和逐项来源
- [x] jagged frontier 按任务/模型/日期限定
- [x] Centaur/Cyborg/AI-first/just-me/human-first 路由
- [x] 合规、隐私、验证、问责与披露
- [x] 辅助表现/无辅助学习分离
- [x] 角色模拟不等于人格/资质/责任
- [x] dependency-free CLI 与测试

```bash
python3 -m unittest discover -s tests -v
python3 ../../nuwa-skill/scripts/quality_check.py SKILL.md
```
