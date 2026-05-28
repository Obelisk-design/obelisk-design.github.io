---
title: 'OpenCLI：把任意网站变成 CLI，让 AI Agent 操作你的浏览器'
description: 'OpenCLI 是一个强大的工具，可以将任何网站转换为 CLI 命令，并让 AI Agent 通过你已登录的浏览器进行自动化操作。支持 100+ 网站适配器。'
pubDate: '2026-05-19'
heroImage: '../../assets/opencli-hero.webp'
tags: ["AI", "CLI", "Browser", "Agent", "自动化", "开源"]
---

## 什么是 OpenCLI？

OpenCLI 是一个开源项目，可以：

- **把任意网站变成 CLI 命令**
- **让 AI Agent 操作你已登录的浏览器**
- **将网站、浏览器会话、Electron 应用转换为确定性接口**

GitHub: https://github.com/jackwener/opencli
官网: https://opencli.info/

---

## 核心功能

### 1. 内置适配器（100+ 网站）

支持 Bilibili、知乎、小红书、Reddit、HackerNews、Twitter/X 等众多网站：

```bash
opencli hackernews top --limit 5
opencli bilibili hot --limit 5
opencli zhihu hot
opencli xiaohongshu search "关键词"
```

### 2. AI Agent 浏览器操作

安装 `opencli-browser` skill 后，AI Agent 可以：

| 操作 | 说明 |
|------|------|
| Navigate | 导航到任意 URL |
| Read | 通过 DOM 快照读取页面内容 |
| Interact | 点击按钮、填写表单、选择选项 |
| Extract | 提取数据或拦截 API 响应 |
| Wait | 等待元素、文本或页面过渡 |

### 3. CLI Hub（本地工具整合）

统一调用现有的命令行工具：

```
gh · docker · vercel · wrangler · obsidian · notion · discord · telegram
```

### 4. 桌面应用适配器

通过 CDP 支持 Electron 应用：
- Cursor / Codex / Antigravity / ChatGPT App / ChatWise / Discord / Doubao

---

## 快速开始

### 安装

```bash
# 需要 Node.js >= 20
npm install -g @jackwener/opencli
```

### 安装浏览器扩展

**推荐方式：Chrome Web Store**
安装 "OpenCLI" 扩展

**手动安装：**
1. 从 GitHub Releases 下载扩展 zip 文件
2. 解压后，打开 `chrome://extensions`
3. 启用开发者模式，点击"加载已解压的扩展程序"

### 验证

```bash
opencli doctor
```

### 运行命令

```bash
opencli list                 # 显示所有注册命令
opencli hackernews top --limit 5
opencli bilibili hot --limit 5
```

---

## 为 AI Agent 安装 Skills

```bash
npx skills add jackwener/opencli
```

或单独安装：

```bash
npx skills add jackwener/opencli --skill opencli-browser      # 浏览器操作
npx skills add jackwener/opencli --skill opencli-adapter-author  # 编写适配器
npx skills add jackwener/opencli --skill opencli-autofix      # 修复适配器
npx skills add jackwener/opencli --skill opencli-usage        # 命令参考
```

### Skills 用途

| Skill | 使用场景 | 示例 |
|-------|---------|------|
| **opencli-adapter-author** | 为新网站编写适配器 | "为抖音热点写个适配器" |
| **opencli-autofix** | 修复失效的适配器 | "知乎 hot 返回空了，修一下" |
| **opencli-browser** | 实时操作浏览器页面 | "帮我检查小红书通知" |
| **opencli-usage** | 命令和站点参考 | "OpenCLI 有哪些 Twitter 命令？" |

---

## 编写新适配器

当需要的网站尚未支持时，使用 `opencli-adapter-author` skill：

1. **侦察网站**：识别模式（SPA / SSR / JSONP / Token / Streaming）
2. **发现端点**：网络检查、初始状态、bundle 搜索、token 追踪
3. **选择认证方式**：PUBLIC / COOKIE / INTERCEPT / UI / LOCAL
4. **解码响应字段**：设计输出列
5. **验证**：`opencli browser recon verify <site>/<name>`

适配器持久化到 `~/.opencli/sites/<site>/`

---

## 浏览器命令详解

```bash
opencli browser <session> open <url>     # 打开页面
opencli browser <session> state          # 获取页面状态
opencli browser <session> click <selector>  # 点击元素
opencli browser <session> type <selector> <text>  # 输入文本
opencli browser <session> fill <selector> <value>  # 填充表单
opencli browser <session> extract <selector>  # 提取数据
opencli browser <session> screenshot     # 截图
opencli browser <session> scroll <direction>  # 滚动
opencli browser <session> wait <selector>  # 等待元素
```

Tab 管理：

```bash
opencli browser <session> tab list       # 列出所有 tab
opencli browser <session> tab new [url]  # 新建 tab
opencli browser <session> tab select <id>  # 选择 tab
opencli browser <session> tab close <id>  # 关闭 tab
```

---

## 配置选项

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `OPENCLI_DAEMON_PORT` | 19825 | daemon-extension 桥接端口 |
| `OPENCLI_PROFILE` | — | Chrome profile 别名 |
| `OPENCLI_BROWSER_CONNECT_TIMEOUT` | 30 | 浏览器连接等待秒数 |
| `OPENCLI_BROWSER_COMMAND_TIMEOUT` | 60 | 单命令等待秒数 |
| `OPENCLI_CDP_ENDPOINT` | — | 远程浏览器或 Electron CDP 端点 |

---

## 项目数据

| 指标 | 数据 |
|------|------|
| ⭐ Stars | **22,523** |
| 🔀 Forks | **2,265** |
| 📜 License | Apache 2.0 |
| 💻 Language | JavaScript |
| 📦 npm | `@jackwener/opencli` |

---

## 为什么选择 OpenCLI？

1. **确定性自动化**：不是截图猜测，而是结构化 DOM 快照
2. **已登录浏览器**：使用你的真实登录状态，无需处理认证
3. **AI Agent 集成**：直接对接 Claude Code、Cursor 等 AI 编程工具
4. **100+ 内置适配器**：覆盖主流中文和英文平台
5. **开源可扩展**：Apache 2.0 许可，自由编写自定义适配器

---

## 适用场景

- 🤖 **AI Agent 自动化**：让 AI 操作浏览器完成任务
- 📊 **数据抓取**：从各种平台提取结构化数据
- 🔧 **CLI 整合**：统一管理本地命令行工具
- 🖥️ **桌面应用自动化**：自动化 Electron 应用
- ✍️ **适配器开发**：快速为新网站编写 CLI 命令

---

## 总结

OpenCLI 是连接 **AI Agent** 和 **真实浏览器** 的桥梁。它让 AI 不只能"说"，还能"做"——通过你的已登录浏览器完成实际操作。

对于 AI Agent 开发者和自动化爱好者来说，这是一个不可多得的工具。

**立即体验：**

```bash
npm install -g @jackwener/opencli
opencli doctor
opencli hackernews top --limit 5
```