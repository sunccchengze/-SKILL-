# 平台兼容性

本礼包以普通目录、Markdown、JSON、CSV、Python 标准库和 tar.gz 为可移植基础。**工作流可移植不等于所有上游命令可移植。**

| 能力 | Arena Agent Mode | Codex/插件环境 | OpenCode/其他 Agent | 处理方式 |
|---|---|---|---|---|
| 阅读 Skill/文件、运行本地脚本 | 通常可用 | 通常可用 | 依产品而定 | 先检查工具和工作区 |
| `/research`、`/ars-*` | 非通用 | 仅安装对应命令时 | 非通用 | 不存在则按 SKILL 步骤手动执行 |
| `$academic-research-suite` | 非通用 | 可能是 Codex 适配语法 | 非通用 | 以实际安装和文档为准 |
| `OPENCODE_ENABLE_EXA=1` | 不适用 | 不应假定 | 特定 OpenCode 配置 | 仅在对应产品官方文档确认后使用 |
| Web/学术 API | 取决于会话工具和网络 | 取决于插件/API | 取决于配置 | 记录真实数据库、查询和日期 |
| MCP | 仅已连接服务 | 仅已安装插件/MCP | 依实现 | 先核验服务、权限、数据政策和费用 |
| Notion | 可通过可用工具/导出 | 官方插件可能可用 | 依连接器 | 始终保留本地规范副本 |
| Zotero | 可用本地/API 工具时 | 插件或本地 API | 依连接器 | 使用 BibTeX/RIS 作为交换层 |
| Jupyter | 可创建/运行文件时 | 官方 Skill 提供流程 | 依本地运行时 | 交付前从头运行并保存环境 |
| SPSS/EndNote/Word | 非内置保证 | 依本地软件/插件 | 依平台 | 作为可选导入导出目标 |

## 兼容性标签

`MANIFEST.json` 的 `compatibility` 只表达上游原生环境或指导可移植程度：

- `cross-platform-guidance`：流程和制品可在多数 Agent 中应用；
- `codex-native-guidance-portable`：原生为 Codex，其他平台只能迁移方法；
- `source-specific-runtime`：依赖上游 Agent、CLI、API 或执行框架；
- `domain-library-guidance`：需要对应 Python/R/科学软件和数据；
- `metadata-only`：因再分发许可不明确，仅提供来源索引。

每次调用前检查 `SKILL.md` 的真实依赖。Manifest 的 `dependencies.declarationFiles` 和 `platformRequirements.declarationFiles` 列出包内识别到的 `requirements*.txt`、`pyproject.toml`、`package.json`、环境/容器/运行时声明与平台清单的**精确相对路径**；空列表只表示未发现这些机器可读文件，不表示“无依赖”。压缩包不会自动安装软件、API、模型、MCP 或凭证。
