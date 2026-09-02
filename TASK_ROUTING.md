# 任务 → 技能路由手册

> 本文档是 Agent 的「任务场景 → 技能推荐」速查表。
> 当用户指派任何任务时，先在此表中找到匹配场景，再加载对应技能。

---

## 一、写作与内容生产

### 1.1 通用中文写作

| 用户意图 | 推荐技能 | 路径 |
|---|---|---|
| 写文章、博客、回答、故事 | **human-writing** | `skills/community/human-writing/SKILL.md` |
| 去掉 AI 腔/模板味 | **stop-slop** | `skills/core/stop-slop/SKILL.md` |
| 让文本更自然/去 AI 痕迹 | **humanizer-zh** | `skills/core/humanizer-zh/SKILL.md` |
| 知乎/论坛长回答 | **human-writing** | `skills/community/human-writing/SKILL.md` |
| 公众号/博客文章 | **human-writing** | `skills/community/human-writing/SKILL.md` |
| 小说/故事/对白 | **human-writing** | `skills/community/human-writing/SKILL.md` |
| 科普/教程/评测文 | **human-writing** | `skills/community/human-writing/SKILL.md` |
| 口播稿/演讲稿 | **human-writing** | `skills/community/human-writing/SKILL.md` |

### 1.2 英文学术写作

| 用户意图 | 推荐技能 | 路径 |
|---|---|---|
| 论文润色/翻译为 Nature 风格 | **nature-polishing** | `skills/community/nature-skills/skills/nature-polishing/SKILL.md` |
| 添加严格引用 | **nature-citation** | `skills/community/nature-skills/skills/nature-citation/SKILL.md` |
| 论文完整写作流程 | **research-paper-writing** | `skills/community/Research-Paper-Writing-Skills-main/research-paper-writing/SKILL.md` |

### 1.3 内容运营

| 用户意图 | 推荐技能 | 路径 |
|---|---|---|
| X/Twitter 运营 | **x-mastery-mentor** | `skills/community/nuwa-skill/examples/x-mastery-mentor/SKILL.md` |
| 内容传播/病毒式扩散 | **book-berger-contagious** | `skills/community/nuwa-distilled/book-berger-contagious/SKILL.md` |
| SEO 优化 | **qiaomu-seo** | `skills/community/qiaomu-seo/SKILL.md` |
| AI 文案批量生产 | **ai-copywriter** | `full-sources/curated/ai-copywriter/SKILL.md` |

---

## 二、工程与代码

### 2.1 调试与排错

| 用户意图 | 推荐技能 | 路径 |
|---|---|---|
| 通用系统调试 | **systematic-debugging** | `full-sources/official/openai-plugins/plugins/superpowers/skills/systematic-debugging/SKILL.md` |
| Python 调试 | **python-debugpy** | `full-sources/research/hermes-agent/skills/software-development/python-debugpy/SKILL.md` |
| 前端测试调试 | **frontend-testing-debugging** | `full-sources/official/openai-plugins/plugins/build-web-apps/skills/frontend-testing-debugging/SKILL.md` |
| 构建/运行/调试 | **build-run-debug** | `full-sources/official/openai-plugins/plugins/build-macos-apps/skills/build-run-debug/SKILL.md` |
| 系统性错误恢复 | **debugging-and-error-recovery** | `skills/community/agent-skills-main/skills/debugging-and-error-recovery/SKILL.md` |

### 2.2 前端与网页开发

| 用户意图 | 推荐技能 | 路径 |
|---|---|---|
| 截图转 HTML/CSS | **screencoder** | `tools/screencoder/SKILL.md` |
| 前端设计方向 | **frontend-design-direction** | `skills/community/ECC/skills/frontend-design-direction/SKILL.md` |
| 前端幻灯片/网页 PPT | **frontend-slides** | `skills/community/ECC/skills/frontend-slides/SKILL.md` |
| UI Demo 原型 | **ui-demo** | `skills/community/ECC/skills/ui-demo/SKILL.md` |
| Angular 开发 | **angular-developer** | `skills/community/ECC/skills/angular-developer/SKILL.md` |
| Django 开发 | **django-patterns** | `skills/community/ECC/skills/django-patterns/SKILL.md` |
| Laravel 开发 | **laravel-patterns** | `skills/community/ECC/skills/laravel-patterns/SKILL.md` |
| MySQL 开发 | **mysql-patterns** | `skills/community/ECC/skills/mysql-patterns/SKILL.md` |
| 3D 网页 (img→three.js) | **img2threejs** | `skills/community/img2threejs/SKILL.md` |

