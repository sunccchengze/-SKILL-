# 《Governing the Commons》制度诊断包

把书的独特分析对象压缩成可执行、可反驳、可追踪的 `COMMONS` 系统，而非通用读书摘要。

## 入口

1. [`SKILL.md`](SKILL.md)：主认知/操作合同、核心模型、工作流、失败门。
2. [`references/claim-layer-map.md`](references/claim-layer-map.md)：28 条唯一 claim 与 A/B/C/D 来源层。
3. [`references/source-notes.md`](references/source-notes.md)：supports / does-not-support / grade / version / conflicts / limitations / unresolved。
4. [`references/templates.md`](references/templates.md)：书特定制品。
5. [`references/research/`](references/research/)：六轮研究，每轮留下 workflow decision 与 failure gate。
6. [`scripts/design_commons_governance.py`](scripts/design_commons_governance.py)：确定性 JSON/Markdown CLI。
7. [`VALIDATION.md`](VALIDATION.md)：验证契约与命令。

## 冻结版本

- 1990 original; 2015 Canto bibliographic anchor ISBN 9781107569782
- 其他作者材料为 B；独立证据/批评为 C；本包 `COMMONS` 为 D。
- 不提供长段原文，不假装替代原书。

## 不变量

- 主链：resource system→boundaries→rules-in-use→monitoring→collective choice→conflict/sanctions→nesting。
- 输出状态：`institutional_diagnosis_not_governance_legitimacy`。
- 每个核心 claim 只有一个主层，并能解析到真实 source ID。
- 不把 open access 当 commons；不把八原则当配方/合法性。
- 人员、劳动、医疗、教育、信用、执法、内容治理默认高风险：真实影响、owner、规则、affected group、独立 contest/appeal、stop 与 rollback 缺项时 code 2；齐全仍是 `governance_review_required`。

## CLI

```bash
python3 scripts/design_commons_governance.py --help
```

CLI 只整理用户提交材料，不访问生产系统、不验证证据、不作现实决定。Markdown 转义用户输入；JSON 使用稳定 key order；重复/空白/超量输入受控失败；`--output` 自动创建父目录。

## 四层表达

| 层 | 表达 |
|---|---|
| A | “锁定原书提出/区分……” |
| B | “作者在后续某年材料扩展……” |
| C | “独立研究/批评在其样本和方法内发现……” |
| D | “本 Skill 创建 `COMMONS` 与发布门……” |

高影响输出不是部署、认证、合法性、临床、人事或法律批准。
