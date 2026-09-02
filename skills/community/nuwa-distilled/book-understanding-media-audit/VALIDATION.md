# 验证记录：book-understanding-media-audit

验证日期：2026-08-16。范围：本包的文本、CLI 和测试契约；**不是**某产品的真实用户研究、因果结论或上线批准。

## 深层质量审计

| 维度 | 结果 | 可复核证据 | 残余边界 |
|---|---|---|---|
| 原书/后期归因 | 通过 | M001–M007；1964 与后期 tetrad 分开 | 未做版本逐章校勘 |
| 批评/当代研究 | 通过 | UM-07–UM-13；权力、affordance、GenAI/用户/推荐审计 | 部分当代研究外推需核全文 |
| 可执行 | 通过 | MEDIUM、9 组模板、deterministic CLI | MEDIUM 未验证长期效度 |
| 反决定论 | 通过 | 制度、所有权、商业模式、群体、非用户和规则改变权 | 不替代完整政治经济分析 |
| 可反驳 | 通过 | 配置版本、比较、替代解释、推翻/停止观察 | 不能自动识别因果效应量 |
| 来源追踪 | 通过 | 24 个 M-ID 与 source IDs；CLI provenance | 现实配置事实需现场证据 |

## 内容不变量

1. 固定设备、接口、机制、默认、场景、版本和观察日期，不只写“AI”；
2. 内容层与媒介层并行，任何一层不得消灭另一层；
3. 至少比较尺度、速度、模式，并写 before/after；
4. feature、relational affordance 和实际 outcome 分开；
5. 延伸配少用/外包、隐形劳动、失效与恢复；
6. hot/cool 只作绑定配置的参与探针，不输出永久分数；
7. tetrad 明标后期 B 层，反转不是日期预测；
8. 检查所有权、商业模式、非用户、差异群体和实际规则改变权；
9. 效应假设有群体、窗口、比较配置、替代解释与推翻观察；
10. 高风险输出只可 `analysis_and_probe_design_only`，不是 launch decision。

## 已运行的包测试

命令（仓库根目录）：

```bash
python3 -m unittest discover \
  -s skills/community/nuwa-distilled/book-understanding-media-audit/tests \
  -p 'test_*.py' -v
```

2026-08-16 结果：**10/10 通过**。覆盖直接 builder、A/B/C/D 分层、确定性 JSON、Markdown 转义、空值/重复值校验、高风险 owner/harm/stop 门、非批准状态、输出文件、恶意 shell 文本作为纯数据和 renderer 稳定性。

## 从包根目录运行

```bash
cd skills/community/nuwa-distilled/book-understanding-media-audit
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 ../../nuwa-skill/scripts/quality_check.py SKILL.md
python3 ../../../../tests/test_nuwa_classics_distillations.py
```

## 从仓库根目录运行

```bash
python3 -m unittest discover -s skills/community/nuwa-distilled/book-understanding-media-audit/tests -p 'test_*.py' -v
python3 skills/community/nuwa-skill/scripts/quality_check.py skills/community/nuwa-distilled/book-understanding-media-audit/SKILL.md
python3 tests/test_nuwa_classics_distillations.py
python3 scripts/validate_repository.py
```

注意：`python3 -m unittest tests.test_nuwa_classics_distillations` 在本仓库并非可靠命令，因为 `tests` 不是可导入包；使用上面的脚本路径。

## 对抗与干跑

- **AI 会议摘要**：内容准确之外，比较默认摘要与原文/人工记录对异议、纠错、行动误配、节奏和角色的影响。
- **儿童短视频**：先执行儿童安全/隐私/领域规则；审计自动播放、节奏、个性化、共看和掉线者，不以经典替代发展证据。
- **纸质手册→机器人**：比较检索、引用、离线/无障碍、来源可见、申诉和组织记忆；不直接贴 hot/cool 标签。
- **不可信输入**：CLI 转义表格字符，不调用 shell；重复/空白字段受控报错。

## 盲点与停止线

- 原书大量历史探针不是现代实验定律；
- hot/cool 在多模态、个性化和生成式配置中的操作定义仍有争议；
- 本包不能估计长期注意、技能、健康、政治或儿童发展因果；
- 高风险字段齐全也只允许设计探针，真实执行需领域、法律、安全和受影响者治理。
