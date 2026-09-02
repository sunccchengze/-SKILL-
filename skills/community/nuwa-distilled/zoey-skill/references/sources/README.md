# Sources

这里保存公开来源的**定位、归属与覆盖元数据**，而不是批量再发布博主的完整内容。

- `ACCOUNT_IDENTITY.md`：目标账号消歧、点点介导核验状态与身份边界；
- `COVERAGE_REPORT.md`：截至 2026-08-16 的可复算覆盖、缺口与下一检查点；
- `coverage.csv`：每条清单记录及不同模态的覆盖状态；
- `content-index.jsonl`：机器可读来源、归属、证据资格、导出定位符和完整性标记；
- `../acquisition/DIANDIAN_INTAKE_2026-08-16.md`：用户提供点点结果的导入与矛盾审计；
- 仓库外原始材料：用户合法提供但不适合公开分发的截图、原图、视频、字幕等。

## 来源等级

1. `first_party_complete`：本人公开内容，相关正文/图片/音视频已完整检查并有可复核材料；
2. `first_party_partial`：报告为本人公开内容，但至少一种关键模态不可见、未保留或未经独立复核；
3. `first_party_metadata`：只确认标题、导出定位符或日期，不能支持实质观点；
4. `secondary`：他人内容或转述，只可导航、排除或交叉验证；
5. `inference`：研究者推断，不得冒充本人观点。

当前没有 `first_party_complete` 记录。点点介导、没有原始件的内容最高只能标 `first_party_partial`。

## 归属与证据资格

`content-index.jsonl` 使用两个独立字段：

- `corpus_membership`：`included_provisional` 或 `excluded`；
- `evidence_eligible`：该来源当前能否支持 `claims.jsonl` 中的知识点。

只有 `included_provisional + evidence_eligible=true + first_party_partial/complete` 的来源能支持直接命题。`excluded`、仅元数据、标题日期错位或处于隔离区的来源不得支持 Zoey 观点。

`N240` 等是点点导出定位符；在补到规范 note ID 前，不称为小红书官方笔记 ID。导出给出的 `/explore/N240` 等 URL 保留用于审计，但字段明确标记 `unverified_export_url`，回答中不得冒充已验证原帖链接。

## 当前状态

截至 2026-08-16：

- 60 行导出清单；
- 3 行后续判为非目标作者并排除；
- 57 行暂定目标；
- 26 行可支持暂定知识，其中 10 行只有压缩命题；
- 31 行不能支持知识（4 隔离 + 27 仅元数据）；
- 0 行拥有仓库可复核原始材料或规范 note ID。

详见 `COVERAGE_REPORT.md`，不得使用导出中不可复算的“87.7%”覆盖率。

## 原始材料规则

- 不提交批量原图、完整视频或大段受版权保护原文；
- 不保存登录凭据、Cookie、私人联系方式或非公开数据；
- 用户授权材料若含敏感信息，先脱敏并保存在仓库外；
- 每个知识点至少回链一个 `ZS-*` 来源编号；
- 工具功能、统计数字、就业与政策类断言需要当前事实交叉核验；
- 若后续收到截图、逐字稿或原文件，记录采集时间、哈希和模态位置，不静默覆盖本次审计。