### 2.3 后端与基础设施

| 用户意图 | 推荐技能 | 路径 |
|---|---|---|
| API 设计 | **api-design** | `skills/community/ECC/skills/api-design/SKILL.md` |
| Kubernetes | **kubernetes-patterns** | `skills/community/ECC/skills/kubernetes-patterns/SKILL.md` |
| Helm Chart | **helm-chart-builder** | `skills/community/alirezarezvani-claude-skills/engineering/helm-chart-builder/SKILL.md` |
| 部署模式 | **deployment-patterns** | `skills/community/ECC/skills/deployment-patterns/SKILL.md` |
| Monorepo 导航 | **monorepo-navigator** | `skills/community/alirezarezvani-claude-skills/engineering/skills/monorepo-navigator/SKILL.md` |
| CI/CD 自动化 | **ci-cd-and-automation** | `skills/community/agent-skills-main/skills/ci-cd-and-automation/SKILL.md` |
| 规范驱动开发 | **spec-kit** | `tools/spec-kit/SKILL.md` |

### 2.4 代码质量与审查

| 用户意图 | 推荐技能 | 路径 |
|---|---|---|
| 代码审查 | **open-code-review** | `skills/community/open-code-review/SKILL.md` |
| 代码变更追溯 | **change-traceability-review** | `full-sources/curated/change-traceability-review/SKILL.md` |
| 代码行血缘追踪 | **trace-file-lineage** | `full-sources/curated/trace-file-lineage/SKILL.md` |

### 2.5 AI/ML 工程

| 用户意图 | 推荐技能 | 路径 |
|---|---|---|
| ML 工程工作流 | **mle-workflow** | `skills/community/ECC/skills/mle-workflow/SKILL.md` |
| 高级 AI Agent 工程 | **ai-agent-engineering** | `skills/community/ai-agent-engineering/SKILL.md` |
| D2L 深度学习实验 | **d2l-lab-backbone** | `skills/community/nuwa-distilled/d2l-lab-backbone/SKILL.md` |
| ML 实验管理 | **ml-experiment** (profile) | `bundles/research-workflow-kit/profiles/ml-experiment.json` |
| 资深数据科学家 | **senior-data-scientist** | `skills/community/alirezarezvani-claude-skills/engineering-team/skills/senior-data-scientist/SKILL.md` |
| 上下文工程 | **context-engineering** | `skills/community/agent-skills-main/skills/context-engineering/SKILL.md` |

---

## 三、研究与科学

### 3.1 科研全生命周期

| 用户意图 | 推荐技能 | 路径 |
|---|---|---|
| 科研总入口/路由 | **research-expert-system** | `skills/core/research-expert-system/SKILL.md` |
| 科研流程总控 | **research-workflow-orchestrator** | `skills/research-workflow-kit/research-workflow-orchestrator/SKILL.md` |
| 文献检索与综述 | **systematic-evidence-synthesis** | `skills/research-workflow-kit/systematic-evidence-synthesis/SKILL.md` |
| 研究问题设计 | **research-question-protocol** | `skills/research-workflow-kit/research-question-protocol/SKILL.md` |
| 可复现分析 | **reproducible-research-analysis** | `skills/research-workflow-kit/reproducible-research-analysis/SKILL.md` |
| 学术诚信/AI 披露 | **academic-integrity-ai-disclosure** | `skills/research-workflow-kit/academic-integrity-ai-disclosure/SKILL.md` |
| 质性研究方法 | **qualitative-mixed-methods** | `skills/research-workflow-kit/qualitative-mixed-methods/SKILL.md` |

