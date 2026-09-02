# -SKILL-

孙承泽的个人 **Agent 技能库 + 研究档案**。

> 本仓库是「2026-08 旧技能库」与「2026-09 重建版」两条世界线的**完全合并体**——所有历史分支的内容均已保留，逐文件核验零丢失（2026-09-02）。结构说明见下方「目录总览」与「世界线说明」。

## 快速开始

```bash
# 用自然语言搜技能（意图识别模式）
python scripts/search_skills.py "帮我做文献综述" --intent --limit 10

# 不知道选什么：
#   根目录 SKILL.md = 通用技能路由器（任务 → 技能组）
#   TASK_ROUTING.md / AGENTS.md / GROWTH_ROADMAP.md = 路由手册 / Agent 协作约定 / 成长路线图
#   categories/     = 九大分类导航（每类含 README + skills.tsv）

# 把某个技能装到别的 Agent
python scripts/install_skills.py --name <skill> --target /path/to/skills

# 拉取 full-sources/ 子模块的上游源码（51 个上游仓库）
git submodule update --init
```

## 目录总览

| 路径 | 说明 |
| --- | --- |
| `SKILL.md` | 通用技能路由器（仓库级入口技能） |
| `TASK_ROUTING.md` / `AGENTS.md` / `GROWTH_ROADMAP.md` | 路由手册 / Agent 协作约定 / 成长路线图 |
| `超级大脑洞察报告.md` | 2026-08-31，基于全部 33 个仓库交叉核验的个人洞察 |
| `Agent驾驭力训练手册.md` | 2026-08-31，Agent 驾驭能力提升方案（资源逐条核验） |
| `四个月脚印计划-2026Sep-Dec.md` | 2026-09-01 制定，9–12 月 22 步计划（每步 ≤3h） |
| `skills/community/academic-research-skills/` | ⭐ 学术研究四件套 v3.3.1（897 文件，完整）：deep-research / academic-paper / academic-paper-reviewer / academic-pipeline。来源 Imbad0202 @ `94436237`，CC-BY-NC-4.0（非商业） |
| `skills/community/scientific-agent-skills/` | ⭐ 163 个自包含科学计算技能 v2.65.0（生物/化学/医学/AI）。来源 K-Dense-AI @ `1dd0fccf`, MIT |
| `skills/community/nuwa-distilled/` | 女娲蒸馏系：`sun-chengze-perspective`（v1.1，9 月新版，四轮访谈）+ 旧版 68 个子技能（book-*、perspective-*、ai-futures-scenario-lab、senpai-council、`tracks/track-paper-aso` 论文研读路线等） |
| `skills/community/*-legacy-snapshot-2026-08-31/` | 8 月旧版快照（academic-research-skills v3.2.0 部分拷贝、scientific-agent-skills 157 技能版）——规范位置已有更新版本，确认无用后可整目录删除 |
| `skills/core/` | 核心学科技能（概率论、分析哲学、年鉴学派、AI 伦理与法律……） |
| `skills/variants/` | 部分社区集合的变体版本 |
| `skills/research-workflow-kit/` | 科研工作流套件 |
| `bundles/` | 两个可离线安装的礼包：`newcomer-starter-pack`（100 项基础技能，15MB tarball）、`research-workflow-kit`（659 payload + 8 profiles） |
| `full-sources/` | 51 个上游来源子模块（`.gitmodules`），含本人的 turbine-blade-ai-platform / wind_farm_viz 等 |
| `tools/` | 工具：opencut、openwiki、rustdesk、screencoder、spec-kit |
| `catalog/` / `categories/` | 技能索引（JSON/TSV）与九大分类导航 |
| `governance/` | AI_CABINET / CONSTITUTION / 多 Agent 编排 / 质量门禁 |
| `guides/` | 使用、检索、来源、工具、领域适配等 6 篇指南 |
| `scripts/` / `tests/` | 检索/安装/校验脚本 与 对应测试 |
| `third_party/` | 第三方许可声明 |
| `README.legacy-vault-2026-08-31.md` | 8 月旧版仓库 README（233 行，含 3,100 候选技能、九大分类、礼包说明） |

## 世界线说明（为什么结构看着像两个仓库）

| 时间 | 分支 | 内容 | 现状 |
| --- | --- | --- | --- |
| 2026-08-16 | `arena/019ffbe9-skill`、`arena/01a0095c-skill` | 旧技能库早期（被 01a048e7 包含） | ✅ 已合入 |
| 2026-08-31 | `arena/01a048e7-skill` | 旧技能库完整版（universal-skill-router + 54 集合 + vault 结构） | ✅ 已合入（2026-09-02） |
| 2026-08-31 | `arena/01a0582f-skill` | 3 篇个人文档 | ✅ 已合入（2026-09-02） |
| 2026-09-01 | `arena/01a0582a-skill`（PR#1） | sun-chengze-perspective v1.1 | ✅ 已在 main |
| 2026-09-02 | `arena/01a06000-skill`（PR#2 + 本次整理） | 两个新技能集合 + 旧世界线合回 | ✅ 本分支 |

- 重叠处理原则：**同集合保留最新版在规范位置，旧版移入 `*-legacy-snapshot-2026-08-31/` 归档**，不丢任何文件。
- 旧分支本身保留在 GitHub 上未删除，随时可再核对。

## 许可注意

`skills/community/academic-research-skills/`（及其旧快照）为 **CC-BY-NC-4.0（非商业用途）**；`scientific-agent-skills` 为 MIT；其余集合各有自己的 LICENSE/NOTICE（见 `third_party/`）。若本仓库未来公开或商用，需逐集合核对。
