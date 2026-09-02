# 孙承泽通用 Agent 技能库

> **先发现，再明确调用，再完整应用，再用证据交付。**

这是一个跨领域 Agent 工作底座：把分散的工程、研究、写作、设计、商业、安全与编排能力统一为可搜索、可追溯、可安装的技能库。它不把某个历史项目的事实强塞给新任务；使用者先理解目标项目，再从 **3,100 个默认可见候选**中组成最小、清晰、可验证的技能组。

- 🎁 第一次来：下载并阅读 [`Agent 新手大礼包`](bundles/newcomer-starter-pack/README.md)（恰好 100 项基础技能）
- 🔬 做科研：领取 [`科研大礼包`](bundles/research-workflow-kit/README.md)（659 个可再分发 payload、Profile 安装、人工门禁）
- 🧭 不知道选什么：打开 [`九大分类导航`](categories/README.md)
- 🔎 已有任务：运行 `python scripts/search_skills.py "帮我做XX" --intent`（意图识别模式）
- 📋 不知道选什么技能：打开 [`任务→技能路由手册`](TASK_ROUTING.md)
- 📦 要装到另一个 Agent：运行 `python scripts/install_skills.py --name <skill> --target /path/to/skills`
- 🧰 要用 OpenCut、RustDesk 或 Spec Kit：查看 [`工具安装与运行`](guides/TOOLS.md)

## 30 秒开始

```bash
# 1. 用自然语言描述任务（意图识别模式，推荐）
python scripts/search_skills.py "帮我做一个产品介绍视频" --intent --limit 10

# 2. 或按场景查阅 TASK_ROUTING.md 找到对应技能组合

# 3. 打开命中技能的 SKILL.md，明确记录调用了什么
# 4. 如需复制技能包
python scripts/install_skills.py --name systematic-debugging --target /path/to/skills

# 5. 交付前验证本仓库
python scripts/validate_repository.py
```

每项非琐碎任务都应**频繁检索、明确点名、充分使用**匹配技能。不能只说“参考了技能库”，也不能列一串名字却跳过技能要求的步骤。但“充分使用”是指完整执行**本轮选中的少数技能**，不是一次加载 100 项甚至 3,092 项；通常使用 1 个主技能，加研究、制作、审查各至多 1 个。

## 按需求找技能

| 你要做什么 | 建议入口 | 示例搜索 |
|---|---|---|
| 先判断应该用哪些能力 | [`universal-skill-router`](SKILL.md) | `task deliverable risks skill routing` |
| 计划、拆分或多 Agent 协作 | [Agent 与编排](categories/agents-orchestration/README.md) | `planning orchestration verification` |
| 开发、测试、调试、评审 | [工程与代码](categories/engineering-code/README.md) | `code test debug review architecture` |
| 做文档、PDF、数据库或分析 | [文档与数据](categories/documents-data/README.md) | `document data database analysis` |
| 做综述、实验、统计或论文 | [研究与科学](categories/research-science/README.md) | `literature review citation statistics` |
| 写作、改稿、内容生产 | [写作与内容](categories/writing-content/README.md) | `writing editing audience evidence` |
| 做 UI、网页、演示、图像或视频 | [设计与媒体](categories/design-media/README.md) | `design ui ux visual media` |
| 做产品、营销、运营或战略决策 | [商业与战略](categories/business-strategy/README.md) | `product strategy market decision` |
| 做安全、隐私、无障碍或合规审查 | [安全、隐私与合规](categories/security-compliance/README.md) | `security privacy compliance audit` |
| 跨领域生产力与项目卫生 | [通用生产力](categories/general/README.md) | `plan communicate productivity` |

搜索结果不等于执行授权。打开命中的 `SKILL.md`，核验来源、依赖、网络、凭据、文件写入、许可证和风险边界后再用。

## 九大分类：完整但不搬家

