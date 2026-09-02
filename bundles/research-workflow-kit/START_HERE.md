# START HERE：交给新 Session 的完整说明

## 先运行

```bash
python3 tools/research_kit.py doctor
python3 tools/research_kit.py search "你的领域 交付物 方法 风险" --limit 20
python3 tools/research_kit.py list --profile core
```

只扫描清单元数据。不要一次读取数百个 `SKILL.md`。

## 新 Session 启动提示（可直接复制）

```markdown
你现在收到一个已解压的 `research-workflow-kit` 科研大礼包。

请先执行：

1. `python3 tools/research_kit.py doctor`
2. 阅读 `START_HERE.md`、`WORKFLOW.md`、`ETHICS.md` 和 `PLATFORM_COMPATIBILITY.md`
3. 只扫描 `MANIFEST.json` 与相关 Profile 的元数据
4. 根据我的具体课题，从当前阶段选择 1 个主 Skill 和最多 3 个互补 Skill
5. 完整阅读这些选中 Skill 的 `SKILL.md`，不要一次加载 `everything`

开始实质工作前，先提交“技能吸收与调用报告”：

- 元数据吸收：扫描了哪些 Profile/条目，如何结合本项目筛选；
- 完整阅读：实际打开了哪些 `SKILL.md`；
- 明确调用：每个 Skill 的准确 ID、选择理由、负责阶段和预期制品；
- 完整应用计划：关键步骤、人工门禁、验证命令/证据与失败回退；
- 本轮不调用：最接近的候选及不调用原因；
- 平台核验：哪些能力来自当前平台，哪些来自 Skill，哪些需要第三方 API/MCP/本地软件。

然后使用：

`python3 tools/research_kit.py init-project <项目目录>`

建立项目制品。默认中文工作，原始论文题名、检索式、变量名和引用信息保留原语言。

强制要求：

- 人类研究负责人批准研究问题、协议、数据、解释和发布；
- 检索记录数据库、完整查询、日期、筛选和纳排理由；
- PDF/OCR/表格抽取的关键数字回到原页核对；
- 每项核心 claim 可追踪到数据、图表、统计量或已核验来源；
- Notebook/脚本保存环境、输入版本、种子、配置、失败和从头运行证据；
- 论文写作只依据已批准的 claim-evidence map；
- 投稿前完成引用审计、独立模拟评审、复现、隐私/伦理/许可和 AI 披露检查；
- 不编造数据/引文/审批，不代写冒充，不规避 AI 检测，不保证发表，不自动投稿。

Skill 名不是通用命令。不得默认 `/research`、`/ars-*`、`$academic-research-suite`、`OPENCODE_ENABLE_EXA=1` 或任意 `npx skills add` 在当前 Arena/Codex/OpenCode 环境有效；先核验平台和包内 `compatibility` 字段。

每次阶段切换重新搜索和组队。交付时报告实际调用、制品、验证结果、偏差和剩余风险，而不是只重复计划。
```

## 推荐使用节奏

1. `core` 起步；
2. 进入文献、定量、质性、写作或 ML 阶段时切换相应 Profile；
3. 搜索元数据后只安装/读取必要条目；
4. 每个阶段通过人工门禁再继续；
5. `everything` 只作为离线 vault 和发现索引。

## 首轮研究者需要补充

- 学科/课题和研究类型；
- 当前阶段与已有材料；
- 数据敏感性、伦理审批和授权；
- 目标交付物、venue 和截止时间；
- 可用软件、API、MCP、计算预算和网络条件；
- 哪些决策必须由导师、PI、合作者或机构批准。
