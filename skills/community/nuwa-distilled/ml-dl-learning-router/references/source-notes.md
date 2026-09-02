# 来源总表

> 复核日期：2026-08-16。路由阈值与 ROUTE-ONE 是 D 层教学综合，不是教材官方分级。

| ID | 层 | 来源 | 用途 | 边界 |
|---|---|---|---|---|
| RTR-A01 | A | Zhang et al. *Dive into Deep Learning*. https://d2l.ai/chapter_preface/index.html；源码 https://github.com/d2l-ai/d2l-en | 文字、数学、代码、可执行 notebook 一体的实验骨架 | 框架/API 会变；不等于所有实验可在 CPU 原规模运行 |
| RTR-A02 | A | 周志华（2016）《机器学习》，清华大学出版社官方书目 | 经典 ML 的问题—评估—监督/无监督序列 | 受版权保护；本 Skill 不重现教材 |
| RTR-A03 | A | Goodfellow, Bengio, Courville (2016). *Deep Learning*. https://www.deeplearningbook.org/ | ML 基础、前馈、正则、优化、CNN、序列与实践方法 | 2016 书不覆盖后来 Transformer 生态 |
| RTR-B01 | B | scikit-learn, “Common pitfalls and recommended practices.” https://scikit-learn.org/stable/common_pitfalls.html | split first、训练折内拟合预处理、pipeline 防泄漏 | 示例围绕 sklearn；原则可迁移，API 细节不能硬套 |
| RTR-B02 | B | Hugging Face, “Fine-tuning.” https://huggingface.co/docs/transformers/en/training | 当前微调需训练、评估数据和指标的实践入口 | 文档会更新；不保证特定模型/数据适用 |
| RTR-B03 | B | Datawhale, Pumpkin Book. https://github.com/datawhalechina/pumpkin-book | 周志华教材部分公式的开源推导辅助 | 仅伴读，不替代原书或独立权威 |

## 主张边界

- 七维评分、阈值、最多三个补丁和“一次一个模块”均为 Skill 设计。
- 泄漏不变量来自独立官方方法文档，不归三本教材独占。
- Transformer/LLM 内容标为 post-2016 supplement。
