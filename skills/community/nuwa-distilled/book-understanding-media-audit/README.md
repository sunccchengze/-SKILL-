# 《理解媒介》媒介效应审计 Skill

Nuwa deep-tier 的中性书籍蒸馏包。它把 Marshall McLuhan 的“媒介即讯息”、延伸/截除、尺度—速度—模式、内容嵌套与 figure/ground 转为 MEDIUM 配置审计，同时防止“内容不重要”、hot/cool 永久标签、技术决定论和“McLuhan 预言了某产品”等误用。

## 适用与路由

适合：AI 搜索/摘要/聊天/推荐、界面默认、排序、通知与协作工具如何改变节奏、可见性、参与、劳动和规则权；同一内容跨媒介比较；上线前提出可反驳的配置效应假设。

不要单独使用：内容准确性/伤害审核（须并行）、具体长期注意/健康/儿童发展/政治因果、真实上线许可、没有版本化配置或比较条件的产品结论。

## 认识论合同

| 层 | 是什么 | 不能说成什么 |
|---|---|---|
| A | 1964 *Understanding Media* 的可定位概念 | 现代平台实证结论 |
| B | 后期 McLuhan / *Laws of Media* 的 tetrad | 1964 原书章节或日期预测 |
| C | 媒体研究、政治经济批评、affordance 与当代审计研究 | 原作者主张或普适效应 |
| D | 本 Skill 创建的 MEDIUM、模板、门禁和 CLI | 原作者方法或已验证量表 |

24 条声明见 [`references/claim-layer-map.md`](references/claim-layer-map.md)，来源的支持/不支持边界见 [`references/source-notes.md`](references/source-notes.md)。

## 快速调用

```text
请显式使用 book-understanding-media-audit 审计“AI 自动摘要成为会议记录默认入口”。
固定配置、版本、场景与观察窗口；内容层和媒介层并行；
比较 before/after 的尺度、速度、模式、可见性与补全劳动，
检查 feature→affordance→outcome、figure/ground、权力和差异影响，给替代解释与推翻观察。
```

## CLI

从本包根目录运行：

```bash
python3 scripts/audit_medium.py \
  --medium "AI 会议摘要 v2，默认自动发送" \
  --use "跨团队决策会的默认记录" \
  --content "讨论、异议与行动项" \
  --actor "主持人" --actor "异议参与者" \
  --affordance "即时压缩" --affordance "自动分发" \
  --constraint "语气和少数意见可能被压平" \
  --harm "高影响行动项被错误归属" \
  --stakes high --owner "协作产品负责人" \
  --stop-condition "高影响误配越过事前阈值" \
  --source-layer D --format json --output /tmp/medium.json
```

最低要求：非空 medium/use/content，1–12 个唯一 actor、affordance、constraint。`--harm` 可重复；`--format` 为 `markdown|json`，`--output` 省略时输出 stdout。

高风险强制要求 owner、至少一项 harm 和 stop condition；成功也只返回 `analysis_and_probe_design_only`，不是 launch decision。输入仅作为数据，Markdown renderer 会转义用户文本。

## MEDIUM 产物

1. **Map configuration**：设备、接口、模型/检索、默认、同步性、版本、商业模式和用户/非用户；
2. **Examine**：内容准确/来源/遗漏与媒介尺度/速度/模式并行；
3. **Detect**：每个 affordance 的延伸、少用/外包、隐形劳动、失效后果与恢复；
4. **Inspect**：figure/ground、所有权、规则改变权、收益/负担和无障碍/非画像替代；
5. **Use tetrad**：明确 B 层，只提出有证据、反例和替代解释的四格假设；
6. **Make probes**：群体、窗口、比较配置、测量、替代解释、推翻与停止观察。

完整配置表单见 [`references/templates.md`](references/templates.md)；六轮研究见 [`references/research/`](references/research/)；复核命令见 [`VALIDATION.md`](VALIDATION.md)。

## 关键边界

- “媒介即讯息”要求补看配置效应，不表示内容无关；
- feature 不是 affordance，affordance 也不是已发生 outcome；
- hot/cool 只作绑定设备、配置、文化和任务的参与探针；
- 参与不等于 agency；须检查能否改规则、拒绝、申诉和使用替代；
- 技术不会脱离制度、所有权、商业模式、文化和用户行动独自产生结果；
- 配置漂移后旧判断失效，必须版本化并保留判断更新日志。

## 验证

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 ../../nuwa-skill/scripts/quality_check.py SKILL.md
```

从 [`SKILL.md`](SKILL.md) 开始完整执行，不要只套一句“媒介即讯息”。
