#!/usr/bin/env python3
"""Search catalog and return SKILL GROUPS — not just ranked individuals.

A skill group for a task = 1 primary + supporting + review + optional orchestration.

Usage:
    # Task-group mode (recommended): returns a complete skill group
    python search_skills.py "帮我做一个产品介绍视频" --group

    # Intent mode: returns top ranked skills with intent categories
    python search_skills.py "帮我做一个产品介绍视频" --intent

    # Keyword mode (traditional): flat ranked list
    python search_skills.py "video remotion" --limit 12
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from catalog_aliases import annotate_alias, is_alias, load_alias_index

REPO = Path(__file__).resolve().parents[1]
CATALOG = REPO / "catalog" / "skills.json"

TIER_BONUS = {
    "maintained": 8,
    "official-source": 7,
    "router": 7,
    "curated-source": 6,
    "full-source": 6,
    "community": 5,
    "tool-bundled": 4,
    "bundled": 3,
    "variant": 0,
}

# ── Synonym groups for cross-language expansion ───────────────────────────

SYNONYM_GROUPS: list[dict[str, list[str]]] = [
    {"keywords": ["写", "writing", "article", "文章", "文案", "博客", "blog", "post"]},
    {"keywords": ["改稿", "edit", "revise", "润色", "polish", "改文"]},
    {"keywords": ["翻译", "translate", "translation", "中英"]},
    {"keywords": ["AI腔", "ai tone", "slop", "模板味", "ai generated", "去ai", "humanize"]},
    {"keywords": ["公众号", "wechat", "微信"]},
    {"keywords": ["演讲", "speech", "presentation", "口播"]},
    {"keywords": ["小说", "fiction", "novel", "故事", "story"]},
    {"keywords": ["开发", "develop", "build", "编程", "code", "写代码"]},
    {"keywords": ["调试", "debug", "排错", "排查", "troubleshoot"]},
    {"keywords": ["部署", "deploy", "deployment", "发布", "上线"]},
    {"keywords": ["测试", "test", "testing", "单元测试", "unit test"]},
    {"keywords": ["api", "接口", "endpoint", "rest"]},
    {"keywords": ["前端", "frontend", "web", "网页", "页面", "html", "css"]},
    {"keywords": ["后端", "backend", "server", "服务器", "api"]},
    {"keywords": ["截图", "screenshot", "screencoder", "还原", "复刻"]},
    {"keywords": ["kubernetes", "k8s", "容器", "container", "helm"]},
    {"keywords": ["ci/cd", "ci cd", "pipeline", "流水线", "自动化"]},
    {"keywords": ["论文", "paper", "论文写作", "学术", "academic", "manuscript"]},
    {"keywords": ["综述", "literature review", "文献", "检索", "search"]},
    {"keywords": ["引用", "citation", "cite", "参考文献", "reference"]},
    {"keywords": ["实验", "experiment", "实验设计"]},
    {"keywords": ["统计", "statistics", "statistical", "回归", "regression"]},
    {"keywords": ["科研", "research", "科学", "scientific"]},
    {"keywords": ["复现", "reproducib", "reproduce"]},
    {"keywords": ["同行评审", "peer review", "审稿", "rebuttal"]},
    {"keywords": ["设计", "design", "视觉", "visual"]},
    {"keywords": ["海报", "poster", "宣传"]},
    {"keywords": ["PPT", "ppt", "演示", "幻灯片", "slides", "powerpoint"]},
    {"keywords": ["UI", "ux", "界面", "用户界面", "交互"]},
    {"keywords": ["品牌", "brand", "branding", "VI"]},
    {"keywords": ["配色", "color", "颜色", "色彩"]},
    {"keywords": ["logo", "标志", "图标", "icon"]},
    {"keywords": ["视频", "video", "影片", "剪辑"]},
    {"keywords": ["动画", "animation", "动效", "motion", "特效"]},
    {"keywords": ["remotion", "视频制作"]},
    {"keywords": ["manim", "数学动画"]},
    {"keywords": ["数据", "data", "分析", "analysis", "analytics"]},
    {"keywords": ["图表", "chart", "plot", "figure", "可视化", "visualization"]},
    {"keywords": ["dashboard", "仪表盘", "看板"]},
    {"keywords": ["excel", "表格", "spreadsheet", "csv"]},
    {"keywords": ["pandas", "numpy", "matplotlib", "seaborn"]},
    {"keywords": ["机器学习", "machine learning", "ML", "深度学习", "deep learning"]},
    {"keywords": ["营销", "marketing", "推广", "获客"]},
    {"keywords": ["定价", "pricing", "price", "收费", "定价策略"]},
    {"keywords": ["竞品", "competitor", "competitive", "竞争分析"]},
    {"keywords": ["市场调研", "market research", "市场分析"]},
    {"keywords": ["运营", "operation", "用户运营", "内容运营"]},
    {"keywords": ["产品", "product", "需求", "prd"]},
    {"keywords": ["商业计划", "business plan", "BP", "融资"]},
    {"keywords": ["landing", "落地页", "着陆页"]},
    {"keywords": ["SEO", "搜索优化", "排名"]},
    {"keywords": ["安全", "security", "漏洞", "vulnerability"]},
    {"keywords": ["审计", "audit", "审查", "合规"]},
    {"keywords": ["隐私", "privacy", "数据保护", "data protection"]},
    {"keywords": ["渗透", "penetration", "pen test", "pentest"]},
    {"keywords": ["加密", "encrypt", "密钥", "secret", "credential"]},
    {"keywords": ["无障碍", "accessibility", "a11y"]},
    {"keywords": ["多agent", "multi-agent", "并行", "parallel", "拆分任务"]},
    {"keywords": ["决策", "decision", "方案比较", "选择"]},
    {"keywords": ["工作流", "workflow", "编排", "orchestrat"]},
    {"keywords": ["远程", "remote", "desktop", "远程桌面"]},
    {"keywords": ["文档生成", "wiki", "知识库"]},
    {"keywords": ["录屏", "screen record", "gif", "浏览器录屏"]},
    {"keywords": ["调研", "research tool", "全网搜索", "search the web"]},
    {"keywords": ["头脑风暴", "brainstorm", "创意", "ideation", "发散"]},
    {"keywords": ["架构", "architecture", "系统设计", "system design"]},
    {"keywords": ["重构", "refactor", "代码质量", "clean code"]},
    {"keywords": ["领域驱动", "DDD", "domain driven", "bounded context"]},
    {"keywords": ["量化", "quant", "金融", "trading", "回测", "backtest"]},
    {"keywords": ["游戏", "game", "unity", "godot"]},
    {"keywords": ["RAG", "向量", "embedding", "检索增强"]},
    {"keywords": ["Figma", "设计稿", "design system"]},
    {"keywords": ["部署", "deploy", "CI/CD", "devops", "运维"]},
    {"keywords": ["监控", "observability", "monitoring", "tracing", "可观测"]},
    {"keywords": ["事故", "incident", "postmortem", "故障", "复盘"]},
    {"keywords": ["转化", "CRO", "conversion", "落地页优化"]},
    {"keywords": ["性能", "performance", "优化", "optimization", "加载速度"]},
    {"keywords": ["创业", "startup", "蓝海", "blue ocean"]},
]

# ── Task-group definitions ────────────────────────────────────────────────
# Each entry defines a task pattern and the skill group to assemble.
# Roles: primary (delivers), support (domain knowledge), review (quality),
#        orchestrate (multi-agent coordination)

SKILL_GROUPS: list[dict] = [
    {
        "pattern": ["写文章", "写博客", "写公众号", "写作", "writing", "写回答", "写稿",
                    "公众号文章", "公众号", "博客文章", "写篇"],
        "categories": ["writing-content"],
        "group": {
            "primary": ["human-writing"],
            "support": ["article-writing", "writing"],
            "review": ["stop-slop", "humanizer-zh"],
            "notes": "中文输出必须经过 stop-slop/humanizer-zh 去除 AI 腔",
        },
    },
    {
        "pattern": ["去AI腔", "去掉AI味", "更自然", "humanize", "像人写的"],
        "categories": ["writing-content"],
        "group": {
            "primary": ["stop-slop", "humanizer-zh"],
            "support": ["human-writing"],
            "review": [],
            "notes": "stop-slop 去英文模板腔，humanizer-zh 去中文 AI 痕迹",
        },
    },
    {
        "pattern": ["科研", "论文", "paper", "学术", "academic", "文献综述"],
        "categories": ["research-science"],
        "group": {
            "primary": ["research-expert-system", "research-workflow-orchestrator"],
            "support": ["systematic-evidence-synthesis", "research-question-protocol"],
            "review": ["academic-integrity-ai-disclosure"],
            "notes": "由 research-expert-system 子路由到具体科研阶段",
        },
    },
    {
        "pattern": ["论文写作", "写论文", "paper writing", "投稿"],
        "categories": ["research-science", "writing-content"],
        "group": {
            "primary": ["research-paper-writing", "nature-polishing"],
            "support": ["nature-citation", "nature-figure"],
            "review": ["academic-integrity-ai-disclosure"],
            "notes": "英文论文用 nature-polishing，中文用 research-paper-writing",
        },
    },
    {
        "pattern": ["画图", "图表", "figure", "chart", "plot", "可视化", "数据可视化"],
        "categories": ["research-science", "design-media", "documents-data"],
        "group": {
            "primary": ["nature-figure", "scipilot-figure-skill"],
            "support": ["data-visualization", "d3-data-visualization"],
            "review": [],
            "notes": "科研图用 nature-figure，通用可视化用 data-visualization",
        },
    },
    {
        "pattern": ["数据分析", "分析数据", "data analysis", "统计"],
        "categories": ["documents-data", "research-science"],
        "group": {
            "primary": ["exploratory-data-analysis", "reproducible-research-analysis"],
            "support": ["dashboard-builder", "data-visualization"],
            "review": [],
            "notes": "先 exploratory 探索，再 reproducible 锁定复现",
        },
    },
    {
        "pattern": ["海报", "poster", "设计", "视觉设计"],
        "categories": ["design-media"],
        "group": {
            "primary": ["victor-design-system"],
            "support": ["taste"],
            "review": ["design-evaluation"],
            "notes": "用 poster adapter；design-evaluation 做交付审查",
        },
    },
    {
        "pattern": ["PPT", "ppt", "演示", "幻灯片", "slides", "powerpoint", "演示文稿"],
        "categories": ["design-media", "documents-data"],
        "group": {
            "primary": ["cyber-ppt", "victor-design-system"],
            "support": ["pptx", "guizang-ppt-skill", "frontend-slides"],
            "review": [],
            "notes": "咨询风格用 cyber-ppt，网页PPT用 guizang-ppt-skill，通用用 pptx",
        },
    },
    {
        "pattern": ["视频", "video", "影片", "动画", "animation", "动效", "motion"],
        "categories": ["design-media"],
        "group": {
            "primary": ["video-shotcraft"],
            "support": ["remotion-video-creation", "demo-video", "manim-video", "video-use"],
            "review": [],
            "notes": "产品视频用 video-shotcraft，技术动画用 manim-video，对话剪辑用 video-use",
        },
    },
    {
        "pattern": ["产品视频", "demo", "产品演示", "产品walkthrough"],
        "categories": ["design-media", "business-strategy"],
        "group": {
            "primary": ["demo-video", "video-shotcraft"],
            "support": ["heygen-video", "oil-motion"],
            "review": [],
            "notes": "产品演示用 demo-video，电影级用 video-shotcraft",
        },
    },
    {
        "pattern": ["UI", "ux", "界面", "网页设计", "web design", "前端设计"],
        "categories": ["design-media", "engineering-code"],
        "group": {
            "primary": ["victor-design-system", "ui-ux-pro-max"],
            "support": ["frontend-design-direction", "frontend-slides"],
            "review": ["better-accessibility"],
            "notes": "用 product-ui adapter；better-accessibility 检查无障碍",
        },
    },
    {
        "pattern": ["截图转代码", "screenshot", "复刻", "还原页面"],
        "categories": ["engineering-code"],
        "group": {
            "primary": ["screencoder"],
            "support": ["frontend-design-direction"],
            "review": [],
            "notes": "screencoder 做截图→HTML/CSS，frontend-design-direction 做风格指导",
        },
    },
    {
        "pattern": ["调试", "debug", "排错", "排查bug", "troubleshoot"],
        "categories": ["engineering-code"],
        "group": {
            "primary": ["systematic-debugging", "debugging-and-error-recovery"],
            "support": ["python-debugpy"],
            "review": [],
            "notes": "先 systematic-debugging 定位根因，再 python-debugpy 具体调试",
        },
    },
    {
        "pattern": ["开发", "写代码", "编程", "coding", "develop", "build"],
        "categories": ["engineering-code"],
        "group": {
            "primary": ["spec-kit"],
            "support": ["systematic-debugging", "context-engineering"],
            "review": ["open-code-review", "change-traceability-review"],
            "notes": "spec-kit 驱动规范开发，open-code-review 做审查",
        },
    },
    {
        "pattern": ["安全", "security", "漏洞", "vulnerability", "审计", "audit"],
        "categories": ["security-compliance", "engineering-code"],
        "group": {
            "primary": ["security-audit", "security-scan"],
            "support": ["security-pen-testing", "skill-security-auditor"],
            "review": ["deep-security-scan", "propose-security-hardening"],
            "notes": "security-audit 综合审查，deep-security-scan 深度扫描",
        },
    },
    {
        "pattern": ["隐私", "privacy", "数据保护", "合规", "compliance"],
        "categories": ["security-compliance"],
        "group": {
            "primary": ["book-privacy-context-flow-audit"],
            "support": ["information-security-manager-iso27001", "compliance-os"],
            "review": ["book-ethical-algorithm-constraints"],
            "notes": "隐私审计用 context-flow，合规用 ISO27001",
        },
    },
    {
        "pattern": ["营销", "marketing", "推广", "获客", "营销方案"],
        "categories": ["business-strategy"],
        "group": {
            "primary": ["marketing-campaign", "marketing-demand-acquisition"],
            "support": ["landing", "content-production"],
            "review": [],
            "notes": "marketing-campaign 做方案，landing 做落地页",
        },
    },
    {
        "pattern": ["定价", "pricing", "price", "收费", "定价策略"],
        "categories": ["business-strategy"],
        "group": {
            "primary": ["pricing-strategist", "pricing-strategy"],
            "support": ["market-research", "competitive-platform-analysis"],
            "review": [],
            "notes": "pricing-strategist 做模型选择，pricing-strategy 做 SaaS 定价",
        },
    },
    {
        "pattern": ["竞品", "competitor", "competitive", "竞争分析"],
        "categories": ["business-strategy"],
        "group": {
            "primary": ["competitive-platform-analysis"],
            "support": ["competitive-report-structure", "market-research"],
            "review": [],
            "notes": "competitive-platform-analysis 做分析，competitive-report-structure 出报告",
        },
    },
    {
        "pattern": ["市场调研", "market research", "市场分析", "调研"],
        "categories": ["business-strategy"],
        "group": {
            "primary": ["market-research", "agent-reach"],
            "support": ["ito-market-intelligence"],
            "review": [],
            "notes": "agent-reach 做全网调研，market-research 做结构化分析",
        },
    },
    {
        "pattern": ["决策", "decision", "方案比较", "选方案", "重要选择"],
        "categories": ["agents-orchestration"],
        "group": {
            "primary": ["ai-cabinet"],
            "support": ["yuqiao-wendui", "guiguzi"],
            "review": [],
            "notes": "ai-cabinet 五席追问；鬼谷子/渔樵问对做补充视角",
        },
    },
    {
        "pattern": ["多agent", "multi-agent", "并行", "拆分任务", "分工"],
        "categories": ["agents-orchestration"],
        "group": {
            "primary": ["multi-agent-orchestration"],
            "support": ["memory-system"],
            "review": [],
            "notes": "定义职责边界、制品契约和合并顺序",
        },
    },
    {
        "pattern": ["SEO", "搜索优化", "排名", "seo"],
        "categories": ["business-strategy", "writing-content"],
        "group": {
            "primary": ["qiaomu-seo"],
            "support": ["landing", "content-production"],
            "review": [],
            "notes": "",
        },
    },
    {
        "pattern": ["造人", "蒸馏", "人物思维", "nuwa", "女娲", "perspective"],
        "categories": ["agents-orchestration", "general"],
        "group": {
            "primary": ["huashu-nuwa"],
            "support": [],
            "review": [],
            "notes": "输入人名→深度调研→蒸馏出人物 Skill",
        },
    },
    {
        "pattern": ["远程桌面", "remote desktop", "远程控制"],
        "categories": ["engineering-code"],
        "group": {
            "primary": ["rustdesk"],
            "support": [],
            "review": [],
            "notes": "需要明确授权，非浏览器预览",
        },
    },
    {
        "pattern": ["生成图片", "画图", "generate image", "logo", "icon"],
        "categories": ["design-media"],
        "group": {
            "primary": ["gpt-image-2-skill"],
            "support": ["fal-ai-media"],
            "review": [],
            "notes": "gpt-image-2 做通用生图，fal-ai 做媒体生成",
        },
    },
    {
        "pattern": ["代码审查", "code review", "review", "代码质量"],
        "categories": ["engineering-code"],
        "group": {
            "primary": ["open-code-review"],
            "support": ["change-traceability-review", "trace-file-lineage"],
            "review": [],
            "notes": "",
        },
    },
    {
        "pattern": ["ML", "机器学习", "深度学习", "deep learning", "训练"],
        "categories": ["engineering-code", "research-science"],
        "group": {
            "primary": ["mle-workflow", "d2l-lab-backbone"],
            "support": ["senior-data-scientist", "context-engineering"],
            "review": [],
            "notes": "mle-workflow 做工程流，d2l-lab-backbone 做实验",
        },
    },
    {
        "pattern": ["运营", "operation", "内容运营", "用户运营"],
        "categories": ["business-strategy", "writing-content"],
        "group": {
            "primary": ["x-mastery-mentor", "content-production"],
            "support": ["book-berger-contagious", "marketing-campaign"],
            "review": [],
            "notes": "X/Twitter 用 x-mastery-mentor，通用内容用 content-production",
        },
    },
    {
        "pattern": ["无障碍", "accessibility", "a11y"],
        "categories": ["security-compliance"],
        "group": {
            "primary": ["better-accessibility"],
            "support": [],
            "review": [],
            "notes": "",
        },
    },
    # ── New groups from antigravity + wondelai sources ──────────────────
    {
        "pattern": ["代码审查", "code review", "review code", "cr"],
        "categories": ["engineering-code"],
        "group": {
            "primary": ["code-reviewer", "open-code-review"],
            "support": ["architect-review"],
            "review": ["change-traceability-review"],
            "notes": "code-reviewer 做代码级审查，architect-review 做架构级审查",
        },
    },
    {
        "pattern": ["架构", "architecture", "系统设计", "system design", "技术方案",
                    "架构设计", "软件架构", "技术架构"],
        "categories": ["engineering-code"],
        "group": {
            "primary": ["architect-review", "architecture-patterns"],
            "support": ["brainstorming", "plan-writing"],
            "review": ["clean-architecture", "domain-driven-design"],
            "notes": "architect-review 做架构审查，clean-architecture/DDD 提供设计原则",
        },
    },
    {
        "pattern": ["TDD", "测试驱动", "test driven", "写测试", "write test"],
        "categories": ["engineering-code"],
        "group": {
            "primary": ["test-driven-development"],
            "support": ["testing-patterns", "systematic-debugging"],
            "review": ["verification-before-completion"],
            "notes": "test-driven-development 做 TDD 流程，testing-patterns 补测试模式",
        },
    },
    {
        "pattern": ["React", "前端组件", "组件开发", "next.js"],
        "categories": ["engineering-code"],
        "group": {
            "primary": ["react-patterns", "react-best-practices", "frontend-developer"],
            "support": ["frontend-design-direction"],
            "review": ["code-reviewer"],
            "notes": "react-patterns 做模式指导，react-best-practices 做性能优化",
        },
    },
    {
        "pattern": ["Python", "python开发", "python优化"],
        "categories": ["engineering-code"],
        "group": {
            "primary": ["python-patterns", "python-performance-optimization"],
            "support": ["python-packaging"],
            "review": ["code-reviewer"],
            "notes": "python-patterns 做模式指导，python-performance-optimization 做性能分析",
        },
    },
    {
        "pattern": ["TypeScript", "typescript开发", "类型"],
        "categories": ["engineering-code"],
        "group": {
            "primary": ["typescript-expert"],
            "support": ["react-patterns", "clean-code"],
            "review": ["code-reviewer"],
            "notes": "",
        },
    },
    {
        "pattern": ["Docker", "容器", "dockerfile", "container"],
        "categories": ["engineering-code"],
        "group": {
            "primary": ["docker-expert"],
            "support": ["aws-serverless"],
            "review": [],
            "notes": "",
        },
    },
    {
        "pattern": ["AWS", "aws开发", "serverless", "云部署"],
        "categories": ["engineering-code"],
        "group": {
            "primary": ["aws-serverless"],
            "support": ["docker-expert"],
            "review": [],
            "notes": "",
        },
    },
    {
        "pattern": ["SQL优化", "sql", "数据库优化", "query"],
        "categories": ["engineering-code", "documents-data"],
        "group": {
            "primary": ["sql-optimization-patterns"],
            "support": ["ddia-systems"],
            "review": [],
            "notes": "sql-optimization-patterns 做查询优化，ddia-systems 做系统设计",
        },
    },
    {
        "pattern": ["头脑风暴", "brainstorm", "创意", "ideation"],
        "categories": ["agents-orchestration", "general"],
        "group": {
            "primary": ["brainstorming"],
            "support": ["plan-writing"],
            "review": [],
            "notes": "brainstorming 做发散创意，plan-writing 做收敛规划",
        },
    },
    {
        "pattern": ["clean code", "代码质量", "重构", "refactor"],
        "categories": ["engineering-code"],
        "group": {
            "primary": ["clean-code", "code-refactoring-refactor-clean"],
            "support": ["code-reviewer"],
            "review": ["architect-review"],
            "notes": "clean-code 做代码整洁原则，code-reviewer 做审查",
        },
    },
    {
        "pattern": ["DDD", "领域驱动", "domain driven", "bounded context"],
        "categories": ["engineering-code"],
        "group": {
            "primary": ["domain-driven-design"],
            "support": ["clean-architecture", "ddia-systems"],
            "review": [],
            "notes": "DDD 做领域建模，clean-architecture 做架构约束，DDIA 做数据系统",
        },
    },
    {
        "pattern": ["SEO", "seo优化", "搜索排名", "搜索引擎"],
        "categories": ["business-strategy", "writing-content"],
        "group": {
            "primary": ["seo-structure-architect", "seo-audit"],
            "support": ["content-marketer", "programmatic-seo"],
            "review": [],
            "notes": "seo-structure-architect 做结构优化，content-marketer 做内容策略",
        },
    },
    {
        "pattern": ["内容营销", "content marketing", "营销内容", "copywriting"],
        "categories": ["business-strategy", "writing-content"],
        "group": {
            "primary": ["content-marketer", "copywriting"],
            "support": ["seo-structure-architect", "content-production"],
            "review": [],
            "notes": "content-marketer 做策略，copywriting 做文案执行",
        },
    },
    {
        "pattern": ["数据分析", "data science", "数据科学家", "机器学习建模"],
        "categories": ["research-science", "engineering-code"],
        "group": {
            "primary": ["data-scientist"],
            "support": ["python-patterns", "sql-optimization-patterns"],
            "review": [],
            "notes": "data-scientist 做建模分析",
        },
    },
    {
        "pattern": ["量化", "quant", "金融建模", "trading", "回测"],
        "categories": ["business-strategy", "research-science"],
        "group": {
            "primary": ["quant-analyst"],
            "support": ["data-scientist", "backtesting-frameworks"],
            "review": [],
            "notes": "quant-analyst 做量化策略，backtesting-frameworks 做回测",
        },
    },
    {
        "pattern": ["渗透测试", "pentest", "penetration", "hacking"],
        "categories": ["security-compliance"],
        "group": {
            "primary": ["pentest-checklist", "security-pen-testing"],
            "support": ["ethical-hacking-methodology", "burp-suite-testing"],
            "review": ["vulnerability-scanner"],
            "notes": "pentest-checklist 做检查清单，ethical-hacking-methodology 做方法论",
        },
    },
    {
        "pattern": ["Mermaid", "流程图", "sequence", "架构图", "diagram"],
        "categories": ["engineering-code", "design-media"],
        "group": {
            "primary": ["mermaid-expert"],
            "support": [],
            "review": [],
            "notes": "mermaid-expert 做所有类型的 Mermaid 图表",
        },
    },
    {
        "pattern": ["创业", "startup", "蓝海", "blue ocean", "商业策略"],
        "categories": ["business-strategy"],
        "group": {
            "primary": ["blue-ocean-strategy", "good-strategy-bad-strategy"],
            "support": ["crossing-the-chasm", "hundred-million-offers"],
            "review": [],
            "notes": "蓝海策略做差异化，好战略坏战略做内核诊断，跨越鸿沟做市场阶段判断",
        },
    },
    {
        "pattern": ["产品设计", "product design", "用户习惯", "hook model", "产品增长"],
        "categories": ["business-strategy", "design-media"],
        "group": {
            "primary": ["hooked-ux", "design-sprint"],
            "support": ["conversion-optimization", "continuous-discovery"],
            "review": [],
            "notes": "Hooked 做习惯养成设计，Design Sprint 做快速验证",
        },
    },
    {
        "pattern": ["管理", "management", "团队管理", "高产出"],
        "categories": ["business-strategy", "general"],
        "group": {
            "primary": ["high-output-management"],
            "support": ["good-strategy-bad-strategy"],
            "review": [],
            "notes": "格鲁夫《高产出管理》: manager 的产出 = 其组织的产出",
        },
    },
    {
        "pattern": ["病毒传播", "viral", "口碑", "word of mouth", "传播"],
        "categories": ["business-strategy", "writing-content"],
        "group": {
            "primary": ["contagious", "book-berger-contagious"],
            "support": ["content-marketer", "marketing-campaign"],
            "review": [],
            "notes": "STEPPS 框架: 社交货币、诱因、情绪、公共性、实用价值、故事",
        },
    },
    {
        "pattern": ["转化优化", "CRO", "conversion", "落地页优化", "注册转化"],
        "categories": ["business-strategy", "design-media"],
        "group": {
            "primary": ["conversion-optimization"],
            "support": ["ab-test-setup", "landing"],
            "review": [],
            "notes": "转化优化做诊断，A/B 测试做验证",
        },
    },
    {
        "pattern": ["前端性能", "web performance", "Core Web Vitals", "加载速度"],
        "categories": ["engineering-code"],
        "group": {
            "primary": ["react-best-practices", "web-performance-optimization"],
            "support": ["high-perf-browser"],
            "review": [],
            "notes": "react-best-practices 含 Vercel 维护的性能优化指南",
        },
    },
    {
        "pattern": ["文档", "docx", "PDF", "文档处理", "Word"],
        "categories": ["documents-data"],
        "group": {
            "primary": ["pdf", "docx"],
            "support": ["anydoc"],
            "review": [],
            "notes": "pdf 处理 PDF，docx 处理 Word，anydoc 通用文档",
        },
    },
    {
        "pattern": ["浏览器自动化", "playwright", "爬虫", "scraping", "web automation"],
        "categories": ["engineering-code"],
        "group": {
            "primary": ["playwright"],
            "support": ["browser-use", "agent-browser"],
            "review": [],
            "notes": "playwright 做自动化测试，browser-use 做浏览器操控",
        },
    },
    {
        "pattern": ["游戏开发", "game dev", "unity", "godot"],
        "categories": ["engineering-code", "design-media"],
        "group": {
            "primary": ["game-design"],
            "support": ["unity-developer", "godot-gdscript-patterns"],
            "review": [],
            "notes": "game-design 做机制设计，unity/godot 做引擎实现",
        },
    },
    {
        "pattern": ["RAG", "向量数据库", "embedding", "检索增强"],
        "categories": ["engineering-code", "research-science"],
        "group": {
            "primary": ["rag-engineer"],
            "support": ["langgraph", "prompt-engineer"],
            "review": [],
            "notes": "rag-engineer 做 RAG 系统设计，langgraph 做 Agent 编排",
        },
    },
    {
        "pattern": ["Figma", "设计稿", "figma设计", "设计系统"],
        "categories": ["design-media", "engineering-code"],
        "group": {
            "primary": ["figma-implement-design", "figma-use"],
            "support": ["figma-create-design-system-rules", "figma-code-connect-components"],
            "review": [],
            "notes": "figma-implement-design 做设计→代码，figma-use 做 Figma API 操作",
        },
    },
    {
        "pattern": ["部署", "deploy", "CI/CD", "devops", "运维"],
        "categories": ["engineering-code"],
        "group": {
            "primary": ["docker-expert", "aws-serverless"],
            "support": ["ci-cd-and-automation", "deployment-patterns"],
            "review": [],
            "notes": "",
        },
    },
    {
        "pattern": ["可观测", "observability", "监控", "monitoring", "tracing"],
        "categories": ["engineering-code"],
        "group": {
            "primary": ["observability-engineer", "distributed-tracing"],
            "support": ["grafana-dashboards", "slo-implementation"],
            "review": [],
            "notes": "observability-engineer 做监控架构，distributed-tracing 做链路追踪",
        },
    },
    {
        "pattern": ["事故", "incident", "postmortem", "故障复盘"],
        "categories": ["engineering-code"],
        "group": {
            "primary": ["incident-responder", "postmortem-writing"],
            "support": ["slo-implementation"],
            "review": [],
            "notes": "incident-responder 做响应，postmortem-writing 做无责复盘",
        },
    },
    {
        "pattern": ["无障碍", "accessibility", "WCAG", "a11y"],
        "categories": ["security-compliance", "design-media"],
        "group": {
            "primary": ["accessibility-compliance-accessibility-audit"],
            "support": ["better-accessibility"],
            "review": [],
            "notes": "",
        },
    },
]



def normalize(text: str) -> str:
    return text.casefold().replace("_", "-")


def query_terms(query: str) -> list[str]:
    query = normalize(query)
    terms = re.findall(r"[a-z0-9][a-z0-9.+#/-]*|[\u3400-\u9fff]+", query)
    expanded: list[str] = []
    for term in terms:
        expanded.append(term)
        if re.fullmatch(r"[\u3400-\u9fff]{4,}", term):
            expanded.extend(term[index : index + 2] for index in range(len(term) - 1))
    return list(dict.fromkeys(expanded))


def build_synonym_index() -> dict[str, list[str]]:
    index: dict[str, list[str]] = {}
    for group in SYNONYM_GROUPS:
        kws = group["keywords"]
        for kw in kws:
            key = kw.lower().replace(" ", "-")
            index[key] = [k.lower() for k in kws if k.lower() != key]
    return index


def expand_with_synonyms(terms: list[str], syn_index: dict[str, list[str]]) -> list[str]:
    extra: list[str] = []
    for term in terms:
        key = term.lower().replace(" ", "-")
        if key in syn_index:
            extra.extend(syn_index[key])
    return list(dict.fromkeys(terms + extra))


def detect_intent_categories(query: str) -> list[str]:
    q = query.lower()
    categories: list[str] = []
    if any(w in q for w in ["写", "文章", "文案", "改稿", "翻译", "润色", "公众号", "博客",
                             "writing", "article", "blog", "edit", "revise", "translate"]):
        categories.append("writing-content")
    if any(w in q for w in ["开发", "代码", "编程", "debug", "调试", "部署", "api", "前端",
                             "后端", "网页", "html", "css", "deploy", "code", "develop",
                             "build", "test", "测试", "kubernetes", "k8s", "截图", "screenshot",
                             "架构", "系统设计", "architecture", "system design"]):
        categories.append("engineering-code")
    if any(w in q for w in ["论文", "科研", "综述", "文献", "引用", "实验", "统计", "学术",
                             "paper", "research", "citation", "experiment", "statistics",
                             "academic", "scientific", "review", "reproduce"]):
        categories.append("research-science")
    if any(w in q for w in ["设计", "海报", "PPT", "演示", "UI", "品牌", "配色", "视频",
                             "动画", "动效", "design", "poster", "presentation", "video",
                             "animation", "motion", "visual", "slides", "ppt", "brand"]):
        # Exclude architecture/system design which belongs to engineering
        if not any(w in q for w in ["架构", "系统设计", "architecture", "system design"]):
            categories.append("design-media")
    if any(w in q for w in ["数据", "图表", "分析", "可视化", "dashboard", "统计",
                             "data", "chart", "plot", "visualization", "analytics",
                             "pandas", "matplotlib", "excel", "表格"]):
        categories.append("documents-data")
    if any(w in q for w in ["营销", "定价", "竞品", "市场调研", "运营", "产品", "商业",
                             "融资", "落地页", "marketing", "pricing", "competitor",
                             "market", "product", "business", "strategy", "landing"]):
        categories.append("business-strategy")
    if any(w in q for w in ["安全", "漏洞", "审计", "隐私", "渗透", "加密", "合规",
                             "security", "vulnerability", "audit", "privacy", "penetration",
                             "encrypt", "compliance", "accessibility"]):
        categories.append("security-compliance")
    if any(w in q for w in ["多agent", "并行", "拆分", "决策", "工作流", "编排",
                             "multi-agent", "parallel", "decision", "workflow", "orchestrat"]):
        categories.append("agents-orchestration")
    return categories


def match_skill_group(query: str) -> dict | None:
    """Match query against predefined skill group patterns."""
    q = query.lower()
    best_match = None
    best_score = 0
    for entry in SKILL_GROUPS:
        score = sum(1 for p in entry["pattern"] if p.lower() in q)
        if score > best_score:
            best_score = score
            best_match = entry
    return best_match if best_score > 0 else None


def score(record: dict[str, object], terms: list[str], full_query: str,
          intent_categories: list[str]) -> int:
    name = normalize(str(record["name"]))
    description = normalize(str(record["description"]))
    path = normalize(str(record["path"]))
    category = normalize(str(record["category"]))
    total = TIER_BONUS.get(str(record["tier"]), 0)
    if is_alias(record):
        total -= 10
    if record.get("sourceStatus") == "upstream-deprecated":
        total -= 4
    if full_query and full_query in f"{name} {description} {path}":
        total += 25
    if intent_categories and category in [c.replace("-", "-") for c in intent_categories]:
        total += 15
    for term in terms:
        if term == name:
            total += 30
        elif term in name:
            total += 14
        if term in description:
            total += 6
        if term in path:
            total += 4
        if term in category:
            total += 2
    return total


def resolve_skill_name(name: str, records: list[dict]) -> dict | None:
    """Find a skill record by name."""
    norm = name.lower()
    # Try exact name match first
    for r in records:
        if r["name"].lower() == norm:
            return r
    # Try partial match
    for r in records:
        if norm in r["name"].lower() or r["name"].lower() in norm:
            return r
    return None


def build_group_output(group_def: dict, records: list[dict]) -> dict:
    """Build a structured skill group from a group definition."""
    result = {
        "roles": {},
        "notes": group_def["group"].get("notes", ""),
    }
    for role in ("primary", "support", "review", "orchestrate"):
        skill_names = group_def["group"].get(role, [])
        resolved = []
        for name in skill_names:
            rec = resolve_skill_name(name, records)
            if rec:
                resolved.append({
                    "name": rec["name"],
                    "path": rec["path"],
                    "category": rec.get("category", ""),
                    "description": rec.get("description", "")[:120],
                    "role": role,
                })
        if resolved:
            result["roles"][role] = resolved
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("query", help="Task description or keywords")
    parser.add_argument("--limit", type=int, default=12)
    parser.add_argument("--category")
    parser.add_argument("--include-variants", action="store_true")
    parser.add_argument("--include-aliases", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--intent", action="store_true",
                        help="Enable intent-aware mode with synonym expansion")
    parser.add_argument("--group", action="store_true",
                        help="Return a complete skill group for the task")
    return parser.parse_args()


def load_all_records() -> list[dict]:
    records = json.loads(CATALOG.read_text(encoding="utf-8"))["skills"]
    for supplemental_name in ("official-skills.json", "research-skills.json",
                              "curated-skills.json", "new-source-skills.json"):
        supplemental_catalog = REPO / "catalog" / supplemental_name
        if supplemental_catalog.is_file():
            records.extend(json.loads(supplemental_catalog.read_text(encoding="utf-8"))["skills"])
    return records


def print_group(group_output: dict, matched_def: dict) -> None:
    """Pretty-print a skill group."""
    role_labels = {
        "primary": "🎯 主技能（负责交付物）",
        "support": "🔧 支撑技能（补足领域/证据）",
        "review": "🔍 审查技能（质量把关）",
        "orchestrate": "🤖 协调技能（多Agent拆分）",
    }
    categories = matched_def.get("categories", [])
    print(f"📋 任务类别: {', '.join(categories)}")
    print()
    for role in ("primary", "support", "review", "orchestrate"):
        skills = group_output["roles"].get(role, [])
        if skills:
            print(f"  {role_labels[role]}")
            for s in skills:
                desc = s["description"][:100] + "..." if len(s["description"]) > 100 else s["description"]
                print(f"    • {s['name']}  [{s['category']}]")
                print(f"      路径: {s['path']}")
                if desc:
                    print(f"      说明: {desc}")
            print()
    if group_output["notes"]:
        print(f"  ⚠️  注意事项: {group_output['notes']}")
    print()


def main() -> None:
    args = parse_args()
    if not CATALOG.is_file():
        raise SystemExit("catalog missing; run: python build_catalog.py")

    records = load_all_records()
    alias_index = load_alias_index()
    records = [annotate_alias(record, alias_index) for record in records]

    # ── Group mode ────────────────────────────────────────────────────────
    if args.group:
        matched = match_skill_group(args.query)
        if matched:
            group_output = build_group_output(matched, records)
            if args.as_json:
                print(json.dumps(group_output, ensure_ascii=False, indent=2))
            else:
                print_group(group_output, matched)
            # Also show additional matches via keyword search
            print("  📎 其他可能相关的技能:")
            terms = query_terms(args.query)
            syn_index = build_synonym_index()
            terms = expand_with_synonyms(terms, syn_index)
            intent_cats = matched.get("categories", [])
            full_query = normalize(args.query.strip())
            # Collect names already in the group
            group_names = set()
            for role_skills in group_output["roles"].values():
                for s in role_skills:
                    group_names.add(s["name"].lower())
            ranked = []
            for record in records:
                if not args.include_variants and record["tier"] == "variant":
                    continue
                if not args.include_aliases and is_alias(record):
                    continue
                if args.category and record["category"] != args.category:
                    continue
                relevance = score(record, terms, full_query, intent_cats)
                baseline = TIER_BONUS.get(str(record["tier"]), 0)
                if is_alias(record):
                    baseline -= 10
                if relevance > baseline and record["name"].lower() not in group_names:
                    ranked.append((relevance, record))
            ranked.sort(key=lambda x: -x[0])
            for relevance, record in ranked[:8]:
                desc = str(record.get("description", ""))[:100]
                print(f"    [{relevance:>3}] {record['name']}  ({record.get('category','')})")
                print(f"          {record['path']}")
                if desc:
                    print(f"          {desc}")
            return
        else:
            # No predefined group matched; fall through to intent mode
            print("  ℹ️  没有预设技能组匹配，切换到意图搜索模式…\n")
            args.intent = True

    # ── Intent / keyword mode ─────────────────────────────────────────────
    terms = query_terms(args.query)
    intent_categories: list[str] = []
    if args.intent:
        syn_index = build_synonym_index()
        terms = expand_with_synonyms(terms, syn_index)
        intent_categories = detect_intent_categories(args.query)

    full_query = normalize(args.query.strip())
    ranked = []
    for record in records:
        if not args.include_variants and record["tier"] == "variant":
            continue
        if not args.include_aliases and is_alias(record):
            continue
        if args.category and record["category"] != args.category:
            continue
        relevance = score(record, terms, full_query, intent_categories)
        baseline = TIER_BONUS.get(str(record["tier"]), 0)
        if is_alias(record):
            baseline -= 10
        if relevance > baseline:
            ranked.append((relevance, record))

    ranked.sort(key=lambda item: (-item[0], str(item[1]["name"]), str(item[1]["path"])))
    selected = [dict(record, score=relevance) for relevance, record in ranked[: max(args.limit, 0)]]

    if args.as_json:
        print(json.dumps(selected, ensure_ascii=False, indent=2))
        return

    if not selected:
        print("No matching skills. Try broader or bilingual keywords.")
        return

    if args.intent and intent_categories:
        print(f"🎯 识别到的意图类别: {', '.join(intent_categories)}")
        print()

    for record in selected:
        description = str(record["description"])
        if len(description) > 140:
            description = description[:137] + "..."
        print(f"[{record['score']:>3}] {record['name']}  ({record.get('category','')}, {record.get('tier','')})")
        print(f"      {record['path']}")
        if record.get("aliasOf"):
            print(f"      alias ({record['aliasReason']}) -> {record['aliasOf']}")
        if description:
            print(f"      {description}")


if __name__ == "__main__":
    main()
