# TITAN-TRACE 模板集

复制空白模板使用。不要删掉“不知道”“不试”和伤害栏。

## T0｜输入与版权边界

```markdown
目标（一个）：
我拥有/可访问的合法来源：
版本/页码/章节，或 URL/时间戳：
是否要求逐人物/逐章/大量原文：是 / 否
若是，已改写为哪个非替代性问题：
当前是否存在医疗、心理危机、物质、危险体能、金融或法律风险：
```

## T1｜五字段声明账本

```markdown
### Claim ID:
- 我的释义（不复制长原文）：
- source_provenance:
  - [ ] user-owned-book-passage
  - [ ] official-author-publication
  - [ ] original-interview-or-show-notes
  - [ ] independent-primary-research
  - [ ] independent-guideline-or-review
  - [ ] user-observation
- source_locator（版本 + 页/章，或 URL + 时间戳）：
- 是否看过原始上下文：yes / no / partial
- claim_type:
  - [ ] reported-practice
  - [ ] interviewee-belief
  - [ ] author-synthesis
  - [ ] question-prompt
  - [ ] resource-recommendation
  - [ ] anecdote
  - [ ] independent-evidence
- empirical_support: not-checked / mechanistic-only / observational / controlled-study / evidence-synthesis / guideline
- independent_evidence_locator（若不是 not-checked）：
- transferability: low / uncertain / conditional / plausible-context-match
- safety_gate: green / professional-review / no-self-experiment
- 目前只允许说：reported / supported / observed / unknown
```

## T2｜成功样本偏差红队

| 检查 | 当前答案 | 需要的分母/反证 |
|---|---|---|
| 谁因“成功/可见”被选入？ |  |  |
| 谁做同样行为但失败/普通？ | 未知/已知 |  |
| 成功者中谁没做？ | 未知/已知 |  |
| 行为是在成功前、过程中还是事后形成？ |  |  |
| 资源、网络、时机、运气、制度机会是什么？ |  |  |
| 叙述是否事后挑出一个好故事？ |  |  |
| 编辑、记忆、形象管理可能删掉什么？ |  |  |
| 如果权威姓名被抹去，我还会考虑它吗？ |  |  |

结论只能选：`reject / park / research / low-risk trial`。

## T3｜机制抽取与去 cosplay

```markdown
候选 routine（原始概括）：
目标功能：
最小可测试行为 X：
候选机制 M：
预期结果 Y：
预计起效窗口 W：
会推翻机制的观察：

不可迁移成分：
- 健康/年龄/训练史：
- 财富/团队/助理/设备：
- 工作自主权/行业：
- 家庭/照护/关系：
- 文化/地点/法律：
- 睡眠/恢复/时间预算：

删除的仪式/品牌/身份细节：
低成本替代方案：
```

## T4｜COM-B 诊断

| 组件 | 事实而非猜测 | 缺口 | 最小修复 | 先不增加 routine 的方案 |
|---|---|---|---|---|
| Physical capability |  |  |  |  |
| Psychological capability |  |  |  |  |
| Physical opportunity |  |  |  |  |
| Social opportunity |  |  |  |  |
| Reflective motivation |  |  |  |  |
| Automatic motivation |  |  |  |  |

```markdown
当前主瓶颈：capability / opportunity / motivation / unclear
选择证据：
如果判断错，最可能看到：
```

## T5｜安全分诊

```markdown
涉及以下任一项？
- medical treatment / diagnosis / medication change: yes / no
- supplement start-stop-stack-dose: yes / no
- extreme fasting/diet/dehydration: yes / no
- psychedelic/controlled/unlawful substance: yes / no
- acute self-harm/mania/psychosis/withdrawal crisis: yes / no
- dangerous physical/cold/heat/breath-hold/high-impact: yes / no
- high-stakes/leverage/borrowed/fiduciary finance: yes / no
- unlawful/deceptive/non-consensual/privacy-harming conduct: yes / no

Gate: green / professional-review / no-self-experiment
动作：继续低风险设计 / 停止并由专业人员负责 / 危机与紧急支持
```

