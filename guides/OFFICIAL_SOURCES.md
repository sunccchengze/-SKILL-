# 官方来源技能层

本仓库把平台发布方维护的技能保留为**固定提交的 Git 子模块**，而不是复制到紧凑索引中。这样可以同时获得上游完整包、可审计版本和较小的主仓库体积。

> “官方来源”只表示所固定仓库由对应发布方账号维护，不表示本仓库替发布方背书，也不表示仓库内所有内容采用同一许可证。

## 当前固定范围

| 来源 | 固定提交 | `SKILL.md` | 许可口径 | 状态 |
|---|---|---:|---|---|
| OpenAI Plugins | `11c74d6ba24d3a6d48f54a194cd00ef3beea18f9` | 608 | 混合、按插件/技能核验；无根许可证 | 当前 Codex 插件市场来源 |
| OpenAI Skills | `49f948faa9258a0c61caceaf225e179651397431` | 44 | 按技能目录内许可证核验 | 上游已标记 deprecated；保留为旧版审计快照 |
| Vercel Agent Skills | `b8caa260a420a73042e35521de4b5c8baf6446cc` | 9 | 固定 README 声明 MIT，但没有独立根许可证文件 | 当前固定快照 |
| Microsoft Skills | `e58528db9a006528a5fb0a2c029790fa6a9a7c0e` | 198 | 根许可证 MIT；仍需遵守插件内附加 notices/许可证 | 当前固定快照 |

合计 **859** 个原始入口。机器目录 [`catalog/official-skills.json`](../catalog/official-skills.json) 保留每条上游路径，其稳定身份是 `sourceId:上游路径`；来源、版本和许可口径锁在 [`catalog/sources.lock.json`](../catalog/sources.lock.json)。默认搜索通过 [`catalog/overlap-policy.json`](../catalog/overlap-policy.json) 隐藏 19 个可解析别名，显示 840 个官方主入口：3 个 exact-blob 包装副本，以及 deprecated `openai-skills` 中 16 个已有当前 `openai-plugins` 同名后继的入口。上游 gitlink、原目录记录和显式安装能力均未删除。

## 查找与安装

搜索会同时读取紧凑目录、官方目录、科研目录和精选目录：

```bash
python scripts/search_skills.py "github review comments"
python scripts/search_skills.py "Azure deploy" --json
python scripts/search_skills.py "React performance" --category engineering-code
# 审计包装副本或 deprecated 入口时才展开别名
python scripts/search_skills.py "gh-address-comments" --include-aliases --json
```

只初始化需要的官方来源，或一次初始化全部来源：

```bash
git submodule update --init full-sources/official/openai-plugins
git submodule update --init full-sources/official/microsoft-skills
git submodule update --init --recursive
```

将选中的完整技能包复制到 Agent 技能目录：

```bash
python scripts/install_skills.py \
  --name gh-address-comments \
  --source openai-plugins \
  --target ~/.agents/skills
```

若同一来源内仍有同名入口，用目录中的精确 `path` 消除歧义：

```bash
python scripts/install_skills.py \
  --name react-best-practices \
  --source openai-plugins \
  --path full-sources/official/openai-plugins/plugins/vercel/skills/react-best-practices/SKILL.md \
  --target ~/.agents/skills
```

`--dry-run` 可在不复制文件时展示选定来源、目标和许可证标签。完整物化工具会把这些来源放在 `full-library/official/`，并写入 `MANIFEST.json`：

```bash
python scripts/materialize_full_library.py
```

## 选择规则

1. 产品或平台专属任务优先选择该平台**当前**官方来源，例如新 Codex 能力优先 `openai-plugins`。
2. 本仓库维护入口承担治理、路由或跨来源组合时，优先使用维护入口，再调用官方技能作为专家包。
3. `openai-skills` 是上游已弃用的旧来源。16 个同名后继默认转到当前 Plugins；只有需要旧行为或复现实验时才用 `--source openai-skills` 或精确 `--path` 选择别名。
4. 同名本身不是压缩依据。除已审计的后继/包装规则外，仍比较 `sourceId`、路径、描述、固定提交和许可，再明确选定一个入口。
5. 使用前阅读整个技能包，不只读 `SKILL.md`；同时检查相邻 `LICENSE*`、`NOTICE*`、脚本、依赖和连接器配置。
6. 涉及发送消息、部署、删除、付费、权限、生产环境或外部连接器时，仍需显式授权、最小权限和执行前确认。

## 许可边界

- Git 子模块是指向上游固定提交的引用；初始化后获得的内容仍受各上游条款约束。
- `openai-plugins` 没有统一根许可证，不能把 608 个入口统称为 MIT 或 Apache-2.0。
- `openai-skills` 的 README 要求在各技能目录查找许可证；文件名大小写也可能不同。
- Vercel 的固定 README 声明 MIT，但固定树中没有独立根 `LICENSE`。本目录如实记录这一差异，不把缺失文件补写成上游许可证。
- Microsoft 有根 MIT 许可证，但某些插件可能包含第三方组件、数据或附加 notices；根许可证不自动覆盖所有外部权利。

### 继承的 Anthropic 文档技能

紧凑社区快照中已有以下四个目录，它们各自带有明确的限制性 `LICENSE.txt`：

- `skills/community/skills-main/skills/docx/`
- `skills/community/skills-main/skills/pdf/`
- `skills/community/skills-main/skills/pptx/`
- `skills/community/skills-main/skills/xlsx/`

其许可文本把使用行为与 Anthropic 服务协议关联，并明确限制在服务外提取或保留、复制、创作衍生作品及分发等行为。**不要把这些目录当作开放源码技能安装、复制、修改或再分发。**只有在适用协议明确授权时才使用；否则选择目录中的其他文档技能。正因为这些条款，本次没有再增加 Anthropic 当前仓库的直接官方子模块。

本说明不是法律意见；最终使用者需核验与其场景、地区和协议相符的权利。

## 维护与验证

更新来源时必须先审计目标提交，再同时修改 gitlink、`officialSources` 锁和目录：

```bash
python scripts/build_official_catalog.py
python scripts/build_catalog.py
python scripts/validate_repository.py
```

目录构建器从固定 Git 树读取全部 `SKILL.md`，记录 Git blob ID，并为缺少可移植 frontmatter 的旧入口使用父目录名作为回退。验证器检查来源数量、gitlink 提交、稳定身份、路径覆盖和 blob 一致性；未初始化官方子模块时会给出警告，并继续执行锁与目录结构检查。