### 3.2 科研绘图与数据可视化

| 用户意图 | 推荐技能 | 路径 |
|---|---|---|
| Nature 风格图表 | **nature-figure** | `skills/community/nature-skills/skills/nature-figure/SKILL.md` |
| 科研数据可视化顾问 | **scipilot-figure-skill** | `skills/community/scipilot-figure-skill/SKILL.md` |
| 论文图表 (figures4papers) | **figures4papers** | `full-sources/curated/figures4papers/SKILL.md` |
| 海报 (Scientific) | **pptx-posters** | `skills/community/scientific-agent-skills/skills/pptx-posters/SKILL.md` |

### 3.3 文献搜索

| 用户意图 | 推荐技能 | 路径 |
|---|---|---|
| Nature 学术搜索 | **nature-academic-search** | `skills/community/nature-skills/skills/nature-academic-search/SKILL.md` |
| 全网调研 | **agent-reach** | `skills/community/agent-reach/agent_reach/skill/SKILL.md` |
| 浏览器自动化 | **browser-use** / **playwright** | `skills/community/browser-use/SKILL.md` |

### 3.4 因果推断与审计

| 用户意图 | 推荐技能 | 路径 |
|---|---|---|
| 因果推断/what-if 分析 | **book-what-if-causal-audit** | `skills/community/nuwa-distilled/book-what-if-causal-audit/SKILL.md` |
| 目标试验模拟 | **emulate_target_trial** | `skills/community/nuwa-distilled/book-what-if-causal-audit/scripts/emulate_target_trial.py` |

---

## 四、设计与视觉

### 4.1 综合设计系统

| 用户意图 | 推荐技能 | 路径 |
|---|---|---|
| 海报设计 | **victor-design-system** (poster) | `skills/community/victor-design/SKILL.md` |
| PPT/演示设计 | **victor-design-system** (slides) | `skills/community/victor-design/SKILL.md` |
| 产品 UI 设计 | **victor-design-system** (product-ui) | `skills/community/victor-design/SKILL.md` |
| 社交图文设计 | **victor-design-system** (graphic-text) | `skills/community/victor-design/SKILL.md` |
| 设计评审 | **design-evaluation** | `full-sources/curated/design-evaluation/SKILL.md` |

### 4.2 图像生成

| 用户意图 | 推荐技能 | 路径 |
|---|---|---|
| GPT Image 生图 | **gpt-image-2-skill** | `skills/community/gpt-image-2-skill/SKILL.md` |
| fal.ai 媒体生成 | **fal-ai-media** | `skills/community/ECC/skills/fal-ai-media/SKILL.md` |
| 故事转手绘视频 | **story-to-handdrawn-video** | `full-sources/curated/story-to-handdrawn-video/SKILL.md` |
| 剪影/抠图 | **cutout_subject.py** | `skills/community/victor-design/scripts/cutout_subject.py` |

### 4.3 网页设计

| 用户意图 | 推荐技能 | 路径 |
|---|---|---|
| 流行网页设计参考 | **popular-web-designs** | `full-sources/curated/popular-web-designs/SKILL.md` |
| UI/UX Pro | **ui-ux-pro-max** | `skills/community/ui-ux-pro-max/SKILL.md` |
| 动效系统 | **motion-ui** / **motion-patterns** | `skills/community/ECC/skills/motion-ui/SKILL.md` |
| 无障碍设计 | **better-accessibility** | `full-sources/curated/better-accessibility/SKILL.md` |
|  Bento 幻灯片 | **bento-slides** | `full-sources/curated/bento-slides/SKILL.md` |

---

## 五、视频与动效

