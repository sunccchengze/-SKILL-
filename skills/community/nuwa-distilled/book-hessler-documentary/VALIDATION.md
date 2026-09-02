# 验证记录：book-hessler-documentary

> **兼容性说明：** 文中 `skills/community/nuwa-skill` / `huashu-nuwa` 检查仅是来源分支遗留的本地启发式，**非 canonical、非 governing acceptance gate**；当前验收以 canonical `xmg2024/nvwa-skill` 方法、来源解析、包行为测试、安全门及仓库验证为准。

验证日期：2026-08-16。范围：本包文本、来源映射、CLI 与对抗测试；**不证明**现实个案中的机制成立，也不构成上线、法律、临床、伦理或编辑批准。

## 深层质量审计

| 维度 | 目标与证据 | 残余边界 |
|---|---|---|
| 原作保真 | A/B 分层，版本与作者谱系不倒灌 | 未逐页复刻所有版本 |
| 独立证据 | C 层包含标准、反证、外部效度与竞争模型 | 不是系统综述或元分析 |
| 可执行 | LEDGERS、模板、dependency-free CLI | 工作流未经普适效度验证 |
| 可反驳 | 每个关键机制含反证、替代解释或停止门 | 工作表本身不识别因果 |
| 安全治理 | 无法理解的同意、脆弱来源再识别、非法/未同意录音、核心指控未核、敏感位置暴露必须暂停并升级。 | 不替代所在地专业程序 |
| 来源追踪 | 18 条 claim IDs 映射 source IDs | 用户案例事实仍须现场核验 |

## 内容不变量

1. A/B/C/D 不坍缩；
2. 原书原则是问题生成器，不是结果保证；
3. 观察和推断分开；
4. 至少保留一个竞争解释；
5. 风险门不能被平均分抵消；
6. 高风险必须有责任人、停止条件与退出/回滚；
7. CLI 输出只是工作底稿，状态不表示批准；
8. 不可信输入被转义且不会执行；
9. JSON/Markdown 对相同输入稳定；
10. 包级测试不得联网或依赖第三方库。

## 测试命令

从仓库根目录：

```bash
python3 -m unittest discover -s skills/community/nuwa-distilled/book-hessler-documentary/tests -p 'test_*.py' -v
python3 skills/community/nuwa-skill/scripts/quality_check.py skills/community/nuwa-distilled/book-hessler-documentary/SKILL.md
```

从包根目录：

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 ../../nuwa-skill/scripts/quality_check.py SKILL.md
```

## 必测对抗行为

- 必填字段空白或仅空格时退出码为 2；
- 重复枚举/不支持格式受控失败；
- 两次相同 JSON 调用逐字节一致；
- Markdown 中 `|`、换行和反斜杠不会破坏表格；
- 触发包专属高风险门时不生成普通建议；
- 超长输入或提示注入只作为文本，不改变执行路径；
- 成功状态固定为 `governance_review_required`，不声称“验证有效”。

## 残余盲点

分别维护 River Town 与 Country Driving 作品账本，把观察、访谈、推断、核验、同意、隐私与再现转成编辑可审计流程；不模仿作者文风。 任何工作表都依赖输入质量、抽样边界、当地制度和责任人判断。CLI 不浏览、不抓取、不保存材料，也不能发现用户没有提供的隐私、权力或伤害信息。若任务进入高风险专业领域，应停止扩张本框架并路由到相应合格人员。

## 实际运行结果

- 运行日期：2026-08-16；
- 包级对抗测试：`10/10` 通过；
- Nuwa `quality_check.py`：`6/6` 通过；
- CLI 编译、JSON 确定性、Markdown 转义、重复值、超长值、提示注入、输出文件与包专属风险门均由测试覆盖；
- 测试全程离线且仅使用 Python 标准库。

这些结果验证的是仓库制品合同，不验证现实机制效果、来源当事事实或专业批准。
