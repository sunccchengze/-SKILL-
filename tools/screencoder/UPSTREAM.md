# ScreenCoder 上游快照说明

本目录是 `leigest519/ScreenCoder` 的紧凑运行时快照。

- 仓库：<https://github.com/leigest519/ScreenCoder>
- 分支：`main`
- 提交：`e7c2caefa59c00e7a770b70cfda3eebc77b82f17`
- 许可证：Apache-2.0
- 上游固定信息：`catalog/sources.lock.json`

## 保留内容

- ScreenCoder 推理主链：区域规划、HTML 生成、占位检测、映射和图片替换；
- `main.py` 与模型适配工具；
- UIED 的 Python 源码、配置、README 和许可证；
- 上游 README、requirements 和根许可证。

## 未复制内容

上游仓库共约 88 MB，包含多个完整训练项目和大量生成制品。为遵守本技能仓库的紧凑语义并集策略，以下内容未复制：

- `post-training/` 中完整的 LLaMA-Factory、VLM-R1 和 vLLM 训练栈；
- 示例截图、检测输出、裁剪图和调试 overlay；
- `tmp.zip` 与 `tmp/` 运行产物；
- UIED 示例数据、输出、模型文件、IDE 配置、日志和 notebook；
- Python 缓存。

这些内容已由 `full-sources/screencoder/` Git 子模块全量固定；执行 `git submodule update --init --recursive` 后即可取得。本目录只面向快速截图转 HTML/CSS 推理，不作为训练仓库镜像。

## 运行注意

上游脚本使用若干硬编码的 `data/input/test1.png`、`data/tmp/`、`data/output/` 和 `*_api.txt` 路径。运行前应在隔离工作副本中统一配置路径，绝不能把 API key 提交到 Git。
