# 《原则》可演化决策系统

这是对 Ray Dalio 2017 年 *Principles: Life and Work* 的 Nuwa deep-tier 蒸馏：不是金句摘要，也不是 Bridgewater 文化复制包，而是一套有版本、反证、权利和来源边界的决策记录系统。

## 核心产物

- 6 个通过跨域复现、生成力、排他性检查的心智模型；
- 10 条可触发、有边界的决策启发式；
- **BRIDGE** 六步法：Bound / Record / Identify / Disagree / Govern / Evaluate；
- 36 条 A/B/C/D 声明与 23 条来源账本；
- 14 个可复制工作制品；
- 确定性 JSON/Markdown CLI；
- 14 个行为测试和仓库级证据/安全测试。

## 它能做什么

- 把复盘故事编译成带 trigger、prediction、exception、falsifier、version 的原则；
- 按目标→问题→诊断→设计→执行拆解混乱决策；
- 记录现实、解释、未知和来源质量；
- steelman 最强异议并寻找真正的反证；
- 只在可比任务上记录暂定可靠性，不给人总分；
- 选择 advice / consent / vote / owner / algorithm-assisted 决策模式；
- 为透明度设置目的、必要性、受众、隐私区、保留和删除边界；
- 用事前预测和版本日志更新原则，而不是结果出来后改写历史。

## 认识论合同

- **输入仅作为数据**：CLI 把用户陈述标为 `user_supplied_claims_not_independently_verified`。
- **作者主张不是外部验证**：2017 原书 A、其他版本/机构后续 B、研究/批评 C、本 Skill D 分开。
- **成功不是因果证据**：Bridgewater 成功不证明某一文化机制造成业绩。
- **任务可靠性不是人的价值**：禁止全局 believability、人格或价值评分。
- **透明不是监控许可**：优先公开决策逻辑，保护个人、举报、保障、特权和安全信息。
- **输出不是部署批准**：高风险状态始终为 `governance_review_required`。

## 快速调用

```text
请使用 book-principles-decision-system 分析“是否扩大产品试点”。
先写目标/现实/未知，再做两个竞争诊断；把候选原则编译成可推翻卡；
steelman 反方，说明决策模式、owner、隐私边界、rollback 和复盘版本。
所有关键声明标 A/B/C/D 与 P/PD ID。
```

## CLI：普通决策

从本包根目录：

```bash
python3 scripts/apply_principles.py \
  --decision "是否把新产品试点扩大到两个市场" \
  --goal "验证留存而不制造不可逆客户伤害" \
  --reality "四周试点有120名活跃用户" \
  --reality "退款率为基线的1.3倍" \
  --principle "只有留存改善且伤害不升高时才扩大" \
  --disagreement "销售团队认为四周样本太小但窗口会关闭" \
  --evidence "试点周报 v3" \
  --domain business-strategy --format markdown
```

## CLI：高风险人员场景

以下命令仍只生成治理审查材料，不批准晋升工具：

```bash
python3 scripts/apply_principles.py \
  --decision "是否用历史项目评分辅助晋升复核" \
  --goal "提高证据一致性且不制造差异伤害" \
  --reality "当前评分跨经理不可直接比较" \
  --reality "过去两轮申诉缺少独立复核" \
  --principle "未经岗位验证和分群影响审计的评分不得进入晋升" \
  --disagreement "业务方认为现有评分已足够" \
  --evidence "真实晋升流程分群验证报告 v1" \
  --domain personnel --risk-level high \
  --accountable-owner "人力与业务共同负责人" \
  --applicable-rule "适用劳动、反歧视、隐私和集体协商规则" \
  --affected-group "候选员工" \
  --impact-evidence "真实晋升流程分群验证报告 v1" \
  --appeal-path "非原决定人的人工复核" \
  --rollback-trigger "任一受保护群体选择率显著恶化" \
  --stop-condition "投诉或伤害指标超过基线" \
  --format json --output /tmp/principles-review.json
```

敏感领域不能用 `--risk-level low` 绕过；必须具备：

- `--accountable-owner`
- `--applicable-rule`
- `--affected-group`
- `--impact-evidence`
- `--appeal-path`
- `--rollback-trigger`
- `--stop-condition`

## 从哪里开始

1. [`SKILL.md`](SKILL.md)：完整模型、工作流、张力与失败模式；
2. [`references/claim-layer-map.md`](references/claim-layer-map.md)：36 条可追踪声明；
3. [`references/source-notes.md`](references/source-notes.md)：来源支持/不支持/版本/冲突；
4. [`references/templates.md`](references/templates.md)：可复制执行制品；
5. [`VALIDATION.md`](VALIDATION.md)：测试证据与不证明事项。

## 最重要的禁止项

- 不用 dots、MBTI 或人格标签决定人的机会；
- 不把公开羞辱包装成 radical truth；
- 不把录制一切包装成学习；
- 不把同一批高权重者的评分循环当客观性；
- 不把 2011、2017 和 2024 材料混为一版；
- 不把争议报道写成裁定，也不把机构否认写成反证完成。
