---
title: "OpenCLI：把任意网站变成 CLI —— 让 AI Agent 拥有「命令行级」的互联网操作能力"
description: "从 Chrome 扩展到站点适配器自修复，OpenCLI 如何用工程化手段解决 AI 操控网页的不确定性问题。"
pubDate: 2026-06-02
tags: ["AI Agent", "浏览器自动化", "CLI", "工程实践", "OpenCLI"]
image: "/blog-placeholder-1.jpg"
featured: false
---

## 开篇

如果你用过 Playwright、Puppeteer 或 Selenium 做网页自动化，你一定经历过这种痛苦：

> 网站改了个 class 名，你的选择器全挂了。
> 网站上了反爬，你的脚本被 403 了。
> 网站 SPA 重写了路由，你的 wait 条件失效了。

OpenCLI 的作者 jackwener 做了一件有意思的事：**把 100+ 个网站的常见操作封装成统一 CLI 命令，并且设计了一套完整的"自修复"体系。**

```bash
opencli bilibili hot --limit 5        # B站热榜
opencli zhihu search "第一性原理"     # 知乎搜索
opencli twitter trending              # Twitter 趋势
opencli xiaohongshu note <id>         # 小红书笔记
```

但这只是冰山一角。OpenCLI 真正的野心是：**把任何网站变成确定性接口（deterministic interface），让 AI Agent 能用命令行操作互联网。**

---

## 一、三层架构：适配、操控、编排

OpenCLI 提供三种使用层次：

### 第一层：内置适配器（Adapter）

100+ 个网站的预封装命令，按策略（Strategy）分类：

| 策略 | 是否需要浏览器 | 典型场景 |
|------|---------------|---------|
| `PUBLIC` | 否 | 公开 API，Node.js 直接 `fetch` |
| `COOKIE` | 是 | 需要登录态，通过 Chrome 扩展抓取 Cookie |
| `INTERCEPT` | 是 | 需要拦截签名请求 |
| `UI` | 是 | 完整 DOM 操作 |
| `LOCAL` | 否 | 本地端点 |

关键洞察：**不是每个命令都需要浏览器**。`PUBLIC` 和 `LOCAL` 策略直接走 HTTP，效率最高。只有真正需要登录态或 DOM 交互的命令才走浏览器桥接。

### 第二层：浏览器驱动（Browser Driving）

当没有现成适配器时，`opencli browser` 提供一套结构化的浏览器操控原语：

```bash
opencli browser session open https://example.com
opencli browser session state          # 结构化 DOM 快照，带 [N] 引用
opencli browser session click 3        # 点击第 3 个元素
opencli browser session type 4 "text"  # 在第 4 个元素输入
opencli browser session network        # 拦截网络请求
```

这套命令的设计哲学是：**AI Agent 是第一个读者，不是人类**。每个命令返回结构化信封（envelope），包含匹配置信度、目标数量、错误码——让 Agent 可以基于机器可读的信号做分支决策。

### 第三层：适配器编写与自修复

这是 OpenCLI 最独特的部分——它不仅提供使用方式，还通过 AI Agent Skills 指导 Agent **自己写适配器、自己修复适配器**。

---

## 二、浏览器桥接：用你的已登录 Chrome 操控一切

OpenCLI 的浏览器通信架构很巧妙：

```
Agent → opencli CLI → 本地 Daemon (port 19825)
                      → Chrome 扩展 (Browser Bridge)
                        → 你的已登录 Chrome 页面
```

不需要启动无头浏览器、不需要管理 WebDriver、不需要处理 Chrome 实例。扩展直接桥接到你日常使用的 Chrome——**Cookie、登录态、SSO 全都在**。

Session 生命周期也设计得很精细：

- **Owned session**：CLI 创建的标签，CLI 管理生命周期，有 idle 自动关闭
- **Bound session**：绑定用户已经打开的标签（比如你手动导航到的登录页面），CLI 不关闭标签，只接管操作权
- **Tab 租约**：每个 session 持有标签租约，支持多标签并行操作

`opencli browser bind` 是最实用的命令——你手动在 Chrome 里打开一个已登录的页面，然后 `bind` 把控制权交给 Agent。Agent 可以操作这个页面，但不会关掉它。

---

## 三、站点适配器开发：从侦察到验证的完整流水线

`opencli-adapter-author` skill 是这套系统最硬核的部分。它定义了一个从零到通过 `verify` 的完整流程：

### Step 1：侦察（Site Recon）

先跑 `opencli browser analyze <url>` 一步拿到站点类型、反爬策略、已有适配器推荐和下一步指引。

### Step 2：API 发现

按五种 Pattern 递进搜索：

1. **§1 network**：直接看浏览器发出的网络请求
2. **§2 state**：从页面 hydration state 中抽取
3. **§3 bundle**：搜索 JS bundle 里的 baseURL
4. **§4 token**：追踪认证 token 来源
5. **§5 intercept**：拦截页面自己发出的请求

