# Tools of Titans｜TITAN-TRACE 个人实验工作台

这是一个可独立调用的 Nuwa deep-tier Skill。它保留 *Tools of Titans: The Tactics, Routines, and Habits of Billionaires, Icons, and World-Class Performers*（Tim Ferriss）的可用操作逻辑，但不做人物档案、名言集、补剂表或替代原书的摘要。

## 它解决什么

把一个候选做法依次转成：

`精确来源 → 声明类型 → 独立证据 → 可迁移性 → 安全门 → COM-B 瓶颈 → 低风险 N-of-1 → continue/change/stop`

默认中文；保留 `provenance`、`claim type`、`COM-B`、`N-of-1` 等必要英文术语。

## 最短调用

向 Agent 明确调用：

```text
请使用 book-tools-of-titans-experiment-lab。
我想改善：下午写作启动延迟。
候选：午饭后做十分钟无编辑草稿。
来源：我持有的纸书，第__页/___章节（或原始 URL/时间戳）。
边界：不涉及补剂、药物、禁食或危险训练。
请先做五字段声明账本与 COM-B 诊断，再判断 reject / park / research / low-risk trial；不要总结人物。
```

若没有精确定位，Skill 会标记 `locator missing`，不会凭记忆补引语。

## CLI：生成一页低风险实验卡

完整示例在 [`SKILL.md`](SKILL.md)。查看参数：

```bash
python3 scripts/build_experiment_card.py --help
```

输出到标准输出：

```bash
python3 scripts/build_experiment_card.py [参数...]
```

或保存为 JSON：

```bash
python3 scripts/build_experiment_card.py [参数...] --output titan-card.json
```

工具 **fail closed**。以下领域不会生成实验卡：医疗治疗、药物/补剂变化、极端禁食饮食、致幻剂/受控物质、急性心理健康危机、危险体能、高风险金融、违法行为。专业复核领域的方案应由合格专业人员设计；本工具不靠一个 `--approved` 开关解锁。

## 复盘调用

```text
请继续调用 book-tools-of-titans-experiment-lab 审查这张实验卡和日志。
不要新增 routine。按预注册阈值检查主结果、伤害、负担、缺失和偏离；至少比较真实机制、期待效应、回归均值、时间趋势和同期变化，最后只选 continue/change/stop 之一。
```

## 文件导航

- [`SKILL.md`](SKILL.md)：完整执行协议、七模型、TITAN-TRACE、安全门和输出契约
- [`references/source-notes.md`](references/source-notes.md)：来源功能与限制
- [`references/claim-layer-map.md`](references/claim-layer-map.md)：可审计声明图
- [`references/templates.md`](references/templates.md)：账本、实验卡、日志、复盘模板
- [`references/copyright-boundaries.md`](references/copyright-boundaries.md)：可做/不可做/转换策略
- [`references/research/`](references/research/)：六轮深研
- [`scripts/build_experiment_card.py`](scripts/build_experiment_card.py)：dependency-free 构建器
- [`tests/test_build_experiment_card.py`](tests/test_build_experiment_card.py)：安全和模式测试
- [`VALIDATION.md`](VALIDATION.md)：验收清单与命令

## 关键边界

本包不声称收录全书内容，也不把作者或受访者报告升级为独立证据。要理解叙事、人物上下文与完整论证，请使用合法原书；要判断健康/行为效果，请另查相应独立证据和专业指南。
