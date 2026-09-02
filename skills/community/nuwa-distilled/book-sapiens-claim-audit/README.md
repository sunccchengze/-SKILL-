# 《人类简史》历史主张审计器

这是对 Yuval Noah Harari《Sapiens: A Brief History of Humankind / 人类简史》的 **Nuwa deep-tier** 蒸馏，不是章节缩写、历史百科或“替作者背书”。

它把书中宏大叙事转换为可核查的 **SCALE-AUDIT**：先固定主张的尺度、年代与地域，再区分直接证据、代理指标、模型与修辞，主动寻找替代解释和反证，最后决定“保留、降格、拆分或停止使用”。

## 适合

- 审查“认知革命”“农业是骗局”“共同想象带来合作”等宏观历史命题；
- 为文章、课程、展览或研究计划制作证据账本；
- 检查从史前证据跳到现代政策、身份或道德结论的越界推理；
- 比较 Harari 的综合叙事与考古学、古基因组学、历史学和合作研究。

## 不适合

- 代替专业史学、考古学或古基因组系统综述；
- 给出祖源、族群优劣、领土权利或现代政治的确定性裁决；
- 把“共同想象”解释成“权利不真实”或“制度可以随意废除”；
- 预测不可证伪的文明必然方向。

## 快速使用

1. 阅读 [SKILL.md](SKILL.md)。
2. 从 [references/templates.md](references/templates.md) 复制主张卡和 SCALE-AUDIT 工作表。
3. 用 [references/source-notes.md](references/source-notes.md) 与 [references/claim-layer-map.md](references/claim-layer-map.md) 回溯证据。
4. 运行：

```bash
python3 scripts/audit_historical_claim.py \
  --claim "七万年前出现一次离散的认知革命" \
  --scale global --period "100000-30000 BP" --region "Africa and Eurasia" \
  --evidence "engraved ochre: proxy for symbolic practice" \
  --evidence "ornaments: uneven regional chronology" \
  --alternative "mosaic accumulation rather than one threshold" \
  --uncertainty "cognition is not directly fossilized" \
  --audience "undergraduate seminar" --use-context education
```

脚本只输出审计计划，不判断历史真伪。

## 内容地图

- `SKILL.md`：触发边界、SCALE-AUDIT、模型、停止规则；
- `references/source-notes.md`：书本、学科证据与反证；
- `references/claim-layer-map.md`：恰好 18 条 A/B/C/D 分层主张；
- `references/templates.md`：可执行模板；
- `references/research/`：六轮研究日志；
- `scripts/audit_historical_claim.py`：确定性标准库 CLI；
- `tests/test_adversarial.py`：包专属对抗测试；
- `VALIDATION.md`：复现命令、通过标准和限制。

## 核心承诺

- 叙事吸引力不等于证据强度；
- 同一词下不混合地点、年代和证据类型；
- “没有直接证据”不等于“相反命题已证实”；
- 历史解释不自动推出当代权利或政策；
- 涉及在世社群、祖源、暴力、殖民和身份时，必须给出异议、咨询、撤回和停止路径。
