# 03 - 社区表达与开源实现

> GitHub/X/社区中如何表达和实践客观决策方法论？有哪些可复用的工具？

## 可信度标注
- 🔴 一手（原始代码/文档）
- 🟡 二手（分析/转述）

---

## 1. 0xcjl/anti-sycophancy (GitHub)

### 🔴 三层防御架构
- **表达方式**：代码化——用 CLAUDE.md + Hook + Skill 三件套实现
- **核心句式**：「质疑用户前提」「不要附和」「先指出假设再回答」
- **社区影响**：被多个 AI prompting 工具引用
- **来源**：https://github.com/0xcjl/anti-sycophancy
- **可信度**：🔴 一手

---

## 2. MADEVAL/Pre-Mortem-Skill (GitHub)

### 🔴 结构化失败分析 SKILL
- **表达方式**：SKILL.md 格式——context gathering → parallel sub-agent deep-dives → structured output
- **输出结构**：failure story / underlying assumption / early warning signs / cheapest mitigation
- **关键创新**：将 pre-mortem 分解为可并行的子任务
- **来源**：https://github.com/MADEVAL/Pre-Mortem-Skill
- **可信度**：🔴 一手

---

## 3. carlkibler/agent-skills pre-mortem (GitHub)

### 🔴 多 Agent 预验尸
- **表达方式**：多角色并行——不同角色从不同维度找失败模式
- **角色设计**：UX / ops / security / support / growth
- **关键创新**：cross-pollination round（交叉授粉）
- **输出**：两份文档——failure report + process log
- **来源**：https://github.com/carlkibler/agent-skills
- **可信度**：🔴 一手

---

## 4. SYCON Benchmark 社区

### 🟡 EMNLP 2025 后续讨论
- **表达模式**：学术社区用 benchmark 量化不同干预的效果
- **社区共识**：盲区提问 > 第三人称 > 显式指令（按效果排序）
- **可信度**：🟡

---

## 5. Prompt 工程社区的反讨好实践

### 🟡 X/Twitter、Reddit 上的讨论
- **高频表达**：
  - "Don't just agree with me"
  - "Tell me what I'm wrong about"
  - "What would make this fail?"
  - "Act as if you're my toughest critic"
- **社区发现**：角色分配（"你是批评者"）效果差于问题设计（"我最可能忽视什么"）
- **可信度**：🟡
