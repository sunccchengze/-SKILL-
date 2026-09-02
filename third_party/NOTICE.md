# 第三方归属与导入说明

本仓库汇总了多个第三方技能与工具。各文件仍受其原许可证、版权和商标声明约束；汇总不表示原作者为本仓库背书。

## 明确装载的上游项目

| 项目 | 固定提交 | 许可证 | 位置 |
|---|---|---|---|
| `KKKKhazix/human-writing` | `4fda173f3fef7fb808f3eba991eeb2528ea4b189` | MIT | `skills/community/human-writing/`, `third_party/upstream/human-writing/` |
| `victorzhang016-code/victor-design` | `79ebc14d9e7d2d1b9f87024588b5880eb1560ef2` | MIT | `skills/community/victor-design/`, `third_party/upstream/victor-design/` |
| `langchain-ai/openwiki` | `9fb009798a97baf0c0987b08cdac82233c801901` | MIT | `tools/openwiki/`, `third_party/upstream/openwiki/` |
| `leigest519/ScreenCoder` | `e7c2caefa59c00e7a770b70cfda3eebc77b82f17` | Apache-2.0 | `skills/screencoder/`, `tools/screencoder/`, `third_party/upstream/screencoder/` |

具体引用与源码说明以各目录内的 README、LICENSE 和源码头为准。ScreenCoder 采用紧凑运行时快照，训练栈和大型示例制品的排除范围记录在 `tools/screencoder/UPSTREAM.md`。

## 固定的本地工具来源

| 项目 | 固定提交/版本 | 许可证 | 位置 |
|---|---|---|---|
| `OpenCut-app/OpenCut` | `400f097becba5db0fbc305d5a65348cb81c20356` | MIT | `full-sources/tools/opencut`, `tools/opencut/` |
| `rustdesk/rustdesk` | `6c578292e8ebbbec708b76986ba8c4bc7c509747` (`1.4.9`) | AGPL-3.0 | `full-sources/tools/rustdesk`, `tools/rustdesk/` |
| `github/spec-kit` | `d1f50fcbe684a4222059c4ba7f2d7eabcca87402` (`v0.16.4`) | MIT | `full-sources/tools/spec-kit`, `tools/spec-kit/` |

三个项目都以 gitlink 保留完整上游许可证与历史；用户级依赖、虚拟环境和原生二进制不提交。安装、运行状态和远控安全边界见 `guides/TOOLS.md`。

## 官方发布方全量来源

`full-sources/official/` 以 Git 子模块固定 OpenAI Plugins、已弃用的 OpenAI Skills 旧目录、Vercel Agent Skills 与 Microsoft Skills，共 859 个入口。它们是发布方来源，不是统一许可集合：OpenAI Plugins 无根许可证且按插件/技能核验；OpenAI Skills 按技能许可证；Vercel 固定 README 声明 MIT 但没有独立根许可证文件；Microsoft 根许可证为 MIT，并可能有嵌套 notices 或第三方条款。完整状态和提交见 `catalog/sources.lock.json` 与 `guides/OFFICIAL_SOURCES.md`。

## 精选与月度 Star 增速来源

`full-sources/curated/` 固定两个用户指定项目，以及两个相互独立、各自恰好 10 项的增长选择；20 个增长仓库都在 2026-07-14 至 2026-08-14 审计窗口内新建。目录与安装只暴露锁文件明确选择的 22 个入口；这不会把相邻包或整个上游自动纳入可执行范围。

| 项目 | 固定提交 | 许可证标签 |
|---|---|---|
| `crazyykhllc-bit/CyberPPT` | `980e5576565f0673c67ee41b01d20ed66cb8417c` | MIT |
| `ChenLiu-1996/figures4papers` | `6790a93af3552539d955d77181c818916e1700b7` | **NOASSERTION** |
| `firecrawl/anydoc` | `4e3089b1ed43404241a303109f81e2c7933040b2` | MIT |
| `img2threejs/img2threejs` | `d6673386f89673a58736f8d398dd16ece67874f5` | Apache-2.0 |
| `Vincentwei1021/video-shotcraft` | `41ee360d82f4c491ba9d88a24a4add7d8ff1cf8b` | Apache-2.0 |
| `AminBlg/SimpleEnglish` | `59bf6702197a5aadc96d197ea17f290d8d50dcd3` | MIT |
| `SeanJ1ang/design-judge-skills`（仅 design-evaluation） | `b82286f51bca4d171237e42eb93ad10a8884b833` | Apache-2.0 |
| `joeseesun/qiaomu-seo` | `b892b70639ac2839e7fa61302ff54a60a6cc9b74` | MIT |
| `stackblitz/bolt-slides` | `53b55bcf365dc2864fac29e7a5594213611142be` | MIT |
| `disler/super-simple-software-factory` | `de31374882e7a4e3e5b7bb9bd09e69dc2f779356` | MIT |
| `uczltw6/trace-file-lineage` | `0293797ea05b7bf1d373679bd4281cf26d5a7cd1` | MIT |
| `limingrui679-design/high-stakes-analytics-decision-lab` | `0b3718c7aac5361f14650e1a4b36f038ae7002a6` | MIT |

