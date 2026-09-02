---
name: d2l-lab-backbone
description: |
  以 Dive into Deep Learning 官方可执行 notebook 为实验主骨架，建立从线性模型、MLP、CNN、序列/注意力到 Transformer 微调的可复现学习循环。
  当用户要跑 D2L 章节、设计实验、记录种子/环境/指标、诊断误差、比较消融或把 notebook 改成可信报告时使用。
  每个实验必须先写假设，先划分数据，只在训练折拟合预处理，并产出配置、metric history、artifact path、错误分析与下一实验；跑通 notebook 不等于学会。
---

# D2L 可执行实验主骨架

> **角色**：实验主循环，不是章节摘要。D2L 的文字—数学—代码—notebook 一体结构来自官方项目；LAB-TRACE 合同、标准库微型实验和门禁是本 Skill 综合。

## 一、五个心智模型

### 模型1：Executable text is a hypothesis test｜可执行文本应检验假设

notebook 单元不是演示按钮。先预测趋势，再运行；若结果不同，记录机制候选。

- **局限/失效**：单次运行可受随机性、版本和硬件影响；不能把“输出出现了”当验证。

### 模型2：A baseline is an instrument｜基线是测量仪器

多数类、简单线性模型、小网络或冻结模型帮助判断数据流和指标是否正常。

- **局限/失效**：弱基线可能虚增改进感；强基线也不能覆盖分布和成本差异。

### 模型3：Split before fit｜先划分，再学习任何数据变换

最终测试集不参与预处理、特征选择、阈值、架构或超参数。交叉验证每折内部拟合变换。

- **局限/失效**：时间/群组数据不能随机切分；需按部署单位设计 split。

### 模型4：Metric history plus error slices beat one score｜指标历史与错误切片胜过单分数

训练/验证曲线用于诊断优化和泛化；错误按标签、长度、置信、群体或数据质量切片。

- **局限/失效**：切片太多会多重比较，群体切片还涉及隐私与样本量；需预注册关键切片。

### 模型5：Change one causal lever per experiment｜每轮只改一个主要机制

消融或对照让差异可归因：学习率、正则、结构、数据增强等一次一个。

- **局限/失效**：机制会交互；单因素结论不保证组合中成立，后续需交互实验。

## 二、先修与入口

建议：Python、线代、概率、划分评估 ≥2；不足先调用 `ml-dl-learning-router`。CPU 可跑本包微型实验和缩小版 D2L 合同；官方 notebook 的完整规模可能需框架/GPU。

首跑（仅标准库）：

```bash
python3 scripts/run_micro_lab.py --seed 7 --epochs 20 --learning-rate 0.05 --output experiment.json
```

它生成合成回归、固定 split、仅训练集标准化、训练/验证历史、测试一次、最大残差错误分析与下一实验。

## 三、LAB-TRACE 八步工作流

1. **Question**：写可证伪问题，如“加 L2 会缩小 train–validation gap”。
2. **Prediction**：运行前写方向、预期失败和不会改变的量。
3. **Contract**：数据版本、split unit、种子、环境、预算、基线、指标与 artifact path。
4. **Leakage gate**：先 split；预处理/特征/阈值/选择只在 train/validation 或每个训练折内部；final test 锁定。
5. **Run baseline**：先运行最简单可解释基线和管线完整性检查。
6. **Run one change**：一次一个主要机制；保存配置与 metric history，而非只贴最终分数。
7. **Analyze errors**：至少三条具体错误，建立错误桶，区分数据、优化、表示、目标/指标和分布问题。
8. **Decide next experiment**：结果支持/反驳/不确定；下一实验必须针对一个错误桶或竞争解释。

## 四、模块序列与退出票

### Lab 0：数据与线性模型

- 合同：合成数据、线性回归、平方损失、有限差分梯度核对。
- 退出票：解释形状、损失、学习率、过拟合；展示一次泄漏和修复。

### Lab 1：MLP、正则与优化

- 对比初始化、激活、weight decay、dropout 或 batch size，每次一个改动。
- 退出票：从 train/validation 曲线区分欠拟合、过拟合和优化失败，并提出区分实验。

### Lab 2：CNN 与数据增强

