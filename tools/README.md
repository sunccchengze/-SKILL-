# 工具 (Tools)

本目录包含仓库内置工具的运行时镜像与技能入口。

| 工具 | 入口 | 说明 |
|---|---|---|
| [OpenCut](opencut/SKILL.md) | `tools/opencut/` | 本地浏览器视频编辑器（源码在 `full-sources/tools/opencut`） |
| [OpenWiki](openwiki/SKILL.md) | `tools/openwiki/` | LangChain OpenWiki CLI，生成面向 Agent 的 Markdown Wiki |
| [RustDesk](rustdesk/SKILL.md) | `tools/rustdesk/` | 原生远程桌面客户端（源码在 `full-sources/tools/rustdesk`） |
| [ScreenCoder](screencoder/SKILL.md) | `tools/screencoder/` | 截图转可编辑 HTML/CSS |
| [Spec Kit](spec-kit/SKILL.md) | `tools/spec-kit/` | GitHub Spec Kit 规范驱动开发 |

## 使用方式

```bash
# 安装所有工具源码（Git 子模块）
bash scripts/setup_tools.sh all

# 运行 OpenCut
HOST=0.0.0.0 PORT=5173 bash scripts/run_opencut.sh

# 核验工具安装
bash scripts/verify_tools.sh
```

完整工具指南见 [`guides/TOOLS.md`](../guides/TOOLS.md)。