### Step 3：Strategy 决策（强制产出）

**在写代码之前，必须产出 strategy note**——这是最关键的工程纪律：

```md
Strategy: PUBLIC_API | COOKIE_API | PAGE_FETCH | INTERCEPT | DOM_STATE | UI_SELECTOR
Contract: stable | visible-ui | internal-unstable
Evidence:
- observed request/state: <endpoint / state global / UI-only signal>
- auth source: <none / browser cookie / csrf from meta / localStorage / page runtime>
- replay result: <status + content-type + non-empty sample shape>
```

核心判断标准不是"API 比 DOM 高级"，而是**数据源有没有外部契约**：

| 策略 | 契约级别 | 维护成本 |
|------|---------|---------|
| `PUBLIC_API` / `COOKIE_API` | stable（公开/官方接口） | 最低 |
| `UI_SELECTOR` / `DOM_STATE` | visible-ui（用户可见界面） | 中等 |
| `PAGE_FETCH` / `INTERCEPT` | internal-unstable（内部无契约接口） | 最高，fix 频率是 PUBLIC 的 7-8 倍 |

实测数据非常有说服力：`PAGE_FETCH` / `INTERCEPT` 的修复频率约为 `PUBLIC_API` 的 7-8 倍。而如果 UI/DOM 语义稳定，不应该强行升级到内部接口——**稳定的 UI 选择器可能比无契约的内部 API 更可靠**。

### Step 4：字段解码

字段解码有三层：

1. **自解释** → 直接用 key
2. **已知代号** → 查 `field-conventions.md` 词典
3. **未知代号** → 用 `field-decode-playbook.md`（排序键对比 / 结构差分 / 常量排查）

### Step 5：生成骨架 + 验证

```bash
opencli browser init <site>/<command>   # 生成适配器骨架
opencli browser verify <site>/<command> # 端到端验证
```

验证通过后生成 fixture 种子文件，手动收紧 pattern 和 notEmpty 约束，确保后续站点改版时能第一时间发现。

### Step 6：回写站点记忆

这是整个系统最精妙的设计之一：**每轮回写站点知识**，下次同一个站点的适配从几小时缩短到 5 分钟。

站点记忆存在两层：

- **In-repo**：`references/site-memory/<site>.md`（公共知识）
- **Local**：`~/.opencli/sites/<site>/`（本地缓存：endpoints.json、field-map.json、notes.md、fixtures/）

字段映射采取"只追加不覆盖"策略——已有的 key 不覆盖，有冲突先和网页值对齐再写。这避免了新旧知识互相覆盖导致的回归。

---

## 四、自修复：当适配器挂掉时的自动诊断流程

`opencli-autofix` skill 定义了一个完整的自修复循环：

### 安全边界

修复开始前，先做硬拦截检查：

- `AUTH_REQUIRED`（退出码 77）→ **STOP**，让用户登录，不修改代码
- `BROWSER_CONNECT`（退出码 69）→ **STOP**，让用户跑 `opencli doctor`
- CAPTCHA / 限流 → **STOP**，不是适配器的问题

### "空结果 ≠ 适配器坏了"

这是最常见的误判。`EMPTY_RESULT` 往往不是适配器 bug：

- 平台可能对你的查询做了反爬降级
- 数据在 Chrome 里看得到，适配器返回空 → 认证态问题
- 软 404：网站返回 HTTP 200 + 空 payload，而不是真正的 404
- 搜索返回 0 条结果本身就是一个有效答案

**在开始修复之前，先用替代查询或正常 Chrome 标签排除这些情况。**

### Trace Artifact：修复的证据链

```bash
opencli <site> <command> --trace retain-on-failure 2>trace-error.yaml
```

失败时生成的 trace 包含：

- `summary.md` → LLM 导向的入口，含 front matter（site、command、adapterSourcePath、errorCode）
- `receipt.json` → 机器可读的追踪凭证
- `trace.jsonl` → 完整时间线
- `network.jsonl` → 网络事件
- `state/` → 最终 DOM 快照
- `screenshots/` → 最终截图

修复规则极其严格：

1. **只做最小改动**——只修坏的部分，不顺便重构
2. **保持输出结构不变**——columns 和返回格式必须兼容
3. **优先用 API 替代 DOM 爬取**——如果在探索中发现了 JSON API，切换到它
4. **最多 3 轮修复**——trace → fix → retry，3 轮后停止并报告
5. **绝对不要放松 fixture 来掩盖失败**——fixture 是用来发现回归的，不是用来让 CI 变绿的

修复成功后，自动起草 GitHub issue 提交到上游——**本地的修复要流回主仓库**。

---

## 五、目标定位合约：结构化引用 vs CSS 选择器

OpenCLI 的浏览器命令有一个精心设计的目标定位系统：

```
<target> ::= <numeric-ref> | <css-selector>
```