仓库采用**加法式分类索引**，不物理搬动数千个 canonical 包，因此原有链接、安装器、哈希和来源锁继续有效。每个分类都有面向人的 README 和包含全部默认候选的 `skills.tsv`。

| 分类 | 默认候选 | 主要能力 |
|---|---:|---|
| [研究与科学](categories/research-science/README.md) | 799 | 检索、综述、引用、实验、统计、论文、评审与复现 |
| [工程与代码](categories/engineering-code/README.md) | 767 | 架构、编码、测试、调试、Git、CI/CD、API 与性能 |
| [Agent 与编排](categories/agents-orchestration/README.md) | 383 | 路由、计划、记忆、评估、多 Agent 与工作流治理 |
| [设计与媒体](categories/design-media/README.md) | 307 | UI/UX、视觉系统、网页、演示、图像、视频与动效 |
| [通用生产力](categories/general/README.md) | 286 | 计划、沟通、会议、工具与跨领域生产力 |
| [文档与数据](categories/documents-data/README.md) | 175 | PDF、结构化文档、表格、数据库和分析交付 |
| [商业与战略](categories/business-strategy/README.md) | 154 | 产品、市场、营销、定价、竞争、运营与决策 |
| [安全、隐私与合规](categories/security-compliance/README.md) | 141 | 安全评审、风险、隐私、无障碍、审计与合规 |
| [写作与内容](categories/writing-content/README.md) | 88 | 中英文写作、编辑、内容研究、技术表达与文案 |

机器可读分类摘要：[`catalog/category-summary.json`](catalog/category-summary.json)。

## 🎁 Agent 新手大礼包（100 项）

[`bundles/newcomer-starter-pack/newcomer-starter-pack.tar.gz`](bundles/newcomer-starter-pack/newcomer-starter-pack.tar.gz) 是可直接解压、离线阅读的 100 项基础组合，包含独立技能包、`START_HERE.md`、完整 `MANIFEST.json` 与许可提醒；SHA-256 见 [`SHA256SUMS`](bundles/newcomer-starter-pack/SHA256SUMS)。完整逐项清单与用途见[礼包 README](bundles/newcomer-starter-pack/README.md)。

```bash
tar -xzf bundles/newcomer-starter-pack/newcomer-starter-pack.tar.gz
cd newcomer-starter-pack
less START_HERE.md
```

礼包强烈要求新会话中的工作者在开工前报告：

1. **如何消化/吸收**：扫描了哪些元数据，如何结合项目筛选，完整阅读了哪些技能；
2. **将明确调用什么**：准确技能名、选择依据、负责阶段和预期制品；
3. **将如何完整应用**：关键步骤、质量门禁、验证证据与失败回退；
4. **本轮不调用什么**：说明取舍，避免把 100 项同时塞入上下文。

阶段变化时重新搜索并明确换组；交付时必须回报实际执行和验证结果，而不是只重复计划。重建礼包：`python scripts/build_starter_bundle.py`。

## 🔬 科研大礼包 · Research Workflow Kit

[`bundles/research-workflow-kit/research-workflow-kit.tar.gz`](bundles/research-workflow-kit/research-workflow-kit.tar.gz) 是可直接领取的科研全生命周期离线包：691 个清单入口中有 659 个可再分发 payload，另保留 32 个有明确原因的 metadata-only 记录。它提供 `core`、文献证据、定量、质性/混合、写作发表、ML 实验、生命科学、非商业 Academic Research Skills 和 `everything` 九个 Profile，并附 33 个项目模板文件、Manifest 驱动安装器、树哈希验证与逐来源许可/归属。

```bash
cd bundles/research-workflow-kit
sha256sum -c SHA256SUMS
# 解压后仍要运行包级验证
tar -xzf research-workflow-kit.tar.gz
cd research-workflow-kit
python3 tools/research_kit.py doctor
python3 tools/research_kit.py verify
python3 tools/research_kit.py install --profile core --target /真实/skills/目录 --dry-run
```

