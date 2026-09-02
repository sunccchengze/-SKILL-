# 验证记录：book-fifth-discipline-learning-system

验证日期：2026-08-16。范围：本包的文本、CLI 和测试契约；**不证明**任何组织已成为学习型组织，也不验证某张现实因果图。

## 深层质量审计

| 维度 | 结果 | 可复核证据 | 残余边界 |
|---|---|---|---|
| 原书/谱系保真 | 通过 | F001–F008；原书、Forrester/系统动力学、组织学习分层 | 未做 1990/2006 逐章校勘 |
| 后续证据 | 通过 | FD-10–FD-14；GMB、模型验证、量表和权力批评 | 不是跨行业效果综述 |
| 可执行 | 通过 | LOOPS、8 组模板、deterministic CLI | LOOPS 未作效度量表验证 |
| 可反驳 | 通过 | 箭头证据、三类时滞、竞争解释、推翻观察、版本日志 | 定性图不估计效应量 |
| 权力/责任 | 通过 | 参与权力记录、责任双轨、高风险门 | 不替代调查、劳动/法律程序 |
| 来源追踪 | 通过 | 24 个 F-ID 与 source IDs；CLI 输出 provenance | 用户案例事实仍需现场来源 |

## 内容不变量

1. 先处理安全、违法、调查与明确责任，不等系统图；
2. 问题必须有可观察变量、时间范围、边界和受影响群体；
3. 单点不是模式，单箭头不是反馈，定性图不是仿真；
4. 关键箭头带证据、作用/观测/治理时滞和反驳条件；
5. 至少保留一个竞争解释和图外变量；
6. 基模写“像……，待核”，并记录不匹配；
7. 结构解释不取消责任，参与/共识不自动证明公平；
8. 干预有限、可逆、可测，有副作用与停止条件；
9. 高风险 CLI 输出只能是 `analysis_only`；
10. 原图和事前预测必须版本化保留。

## 已运行的包测试

命令（仓库根目录）：

```bash
python3 -m unittest discover \
  -s skills/community/nuwa-distilled/book-fifth-discipline-learning-system/tests \
  -p 'test_*.py' -v
```

2026-08-16 结果：**10/10 通过**。覆盖直接 builder、确定性 JSON、Markdown 转义、空值/重复值/最小变量校验、高风险门、analysis-only 状态、输出文件和 renderer 稳定性。

## 从包根目录运行

```bash
cd skills/community/nuwa-distilled/book-fifth-discipline-learning-system
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 ../../nuwa-skill/scripts/quality_check.py SKILL.md
python3 ../../../../tests/test_nuwa_classics_distillations.py
```

## 从仓库根目录运行

```bash
python3 -m unittest discover -s skills/community/nuwa-distilled/book-fifth-discipline-learning-system/tests -p 'test_*.py' -v
python3 skills/community/nuwa-skill/scripts/quality_check.py skills/community/nuwa-distilled/book-fifth-discipline-learning-system/SKILL.md
python3 tests/test_nuwa_classics_distillations.py
python3 scripts/validate_repository.py
```

注意：`python3 -m unittest tests.test_nuwa_classics_distillations` 在本仓库并非可靠命令，因为 `tests` 不是可导入包；使用上面的脚本路径。

## 对抗与干跑

- **版本赶工**：主回路可为压力→测试压缩→延迟缺陷→返工→压力；必须保留需求复杂度、人员更替和口径变化等竞争解释。
- **折扣依赖**：可探查舍本逐末，但须以客户分群、价格弹性和根本能力数据区分，不凭基模定论。
- **校园安全事故**：先保护、报告、调查和补救；结构复盘不能洗去违规责任。
- **不可信输入**：CLI 对表格元字符转义，空白/重复受控报错，不执行输入文本。

## 盲点与停止线

- 未实现 stock-flow、方程、参数、敏感性分析或仿真；
- GMB 参与质量仍受职位、语言、促导与缺席群体影响；
- 学习型组织没有本包认可的统一普适分数；
- 若用户要求精确预测、法律/临床判断或紧急处置，必须路由而不是扩大 LOOPS。
