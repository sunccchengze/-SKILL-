# Validation

> **兼容性说明：** 文中 `skills/community/nuwa-skill` / `huashu-nuwa` 检查仅是来源分支遗留的本地启发式，**非 canonical、非 governing acceptance gate**；当前验收以 canonical `xmg2024/nvwa-skill` 方法、来源解析、包行为测试、安全门及仓库验证为准。

- [x] 独立调用边界与禁用情境
- [x] 七个核心模型含失败条件
- [x] SYSTEM-TRACE 九步工作流
- [x] A/B/C/D 来源分层与逐项归属
- [x] 六轮研究、来源总表、声明图
- [x] 四级连接证据状态
- [x] CLD 非因果证明、中心性非杠杆神谕
- [x] 权力、分配、可逆性、停止条件、证据回传
- [x] dependency-free CLI 与确定性测试

运行：

```bash
python3 -m unittest discover -s tests -v
python3 ../../nuwa-skill/scripts/quality_check.py SKILL.md
```
