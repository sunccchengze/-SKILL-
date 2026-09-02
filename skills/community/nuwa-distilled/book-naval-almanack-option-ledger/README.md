# 《纳瓦尔宝典》归因式选择权账本

这是 Eric Jorgenson 编纂的 *The Almanack of Naval Ravikant / 纳瓦尔宝典* 的 **Nuwa deep-tier** 蒸馏。它不是“致富语录生成器”，也不把编辑后的书写成 Naval 亲笔、把少数赢家经验写成普遍公式。

本包把 specific knowledge、accountability、leverage、ownership、judgment、compounding、happiness 与 mindfulness 转换为 **NAVAL-OPTION**：逐条归因，加入基率、准入约束、结构性反证和 ruin 边界，再做小额、可逆、可停止的选择权实验。

## 核心来源纪律

- 书由 Eric Jorgenson 编纂，材料来自 Naval 的推文、访谈、播客等；不是 Naval 连续写成的手稿。
- 若标“Naval 原话”，必须回到官方 sources 指向的原始推文/音频/文本；书中编辑措辞不能自动当逐字引文。
- 书中引用他人的话，不能重新归给 Naval。
- Skill 的实验、风险门与组合建议一律标 D 层。

## 快速使用

```bash
python3 scripts/build_option_experiment.py \
  --proposition "publish one reusable technical explainer" \
  --attribution naval-primary --primary-text-checked \
  --source "https://nav.al/productize-yourself" \
  --domain leverage --base-rate "audience growth is highly skewed" \
  --access-constraint "two hours weekly and an existing research note" \
  --downside-cap "one draft; no paid promotion" \
  --reversible-test "publish one article under my own name" \
  --success-metric "three qualified replies in 30 days" \
  --harm-metric "no confidential or employer-owned material" \
  --stop-condition "stop if review conflicts with employment policy" \
  --review-days 30 --stake low --owner "experimenter"
```

脚本不计算财富概率，也不提供个性化投资、税务、法律或医疗建议。

## 内容地图

- `SKILL.md`：NAVAL-OPTION、归因协议、选择权组合与安全门；
- `references/claim-layer-map.md`：恰好 18 条 A/B/C/D 主张；
- `references/source-notes.md`：官方编纂说明、Naval 原始来源和独立反证；
- `references/templates.md`：归因卡、基率/约束卡、可逆试验和组合评审；
- `references/research/`：六轮研究；
- `scripts/build_option_experiment.py`：确定性标准库 CLI；
- `tests/test_adversarial.py`：包专属对抗测试。

## 硬边界

- 不承诺致富、创业成功、被动收入或幸福；
- 不将辞职、负债、集中下注或无保险风险包装成“承担责任”；
- 不把 permissionless leverage 的可访问性夸成机会平等；
- 不把冥想替代诊疗，不处理危机；
- 不为剥削、违法、操纵或未授权使用他人作品提供方案。
