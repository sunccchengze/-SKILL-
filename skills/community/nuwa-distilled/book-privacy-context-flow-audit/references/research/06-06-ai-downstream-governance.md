# Research track 06｜推断、LLM、下游链与发布门

- **研究问题**：推断、LLM、下游链与发布门
- **来源层**：见 `../source-notes.md`；本文件不创建新的 A 层归因。
- **方法**：版本核对 + 机制拆分 + 支持/反证并列 + 工作流落地。

## 主要发现

1. derived/inferred attributes 和 downstream recipients 会改变 flow。
2. LLM benchmark 显示 contextual privacy/secret keeping 不可靠。
3. security/consent 都不能单独证明 appropriateness。
4. NIST 提供 inventory/lineage/inference/control 衔接但非法律证明。

## 归因与反证

- 原书主张、作者后续、独立证据和本包设计保持 A/B/C/D 分层。
- 发现支持机制候选，不把案例、报告完整度或专家一致当普遍因果证明。
- 与其他研究冲突时保留来源身份、方法和未决状态，不取无依据的中间值。

## 本轮造成的具体改变

- **workflow decision**：高风险强制真实影响、owner/rule/contest/stop/rollback。
- **failure gate**：LLM 不可作真实披露裁决者；FLOW 不作 legal approval。
- 这项改变已经进入 `SKILL.md`、CLI schema、模板或验证契约；不是扩写背景散文。

## 仍未验证

- agent memory/tool runtime flow 的实地验证。
- 本包的 D 层工作流尚无外部效度、可靠性或结果改善证明。
- 用户输入、领域法律和现实系统行为默认未核验。
