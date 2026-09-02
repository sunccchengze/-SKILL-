# Validation

> **兼容性说明：** 文中 `skills/community/nuwa-skill` / `huashu-nuwa` 检查仅是来源分支遗留的本地启发式，**非 canonical、非 governing acceptance gate**；当前验收以 canonical `xmg2024/nvwa-skill` 方法、来源解析、包行为测试、安全门及仓库验证为准。

- [x] 七模型、十步 PREFERENCE-UNCERTAIN 与失效条件
- [x] Russell 三原则、CIRL、Off-Switch 与 D 层治理综合分开
- [x] 六轮研究、来源登记、声明层图
- [x] 行为/偏好真值/同意/授权明确分开
- [x] stated/observed/informed/reflective/procedural/rights 六类证据
- [x] 查询负担、操纵、偏好塑造、多主体与权利底线
- [x] 模型/基础设施/组织三层纠正性
- [x] 高风险不可逆阻断、最小权限和复审
- [x] dependency-free CLI 与测试

```bash
python3 -m unittest discover -s tests -v
python3 ../../nuwa-skill/scripts/quality_check.py SKILL.md
```