它不是“一键论文机”：问题、协议、数据权限、方法、解释和发布均有人类门禁；禁止伪造引用/数据/审批、代写冒充、检测规避与自动投稿。新 Session 必须先读 [`START_HERE.md`](bundles/research-workflow-kit/START_HERE.md)，提交“技能吸收与调用报告”，每阶段只完整读取并明确调用少量互补技能。精确领取、校验、安装和项目初始化方法见[礼包安装文档](bundles/research-workflow-kit/INSTALL.md)，本次 clean-room 结果见[验证记录](bundles/research-workflow-kit/VALIDATION_RESULT.md)。重建命令：`python scripts/build_research_bundle.py`。

## 五个本地工具

工具运行时与技能入口统一放在 `tools/`，上游源码固定为 Git 子模块，日常依赖和二进制不提交。

| 工具 | 入口 | 用途 |
|---|---|---|
| [OpenCut](tools/opencut/SKILL.md) | `tools/opencut/` | 本地浏览器视频编辑器 |
| [OpenWiki](tools/openwiki/SKILL.md) | `tools/openwiki/` | 面向 Agent 的 Markdown Wiki 生成器 |
| [RustDesk](tools/rustdesk/SKILL.md) | `tools/rustdesk/` | 经明确授权的原生远程桌面 |
| [ScreenCoder](tools/screencoder/SKILL.md) | `tools/screencoder/` | 截图转可编辑 HTML/CSS |
| [GitHub Spec Kit](tools/spec-kit/SKILL.md) | `tools/spec-kit/` | specification-driven development |

```bash
# OpenCut + Spec Kit + RustDesk 源码
bash scripts/setup_tools.sh all

# 运行 OpenCut
HOST=0.0.0.0 PORT=5173 bash scripts/run_opencut.sh

# 核验源码与已安装 CLI
bash scripts/verify_tools.sh
```

RustDesk 是需要桌面会话、系统动态库和授权连接的原生应用，不是浏览器 Live Preview。官方包下载受阻时必须明确报告“源码已固定、二进制未装”，不能换用未验证镜像或把 gitlink 当作可运行 GUI。完整说明与提供本地官方 `.deb` 的安装方式见 [`guides/TOOLS.md`](guides/TOOLS.md)。

## 仓库如何组织

```text
AGENTS.md                         Agent 指令层级与最小技能组规则
SKILL.md                          通用技能路由器（意图识别）
TASK_ROUTING.md                   任务→技能路由手册（100+ 场景映射）
README.md                         公共入口（本页）

bundles/                          新手大礼包 + 科研大礼包
  newcomer-starter-pack/          100 项礼包、清单、压缩包和校验和
  research-workflow-kit/          科研大礼包、Profiles、模板、安装/验证 CLI

categories/                       九大加法式分类导航
  <category>/README.md            分类说明与代表入口
  <category>/skills.tsv           该类全部默认可见技能

skills/                           技能库主体
  core/                           核心路由器与系统级技能（6 项）
  community/                      社区贡献的完整技能包（50+ 项）
  variants/                       同名但正文不同的轻量变体（17 项）
  research-workflow-kit/          科研工作流专项技能（6 项）

tools/                            内置工具的运行时与技能入口
  opencut/                        浏览器视频编辑器
  openwiki/                       Agent Wiki 生成器
  rustdesk/                       原生远程桌面
  screencoder/                    截图转 HTML/CSS
  spec-kit/                       规范驱动开发

catalog/                          统一目录、来源锁、重叠策略、分类摘要
scripts/                          搜索、安装、分类、打包、校验与重建工具
guides/                           使用、科研、官方/精选来源与工具指南
governance/                       宪法、多 Agent 与质量门禁

full-sources/                     固定提交的完整上游仓库（Git 子模块）
  aggregate-*                     三个历史技能库
  official/                       OpenAI、Vercel、Microsoft 官方发布方来源
  research/                       11 个科研来源
  curated/                        用户指定与两轮精选来源
  tools/                          OpenCut、RustDesk、GitHub Spec Kit
full-library/                     可选的本地全量物化并集（忽略，不提交）
third_party/                      上游 README、许可证与归属说明
tests/                            仓库验证测试
```

