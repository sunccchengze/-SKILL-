# Validation

> **兼容性说明：** 文中 `skills/community/nuwa-skill` / `huashu-nuwa` 检查仅是来源分支遗留的本地启发式，**非 canonical、非 governing acceptance gate**；当前验收以 canonical `xmg2024/nvwa-skill` 方法、来源解析、包行为测试、安全门及仓库验证为准。

## 内容与边界

- [x] 可独立调用的精确 frontmatter 名称与中文默认说明
- [x] 七个核心心智模型逐项包含局限/失效条件
- [x] TITAN-TRACE 十步法明确标为 Skill 综合，而非原书方法
- [x] A/B/C/D 来源层与五个正交字段
- [x] 六轮研究、来源总表、26 条原子声明图
- [x] 幸存者偏差、选择成功、事后故事、权威、情境错配、多重比较红队
- [x] COM-B 先于 routine；if–then 只用于已选低风险行为
- [x] 基线、比较、单一主结果、伤害、停止线、竞争解释与 continue/change/stop
- [x] 医疗/药物/补剂/极端禁食饮食进入专业门且 CLI 拒绝设计
- [x] 致幻剂/受控物质、急性心理危机、危险体能、高风险金融、违法行为硬停
- [x] 逐章/逐人物/引语/补剂清单/索引替代的版权拒答和安全转换
- [x] 不将个人试验外推为群体因果或高成就原因

## 自动验证

在本包目录运行：

```bash
python3 -m unittest discover -s tests -v
python3 ../../nuwa-skill/scripts/quality_check.py SKILL.md
```

仓库根目录运行：

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_repository.py
```

## CLI 正例

运行 [`SKILL.md`](SKILL.md) 第九节示例，预期：

- 退出码 0；
- 输出合法 JSON；
- `schema_version == "titan-trace/1.0"`；
- `safety_gate == "green"`；
- `not_proof_of_causality` 与 `no_population_generalization` 均为 true。

## CLI 反例

把正例中的 domain 改为：

```bash
--domain supplement-change
```

预期：退出码非 0，stderr 含 `professional-review`，且不生成 JSON。九个受限 domain 和文本伪装都由测试覆盖。

## Catalog 验收

重建后检查：

```bash
python3 scripts/build_catalog.py
python3 scripts/build_categories.py
python3 scripts/search_skills.py "TITAN-TRACE survivorship COM-B" --limit 5
```

预期 `book-tools-of-titans-experiment-lab` 精确进入 reviewed `general` 分类。
