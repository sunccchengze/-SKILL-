# 《原则》跨分支集成审计

> **历史记录，非当前验收标准。** 本文件随 `arena/019ffbe9-skill` 合并，用来保留该分支当时的导入判断；其中 `skills/community/nuwa-skill` / `huashu-nuwa` 自动检查属于旧分支的非 canonical 启发式，不作为本分支的 governing standard。当前 canonical 方法依据是外部 `xmg2024/nvwa-skill` 冻结快照 `fdb181f0e057e837e15942707b1ea35845850979`，最终验收以来源解析、行为测试、安全门和仓库验证为准。

审计日期：2026-08-16。以下远端头、文件数和测试数均是当时快照事实，不自动更新为合并后的现状。

## 结论

对 `origin/arena/01a0095c-skill` 做精确远端刷新后，远端头为
`6391e8892dca507c553b365f97e5b95f7a942187`。该快照相对本分支确有且只有一个新的书籍包：

- `book-principles-decision-system` — Ray Dalio 2017 年 *Principles: Life and Work* 的可演化决策系统。

源包 tree OID 为 `957200e601a965b2788a5f795ccd4c4b48c973a9`，源 `SKILL.md` blob OID 为
`385e6b94fe5a492b0f4026e36edda8d0ea90c57a`。本分支选择性导入该包，不合并源分支生成目录。

## 完整性检查，而非只看目录名

审计枚举了源分支 `skills/community/nuwa-distilled` 下全部 `book-*/SKILL.md`，也检查了独立的
`book-*.md` 文件。源快照共有 18 个书籍包和 1 个独立桥接文档：

- 《易经》与《原子习惯》均已存在；
- 《第五项修炼》《人有人的用处》《理解媒介》均已存在，且源分支最新加固内容与本分支逐文件一致；
- `book-change-habit-bridge.md` 已存在且 blob 内容一致，它是跨书行为改变桥接文档，不是遗漏的新书包；
- 其余源包要么一致，要么已经在本分支完成更深的七书升级；不以源版本覆盖本地深层版本；
- 唯一缺失身份是 `book-principles-decision-system`，未发现别名包或第二本新书。

## 导入前质量审计

源包不是摘要壳：

- 15 个文件，包含 `SKILL.md`、README、VALIDATION、6 轮研究、36 条 A/B/C/D 声明、23 条来源记录、模板、CLI 与测试；
- 认识论边界明确区分 2017 原书、其他版本/后续机构材料、独立研究/争议和本 Skill 综合；
- 对 radical transparency、believability weighting、人员测评和组织成功的因果外推设置了反证与权利边界；
- CLI 输出确定性 JSON/Markdown；人员等敏感域不能被用户声明为低风险来绕过治理门；
- 导入前包级行为测试 **14/14** 通过，Python 编译通过；
- 导入前 Nuwa 自动质量门为 **5/6**：正文实际列出十组不同的内在张力，但自动检查器只识别到标题中的一次“张力”标记。

因此源包质量足以作为深层基线，但不能原样宣布全部通过。

## 本地加固与分池

本分支做了三项有意适配：

1. 将十组张力逐项标记为“张力 1”至“张力 10”，让语义结构和自动质量门一致；
2. 在 README/VALIDATION 中记录跨分支谱系、质量门和复验命令；
3. 在 `scripts/build_catalog.py` 的人工语义覆盖中将其路由到 `business-strategy`，再由本分支生成器重建 catalog/category 文件。

评审理由：该包的主输出是决策界定、原则编译、异议设计、责任治理和结果更新，核心用途是组织与业务决策；
虽然包含合规失败门，但不应仅因安全词频被误分到 `security-compliance`。

## 集成后复验

- 包级行为测试：14/14；
- 仓库级《原则》聚焦测试：13/13；
- 根测试发现：73/73；
- Nuwa 自动质量门：6/6；
- catalog/category 连续重建哈希一致，得到 2216 个紧凑技能入口和 3119 个默认可见入口；
- 仓库验证通过：10180 个实测文件，低于 10200 上限；
- `git diff --check` 通过。

这些结果证明结构、追踪、确定性行为和失败门满足仓库合同；不证明现实效果。

## 明确未做

- 未 cherry-pick 源提交；
- 未导入或手工拼接源分支的 `catalog/*`、`categories/*` 生成结果；
- 未覆盖本分支已有、更深或相同的书籍包；
- 未把 BRIDGE 误归因为 Dalio 原方法；
- 未把包级测试通过解释成书中主张、Bridgewater 文化或现实决策效果已获验证。
