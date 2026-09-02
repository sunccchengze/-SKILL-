---
name: ml-dl-learning-router
description: |
  诊断 Python、线代、微积分、概率统计、数据划分评估、神经网络熟悉度与算力，并在 周志华经典机器学习推理、D2L 可执行实验、Goodfellow 深度学习理论三个模块中只选择一个下一站。
  当用户不知道从哪学、反复收藏路线却不实验、要从经典 ML 转深度学习/Transformer，或需要可验证的先修补丁与退出票时使用。
  不按学历或自信打分，不生成巨型书单；诊断只是可修订路由，不是能力测验或就业认证。
---

# ML/DL 学习路由器

> **唯一任务**：给出一个下一模块、少量阻塞先修、一个可运行入口和退出标准。不是“把三本书从头读到尾”。

## 一、五个心智模型

### 模型1：Observable diagnostics beat self-labels｜可观察诊断胜过“我是新手”

用小任务检查七维：Python、线代、微积分、概率统计、划分/评估、神经网络、算力。

- **局限/失效**：自评 0–3 受信心和经验影响；应由小测产物校正，不用于筛人。

### 模型2：One next module, not a giant itinerary｜一次只选一个下一站

学习瓶颈通常不是资料不够，而是下一实验不清楚。路由器只给一个模块和最多三个补丁。

- **局限/失效**：真实项目可跨模块；“一个下一站”是执行约束，不是否认知识互联。

### 模型3：Reasoning, execution and theory are distinct loops｜推理、运行、理论三条回路

- 周志华模块：问题设定、模型比较、评估和经典方法推理；
- D2L：可运行 notebook/实验与误差分析；
- Goodfellow：假设→方程→计算→优化→泛化。

- **局限/失效**：三者并非互斥；路由只是决定当前主循环。

### 模型4：Artifacts are evidence of learning｜产物才是学习证据

每站必须交：预测/假设、可复现配置、指标、错误分析和下一实验；理论站交推导与数值检查。

- **局限/失效**：产物可被照抄；需现场解释、变式和无辅助复现。

### 模型5：Exit tickets prevent endless reading｜退出票防止无限阅读

开始前定义可运行/可解释/可迁移的退出票，满足后再路由。

- **局限/失效**：退出票过窄会制造“过关但不理解”；加入失败案例与迁移题。

## 二、诊断量表（0–3）

| 维度 | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Python | 未能运行脚本 | 能改变量/循环 | 能写函数、读错误、处理数据 | 能组织小实验并测试 |
| 线代 | 不识向量/矩阵 | 会形状和点积 | 能解释线性变换/特征 | 能推导矩阵微分/分解用途 |
| 微积分 | 不识导数 | 会单变量导数 | 会链式法则/偏导 | 能推梯度和优化性质 |
| 概率统计 | 不识分布/期望 | 会均值方差 | 会条件概率、似然、抽样 | 能分析估计、区间与偏差 |
| 划分评估 | 在全数据调模型 | 知 train/test 名称 | 能先切分并解释指标 | 能设计嵌套选择/不确定性 |
| 神经网络 | 未知层/激活 | 能描述前向 | 能解释反传/损失 | 能诊断优化与泛化 |
| 算力 | 不明 | CPU、小内存 | 稳定 CPU/云 notebook | 可用 GPU 且能记录环境 |

算力不是智力。CPU 也可完成所有核心微型实验；GPU 只影响规模。

## 三、路由规则

1. **若划分评估 < 2 或概率统计 < 2** → `zhou-classical-ml-reasoning`。先建立问题、评估与泄漏纪律。
2. 否则若目标为 `theory` 且线代、微积分、概率统计均 ≥ 2 → `goodfellow-deep-learning-theory`。
3. 否则若目标为 `transformers` 且神经网络 < 2 → `d2l-lab-backbone`，先完成网络/注意力桥。
4. 否则若目标为 `classical` → `zhou-classical-ml-reasoning`。
5. 其他情况 → `d2l-lab-backbone`。

先修低于 2 时不会假装消失：它们成为**阻塞补丁**，先做 30–90 分钟最小任务，再进入所选模块。路由输出仍只有一个模块。

