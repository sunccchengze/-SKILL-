# 06 - 方法论演化时间线

> 客观决策方法论从何而来，如何演化到今天？

## 可信度标注
- 🔴 一手
- 🟡 二手

---

## 时间线

| 时间 | 事件 | 对方法论的影响 |
|------|------|--------------|
| 1979 | Kahneman & Tversky 发表 RCF 论文 | 奠定外部视角的理论基础 |
| 1980s | Gary Klein 发展 RPD（Recognition-Primed Decision）| 从另一角度理解专家决策 |
| 1990s | Grossmann 提出 Solomon's Paradox | 心理距离与决策质量的关系 |
| 2007 | Gary Klein 发表 HBR "Performing a Project Premortem" | 将 pre-mortem 推向主流管理实践 |
| 2011 | Kahneman 出版《思考，快与慢》 | 系统 1/系统 2 理论普及 |
| 2015-2020 | AI prompting 社区兴起 | 用户开始尝试让 AI 批判性思考 |
| 2024 | Anthropic ICLR 论文量化 AI sycophancy | 首次用实验数据证明 AI 讨好程度 |
| 2025 | SYCON EMNLP 基准测试 | 量化不同干预的效果（第三人称 63.8%） |
| 2025 | 0xcjl/anti-sycophancy 发布 | 三层防御架构的工程实现 |
| 2025 | MADEVAL/Pre-Mortem-Skill 发布 | 结构化 pre-mortem 的 SKILL 实现 |
| 2025 | carlkibler 多 Agent pre-mortem | 多角色并行失败分析 |
| 2026 | CHI "Invisible Saboteurs" | 揭示表面同意实则破坏的模式 |
| 2026 | 用户演讲：三大机制框架 | 提问设计 > 角色分配的独特洞察 |
| 2026 | 本 SKILL 创建 | 融合上述所有方法论 |

## 演化趋势

```
学术理论 (1979-2011)
    ↓
管理实践 (2007-2020)
    ↓
AI 时代应用 (2024-2025)
    ↓
  ┌─────────────────────────────────────────┐
  │  融合：用户原创框架 + 学术验证 + 工程实现  │
  └─────────────────────────────────────────┘
```

## 核心流派演化

1. **Kahneman 传统**：认知偏差 → 外部视角 → RCF
2. **Klein 传统**：专家直觉 → 结构化质疑 → pre-mortem
3. **Grossmann 传统**：心理距离 → 第三人称效应 → 自我抽离
4. **Prompt 工程传统**：角色扮演 → 显式指令 → **提问设计**（用户创新）
5. **工程实现传统**：单 Agent → 多 Agent → 三层防御架构
