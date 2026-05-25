---
title: 'Matt Pocock 的 AI Agent Skills：工程师的实战武器库'
description: '深入解析 10 万 Star 的 AI 编程技能库，从入门到精通'
pubDate: '2026-05-25'
heroImage: '../../assets/blog-placeholder-1.jpg'
tags: ['AI', 'Engineering', 'Productivity', 'Claude', 'TypeScript']
---

## 前言：一个 TypeScript 巫师的秘密武器

在 GitHub 上，有一个仓库获得了超过 **10 万 Star**——这在技术圈是罕见的。更罕见的是，它的作者 Matt Pocock 将这些内容称为「给真正工程师的技能」，而不是「给 AI 爱好者的玩具」。

Matt Pocock 是谁？

- **TypeScript 领域权威**：Total TypeScript 课程创始人
- **前 Vercel、Stately 工程师**
- **近 2 万 GitHub 粉丝**
- **XState 状态机库的重要贡献者**

这个仓库的名字叫 `skills`，但它不是传统意义上的「技能列表」。它是一套可被 Claude Code、Codex 等 AI 编程助手直接加载的**指令文件系统**——一套将几十年软件工程经验压缩成可复用模式的完整体系。

---

## 第一层理解：什么是 AI Agent Skills？

### 从「提示词工程」到「技能文件」

你可能用过 ChatGPT，写过类似这样的提示词：

```
请帮我写一个登录页面，要求：
1. 有用户名和密码输入框
2. 有记住我选项
3. 点击登录后验证...
```

这种方式有个致命问题：**每次都要重新描述你的期望**。

AI Agent Skills 解决了这个问题。它的工作方式是：

```
/project/
├── .claude/
│   └── skills/
│       ├── tdd/SKILL.md
│       ├── diagnose/SKILL.md
│       └── grill-me/SKILL.md
```

当你在项目目录下启动 Claude Code 时，它会**自动加载**这些技能文件。之后你只需要说：

```
/tdd 实现用户登录功能
```

AI 就会按照 `tdd/SKILL.md` 中定义的完整流程执行——包括测试先行、红绿重构、避免坏测试等一系列工程实践。

### 一个技能文件长什么样？

让我们看一个真实的例子——`/grill-me` 技能：

```markdown
---
name: grill-me
description: Interview the user relentlessly about a plan or design 
  until reaching shared understanding...
---

Interview me relentlessly about every aspect of this plan 
until we reach a shared understanding. Walk down each branch 
of the design tree, resolving dependencies between decisions 
one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time.

If a question can be answered by exploring the codebase, 
explore the codebase instead.
```

不到 100 字，但包含了完整的**意图、策略和约束**。这就是技能文件的精髓——将复杂的工程智慧压缩成可复用的指令模式。

---

## 第二层理解：核心技能深度解析

Matt Pocock 将技能分为三大类：工程类、效率类和杂项。让我们深入理解最核心的几个。

### 1. `/grill-me` 和 `/grill-with-docs`：对齐的艺术

**问题背景**：软件开发中最常见的失败模式是什么？

> "No-one knows exactly what they want"
> — *The Pragmatic Programmer*

你告诉 AI「做一个登录页面」，AI 做出来，你发现不是你想要的。你说「不对，我要的是邮箱登录」，AI 改了，你又说「不对，验证码呢？」

**技能原理**：`/grill-me` 的核心是**设计树的逐分支解析**。

```
                    你的需求
                      │
        ┌─────────────┼─────────────┐
        │             │             │
     认证方式      安全级别      用户体验
        │             │             │
    ┌───┴───┐     ┌──┴──┐      ┌───┴───┐
   邮箱  手机     高   中      极简  丰富
    │       │     │    │       │       │
  验证码?  短信?  MFA? 仅密码?  动画?   仪表盘?
```

AI 会一个分支一个分支地问你，每个问题都给出**推荐答案**。你不必回答所有问题——AI 会帮你发现你没想到的边界情况。

**进阶版** `/grill-with-docs` 更进一步：

1. 检查你的回答是否与项目现有术语一致
2. 如果你说「取消」，但项目里定义的是「撤回」，AI 会立刻指出冲突
3. 每确定一个术语，立即更新 `CONTEXT.md` 文档

这解决了一个深层问题：**AI 往往用 20 个词描述可以用 1 个词说清楚的概念**。

```
❌ 之前：「当一个课程里的一个章节被正式创建时，也就是有了真实的文件路径时...」
✅ 之后：「当 materialization cascade 触发时...」
```

### 2. `/tdd`：测试驱动的正确姿势

你可能听过 TDD（测试驱动开发）：先写测试，再写实现，然后重构。但你可能不知道，大多数人做的 TDD 是错的。

