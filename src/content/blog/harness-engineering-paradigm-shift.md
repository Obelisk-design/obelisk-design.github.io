---
title: "Harness Engineering：从 Prompt 到 Agent 环境的范式转移"
pubDate: "2026-05-26"
description: "为什么 Agents 难的不是模型而是环境？深入解析三阶段演进与业界实践"
heroImage: '../../assets/blog-placeholder-1.jpg'
tags: ['Harness Engineering', 'Agent', 'LLM', 'Prompt Engineering', 'Context Engineering', 'Anthropic', 'Stripe', 'Codex']
---

## 开篇

2022 年，ChatGPT 发布后的几个月里，整个行业都在讨论同一件事：**怎么写 prompt**。

人们总结出了 few-shot、Chain-of-Thought、角色扮演、输出格式约束——这些技巧确实有效，但它们有一个共同的特征：**每一次对话都是一次性的**。你写好 prompt，得到结果，下次可能需要重新写。

2025 年，Karpathy 提出了 Context Engineering——重心从"怎么写"转向了"往 context window 里放什么"。Cursor、Lovable 这类工具的出现，标志着我们开始把代码库、LSP 信息、依赖关系这些结构化的知识塞进 AI 的"工作记忆"。

但到了 2026 年，一个更深刻的认知开始浮现：

> **"Agents aren't hard; the Harness is hard."**

这不是口号，而是无数工程团队在实战中撞出来的结论。今天这篇文章要回答的问题是：

**为什么 Harness 才是真正的工程难点？它到底难在哪里？**

---

## 第一层：从"对话"到"环境"的认知跃迁

### 1.1 三个阶段，三种心智模型

| 阶段 | 核心问题 | 典型产物 | 失败模式 |
|------|---------|---------|---------|
| Prompt Engineering（~2022） | "怎么跟 AI 说话？" | prompt 模板、few-shot 示例 | 同样的 prompt，每次输出不同 |
| Context Engineering（~2025） | "AI 需要知道什么？" | 代码库索引、系统 prompt、工具列表 | context rot、信息过载 |
| Harness Engineering（~2026） | "AI 在什么环境中运行？" | Agent SDK、反馈循环、控制系统 | 环境不可观测、错误不可回溯 |

这三个阶段不是取代关系，而是**嵌套关系**。Harness 包含 Context，Context 包含 Prompt——每一层都在回答更深层的工程问题。

### 1.2 为什么会有这种演进？

根本原因在于 **LLM 能力本身的快速商品化**。

当 GPT-3.5 发布时，"能让 AI 写出像样的代码"本身就是竞争力。但到了 GPT-4o、Opus 4.5、Claude 4 这一代，**模型写代码的能力已经不再是瓶颈**。瓶颈变成了：

- AI 不知道项目的约定是什么
- AI 不知道哪些模块是高风险的、不能碰的
- AI 不知道自己写完之后该怎么验证
- AI 不知道运行出错了该怎么修复
- AI 不知道多个 session 之间怎么交接

这些不是模型能力问题，而是**运行环境问题**。

这就引出了 Harness Engineering 的核心定义。

---

## 第二层：Harness 是什么——不仅仅是工具包装

### 2.1 重新定义 Harness

在编程语境中，"Harness" 原本是一个测试术语——test harness，指**包裹在代码外面的测试框架**，负责提供输入、捕获输出、验证结果。

Anthropic 在 2025 年 11 月的工程博客中给了一个更精确的定义：

> Harness 是让 agent 有效使用工具、管理上下文、执行任务并验证结果的**结构化环境**。

这个定义包含四个关键词：

1. **使用工具** —— agent 需要什么能力（读文件、运行命令、调用 API）
2. **管理上下文** —— 在多窗口工作中如何保持连续性
3. **执行任务** —— 如何分解、调度、推进
4. **验证结果** —— 怎么知道做得对不对

### 2.2 Harness ≠ 框架

这是最常见的误解。很多人以为用了 Claude Agent SDK、CrewAI、LangGraph 就是在做 Harness Engineering——但框架只是 Harness 的**基础设施层**。

真正的 Harness 包括：

```
Harness = 框架（SDK/工具） 
        + 约束（规则/权限/边界）
        + 观测（日志/监控/告警）
        + 反馈（测试/验证/修复循环）
        + 状态管理（session 间的信息传递）
        + 人机协作（何时介入、如何介入）
```

Anthropic 的实践给出了一个极简但深刻的例子：让 agent 在每次 session 结束时写 `claude-progress.txt`，下一个 session 从这里开始。

这看起来很简单，但它解决的正是**跨 session 状态连续性**这个 Harness 核心问题。

---

## 第三层：Harness 到底难在哪里？

### 3.1 五种核心挑战

#### 挑战一：状态连续性问题

Anthropic 描述了一个生动比喻：

> 想象一个软件项目由轮班制的工程师完成，每个新工程师上班时都对上一班做了什么毫无记忆。

