---
name: goodfellow-deep-learning-theory
description: |
  以 Goodfellow、Bengio、Courville《深度学习》官方在线书为数学/理论主模块，将假设、方程、计算图、梯度、优化行为与泛化失败连接到可运行数值检查。
  当用户要理解前馈网络、正则化、优化、CNN、序列建模、实践方法，诊断推导或为 Transformer/LLM 补理论基础时使用。
  必须交符号表、形状、假设、手推/数值梯度核对、失败案例与下一实验；Transformer/LLM 明确标为 post-2016 补充，不归原书。
---

# Goodfellow 深度学习理论模块

> **目标**：不把公式当咒语。每个主题走“假设 → 方程 → 计算 → 梯度/优化 → 泛化 → 失败实验”闭环。

## 一、六个心智模型

### 模型1：Assumptions precede equations｜方程之前先写假设

损失、概率、独立性、平稳性、可微性、标签和数据分布都带假设。

- **局限/失效**：假设全列完才动手会瘫痪；优先列会改变结论的 2–5 项并实测敏感性。

### 模型2：A computational graph is the bridge｜计算图连接数学与程序

把复合函数拆成节点、形状和局部导数，反向模式复用中间量。

- **局限/失效**：图正确不保证数值稳定、实现无广播错误或目标正确。

### 模型3：Optimization behavior is part of the model｜优化行为也是模型的一部分

初始化、尺度、曲率、学习率、batch 噪声和停止条件改变最后找到的函数。

- **局限/失效**：训练曲线不能单独识别原因；欠拟合、坏优化和数据问题可表现相似。

### 模型4：Regularization encodes preferences｜正则化编码偏好

权重衰减、早停、数据增强、dropout 等改变可接受解或训练动态，不只是“防过拟合按钮”。

- **局限/失效**：固定强度跨数据/架构外推会欠拟合；某些方法的简单解释并不完整。

### 模型5：Architecture expresses inductive structure｜架构表达归纳结构

卷积利用局部/共享结构，序列模型处理顺序状态；注意力重新组织交互和路径长度。

- **局限/失效**：架构标签不保证学到预期不变性；数据、位置编码、优化和规模共同作用。

### 模型6：Theory earns trust through numerical falsification｜理论靠数值反证获得信任

有限差分、极端输入、形状断言、消融和合成数据可发现符号/实现错误。

- **局限/失效**：有限差分受步长和浮点误差影响，只核对局部导数，不验证整体科学主张。

## 二、理论主线

按官方书结构提取主线，不复制全文：

1. **Ch.5 ML basics**：泛化、估计、最大似然、监督/无监督、挑战；
2. **Ch.6 Deep feedforward networks**：函数复合、输出、隐藏单元、架构与反向传播；
3. **Ch.7 Regularization**：参数范数、约束、数据增强、噪声、半监督、多任务、早停、dropout；
4. **Ch.8 Optimization**：经验风险、batch、初始化、自适应方法与优化挑战；
5. **Ch.9 CNN**：卷积、池化、结构先验与变体；
6. **Ch.10 Sequence modeling**：RNN、展开、长期依赖与门控；
7. **Ch.11 Practical methodology**：指标、基线、调试和改进策略。

Ch.2–4 数学基础按需补，不要求先把整本数学从头读完。

## 三、THEORY-TRACE 九步工作流

1. **Question**：要解释什么行为？例如梯度为何消失、正则为何改变 gap。
2. **Assumptions**：数据、概率、光滑、独立、尺度和近似前提。
3. **Notation and shapes**：每个符号、域、形状、batch 维和单位。
4. **Equation chain**：从目标到局部式逐步推，不跳“显然”。
5. **Computational graph**：节点、依赖、前向缓存和反向路径。
6. **Numerical check**：标准库小例子、有限差分、极端值和形状断言。
7. **Optimization prediction**：对学习率、初始化、batch/曲率的曲线先做方向预测。
8. **Generalization/error analysis**：区分推导、实现、优化、数据、目标和外推错误。
9. **Experiment and update**：只改一个假设/机制，记录配置、seed、环境、metric history、artifact path 与下一实验。

## 四、推导交付合同

```yaml
question: ...
source_chapter: ...
assumptions: [...]
notation_and_shapes: ...
objective: ...
equation_steps: ...
computational_graph: ...
analytic_gradient: ...
numerical_check:
  method: central finite difference
  step_sizes: [...]
  relative_error: ...
extreme_cases: ...
optimization_prediction: ...
generalization_failure: ...
error_analysis: ...
artifact_path: ...
next_experiment: ...
```

### 推导错误桶