**错误的做法（水平切片）**：

```
RED 阶段：写完所有测试（test1, test2, test3, test4, test5）
GREEN 阶段：写完所有实现（impl1, impl2, impl3, impl4, impl5）
```

这会产生**坏测试**：
- 测试的是想象中的行为，不是实际行为
- 测试的是数据结构的形状，不是用户场景
- 重构时测试全挂，行为没变却要改测试

**正确的做法（垂直切片）**：

```
RED→GREEN：test1 → impl1
RED→GREEN：test2 → impl2
RED→GREEN：test3 → impl3
```

每次只写一个测试，只写一个实现。测试告诉你刚才写的代码实际做了什么，下一个测试基于这个认知调整。

**什么是好测试？**

```typescript
// ✅ 好测试：测试通过公共接口的 observable 行为
test("user can checkout with valid cart", async () => {
  const cart = createCart();
  cart.add(product);
  const result = await checkout(cart, paymentMethod);
  expect(result.status).toBe("confirmed");
});

// ❌ 坏测试：测试实现细节
test("checkout calls paymentService.process", async () => {
  const mockPayment = jest.mock(paymentService);
  await checkout(cart, payment);
  expect(mockPayment.process).toHaveBeenCalledWith(cart.total);
});
```

坏测试的问题是：你重命名了 `paymentService` 的某个方法，测试就挂了——但**行为根本没变**。

**什么时候该 Mock？**

只 Mock **系统边界**：
- 外部 API（支付、邮件服务）
- 数据库（有时）
- 时间/随机性
- 文件系统（有时）

**绝对不要 Mock**：
- 你自己的类/模块
- 内部协作对象
- 任何你能控制的东西

### 3. `/diagnose`：调试的纪律

当你遇到一个棘手的 bug，第一反应是什么？

如果你直接开始看代码、打 log、改代码试试——你已经在浪费时间了。

**`/diagnose` 的核心洞察**：**反馈回路就是调试技能的全部**。

如果你有一个快速、确定性、可自动运行的 pass/fail 信号，你迟早会找到 bug。如果你没有，看再多代码也没用。

**构建反馈回路的 10 种方法（按优先级排序）**：

1. **写一个失败的测试**——能到达 bug 的任何层级都行
2. **curl/HTTP 脚本**——对着运行中的开发服务器
3. **CLI 调用**——用 fixture 输入，diff 输出
4. **无头浏览器脚本**（Playwright/Puppeteer）
5. **重放捕获的 trace**——保存真实的网络请求，隔离重放
6. **临时 harness**——启动系统的最小子集
7. **属性/模糊测试**——跑 1000 个随机输入
8. **二分 harness**——`git bisect run` 自动化
9. **差分循环**——旧版本 vs 新版本，diff 输出
10. **人工循环脚本**——让人必须点击时，用脚本驱动人

**反馈回路优化的三个问题**：

- 能更快吗？（缓存 setup，跳过无关初始化）
- 信号更清晰吗？（断言具体症状，而不是「没崩溃」）
- 更确定吗？（固定时间，固定随机种子，隔离文件系统）

一个 30 秒的抖动回路几乎等于没有。一个 2 秒的确定性回路是调试超能力。

### 4. `/improve-codebase-architecture`：避免泥球

**问题**：AI 能极大加速编码，也能极大加速软件腐烂。代码库变成「泥球」的速度前所未有。

**核心概念**：**模块深度（Module Depth）**

> "The best modules are deep. They allow a lot of functionality 
> to be accessed through a simple interface."
> — *A Philosophy of Software Design*

```
         浅模块                          深模块
    ┌─────────────────┐              ┌─────────┐
    │ 接口            │              │ 接口    │
    │ ├─ 配置项 1     │              │ (3 个参数)
    │ ├─ 配置项 2     │              └────┬────┘
    │ ├─ 回调函数     │                   │
    │ ├─ 错误处理     │              ┌────┴────┐
    │ └─ ...更多...   │              │         │
    ├─────────────────┤              │   大量   │
    │ 实现（简单）    │              │   复杂   │
    └─────────────────┘              │   实现   │
                                     │         │
                                     └─────────┘
```

**删除测试**：想象删除这个模块。如果复杂度消失了，它只是个传递层。如果复杂度在 N 个调用者身上重现，它本来就在赚它的位置。

**接口即测试面**：测试通过接口验证行为，不关心实现。

**一个 Adapter = 假设的 Seam；两个 Adapter = 真正的 Seam**：如果你只有一个数据库实现，那不是真正的抽象层，只是一个希望未来灵活的幻想。

---

## 第三层理解：核心理念的哲学根基

