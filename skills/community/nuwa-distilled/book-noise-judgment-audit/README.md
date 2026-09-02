# 《噪音》判断系统审计器

这是 Daniel Kahneman、Olivier Sibony、Cass R. Sunstein《Noise: A Flaw in Human Judgment / 噪音》的 **Nuwa deep-tier** 蒸馏。它不教用户用“意见不一致”证明谁更准确，而是把书中的系统噪音、噪音审计和决策卫生转换为可执行的 **NOISE-AUDIT**。

## 它解决什么

- 同类案件由不同人判断为何差异巨大；
- 如何区分偏差、水平噪音、模式噪音与场合噪音；
- 没有可信真值时能测量什么、不能声称什么；
- 如何在独立判断、结构化信息、机械汇总、规则与专业裁量之间做组合；
- 如何防止“一致性”固化结构性偏差、剥夺申诉或把人变成分数。

## 快速使用

```bash
python3 scripts/audit_judgment_system.py \
  --system "grant triage" --case-spec "same dossier and rubric" \
  --equivalence-rule "cases in one funding track at the same stage" \
  --judge-count 4 --repeat-rounds 1 --target-type policy-rule \
  --outcome "fund / revise / decline" \
  --intervention "independent criterion ratings before discussion" \
  --cost-risk "false declines can suppress unconventional work" \
  --owner "program director" --use-context management
```

脚本只生成测量与治理计划，不产生个案判决。

## 内容

- `SKILL.md`：NOISE-AUDIT、模型、权利门和停止规则；
- `references/claim-layer-map.md`：18 条 A/B/C/D 分层主张；
- `references/source-notes.md`：原书/作者语境、统计证据与公平性反证；
- `references/templates.md`：审计设计、判断协议、干预试验和申诉模板；
- `references/research/`：六轮研究；
- `scripts/audit_judgment_system.py`：确定性标准库 CLI；
- `tests/test_adversarial.py`：系统噪音专属红队测试。

## 硬边界

- 没有“应相同判断”的规范理由，就不能把差异叫作系统噪音；
- 没有可信目标，就只能讨论一致性/可靠性，不能声称准确性提高；
- 降噪不自动降偏差，也不自动改善程序正义；
- 医疗、法律、福利、招聘等高影响场景必须有合格审阅、群体影响审计、解释/申诉与停止条件；
- 本包不替专业诊疗、法律裁判、资格裁决或紧急处置。