| 用户意图 | 推荐技能 | 路径 |
|---|---|---|
| 电影级产品视频 | **video-shotcraft** | `full-sources/curated/video-shotcraft/SKILL.md` |
| Remotion 视频制作 | **remotion-video-creation** | `skills/community/ECC/skills/remotion-video-creation/SKILL.md` |
| 通用视频编辑 | **video-editing** | `skills/community/ECC/skills/video-editing/SKILL.md` |
| 视频数据库管理 | **videodb** | `skills/community/ECC/skills/videodb/SKILL.md` |
| Manim 数学动画 | **manim-video** | `skills/community/ECC/skills/manim-video/SKILL.md` |
| 动效基础 | **motion-foundations** | `skills/community/ECC/skills/motion-foundations/SKILL.md` |
| 高级动效 | **motion-advanced** | `skills/community/ECC/skills/motion-advanced/SKILL.md` |
| 本地视频编辑工具 | **opencut** | `tools/opencut/SKILL.md` |
| Claude 视频生成 | **claude-video** | `skills/community/claude-video/SKILL.md` |
| Demo 视频 | **demo-video** | `skills/community/alirezarezvani-claude-skills/engineering/demo-video/skills/demo-video/SKILL.md` |
| 产品视频/油动效 | **oil-motion** | `full-sources/curated/oil-motion/SKILL.md` |

---

## 六、文档、数据与演示

### 6.1 PPT/演示文稿

| 用户意图 | 推荐技能 | 路径 |
|---|---|---|
| 咨询风格 PPTX | **cyber-ppt** | `full-sources/curated/cyberppt/SKILL.md` |
| 论文转 Nature PPT | **nature-paper2ppt** | `skills/community/nature-skills/skills/nature-paper2ppt/SKILL.md` |
| 通用 PPTX 制作 | **pptx** | `skills/community/skills-main/skills/pptx/SKILL.md` |
| 科研海报 PPTX | **pptx-posters** | `skills/community/scientific-agent-skills/skills/pptx-posters/SKILL.md` |
| 归藏网页 PPT | **guizang-ppt-skill** | `skills/community/guizang-ppt-skill-main/SKILL.md` |
| Bolt 幻灯片 | **bolt-slides** | `full-sources/curated/bolt-slides/SKILL.md` |
| 小说大纲/文档 | **novel-outline** | `full-sources/curated/novel-outline/SKILL.md` |

### 6.2 数据分析

| 用户意图 | 推荐技能 | 路径 |
|---|---|---|
| Dashboard 构建 | **dashboard-builder** | `skills/community/ECC/skills/dashboard-builder/SKILL.md` |
| 数据抓取 | **data-scraper-agent** | `skills/community/ECC/skills/data-scraper-agent/SKILL.md` |
| 可复现研究分析 | **reproducible-research-analysis** | `skills/research-workflow-kit/reproducible-research-analysis/SKILL.md` |
| 任何文档处理 | **anydoc** | `full-sources/curated/anydoc/SKILL.md` |

---

## 七、商业与策略

| 用户意图 | 推荐技能 | 路径 |
|---|---|---|
| 市场调研 | **market-research** | `skills/community/ECC/skills/market-research/SKILL.md` |
| 营销方案 | **marketing-campaign** | `skills/community/ECC/skills/marketing-campaign/SKILL.md` |
| 竞品分析 | **competitive-platform-analysis** | `skills/community/ECC/skills/competitive-platform-analysis/SKILL.md` |
| 竞品报告 | **competitive-report-structure** | `skills/community/ECC/skills/competitive-report-structure/SKILL.md` |
| 品牌发现 | **brand-discovery** | `skills/community/ECC/skills/brand-discovery/SKILL.md` |
| 营销获客 | **marketing-demand-acquisition** | `skills/community/alirezarezvani-claude-skills/marketing-skill/skills/marketing-demand-acquisition/SKILL.md` |
| Landing Page | **landing** | `skills/community/alirezarezvani-claude-skills/marketing/landing/skills/landing/SKILL.md` |
| 商业运营 | **business-operations-skills** | `skills/community/alirezarezvani-claude-skills/business-operations/skills/business-operations-skills/SKILL.md` |
| 商业技能 | **commercial-skills** | `skills/community/alirezarezvani-claude-skills/commercial/skills/commercial-skill/SKILL.md` |
| 财务/计费 | **finance-billing-ops** / **customer-billing-ops** | `skills/community/ECC/skills/finance-billing-ops/SKILL.md` |
| 产品分析师 | **cs-product-analyst** | `skills/community/alirezarezvani-claude-skills/.gemini/skills/cs-product-analyst/SKILL.md` |
| 公司 OS | **company-os** | `skills/community/alirezarezvani-claude-skills/c-level-advisor/skills/company-os/SKILL.md` |

