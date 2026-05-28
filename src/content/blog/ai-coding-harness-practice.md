---
title: 从 Prompt 到 Harness：AI Coding 的工程治理实践
pubDate: 2025-05-20
description: 如何让 AI 从"会写代码"进化到"持续稳定地写出符合项目规范的代码"——Skills、DSL 中间层、三角验证与 Development Harness 的完整实践路径。
heroImage: '../../assets/ai-coding-harness-hero.webp'
tags: ["AI Coding", "工程治理", "Claude Code", "Skills", "Harness"]
---

## 开篇：一个前端工程师的真实困境

"一开始，我只是想让 Claude Code 帮我写代码。"

我是一个使用 Vue2 和 ElementUI 的前端，主要负责数据治理平台、中后台系统开发。刚开始接触 Claude Code 时，最大的感受只有一句话：

> "卧槽，真强。"

生成页面、补逻辑、写 CRUD、改样式……速度远超手写。

但很快，问题开始出现：

- AI 改代码改着改着，我开始看不懂了
- 它越写越不像我们的项目
- 它会重复造轮子，自己重新封装 table
- 它会忽然写出 Vue3 风格代码
- 有时候很懂项目，有时候又像刚学前端的新手

最痛苦的不是"AI 不会写"，而是：**"AI 有时候会，有时候不会。"**

于是我意识到：问题可能不是模型能力，而是——**AI 根本不知道什么叫"我们团队的规范"。**

---

## 第一层：问题的本质

### Prompt 的局限性

Prompt 是**瞬时的、碎片化**的"散沙"，高度依赖个人表达与单次上下文。

它的痛点在于：
- **缺乏一致性**：同样的需求，不同时间问，输出不同
- **无法资产化**：Prompt 不存在于代码库，无法传承
- **难以维持标准**：大型工程中，无法保证统一的技术规范

核心观点：

> **Prompt 解决的是"怎么做"的问题；Skill 解决的是"怎么做得符合标准"的问题。**
> **Prompt 最大的问题，不是写得不够好，而是无法保证"下一次还这样做"。**

---

## 第二层：什么是 Skill？（工程化定义）

Skill 的本质：一个**封装了环境感知、工具权限与输出约束**的标准化能力单元。

### 核心价值：确定性 (Determinism)

| 约束类型 | 解决的问题 |
|---------|-----------|
| Schema 约束 | 锁定入参/出参，拒绝 AI 的"参数幻觉" |
| 工具锚定 | 让 AI 访问真实数据（GitLab/Yapi/Zentao），而非概率预测 |
| 资产化 | 将团队经验固化为代码库资产（如 `CLAUDE.md`） |

### Claude Code 的明星 Skills

- **skills creator**：通过对话实时沉淀新流程，把一次性 Prompt 固化为长期能力
- **find skills**：能力发现引擎，解决"功能边界模糊"问题
- **gstack**：把项目结构、文档、规范组织成 AI 更容易理解的环境
- **superpowers**：全局能力增强，核心目标是"让 AI 更懂项目"

---

## 第三层：DSL 中间层——为什么 AI Coding 需要它？

一开始，我也尝试过：设计稿截图 → AI 直接生成代码。

理论上看起来合理，因为大模型已经具备：
- UI 识别能力
- OCR 能力
- 页面理解能力
- 代码生成能力

于是 AI 看着设计稿，确实"能生成"。但问题很快就出现：

| 问题类型 | 具体表现 |
|---------|---------|
| 字段遗漏 | 必填字段缺失 |
| 顺序错误 | 表格列顺序不一致 |
| API 不一致 | 参数命名风格漂移 |
| 级联理解错误 | 父子关系搞反 |
| 命名漂移 | fieldName → fieldNmae |

更麻烦的是：这些问题很多不是"代码报错"，而是"看起来差不多，但其实已经偏了"。

### DSL 的本质：AI Coding 的 IR（中间表示层）

类比传统编译器：

```
源码 → AST → IR → Machine Code
```

AI Coding：

```
设计稿 → DSL → Code → Review
```

