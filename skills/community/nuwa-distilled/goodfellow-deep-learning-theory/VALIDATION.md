# Validation

> **兼容性说明：** 文中 `skills/community/nuwa-skill` / `huashu-nuwa` 检查仅是来源分支遗留的本地启发式，**非 canonical、非 governing acceptance gate**；当前验收以 canonical `xmg2024/nvwa-skill` 方法、来源解析、包行为测试、安全门及仓库验证为准。

- [x] 官方 Ch.5–11 理论主线与版权边界
- [x] 六模型、九步 THEORY-TRACE、推导合同与错误桶
- [x] 假设/符号/形状/计算图/解析与数值梯度
- [x] 优化行为、泛化失败、实验日志和下一实验
- [x] Transformer/LLM 严格标为 post-2016 补充
- [x] 标准库稳定 loss、步长扫描、极端值测试
- [x] 来源/声明分层、六轮研究、Nuwa 深层要素

运行：

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 ../../nuwa-skill/scripts/quality_check.py SKILL.md
```
