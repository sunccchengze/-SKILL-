# 来源总表

> 复核日期：2026-08-16。

| ID | 层 | 来源 | 支持 | 边界 |
|---|---|---|---|---|
| D2L-A01 | A | Zhang, Lipton, Li, Smola. *Dive into Deep Learning*, official preface. https://d2l.ai/chapter_preface/index.html | 文字、数学、代码、可执行 notebook 一体 | 不证明每个运行结果可泛化 |
| D2L-A02 | A | 官方源码/notebooks：https://github.com/d2l-ai/d2l-en | 可下载、版本化的 notebook 骨架 | 依赖/API/分支会更新 |
| D2L-B01 | B | scikit-learn, Common pitfalls. https://scikit-learn.org/stable/common_pitfalls.html | 不一致预处理、数据泄漏、随机性规则 | sklearn API 示例不等于所有框架实现 |
| D2L-B02 | B | scikit-learn, Pipelines. https://scikit-learn.org/stable/modules/compose.html | 训练流程中封装状态变换，降低泄漏 | pipeline 也可能被错误切分/使用 |
| D2L-B03 | B | Hugging Face Transformers, Training. https://huggingface.co/docs/transformers/en/training | 当前 fine-tuning 与评估数据/指标 | 文档、API 和推荐会变 |
| D2L-B04 | B | Pineau et al. (2021). “Improving Reproducibility in Machine Learning Research.” *JMLR* 22. http://jmlr.org/papers/v22/20-303.html | 代码、数据、实验细节和结果报告纪律 | 清单不保证完全复现 |
| D2L-C01 | C | Sculley et al. (2015). “Hidden Technical Debt in Machine Learning Systems.” NeurIPS. | 数据依赖、反馈、管线和部署债务 | 非 D2L 教学评估研究 |

LAB-TRACE、YAML 合同、标准库微型实验和退出票属于 D 层 Skill 综合。