DSL 不只是为了"生成代码"，更是为了**把设计意图结构化**。让 AI：
- 不再依赖猜测
- 不再只靠视觉识别
- 不再只靠上下文记忆

而是：
- 基于结构化语义生成
- 基于约束生成
- 基于可验证数据生成

---

## 第四层：三角交叉验证——阻断错误传播链

### 为什么单链路验证不够？

如果 DSL 在 OCR/视觉识别阶段误识别了：`fieldName` → `fieldNmae`

随后代码生成阶段，AI 又完全忠实地实现了 DSL：
```javascript
formData.fieldNmae  // 跟着 DSL 错了
```

这时候：DSL ↔ Code = PASS（彼此一致）

但问题是：**它们一起错了。**

这是最危险的情况——AI 最大的问题是"两者都错，但彼此一致"。

### 三角验证的原理

```
        Modao（设计源）
           ↑
          / \
         /   \
        /     \
     Code ←→ DSL
```

三条验证链：

| 验证层 | 对比对象 | 作用 |
|-------|---------|------|
| L2 | DSL ↔ Code | 验证代码是否正确实现 DSL |
| L2.5 | DSL ↔ Modao | 验证 DSL 是否正确理解设计 |
| L3 | Code ↔ Modao | 验证最终页面是否符合设计 |

### 交叉验证场景诊断

| 场景 | DSL↔Code | Code↔Modao | DSL↔Modao | 诊断 |
|-----|----------|-----------|----------|------|
| DSL正确，Code正确 | PASS | PASS | PASS | ✅ 全部正确 |
| DSL正确，Code错误 | FAIL | FAIL | PASS | Code生成阶段出错 |
| DSL错误，Code跟随 | PASS | FAIL | FAIL | DSL识别阶段出错 |
| DSL错误，Code修正 | FAIL | PASS | FAIL | DSL错误但人工修正 |

### 核心价值

> 三角验证真正解决的不是"有没有错误"，而是：**错误终于开始"可溯源"。**

以前只能知道"页面错了"，现在可以区分：
- DSL 生成错误 → 重生成 DSL
- Code 生成错误 → 修代码
- 视觉实现错误 → 调整样式
- DSL 已被人工修复 → 回写 DSL

---

## 第五层：Development Harness——工程级约束体系

### 为什么需要 Harness？

几个真实事故：

**事故 1：AI 偷偷重构公共分页逻辑**

AI 觉得公共分页"不够优雅"，于是：
- 自己重新实现分页
- 自己管理 current/pageSize
- 自己封装请求状态

看起来代码挺"高级"，但统一分页行为不一致了。

**事故 2：AI 在 Vue2 项目里写 Vue3**

AI 开始使用 Composition API、setup()、ref/reactive……甚至"半 Vue2 半 Vue3 混写"。

**事故 3：AI 疯狂重复造轮子**

项目已有 CompanyProTable、公共搜索组件、标准 request 封装，但 AI 还是会新封装一遍。

**事故 4：CSS 反复试错**

AI 调整 el-select 下拉菜单宽度，试了 4 轮：`::v-deep` → `/deep/` → important → 换选择器……

最后才发现根因：**el-select 的下拉菜单是通过 portal 挂载到 `<body>` 的，scoped 样式穿透不到。**

AI 不是"写错代码"，而是"用错误的方式猜正确答案"——这比直接写错更危险。

### Pattern Drift（模式漂移）

AI 会发生模式漂移：
- 一开始参考项目代码
- 后来开始参考自己生成的代码
- 最终逐渐偏离整个工程体系

最危险的是：AI 不一定会立刻写错，但它会在你没察觉的时候，慢慢破坏工程一致性。

---

## 第六层：Harness 的结构设计

```
.claude/
├── CLAUDE.md
├── settings.json
├── harness/
│   ├── README.md
│   ├── index.md
│   ├── rules/       # 硬规则：Vue2 编码规范、API 模式、命名规范
│   ├── specs/       # 架构说明：组件模式、Vuex 模式、路由模式
│   ├── risk/        # 高风险模块：SSE 流处理、工作流编辑器
│   ├── checklists/  # 任务自查清单：新增模块、API 改动
│   └── templates/   # 标准脚手架：页面模板、API 模板
```

