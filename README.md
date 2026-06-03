# Obelisk Design Blog

> 从原理到实践，深入探索 AI 与工程的世界。

🌐 **在线地址**：[obelisk-design.github.io/blog](https://obelisk-design.github.io/blog/)
🌐 **在线地址**：[43.153.156.249:8080](http://43.153.156.249:8080/)

## 关于

这是一个用 [Astro](https://astro.build) 构建的个人技术博客，专注于以下主题：

- **AI Agent 工程化** — 从 LLM 到 Agent 的范式转变、编排模式、工具调用、RAG
- **AI 开发工具生态** — Claude Code、Cursor、Codex、MCP、v0 等工具的深度解析与实战
- **技术前沿追踪** — 每日从 Dev.to、Hacker News、GitHub Trending 自动筛选、AI 分析、中文编译
- **工程方法论** — 架构设计、中间层实践、CLI 到 Agent 的工作流演进

所有文章均为中文，目标读者是有一定技术背景但对 AI 领域持续好奇的开发者。

## 技术栈

| 组件 | 技术 |
|------|------|
| 框架 | Astro 4.x |
| 内容 | Markdown + MDX (Content Collections) |
| 样式 | 自定义 CSS (深色科技风) |
| 字体 | Atkinson Hyperlegible (本地托管) |
| 构建 | pnpm + GitHub Actions |
| 部署 | GitHub Pages + 本地 nginx (双通道) |
| SEO | Sitemap + JSON-LD + Open Graph + robots.txt |

## 自动化 Pipeline

博客内容通过两套自动化系统生成并发布：

### 1. 技术日报 (Tech Daily Digest)

- 定时从 Dev.to、Hacker News、GitHub Trending 抓取 AI 相关内容
- 7 天去重，过滤已发布内容
- AI 按渠道独立生成中文点评文章
- 每天最多 3 篇（每渠道 1 篇）
- 推送至 `dev-blog` 分支，每日 17:00 自动合并到 `main` 触发部署

### 2. 微信文章处理

- 用户发送微信文章链接 → 抓取 → AI 深度拓展写作
- 目标篇幅：源材料的 3-5 倍深度
- 交叉引用业界实践，补充历史脉络与工程洞察

## 项目结构

```
├── .github/workflows/
│   └── deploy.yml          # GitHub Actions 构建部署
├── public/                  # 静态资源 (favicon, robots.txt, manifest)
├── src/
│   ├── assets/             # 图片、字体
│   ├── components/         # Astro 组件
│   ├── content/blog/       # 博客文章 (Markdown/MDX)
│   ├── layouts/            # 页面布局
│   ├── pages/              # 路由页面
│   └── styles/             # 全局样式
├── astro.config.mjs        # Astro 配置
└── package.json
```

## 本地开发

```bash
# 安装依赖
pnpm install

# 启动开发服务器 (localhost:4321)
pnpm run dev

# 生产构建
pnpm run build
```

## 分支策略

| 分支 | 用途 |
|------|------|
| `main` | 生产分支，GitHub Pages 从此构建部署 |
| `dev-blog` | 日常内容推送，每日 17:00 自动合并到 `main` |

## License

MIT
