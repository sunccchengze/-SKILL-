# 验证记录：book-human-use-cybernetics

验证日期：2026-08-16。范围：本包的文本、CLI 和测试契约；**不构成**伦理认证、法律意见、劳动协商结果或现实部署影响评估。

## 深层质量审计

| 维度 | 结果 | 可复核证据 | 残余边界 |
|---|---|---|---|
| 版本/归因 | 通过 | H001–H008；1950/1954、1948/1961 与现代治理分开 | 未做两个版本逐章校勘 |
| 当代治理 | 通过 | HU-10–HU-13；NIST、ILO、EDPS | 需逐法域/行业核适用规则 |
| 科学边界 | 通过 | 功能类比≠伦理同等；社会熵不伪量化 | 跨层类比仍有解释争议 |
| 可执行 | 通过 | HUMAN、9 组治理模板、deterministic CLI | HUMAN 未作为量表验证 |
| 人本/劳动 | 通过 | meaningful review、申诉/退出、任务/技能/监控/分配 | 不替代工会/员工协商 |
| 来源追踪 | 通过 | 24 个 H-ID 与 source IDs；CLI provenance | 用户系统事实仍需现场证据 |

## 内容不变量

1. 先写直接人的目的与不可交易护栏，再写代理指标；
2. 控制论描述、历史类比、规范判断和现代机制分层；
3. 代理、直接结果、伤害、分群结果和申诉信号分开；
4. 数据收集或投诉入口存在不等于反馈闭环；
5. 人工监督必须有信息、时间、训练、覆盖权、无惩罚和回写；
6. 必须记录任务迁移、隐形劳动、监控、自主、技能与收益/成本分配；
7. 高风险要求 owner、rule、appeal、rollback 四字段；
8. 四字段齐全仍只进入 `governance_review_required`，不是批准；
9. 责任可分布但不得消失；重复伤害须考虑停止/退役；
10. Wiener 经典不能证明具体当代 AI 产品结果。

## 已运行的包测试

命令（仓库根目录）：

```bash
python3 -m unittest discover \
  -s skills/community/nuwa-distilled/book-human-use-cybernetics/tests \
  -p 'test_*.py' -v
```

2026-08-16 结果：**10/10 通过**。覆盖直接 builder、确定性 JSON、Markdown 转义、空值/重复值校验、高风险四字段门、非批准状态、输出文件、恶意 shell 文本作为纯数据和 renderer 稳定性。

## 从包根目录运行

```bash
cd skills/community/nuwa-distilled/book-human-use-cybernetics
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 ../../nuwa-skill/scripts/quality_check.py SKILL.md
python3 ../../../../tests/test_nuwa_classics_distillations.py
```

## 从仓库根目录运行

```bash
python3 -m unittest discover -s skills/community/nuwa-distilled/book-human-use-cybernetics/tests -p 'test_*.py' -v
python3 skills/community/nuwa-skill/scripts/quality_check.py skills/community/nuwa-distilled/book-human-use-cybernetics/SKILL.md
python3 tests/test_nuwa_classics_distillations.py
python3 scripts/validate_repository.py
```

注意：`python3 -m unittest tests.test_nuwa_classics_distillations` 在本仓库并非可靠命令，因为 `tests` 不是可导入包；使用上面的脚本路径。

## 对抗与干跑

- **AI 客服**：平均时长不得替代正确解决；记录紧急用户错拒、重复联系、分群、申诉可达和一线覆盖权。
- **自动排班**：记录可预期性、照护/健康限制、监控、自主、异常劳动、分配与代表性参与。
- **医疗分诊**：只生成治理工作表；要求临床 owner、验证、规则、人工通道、事故响应和不可自动项。
- **不可信输入**：CLI 转义表格字符，不调用 shell；重复/空白字段受控报错。

## 盲点与停止线

- 不提供具体法域法律意见、医学验证、安全认证或宏观就业预测；
- meaningful review 的充分时间/能力阈值依风险而变；
- 高风险缺少任何四字段时拒绝生成；即使字段齐全也不得描述为合规或上线批准；
- 没有日志、分群、申诉、劳动与结果数据时，只能保留待验证假设。
