---
name: zhou-classical-ml-reasoning
description: |
  以周志华《机器学习》的经典模块序列训练问题设定、模型假设、评估选择和错误分析，并用开源南瓜书仅辅助难公式推导。
  当用户要学习或比较线性模型、决策树、SVM、贝叶斯、集成、聚类、降维，或在深度学习前补数据划分与模型选择纪律时使用。
  必须先定义预测单位、标签时点和部署分布，split first，所有预处理/特征选择/阈值/模型选择在训练/验证内部完成；南瓜书不是原教材替代品。
---

# 周志华经典机器学习推理模块

> **目标**：不是背算法目录，而是练成“问题设定 → 假设 → split → 基线 → 模型对比 → 错误/不确定性 → 下一实验”的经典 ML 推理。

## 一、六个心智模型

### 模型1：Inductive bias is the real model choice｜模型选择是归纳偏好选择

线性、树、间隔、概率、集成分别约束函数形状、分割、几何、生成过程或误差组合。

- **局限/失效**：标签“可解释/非线性”太粗；实际行为还受特征、正则、优化和数据影响。

### 模型2：Evaluation design precedes algorithm choice｜评估设计先于算法

预测单位、标签可得时点、部署群体、错误代价和 split 决定分数含义。

- **局限/失效**：离线评估仍可能无法反映反馈回路、制度变化和部署成本。

### 模型3：Bias–variance is a diagnostic lens, not one decomposition for all｜偏差—方差是诊断镜头

比较训练/验证随样本与复杂度变化可提出欠拟合、过拟合或噪声假设。

- **局限/失效**：现实损失、非独立数据和现代模型不总能由教科书式分解充分解释。

### 模型4：Geometry and probability offer rival explanations｜几何与概率是竞争解释

SVM/距离/降维强调几何；贝叶斯/似然强调生成与不确定；同一结果可由不同假设解释。

- **局限/失效**：高维距离退化、概率模型错设和未校准分数都会误导。

### 模型5：Ensembles trade diversity for complexity｜集成用差异换稳健，也增加复杂性

bagging 降低不稳定，boosting 逐步聚焦误差；收益取决于基学习器误差相关性。

- **局限/失效**：更多模型不自动更好；计算、校准、可解释与分布漂移成本上升。

### 模型6：Unsupervised structure is objective-relative｜无监督结构依赖目标

聚类/降维发现的是由距离、尺度、维数或重构目标定义的结构，不是数据天然类别。

- **局限/失效**：漂亮二维图、轮廓系数或稳定簇不自动具有领域意义或因果性。

## 二、先修与模块顺序

顺序服务推理依赖，不是原书唯一读法：

1. **问题设定与评估**：假设空间、经验误差、泛化、train/validation/test、指标与代价；
2. **线性模型**：回归、分类、正则、校准和可解释基线；
3. **决策树**：分裂、剪枝、缺失、类别/连续属性与不稳定；
4. **SVM/核**：间隔、软间隔、核假设、尺度和计算；
5. **贝叶斯**：生成假设、条件独立、平滑、概率与决策；
6. **集成**：bagging、boosting、偏差/方差/相关性；
7. **聚类**：距离、原型、密度/层次、稳定性与外部意义；
8. **降维/表示**：PCA 等线性结构、可视化与信息损失。

难公式可查 Datawhale **Pumpkin Book/南瓜书** 的开源推导；它是伴读，不是权威勘误、完整教材或版权替代。

## 三、CLASSIC-TRACE 九步工作流

1. **Frame**：预测/描述/排序/决策？样本单位、目标总体、时间和动作是什么？
2. **Label audit**：标签何时可得、谁标、噪声/选择/代理/未来信息在哪里？
3. **Metric and cost**：先选主要指标和错误代价；不平衡时不只看 accuracy。
4. **Split before fit**：按时间/主体/群组/部署单位切分；final test 锁定。
5. **Baseline**：多数/均值、简单线性或领域规则；同数据流、同指标。
6. **Assumption card**：模型为何适合？列关键假设、诊断、计算和解释成本。
7. **Train/validate inside the boundary**：预处理、特征、阈值、超参和模型选择只在训练/验证或 CV 折内。
8. **Error and uncertainty analysis**：混淆矩阵/残差、至少三类错误、切片、校准/区间和竞争解释。
9. **Freeze, test once, decide**：冻结方案后一次测试；决定部署/补数据/换指标/换模型，并开新版本。

## 四、模型假设卡

