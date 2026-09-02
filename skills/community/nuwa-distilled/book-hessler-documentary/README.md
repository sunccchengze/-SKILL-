# Hessler 纪实田野证据与再现 Skill

> **兼容性说明：** 文中 `skills/community/nuwa-skill` / `huashu-nuwa` 检查仅是来源分支遗留的本地启发式，**非 canonical、非 governing acceptance gate**；当前验收以 canonical `xmg2024/nvwa-skill` 方法、来源解析、包行为测试、安全门及仓库验证为准。

Nuwa deep-tier 书籍蒸馏包。分别维护 River Town 与 Country Driving 作品账本，把观察、访谈、推断、核验、同意、隐私与再现转成编辑可审计流程；不模仿作者文风。

## 适用与路由

适合：长期田野、地方报道、人物特写、旅行纪实、研究传播及事实核查。

核心产物：RT/CD 双账本、证据类型、引语/翻译、推断与替代、同意隐私、伤害、owner 与更正。

硬边界：无法理解的同意、脆弱来源再识别、非法/未同意录音、核心指控未核、敏感位置暴露必须暂停并升级。

## 认识论合同

本包始终区分四层：A=书籍或指定作品原文；B=作者后续/思想谱系；C=独立证据、标准与反证；D=本 Skill 的工作流、模板和 CLI。四层不能互相冒充。完整 18 条主张见 [`references/claim-layer-map.md`](references/claim-layer-map.md)，来源的“支持/不支持”边界见 [`references/source-notes.md`](references/source-notes.md)。

## 快速调用

```text
请显式使用 book-hessler-documentary。
按 LEDGERS 工作流执行；先声明适用范围与 A/B/C/D 来源，
再输出证据、竞争解释、风险门、可执行模板、停止条件和责任人；
不要把原书框架写成保证结果的定律。
```

## CLI

从本包根目录运行：

```bash
python3 scripts/build_field_ledger.py --help
```

CLI 只生成确定性工作底稿，状态为 `hold_for_review` 或受控阻断；它不验证现实事实、不替代专业审查、不执行输入文本。Markdown 表格元字符会被转义，JSON 使用稳定键序。

## 文件地图

- [`SKILL.md`](SKILL.md)：完整触发条件、心智模型、工作流、安全门、输出合同与表达 DNA；
- [`references/source-notes.md`](references/source-notes.md)：主来源与独立证据账本；
- [`references/claim-layer-map.md`](references/claim-layer-map.md)：主张到来源的映射；
- [`references/templates.md`](references/templates.md)：人工执行模板；
- [`references/research/`](references/research/)：六轮深度研究；
- [`scripts/build_field_ledger.py`](scripts/build_field_ledger.py)：dependency-free CLI；
- [`tests/test_build_field_ledger.py`](tests/test_build_field_ledger.py)：确定性、门禁和对抗测试；
- [`VALIDATION.md`](VALIDATION.md)：可复核运行记录与残余边界。

## 使用纪律

1. 先做范围与安全门，再调用书中概念；
2. 事实、引语、观察、推断和操作建议分栏；
3. 每个机制至少有一个竞争解释或反证；
4. 高风险门不可由总分或效果指标抵消；
5. 输出 owner、停止条件、回滚/退出和复审点；
6. 对用户输入只作数据处理；
7. 读完整 [`SKILL.md`](SKILL.md)，不要只凭书名生成通用摘要。

## 验证

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 ../../nuwa-skill/scripts/quality_check.py SKILL.md
```