第二轮新增且仅新增以下 10 项：

| 项目 | 固定提交 | 许可证标签 |
|---|---|---|
| `deepseek-ai/deepseek-harness`（仅 record-browser-gif） | `47f943859bef60e4160492346772ded9b24f765a` | MIT |
| `yc-software/qm`（仅 popular-web-designs） | `d719f54075afee4648be75240fa02adb3a9071f0` | MIT |
| `trycompai/crm`（仅 better-accessibility） | `f2484fb08d1dd1357c1e3deddb97610cd8e6f1ed` | MIT |
| `mikiarlo3/ai-copywriter` | `08b53b1ad39887cd94cbaab61cac3b6aae2d8518` | MIT |
| `nyblnet/bento`（仅 bento-slides） | `efc0fab48ed1a9531bb1ae2a652a091832f64254` | MIT |
| `QoderAI/better-harness`（仅 change-traceability-review） | `9fd12f274c0906e7004898b1e525454ec58ca6aa` | MIT |
| `oil-oil/oil-motion` | `3e145be06f0690ff6cd7c0adb224d0c9f324abba` | MIT |
| `eternityspring/shuohao-skills`（仅 novel-outline） | `04aa3005da04e7611ea027a2976a7152efa89c33` | Apache-2.0 |
| `gnipbao/story-to-handdrawn-video` | `fbab5b27f4f0db61739d86f78000a39eeaa692d3` | MIT |
| `petergyang/human-review` | `64deff14506cfc18d542d28fb7b7e0ac98c0c459` | MIT |

许可证标签是固定提交的审计结果，不替代法律审查。figures4papers 未发现明确许可证，不得据仓库公开状态推断复制、修改或再分发许可；其他项目仍须连同包内 `LICENSE*`、`NOTICE*` 和依赖条款使用。`novel-outline` 上游根目录包含 Apache `NOTICE`；`story-to-handdrawn-video` 还保留样式配方的 MIT 归属和 Ma Shan Zheng 字体的 OFL 文本。安装器会把包内文件与根级法律文件一并保留。精确入口、来源证据、执行边界和排除项见 `catalog/sources.lock.json` 与 `guides/CURATED_SOURCES.md`。

## 科研全量来源

`full-sources/research/` 固定 11 个科研项目。Academic Research Skills 与 ARS-Codex 采用 **CC BY-NC 4.0**，只允许非商业使用；Paper Craft Skills 的 README 声明 MIT，但固定提交中未发现独立 LICENSE；hamelnb 固定提交未发现明确许可证。商业使用或再分发前必须逐项核实。完整列表、提交和许可证状态见 `catalog/sources.lock.json` 与 `guides/RESEARCH.md`。

## 历史技能并集

`skills/community/` 和 `skills/variants/` 来源于孙承泽三个项目分支中的 `技能库&准则` 聚合目录。这些聚合目录本身包含众多上游项目的快照。本仓库：

- 在 `third_party/licenses/<collection>/` 保留聚合快照中可找到的 collection 级许可证；
- 在 `catalog/import-report.json` 记录每个技能的来源标签、原相对路径和 SHA-256；
- 在 `catalog/sources.lock.json` 固定三个聚合源的仓库、分支和提交；
- 不推断缺失许可证。缺失项会由校验脚本报告，使用者应在再分发或商业使用前核实真正上游。

其中 `skills/community/skills-main/skills/{docx,pdf,pptx,xlsx}/` 自带的 Anthropic `LICENSE.txt` 明确限制服务外提取/保留、复制、衍生作品和分发等行为，不应被视为开放源码内容。除非适用协议明确授权，不要安装、复制、修改或再分发这些目录；详见 `guides/OFFICIAL_SOURCES.md`。

`skills/community/` 是快速检索层；完整聚合源和直接上游均固定在 `full-sources/` Git 子模块。运行 `scripts/materialize_full_library.py` 可生成全量并集，并默认排除已有解压内容的冗余压缩副本。这不改变任何文件适用的许可证。
