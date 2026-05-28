---
name: astro-blog-optimization
description: Astro 博客全面优化设计方案 - 极简科技风格
metadata:
  type: project
---

# Astro 博客全面优化设计文档

## 项目概述

将 Obelisk Design 博客优化为世界级现代化技术博客，采用极简科技风格（Vercel/Linear 风格参考）。

**优化目标**：
- 视觉与交互体验提升
- 内容阅读体验优化
- SEO 与社交分享增强

**实施策略**：模块化分阶段重构，4 个独立模块逐步完成。

---

## 设计决策记录

### 1. Header/Hero 设计

**选择**：方案 A - 极简透明风格

**设计要点**：
- 透明背景 + backdrop-filter blur
- Logo + 导航链接 + GitHub 图标
- Hero 区域：渐变标题 + 简洁副标题 + 探索按钮
- 保持当前风格，优化细节

**Why**: 用户偏好保留现有风格，改动较小，风险低。

**How to apply**: 微调 Header 组件样式，优化 Hero 区域文案和布局。

---

### 2. 文章页面布局

**选择**：方案 B - 紧凑布局

**设计要点**：
- 内容宽度：720px（更窄，阅读舒适）
- TOC：底部浮动折叠（桌面端右侧圆点进度）
- 阅读进度：右侧圆点式（独特、现代）
- 阅读时间：与日期同行显示

**Why**: 用户偏好独特现代的设计，Linear 风格更符合极简科技定位。

**How to apply**: 重构 BlogPost.astro 布局，新建 TOC 和 ProgressDots 组件。

---

### 3. 代码块设计

**选择**：方案 A - 经典样式

**设计要点**：
- 头部显示文件名/语言
- 复制按钮在头部右侧
- 有边框分隔，层次感强
- VS Code 风格语法高亮

**Why**: 用户偏好信息完整的显示方式，便于理解代码上下文。

**How to apply**: 创建 CodeBlock 组件，配置 Shiki 自定义主题。

---

### 4. 博客列表设计

**选择**：方案 A - 大卡片布局

**设计要点**：
- Featured 文章：大卡片 + 图片 + 完整信息
- 普通文章：网格布局（2列）
- 卡片信息：标签 + 标题 + 描述 + 日期 + 阅读时间
- Hover 效果：上移 + 边框高亮

**Why**: 用户偏好视觉丰富的布局，Featured 突出显示。

**How to apply**: 重构 blog/index.astro，优化卡片组件样式。

---

## 功能清单

### 模块 1：视觉基础与动画

| 功能 | 说明 | 文件 |
|------|------|------|
| View Transitions | 页面切换平滑动画 | astro.config.mjs |
| Header 优化 | 极简透明风格微调 | Header.astro |
| Footer 优化 | 更精致简洁设计 | Footer.astro |
| Hero 优化 | 渐变标题 + 简洁描述 | index.astro |
| 动画系统 | 悬停、过渡效果 | animations.css |

### 模块 2：文章阅读体验

| 功能 | 说明 | 文件 |
|------|------|------|
| 目录 TOC | 底部浮动折叠 | article/TOC.astro |
| 阅读进度 | 右侧圆点式 | article/ProgressDots.astro |
| 代码复制 | 头部复制按钮 | article/CopyButton.astro |
| 阅读时间 | 与日期同行显示 | article/ReadingTime.astro |
| 文章布局 | 720px 宽度 + 底部 TOC | BlogPost.astro |

### 模块 3：增强功能

| 功能 | 说明 | 文件 |
|------|------|------|
| 相关文章 | 基于标签推荐 | article/RelatedPosts.astro |
| 代码高亮 | Shiki 自定义主题 | syntax.css |
| 博客列表 | Featured + 网格布局 | blog/index.astro |

### 模块 4：SEO 与分享

| 功能 | 说明 | 文件 |
|------|------|------|
| OG 图片生成 | satori 方案 | seo/OGImage.astro |
| 结构化数据 | 更丰富的 JSON-LD | BaseHead.astro |
| 社交分享 | Twitter/OG 完善 | BaseHead.astro |

---

## 文件结构变化

```
src/
├── components/
│   ├── ui/              # 新增
│   │   └── ProgressBar.astro
│   ├── article/         # 新增
│   │   ├── TOC.astro
│   │   ├── ProgressDots.astro
│   │   ├── CodeBlock.astro
│   │   ├── CopyButton.astro
│   │   ├── ReadingTime.astro
│   │   └── RelatedPosts.astro
│   ├── seo/             # 新增
│   │   └── OGImage.astro
│   ├── Header.astro     # 优化
│   ├── Footer.astro     # 重构
│   ├── BaseHead.astro   # 增强
│   └── FormattedDate.astro  # 增强
├── styles/
│   ├── global.css       # 微调
│   ├── animations.css   # 新增
│   ├── prose.css        # 新增（可选）
│   └── syntax.css       # 新增
├── layouts/
│   └── BlogPost.astro   # 重构
├── pages/
│   ├── index.astro      # Hero 优化
│   └── blog/
│       └── index.astro  # 重构
└── content.config.ts    # 增强（阅读时间计算）
```

---

## 技术选型

| 功能 | 技术 | 说明 |
|------|------|------|
| View Transitions | Astro 内置 | `transition:animate` |
| 动画 | CSS + Motion One | Motion One 可选，轻量 |
| TOC | 自建组件 | 提取 h2/h3 标题 |
| 代码高亮 | Shiki | Astro 内置，自定义主题 |
| OG 图片 | satori | HTML to PNG，无需浏览器 |
| 相关文章 | Content Collections | 基于标签匹配 |

**新增依赖**（可选）：
- `motion` - Motion One 动画库（轻量）
- `satori` - OG 图片生成
- `sharp` - 已有，用于图片处理

---

## 性能目标

| 指标 | 目标 | 当前预估 |
|------|------|----------|
| Lighthouse Performance | 95+ | 预计可达 |
| LCP | < 2.5s | 预计可达 |
| CLS | < 0.1 | 预计可达 |
| JS Bundle | < 50KB | View Transitions + Motion One ~20KB |

**优化策略**：
- 静态生成，零运行时
- View Transitions 使用浏览器原生 API
- Motion One 仅在需要时加载
- 图片使用 Astro Image 优化

---

## SEO 目标

| 功能 | 实现 |
|------|------|
| JSON-LD | BlogPosting + Organization + WebSite |
| OG 图片 | 自动生成，含标题+标签+Logo |
| Canonical | 已有，保持 |
| Sitemap | 已有，保持 |
| RSS | 已有，保持 |

---

## 实施计划

### 预估工作量

| 模块 | 时间 | 优先级 |
|------|------|--------|
| 模块 1：视觉基础 | 2-3 小时 | P0 |
| 模块 2：阅读体验 | 3-4 小时 | P0 |
| 模块 3：增强功能 | 2-3 小时 | P1 |
| 模块 4：SEO | 1-2 小时 | P1 |

**总计**：8-12 小时

### 执行顺序

1. **模块 1** → 基础视觉体验
2. **模块 2** → 核心阅读功能
3. **模块 3** → 增强体验
4. **模块 4** → SEO 完善

每个模块完成后独立提交验证。

---

## 相关记忆

- [[user-preference-visual-style]] - 用户偏好极简科技风格
- [[user-preference-article-layout]] - 用户偏好紧凑布局、底部 TOC