### 分层风险防护

| 层级 | 机制 | 作用 |
|-----|------|------|
| Tier 1 | CLAUDE.md 警告 | 会话启动即提醒 |
| Tier 2 | harness/risk | 详细风险说明 |
| Tier 3 | checklists | 强制任务检查 |
| Tier 4 | 源码内联注释 | 打开文件即警告 |

源码内联注释示例：

```javascript
/*
 * [HARNESS-RISK] workflow-editor.vue
 * Loop detection is COMMENTED OUT
 * do NOT re-enable
 * See harness/risk/high-risk-modules.md
 */
```

### Checklist：将 Review 前置

```markdown
## 新增模块 Checklist
- [ ] 检查是否已有同类模块
- [ ] 检查是否已有 domain API
- [ ] 是否复用标准分页
- [ ] 是否复用 CompanyProTable
- [ ] 是否统一 request
```

---

## 第七层：Harness 的现实问题

### 问题 1：慢

每次开发任务，AI 不会直接写代码，而是：
1. 先读 `index.md`
2. 再读 `checklists/`
3. 如果涉及高风险模块，读 `risk/`
4. 读 `rules/`
5. 读 `specs/`

**真正写代码之前，AI 已经花了好几轮在"读文件"上。**

### 问题 2：context 消耗

每个文件都占上下文窗口。规则越多、文件越多，留给实际对话的空间就越少。

### 问题 3：膨胀

当 Harness 文件本身也在增长（新规则、新风险点），这个膨胀怎么控制？

---

## 第八层：AI 时代程序员角色的变化

以前，程序员最重要的是：
- 写代码
- 实现需求
- 调接口
- 修 Bug

现在，真正重要的能力变成：
- 定义规则
- 设计 Guardrails
- 管理上下文
- 沉淀工程模式
- 约束 AI 输出
- 控制架构熵增

以前是"人写代码"，现在越来越像"人管理代码生成系统"。

### Review 的重心变化

以前 Review：
- 看实现细节
- 看代码风格
- 看逻辑是否正确

现在 Review：
- 检查 Guardrails
- 检查 Pattern Alignment
- 检查领域边界
- 检查是否复用已有能力
- 检查是否破坏工程一致性

以前 Review 的对象是"代码"，现在越来越变成"代码生成体系"。

---

## 第九层：AI 工程化的四个阶段

### 第一阶段：个人增强

核心目标："让 AI 开始像你。"

重点：
- 建立 `CLAUDE.md`
- 建立 Golden Samples
- 固定技术栈规则
- 固定页面模式

### 第二阶段：团队规范

核心目标："让 AI 开始像团队。"

重点：
- 建立 Guardrails
- 建立 Checklist
- 建立 Pattern Injection
- 建立风险约束

### 第三阶段：工程体系

核心目标："让 AI 开始像组织。"

重点：
- 引入 Harness
- 建立 Risk Layer
- 建立 Domain Skills
- 建立 Routing

### 第四阶段：组织级 AI 工程化

核心目标："让 AI 成为研发基础设施的一部分。"

重点：
- MCP
- 多仓库上下文
- Skill 平台化
- AI Workflow
- Agent 协同

---

## 总结：从工具到资产

> "如果你维护一个长达三年的数据平台，最可怕的是什么？"

答案是：**"逻辑的腐烂与共识的消失。"**

我们今天沉淀的每一个 Skill，都不只是为了提效，而是为了：**将团队经验固化为数字资产。**

未来团队真正的竞争力，不在于"谁写代码更快"，而在于：**"谁拥有更成熟的 AI 工程体系。"**

---

## 关键要点回顾

1. **Prompt → Skill → Harness** 是必然演进路径
2. **DSL 中间层** 让 AI 输出可量化、可验证、可追溯
3. **三角交叉验证** 阻断错误传播链，让错误可溯源
4. **Harness** 是工程级约束体系，解决长期一致性问题
5. **程序员角色** 正在从"写代码"转向"管理代码生成系统"