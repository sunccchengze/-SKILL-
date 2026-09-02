# academic-research-skills（学术研究技能包）

> 来源：[Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) @ `94436237`（main，2026-09-02 装载，对应 v3.21.1）
> 协议：CC-BY-NC-4.0（见 `LICENSE`，非商业用途）

学术研究全流程技能包：**研究 → 写作 → 评审 → 修改 → 定稿**。

## 包含的 4 个技能

| 技能 | 用途 |
| --- | --- |
| `deep-research/` | 通用深度研究：13-agent 流水线，8 种模式（完整研究 / 快速简报 / 论文评审 / 文献综述 / 事实核查 / 三段式文献扫描 / 苏格拉底式引导研究 / 系统综述+meta 分析） |
| `academic-paper/` | 论文写作：大纲、逐章草稿、引用管理、写作质量检查 |
| `academic-paper-reviewer/` | 论文评审：多角色评审团、sprint 合同式审稿 |
| `academic-pipeline/` | 总编排：把研究→写作→评审→修改串成完整流水线 |

## 目录结构（保留上游仓库布局）

本目录**按上游仓库根目录的结构原样装载**，因为技能之间大量交叉引用（`shared/`、`scripts/`、`docs/`、`examples/`、`commands/`），拆散单个技能目录会破坏相对路径引用：

- `academic-paper/` `academic-paper-reviewer/` `academic-pipeline/` `deep-research/` — 4 个技能（各自含 `SKILL.md`、`agents/`、`references/`）
- `shared/` — 跨技能共享协议、契约（contracts）、模板、agent 提示词
- `scripts/` — 运行时脚本（文献检索 API 客户端、引文核验、流水线完整性检查等；**已移除 `test_*.py` 与 `legacy/`**）
- `docs/` — 架构、能力矩阵（`STAGE_CAPABILITY_MATRIX.md`）、设计文档
- `examples/` — 各模式的使用示例
- `commands/` — `/ars-*` 斜杠命令
- `agents/` — 插件暴露的 3 个 agent
- `.claude/` — 路由纪律（Routing Discipline）配置
- `.claude-plugin/` — 插件清单（plugin.json / marketplace.json）
- `CHANGELOG.md`、`MODE_REGISTRY.md`、`CITATION.cff`、`NOTICE.md` — 上游元信息
- `README.upstream.md` / `README.zh-CN.upstream.md` — 上游原始 README（含中文）

## 使用方法

1. **本目录即插件根**：所有相对引用（`shared/...`、`scripts/...`）都以本目录为基准。
   在 Claude Code 中使用：进入本目录启动会话，或把本目录整体作为项目根。
2. 触发方式：
   - 自然语言关键词（如「帮我做文献综述」「research the impact of …」「review my paper」）；
   - 斜杠命令 `/ars-research`、`/ars-paper`、`/ars-reviewer`、`/ars-pipeline` 等（见 `commands/`）。
3. 可选依赖：PDF 内容分类器需要 `pip install -r requirements-pdf-content-classifier.txt`（默认路径不依赖它）。

## 卸载

整个目录即全部足迹：`rm -rf skills/community/academic-research-skills`。