| 家族 | 首问 | 最小诊断 | 常见误用 |
|---|---|---|---|
| 线性/逻辑 | 线性预测器与尺度是否合理？ | 残差、正则路径、校准 | 系数直接作因果效应 |
| 树 | 分裂是否稳定、深度是否过拟合？ | 学习曲线、扰动稳定性 | feature importance 当因果 |
| SVM/核 | 间隔/核与尺度是否合适？ | 标准化、C/核敏感性 | 高维/大样本盲调 |
| 贝叶斯 | 生成/独立假设哪里错？ | 类条件误差、校准 | 后验概率自动可信 |
| 集成 | 基学习器错误是否有差异？ | 单模型对照、相关错误 | 只加模型不算成本 |
| 聚类 | 距离和 K 为何有意义？ | 多初始化/尺度稳定、领域审阅 | 把簇命名为真实类型 |
| 降维 | 保留哪种结构/损失？ | 重构、下游、稳定性 | 二维图距离过度解释 |

## 五、可运行微实验

```bash
python3 scripts/run_micro_experiment.py \
  --exercise split-baseline --seed 11 --epochs 80 \
  --output classic-experiment.json
```

标准库脚本生成有噪声二分类：固定 train/validation/test；只在 train 拟合标准化；比较多数基线与逻辑回归；输出 loss history、混淆矩阵、三个最大损失样本、错误桶、一次 final test 和下一实验。

### 每次实验必须交

- problem/target/split unit/label timing；
- hypothesis + model assumption card；
- data version、seed、environment、configuration；
- baseline 与 metric history；
- artifact path、error analysis、uncertainty；
- final-test touches=1、限制和下一实验。

## 六、泄漏不变量

1. split 在标准化、填补、特征选择、采样、阈值和模型选择之前；
2. CV 的每一折内部重新拟合所有数据依赖步骤；
3. 时间任务只能用预测时可见特征；同一人/设备/文档的相关样本按组处理；
4. final test 不用于选择指标、模型、阈值或特征；
5. 看过 test 后的任何修改都创建新版本和新最终评估。

## 七、Transformer/LLM 连接（post-2016/current supplement）

经典推理仍适用于：冻结 embedding 的线性 probe、检索/分类基线、阈值与校准、错误切片、聚类稳定性和低维诊断。不要把 probe 表现当表示“理解”，也不要用 t-SNE/UMAP 图证明语义类别。微调转 `d2l-lab-backbone`，理论转 `goodfellow-deep-learning-theory`；当前 API/评估以 Hugging Face 官方文档为准。

## 八、表达DNA

- **句式**：先写证据/假设与边界，再写动作；**词汇**：优先使用本 Skill 的工作流术语；**语气**：校准而不绝对化；**引用**：关键声明保留来源层和日期。

- **句式**：“模型假设 X；若 Y 诊断失败，就换解释而非只调参。”
- **词汇**：预测单位、标签时点、归纳偏好、split unit、基线、错误代价。
- **语气**：先问问题与评估，再谈算法；不崇拜复杂模型。
- **节奏**：设定 → 假设 → 基线 → 对照 → 错误 → 决定。
- **确定性**：区分预测、关联、概率校准和因果，不用准确率替代全部价值。
- **引用**：经典模块归教材；南瓜书仅伴读；CLASSIC-TRACE 归本 Skill。

## 九、内在张力

> 下列每项都是必须保留、不能用口号消解的工作流张力。

- **模型简洁 vs 表达能力**：简单模型易审计但可能欠拟合；复杂模型需证明净增益。
- **指标统一 vs 错误代价异质**：同一分数方便比较，却可能掩盖群体/类别代价。
- **概率形式 vs 模型错设**：概率输出看似精确，假设错误时会过度自信。
- **探索 test 错误 vs 保留无偏评估**：错误很有价值，但看过后必须进入新周期。

## 十、诚实边界

- 本模块不复制《机器学习》原文/习题答案，也不替代购买或课程教学。
- 南瓜书是开源推导伴读，不代表周志华原书，也不保证无误。
- 标准库微实验只示范推理/记录合同，不是高性能 ML 库。
- 离线评估和经典统计假设不能保证部署、公平、因果或长期反馈安全。
- Transformer 连接是后续补充，不归入 2016 年教材原有内容。

## 十一、来源导航

- [`references/source-notes.md`](references/source-notes.md)
- [`references/claim-layer-map.md`](references/claim-layer-map.md)
- [`references/templates.md`](references/templates.md)
- [`references/research/`](references/research/)
- [`VALIDATION.md`](VALIDATION.md)
