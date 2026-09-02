# 来源总表

> 复核日期：2026-08-16。原书内容与 2016 后补充严格分栏。

| ID | 层 | 来源 | 支持 | 边界 |
|---|---|---|---|---|
| GDL-A01 | A | Goodfellow, Bengio, Courville (2016). *Deep Learning*. https://www.deeplearningbook.org/ | 官方在线书和 Ch.2–11 理论结构 | 不含后来 Transformer/LLM 生态 |
| GDL-A02 | A | 官方 Ch.7 Regularization slides. https://www.deeplearningbook.org/slides/07_regularization.pdf | 正则化主题一手教学材料 | 幻灯片不替代完整章/最新研究 |
| GDL-B01 | B/post-2016 | Vaswani et al. (2017). “Attention Is All You Need.” NeurIPS. https://papers.nips.cc/paper/7181-attention-is-all-you-need | Transformer 原始架构来源 | 不代表所有当前变体/规模结论 |
| GDL-B02 | B/current | Hugging Face Transformers, Training. https://huggingface.co/docs/transformers/en/training | 当前微调与评估实现入口 | API/建议会更新 |
| GDL-B03 | B | Baydin et al. (2018). “Automatic Differentiation in Machine Learning: a Survey.” *JMLR* 18. https://jmlr.org/papers/v18/17-468.html | AD 模式、计算图与数值/符号微分区分 | 不验证具体实现 |
| GDL-B04 | B | Pineau et al. (2021). “Improving Reproducibility in ML Research.” *JMLR* 22. | 环境、代码、数据和实验报告纪律 | 清单不保证复现 |
| GDL-C01 | C | Recht et al. (2019). “Do ImageNet Classifiers Generalize to ImageNet?” ICML. https://proceedings.mlr.press/v97/recht19a.html | 分布/采样变化下的泛化评估风险 | 不否定 ImageNet 或所有基准 |

THEORY-TRACE、推导合同、错误桶和标准库核对脚本属于 D 层综合。
