# 技能库 (Skills)

本目录是仓库的核心技能集合，按角色和来源分层组织。

## 目录结构

```
skills/
  core/                  核心路由器与系统级技能（6 项）
  community/             社区贡献的完整技能包（50+ 项）
  variants/              同名但正文不同的轻量变体（17 项）
  research-workflow-kit/ 科研工作流专项技能（6 项）
```

## 分层说明

| 层 | 目录 | 数量 | 说明 |
|---|---|---:|---|
| 核心 | `core/` | 6 | 路由、决策、多 Agent、质量审查等基础能力 |
| 社区 | `community/` | 50+ | 来自历史并集、官方精选、科研项目的完整技能 |
| 变体 | `variants/` | 17 | 同名技能的不同实现版本 |
| 科研 | `research-workflow-kit/` | 6 | 科研全生命周期专项技能 |

## 搜索与安装

```bash
# 搜索技能
python scripts/search_skills.py "web app implementation" --limit 12

# 安装单个技能到目标 Agent
python scripts/install_skills.py --name systematic-debugging --target /path/to/skills
```
