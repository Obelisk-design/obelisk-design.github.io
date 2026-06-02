---
title: "Matt Pocock 的 Agent Skills 系统：用工程纪律驯服 AI 编程助手"
description: "从沟通对齐到测试驱动，一套可组合的 AI Agent 技能系统如何解决 AI 编程的真实失败模式。"
pubDate: 2026-06-02
tags: ["AI Agent", "软件工程", "开发工具", "TDD", "DDD"]
image: "/blog-placeholder-1.jpg"
featured: true
---

## 写在前面

Matt Pocock（Total TypeScript 创始人）公开了一套他日常使用的 AI Agent Skills——不是"让 AI 写代码更快"的技巧，而是一整套**工程纪律的编码化**。

这个项目的出发点很朴素：

> Developing real applications is hard. Approaches like GSD, BMAD, and Spec-Kit try to help by owning the process. But while doing so, they take away your control and make bugs in the process hard to resolve.

他认为现有的 AI 开发流程框架（Spec-Kit、BMAD 等）本质上是在**接管流程**——把控制权从开发者手里拿走。而他选择了一条完全不同的路：**小而可组合的纪律单元**，让开发者保持控制。

这篇文章会带你拆解这套系统的每个 skill，理解它们背后的工程哲学，以及为什么它们比"让 AI 一次干完所有事"要有效得多。

---

## 一、问题诊断：AI 编程的四大失败模式

Matt 把 AI 编程的失败归为四类，每类对应一个或一组 skill：

| 失败模式 | 症状 | 对应 Skill |
|---------|------|-----------|
| **#1 Agent 不理解你要什么** | 构建方向错误，交付物和预期不符 | `grill-me` / `grill-with-docs` |
| **#2 Agent 过于啰嗦** | token 浪费，术语不一致，代码命名混乱 | `grill-with-docs`（共享语言） |
| **#3 Agent 写的代码不能跑** | 缺少反馈循环，盲目编码 | `tdd` / `diagnose` |
| **#4 代码变成泥球** | 架构熵增加速，模块越来越浅 | `improve-codebase-architecture` / `zoom-out` |

关键洞察是：**AI 加速了编码，同时也加速了软件熵**。没有纪律约束的 AI 编程，比没有 AI 时腐烂得更快。

---

## 二、对齐优先：Grill-Me 与 Grilling 哲学

### 核心思想

> "No-one knows exactly what they want" — The Pragmatic Programmer

最常见的失败不是技术能力不足，而是**沟通不对齐**。你以为 agent 理解了你的需求，看到交付物才发现完全不是一回事。

`grill-me` 的 SKILL.md 只有 10 行，但哲学极深：

```markdown
Interview me relentlessly about every aspect of this plan
until we reach a shared understanding. Walk down each branch
of the design tree, resolving dependencies between decisions
one-by-one. For each question, provide your recommended answer.
Ask the questions one at a time.
```

关键词：** relentlessly（无情地追问）**、**one at a time（逐个回答）**、**provide your recommended answer（给出推荐方案）**。

这不是"你问我答"——这是 agent 主动遍历决策树，在每个分支上给出建议，逼迫用户做出明确选择。

### Grill-with-Docs：从对话到持久化知识

`grill-me` 解决的是即时对齐。`grill-with-docs` 更进一步——在对话过程中**实时构建项目文档**。

它引入两个核心文档：

**CONTEXT.md**——领域术语表，只记录项目特有的术语定义：

```markdown
## Language

**Order**:
A customer's request to purchase one or more products.
_Avoid_: Purchase, transaction

**Materialization**:
The process of giving a lesson a permanent spot in the file system.
_Avoid_: Publishing, saving, making real
```

规则极其严格：
- **必须有立场**——同义词只留一个，其他的放进 `_Avoid_`
- **定义要精准**——一两句话，讲"是什么"不讲"做什么"
- **不要包含通用概念**——timeout、error handling 这些不属于 CONTEXT.md

**ADR（Architecture Decision Record）**——架构决策记录，只在三个条件同时满足时创建：
1. 难以回退——后期改变代价很大
2. 缺少上下文时显得突兀——未来的读者会困惑"为什么这么做"
3. 是真实权衡的结果——有替代方案，选择了其中一个

