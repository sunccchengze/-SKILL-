# 塑成·装备聚焦改造专项 — 技能获取与调用指南

> 收件人：塑成  
> 发送人：技能库管理  
> 时间：2026-08-29  
> 优先级：**紧急**

---

## 一、技能库在哪

```
仓库地址：https://github.com/sunccchengze/-SKILL-/tree/arena%2F01a048e7-skill
当前分支：arena/01a048e7-skill（不是 main，main 是空的）
```

拉取方式：

```bash
# 方式 A：直接 clone 整个仓库
git clone -b arena/01a048e7-skill https://github.com/sunccchengze/-SKILL-.git

# 方式 B：如果已有仓库，切到正确分支
cd -SKILL-
git fetch origin
git checkout arena/01a048e7-skill
```

---

## 二、你要的 8 项技能在哪些路径

全部放在 `skills/core/` 下，直接能用：

| 你的需求 | 文件路径 | 打开就能看 |
|---|---|---|
| ② 工科术语守门 | `skills/core/engineering-terminology-gate/SKILL.md` | 术语四层分类 + 四问判定流程 + 5 个翻车案例验收集 |
| ③ 图文一致性审计 | `skills/core/page-image-text-audit/SKILL.md` | OCR 流程 + 四类标记（图文不符/AI痕迹/水印/重复） |
| ④ 精确取图工具 | `skills/core/slide-image-extractor/SKILL.md` | PPTX 全量提取 + PDF 区域裁剪 + JSON 清单（含 Python 脚本） |
| ⑤ 图表风格系统 | `skills/core/defense-presentation-toolkit/SKILL.md` 的 §⑤ | matplotlib 模板代码 + 设计令牌（深蓝/青/金）+ 中文字体粗体方案 |
| ⑥ 导出前质检 | `skills/core/defense-presentation-toolkit/SKILL.md` 的 §⑥ | 黑名单扫描器 + P19 手记测试用例 + PDF 双层比对思路 |
| ⑦ 答辩证据映射 | `skills/core/defense-presentation-toolkit/SKILL.md` 的 §⑦ | 三联表模板（规则维度→页面证据→30 秒话术） |
| ⑧ 叙事节奏审查 | `skills/core/defense-presentation-toolkit/SKILL.md` 的 §⑧ | 路由到已有的 `analyze-pitch-deck` 技能 |

### 辅助技能（你已有的，继续用）

| 技能 | 路径 | 用途 |
|---|---|---|
| 归藏 PPT | `full-sources/curated/cyberppt/SKILL.md` | 咨询风格 PPTX 生成 |
| Agent Reach | `skills/community/agent-reach/` | 情报检索 |
| Stop-slop | `skills/core/stop-slop/SKILL.md` | 去 AI 模板腔 |
| Humanizer-zh | `skills/core/humanizer-zh/SKILL.md` | 去中文 AI 痕迹 |
| Human-writing | `skills/community/human-writing/SKILL.md` | 通用中文创作 |
| Victor Design | `skills/community/victor-design/SKILL.md` | 视觉设计系统 |

---

## 三、怎么把技能挂进你的工作流

### 3.1 快速接入

把技能文件复制到你的项目目录：

```bash
cd 你的项目/04-技能库与准则/04-装备聚焦改造专项/

# 复制 4 个新建技能
cp /path/to/-SKILL-/skills/core/engineering-terminology-gate/SKILL.md ./
cp /path/to/-SKILL-/skills/core/page-image-text-audit/SKILL.md ./
cp /path/to/-SKILL-/skills/core/slide-image-extractor/SKILL.md ./
cp /path/to/-SKILL-/skills/core/defense-presentation-toolkit/SKILL.md ./
```

### 3.2 挂进路由表

在你的 `00-SKILL运用指南.md` 路由表中加入：

