# 🔬 科研大礼包 · Research Workflow Kit

一个可直接解压、离线检索、按 Profile 安装的科研 Skill 压缩包。它把研究问题、协议、文献与 PDF、引用管理、证据综合、Jupyter/统计/实验、质性与混合方法、论文写作、模拟同行评审、修订、复现、伦理与 AI 披露组织成一套**人工在环**工作流。

下载文件：[`research-workflow-kit.tar.gz`](research-workflow-kit.tar.gz)（52.6 MiB）  
完整清单：[`MANIFEST.json`](MANIFEST.json)（691 个入口；659 个 payload；32 个 metadata-only）  
校验值：[`SHA256SUMS`](SHA256SUMS)

## 三分钟开始

```bash
# 在压缩包和 SHA256SUMS 所在目录，必须先验 checksum
sha256sum -c SHA256SUMS
tar -xzf research-workflow-kit.tar.gz
cd research-workflow-kit
python3 tools/research_kit.py doctor
python3 tools/research_kit.py list --profile core
python3 tools/research_kit.py install --profile core --target "$HOME/.agents/skills" --dry-run
python3 tools/research_kit.py install --profile core --target "$HOME/.agents/skills"
python3 tools/research_kit.py init-project ./my-research-project
```

如果平台有不同的 Skill 目录，将 `--target` 改成该目录；不确定时不要猜，先让 Agent 检查平台文档和当前工作区。也可以不安装，直接让 Agent 阅读 `START_HERE.md`，再从 `vault/` 按当前阶段打开少量 `SKILL.md`。

## 它不是“一键论文机”

- 人类研究负责人批准问题、协议、数据、解释和发布；
- AI 不得编造论文、数据、受试者、引用、运行或伦理审批；
- 不提供 AI 检测规避、代写冒充、保证发表或自动投稿；
- Notion、Zotero、EndNote、SPSS、Word 等是可选连接器，Markdown/CSV/JSONL/BibTeX/Notebook 是可迁移底稿；
- `everything` 是离线资料库，不应一次全部加载或激活。

## Profile

| Profile | 用途 |
|---|---|
| `core` | 跨学科最小完整流程，推荐默认 |
| `literature-evidence` | 检索、PDF、引文、证据表、综述 |
| `quantitative` | 实验设计、功效、统计、Notebook、可视化 |
| `qualitative-mixed` | 访谈/观察、编码、反身性、mixed-method joint display |
| `writing-publication` | claim-evidence、论文、审稿、回复、格式与披露 |
| `ml-experiment` | AI/ML 研究工程和受限自动实验 |
| `life-science-vault` | 生物、医学、化学、材料等领域工具库 |
| `ars-noncommercial` | CC BY-NC 4.0 的 Academic Research Skills 与 Codex 适配器 |
| `everything` | 所有可再分发 payload；仅用于离线检索 |

`everything` 包含全部 659 个可再分发包，不代表依赖、安全或平台命令均已验证；应先搜索元数据，再为当前阶段选择至多 4 个互补 Skill。`MANIFEST.json` 另保留 32 个 metadata-only 入口，其中含 26 个精确重复别名和 6 个许可证未充分明确的包；它们不会被静默装入任何 payload。

## 可选“学长姐联合体”顾问层

来源归属透明的 `ai-research-senpai-council` 已作为可选 payload 纳入，但**不在 `core` 中**。它汇集 12 位中外科研创作者的已归因公开材料，用于经验会诊，不可替代学术证据、导师/PI、伦理审批或领域专家。单独预览安装：

```bash
python3 tools/research_kit.py install \
  --id 'skill-repository::ai-research-senpai-council' \
  --target "$HOME/.agents/skills" --dry-run
```

调用时必须按成员显示来源、证据强弱、分歧与商业关系，不得模仿真人或把通用建议冒充为其观点。

## 给新 Session 的一句话

```text
请先解压科研大礼包，运行 doctor，只扫描 MANIFEST 和 core 元数据；提交“技能吸收与调用报告”后，按当前研究阶段完整读取并调用最多 4 个互补技能，使用 project-template 维护制品和人工门禁。不要一次加载 everything，也不要把 Skill 名称当成未经核验的平台命令。
```

详见：[`START_HERE.md`](START_HERE.md)、[`INSTALL.md`](INSTALL.md)、[`WORKFLOW.md`](WORKFLOW.md)、[`ETHICS.md`](ETHICS.md)、[`PLATFORM_COMPATIBILITY.md`](PLATFORM_COMPATIBILITY.md)。
