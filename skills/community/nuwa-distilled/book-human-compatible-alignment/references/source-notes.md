# 来源总表与主张登记

> 复核日期：2026-08-16。形式模型结论必须连同假设表述；行为数据不得被写成授权或合法性。

| ID | 层 | 来源 | 支持 | 不支持 |
|---|---|---|---|---|
| HC-A01 | A | Russell, S. (2019). *Human Compatible: Artificial Intelligence and the Problem of Control*. Viking/Penguin Random House. https://www.penguinrandomhouse.com/books/566677/human-compatible-by-stuart-russell/ | 标准模型批评、可证明有益机器、偏好不确定性的书中论证 | 不代表问题已解决或所有人共享一个效用函数 |
| HC-A02 | A | Russell, S. (2021). “Provably Beneficial Artificial Intelligence.” In *The Frontiers Collection*. DOI: 10.1007/978-3-030-86144-5_3 | 作者对三原则的明确表述与研究议程 | 不提供现实部署安全保证 |
| HC-B01 | B | Hadfield-Menell et al. (2016). “Cooperative Inverse Reinforcement Learning.” NeurIPS 29. https://papers.nips.cc/paper/6420-cooperative-inverse-reinforcement-learning | CIRL 形式化：共享回报、机器对回报参数不确定、从互动学习 | 假设不自动适配现实多主体社会 |
| HC-B02 | B | Hadfield-Menell et al. (2017). “The Off-Switch Game.” IJCAI-17, 220–227. DOI: 10.24963/ijcai.2017/32 | 在特定博弈/理性假设下，不确定性与服从关闭的激励关系 | 不证明任何“有不确定性”的系统现实可关闭 |
| HC-B03 | B/C | Ng, A. Y., & Russell, S. (2000). “Algorithms for Inverse Reinforcement Learning.” ICML. | 从行为反推奖励的经典形式问题及欠定性背景 | 不把反推奖励等同真实/合法偏好 |
| HC-C01 | C | Milli et al. (2017). “Should Robots be Obedient?” IJCAI-17. DOI: 10.24963/ijcai.2017/30 | 不完全理性模型下服从与偏好学习问题 | 不提供通用治理方案 |
| HC-C02 | C | Sen, A. (1977). “Rational Fools.” *Philosophy & Public Affairs*, 6(4), 317–344. | 对以选择/自利效用穷尽承诺、规范与行为的经典批评 | 不直接评估 AI 偏好学习算法 |
| HC-C03 | C | Elster, J. (1982). “Sour Grapes—Utilitarianism and the Genesis of Wants.” In *Utilitarianism and Beyond*. | 适应性偏好与欲望形成问题 | 不说明所有偏好变化都不正当 |
| HC-C04 | C | Selbst et al. (2019). “Fairness and Abstraction in Sociotechnical Systems.” FAccT. DOI: 10.1145/3287560.3287598 | 社会技术抽象、制度边界与实施陷阱 | 不否定所有形式化 |
| HC-C05 | C | NIST (2023). *AI Risk Management Framework 1.0*. DOI: 10.6028/NIST.AI.100-1 | 治理、风险映射、测量、管理和责任 | 不解决偏好聚合哲学问题 |

## 主张—来源—边界

| 主张 | 类型 | 来源 | 必须附带的边界 |
|---|---|---|---|
| 三原则以人的偏好为目标、机器起初不确定、行为为信息来源 | Russell 研究提案 | HC-A01, HC-A02 | 行为不是授权；偏好主体/聚合/合法性仍未解决 |
| CIRL 将协助建模为共享回报和信息不对称博弈 | 技术模型 | HC-B01 | 依赖共享回报、行为模型等假设 |
| 偏好不确定在 Off-Switch Game 中可改变关闭激励 | 形式结果 | HC-B02 | 非现实系统安全证明；需技术+基础设施+组织测试 |
| 选择可受约束、承诺和适应影响 | 规范/社会批评 | HC-C02, HC-C03 | 不意味着观察或陈述一概无用 |
| 六类证据、查询预算、社会技术纠正性和十步审查 | D 层综合 | HC-A01–HC-C05 | 不是 Russell 原流程或通用安全算法 |

## 引用纪律

1. 三原则的概括归 Russell；PREFERENCE-UNCERTAIN 归本 Skill。
2. 提及 Off-Switch 结论必须写“在模型假设下”，不得简化为“AI 不确定就愿意关机”。
3. `observed behavior` 只能进入证据登记，不能直接标为同意、福利或权限。
4. 聚合规则、权利底线、否决与申诉需引用本地法律/制度/参与记录，而非只引 AI 论文。