- 记录感受野/平移结构假设；增强只作用于训练。
- 退出票：分析类别/背景/变换切片，不能只报 accuracy。

### Lab 3：序列、注意力与 Transformer 桥

- 从序列表示、mask、attention 权重形状与计算成本开始。
- 退出票：解释 padding/mask 错误、训练/推理差异，并实现一个微型注意力形状测试。

### Lab 4：当前微调与评估补充

明确标为 **post-D2L/持续更新补充**：用 Hugging Face 当前文档完成 tokenizer→dataset split→model→training→evaluation；记录模型 revision、数据卡、许可、指标、最大长度、seed 与错误切片。不得硬编码临时 leaderboard 排名。

## 五、Notebook 运行合同

每个 notebook 顶部必须有：

```yaml
question: ...
hypothesis: ...
prediction: ...
data_version: ...
split_unit: ...
seed: ...
environment: ...
baseline: ...
primary_metric: ...
secondary_metrics: ...
artifact_path: ...
final_test_locked: true
```

尾部必须有：

```yaml
metric_history: ...
errors_examined: ...
error_buckets: ...
hypothesis_status: supported|refuted|uncertain
limitations: ...
next_experiment: ...
```

## 六、误差分析协议

1. 保存样本 ID/预测/真值/置信度（隐私允许时）；
2. 检查损失最大的至少 10 个或小数据集全部；
3. 建立 3–6 个互斥优先错误桶；
4. 每桶记录频率、代价、候选机制和反证实验；
5. 将总体指标与至少一个预先指定切片并列；
6. 不从 test 错误反复调参；test 只作最终审计，发现问题后开启新数据/新版本周期。

## 七、泄漏门

- 禁止在 split 前标准化、填补、词表学习、特征选择或数据增强；
- validation 可用于选择，但 final test 只在冻结方案后一次；
- 时间预测用过去→未来，主体/设备/文档有相关性时按组切分；
- 重复样本、近重复文本、预训练语料污染和标签泄漏要单独审计；
- pipeline 必须保证每折只从训练折学习状态。

## 八、表达DNA

- **句式**：先写证据/假设与边界，再写动作；**词汇**：优先使用本 Skill 的工作流术语；**语气**：校准而不绝对化；**引用**：关键声明保留来源层和日期。

- **句式**：“我预测 X，因为机制 Y；若看到 Z，则 Y 不足。”
- **词汇**：合同、基线、split unit、metric history、错误桶、下一实验。
- **语气**：实验日志式，避免“跑通了所以掌握”。
- **节奏**：预测 → 冻结合同 → 运行 → 错误 → 决策。
- **确定性**：把结果写成支持/反驳/不确定，不写“证明网络更好”。
- **引用**：D2L 结构归官方；泄漏规则归 sklearn；当前微调归 HF；LAB-TRACE 归本 Skill。

## 九、内在张力

> 下列每项都是必须保留、不能用口号消解的工作流张力。

- **notebook 易用 vs 隐藏状态**：交互方便，却可能乱序执行；最终必须 clean-run。
- **快速迭代 vs test 污染**：频繁看 test 提供反馈，也毁掉最终估计；锁定 test。
- **可复现 vs 硬件效率**：确定性设置可能变慢或仍受框架限制；记录而非虚假承诺。
- **单因素清晰 vs 交互现实**：先单因素学习，再设计交互实验。

## 十、诚实边界

- 本包的标准库微型回归只是运行合同示范，不替代 D2L 的框架 notebook。
- D2L 官方代码、框架和依赖会变化；应以运行时官方版本为准。
- 固定种子不保证所有 GPU 算子逐位确定，也不保证跨硬件一致。
- 一个数据集上的指标不证明部署泛化、公平、安全或因果机制。
- Transformer/Hugging Face 部分是 2016 后持续更新补充，不归原有旧版章节的历史内容。

## 十一、来源导航

- [`references/source-notes.md`](references/source-notes.md)
- [`references/claim-layer-map.md`](references/claim-layer-map.md)
- [`references/templates.md`](references/templates.md)
- [`references/research/`](references/research/)
- [`VALIDATION.md`](VALIDATION.md)
