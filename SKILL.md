---
name: universal-skill-router
description: 面向任意任务的技能检索与路由入口。根据用户自然语言任务描述，识别意图类别，推荐最匹配的技能组合。
---

# 通用技能路由器

> **你描述任务，我推荐技能组。** 每个任务对应一组互补技能，不是单个技能。

## 核心概念：技能组

每个任务都推荐一个**技能组**，由四种角色的技能组成：

```
🎯 主技能 (1-2个)  → 负责最终交付物
🔧 支撑技能 (1-3个) → 补足领域知识、证据、专项方法
🔍 审查技能 (0-1个) → 质量门禁、安全审计、交付验证
🤖 协调技能 (0-1个) → 多 Agent 并行（仅复杂任务）
```

**不是挑一个技能，是挑一组技能协作完成任务。**

## 使用方式

```bash
# 用法 1（推荐）：返回完整技能组
python scripts/search_skills.py "帮我做一个产品介绍视频" --group

# 用法 2：意图识别 + 关键词搜索
python scripts/search_skills.py "帮我做一个产品介绍视频" --intent

# 用法 3：浏览任务→技能映射表
# 打开 TASK_ROUTING.md
```

### 示例输出

```
$ python scripts/search_skills.py "帮我做一个产品介绍视频" --group

📋 任务类别: design-media

  🎯 主技能（负责交付物）
    • video-shotcraft  — 电影级产品视频

  🔧 支撑技能（补足领域/证据）
    • remotion-video-creation  — Remotion 技术实现
    • demo-video               — 产品演示/ walkthrough
    • manim-video              — 技术概念动画
    • video-use                — 对话式视频剪辑

  ⚠️  注意事项: 产品视频用 video-shotcraft，技术动画用 manim-video
```

## 任务意图分类

路由器识别以下 9 大意图类别，每类对应仓库的一个技能域：

| 意图类别 | 典型触发词 | 对应分类 | 首选技能 |
|---|---|---|---|
| 📝 写作与内容 | 写、改稿、文案、翻译、公众号 | writing-content | human-writing, stop-slop, humanizer-zh |
| 💻 工程与代码 | 开发、调试、部署、API、测试 | engineering-code | systematic-debugging, 按技术栈匹配 |
| 🔬 研究与论文 | 论文、综述、引用、实验、统计 | research-science | research-expert-system → 子路由 |
| 🎨 设计与视觉 | 海报、UI、PPT、配色、品牌 | design-media | victor-design-system, 按载体匹配 |
| 🎬 视频与动效 | 视频、动画、剪辑、Remotion | design-media | video-shotcraft, remotion-video-creation |
| 📊 数据与分析 | 图表、数据、统计、dashboard | documents-data / research-science | dashboard-builder, scipilot-figure |
| 💼 商业与策略 | 定价、营销、竞品、BP、运营 | business-strategy | market-research, marketing-campaign |
| 🔒 安全与合规 | 审计、漏洞、隐私、合规 | security-compliance | security-audit, skill-security-auditor |
| 🤖 编排与协调 | 多Agent、并行、工作流 | agents-orchestration | multi-agent-orchestration |

## 路由流程

### 1. 意图识别

从用户描述中提取：
- **动作**（做什么）：写、做、画、分析、审查、设计、调试…
- **对象**（对什么）：视频、论文、海报、代码、数据…
- **领域**（什么场景）：科研、商业、工程、创意…

### 2. 类别定位

根据意图定位到 1-2 个主要分类，在该分类内优先搜索。

### 3. 技能推荐

```
主技能 (1 个)  → 负责最终交付物
支撑技能 (0-2) → 补足领域知识或证据
审查技能 (0-1) → 质量检查、安全审计
```

### 4. 执行闭环

1. 只读命中技能的 `SKILL.md`
2. 再读它要求的 references
3. 只运行当前任务需要的 scripts
4. 交付前验证结果

## 快速场景路由（技能组速查）

| 用户说… | 🎯 主技能 | 🔧 支撑 | 🔍 审查 |
|---|---|---|---|
| "帮我写篇文章/改稿" | human-writing | article-writing | stop-slop, humanizer-zh |
| "帮我去掉AI腔" | stop-slop, humanizer-zh | human-writing | — |
| "帮我写科研论文" | research-paper-writing | nature-citation, nature-figure | academic-integrity |
| "帮我做张海报" | victor-design-system | taste | design-evaluation |
| "帮我做个PPT" | cyber-ppt | pptx, guizang-ppt-skill | — |
| "帮我做个产品视频" | video-shotcraft | demo-video, remotion, manim | — |
| "帮我分析数据画图" | nature-figure, scipilot-figure | data-visualization, d3 | — |
| "帮我做定价策略" | pricing-strategist | market-research, competitive | — |
| "帮我审代码安全" | security-audit, security-scan | security-pen-testing | deep-security-scan |
| "帮我拆任务并行做" | multi-agent-orchestration | memory-system | — |
| "帮我做个网页" | screencoder | frontend-design-direction | — |
| "帮我调研一下X" | market-research, agent-reach | ito-market-intelligence | — |
| "帮我做营销方案" | marketing-campaign | landing, content-production | — |
| "帮我做竞品分析" | competitive-platform-analysis | competitive-report-structure | — |
| "帮我做UI设计" | victor-design-system, ui-ux-pro-max | frontend-design | better-accessibility |
| "重要决策/方案选择" | ai-cabinet | yuqiao-wendui, guiguzi | — |

完整技能组定义见 [`TASK_ROUTING.md`](TASK_ROUTING.md)。

## 渐进加载

1. 只读命中技能的 `SKILL.md`
2. 再读它要求的 references
3. 只运行当前任务需要的 scripts
4. variants 仅用于比较替代方法
5. 官方来源命中时按需初始化对应子模块
6. 需要完整包资源时，读取 `full-sources/` 中的固定上游

## 治理文档

- 重大决策：[`governance/AI_CABINET.md`](governance/AI_CABINET.md)
- 多 Agent 协作：[`governance/MULTI_AGENT_ORCHESTRATION.md`](governance/MULTI_AGENT_ORCHESTRATION.md)
- 质量门禁：[`governance/QUALITY_GATES.md`](governance/QUALITY_GATES.md)
- 宪法：[`governance/CONSTITUTION.md`](governance/CONSTITUTION.md)
