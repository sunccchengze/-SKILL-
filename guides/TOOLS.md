# OpenCut、RustDesk 与 GitHub Spec Kit 本地工具

本页把“固定源码”“安装依赖”“可执行程序”“实际运行验证”分开记录，避免把一个 Git 子模块误报成已经可用的应用。三个上游都以 Git 子模块锁定在 `full-sources/tools/`，版本身份见 `catalog/sources.lock.json`。

## 当前固定版本与本次环境状态

| 工具 | 固定源码 | 本地安装/运行状态 | 入口 |
|---|---|---|---|
| OpenCut | `400f097becba5db0fbc305d5a65348cb81c20356` (`main`, 2026-08-01) | Bun `1.3.11` 和 665 个 web 依赖已安装；开发服务器已在 `0.0.0.0:5173` 启动并取得 HTTP 200 | `tools/opencut/` |
| RustDesk | `6c578292e8ebbbec708b76986ba8c4bc7c509747` (`1.4.9`) | 稳定源码已安装并核验；本次沙箱到 GitHub release-assets 的 TLS 连接持续中断，因此原生 Debian 包**未完成安装，也未宣称 GUI 可运行** | `tools/rustdesk/` |
| GitHub Spec Kit | `d1f50fcbe684a4222059c4ba7f2d7eabcca87402` (`v0.16.4`) | `specify-cli 0.16.4` 已装在 `~/.local/share/specify-cli/venv`，`~/.local/bin/specify` 可用 | `tools/spec-kit/` |

这里的本地依赖、虚拟环境、下载包、`node_modules` 和生成文件都不提交；仓库只提交可复现脚本、技能入口、文档和精确 gitlink。

## 一键准备

```bash
# OpenCut + Spec Kit + RustDesk 固定源码（不自动强装原生 GUI 包）
bash scripts/setup_tools.sh all

# 查看精确子命令
bash scripts/setup_tools.sh --help

# 核验三个源码 pin、Bun 与 Specify CLI
bash scripts/verify_tools.sh
```

`all` 故意只初始化 RustDesk 源码：原生包与操作系统、架构、桌面会话、安全策略有关，不应在无确认时静默安装或启动远控。

## OpenCut：安装并运行

```bash
bash scripts/setup_tools.sh opencut
HOST=0.0.0.0 PORT=5173 bash scripts/run_opencut.sh
```

另一个终端检查：

```bash
curl --fail --show-error http://127.0.0.1:5173/
```

固定提交当前没有 Bun lockfile，所以安装器使用上游 `package.json` 并加 `--no-save`，不会生成待提交锁文件。它是开发运行，不是生产部署。启动时 Cloudflare Vite 插件可能因外网不可达而提示无法取得 `Request.cf`，随后采用本地占位值；应以 HTTP 页面和实际编辑操作判断是否可用，而不是只看这条非致命提示。

本次 `bun run build` 已通过，`/` 与 `/editor` 均返回 HTTP 200。`bun run test` 则在收集测试前因当前 Vite/Cloudflare worker 组合报 `depsOptimizer is required in dev mode`；因此不能把单元测试标为通过。这是上游无锁、含 `latest` 依赖的当前安装状态，修复前应以“构建和页面验证通过、测试启动受阻”准确报告，不要静默忽略。

若开发服务器重排 `apps/web/src/routeTree.gen.ts`，那是上游路由生成器的本地副作用；除非确实修改了路由，否则不要把它作为本仓库改动提交。

## Spec Kit：安装并用于项目

```bash
bash scripts/setup_tools.sh spec-kit
specify --version
specify check
```

在目标项目中，先阅读已有 `AGENTS.md`、需求和约束，再选择集成并初始化。不要无审查覆盖已有规则：

```bash
cd /path/to/project
specify init --here --integration <integration>
```

随后按 constitution → specify/clarify → plan → tasks → implement → converge/verify 推进。具体 Agent 的命令可能是 `/speckit.*` 或 `$speckit-*`，以初始化结果为准。

## RustDesk：源码、包与 GUI 分级验证

### 1. 固定源码

```bash
bash scripts/setup_tools.sh rustdesk-source
```

这一步可用于审计或后续平台构建，但不等于有原生可执行文件。

### 2. Debian x86_64 用户级包

安装器只接受从官方发布页取得的 `1.4.9` x86_64 Debian 包，并核验固定发布文件大小、包名、版本和架构，然后解压到 `~/.local/share/rustdesk/root`；不调用 `sudo` 或修改系统 dpkg 数据库。该发布没有上游 checksum 清单，所以这些元数据检查**不是密码学来源证明**；离线传入的文件仍必须经可信渠道从官方页面取得，不能用同尺寸或同元数据替代真实性。

```bash
# 网络可直接访问官方 GitHub release asset 时
bash scripts/setup_tools.sh rustdesk-package

# 或先从官方发布页下载，再明确传入文件
RUSTDESK_PACKAGE=/absolute/path/rustdesk-1.4.9-x86_64.deb \
  bash scripts/setup_tools.sh rustdesk-package
```

脚本不会自动改用第三方镜像。官方资产无法到达时，必须报告“源码已固定、二进制安装受阻”，不能把零字节/半截下载当成包，也不能把未经验证的镜像文件当成官方制品。

### 3. 原生桌面运行

```bash
bash scripts/run_rustdesk.sh
```

必须有 X11 或 Wayland 会话、兼容动态库，并获得远端与本端所有者的明确授权。原生 GUI 不能在浏览器 Live Preview 中等价验证。分别报告：源码 pin、包元数据、依赖检查、GUI 启动、授权连接测试；没有做过的层级必须明确标为未验证。

## 安全与许可

- OpenCut 和 Spec Kit 固定提交采用 MIT；RustDesk 固定提交采用 AGPL-3.0。原始许可证保留在各子模块中。
- OpenCut 素材可能包含个人、商业或版权敏感内容，不得擅自上传。
- RustDesk 可暴露屏幕、输入、剪贴板、音频、文件和隧道，只能用于知情、授权的远程支持；禁止隐蔽控制、绕过同意、凭据窃取或持久化。
- Spec Kit 会向目标项目写入模板和 Agent 配置；初始化前先审查目标路径与已有文件。
- 依赖安装与外网下载属于有副作用操作；自动化前应明确网络、凭据、文件写入和许可证边界。