这种"延迟创建"（create lazily）的设计非常关键——不是在项目开始时就写好所有文档，而是在对话中**当第一个术语被澄清时才创建文件**。

---

## 三、共享语言的力量

> "With a ubiquitous language, conversations among developers and expressions of the code are all derived from the same domain model." — Eric Evans, Domain-Driven Design

这是整套系统中**最强大**的技术。`grill-with-docs` 不仅是"问问题"，而是在帮助你和 AI 建立**共同的语言体系**——这正是 DDD 中 Ubiquitous Language 的概念。

举个例子：

- **之前**："When a lesson inside a section of a course is made 'real' (i.e. given a spot in the file system)"
- **之后**："There's a problem with the materialization cascade"

共享语言带来的好处：

1. **命名一致性**——变量、函数、文件都使用统一术语
2. **更易导航**——agent 理解代码结构更准确
3. **更少 token 消耗**——用 1 个词代替 20 个词的解释
4. **减少歧义**——"account" 是 Customer 还是 User？CONTEXT.md 告诉你

---

## 四、反馈循环：TDD 与 Diagnose

### TDD：红-绿-重构的正确姿势

这套系统的 TDD skill 有两个极其重要的反模式警告：

**❌ 水平切片（Horizontal Slicing）——绝对不要这样做：**

```
WRONG:
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5
```

一次性写完所有测试，再一次性写完所有实现。这会产生"垃圾测试"——测试的是**想象中的行为**而非**真实的行为**。

**✅ 垂直切片（Vertical Slicing）——正确做法：**

```
RIGHT:
  RED→GREEN: test1→impl1
  RED→GREEN: test2→impl2
  RED→GREEN: test3→impl3
```

每个测试-实现循环都是对前一次学习的响应。因为你刚写完代码，所以你知道什么行为最重要、怎么验证它。

TDD skill 还强调：

- **测试公共接口，不测实现细节**——好测试读起来像规格说明
- **通过领域语言命名测试**——测试名和接口词汇与项目的语言一致
- **深度模块优先**——小接口，大实现
- **永远不要在 RED 状态下重构**——先 GREEN，再重构

### Diagnose：硬 Bug 的诊断纪律

`diagnose` 是最长的 skill（117 行），也是最硬核的一个。它定义了一个 6 阶段的诊断流程：

1. **建立反馈循环**——这是核心技能。用 9 种方式之一构建可自动运行的 pass/fail 信号
2. **复现**——看着 bug 出现，确认就是你以为的那个 bug
3. **假设**——生成 3-5 个排好序的假设，每个必须是可证伪的
4. **仪器化**——每次探测对应一个假设，一次只改一个变量
5. **修复 + 回归测试**——在正确的 seam 上写回归测试
6. **清理 + 复盘**——所有 DEBUG 日志清除，原型删除

最关键的洞察在第一阶段：

> Build the right feedback loop, and the bug is 90% fixed.

它提供了 10 种构建反馈循环的方式，按优先级排列：失败测试 → curl 脚本 → CLI 调用 → 无头浏览器脚本 → 重放 trace → 最小化 harness → 模糊测试 → git bisect → 差分测试 → 人机协作循环。

并且强调：

> A 30-second flaky loop is barely better than no loop. A 2-second deterministic loop is a debugging superpower.

这个诊断系统最聪明的地方在于——**修复之后还要问：什么架构变更能防止这类 bug？** 如果答案是"需要架构变更"（没有好的测试 seam、调用者纠缠、隐藏耦合），就自动交接给 `improve-codebase-architecture`。

---

## 五、架构治理：深度化与 Zoom-Out

### Improve-Codebase-Architecture

这个 skill 的核心概念来自 John Ousterhout 的《A Philosophy of Software Design》：**深度模块**（小接口，大实现）vs **浅层模块**（接口几乎和实现一样复杂）。

它定义了一套精确的术语表：

