# 《易经》变化决策 Skill

这是一个 Nuwa deep-tier 的中性书籍/经典蒸馏包。它不扮演古人、算命师或某一门派传人，而是把《周易》与其解释史转化为**可追溯、可反驳、可复盘**的不确定性决策流程。

## 核心特点

- 区分《周易》古经、《十翼》与后世解释，不把复合文本写成一个人的整齐理论；
- 以变化、时—位—应、刚柔互补、知几、安不忘危、穷变通久为六个模型；
- 把卦象限制为假设生成和反思提示，不声称经科学验证的预测力；
- 每次输出分开事实层、经典层、历史解释、现代操作化与行动层；
- 提供可运行的 CHANGE 工作表生成器、固定模板、失败模式和验证记录。

## 快速使用

在 Agent 中显式调用：

```text
请使用 book-yijing-change-decision，按 CHANGE 七步法分析：
我在考虑未来三个月是否转项目。不要起卦；请分开事实与经典类比，给两个竞争情景、一个72小时可逆动作和复盘条件。
```

分析用户给出的卦爻：

```text
请使用 book-yijing-change-decision 分层解释“乾九三”。
依次标明：古经、十翼、后世解释、Skill现代转译、不能推出的事实；不要做命定预测。
```

生成工作表：

```bash
python3 scripts/frame_change.py --question "是否转项目？" --horizon "三个月" \
  --fact "当前项目两周后评审" --assumption "新项目成长更快" \
  --unknown "名额是否正式" --stakeholder "导师"
```

## 推荐阅读顺序

1. [`SKILL.md`](SKILL.md)：执行协议与输出格式；
2. [`references/claim-layer-map.md`](references/claim-layer-map.md)：声明属于哪一文本/解释层；
3. [`references/source-notes.md`](references/source-notes.md)：来源、证据范围与局限；
4. `references/research/`：六篇深挖笔记；
5. [`VALIDATION.md`](VALIDATION.md)：试运行与质量矩阵。

## 可选跨书桥

只有当情境变化需要转成短周期习惯实验时，才显式使用 [`../book-change-habit-bridge.md`](../book-change-habit-bridge.md)。它是 D 层现代综合，不建立《易经》与现代习惯科学的历史/科学等价；本 Skill 仍可且默认独立调用。

## 边界

本 Skill 可以帮助构造问题、发现遗漏条件和设计下一次验证。它不能证明超自然预测能力，也不能代替医生、律师、持牌财务顾问、安全人员或当事人的知情判断。对传统占筮实践保持尊重，不等于把其预测效力陈述为科学事实。
