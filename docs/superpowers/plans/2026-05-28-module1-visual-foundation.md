# Astro 博客优化 - 模块 1：视觉基础与动画

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 Astro 博客添加 View Transitions 和优化视觉基础组件

**Architecture:** 使用 Astro 内置 View Transitions API 实现页面切换动画，优化 Header/Footer/Hero 组件样式，新建动画系统 CSS 文件

**Tech Stack:** Astro 6.x, CSS, View Transitions API

---

## 文件结构

| 文件 | 操作 | 说明 |
|------|------|------|
| `astro.config.mjs` | 修改 | 添加 View Transitions 配置 |
| `src/styles/animations.css` | 新建 | 动画系统 |
| `src/components/Header.astro` | 修改 | 微调样式 |
| `src/components/Footer.astro` | 重构 | 精致简洁设计 |
| `src/pages/index.astro` | 修改 | Hero 区域优化 |
| `src/styles/global.css` | 修改 | 引入 animations.css |

---

## Task 1: 配置 View Transitions

**Files:**
- Modify: `astro.config.mjs`

- [ ] **Step 1: 安装 View Transitions 包**

```bash
npm install @astrojs/view-transitions
```

- [ ] **Step 2: 在 astro.config.mjs 中添加配置**

修改 `astro.config.mjs`，添加 View Transitions 集成：

```javascript
// @ts-check

import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import viewTransitions from '@astrojs/view-transitions';
import { defineConfig, fontProviders } from 'astro/config';

// https://astro.build/config
export default defineConfig({
  site: 'https://obelisk-design.github.io',
  integrations: [
    mdx(),
    sitemap({
      i18n: {
        defaultLocale: 'zh',
        locales: {
          zh: 'zh-CN',
        },
      },
    }),
    viewTransitions(),
  ],
  fonts: [
    // ... 保持原有字体配置
  ],
});
```

- [ ] **Step 3: 在 BaseHead.astro 中添加 View Transitions 标签**

修改 `src/components/BaseHead.astro`，在 `<head>` 部分添加：

```astro
---
// ... 现有代码
---

<!-- Global Metadata -->
<meta charset="utf-8" />
<!-- ... 其他 meta 标签 -->

<!-- View Transitions -->
<meta name="view-transition" content="same-origin" />

<!-- ... 其余代码保持不变 -->
```

- [ ] **Step 4: 构建验证**

```bash
npm run build
```

Expected: 构建成功，无错误

- [ ] **Step 5: 提交**

```bash
git add astro.config.mjs src/components/BaseHead.astro package.json package-lock.json
git commit -m "feat: add View Transitions support for smooth page navigation"
```

---

## Task 2: 创建动画系统 CSS

**Files:**
- Create: `src/styles/animations.css`
- Modify: `src/styles/global.css`

- [ ] **Step 1: 创建 animations.css**

新建 `src/styles/animations.css`：

```css
/*
  Animation System
  Smooth, subtle animations for premium feel
*/

/* View Transitions - Page fade */
::view-transition-old(root),
::view-transition-new(root) {
  animation-duration: 0.3s;
  animation-timing-function: ease-in-out;
}

::view-transition-old(root) {
  animation-name: fade-out;
}

::view-transition-new(root) {
  animation-name: fade-in;
}

@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fade-out {
  from {
    opacity: 1;
  }
  to {
    opacity: 0;
  }
}

/* Hover lift effect */
.hover-lift {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.hover-lift:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

/* Smooth color transitions */
.transition-colors {
  transition: color 0.2s ease, background-color 0.2s ease, border-color 0.2s ease;
}

/* Link hover glow */
.link-glow:hover {
  text-shadow: 0 0 8px rgba(0, 212, 255, 0.3);
}

/* Card border highlight */
.card-highlight {
  transition: border-color 0.2s ease, transform 0.2s ease;
}

.card-highlight:hover {
  border-color: rgba(0, 212, 255, 0.3);
}

/* Button press effect */
.btn-press:active {
  transform: scale(0.98);
}

/* Skeleton loading pulse */
@keyframes skeleton-pulse {
  0%, 100% {
    opacity: 0.4;
  }
  50% {
    opacity: 0.8;
  }
}

.skeleton {
  animation: skeleton-pulse 1.5s ease-in-out infinite;
}

/* Mobile touch feedback */
@media (max-width: 768px) {
  .hover-lift:hover {
    transform: none;
    box-shadow: none;
  }

  .hover-lift:active {
    transform: scale(0.98);
  }
}
```

- [ ] **Step 2: 在 global.css 中引入 animations.css**

修改 `src/styles/global.css`，在文件顶部添加导入：