### 决策与战略思维

| 用户意图 | 推荐技能 | 路径 |
|---|---|---|
| 重要决策/方案比较 | **ai-cabinet** | `skills/core/ai-cabinet/SKILL.md` |
| 鬼谷子式谈判/谋略 | **guiguzi** | `skills/community/guiguzi/SKILL.md` |
| 渔樵问对式追问 | **yuqiao-wendui** | `skills/community/yuqiao-wendui/SKILL.md` |
| 高层决策诊断 | **challenge** | `skills/community/alirezarezvani-claude-skills/c-level-advisor/executives/challenge/SKILL.md` |
| 组织健康诊断 | **org-health-diagnostic** | `skills/community/alirezarezvani-claude-skills/c-level-advisor/skills/org-health-diagnostic/SKILL.md` |

---

## 八、安全与合规

| 用户意图 | 推荐技能 | 路径 |
|---|---|---|
| 综合安全审计 | **security-audit** | `skills/community/buildwithclaude-hub/plugins/agent-triforce/skills/security-audit/SKILL.md` |
| 技能安全审计 | **skill-security-auditor** | `skills/community/alirezarezvani-claude-skills/engineering/skills/skill-security-auditor/SKILL.md` |
| 渗透测试 | **security-pen-testing** | `skills/community/alirezarezvani-claude-skills/engineering-team/skills/security-pen-testing/SKILL.md` |
| 安全扫描 | **security-scan** | `full-sources/official/openai-plugins/plugins/codex-security/skills/security-scan/SKILL.md` |
| 深度安全扫描 | **deep-security-scan** | `full-sources/official/openai-plugins/plugins/codex-security/skills/deep-security-scan/SKILL.md` |
| 漏洞报告 | **vulnerability-writeup** | `full-sources/official/openai-plugins/plugins/codex-security/skills/vulnerability-writeup/SKILL.md` |
| 安全加固 | **propose-security-hardening** | `full-sources/official/openai-plugins/plugins/codex-security/skills/propose-security-hardening/SKILL.md` |
| 隐私审计 (Context Flow) | **book-privacy-context-flow-audit** | `skills/community/nuwa-distilled/book-privacy-context-flow-audit/SKILL.md` |
| AI 安全控制审计 | **book-safer-world-control-audit** | `skills/community/nuwa-distilled/book-safer-world-control-audit/SKILL.md` |
| 伦理算法约束 | **book-ethical-algorithm-constraints** | `skills/community/nuwa-distilled/book-ethical-algorithm-constraints/SKILL.md` |
| ISO 27001 ISMS | **information-security-manager-iso27001** | `skills/community/alirezarezvani-claude-skills/ra-qm-team/skills/information-security-manager-iso27001/SKILL.md` |
| ISMS 审计 | **isms-audit-expert** | `skills/community/alirezarezvani-claude-skills/ra-qm-team/skills/isms-audit-expert/SKILL.md` |
| 合规 OS | **compliance-os** | `skills/community/alirezarezvani-claude-skills/compliance-os/skills/compliance-os/SKILL.md` |
| DeepSec 安全 | **deepsec** | `skills/community/deepsec/SKILL.md` |
| 高风险分析 | **high-stakes-analytics** | `full-sources/curated/high-stakes-analytics/SKILL.md` |
| 人工审查 | **human-review** | `full-sources/curated/human-review/SKILL.md` |
| 无障碍审查 | **better-accessibility** | `full-sources/curated/better-accessibility/SKILL.md` |
| 密钥管理 | **secrets-vault-manager** | `skills/community/alirezarezvani-claude-skills/engineering/skills/secrets-vault-manager/SKILL.md` |