这正是多 session agent 面临的问题。Context window 是有限的，compaction 不够完美，agent 倾向于一次性做太多事然后在半路断掉。

Anthropic 的解决方案是**双 agent 模式**：

```
Initializer Agent（只运行一次）
  ├── 创建环境骨架
  ├── 写出完整 Feature List（200+ 条，初始标记为 failing）
  ├── 创建 progress 日志文件
  └── 初始 Git commit
  
Coding Agent（循环运行）
  ├── 读取 progress 文件 + Git 历史
  ├── 做增量工作
  ├── 更新 progress 文件
  └── 保持代码库可合并状态
```

这个模式的核心洞察是：**让 agent 像人类工程师一样交接工作**——用文件记录进度、用 Git 管理变更、用 Feature List 定义完成标准。

#### 挑战二：环境隔离与安全边界

Stripe 的 Minions 项目展示了另一种思路：

> **One-shot, End-to-End Coding Agents**——一次性完成端到端的编码任务。

Minions 的核心做法是让多个 agent 并行工作，每个 agent 负责不同的子任务。但这就引出了 Harness 的另一个关键问题：**怎么让多个 agent 同时修改同一个代码库而不互相破坏？**

这需要：
- 文件系统级别的隔离（每个 agent 在独立分支工作）
- 权限控制（哪些 agent 可以合并到 main，哪些不能）
- 冲突检测和自动解决策略
- 合并后的回归测试

#### 挑战三：反馈循环的质量

Harness 不是单向的。它需要建立"做 → 验证 → 修复 → 再做"的循环。

但这里的难点在于：**验证本身可能比执行更难。**

以 Stripe Minions 为例，他们的"1000 PR agent"不是让 agent 写 1000 个 PR 就完了——而是每个 PR 都必须通过 CI、代码审查、测试验证。Harness 必须保证：

- agent 能看到测试失败的原因
- agent 有能力修复测试失败
- agent 不会在修复 A 时引入 B
- agent 知道什么时候该停下来请求人类帮助

#### 挑战四：可观测性与调试

当 agent 在 10 个 context window 中工作了几小时，突然产出了错误的结果——你怎么定位问题出在哪个环节？

传统的 debug 工具（断点、日志、profiler）是为人类设计的。Agent 需要的是：

- Session 级别的执行轨迹（每个 window 做了什么决策）
- 工具调用的时间线和参数
- 验证结果的汇总
- 跨 session 的因果链

这就是为什么 Anthropic 特别强调 progress 文件——它本质上是一个**低带宽但高可靠的状态同步通道**。

#### 挑战五：人机协作的时机

Harness 不是完全自动化的。**人什么时候介入，比自动化本身更重要。**

介入太早 → 打断 agent 的节奏，浪费了自主能力
介入太晚 → agent 已经跑偏了很长时间，修正成本巨大

这个问题的答案不在 Harness 本身，而在 **Harness 的观测系统**——只有当你能实时看到 agent 在做什么、做得对不对，你才能在正确的时间点介入。

---

## 第四层：业界实践——三种不同的 Harness 哲学

### 4.1 Anthropic：渐进式 + 状态管理

**核心理念：让 agent 做人类工程师做的事。**

- Initializer + Coding Agent 双模式
- Progress 文件作为跨 session 状态载体
- Git 作为版本管理和交接媒介
- Feature List 作为完成度追踪
- 每个 session 结束时保持"可合并"状态

**适用场景：** 复杂的、需要长时间工作的项目（构建完整应用、重构大型代码库）。

### 4.2 Stripe：并行 + 一次性完成

**核心理念：让多个 agent 同时工作，一次性完成端到端任务。**

- Minions 模式：一个主 agent 分解任务，多个子 agent 并行执行
- 每个 agent 独立分支，避免冲突
- 完成后自动合并 + 验证
- 目标是"提交一个完整的 PR"，而不是"做几步然后等人类"

**适用场景：** 可以并行分解的独立任务（批量重构、API 迁移、批量测试）。

### 4.3 OpenAI Codex：终端驱动 + 沙箱执行

**核心理念：agent 在沙箱终端中工作，通过终端输出获得即时反馈。**

- Agent 通过终端工具执行命令
- 终端输出作为反馈信号
- 沙箱环境隔离风险
- 支持长时间运行的后台任务

**适用场景：** 需要频繁运行命令、查看输出的开发工作（调试、构建、测试）。

### 4.4 三种哲学的对比

| 维度 | Anthropic | Stripe | Codex |
|------|-----------|--------|-------|
| 工作模式 | 串行、渐进 | 并行、一次性 | 交互式、终端驱动 |
| 状态管理 | Progress 文件 + Git | 分支隔离 | 沙箱环境 |
| 验证方式 | Feature List 逐项检查 | CI + 自动化审查 | 终端输出 |
| 人的角色 | 关键节点审核 | 最终审查 | 实时交互 |
| 擅长场景 | 长期复杂项目 | 可并行批量任务 | 即时开发调试 |