读完这些技能，你会发现一个模式：**它们都是对「AI 时代软件工程失败模式」的回应**。

### 失败模式一：不对齐

**现象**：你想要 A，AI 做了 B。你改需求，AI 做了 C。无限循环。

**根源**：人类的模糊性和 AI 的字面理解之间的鸿沟。

**解决方案**：`/grill-me` 的**分支逐一解析**——把模糊的需求分解成一棵决策树，每个叶子节点都必须被确认。

### 失败模式二：术语膨胀

**现象**：AI 用 20 个词描述一个概念，每次描述还不一样。代码里到处是 `cancel`、`abort`、`terminate`、`stop` 指同一件事。

**根源**：AI 缺乏项目的「共同语言」。

**解决方案**：`CONTEXT.md` 和 ADR（架构决策记录）——建立项目的领域词典和决策档案。

```
项目根目录/
├── CONTEXT.md          # 领域词汇表
├── docs/
│   └── adr/            # 架构决策记录
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

### 失败模式三：坏测试

**现象**：重构时测试全挂，行为明明没变。或者测试通过了，行为却错了。

**根源**：测试了实现而不是行为。

**解决方案**：`/tdd` 的**垂直切片**原则——一个测试一个实现，测试必须描述「what」而不是「how」。

### 失败模式四：无反馈

**现象**：bug 修了一天还不知道原因，只是在瞎试。

**根源**：没有确定性的可重复的失败信号。

**解决方案**：`/diagnose` 的**反馈回路优先**原则——90% 的调试精力应该花在构建反馈回路上。

### 失败模式五：泥球架构

**现象**：代码库越来越难改，牵一发而动全身。

**根源**：每次修改都增加了浅模块（接口和实现一样复杂的模块）。

**解决方案**：`/improve-codebase-architecture` 的**深度模块**原则——让接口简单，让实现负责复杂。

---

## 第四层理解：从使用到创造

### 安装和使用

**快速开始（30 秒）**：

```bash
npx skills@latest add mattpocock/skills
```

然后：
1. 选择你需要的技能
2. 选择要安装到哪个 AI 编程助手
3. 运行 `/setup-matt-pocock-skills` 配置项目

**核心技能推荐**：

| 技能 | 用途 | 使用频率 |
|------|------|----------|
| `/grill-with-docs` | 新功能设计前 | 每次新功能 |
| `/tdd` | 编写代码时 | 每次编码 |
| `/diagnose` | 调试 bug 时 | 每次 bug |
| `/triage` | 管理任务时 | 每周 |
| `/improve-codebase-architecture` | 重构优化 | 每几天 |

### 创造你自己的技能

Matt 的技能文件遵循一个简单的格式：

```markdown
---
name: your-skill-name
description: When to use this skill (auto-triggers matter)
argument-hint: "Optional: what argument to expect"
---

The actual skill content...

Use markdown sections to organize.
Reference other files with relative paths.
```

**好的技能文件特征**：

1. **触发条件清晰**：description 说明何时自动激活
2. **渐进披露**：先核心，再细节
3. **可验证**：包含明确的验收标准
4. **可扩展**：引用外部文件而不是塞进一个文件

### 与现有工具集成

这些技能不是替代你的工具，而是**增强你的 AI 编程助手**：

```
你的项目
├── .claude/          # Claude Code
│   └── skills/
├── .cursor/          # Cursor
│   └── skills/
├── .codex/           # Codex
│   └── AGENTS.md
└── .vscode/
    └── ...
