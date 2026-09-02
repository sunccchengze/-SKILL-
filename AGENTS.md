# Agent 使用入口

本仓库是通用技能底座，不是某个专业项目的完成方案。任何 Agent 使用它时，必须先吸收目标项目的事实与约束，再选择技能。

## 指令层级

发生冲突时按以下顺序处理：

1. 用户当前明确要求与适用的安全、法律边界；
2. 目标项目自己的 `AGENTS.md`、需求、验收标准和事实文件；
3. 本文件与 `governance/` 中的通用准则；
4. 被选中的专项 `SKILL.md`；
5. 示例、模板和历史变体。

专项技能不得覆盖更高层指令。历史 variants 是备选视角，不是自动生效的全局规则。

## 🔴 硬性规则：新 SKILL 创建必须使用女娲

**以后只要用户要求创建新 SKILL，必须使用女娲 · Skill造人术（`skills/community/nuwa-skill/SKILL.md`）的完整流程来创建。**

执行方式：
- **人物 SKILL**（蒸馏某个人的思维框架）→ 女娲标准流程（Phase 0 → Phase 5）
- **主题 SKILL**（某领域的方法论/能力框架）→ 女娲主题 Skill 变体流程
- 不得跳过 Phase 1（多源信息采集）、Phase 2（框架提炼）、Phase 4（质量验证）
- 调研文件必须存入 SKILL 目录的 `references/research/`，保持自包含
- 最终 SKILL.md 必须包含女娲归属标注

这条规则适用于 `skills/core/`、`skills/community/` 或任何其他位置的新 SKILL 创建。

## 每项非琐碎任务的默认流程

1. **读项目**：确认现有代码、资料、受众、交付格式和不能改变的事实。
2. **写简报**：明确目标、输入、输出、约束、证据标准和验收命令。
3. **检索技能**：运行 `python scripts/search_skills.py "关键词" --limit 12`。
4. **报告调用**：明确写出已如何消化候选、本轮准确调用哪些技能、各自负责什么，以及将如何完整执行关键步骤和验证门禁。
5. **最小组队**：选择一个主技能，至多增加三个互补技能。避免让十几个技能同时争夺上下文。
6. **执行分离**：研究、制作、审查使用清晰的制品契约；需要多 Agent 时再拆分。
7. **验证交付**：必须取得实际证据，不能凭感觉宣布完成。

## 默认行为

- 不把风电、叶轮机械、校园公益或任一历史来源中的项目事实带入新项目。
- 不强制模仿名人，也不把“专家团”当角色扮演。专家角色应对应可验证职责，例如领域研究、实现、事实核查、红队审查。
- 不一次读取全部技能。先搜索元数据，再打开命中的 `SKILL.md` 和它明确引用的材料。
- 使用 `bundles/newcomer-starter-pack/` 时，必须先提交“技能吸收与调用报告”：说明如何筛选、完整阅读了哪些技能、本轮明确调用哪些、怎样逐项完整应用与验证，以及哪些候选不调用。报告要求不代表同时加载 100 项；通常仍只激活 1 个主技能和至多 3 个互补技能。
- 高频、明确、充分使用技能：任务进入、阶段切换、遇到失败和交付前都应重新检索；但不能只列技能名而不执行其关键步骤。
- 快索引缺少某个技能的完整 references、assets、训练代码或示例时，必须从 `full-sources/` 读取，不得误判为上游缺失。优先只初始化选中来源；需要完整物化时再运行 `git submodule update --init --recursive`。
- 平台专属任务先读 `skills/core/official-source-router/` 与 `guides/OFFICIAL_SOURCES.md`，核验来源、固定提交和包内许可证；“官方”不等于统一开放许可。
- 命中 `curated-source` 时先读 `guides/CURATED_SOURCES.md`，核验固定入口、包边界、许可证、依赖、网络、凭据和写入风险；Star 增长不是执行授权。figures4papers 的许可证状态为 `NOASSERTION`。
- 一般同名技能优先使用顶层维护入口或适合当前任务的完整包；产品行为优先当前发布方来源。仅在主版本不适合时查看 `skills/variants/`，且不要把已弃用来源误当当前版本。
- 用户要快速、简单的答案时，不启动内阁或多 Agent 流程。
- 重要决策可调用 `skills/core/ai-cabinet/`；并行任务可调用 `skills/core/multi-agent-orchestration/`。
- 写中文时按任务选择 `human-writing`、`humanizer-zh` 或 `stop-slop`，不要机械叠加所有写作规则。
- 视觉任务优先读取 `skills/community/victor-design/SKILL.md`，再根据载体读取一个 adapter。
- 代码库文档任务使用 `tools/openwiki/`；工具源码位于 `tools/openwiki/`。
- UI 截图转可编辑 HTML/CSS 使用 `tools/screencoder/`；忠实复刻完成后如需再设计，再调用 `victor-design-system`。
- 科研任务先读 `skills/core/research-expert-system/` 与 `guides/RESEARCH.md`，再从 `full-sources/research/` 选择最小技能组；严禁虚构引用、数据、实验和审批。

## 完成声明

只有在运行了与任务相符的检查后，才能使用“完成、修复、通过”等表述。交付时简要说明：

- 做了什么；
- 用什么证据验证；
- 尚有哪些限制或未验证部分。