---

## 第五层：Harness 的未来——正在形成的标准

### 5.1 NIST AI Agent Standards Initiative

2026 年 2 月，NIST CAIS 启动了 AI Agent 标准倡议。这标志着 Harness Engineering 从"各家公司自己做"进入了"行业标准化"阶段。

虽然具体标准还在制定中，但以下几个方向已经达成共识：

1. **Agent 能力的标准化描述** —— 一个 agent 能做什么、不能做什么，应该有机器可读的描述
2. **工具接口的标准化** —— agent 调用工具的方式应该有统一协议
3. **安全边界的标准化** —— 什么操作需要人类确认，什么可以自动执行
4. **观测与审计的标准化** —— agent 的行为应该可以被记录、回放、审计

### 5.2 Terminal Bench 2.0

Terminal Bench 是评估 agent 能力的基准测试。2.0 版本的重点从"agent 能不能写代码"转向了"agent 能不能在真实终端环境中完成任务"——这恰恰是 Harness 的核心。

因为 **Harness 的质量决定了 agent 在真实环境中能发挥多少能力**。一个在 benchmark 中得分 95 的 agent，在一个糟糕的 Harness 中可能连 60 都达不到。

### 5.3 MCP（Model Context Protocol）的崛起

Anthropic 提出的 MCP 协议正在成为 agent 工具调用的事实标准。它的核心价值在于：

> **把工具的定义和调用标准化，让同一个 agent 可以跨不同环境使用相同的工具接口。**

这是 Harness 工程化的重要一步——当工具接口标准化后，Harness 可以专注于更高层次的问题：调度、观测、反馈循环。

---

## 第六层：给你的行动指南

### 6.1 如果你刚开始用 AI 编程

不要一开始就追求复杂的 Harness。按这个顺序来：

1. **先用好 prompt** —— 学会写清晰、具体、可重复的 prompt
2. **建立 context 意识** —— 开始思考"AI 需要知道什么才能做出正确决策"
3. **沉淀 CLAUDE.md / AGENTS.md** —— 把项目规范写到代码库里
4. **建立反馈循环** —— 让 AI 写完代码后自己跑测试、修 bug
5. **再谈 Harness** —— 当上面的步骤都稳定了，再考虑更复杂的 agent 编排

### 6.2 如果你已经在用 AI 做开发

问自己这几个问题：

- 你的 agent 在 session 之间能无缝交接吗？
- 你能看到 agent 的完整决策轨迹吗？
- agent 出错时，能自己发现并修复吗？
- 你知道 agent 在哪些时刻需要人类介入吗？
- 你的 Harness 有没有在膨胀（文件越来越多、越来越难维护）？

如果有一个问题的答案是"不能"或"不确定"，那就是你需要改进的方向。

### 6.3 Harness 设计的三个原则

1. **可观测性优先于自动化** —— 先让 agent 的行为可见，再追求全自动
2. **渐进式约束** —— 从宽松到严格，让 agent 有机会犯错但不要造成不可逆的伤害
3. **状态显式化** —— 所有 session 间的状态传递都通过文件、Git commit、日志等显式载体，不要依赖隐式的"agent 应该记得"

---

## 总结

Harness Engineering 的本质不是"给 AI 加约束"，而是**给 AI 建一个能安全、可靠、可观测地工作的环境**。

Prompt Engineering 解决的是"怎么跟 AI 沟通"的问题。
Context Engineering 解决的是"AI 需要什么信息"的问题。
Harness Engineering 解决的是"AI 在什么条件下工作"的问题。

从"说话"到"信息"到"环境"——这是 AI 工程化能力不断深化的自然路径。

> **AI 模型的能力在快速商品化。真正的工程壁垒，是你构建的那个 Harness。**

它不是某个 SDK 或框架，而是一整套**让 AI 在正确约束下执行、在正确时机被人类介入、在所有行为都可观测可追溯**的工程体系。

这不是未来主义的空谈。Stripe、Anthropic、OpenAI 已经在生产环境中实践了这些模式。NIST 在制定标准。Terminal Bench 在量化评估。

**Harness Engineering 的时代，已经来了。**

---

## 延伸阅读

- Anthropic: [Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)（2025.11）
- Anthropic: [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)
- Stripe Engineering: [Minions: Stripe\'s One-Shot, End-to-End Coding Agents](https://stripe.com/blog/minions)
- Ryan Lopopolo: [Harness Engineering: Leveraging Codex](https://github.com/openai/codex)
- LangChain: [The Anatomy of an Agent Harness](https://blog.langchain.dev/)
- NIST CAIS: [AI Agent Standards Initiative](https://www.nist.gov/) (2026.02)
- Andrej Karpathy: [Context Engineering](https://x.com/karpathy) (2025.06)
