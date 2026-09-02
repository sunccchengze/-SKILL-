# Validation｜CONTROL

## 合同检查

- frontmatter `name/description` 可由仓库 parser 解析；
- `ESW001`–`ESW028` claim ID 唯一，A/B/C/D 层显式；
- source ledger 的每个引用 ID 存在，并有 supports / does-not-support / evidence grade / version / conflict-or-limit / unresolved；
- 六个 research tracks 均含 `workflow decision`、`failure gate`、`仍未验证`；
- CLI provenance 的 claim/source 均存在；
- schema 包含 `scope / control_structure / unsafe_control_actions / loss_scenarios`；
- epistemic status 固定 `hazard_analysis_not_safety_certification`；
- 高风险完整输入也只能 `governance_review_required`；
- analysis output 不出现 `status: approved`。

## 包行为测试

```bash
python3 -m unittest discover -s skills/community/nuwa-distilled/book-safer-world-control-audit/tests -v
```

10 个行为测试覆盖：确定性、书特定 schema、provenance、空值、重复值、高风险缺项、完整高风险仍审查、Markdown adversarial escaping、嵌套文件写入、不得批准。

## 仓库语义/来源测试

```bash
python3 -m unittest tests/test_nuwa_ai_era_core_classics.py -v
```

该套件不是关键词打卡：解析 claim/source 表，验证实际 source 存在；导入 CLI 运行书特定断言；检查四套 workflow/状态不互换；执行高风险门与 Markdown escaping；确认 24 个研究轨都有具体决策。

## CLI dry-run 类型

1. 普通 JSON：检查 schema、稳定排序、TODO 与非证明状态。
2. 普通 Markdown：检查用户内容转义和核心制品。
3. 高风险缺门：必须 stderr 列缺字段并 code 2。
4. 高风险完整：保留提交证据文本，标 `submitted_not_verified`，状态仍 review。

## 回归与目录

```bash
python3 -m unittest tests/test_nuwa_principles_distillation.py tests/test_nuwa_classics_distillations.py tests/test_nuwa_book_distillations.py -v
python3 scripts/build_catalog.py
python3 scripts/build_categories.py
python3 scripts/validate_repository.py
```

目录脚本顺序运行，避免覆盖。

## 尚未验证

- 本包未做外部可靠性、效度、inter-rater consistency 或现实 outcome 改善试验；
- source ledger 记录公开材料边界，不验证用户输入或生产系统；
- CLI 不替代统计/安全/制度/隐私领域专家、受影响者、法律或监管；
- 字段完成、测试通过和文件齐全都不等于现实方法有效或允许部署。