## 数据层、来源与去重

本仓库保留完整来源，同时让日常搜索保持轻量：

1. **紧凑层**：本地 `skills/` 与工具内技能，适合立即搜索和安装；
2. **官方来源层**：OpenAI Plugins、历史 OpenAI Skills、Vercel Agent Skills、Microsoft Skills；“官方”只表示发布方来源，不表示许可证相同；
3. **科研层**：11 个固定科研项目，覆盖选题、综述、实验、统计、科学计算、论文、审稿与复现；
4. **精选层**：用户指定来源，加两轮各恰好 10 项的月度增长审计；
5. **全量源层**：`full-sources/` 保留上游 references、scripts、assets、示例和其他文件。

四个机器目录当前共有 **3,758 个原始入口**。默认搜索隐藏正文变体和 45 个已审计的包装/继任/宿主别名，呈现 **3,100 个主候选**；需要时使用 `--include-variants` 或 `--include-aliases` 展开。不同实现不会只因同名就被删除。

- 来源与提交：[`catalog/sources.lock.json`](catalog/sources.lock.json)
- 重叠规则：[`catalog/overlap-policy.json`](catalog/overlap-policy.json)
- 官方来源边界：[`guides/OFFICIAL_SOURCES.md`](guides/OFFICIAL_SOURCES.md)
- 科研工作流：[`guides/RESEARCH.md`](guides/RESEARCH.md)
- 精选审计：[`guides/CURATED_SOURCES.md`](guides/CURATED_SOURCES.md)

## Agent 默认工作法

1. **读项目**：确认目标、事实、受众、交付格式、现有指令和不可改变项。
2. **写简报**：列输入、输出、约束、证据标准、风险和验收命令。
3. **搜技能**：元数据优先，通常查看 12 个候选以内。
4. **最小组队**：1 个主技能，至多 3 个互补技能；明确每项职责和制品契约。
5. **完整执行**：真正落实选中技能的关键步骤，不选择性跳过质量门禁。
6. **验证交付**：运行测试、检查页面/文件/数据/引用，记录命令和结果。
7. **回报使用**：说明实际调用的技能、证据、偏差、未验证项和下一步。

重要决策可调用 [`ai-cabinet-decision-making`](skills/core/ai-cabinet/SKILL.md)，并行工作可调用 [`multi-agent-orchestration`](skills/core/multi-agent-orchestration/SKILL.md)；快速简单问题不要为了形式启动内阁或多 Agent。

## 初始化、重建与验证

```bash
# 只初始化当前需要的来源（推荐）
git submodule update --init full-sources/tools/spec-kit

# 或取得全部上游文件
git submodule update --init --recursive

# 物化全量本地并集（full-library/ 不提交）
python scripts/materialize_full_library.py

# 重建目录与导航
python scripts/build_catalog.py
python scripts/build_official_catalog.py
python scripts/build_curated_catalog.py
python scripts/build_categories.py
python scripts/build_starter_bundle.py
python scripts/build_research_bundle.py

# 完整验证与测试
python scripts/validate_repository.py
python -m unittest discover -s tests -v
```

## 许可证、安全与责任

第三方技能和工具各自遵循其上游许可证；本仓库的整理、分类、路由和打包不改变任何上游权利声明。OpenCut 与 Spec Kit 固定提交采用 MIT；RustDesk 固定提交采用 AGPL-3.0。部分历史聚合集合没有可发现的集合级许可证，使用与再分发前必须逐项核验。详见 [`third_party/NOTICE.md`](third_party/NOTICE.md)。

任何涉及远程控制、凭据、网络、文件写入、个人数据、受版权素材、医疗/法律/财务判断、实验、引用或生产部署的技能，都必须取得相应授权、保留数据与来源血缘、执行独立验证，并明确报告未验证边界。
