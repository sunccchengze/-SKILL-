# 精选来源、月度 Star 增速与运行边界

本层固定 22 个经过路径、许可证、包边界与明显执行风险核验的技能包：用户指定的 CyberPPT、figures4papers，第一轮 **恰好 10 个**近一个月高速增长项，以及再次寻宝后 **新增且仅新增 10 个**增长项。机器目录为 [`catalog/curated-skills.json`](../catalog/curated-skills.json)，精确提交、Git tree、入口、Blob 与审计快照见 [`catalog/sources.lock.json`](../catalog/sources.lock.json)。

## 用户指定来源

| 来源 | 固定提交 | 精选入口 | 许可证状态 | 用途 |
|---|---|---|---|---|
| [`crazyykhllc-bit/CyberPPT`](https://github.com/crazyykhllc-bit/CyberPPT) | `980e5576565f0673c67ee41b01d20ed66cb8417c` | `SKILL.md` | MIT | 从文档、报告和数据生成可编辑的咨询风格 PPTX，并做渲染质检 |
| [`ChenLiu-1996/figures4papers`](https://github.com/ChenLiu-1996/figures4papers) | `6790a93af3552539d955d77181c818916e1700b7` | `scientific-figure-making/SKILL.md` | **NOASSERTION** | 科学图表设计、演示、教程和通用模式 |

figures4papers 的固定提交没有发现 LICENSE 或明确仓库许可证。这里的固定与索引不授予额外权利；复制、修改、再分发或商业使用前应向上游核实权限。

## 近一个月高速增长：第一轮最终 10 项

审计窗口为 **2026-07-14 至 2026-08-14**。下列仓库全部在窗口内创建，因此审计时的总 Star 都是在该窗口内获得的；`Stars` 是 2026-08-14 通过 GitHub Repository API 记录的可复核快照，不是未来增长承诺。我们同时读取递归 Git tree、精确 `SKILL.md`、引用文件、脚本边界和许可证文本，再按工作流完整性、差异化能力、质量门禁、可安装边界及明显安全风险筛选。

| # | 精选技能（来源） | 创建时间（UTC） | Stars | 许可证 | 为什么入选 |
|---:|---|---|---:|---|---|
| 1 | `convert-documents-to-markdown` — [`firecrawl/anydoc`](https://github.com/firecrawl/anydoc) | 2026-08-03 | 15,601 | MIT | Word、PowerPoint、Excel、OpenDocument、EPUB、CSV、PDF 到 Markdown 的紧凑执行入口 |
| 2 | `img2threejs` — [`img2threejs/img2threejs`](https://github.com/img2threejs/img2threejs) | 2026-07-15 | 11,572 | Apache-2.0 | 从参考图到程序化 Three.js 模型，带状态机、多视角证据和有界修正循环 |
| 3 | `video-shotcraft` — [`Vincentwei1021/video-shotcraft`](https://github.com/Vincentwei1021/video-shotcraft) | 2026-07-19 | 4,930 | Apache-2.0 | 基于镜头卡、Remotion、真实页面截图、音效与整片复核的产品视频流程 |
| 4 | `simple-english` — [`AminBlg/SimpleEnglish`](https://github.com/AminBlg/SimpleEnglish) | 2026-07-21 | 2,288 | MIT | 面向技术文档和国际读者的受控英语规则、检查表与用例 |
| 5 | `design-evaluation` — [`SeanJ1ang/design-judge-skills`](https://github.com/SeanJ1ang/design-judge-skills) | 2026-07-18 | 1,174 | Apache-2.0 | 透明、证据驱动的设计分类、评分、风险和展示质量评估 |
| 6 | `slides` — [`stackblitz/bolt-slides`](https://github.com/stackblitz/bolt-slides) | 2026-07-14 | 698 | MIT | 可响应、可访问、有导航与构建动画的 React Web 演示文稿工程 |
| 7 | `sssf` — [`disler/super-simple-software-factory`](https://github.com/disler/super-simple-software-factory) | 2026-08-02 | 622 | MIT | 可重复的 Agent + 代码工作流、类型化交接、写入边界和可观测性 |
| 8 | `trace-file-lineage` — [`uczltw6/trace-file-lineage`](https://github.com/uczltw6/trace-file-lineage) | 2026-07-29 | 512 | MIT | 本地文件来源、上下游影响、任务历史、搜索与隐私脱敏 |
| 9 | `qiaomu-seo` — [`joeseesun/qiaomu-seo`](https://github.com/joeseesun/qiaomu-seo) | 2026-08-03 | 364 | MIT | 技术 SEO、内容、迁移、国际化、搜索平台和 AI 搜索的证据化工作流 |
| 10 | `high-stakes-analytics-decision-lab` — [`limingrui679-design/high-stakes-analytics-decision-lab`](https://github.com/limingrui679-design/high-stakes-analytics-decision-lab) | 2026-07-29 | 349 | MIT | 为高后果决策提供从描述到处方分析、数据质量、溯源和不确定性门禁 |

`design-judge-skills` 的上游仓库共有七个 `SKILL.md`，但本层只选择、索引、安装和物化 `skills/design-evaluation/SKILL.md`，避免用六个未经本轮选定的相邻入口突破“恰好 10 个”配额。完整上游仓库仍作为固定 Git 子模块保留，以便核验提交与许可证。

## 再次寻宝：新增且仅新增 10 项

第二轮继续使用 **2026-07-14 至 2026-08-14** 这一可复核窗口。GitHub 查询命中 1,323 个窗口内创建且至少 100 Stars 的仓库；许可证初筛与递归树扫描后，对 31 个仓库中的 232 个 `SKILL.md` 逐个读取，并核对所选入口的完整包、脚本、依赖、法律文件和精确 Blob。最终 10 项的审计时 Stars 合计 **67,998**。它们都在窗口内创建，因此下表总 Stars 是月内增长的保守下界，而不是对未来热度的承诺。

| # | 新增技能（来源） | 创建时间（UTC） | Stars | 许可证 | 为什么入选 |
|---:|---|---|---:|---|---|
| 1 | `record-browser-gif` — [`deepseek-ai/deepseek-harness`](https://github.com/deepseek-ai/deepseek-harness) | 2026-08-13 | 34,181 | MIT | 把真实分支、真实服务和浏览器步骤录成带提交溯源、时长控制与编码复核的 GIF 证据 |
| 2 | `popular-web-designs` — [`yc-software/qm`](https://github.com/yc-software/qm) | 2026-07-29 | 13,405 | MIT | 54 套可检索网页设计参考，给出可落地的颜色、排版、组件、响应式和验证规则 |
| 3 | `better-accessibility` — [`trycompai/crm`](https://github.com/trycompai/crm) | 2026-07-31 | 8,382 | MIT | 从语义、键盘、焦点、表单、命中区、缩放、动画到读屏器的代码审计与修复清单 |
| 4 | `bento-slides` — [`nyblnet/bento`](https://github.com/nyblnet/bento) | 2026-07-17 | 3,974 | MIT | 以单文件 JSON 文档生产交互式 HTML 演示，覆盖图表、Morph、状态页、动效与逐页目检 |
| 5 | `change-traceability-review` — [`QoderAI/better-harness`](https://github.com/QoderAI/better-harness) | 2026-07-21 | 1,828 | MIT | 用 issue、规格、提交、分支和 diff 证据复核改动意图、覆盖与可追溯性 |
| 6 | `oil-motion` — [`oil-oil/oil-motion`](https://github.com/oil-oil/oil-motion) | 2026-08-07 | 1,675 | MIT | 从 Motion Brief、关键帧和质量门到网页图集/绿幕视频优化与多格式交付的完整动效流水线 |
| 7 | `story-to-handdrawn-video` — [`gnipbao/story-to-handdrawn-video`](https://github.com/gnipbao/story-to-handdrawn-video) | 2026-07-21 | 1,357 | MIT | 将故事或本地图页变成手绘 Remotion 视频，带 20 种风格、分镜校验、预览和最终渲染 |
| 8 | `novel-outline` — [`eternityspring/shuohao-skills`](https://github.com/eternityspring/shuohao-skills) | 2026-08-06 | 1,282 | Apache-2.0 | 长篇小说分卷、集、节拍、资产和质量门的分层大纲流程，附零依赖校验与可视报告 |
| 9 | `ai-copywriter` — [`mikiarlo3/ai-copywriter`](https://github.com/mikiarlo3/ai-copywriter) | 2026-07-24 | 971 | MIT | 读者优先的营销文案、微文案和自然语言编辑，明确禁止虚构数据、伪造证明和暗黑模式 |
| 10 | `human-review` — [`petergyang/human-review`](https://github.com/petergyang/human-review) | 2026-07-27 | 943 | MIT | 在回环地址浏览器中让人直接批注 HTML、Markdown 或本地页面，再结构化交还修改意见 |

第二轮采用内容级“新增”门禁：每个所选 `SKILL.md` 的 SHA-256 必须与快索引层、用户指定项、第一轮及本轮其他入口不同。初选的 `KKKKhazix/human-writing` 与仓库既有直接来源同为提交 `4fda173f3fef7fb808f3eba991eeb2528ea4b189`，入口内容也逐字节相同，因此被剔除并由 `ai-copywriter` 替换；最终配额仍严格停在 10。校验器会重新计算这项去重门禁，防止以后把相同技能换一个路径重复计数。

## 能力重叠检查

- `slides` 生产运行中的 React 演示站点；CyberPPT 生产可编辑 PPTX，交付介质不同。
- `design-evaluation` 是评价与证据评分器；现有 `victor-design` 主要承担设计生产。
- `simple-english` 是受控技术英语，不替代通用中文/英文创作技能。
- `trace-file-lineage` 处理本地制品血缘；`high-stakes-analytics-decision-lab` 处理决策分析与数据证据链。
- `anydoc` 做格式转换；figures4papers、CyberPPT 和视频技能做下游视觉交付。
- `bento-slides` 生产可编辑单文件交互式 deck；第一轮 `slides` 是 React 演示站点，CyberPPT 则交付 PPTX。
- `popular-web-designs` 提供 54 套实现参考，`better-accessibility` 承担无障碍审计；它们都不替代 `victor-design` 的原创视觉生产或 `design-evaluation` 的评分职责。Hermes 中同布局的 `popular-web-designs` 是宿主适配包，默认搜索以本轮审计过的 QM 精选包为 canonical；Hermes 路径仍可用 `--source hermes-agent` 显式安装。
- `change-traceability-review` 核对规格、提交与 diff 意图；`trace-file-lineage` 追踪文件制品来源，证据对象不同。
- `oil-motion` 解决网页动效与视频/图集优化，`story-to-handdrawn-video` 解决手绘叙事，第一轮 `video-shotcraft` 解决产品宣传片。
- `novel-outline` 只负责长篇结构与质量门；`ai-copywriter` 聚焦真实、读者优先的营销和微文案；既有 `human-writing` 与 `simple-english` 分别偏中文创作和受控技术英语。
- `human-review` 是人机评审批注通道，`record-browser-gif` 是可追溯演示证据工具；两者都不是另一个写作或视频制作技能。

这些边界和内容哈希门禁保证第二轮新增项补充能力，而不是仅凭 Star、仓库名或路径重复已有技能。

## 静态安全与执行审计

固定或搜索技能**不会自动执行上游脚本**。初始化子模块只取得固定源码；真正运行技能前仍需审查当前任务会触发的命令。静态审计未发现要求上传任意凭据、绕过用户授权或无条件删除用户数据的提示，但不同技能具有以下显式能力边界：

### 第一轮 10 项

| 技能 | 网络、凭据与依赖 | 写入或高影响边界 |
|---|---|---|
| `convert-documents-to-markdown` | 指示 `npx -y @firecrawl/anydoc`，会从 npm 取得可执行包；托管 OCR 是另一个外部 API | 只应处理用户授权文件；需要更强供应链复现性时先固定 npm 版本 |
| `img2threejs` | 核心 Forge 流程以本地 Python 为主；可选视觉/网格适配器会下载模型或使用 Hugging Face 凭据；仓库维护脚本可使用 GitHub token | 在项目/状态目录生成模型、证据与渲染；不要把维护脚本当成建模必需步骤 |
| `video-shotcraft` | 使用 npm/Remotion、浏览器与 ffmpeg；样片拉取脚本会联网 | 生成截图、音频和渲染制品；发布、外部截图和安装依赖前确认授权 |
| `simple-english` | 无运行脚本或必需网络 | 文本改写；保留技术含义并由人复核安全警示 |
| `design-evaluation` | 精选包脚本为本地 Python/JSON 数据处理，无必需网络 | 生成评分和批量评估；不能把“奖项对齐”写成官方评审或获奖预测 |
| `slides` | 完整模板需要 npm/Vite/React | 安装器保留仓库级运行脚手架；发布或替换现有站点前确认目标范围 |
| `sssf` | Agent 阶段可调用模型提供方并读取相应 API key；代码阶段可运行配置的命令 | `bash`、Git checkout 和写文件本质上是高权限能力；必须收紧 `writes`、保护路径、预算和人工门禁 |
| `trace-file-lineage` | 核心扫描是本地的；可调用 Git、OCR 和平台元数据工具 | 默认不跟随外部符号链接并脱敏命令；`run` 会执行用户给出的子命令，导出到外部 Obsidian 路径需显式指定 |
| `qiaomu-seo` | 当前平台规则需要重新打开官方网页；本地校验器无需网络 | 审计默认只读；提交 URL、改索引控制、发布、删页和第三方联系必须显式授权 |
| `high-stakes-analytics-decision-lab` | 核心分析本地运行；真实数据示例支持 HTTPS 下载并带 SSRF/重定向限制 | 可生成案例、报告和清洗数据；高后果结论必须保留来源、不确定性、人工决策和回滚边界 |

### 第二轮新增 10 项

| 技能 | 网络、凭据与依赖 | 写入或高影响边界 |
|---|---|---|
| `record-browser-gif` | 需要现有浏览器控制能力、Python、`ffmpeg`/`ffprobe`；真实演示可读取应用正常使用的 API key，但要求不回显、不另装驱动 | 会启动真实分支服务、调用可能计费的真实模型、截取页面并写入帧/GIF；必须先清除敏感信息、确认成本和精确提交 |
| `popular-web-designs` | 包内只有 Markdown；建议用本地 HTTP、`curl` 与 headless Chromium 目检成品 | 会根据参考写网页；参考是设计语言证据，不是复制第三方商标、文案或受保护素材的授权 |
| `better-accessibility` | 包内没有运行脚本或必需网络；最终结论仍需真实浏览器、键盘及目标读屏器验证 | 可修改用户代码；先审计再做最小修复，不能只凭静态清单宣称合规 |
| `bento-slides` | 新建 deck 会从 `bento.page` 下载最新运行时和 schema；现有文件可能内含协作私钥或邀请凭据 | 只改 `#bento-doc` JSON 块；发现协作密钥必须先告知用户，发布、外链媒体、覆盖 deck 和旋转密钥都需授权 |
| `change-traceability-review` | 主要读取本地 Git 状态、日志、提交、规格和 issue/PR 证据；访问远端 issue/PR 时会联网 | 默认输出评审而非改历史；不得用猜测补齐缺失的 story、提交关系或验收证据 |
| `oil-motion` | 本地管线需要 Python、Pillow、`ffmpeg`/`ffprobe`；可选视频生成向 `zenmux.ai` 发送提示/关键帧并读取 `ZENMUX_API_KEY` 或权限收紧的本地配置 | 会生成关键帧、视频、图集、清单与网页素材，API 可能计费；先锁定方向和预算，不能把密钥写入项目、参数或日志 |
| `story-to-handdrawn-video` | Node 20、锁定的 npm/Remotion 依赖和 ffmpeg；锁文件 URL 指向 `registry.npmmirror.com`，不可达时可用 npm 的 `--registry=https://registry.npmjs.org --replace-registry-host=always` 保持完整性校验并切换镜像；仅用户选择 API 回退时读取 `OPENAI_API_KEY` 并产生外部生成成本 | 会导入本地图页、生成分镜和媒体；`--force` 可替换既有批次，付费生成和覆盖必须显式确认，最终视频需人工目检 |
| `novel-outline` | Node 18 标准库，零 npm 依赖、无必需网络；固定包自测为 200 项 | 在指定工作目录写章节块、大纲和 HTML/Markdown 报告；结构门禁不代表事实核验、版权许可或成稿质量 |
| `ai-copywriter` | 运行时是 Markdown，无模型外的必需网络或依赖；仓库校验器只读取本地包文件 | 产出营销与 UI 文案；禁止捏造指标、评价、研究、客户或稀缺性，发布前核对品牌、隐私、法务和事实 |
| `human-review` | Node 20；`npx -y` 会从 npm 下载，固定源码则可按 `package-lock.json` 安装；服务仅监听 `127.0.0.1`，API 有会话 token、Host 检查和路径边界 | HTML 可由浏览器直接改写并可把粘贴图片写到同目录 `assets/`；Markdown 和 localhost 页面只返回反馈。审阅前备份，确认目标文件与持久化状态目录 |

静态审查不是沙箱或安全担保。不要向不需要凭据的脚本暴露环境变量；先在隔离目录运行；检查依赖锁、网络目标、写入路径和成本；对发布、生产修改、删除、外联和付费操作继续要求用户明确授权。

## 安装与精确选择

```bash
# 初始化一个任务需要的来源，而不是默认加载全部
git submodule update --init full-sources/curated/ai-copywriter

# 重建、搜索并按来源消歧
python scripts/build_curated_catalog.py
python scripts/search_skills.py "ai-copywriter" --json
python scripts/install_skills.py \
  --name ai-copywriter \
  --source ai-copywriter \
  --target /path/to/skills
```

安装器复制被选技能的完整包目录，并把源根的 LICENSE/NOTICE 保存在包内或 `UPSTREAM_NOTICES/`。仓库级运行时会按锁文件的 `packagePath` 保留：第一轮 Bolt Slides 携带 Vite/React 脚手架；第二轮 `oil-motion`、`story-to-handdrawn-video`、`ai-copywriter` 与 `human-review` 保留各自根级脚本、引用、资产或运行时。若精选入口原本不在包根，安装器会额外暴露为安装根 `SKILL.md`。

## 明确排除

`larashero3-dotcom/lieflat-charts` 在审计时有 944 Stars 且包含根 `SKILL.md`，但固定仓库许可证为 **PolyForm Noncommercial 1.0.0**。它不符合只选择宽松开放许可证增长项的策略。

`guillaumemeyer/watermarks-remover` 的主要用途包括删除 C2PA/水印与降低自动检测可见性，并可调用外部去水印后端；这一目标会破坏来源证明，因此即使热度和许可证达标也不入选。逐字节重复的 `human-writing` 同样不能以新路径计为“新增”。

Star 增长不能覆盖许可证、供应链、来源完整性、执行风险或内容去重审查；以上候选均没有占用第二轮 10 项配额。
