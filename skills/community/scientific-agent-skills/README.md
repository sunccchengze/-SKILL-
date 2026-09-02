# scientific-agent-skills（科学计算技能库）

> 来源：[K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) @ `1dd0fccf`（main，2026-09-02 装载，对应 v2.65.0）
> 协议：MIT（见 `LICENSE.md`，可自由使用/分发/修改）

K-Dense 出品的 **163 个现成科学/研究 Agent 技能**，覆盖生物、化学、医学及相邻工作流。

## 内容

- 每个技能一个目录，**完全自包含**（`SKILL.md` + `references/`，部分含 `scripts/`），可单独取走、互不依赖
- `plugin.json` — 上游插件清单（参考用）
- `README.upstream.md` — 上游原始 README（全部 163 个技能的目录索引）
- 未搬入：上游 `docs/`（约 240MB 演示媒体）、`tests/`（CI 测试），与技能运行无关

## 覆盖领域（节选）

- **生物信息学**：`anndata`、`biopython`、`bulk-rnaseq`、`bids`、`bioservices`、`cellxgene-census`、`deeptools`、`depmap`、`scanpy` 等
- **化学/计算化学**：`datamol`、`deepchem`、`diffdock`、`rdkit`、`cobrapy` 等
- **医学/临床**：`clinical-decision-support`、`clinical-reports`、`clinical-trial-protocol` 等
- **AI/科学计算**：`dask`、`astropy`、`cirq`、`pytorch-lightning` 等
- **通用研究**：`citation-management`、`database-lookup`、`latex-posters`、`markdown-mermaid-writing`、`autoskill`（元技能：自动生成新技能）等

完整清单见 `README.upstream.md`。

## 使用方法

- 触发：自然语言关键词即可（每个技能的 `SKILL.md` frontmatter 里有触发词描述），例如「用 RDKit 算一下这个分子的理化性质」。
- 某个技能需要额外 Python 包时，其 `SKILL.md` 会写明安装方式（如 `pip install rdkit`）。
- 想用其中某一个：直接拿走该目录即可，无需其他文件。

## 卸载

整个目录即全部足迹：`rm -rf skills/community/scientific-agent-skills`。
