# Knowledge schema

`claims.jsonl` 每行一个 JSON 对象，每条只表达一个可独立检索和调用的知识点。

必填字段：

```json
{
  "claim_id": "ZC-0001",
  "statement": "忠实转述的一条原子知识",
  "evidence_level": "direct",
  "confidence": "medium",
  "source_ids": ["ZS-0001"],
  "topics": ["文献阅读"],
  "keywords": ["论文矩阵"],
  "audiences": ["硕士", "博士"],
  "conditions": ["适用条件"],
  "actions": ["可执行步骤"],
  "warnings": ["风险或失效条件"],
  "tools": ["明确提到的工具"],
  "published_at": "YYYY-MM-DD或unknown",
  "verified_at": "YYYY-MM-DD",
  "verification_status": "provisional_diandian_mediated",
  "notes": "矛盾、更新、模态位置或证据限制"
}
```

## 证据层

- `direct`：来源明确表达了该单一命题；不表示已有逐字稿。当前点点摘要可标 `direct`，但必须同时标 `provisional_diandian_mediated`。
- `synthesis`：至少两条直接来源共同支持的稳定归纳；回答时必须称“归纳”。
- `inference`：由已有材料推演，不能写成“Zoey明确说过”。

## 置信度

- `high`：规范来源可回访，关键模态和原始位置已复核，且没有未解决的重大矛盾；
- `medium`：一手内容可识别但存在点点介导、原始件缺失或非关键模态缺口；
- `low`：只有压缩摘要、上下文不足或经验性主张缺少限定。

当前导入没有任何 `high` 命题。

## 来源资格

- `direct` 至少关联一个 `first_party_complete` 或 `first_party_partial` 来源；
- 来源必须是 `corpus_membership=included_provisional` 且 `evidence_eligible=true`；
- `first_party_metadata`、`secondary`、`excluded` 和隔离记录不能支持直接命题；
- `synthesis` 至少关联两个合格来源；
- 每个 `source_id` 必须同时存在于 `content-index.jsonl` 与 `coverage.csv`。

## 内容边界

- 通用学术知识不进入本文件，避免污染人物知识库；
- 点点或整理者的高层分析只有能回链时才作为 `synthesis`，否则留在研究备忘；
- 原文短引文如确有必要，另加 `short_quote` 与 `quote_locator`，保持最小引用；
- 就业统计、工具功能、价格、产品星数、政策和平台能力等时效事实必须另行核验；
- 导师冲突、健康与就业建议必须保留情境和风险，不能把激烈表达直接变成行为命令；
- 任何“去 AI 味”工具不得用于掩盖代写、抄袭或规避学校/期刊披露规则。