```css
/*
  Obelisk Design Theme
  Dark, minimal, tech-inspired
*/

@import './animations.css';

:root {
  /* ... 保持原有变量 */
}
```

- [ ] **Step 3: 构建验证**

```bash
npm run build
```

Expected: 构建成功，CSS 无错误

- [ ] **Step 4: 提交**

```bash
git add src/styles/animations.css src/styles/global.css
git commit -m "feat: add animation system with View Transitions and hover effects"
```

---

## Task 3: 优化 Header 组件

**Files:**
- Modify: `src/components/Header.astro`

- [ ] **Step 1: 微调 Header 样式**

修改 `src/components/Header.astro` 的 `<style>` 部分，添加动画过渡：

```astro
---
import { SITE_TITLE } from '../consts';
import HeaderLink from './HeaderLink.astro';
---

<header>
  <nav transition:animate="slide">
    <div class="logo">
      <a href="/">
        <span class="logo-text">{SITE_TITLE}</span>
      </a>
    </div>
    <div class="nav-links" id="nav-links">
      <HeaderLink href="/">首页</HeaderLink>
      <HeaderLink href="/blog">博客</HeaderLink>
      <HeaderLink href="/about">关于</HeaderLink>
    </div>
    <div class="nav-right">
      <div class="social-links">
        <a href="https://github.com/Obelisk-design" target="_blank" aria-label="GitHub">
          <svg viewBox="0 0 16 16" width="20" height="20" fill="currentColor">
            <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
          </svg>
        </a>
      </div>
      <button class="menu-toggle" id="menu-toggle" aria-label="菜单">
        <span></span>
        <span></span>
        <span></span>
      </button>
    </div>
  </nav>
</header>

<script>
  const toggle = document.getElementById('menu-toggle');
  const navLinks = document.getElementById('nav-links');

  toggle.addEventListener('click', () => {
    toggle.classList.toggle('open');
    navLinks.classList.toggle('open');
    document.body.style.overflow = navLinks.classList.contains('open') ? 'hidden' : '';
  });

  navLinks.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      toggle.classList.remove('open');
      navLinks.classList.remove('open');
      document.body.style.overflow = '';
    });
  });
</script>

<style>
  header {
    position: sticky;
    top: 0;
    z-index: 100;
    backdrop-filter: blur(12px);
    background: rgba(10, 14, 23, 0.85);
    border-bottom: 1px solid var(--border);
    transition: background 0.2s ease;
  }

  nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    max-width: 1000px;
    margin: 0 auto;
    padding: 0.75rem 1.5rem;
  }

  .logo a {
    display: flex;
    align-items: center;
    color: var(--text-primary);
    font-weight: 600;
    transition: color 0.2s ease;
  }

  .logo-text {
    font-size: 1rem;
    letter-spacing: -0.02em;
  }

  .logo a:hover {
    color: var(--accent);
  }

  .nav-links {
    display: flex;
    gap: 0.5rem;
  }

  .nav-right {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .social-links {
    display: flex;
    gap: 0.5rem;
  }

  .menu-toggle {
    display: none;
  }

  .social-links a {
    color: var(--text-muted);
    padding: 0.5rem;
    border-radius: 6px;
    transition: all 0.2s ease;
  }

  .social-links a:hover {
    color: var(--accent);
    background: var(--bg-card);
  }

  /* Mobile styles - 保持原有 */
  @media (max-width: 768px) {
    nav {
      padding: 0.75rem 1rem;
    }

    .nav-links {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(10, 14, 23, 0.98);
      flex-direction: column;
      justify-content: center;
      align-items: center;
      gap: 1.5rem;
      z-index: 200;
      opacity: 0;
      visibility: hidden;
      transition: opacity 0.3s ease, visibility 0.3s ease;
    }

    .nav-links.open {
      opacity: 1;
      visibility: visible;
    }

    .nav-links a {
      font-size: 1.25rem;
      padding: 1rem 1.5rem;
      min-height: 48px;
      display: inline-block;
    }

    .social-links {
      display: none;
    }

    .menu-toggle {
      display: flex;
      flex-direction: column;
      gap: 5px;
      background: none;
      border: none;
      cursor: pointer;
      padding: 0.75rem;
      z-index: 300;
      min-width: 48px;
      min-height: 48px;
      touch-action: manipulation;
    }

    .menu-toggle span {
      display: block;
      width: 24px;
      height: 2px;
      background: var(--text-primary);
      transition: all 0.3s ease;
      margin: 0 auto;
    }

    .menu-toggle.open span:nth-child(1) {
      transform: rotate(45deg) translate(5px, 5px);
    }

    .menu-toggle.open span:nth-child(2) {
      opacity: 0;
    }

    .menu-toggle.open span:nth-child(3) {
      transform: rotate(-45deg) translate(5px, -5px);
    }
  }
</style>
```

