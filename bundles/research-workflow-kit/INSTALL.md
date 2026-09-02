# 安装与更新

## 方式 A：直接校验并解压（推荐）

`SHA256SUMS` 是压缩包的外部校验值，必须在解压前、两者位于同一目录时检查。不要用 `|| true` 吞掉失败：

```bash
sha256sum -c SHA256SUMS
tar -xzf research-workflow-kit.tar.gz
cd research-workflow-kit
python3 tools/research_kit.py doctor
python3 tools/research_kit.py verify
```

外部 checksum 验证传输后的压缩包；解压后的 `verify` 再验证 Manifest、Profile 引用、全部 payload 树哈希、路径与项目模板。macOS 可用 `shasum -a 256 research-workflow-kit.tar.gz`，并与 `SHA256SUMS` 中的值逐字比较。

## 方式 B：只安装 Core

先 dry-run：

```bash
python3 tools/research_kit.py install \
  --profile core \
  --target "$HOME/.agents/skills" \
  --dry-run
```

确认目标目录符合当前 Agent 平台后再去掉 `--dry-run`。重复安装不会静默覆盖；确需更新时显式加 `--force`。

## 方式 C：只装指定 Skill

```bash
python3 tools/research_kit.py search "citation verification"
python3 tools/research_kit.py install \
  --id 'scientific-agent-skills::skills/citation-management' \
  --target "$HOME/.agents/skills" \
  --dry-run
```

ID 以实际 `MANIFEST.json` 为准。

## 建立研究项目

```bash
python3 tools/research_kit.py init-project ./my-project
```

目标非空时默认停止；`--force` 只应用于你已审查过的模板合并场景。

## 安全说明

- 安装器只复制本地文件，不联网、不执行第三方安装脚本、不读取凭证；
- Skill payload 不等于依赖已经安装。读取 `SKILL.md` 后再安装必要软件，并固定版本；
- `metadata-only` 条目因缺乏明确再分发许可未装入 payload；工具默认拒绝安装它们；
- 某些上游 Skill 依赖特定 Codex、Claude、Hermes、MCP、API 或 GPU。兼容性字段是路由提示，不是运行保证；
- 不运行未经核验的 `curl | sh`，不把 API key 写入仓库、Notebook 或聊天。

## 从 Skill 仓库领取

新 Arena Session Agent 可在任意工作目录逐字执行；这不会切换它自己的固定分支：

```bash
git fetch origin arena/019ffbe9-skill
mkdir -p /tmp/research-workflow-kit-download

git show origin/arena/019ffbe9-skill:bundles/research-workflow-kit/research-workflow-kit.tar.gz \
  > /tmp/research-workflow-kit-download/research-workflow-kit.tar.gz
git show origin/arena/019ffbe9-skill:bundles/research-workflow-kit/SHA256SUMS \
  > /tmp/research-workflow-kit-download/SHA256SUMS

cd /tmp/research-workflow-kit-download
sha256sum -c SHA256SUMS
tar -xzf research-workflow-kit.tar.gz
cd research-workflow-kit
python3 tools/research_kit.py doctor
python3 tools/research_kit.py verify
less START_HERE.md
```

随后用 `install --profile core --target <该平台真实 Skill 目录> --dry-run` 预览；确认后再安装并执行 `init-project`。新 Arena Session 有自己的固定分支时，**不要切换到本 Session 的分支**；上面的 `git show` 只读取远端对象。若分支尚未推送或 GitHub 连接失败，应先报告，不能用来源不明的镜像替代。
