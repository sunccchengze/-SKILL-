# Validation

> **兼容性说明：** 文中 `skills/community/nuwa-skill` / `huashu-nuwa` 检查仅是来源分支遗留的本地启发式，**非 canonical、非 governing acceptance gate**；当前验收以 canonical `xmg2024/nvwa-skill` 方法、来源解析、包行为测试、安全门及仓库验证为准。

- [x] 七模型、九步 AGENCY-MIRROR 与失败条件
- [x] 哲学/实证/批评/Skill 综合分层
- [x] 六轮研究、来源总表、声明地图
- [x] 预测/目的、辅助/授权、拟人/理解明确分开
- [x] 人类判断不被浪漫化，权力与分配进入审计
- [x] 受影响者路径、无 AI 路径、真实异议/退出
- [x] 不可逆高风险自动化阻断
- [x] dependency-free CLI 与测试

```bash
python3 -m unittest discover -s tests -v
python3 ../../nuwa-skill/scripts/quality_check.py SKILL.md
```