---

## 九、编排与协调

| 用户意图 | 推荐技能 | 路径 |
|---|---|---|
| 多 Agent 任务拆分 | **multi-agent-orchestration** | `skills/core/multi-agent-orchestration/SKILL.md` |
| 官方来源路由 | **official-source-router** | `skills/core/official-source-router/SKILL.md` |
| 技能搜索路由 | **universal-skill-router** | `SKILL.md` (本文件) |
| 记忆系统 | **memory-system** | `skills/community/memory-system/SKILL.md` |
| Agent 自主能力 | **superpowers-main** | `skills/community/superpowers-main/SKILL.md` |
| Prime Agent | **prime-agent** | `skills/community/prime-agent/SKILL.md` |

---

## 十、工具类

| 用户意图 | 推荐技能 | 路径 |
|---|---|---|
| 本地视频编辑器 | **opencut** | `tools/opencut/SKILL.md` |
| 远程桌面 | **rustdesk** | `tools/rustdesk/SKILL.md` |
| 规范驱动开发 | **spec-kit** | `tools/spec-kit/SKILL.md` |
| 代码库 Wiki 生成 | **openwiki** | `tools/openwiki/SKILL.md` |
| 截图转代码 | **screencoder** | `tools/screencoder/SKILL.md` |
| LLM Wiki 技能 | **llm-wiki-skill** | `skills/community/llm-wiki-skill-main/SKILL.md` |
| Draw.io 图表 | **drawio-skill** | `skills/community/drawio-skill/SKILL.md` |

---

## 十一、特殊能力

| 用户意图 | 推荐技能 | 路径 |
|---|---|---|
| 深度调研任何主题 | **agent-reach** | `skills/community/agent-reach/agent_reach/skill/SKILL.md` |
| 造一个"人物思维"Skill | **huashu-nuwa (女娲)** | `skills/community/nuwa-skill/SKILL.md` |
| 理解任何复杂事物 | **understand-anything** | `skills/community/understand-anything/SKILL.md` |
| 文档浏览器 GIF | **record-browser-gif** | `full-sources/curated/record-browser-gif/SKILL.md` |
| 英文简化 | **simple-english** | `full-sources/curated/simple-english/SKILL.md` |
| 免费域名服务 | **free-domain-service** | `skills/community/free-domain-service/SKILL.md` |
| GSAP 动画 | **gsap-skills** | `skills/community/gsap-skills/SKILL.md` |
| 全流程设计 | **epic-design** | `skills/community/alirezarezvani-claude-skills/engineering-team/skills/epic-design/SKILL.md` |
| GStack 全栈 | **gstack** | `skills/community/gstack/SKILL.md` |
|  taste 审美 | **taste** | `skills/community/ECC/skills/taste/SKILL.md` |
| 深度辅导 (DeepTutor) | **DeepTutor** | `skills/community/DeepTutor/SKILL.md` |
| 科研学长姐会诊 | **ai-research-senpai-council** | `skills/community/nuwa-distilled/ai-research-senpai-council/SKILL.md` |
| 个人实验工作台 | **book-tools-of-titans-experiment-lab** | `skills/community/nuwa-distilled/book-tools-of-titans-experiment-lab/SKILL.md` |
| 治理commons制度设计 | **book-governing-commons-institution-design** | `skills/community/nuwa-distilled/book-governing-commons-institution-design/SKILL.md` |

---

## 路由原则

1. **先场景后技能**：先确定用户要完成什么场景任务，再在该场景内找最佳技能
2. **最小组队**：1 主 + ≤3 互补，不要一次加载所有匹配技能
3. **主技能优先**：每个场景表的第一项通常是首选主技能
4. **中文写作必过 stop-slop**：任何中文输出交付前，检查 AI 腔
5. **科研必过人类门禁**：问题、数据、方法、引用和发布都需人工确认
6. **安全类任务双重审查**：先用领域技能执行，再用安全技能审查
7. **不确定时问用户**：意图模糊且会改变方案时，先确认再推荐