| 术语 | 定义 |
|------|------|
| **Module** | 任何有接口和实现的东西（函数、类、包、切片） |
| **Interface** | 调用者需要知道的一切（类型、不变量、错误模式、顺序、配置） |
| **Depth** | 接口背后的杠杆率：大量行为藏在简单接口后面 |
| **Seam** | 接口所在的位置；可以改变行为而不修改原代码的地方 |
| **Adapter** | 在 seam 处满足接口的具体实现 |

关键原则：

- **删除测试**——想象删除一个模块。如果复杂度消失了，它是透传；如果复杂度在 N 个调用者中重新出现，它才是真正有价值的
- **接口就是测试面**
- **一个 adapter = 假设的 seam；两个 adapters = 真正的 seam**

它会生成 HTML 报告，用 Mermaid 图表和手写 CSS 可视化每个候选重构的"之前/之后"架构对比。

### Zoom-Out

最简单的 skill——只有 7 行。它的用途是让 agent 退后一步，给出更高层级的视角：

```markdown
I don't know this area of code well. Go up a layer of abstraction.
Give me a map of all the relevant modules and callers.
```

这解决了一个实际问题：agent 在局部代码中迷路时，需要一张地图。

---

## 六、工作流编排：从 PRD 到 Issue

这套系统还覆盖了完整的工作流：

### To-PRD → To-Issues → Triage → TDD

1. **To-PRD**：把对话内容合成 PRD（不追问用户，直接利用已有上下文），发布到 issue tracker
2. **To-Issues**：把 PRD 拆成**垂直切片**的独立 issue，每个 slice 是端到端的、可演示的
3. **Triage**：用状态机管理 issue 生命周期（`needs-triage` → `ready-for-agent` → `ready-for-human` → `wontfix`）
4. **TDD**：拿到 `ready-for-agent` 的 issue 后，用红-绿-重构循环实现

这个流程的关键是**每个 issue 都是垂直切片**——不是"写后端 API"和"写前端 UI"的水平拆分，而是"作为用户，我想完成 checkout"这样的端到端 slice。

### Handoff

在对话即将结束时，把当前对话压缩成一份交接文档，让新的 agent 可以无缝接手。不重复已有内容（PRD、ADR、issue），只引用路径或 URL。

---

## 七、系统设计哲学

通读全部源码后，我总结出几个贯穿始终的设计原则：

### 1. 组合优于接管

每个 skill 都是独立的、可插拔的。你可以只用 `tdd`，或者只用 `grill-with-docs`，或者组合使用。它们不强制你遵循特定流程——**你保持控制权**。

### 2. 延迟创建

文档不是项目开始时一次性写好的。CONTEXT.md 在第一个术语被澄清时才创建。ADR 在真正有决策需要记录时才写。这种"按需创建"避免了文档维护的开销。

### 3. 语言先行

在写任何代码之前，先确保你和 agent 使用**同一套语言**。这比任何代码生成技巧都重要。

### 4. 纪律编码化

TDD 的红-绿-重构、diagnose 的六阶段流程、triage 的状态机——这些不是"建议"，而是**编码在 skill 中的纪律**。AI 不是不知道这些实践，而是缺少执行它们的外部约束。

### 5. 反馈循环是核心

无论是调试（diagnose）还是开发（tdd），核心都在于构建**快速、确定性的反馈循环**。没有反馈循环的编码就是盲飞。

---

## 八、对我的启发

作为第一性原理工程师，我认为这套系统最有价值的不是任何单个 skill，而是它回答了一个根本问题：

**在 AI 编程时代，什么是"好的工程实践"？**

答案是：**没有变**。TDD、DDD、架构治理、反馈循环——这些经典实践反而变得更重要了。因为 AI 加速了编码速度，也就加速了架构熵增。没有纪律约束的 AI 编程，比没有 AI 时腐烂得更快。

Matt 的贡献不是发明了新的工程实践，而是**把这些实践编码化为 AI 可执行的技能**——让 AI 不只是写代码的工具，而是真正理解工程纪律的协作伙伴。

这套系统的局限在于它需要人工参与（grilling session、issue triage），但这恰恰是它的优势——**你保持控制权**。AI 不是替代工程师，而是放大工程师的判断力。

---

*完整源码：[github.com/mattpocock/skills](https://github.com/mattpocock/skills)*
