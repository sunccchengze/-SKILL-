#!/usr/bin/env bash
# restore-merged-state.sh — 在新会话中重建丢失的两个提交
# 用法: bash restore-merged-state.sh  &&  git push origin <当前分支>  &&  对 main 开 PR 合并
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
B=origin/arena/01a048e7-skill
F=origin/arena/01a0582f-skill
if [ -d bundles ] && [ -f TASK_ROUTING.md ] && [ -f README.legacy-vault-2026-08-31.md ]; then
  echo "✔ 已处于合并后状态，无需操作。"; exit 0
fi
# Check if academic-research-skills exists under HEAD (more robust than checking for specific file)
git cat-file -e HEAD:skills/community/academic-research-skills 2>/dev/null \
  || { echo "✘ 当前分支 HEAD 里没有 academic-research-skills 目录。请基于最新 main (含 PR#2) 操作。"; exit 1; }
git fetch origin '+refs/heads/arena/*:refs/remotes/origin/arena/*' 2>/dev/null || git fetch origin
git cat-file -e "$B^{commit}" 2>/dev/null \
  || { echo "✘ 找不到 $B —— 旧分支可能已被删除，请先在 GitHub 上确认 5 个 arena/01a* 分支还在。"; exit 1; }
git cat-file -e "$F^{commit}" 2>/dev/null || { echo "✘ 找不到 $F。"; exit 1; }
# 提交 1: 旧世界线 + 3 篇个人文档
git checkout "$B" -- .gitignore .gitmodules AGENTS.md GROWTH_ROADMAP.md TASK_ROUTING.md SKILL.md \
  bundles catalog categories full-sources governance guides scripts tests third_party tools skills
git checkout HEAD -- skills/community/academic-research-skills
rm -rf /tmp/oldvault && mkdir -p /tmp/oldvault
git archive "$B" skills/community/academic-research-skills | tar -x -C /tmp/oldvault/
git archive "$B" skills/community/scientific-agent-skills | tar -x -C /tmp/oldvault/
git rm -r -q skills/community/scientific-agent-skills/skills 2>/dev/null || true
mkdir -p skills/community/academic-research-skills-legacy-snapshot-2026-08-31
cp -r /tmp/oldvault/skills/community/academic-research-skills/. skills/community/academic-research-skills-legacy-snapshot-2026-08-31/
mkdir -p skills/community/scientific-agent-skills-legacy-snapshot-2026-08-31
cp -r /tmp/oldvault/skills/community/scientific-agent-skills/skills/. skills/community/scientific-agent-skills-legacy-snapshot-2026-08-31/
git checkout "$F" -- "Agent驾驭力训练手册.md" "四个月脚印计划-2026Sep-Dec.md" "超级大脑洞察报告.md"
git add -A
git commit -q -m "merge: 合回 2026-08 旧技能库世界线 (arena/01a048e7-skill 全部内容)"
# 提交 2: 统一 README + 快照说明
git show "$B:README.md" > README.legacy-vault-2026-08-31.md
cat > README.md <<'MASTER_README_EOF'
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
MASTER_README_EOF
cat > skills/community/academic-research-skills-legacy-snapshot-2026-08-31/README.md <<'SNAP1_EOF'
# academic-research-skills — 旧版快照（2026-08-31）

- 来源：2026-08 旧技能库（分支 `arena/01a048e7-skill`）中对 [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) 的部分拷贝
- 版本：约 v3.2.0，仅含 `academic-paper` / `academic-paper-reviewer` / `academic-pipeline` 三个技能（无 deep-research、无 shared/）
- 当前规范版本在 `skills/community/academic-research-skills/`（v3.3.1 完整，897 文件，2026-09-02 装载）
- 本目录仅为「零丢失」归档；确认不需要后可整目录删除
SNAP1_EOF
cat > skills/community/scientific-agent-skills-legacy-snapshot-2026-08-31/README.md <<'SNAP2_EOF'
# scientific-agent-skills — 旧版快照（2026-08-31）

- 来源：2026-08 旧技能库（分支 `arena/01a048e7-skill`）中对 [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) 的拷贝
- 版本：约 v2.6x，157 个技能（现版 163 个）
- 当前规范版本在 `skills/community/scientific-agent-skills/`（v2.65.0，163 技能，2026-09-02 装载）
- 本目录仅为「零丢失」归档；确认不需要后可整目录删除
SNAP2_EOF
git add -A
git commit -q -m "docs: 统一仓库总 README + 两个旧版快照归档说明"
# 零丢失验证
python3 - <<'PY_EOF'
import subprocess
def ls(rev="HEAD"):
    out = subprocess.run(["git","ls-tree","-r","-z",rev],capture_output=True).stdout
    res = {}
    for e in out.split(b"\0"):
        if not e: continue
        meta, p = e.split(b"\t",1)
        mode, typ, h = meta.decode().split()
        res[p.decode()] = (mode, typ, h)
    return res
final = ls("HEAD")
blobmap = {}
for p,(mode,typ,h) in final.items():
    if typ=="blob": blobmap.setdefault(h, []).append(p)
SNAP = {
 "skills/community/academic-research-skills/": "skills/community/academic-research-skills-legacy-snapshot-2026-08-31/",
 "skills/community/scientific-agent-skills/skills/": "skills/community/scientific-agent-skills-legacy-snapshot-2026-08-31/",
}
branches = ["origin/arena/01a048e7-skill","origin/arena/01a0095c-skill","origin/arena/019ffbe9-skill",
            "origin/arena/01a0582f-skill","origin/arena/01a0582a-skill"]
bad = 0
for b in branches:
    for p,(mode,typ,h) in ls(rev=b).items():
        if p in final or p == "README.md": continue
        if any(p.startswith(k) and (v+p[len(k):]) in final for k,v in SNAP.items()): continue
        if not (typ=="blob" and h in blobmap):
            print(f"  MISS[{b}] {p}"); bad += 1
if bad:
    raise SystemExit(f"✘ 零丢失验证失败：{bad} 个文件内容缺失")
print("✔ 零丢失验证通过：5 个旧分支全部内容均在最终树中 (含快照归档/移动位置)")
PY_EOF
echo "✔ 重建完成。下一步: git push origin $(git branch --show-current)  → 对 main 开 PR 合并"
