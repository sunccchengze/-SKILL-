# AI科研学长姐联合体

一个默认中文、可追溯到创作者和具体来源的硕博科研顾问 Skill。

它把12位中文与国际创作者放进同一对话入口，但**不把他们伪装成一个人**。每条建议保留成员归属、原子声明 ID、来源链接、证据模态、抽取覆盖、置信度、商业背景和分歧。

## 第一批成员（固定12位）

1. 爱读书的Zoey / Zoey-SKILL
2. 爱研究的杨师兄
3. 读论文的麦小哲
4. 一只思敏在浙大
5. 何静
6. 李沐
7. Andy Stapleton
8. Amina Yonis
9. Tara Brabazon
10. James Hayton
11. Qualitative Researcher Dr Kriukow
12. Academic English Now

覆盖 AI 工作流、文献、写作、研究设计、质性方法、发表、导师关系、效率、身心边界和职业选择。调查截止日：**2026-08-16**。

## 快速使用

```bash
cd skills/community/nuwa-distilled/ai-research-senpai-council
python3 scripts/retrieve_council.py --query "怎么用AI做文献综述并核验引用？" --top-k 8
python3 scripts/retrieve_council.py --query "博士期间应该先完成论文还是多发文章？" --json
```

检索结果分三档：

- `grounded`：至少有完整逐字稿或创作者详细提纲支持的直接证据；
- `weak_only`：只有标题、简介、二手摘要或介导导出，不得补写步骤；
- `abstain`：没有足够匹配证据，后续只能单列“通用科研建议”。

完整对话协议见 [`SKILL.md`](SKILL.md)。

## 为什么不是“AI科研万能导师”

- 创作者之间可能强调不同优先级；本项目保留张力，不制造共识。
- 有些公开页只有标题或简介，知道主题不等于知道方法。
- 工具测评可能带联盟链接、课程或自有产品。
- 播放量、客户案例、个人速度和“保证发表”不是独立效果证据。
- 检测规避、代写、造假、未授权敏感数据处理和保证录用永不进入合法建议。
- Zoey 继续保留其点点介导、身份未独立归档和不完整覆盖状态。

## 数据结构

```text
ai-research-senpai-council/
├── SKILL.md
├── README.md
├── VALIDATION.md
├── references/
│   ├── knowledge/
│   │   ├── creators.json           # 12位成员注册表
│   │   ├── claims.jsonl            # 原子声明，只保存 source_id 引用
│   │   └── SCHEMA.md
│   ├── sources/
│   │   ├── sources.jsonl           # 规范来源与商业/覆盖元数据
│   │   ├── false-positives.json    # 错误归因与不可作证据的内容
│   │   └── COVERAGE_REPORT.md
│   ├── governance/
│   │   ├── routing.json
│   │   ├── disagreements.jsonl
│   │   ├── commercial-conflicts.jsonl
│   │   └── integrity-rules.json
│   ├── schemas/                    # Draft 2020-12 机器可读结构契约与映射
│   │   ├── manifest.json
│   │   └── *.schema.json
│   └── research/                   # 女娲深度档六维调研记录
├── scripts/
│   ├── retrieve_council.py
│   └── validate_corpus.py
└── tests/
```

`sources.jsonl` 是来源元数据的唯一规范账本。声明不复制 URL、标题、平台或发布日期，避免两份来源信息漂移。字段语义见 [`references/knowledge/SCHEMA.md`](references/knowledge/SCHEMA.md)，机器映射见 [`references/schemas/manifest.json`](references/schemas/manifest.json)。

## 校验

```bash
python3 scripts/validate_corpus.py --require-content
python3 -m unittest discover -s tests -v
```

完整的基线、行为冒烟测试和更新流程见 [`VALIDATION.md`](VALIDATION.md)。

校验器会拒绝：

- 固定12人之外的成员或缺失成员；
- 声明引用不存在、错误创作者或已排除来源；
- 已确认错误归因的内容 ID 重新进入来源账本；
- 声明复制规范来源 URL/标题等元数据；
- 二手摘要冒充高置信直接证据；
- 元数据级声明没有覆盖警告；
- 隔离声明没有警告，或诚信规则引用未隔离声明；
- 路由、商业披露和分歧账本引用未知成员、来源或声明。

## 维护原则

新增材料时优先原创频道和具体视频。先写 `sources.jsonl`，再把可独立检索的命题写入 `claims.jsonl`。逐字稿、简介、元数据、二手摘要和机构页必须分开标注。无法访问的内容进入缺口或排除账本，不从标题猜正文。

仓库只保存必要的结构化转述和来源定位，不批量转载完整视频、字幕或受版权保护的大段文本。