## 四、ROUTE-ONE 工作流

1. **Declare goal**：`classical` / `deep-practice` / `theory` / `transformers`，以及一个 2–6 周可观察结果。
2. **Score seven dimensions**：自评并附一个证据链接/文件；没有证据则标 provisional。
3. **Run red-flag gate**：若不会先切分、把 test 当调参集，立即标泄漏阻塞。
4. **Select exactly one module**：应用上方规则，不输出并行路线。
5. **Attach ≤3 prerequisite patches**：每项含任务、时间盒和通过标准。
6. **Create first runnable contract**：固定种子、环境、数据、基线、指标、产物路径。
7. **Define exit ticket**：解释、运行、错误分析、迁移四件套。
8. **Re-route from evidence**：只根据产物和退出票更新评分，不按读了多少页。

## 五、首站契约

### 周志华经典 ML

交：问题卡、split-before-fit 数据流、一个标准库微型基线、指标选择理由、至少三个错误桶。退出：能解释为什么某模型/指标适用，以及如何避免泄漏。

### D2L 实验站

交：可执行 notebook 合同、假设、配置/种子/环境、metric history、artifact path、错误分析、下一实验。退出：从空白重跑一个小实验并解释失败模式。

### Goodfellow 理论站

交：假设、符号、关键方程、手算或标准库数值检查、梯度/优化行为、泛化失败例。退出：能把一个方程落到计算图和实验预测。

## 六、当前 Transformer/LLM 桥

Transformer 是**后 2016 补充**，不是塞回原书。进入条件：Python/线代/概率/划分评估 ≥2，神经网络 ≥2 或先完成 D2L 注意力桥。实践路线转到 D2L + Hugging Face；理论路线先用 Goodfellow 的表示、优化、正则与序列基础，再读注意力/Transformer 原论文与当前文档。任何微调都必须有独立评估集、明确指标和错误分析。

## 七、CLI

```bash
python3 scripts/diagnose_path.py \
  --goal transformers --python 2 --algebra 2 --calculus 1 \
  --probability 2 --evaluation 2 --neural-networks 1 --compute cpu \
  --output next-module.md
```

输出：七维雷达表、一个模块、最多三项补丁、首个运行命令、artifact contract 和退出票。

## 八、表达DNA

- **句式**：先写证据/假设与边界，再写动作；**词汇**：优先使用本 Skill 的工作流术语；**语气**：校准而不绝对化；**引用**：关键声明保留来源层和日期。

- **句式**：先“下一站是 X，因为 Y”，再列补丁；不用宏大路线压人。
- **词汇**：证据、阻塞补丁、运行契约、退出票、重路由。
- **语气**：像实验教练，不像入学考官；分数可修订。
- **节奏**：诊断 → 一个动作 → 产物 → 退出 → 重路由。
- **确定性**：用规则说明理由，不假装个性测评精确。
- **引用**：课程结构归原教材/官方文档；ROUTE-ONE 归本 Skill。

## 九、内在张力

> 下列每项都是必须保留、不能用口号消解的工作流张力。

- **先修完整 vs 尽快动手**：先修不足会卡住，补太久又无项目反馈；采用最小阻塞补丁。
- **单一路由 vs 知识互联**：一次一个主循环提高执行，但反思日志可记录跨模块问题。
- **自评效率 vs 测量误差**：自评很快但偏差大；用产物更新。

## 十、诚实边界

- 0–3 分和路由阈值是本 Skill 的教学启发，不是经验证量表。
- 它不认证学历、岗位能力或课程等价性，也不保证完成时间。
- 三个来源的版本、代码和外部框架会更新；运行前核对官方环境。
- CPU 合同保证的是小规模学习，不保证复现大模型训练。
- Transformer 补充明确晚于三本核心来源，不能归给原作者的旧版内容。

## 十一、来源导航

- [`references/source-notes.md`](references/source-notes.md)
- [`references/claim-layer-map.md`](references/claim-layer-map.md)
- [`references/templates.md`](references/templates.md)
- [`references/research/`](references/research/)
- [`VALIDATION.md`](VALIDATION.md)