**数字引用**（来自 `state` 或 `find` 的 `[N]` 索引）是首选——CLI 对每个被标记的元素做了指纹识别，数字引用能在轻度 DOM 漂移中存活。

每次交互返回 `match_level`：

| 级别 | 含义 | 你应该 |
|------|------|--------|
| `exact` | 指纹完全匹配，最多一次软漂移 | 继续 |
| `stable` | 标签 + 强 ID 一致，软信号漂移 | 继续，但如果操作很重要，用 `get value` 验证 |
| `reidentified` | 原始引用消失了，CLI 找到了唯一替代品 | 在继续写操作之前验证 |

结构化错误码也是机器可读的：`not_found`、`stale_ref`、`selector_ambiguous`、`option_not_found`——Agent 应该**分支在 code 上，而不是 message 字符串上**。

还有一个实用的设计：`compound` 字段。日期、下拉、文件上传这些复杂表单控件自带结构化元数据：

```json
{
  "control": "select",
  "current": "United States",
  "options": [
    { "label": "United States", "value": "us", "selected": true }
  ],
  "options_total": 137
}
```

不需要正则解析属性——`current` 永远正确（即使选项列表被截断到 50 条）。

---

## 六、成本意识：Agent 友好的输出预算

OpenCLI 明确设计了成本层级：

| 命令 | 成本 | 使用时机 |
|------|------|---------|
| `state` | 中等（有内部预算限制） | 每次页面首次加载、每次导航后 |
| `find --css` | 小 | 已知选择器时的快速查询 |
| `get text/value` | 极小 | 验证单个字段 |
| `get html --as json` | 中等→巨大 | 需要推理结构时，必须带预算参数 |
| `screenshot` | 大 | 只有视觉内容（验证码、图表）时才用 |
| `network --raw` | 巨大 | 只有在 `--filter` 缩小范围后才用 |

经验法则：**每次页面转换一次 `state`，每次后续查询一次 `find`，每次操作一次 `get/click/type`**。如果你在一个页面上需要 >10 次调用，你可能在爬取而不是在交互——考虑用 `extract` 或 `network`。

---

## 七、CLI Hub：统一入口的哲学

OpenCLI 不只是网站适配器——它还是一个 CLI 中心：

```bash
opencli gh pr list          # 直接透传 gh CLI
opencli docker ps           # 透传 docker
opencli ntn list pages      # 透传 Notion CLI
```

通过 `opencli external register <name>` 可以把任何本地 CLI 注册到 OpenCLI 的发现表面。甚至支持 Electron 桌面应用的 CDP 适配（Cursor、ChatGPT App、Discord 等）。

统一入口的价值在于：**Agent 不需要知道命令是网站适配器、本地 CLI 还是桌面应用**——它只需要 `opencli <name> <command>`。

---

## 八、工程哲学：纪律编码化

通读 OpenCLI 的源码和 Skills 后，我看到的是一套高度自律的工程系统：

1. **Strategy 决策强制产出**——写适配器前必须填写 strategy note，没有这段 note 不要开始写代码
2. **验证先于信任**——站点记忆命中了 endpoint？不能直接写适配器，必须先 fetch 验证（记忆可能过期）
3. **字段值 vs 网页肉眼对比**——verify 通过了不等于数据是对的，11 种静默失败模式（`success-rate-pitfalls.md`）等着你踩
4. **调试产物隔离**——临时 dump 只能落在 `~/.opencli/sites/<site>/fixtures/` 或 `/tmp/`，严禁留在 repo 里污染 PR
5. **Typed Error 分类**——5 类 typed error（ArgumentError / EmptyResultError / CommandExecutionError / AuthRequiredError / TimeoutError），禁止 silent `return []`
6. **JSDOM Fixture 纪律**——有意 commit 进 repo 的测试 HTML 必须按 5 步完成，含 mandatory 空白行收紧 + reverse-validation

这些纪律的共性是：**不信任任何中间状态的"看起来对了"**。verify 能通过但数据是错的——这是 OpenCLI 最反复强调的陷阱。

---

## 九、对 AI Agent 编程的启示

OpenCLI 回答了一个根本问题：**在 AI Agent 操控网页的时代，什么是可靠的工程实践？**

答案是：

- **结构化信封优于屏幕截图**——Agent 需要机器可读的信号，不是像素
- **契约优先于实现**——有外部契约的 API 比无契约的内部接口可靠 7-8 倍
- **自修复优于报告**——失败时不要只报错，收集证据链、定位根因、修复、验证
- **站点记忆优于重新探索**——每轮回写知识，下次从几小时缩短到 5 分钟
- **最小改动优于重构**——修复适配器时只做最小变更，保持输出结构兼容

OpenCLI 不是"让 AI 随便操控网页"——它是**用工程纪律约束 AI 的网页操作**，让不确定性变成可管理、可追踪、可修复的过程。

---

*完整源码：[github.com/jackwener/opencli](https://github.com/jackwener/opencli/)*
