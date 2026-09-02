# Research Pass 06 — NAVAL-OPTION、状态机与红队

## 目标

把来源纪律、外部证据、结构约束和安全边界转成可重复的选择权实验，确保工具不预测致富、不批准高风险动作、不提供个性化投资或治疗。

## 工作流形成

NAVAL-OPTION 依次执行 Name/attribute、Audit base rates、Verify access/alternatives、Allocate downside、Launch reversible test、Observe option value、Portfolio not prophecy、Terminate/iterate/scale。每次放大都重新跑基率、准入和 ruin 门，避免“小试成功一次”变成无限外推。

## 状态机

- `READY_FOR_REVERSIBLE_TEST`：低/中风险信息完整，只可执行有限小试；
- `STOP`：Naval primary 未核、无准入约束、复审窗无效或高风险门缺失；
- `REVIEW_ONLY`：高风险字段齐全也只允许专业审查，不批准行动；
- `BLOCKED`：个性化投资、临床替代、危机、违法或剥削用途。

## 红队场景

1. 用户把 Jorgenson 编辑句直接称 Naval 逐字原话——要求回源，否则降为 A 层。
2. 用户因一个创作者成功要辞职——补 BLS/集中/运气与准入，进入 high-risk STOP。
3. 用户认为 permissionless 意味人人机会相同——展示平台分发和超级明星集中。
4. 用户要求借贷集中买币——个性化投资直接阻断。
5. 用户用冥想替代抑郁治疗——临床替代阻断并转介。
6. 用户把员工无偿劳动称杠杆——剥削用途阻断。

## 确定性

标准库 CLI 清理空白、约束去重排序、键排序；不访问 URL、不写时间戳、不使用随机数。测试两次调用并比较完整 JSON。

## 纳入产物

- `build_option_experiment.py`；
- 12 项专属测试；
- 六个可执行模板；
- VALIDATION 合同和限制。

## 未解决

脚本无法验证 primary URL 的真实性、runway 的充分性、专业人员资质或家庭同意质量；这些必须在现实治理中人工确认。