---

## 十二、代码质量与架构（新增来源: antigravity + wondelai）

### 12.1 代码整洁与重构

| 用户意图 | 🎯 主技能 | 🔧 支撑 | 🔍 审查 |
|---|---|---|---|
| 重构代码 | clean-code, code-refactoring-refactor-clean | code-reviewer | architect-review |
| 代码审查 | code-reviewer, open-code-review | architect-review | change-traceability-review |
| 架构设计 | architect-review, architecture-patterns | brainstorming, plan-writing | clean-architecture, domain-driven-design |
| DDD 领域建模 | domain-driven-design | clean-architecture, ddia-systems | — |
| TDD 测试驱动 | test-driven-development | testing-patterns | verification-before-completion |

### 12.2 技术栈专项

| 用户意图 | 🎯 主技能 | 🔧 支撑 | 🔍 审查 |
|---|---|---|---|
| React 开发 | react-patterns, react-best-practices | frontend-developer | code-reviewer |
| Python 开发 | python-patterns, python-performance-optimization | python-packaging | code-reviewer |
| TypeScript 开发 | typescript-expert | react-patterns, clean-code | code-reviewer |
| Docker 容器 | docker-expert | aws-serverless | — |
| AWS 云部署 | aws-serverless | docker-expert | — |
| SQL 优化 | sql-optimization-patterns | ddia-systems | — |
| 前端性能 | react-best-practices, web-performance-optimization | high-perf-browser | — |
| Mermaid 图表 | mermaid-expert | — | — |

### 12.3 DevOps 与运维

| 用户意图 | 🎯 主技能 | 🔧 支撑 | 🔍 审查 |
|---|---|---|---|
| 部署上线 | docker-expert, aws-serverless | ci-cd-and-automation | — |
| 监控可观测 | observability-engineer, distributed-tracing | grafana-dashboards, slo-implementation | — |
| 故障响应 | incident-responder, postmortem-writing | slo-implementation | — |
| 浏览器自动化 | playwright | browser-use, agent-browser | — |

---

## 十三、商业战略（新增来源: wondelai）

| 用户意图 | 🎯 主技能 | 🔧 支撑 | 🔍 审查 |
|---|---|---|---|
| 创业方案 | blue-ocean-strategy, good-strategy-bad-strategy | crossing-the-chasm, hundred-million-offers | — |
| 产品设计/用户习惯 | hooked-ux, design-sprint | conversion-optimization, continuous-discovery | — |
| 团队管理 | high-output-management | good-strategy-bad-strategy | — |
| 病毒传播/口碑 | contagious, book-berger-contagious | content-marketer, marketing-campaign | — |
| 转化优化/CRO | conversion-optimization | ab-test-setup, landing | — |
| SEO 优化 | seo-structure-architect, seo-audit | content-marketer, programmatic-seo | — |
| 内容营销 | content-marketer, copywriting | seo-structure-architect | — |

---

## 十四、量化与 AI（新增来源: antigravity）

| 用户意图 | 🎯 主技能 | 🔧 支撑 | 🔍 审查 |
|---|---|---|---|
| 量化交易/金融建模 | quant-analyst | data-scientist, backtesting-frameworks | — |
| 数据科学/建模 | data-scientist | python-patterns, sql-optimization-patterns | — |
| RAG/向量数据库 | rag-engineer | langgraph, prompt-engineer | — |
| 头脑风暴/创意 | brainstorming | plan-writing | — |

---

## 十五、设计与 Figma（新增来源: VoltAgent/awesome-agent-skills）

| 用户意图 | 🎯 主技能 | 🔧 支撑 | 🔍 审查 |
|---|---|---|---|
| Figma 设计→代码 | figma-implement-design, figma-use | figma-create-design-system-rules | — |
| 游戏开发 | game-design | unity-developer, godot-gdscript-patterns | — |
| 无障碍/WCAG | accessibility-compliance-accessibility-audit | better-accessibility | — |
| 文档处理 (Word/PDF) | pdf, docx | anydoc | — |
