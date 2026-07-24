---
title: "baoyu-skills：20+ 即用技能，让 Claude Code / Codex 工作流立刻上手"
description: "baoyu-skills 是一个面向 Claude Code、Codex 等 AI Agent 的技能库，覆盖微信公众号配图、排版、发布全流程，最小安装只需 3 个 skill。"
pubDate: 2026-07-24
tags: ["AI", "Claude Code", "Skills", "微信公众号"]
heroImage: "../../assets/blog-placeholder-1.jpg"
url: https://github.com/JimLiu/baoyu-skills
source: github.com
---

# baoyu-skills：20+ 即用技能，让 Claude Code / Codex 工作流立刻上手

JimLiu 在 GitHub 开源的 [baoyu-skills](https://github.com/JimLiu/baoyu-skills) 是给 AI Agent（Claude Code、Codex 等）准备的能力扩展包。它把"配图 → 改稿 → 排版 → 发布微信公众号"这条长链路拆成 20+ 个独立的 skill，按需安装即可。

> 一次性装全部 = 给 Agent 加无关 context 开销。只装你需要的。

## 一句话安装

```bash
npx skills add jimliu/baoyu-skills
```

## 微信公众号文章工作流的最小集合

如果只做"微信公众号发布"这一件事，三个 skill 就够：

| Skill | 职责 |
|-------|------|
| `baoyu-cover-image` | 生成封面图 |
| `baoyu-article-illustrator` | 文中插图 |
| `baoyu-post-to-wechat` | 一键发到公众号（含 Markdown → 公众号 HTML 转换） |

> 不需要单独装 `baoyu-markdown-to-html`——`baoyu-post-to-wechat` 已经内置了 Markdown → 公众号就绪 HTML 的流程。
> 只有当你需要先把草稿/纯文本变成结构化 Markdown（标题、摘要、加粗、列表）时，才装 `baoyu-format-markdown`。

## Codex 项目级安装（按需 symlink）

Codex 在项目里扫 `.agents/skills`。如果你只需要其中几个 skill，直接把目录拷贝或软链过去：

```
<project>/.agents/skills/baoyu-cover-image/SKILL.md
<project>/.agents/skills/baoyu-article-illustrator/SKILL.md
<project>/.agents/skills/baoyu-post-to-wechat/SKILL.md
```

## 微信公众号 API 凭证放置

按作用域分两种：

- **用户级（所有项目共享）**：`~/.baoyu-skills/.env`
- **项目级（只对当前项目生效）**：`<project>/.baoyu-skills/.env`

> 项目级 `.env` 别 commit 到 Git。建议加进 `.gitignore`。

## 发布到 ClawHub / OpenClaw

每个 `skills/baoyu-*` 目录都可以单独作为 ClawHub skill 发布：

```bash
./scripts/sync-clawhub.sh --dry-run   # 预览
./scripts/sync-clawhub.sh --all       # 真正发布
```

发布后用户可以单独安装，例如：

```bash
clawhub install baoyu-image-gen
clawhub install baoyu-markdown-to-html
```

> ClawHub 是按 skill 装的，不是整包 marketplace。发布到 ClawHub 的 skill 协议是 **MIT-0**。

## 注册为 Plugin Marketplace

在你的 Agent 里跑：

```
/plugin marketplace add jimliu/baoyu-skills
```

## 怎么挑自己需要的 skill

20+ skill 不是越多越好。判断标准：

1. **你目前的工作流里哪一步在重复劳动？**——选能消掉那一步的 skill。
2. **装完有没有真的用上？**——装而不用的 skill 每次都会消耗 Agent 的 context window。
3. **是否依赖外部凭证？**——例如微信公众号 API、Notion API 等，没配凭证的 skill 装上也跑不起来。

## 适配 OpenClaw / ClawHub 生态

这个仓库已经支持把每个 `skills/baoyu-*` 作为独立 ClawHub skill 发布。这意味着你可以：

- 只取自己需要的 skill，避免"全量安装"的 context 浪费
- 复用 ClawHub 现有的认证、安装、版本管理基础设施
- 自己 fork 后只改某个 skill 再发布，不影响其它

## 总结

baoyu-skills 的核心价值是**把"AI Agent 干微信公众号长链路"这件事拆成可独立安装、可独立升级的模块**。如果你只做一件事，先装 `baoyu-post-to-wechat`；如果还要配图，加上 `baoyu-cover-image` 和 `baoyu-article-illustrator`。其它 skill 留到真需要时再装。

---

**原文链接**：[github.com/JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills)