- **符号**：变量重名、转置/求和索引错；
- **形状**：batch/feature 广播，标量与向量混淆；
- **微分**：链式法则、非光滑点、停止梯度；
- **数值**：overflow/underflow、灾难消减、步长不当；
- **优化**：梯度对但更新/尺度/初始化坏；
- **科学**：目标代理错、数据泄漏、分布不符、因果越权。

## 五、标准库数值核对

```bash
python3 scripts/check_derivation.py \
  --exercise finite-difference --x 0.7 --target 1 \
  --step 1e-5 --output derivation.json
```

脚本核对标量 logistic cross-entropy 对权重的解析梯度与中心有限差分，扫描多个步长，输出相对误差、极端案例、配置/环境和错误分类。它是微型合同，不替代自动微分或完整网络。

## 六、优化与泛化诊断矩阵

| 现象 | 候选机制 | 区分实验 |
|---|---|---|
| train/val 都差 | 表达不足、优化失败、标签/管线错 | 小样本过拟合、梯度/形状检查、更强基线 |
| train 好 val 差 | 方差、漂移、泄漏后反差 | 学习曲线、正则/增强、按部署 split |
| loss 振荡/爆炸 | 学习率、尺度、曲率、数值 | 降 LR、梯度范数、标准化/裁剪对照 |
| 早期快后停 | 饱和、条件数、优化器/表示 | 激活/初始化/归一化单因素对照 |
| 指标好但关键错误多 | 指标错配/切片掩盖 | 预先指定错误桶、代价/校准/群体指标 |

矩阵只生成假设，不替代实验识别。

## 七、Transformer/LLM 补充（post-2016）

原书出版于 2016 年；下列内容不得写成原作者原章节：

1. **Attention/Transformer**：从点积、softmax、mask、残差、归一化、位置表示和复杂度推导；读 Vaswani et al. 原论文。
2. **预训练目标**：tokenization、next-token/masked objectives 与数据分布；目标性能不等于事实性/推理/价值一致。
3. **微调/PEFT/对齐后训练**：以 Hugging Face Transformers 当前文档等版本化框架资料为实现入口，记录 model revision、文档访问日期、许可、数据、评估和错误。
4. **评估**：独立集、污染、生成指标不足、人工评价一致性和任务切片；不硬编码短命 leaderboard。
5. **能力边界**：把缩放/涌现陈述限定到具体模型、指标和日期，保留替代解释。

实践转 `d2l-lab-backbone`；经典基线/评估转 `zhou-classical-ml-reasoning`。

## 八、表达DNA

- **句式**：先写证据/假设与边界，再写动作；**词汇**：优先使用本 Skill 的工作流术语；**语气**：校准而不绝对化；**引用**：关键声明保留来源层和日期。

- **句式**：“在假设 A 下，由步骤 B 得 C；数值核对 D；若实验 E 失败，优先怀疑 F。”
- **词汇**：假设、形状、计算图、局部导数、条件数、泛化失败、反证。
- **语气**：黑板推导与实验调试交替，不用“数学证明所以现实有效”。
- **节奏**：定义 → 推导 → 算例 → 极端值 → 曲线预测 → 错误。
- **确定性**：定理结论附假设；经验判断附数据/环境。
- **引用**：2016 理论归官方书；Transformer/HF 归后续原始论文/当前文档；流程归本 Skill。

## 九、内在张力

> 下列每项都是必须保留、不能用口号消解的工作流张力。

- **数学抽象 vs 工程细节**：抽象揭示结构，广播/精度/缓存却能推翻实现。
- **优化成功 vs 科学正确**：loss 降低证明优化了目标，不证明目标或数据正确。
- **正则偏好 vs 数据证据**：先验有助小样本，也可能压制少数模式。
- **经典理论稳定 vs 当前架构漂移**：基础概念长寿，API/架构/评估快速变化。

## 十、诚实边界

- 本模块不复制官方在线书，仍需阅读原章节和练习。
- 数值梯度核对不证明解析式在所有点、张量形状或浮点环境正确。
- 理论简化假设不自动适用于大规模非凸、非独立、反馈式部署。
- 固定种子和环境日志提高可追溯性，不保证 GPU/框架跨平台逐位复现。
- Transformer/LLM 是明确的 2016 后补充；当前文档和能力结论会过期。

## 十一、来源导航

- [`references/source-notes.md`](references/source-notes.md)
- [`references/claim-layer-map.md`](references/claim-layer-map.md)
- [`references/templates.md`](references/templates.md)
- [`references/research/`](references/research/)
- [`VALIDATION.md`](VALIDATION.md)