- [ ] **Step 2: 构建验证**

```bash
npm run build
```

Expected: 构建成功

- [ ] **Step 3: 提交**

```bash
git add src/components/Header.astro
git commit -m "feat: enhance Header with View Transitions and smooth hover effects"
```

---

## Task 4: 重构 Footer 组件

**Files:**
- Modify: `src/components/Footer.astro`

- [ ] **Step 1: 重构 Footer 样式**

修改 `src/components/Footer.astro`：

```astro
---
const today = new Date();
---

<footer transition:animate="fade">
  <div class="footer-content">
    <div class="footer-brand">
      <span class="brand-text">Obelisk Design</span>
      <span class="brand-tagline">从原理到实践</span>
    </div>
    <div class="footer-links">
      <a href="https://github.com/Obelisk-design" target="_blank" rel="noopener">
        <svg viewBox="0 0 16 16" width="18" height="18" fill="currentColor">
          <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
        </svg>
        GitHub
      </a>
    </div>
  </div>
  <div class="footer-bottom">
    <p>&copy; {today.getFullYear()} Obelisk Design. All rights reserved.</p>
  </div>
</footer>

<style>
  footer {
    padding: 3rem 1.5rem 4rem;
    background: var(--bg-secondary);
    border-top: 1px solid var(--border);
    transition: opacity 0.3s ease;
  }

  .footer-content {
    max-width: 1000px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .footer-brand {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .brand-text {
    color: var(--text-primary);
    font-size: 0.95rem;
    font-weight: 600;
  }

  .brand-tagline {
    color: var(--text-muted);
    font-size: 0.8rem;
  }

  .footer-links {
    display: flex;
    gap: 1.5rem;
  }

  .footer-links a {
    color: var(--text-secondary);
    font-size: 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    transition: color 0.2s ease;
  }

  .footer-links a:hover {
    color: var(--accent);
  }

  .footer-links svg {
    opacity: 0.7;
  }

  .footer-links a:hover svg {
    opacity: 1;
  }

  .footer-bottom {
    max-width: 1000px;
    margin: 2rem auto 0;
    text-align: center;
  }

  .footer-bottom p {
    color: var(--text-muted);
    font-size: 0.85rem;
    margin: 0;
  }

  @media (max-width: 768px) {
    footer {
      padding: 2rem 1rem 3rem;
    }

    .footer-content {
      flex-direction: column;
      gap: 1.5rem;
    }

    .footer-brand {
      align-items: center;
    }
  }

  @media (max-width: 480px) {
    footer {
      padding: 1.5rem 0.75rem 2.5rem;
    }

    .brand-text {
      font-size: 0.85rem;
    }

    .brand-tagline {
      font-size: 0.75rem;
    }

    .footer-links a {
      font-size: 0.85rem;
    }

    .footer-bottom p {
      font-size: 0.8rem;
    }
  }
</style>
```

- [ ] **Step 2: 构建验证**

```bash
npm run build
```

Expected: 构建成功

- [ ] **Step 3: 提交**

```bash
git add src/components/Footer.astro
git commit -m "feat: refactor Footer with refined design and brand identity"
```

---

## Task 5: 优化 Hero 区域

**Files:**
- Modify: `src/pages/index.astro`

- [ ] **Step 1: 优化 Hero 区域样式**

修改 `src/pages/index.astro` 的 `<style>` 部分：