```markdown
## 装备聚焦改造专项技能路由

| 改造阶段 | 必调技能 | 调用时机 |
|---|---|---|
| 逐页诊断 | ③ page-image-text-audit | 每改完一页，渲染 PNG 跑一遍审计 |
| 术语替换 | ② engineering-terminology-gate | 每一句改造文案提交前过四问 |
| 取图定位 | ④ slide-image-extractor | 需要配图时先跑提取，拿精确坐标 |
| 图表生成 | ⑤ matplotlib 模板 | 需要新图表时直接用模板代码 |
| 导出前 | ⑥ 黑名单扫描 | 最终 PDF 导出前必跑 |
| 答辩准备 | ⑦ 三联表 + ⑧ 节奏审查 | 定稿后做一轮话术演练 |
```

---

## 四、关键提醒：一定要多调用、主动调用

### 4.1 不要"知道有但不用"

技能库最大的浪费是"知道有这个技能但嫌麻烦没调用"。你的翻车记录（构件熔点、P3 头骨图、P19 手记）全是**本可以被技能拦截的**。

**强制执行规则**：

```
每一句改造文案 → 必须过 ② 术语四问（30 秒，不能省）
每一页改完后 → 必须过 ③ 图文审计（渲染 PNG 对比）
每次导出 PDF → 必须过 ⑥ 黑名单扫描（5 秒自动检查）
```

### 4.2 不要只调一个技能

单个技能解决不了完整问题。正确用法是**技能组协作**：

```
改造 P5：
  ① 先用 ③ 图文审计 看当前页有什么问题
  ② 改文案时用 ② 术语守门 判定每句话
  ③ 配图时用 ④ 精确取图 定位毕业答辩 PPT 里的素材
  ④ 改完后再跑一遍 ③ 确认图文一致
  ⑤ 全部改完后跑 ⑥ 黑名单扫描
```

### 4.3 《毕业答辩》的参照权重必须提高

**这是你的核心素材池**，但目前你的引用粒度太粗（"毕业答辩 P14 那张设备照片"）。

**提高权重的具体做法**：

1. **先把素材池结构化**：用 ④ 精确取图工具把《毕业答辩》49 页里的所有图片全部提取出来，得到 `image_manifest.json`，这样你就有了一份完整的素材索引。

2. **建立页面映射表**：

```markdown
## 08277.pdf ↔ 毕业答辩.pptx 页面映射

| 08277 页码 | 需要什么素材 | 毕业答辩 来源页 | 来源图片文件名 | 已提取？ |
|---|---|---|---|---|
| P3 | 设备实物照 | P14 设备照片 | P14_01_L2.5T3.0W...jpg | ☐ |
| P5 | 温控系统截图 | P38 系统界面 | P38_02_L...jpg | ☐ |
| P15 | 构件实物照 | P42 构件特写 | P42_01_L...jpg | ☐ |
```

3. **每次配图建议必须精确到文件名**，不许出现"P14 那张"这种描述——用 `image_manifest.json` 里的精确文件名。

4. **在 SKILL 运用指南中把《毕业答辩》列为一级来源**，和"仓库素材库"并列，而不是"参考看看"。

---

## 五、执行优先级

```
P0（今天就做）：
  □ 拉取仓库，复制 4 个技能文件
  □ 运行 ④ 精确取图，提取《毕业答辩》全量图片，建立索引
  □ 建立 08277 ↔ 毕业答辩 页面映射表

P0（每页改造时执行）：
  □ 改文案前：过 ② 术语四问
  □ 改文案后：跑 ③ 图文审计
  □ 配图时：用 ④ 精确文件名

P1（全部改完后执行）：
  □ 跑 ⑥ 黑名单扫描
  □ 跑 ⑧ 叙事节奏审查
  □ 建 ⑦ 答辩话术三联表
```

---

## 六、遇到问题的反馈路径

- 技能使用问题：直接在技能文件里找 `注意事项` 章节
- 术语判定争议：按 ② 的四步流程走，有争议的记录下来等负责人拍板
- 取图坐标不对：检查 PDF 版本是否一致，DPI 设置是否为 300
- 技能不够用：记录缺口，反馈到技能库补充

---

**最后一句：技能摆在那里不叫有，用了才叫有。每改一页就调一轮，别攒着。**
