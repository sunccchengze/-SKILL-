# 《第五项修炼》学习系统 Skill

Nuwa deep-tier 的中性书籍蒸馏包。它保留 Peter Senge《第五项修炼》的五项修炼与系统视角，但不把管理隐喻包装成因果证明；原书、方法谱系、后续证据/批评和本 Skill 创建的 LOOPS 工作流始终分层。

## 适用与路由

适合：反复救火、局部 KPI 优化却整体恶化、增长上限、延迟副作用、心智模型冲突、共同愿景或团队学习失效。

不要单独使用：紧急安全/违法/骚扰/欺诈事项（先保护、留证、报告、履责）；简单可复现局部故障（先做直接根因分析）；效应量、概率、预测日期（需定量设计/仿真）；强迫员工认同既定“共同愿景”。

## 认识论合同

| 层 | 是什么 | 不能说成什么 |
|---|---|---|
| A | 《第五项修炼》的五项修炼、学习障碍与整合框架 | 普适组织因果定律 |
| B | Senge 其他材料或明确的作者邻近材料 | 原书逐字主张 |
| C | 系统动力学、GMB、模型验证、测量与权力批评 | Senge 独创或跨行业效果证明 |
| D | 本 Skill 创建的 LOOPS、模板、门禁和 CLI | 原作者的方法或已验证量表 |

24 条可追踪声明见 [`references/claim-layer-map.md`](references/claim-layer-map.md)，来源的支持/不支持边界见 [`references/source-notes.md`](references/source-notes.md)。

## 快速调用

```text
请显式使用 book-fifth-discipline-learning-system。
按 LOOPS 区分事实、原书、系统动力学谱系、后续证据和 Skill 综合；
固定时间范围与边界，画行为随时间，给回路/时滞/竞争解释/图外变量，
同时保留责任与权力分析，并设计一个可逆、可测、有停止条件的探针。
```

## CLI

从本包根目录运行：

```bash
python3 scripts/map_learning_system.py \
  --problem "版本越赶返工越多" --horizon "12 周" \
  --variable "发布压力" --variable "测试时间" --variable "返工量" \
  --delay "延迟缺陷约两周后显现" \
  --assumption "压缩测试能追回进度" \
  --evidence "发布日志与缺陷回流" \
  --stakeholder "测试人员" \
  --risk-level moderate --owner "工程负责人" \
  --stop-condition "严重缺陷或人员负荷越界" \
  --source-layer D --format json --output /tmp/loops.json
```

最低要求：非空 problem/horizon、2–8 个唯一 variable、1–8 个唯一 assumption。`--delay`、`--evidence`、`--stakeholder` 可重复；`--format` 为 `markdown|json`，`--output` 可省略并输出 stdout。

高风险时必须同时给 `--owner` 与 `--stop-condition`；成功也只生成 `analysis_only` 假设工作表，不是处置、调查或批准。输入仅作为数据，Markdown 表格会转义用户文本。

## LOOPS 产物

1. **Limit**：先行安全/法律/责任检查与边界；
2. **Locate**：可观察的重复结果与受影响者；
3. **Observe**：行为随时间、数据质量和三类时滞；
4. **Outline**：闭环、箭头证据、反驳条件，不把单箭头当反馈；
5. **Probe**：基模匹配与不匹配、竞争解释、图外变量、目标定义权；
6. **Select**：一个小规模可逆探针、事前预测、伤害指标和停止条件。

完整可执行表单见 [`references/templates.md`](references/templates.md)；六轮研究见 [`references/research/`](references/research/)；包级与仓库级命令见 [`VALIDATION.md`](VALIDATION.md)。

## 关键边界

- 因果环图是待检验共同理论，不是因果证明或效应量；
- 基模只负责发问，必须写不匹配与推翻观察；
- “系统造成”不能取消个人/机构责任、权利与伦理；
- 参与、对话或共识不自动证明公平，必须检查谁能改图、拒绝和承担成本；
- 未实现 stock-flow、方程、参数、敏感性分析或仿真；
- 干预须有限、可逆、可测，保留原图和判断更新日志。

## 验证

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 ../../nuwa-skill/scripts/quality_check.py SKILL.md
```

从 [`SKILL.md`](SKILL.md) 开始完整执行，不要只引用书名或基模标签。