```astro
---
import BaseHead from '../components/BaseHead.astro';
import Footer from '../components/Footer.astro';
import Header from '../components/Header.astro';
import { SITE_DESCRIPTION, SITE_TITLE } from '../consts';
---

<!doctype html>
<html lang="zh-CN">
  <head>
    <BaseHead title={SITE_TITLE} description={SITE_DESCRIPTION} />
  </head>
  <body>
    <Header />
    <main>
      <section class="hero" transition:animate="slide">
        <div class="hero-content">
          <h1>从原理到实践</h1>
          <p class="hero-subtitle">深入探索技术与设计</p>
          <div class="hero-cta">
            <a href="/blog" class="btn-primary">探索文章</a>
          </div>
        </div>
      </section>

      <section class="features" transition:animate="fade">
        <div class="feature-grid">
          <div class="feature-card hover-lift">
            <div class="feature-icon">01</div>
            <h3>第一性原理</h3>
            <p>不依赖类比和惯例，从根本真理出发推导解决方案</p>
          </div>
          <div class="feature-card hover-lift">
            <div class="feature-icon">02</div>
            <h3>深度解析</h3>
            <p>超越表面，追溯知识源头，揭示隐藏的机制和假设</p>
          </div>
          <div class="feature-card hover-lift">
            <div class="feature-icon">03</div>
            <h3>实战导向</h3>
            <p>理论服务于实践，提供可直接应用的工作流和方法论</p>
          </div>
        </div>
      </section>
    </main>
    <Footer />
  </body>
</html>

<style>
  .hero {
    padding: 8rem 0 5rem;
    text-align: center;
    position: relative;
  }

  .hero::before {
    content: '';
    position: absolute;
    top: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 600px;
    height: 400px;
    background: radial-gradient(ellipse 50% 30% at center, rgba(0, 212, 255, 0.1) 0%, transparent 70%);
    pointer-events: none;
  }

  .hero-content {
    max-width: 600px;
    margin: 0 auto;
    position: relative;
    z-index: 1;
  }

  .hero h1 {
    font-size: 3.5rem;
    margin-bottom: 1.5rem;
    letter-spacing: -0.03em;
    background: var(--accent-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .hero-subtitle {
    font-size: 1.25rem;
    color: var(--text-secondary);
    margin-bottom: 2.5rem;
    line-height: 1.6;
  }

  .hero-cta {
    display: flex;
    gap: 1rem;
    justify-content: center;
  }

  .btn-primary {
    padding: 0.875rem 2rem;
    background: var(--accent-gradient);
    color: var(--bg-primary);
    font-weight: 600;
    border-radius: 8px;
    transition: all 0.2s ease;
    display: inline-block;
  }

  .btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: var(--glow);
    color: var(--bg-primary);
  }

  .features {
    padding: 3rem 0 4rem;
  }

  .feature-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
  }

  .feature-card {
    padding: 2rem;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    transition: all 0.2s ease;
  }

  .feature-card:hover {
    border-color: var(--border-accent);
  }

  .feature-icon {
    font-family: var(--font-mono);
    font-size: 0.9rem;
    color: var(--accent);
    margin-bottom: 1rem;
    letter-spacing: 0.1em;
  }

  .feature-card h3 {
    margin-bottom: 0.75rem;
    font-size: 1.1rem;
  }

  .feature-card p {
    font-size: 0.95rem;
    color: var(--text-muted);
    margin-bottom: 0;
    line-height: 1.6;
  }

  @media (max-width: 768px) {
    .hero {
      padding: 5rem 0 3rem;
    }

    .hero h1 {
      font-size: 2.5rem;
    }

    .hero-subtitle {
      font-size: 1.1rem;
    }

    .feature-grid {
      grid-template-columns: 1fr;
    }

    .feature-card {
      padding: 1.5rem;
    }
  }

  @media (max-width: 480px) {
    .hero {
      padding: 4rem 0 2rem;
    }

    .hero h1 {
      font-size: 2rem;
    }

    .hero-subtitle {
      font-size: 1rem;
    }

    .btn-primary {
      padding: 0.75rem 1.5rem;
      font-size: 0.95rem;
    }

    .feature-card {
      padding: 1.25rem;
    }

    .feature-card h3 {
      font-size: 1rem;
    }

    .feature-card p {
      font-size: 0.9rem;
    }
  }
</style>
```

- [ ] **Step 2: 构建验证**

```bash
npm run build
```

Expected: 构建成功

- [ ] **Step 3: 提交**

```bash
git add src/pages/index.astro
git commit -m "feat: optimize Hero section with refined gradient and glow effect"
```

---

## Task 6: 模块 1 完成验证

- [ ] **Step 1: 启动开发服务器验证**

```bash
npm run dev
```

验证项目：
- View Transitions 页面切换动画是否平滑
- Header hover 效果是否生效
- Footer 新样式是否正常
- Hero 区域光晕效果是否可见
- Feature cards hover lift 是否正常

- [ ] **Step 2: 构建最终验证**

```bash
npm run build
npm run preview
```

Expected: 构建成功，预览正常

- [ ] **Step 3: 模块完成标记**

```bash
git log --oneline -5
```

确认以下提交存在：
- View Transitions support
- Animation system
- Header enhancement
- Footer refactor
- Hero optimization

---

## 完成标准

| 项目 | 验证方式 |
|------|----------|
| View Transitions | 页面切换有 fade/slide 动画 |
| Header 动画 | Logo hover 变色，导航过渡平滑 |
| Footer 新样式 | 品牌名 + 标语 + GitHub 链接 |
| Hero 光晕 | 背景有微妙渐变光晕 |
| Feature cards | Hover 时上移 4px + 边框高亮 |
| 构建成功 | `npm run build` 无错误 |

---

## 后续模块

完成后继续：
- [[模块 2：文章阅读体验]] - TOC、阅读进度、代码复制
- [[模块 3：增强功能]] - 相关文章、代码高亮
- [[模块 4：SEO 优化]] - OG 图片、结构化数据