# 《人有人的用处》人本控制论 Skill

Nuwa deep-tier 的中性书籍蒸馏包。它把 Norbert Wiener 对反馈、通信、自动化与人的用途的讨论转为 HUMAN 治理审计，同时严格分开版本、其他 Wiener 著作、后续治理资料与本 Skill 的操作化；不扮演作者，也不把社会问题伪装成可直接计算的信息熵。

## 适用与路由

适合：AI/自动化目的审计、指标代理与反馈失真、人工复核/覆盖、申诉退出、算法管理、任务与技能迁移、收益和错误的分配。

不要单独使用：具体法域法律判断、临床/安全验证、伦理或合规认证、宏观就业预测、没有真实日志与受影响者证据的部署批准。高风险事项必须交给合格领域人员和适用治理程序。

## 认识论合同

| 层 | 是什么 | 不能说成什么 |
|---|---|---|
| A | *The Human Use of Human Beings* 的版本化主张 | 当代 AI 产品效果证明 |
| B | *Cybernetics*、论文与其他 Wiener 材料 | 《人有人的用处》的逐字内容 |
| C | 后续批评及 NIST、ILO、EDPS 等现代治理资料 | Wiener 已提出这些现代机制 |
| D | 本 Skill 创建的 HUMAN、模板、门禁和 CLI | 原作者方法或合规标准 |

功能类比不等于人机伦理同等；反馈存在不证明目的正当；human-in-the-loop 标签不证明有真实复核权。24 条声明见 [`references/claim-layer-map.md`](references/claim-layer-map.md)，证据边界见 [`references/source-notes.md`](references/source-notes.md)。

## 快速调用

```text
请显式使用 book-human-use-cybernetics 审计 AI 客服分流。
按 HUMAN 分开原书、Wiener 邻近材料、后续治理证据和 Skill 综合；
检查直接人的目的、代理指标、真实反馈、人工权限、申诉/回滚、劳动与分配，
并说明未知、适用规则、责任 owner 与非批准边界。
```

## CLI

从本包根目录运行：

```bash
python3 scripts/audit_automation.py \
  --system "AI 客服分流 v3" \
  --purpose "用户及时获得正确帮助" \
  --metric "平均处理时长" --metric "首次正确解决率" \
  --affected "紧急问题用户" --affected "一线客服" \
  --decision "是否转人工" --harm "错拒或延迟支持" \
  --risk-level high \
  --accountable-owner "客服运营负责人" \
  --applicable-rule "适用消费者保护、隐私和行业规则待法律复核" \
  --appeal-path "可追踪人工复核入口" \
  --rollback-trigger "紧急错拒越过事前阈值" \
  --source-layer D --format json --output /tmp/human.json
```

最低要求：非空 system/purpose，1–8 个唯一 metric、1–12 个唯一 affected、1–8 个唯一 decision、1–12 个唯一 harm。重复参数可多次给出；`--format` 为 `markdown|json`。

高风险强制要求 accountable owner、applicable rule、appeal path、rollback trigger；字段齐全也只返回 `governance_review_required`，不是合法、安全、公平、有效或可上线证明。输入仅作为数据，Markdown renderer 会转义用户文本。

## HUMAN 产物

1. **Human ends**：直接人的结果、不可牺牲边界、谁定义目的/能拒绝；
2. **Understand system**：输入—规则/模型—决定—人类动作—现实结果与供应链；
3. **Map feedback**：代理/直接结果/伤害/分群/申诉信号分开，记录时滞和改规则权；
4. **Assign agency**：信息、时间、训练、无惩罚覆盖、回写、可达申诉和最终责任；
5. **Negotiate test and exit**：基线、有限试点、阈值、暂停/回滚/退役和决策日志；
6. **劳动与分配**：被移除任务、新异常/情绪劳动、监控、自主、技能、收益方和风险承担者。

完整治理表单见 [`references/templates.md`](references/templates.md)；六轮研究见 [`references/research/`](references/research/)；复核命令见 [`VALIDATION.md`](VALIDATION.md)。

## 关键边界

- 数据收集、评分或投诉入口不自动构成闭环反馈；
- meaningful review 要求实际信息、时间、能力、覆盖权和组织支持；
- 人、动物和机器可作受限功能类比，不因此有相同经验或伦理地位；
- 责任可以分布但不能消失，重复伤害须考虑暂停或退役；
- 受影响者参与须检查代表性与实际规则改变权，不把咨询会当同意；
- 没有分群结果、申诉、劳动和真实结果数据时，只能保留待验证假设。

## 验证

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 ../../nuwa-skill/scripts/quality_check.py SKILL.md
```

从 [`SKILL.md`](SKILL.md) 开始完整执行，不要用“Wiener 会怎么说”替代现实治理证据。