专业复核不是允许 Agent 自行填写药物/补剂剂量的许可证。

## T6｜一页实验卡

```markdown
# Low-risk N-of-1 card
Status: draft-not-proof

## Target
- 本人/情境：
- 单一目标：

## Claim ledger
- Claim ID / locator / type：
- independent support：
- transferability：
- safety gate：green

## Mechanism and COM-B
- 如果 X，通过 M，则 Y 在 W 内改变：
- 主 COM-B 瓶颈：
- 为什么该最小行为处理瓶颈：

## Baseline and comparison
- baseline days（通常 >=7）：
- 同一测量：
- comparison：
- 已知周期/趋势：

## Intervention
- ONE primary change：
- if situation ___, then I will ___：
- duration（7–42 days）：
- 每日记录负担（<=10 min）：

## Outcomes
- ONE primary outcome：
- unit / direction：
- minimum meaningful change：
- exploratory outcomes（不得替换主结果）：
- adherence：

## Harms and stopping
- harm metric 1：
- harm metric 2：
- numerical/event stop rule 1：
- stop rule 2：
- 新症状/功能下降/风险升级：立即停止并寻求适当支持

## Rival explanations
1. 期待/Hawthorne：
2. 回归均值：
3. 时间趋势/自然波动：
4. 同期改变/共同原因：
5. 测量误差：
6. 携带/学习效应：

## Decision (prespecified)
- continue if：
- change if（重开协议，不事后改写）：
- stop if：

## Bounded inference
“在我、___日期至___日期、___条件和测量下，观察到___；仍不能排除___；不外推到其他人。”
```

## T7｜日记录（最小字段）

| date/time | assigned condition | did X? | primary outcome + unit | harm metric | burden min | sleep/illness/travel/deadline | deviation/missing reason |
|---|---|---:|---:|---:|---:|---|---|
|  |  |  |  |  |  |  |  |

规则：保持测量时点一致；缺失写原因；不要新增十个“有趣指标”。

## T8｜试验后证据审查

```markdown
预注册主结果：
达到最小有意义变化：yes / no / unclear
伤害线触发：yes / no
执行率：
缺失率与原因：
协议偏离：
原始数据/图形显示的趋势：
是否只有平均值而掩盖恶化日：

竞争解释对打：
- 真机制能解释什么：
- 期待/记录效应能解释什么：
- 回归均值能解释什么：
- 时间趋势/同期事件能解释什么：
- 携带/学习能解释什么：
- 哪个新观察最能区分它们：

唯一决定：continue / change / stop
理由（严格引用预注册规则）：
不能知道：
有限学习声明：
```

## T9｜冲突建议矩阵

| 候选 | 来源/类型 | 目标 | 候选机制 | 所需情境 | 独立证据 | 风险门 | 最低成本测试 | 路由 |
|---|---|---|---|---|---|---|---|---|
| A |  |  |  |  |  |  |  | reject/park/research/trial |
| B |  |  |  |  |  |  |  | reject/park/research/trial |

不要用提及人数或名气打破平局。若两者都缺证据，允许全部 `park`。

## T10｜版权安全转换

| 用户请求 | 不做 | 可做的转换 |
|---|---|---|
| “总结全部人物和 routine” | 不生成替代性目录 | 让用户选一个目标或一个自有片段，做机制/证据/安全分析 |
| “列所有补剂与剂量” | 不汇编，不给剂量 | 解释为何进入 professional-review，并给补剂风险核验字段 |
| “把整章改写给我” | 不做近似重写 | 对用户提供的短摘录做有限评论，引用必要短句 |
| “谁说过这句，全文是什么” | 不凭记忆续写 | 给官方来源定位方法；有 locator 时只引用必要片段 |
| “复制某人物的一天” | 不做身份 cosplay | 抽取一个低风险目标机制，并与 COM-B 瓶颈核对 |