```

---

## 第五层理解：AI 时代的工程哲学

### 为什么这些技能重要？

**核心洞察**：AI 编程助手让编码速度提升了 10 倍，但**也让错误速度提升了 10 倍**。

传统的软件工程实践——测试、重构、代码审查——是在人类编码速度下演化的。当编码速度提升一个数量级，这些实践需要重新设计。

Matt Pocock 的技能体系正是这种重新设计：

| 传统实践 | AI 时代的演进 |
|----------|---------------|
| 需求文档 | `/grill-with-docs` 动态对齐 |
| 代码审查 | `/tdd` 内置质量门 |
| 调试技巧 | `/diagnose` 系统化反馈回路 |
| 重构直觉 | `/improve-codebase-architecture` 深度分析 |

### 核心原则的抽象

贯穿所有技能的核心原则可以抽象为：

1. **对齐先于行动**：在写代码前，确保 AI 和你理解一致
2. **行为高于实现**：测试和描述都要聚焦于「做什么」，而非「怎么做」
3. **反馈回路是超能力**：能自动验证的，就不要猜测
4. **语言是压缩**：共享术语能将 token 消耗降低 75%
5. **深度模块降低熵**：每个模块都应该在「赚它的位置」

### 适用边界

**这些技能适合谁？**

- 已经有一定工程经验，想用 AI 提升效率的人
- 在使用 Claude Code、Codex、Cursor 等 AI 编程助手的人
- 愿意学习新的工作流，而不是直接「让 AI 替我写代码」的人

**这些技能不适合谁？**

- 想要「AI 一键生成」不做任何思考的人
- 没有软件工程基础，期望 AI 弥补所有能力差距的人
- 项目很简单（几百行代码），不需要复杂工作流的人

---

## 实战：一个完整的工作流示例

假设你要实现一个用户积分系统：

### Step 1: 对齐需求

```
/grill-with-docs 实现用户积分系统，用户可以通过购买商品、
签到、邀请新用户获得积分，积分可以兑换优惠券
```

AI 会问你：

1. 积分有效期是永久的还是有过期时间？
2. 购买商品的积分比例是固定的还是可配置的？
3. 签到积分每天一样还是有连续签到加成？
4. 邀请积分是单次还是按新用户活跃度发放？
5. 优惠券的面额和积分兑换比例？

每个问题，AI 都会根据你的项目上下文给出**推荐答案**。

### Step 2: 创建 PRD

```
/to-prd
```

AI 会根据刚才的对齐结果，自动创建一份产品需求文档（以 GitHub Issue 形式），包含：
- 问题陈述
- 解决方案
- 用户故事列表
- 实现决策
- 模块划分建议

### Step 3: 拆分任务

```
/to-issues
```

AI 会将 PRD 拆分成一系列独立的可领取的任务（Vertical Slices），每个任务包含：
- 具体要做什么
- 涉及哪些模块
- 如何测试

### Step 4: TDD 实现

```
/tdd 实现积分累计模块
```

AI 会：
1. 确认接口变更
2. 确认要测试的行为（优先级排序）
3. 写一个测试 → 写实现 → 重构 → 写下一个测试...
4. 确保每个测试都是行为测试，不是实现测试

### Step 5: 遇到 Bug

```
/diagnose 积分累计有时会重复计算
```

AI 会引导你：
1. 构建一个能稳定复现的测试用例
2. 逐步缩小问题范围
3. 形成假设
4. 用最少代码修复
5. 写回归测试

---

## 总结：从工具到方法论

Matt Pocock 的 Skills 仓库，表面上是一堆 Markdown 文件，实质上是**一套完整的 AI 时代软件工程方法论**。

它的价值不在于具体的命令格式，而在于背后的工程原则：

- **对齐是第一位的**：在你和 AI 的理解一致之前，任何代码都是浪费
- **测试不是负担**：好的测试是设计的体现，是行为的文档
- **调试是反馈回路的艺术**：如果你不能自动验证，你就是在猜
- **架构是熵管理**：深度模块让复杂度有处安放

这些原则，在 AI 出现之前就存在。但 AI 的出现，让我们必须**更严格、更系统化**地执行它们。

因为现在，一个错误的决定，会在几秒钟内被扩散到整个代码库。

---

## 附录：技能速查表

### 工程类技能

| 技能 | 用途 | 触发条件 |
|------|------|----------|
| `/grill-with-docs` | 需求对齐 | 新功能设计前 |
| `/tdd` | 测试驱动开发 | 编码时 |
| `/diagnose` | 调试 | Bug 或性能问题 |
| `/to-prd` | 创建产品需求 | 从对话生成 PRD |
| `/to-issues` | 任务拆分 | 从 PRD 生成任务 |
| `/triage` | 任务管理 | 管理待办事项 |
| `/improve-codebase-architecture` | 架构优化 | 每几天运行 |
| `/zoom-out` | 理解代码 | 不熟悉的代码区域 |
| `/prototype` | 原型验证 | 不确定的设计 |

### 效率类技能

| 技能 | 用途 | 效果 |
|------|------|------|
| `/grill-me` | 快速对齐 | 非 coding 场景 |
| `/caveman` | 极简沟通 | token 降低 75% |
| `/handoff` | 会话交接 | 切换 AI session |
| `/write-a-skill` | 创建新技能 | 扩展技能库 |

---

## 参考资料

- GitHub 仓库：[mattpocock/skills](https://github.com/mattpocock/skills)
- 安装命令：`npx skills@latest add mattpocock/skills`
- Matt Pocock：TypeScript 领域专家，Total TypeScript 创始人
- 相关仓库：[sandcastle](https://github.com/mattpocock/sandcastle)（沙箱化 AI 代理编排）

---

*本文基于 Matt Pocock 的 `skills` 仓库撰写，旨在传播优秀的软件工程实践。仓库采用 MIT 许可证。*