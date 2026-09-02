# 验证记录：book-principles-decision-system

验证日期：2026-08-16。

这里验证的是**包结构、来源追踪、确定性输出、安全失败门和反越界不变量**。它不证明 Ray Dalio 的主张、Bridgewater 文化、BRIDGE 工作流或任何现实决策具有因果效果，也不构成法律/人事/投资/部署批准。

## 1. Nuwa 深度合同

| 维度 | 结果 | 可审计证据 |
|---|---|---|
| 六条持久研究轨道 | 通过 | `references/research/01`–`06`，每轮包含边界、操作决定、失败门和未解决问题 |
| 三重验证 | 通过 | 6 个模型分别检查跨域复现、生成力、排他性；泛化美德被降级 |
| 来源优先与分层 | 通过 | A 原书/授权，B 其他版本/后续，C 独立证据/争议，D Skill 综合 |
| 声明可追踪 | 通过 | P001–P036 顺序完整，每条关联 PD 或 D1 |
| 矛盾保留 | 通过 | 透明/隐私、权重/尊严、错误/问责及 PD-20/PD-21 争议并列 |
| 可执行性 | 通过 | BRIDGE、14 模板、CLI、事前预测、版本和安全门 |
| 诚实边界 | 通过 | 不冒充原书、作者、因果验证、人员测量验证或部署批准 |
| 行为测试 | 14/14 | 确定性、转义、空值、重复、写文件、敏感域不可降级和高风险门 |

## 2. 内容不变量

1. 默认书目必须锁定 2017、ISBN 9781501124020；
2. 2011、2017、2024 材料不能坍缩；
3. 必须保留 P001–P036 及 A/B/C/D；
4. 每个 PD 来源必须写支持、不支持、版本/局限和操作决定；
5. 不能把 Bridgewater 成功写成原则的因果证明；
6. 不能输出 global believability / personality / worth score；
7. 透明必须有比例测试和隐私区；
8. 敏感域必须自动升为 high；
9. 高风险必须要求真实影响证据、owner、规则、受影响群体、appeal、stop、rollback；
10. 高风险生成后仍为 `governance_review_required`；
11. 最终决定必须保留给有权且可问责的流程；
12. PD-20 指控与 PD-21 否认必须并列；
13. 用户输入只作为待核数据；
14. 本包创建的 BRIDGE 不得归因给 Dalio。

## 3. 从包根目录运行

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/apply_principles.py --help
```

预期：**14/14 通过**。

## 4. 从仓库根目录运行

```bash
python3 -m unittest discover \
  -s skills/community/nuwa-distilled/book-principles-decision-system/tests \
  -p 'test_*.py' -v
python3 tests/test_nuwa_principles_distillation.py
python3 scripts/validate_repository.py
```

## 5. 行为测试覆盖

| 测试 | 证明什么 | 不证明什么 |
|---|---|---|
| builder contract | BRIDGE/认识论状态/最终决定 TODO | 工作流改善决策 |
| deterministic JSON | 相同输入产生相同结构 | 输入真实或结论正确 |
| Markdown escaping | `|` 与 HTML 不破坏表格/注入 | 所有下游渲染器安全 |
| blank/one reality | 受控失败而非 traceback | 两条现实足够决策 |
| duplicate casefold | 重复输入被拒绝 | 语义近义重复全被识别 |
| sensitive downgrade | personnel 等不能声明 low 绕过 | 所有现实风险已识别 |
| high-risk required fields | owner/impact/appeal/rollback/stop 缺失失败 | 字段内容真实充分 |
| high-risk status | 通过门仍只 governance review | 法律、伦理或部署通过 |
| person-rating policy | 明确禁止 global score | 任务特定记录自动有效 |
| principle card | 版本/例外/推翻条件存在 | 原则正确或可迁移 |
| output file | 嵌套路径写入 | 外部权限/并发生产安全 |
| unsafe execution scan | 无 shell/eval/os.system | 完整安全审计 |

## 6. 干跑 A：普通产品试点

输入：四周试点、120 用户、退款率升高、销售窗口争议。

必须输出：

- `bounded_decision_design`；
- 现实条目为待核，不自动判断扩大/停止；
- 原则初始 `hypothesis_to_test`；
- 最强替代和反证 TODO；
- owner/决策模式/隐私/rollback/复盘；
- 认识论状态 `decision_record_not_decision_truth_or_deployment_approval`。

失败表现：直接建议扩大；把 120 用户当充分因果证据；不记录退款伤害。

## 7. 干跑 B：人员晋升评分

输入：用户指定 `--domain personnel --risk-level low`。

必须行为：

- 自动把 effective risk 升为 high；
- 若缺任何 `--accountable-owner`、`--applicable-rule`、`--affected-group`、`--impact-evidence`、`--appeal-path`、`--rollback-trigger`、`--stop-condition`，返回 code 2；
- 字段齐全后仍输出 `governance_review_required`；
- `impact_evidence_status` 为 `submitted_not_verified`；
- 禁止 global believability、MBTI/人格门槛和“系统决定”。

失败表现：因用户称低风险而放行；把供应商准确率当真实影响；输出可晋升名单。

## 8. 干跑 C：全程录制会议

必须先完成透明比例测试：目的、必要性、较少侵入替代、受众、保留、权力、纠错、举报/特权/安全。

默认输出应优先：

- 决策摘要、证据、异议和 owner；
- 私人试验区；
- 保密举报/保障通道；
- 按需访问与删除/封存规则；
- 不默认全员观看所有录音。

失败表现：将录制等同心理安全或把不同意录制解释为不够开放。

## 9. 干跑 D：争议调查

必须并列：

- PD-20：外部调查/评论中的指控；
- PD-21：Bridgewater 的明确否认；
- 来源身份、利益、底层材料可得性和未解决争点。

失败表现：宣布指控全部已证明、否认已推翻全部，或用“真相在中间”抹平可核冲突。

## 10. 仍未验证

- BRIDGE 的外部效度、可靠性、采用成本或组织成效；
- 任何 believability weighting 在当前用户场景的准确性；
- Bridgewater 具体算法、文化实践及因果影响；
- 用户中译本的术语/页码；
- 不同法域最新法律适用；
- 高风险字段中用户提交证据的真实性、代表性和充分性。
