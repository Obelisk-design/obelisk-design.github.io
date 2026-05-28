---
title: '从 LLM 到 Agent：理解 AI 智能体的底层逻辑'
description: '深入剖析 LLM 的本质机制，从 Token、Prompt、Context 到 Scaling Law 与涌现，理解为什么"预测下一个词"的模型能推理、写代码、做 Agent'
pubDate: '2026-05-22'
heroImage: '../../assets/llm-to-agent-hero.webp'
tags: ['AI', 'LLM', 'Agent', 'Deep Learning', 'Scaling Law']
---

## 开篇：Agent 到底是什么？

你可能听说过 AI Agent、Claude Code、Codex、Manus 这些产品。但真正追问下去：Agent 和 Chatbot 有什么本质区别？为什么同样是大模型，有的只能聊天，有的却能读文件、改代码、跑命令、持续完成任务？

**核心结论先行**：

```
Agent = LLM + Harness
```

- **LLM**（大语言模型）：大脑，负责推理和生成
- **Harness**：工程身体，包括工具、记忆、环境、权限、反馈回路

LLM 没有"手脚"，不能操作文件、运行命令。Harness 把它接入真实世界——让它从"会说"变成"能做"。

拿 Claude Code 举例：它把 Claude 这个 LLM 接入代码仓库、终端、文件系统、工具调用。真正让它变成 Agent 的，不只是模型本身，而是模型外面这套工程身体。

---

## 第一层：LLM 的底层机制

LLM 到 Agent 之间不是直接跳过去的。先理解 LLM 这个"大脑"本身。

### LLM 的本质：预测下一个 Token

LLM 是基于 Transformer 的**自回归语言模型**。

"自回归"的意思：一个词一个词地接着往下生成。

工作流程：

```
给一段上文 → 计算下一个词的概率分布 → 选一个词 → 拼到上文末尾 → 重复
```

这个机制决定了 LLM 的一切。本质就是一句话：**根据上文预测下一个词（Token）**。

### Token：最小的处理单元

LLM 无法直接处理原始文字。文字先被切成一个个最小处理单元——Token。

Token 不是完整的词，而是"子词"或字符片段。比如 "unbelievable" 可能被切成 `["un", "believe", "able"]`。

**为什么不用字母或完整词？**

| 方案 | 问题 |
|------|------|
| 每个字母一个 Token | 语义单元太小，无法理解"like"是动词还是介词 |
| 每个词独立 Token | 词汇表膨胀到几百万，eat/eats/eating 被当成三个完全不同的东西 |

子词分词法正好平衡两者：几千个积木覆盖几十万单词的全部变化。模型既能知道核心意思来自 `eat`，又能通过 `ing` 理解时态。

**Token 已经是 AI 花销的基本计量单位**。管理 AI 成本，本质是分配 Token 预算。

### Prompt：初始输入

模型需要一个初始输入才能开始计算概率。这个初始输入就是 Prompt。

从数学角度：Prompt 是你给模型的**条件概率的前置条件**。

```
P(下一个词 | "请用李白的风格写一首咏月的诗")
```

模型在训练时读过无数诗词。当上文出现"李白""风格""诗"，后续大概率是古诗体词汇。

Prompt 的本质：**通过控制上文来操控输出概率分布**。Prompt 变化 → 条件变化 → 输出分叉。

### Context：上下文窗口

模型生成每个新词时都"回顾"之前见过的所有内容。这个被回顾的整个上文就是 Context。

**关键约束**：Context 不能无限长。

标准 Transformer 的自注意力计算复杂度是 `O(n²)`。Token 数量翻倍，计算量翻四倍。系统必须划定最大长度——这就是**上下文窗口（Context Window）**。

**窗口大小的演进**：

| 阶段 | 容量 | 类比 |
|------|------|------|
| 便利贴 (≤4K) | 短问答 | 巴掌大的纸，聊几句就得擦掉 |
| 小说/说明书 (32K) | 文档处理 | 能摊开一份产品手册 |
| 项目文档 (128K-200K) | 主流工作台 | 能装下《三体》第一部 |
| 全集/图书馆 (1M-10M) | 代码仓库 | 整个哈利波特系列 |

**重要缺陷**：Lost in the Middle 效应

窗口大了，不代表每样东西都能被找到。模型对文档开头和结尾抓得最准，中间部分容易"视而不见"。

上下文工程的核心：**不只是换更大的桌子，而是把最重要的材料永远摆在显眼位置**。

---

## 第二层：为什么"接话"模型会推理、写代码

一个只会"词语接龙"的统计模型，怎么突然会写诗、翻译、写代码了？

两个关键词：**Scaling Law** 和 **Emergence**。

### Scaling Law：规模法则

2017 年，百度研究院发表《Deep Learning Scaling is Predictable, Empirically》：深度学习模型的泛化能力与模型大小、数据量呈可预测的幂律关系。

2020 年，OpenAI 发布划时代论文《Scaling Laws for Neural Language Models》：

```
模型性能与计算量、数据量、参数量之间
存在跨越 7 个数量级的稳定幂律关系
```

用一句话翻译：**投入多少资源，模型就会可预测地变好多少**。

这让大模型训练从赌博变成有依据的工程投入。LLM 军备竞赛的大门由此打开。

**Scaling Law 到头了吗？**

研究者访谈观点（非论文结论）：

- **理论上**：Scaling Law 本身依然有效，潜力巨大
- **实践上**："撞墙"多是执行层面的 Bug，掩盖真实进步
- **未来上**：从"狼吞虎咽"转向"细嚼慢咽"——推理时计算、合成数据、Agent Scaling

### Chinchilla Law：营养配方

2022 年 Google DeepMind 发现：很多模型是"营养不良"的——胃大，食物不够。

**Chinchilla Law**：模型参数与训练 Token 数的理想比例约 **1:20**。

Chinchilla 模型（70B 参数）比 Gopher（280B 参数）小得多，但"吃"了 4 倍数据，表现反而更优。

### Emergence：涌现

当参数从几千万膨胀到百亿千亿，某些小模型完全不存在的"智能行为"自己冒出来了。模型没有专门训练这些行为——训练目标始终是简单的"预测下一个词"。

**涌现的定义**：小规模模型不存在，大规模模型存在的能力。

**涌现的本质**：量变引起质变。借用复杂科学的概念——"多者异也"（More is different）。

类比：

| 系统 | 个体 | 涌现属性 |
|------|------|----------|
| 水 | H₂O 分子 | 湿润、流动 |
| 蚁群 | 单只蚂蚁 | 种植真菌、饲养蚜虫 |
| 神经网络 | 参数 | 推理、编程、翻译 |

**涌现的发现历程**：

1. **GPT-3 (2020)**：1750 亿参数，首次系统展示上下文学习——无需微调，仅凭几个示例就能执行翻译、问答、算术等任务
2. **Google 论文 (2022)**：《Emergent Abilities of Large Language Models》正式确立"涌现"概念，证明存在临界点

**典型涌现能力**：

| 能力 | 描述 |
|------|------|
| 思维链 (CoT) | 自己写出"一步步思考"，不瞎猜答案 |
| 算术推理 | 理解十进制、进位，而非背答案 |
| 代码生成 | 懂算法、逻辑控制流，不只是模仿代码样子 |
| 多语言翻译 | 构建语义中间层，无师自通跨语种 |
| MMLU | 57 个学科的通才，调用背景知识推理 |

**关键区分**：

- **能力涌现** (Emergent Abilities)：可观察、可评估的现象
- **智能涌现** (Emergent Intelligence)：未被严格证明的本质

我们今天对大模型的驾驭，正处在 18 世纪物理学家用蒸汽机改变世界但未完全理解热力学的相似时刻。

---

## 第三层：从 LLM 到 Agent 的路径

LLM 的底层机制讲清楚了。下一篇会沿着这条路径继续：

```
LLM → Chatbot → Prompt Engineering → Context Engineering → Agent
```

- **Chatbot**：把大脑接进聊天界面，装了一张嘴
- **Prompt Engineering**：发现问法不同输出差巨大，研究如何组织语言
- **Context Engineering**：不只是 Prompt，而是整个 Context 如何组织——资料、历史、规则、工具结果
- **Agent**：不只是回答，而是调用工具、观察结果、继续行动

真正的 Agent 问题，在 LLM 开始调用工具、观察结果、持续行动时才出现。

---

## 第四层：为什么需要理解这些基础

理解底层原理后，你会发现很多"AI 使用技巧"根本没有意义——核心原理就是那些。

不是天天用就叫会用 AI，不是嘴上说蒸馏、skill 就叫懂了 AI。理解 Token、Prompt、Context、Scaling Law、涌现，才能真正用好 AI，也能识别哪些是干货、哪些是割韭菜的营销。

---

## 总结

| 概念 | 本质 |
|------|------|
| Agent | LLM + Harness（大脑 + 工程身体） |
| Token | 最小处理单元，子词分词平衡词汇量和长度 |
| Prompt | 条件概率的前置条件，控制输出分布 |
| Context | 上文窗口，约束是 O(n²) 计算复杂度 |
| Scaling Law | 投入资源 → 可预测的性能提升 |
| Emergence | 量变引起质变，临界点后能力突变 |

LLM 最底层的工作方式：根据上文预测下一个 Token。Scaling Law 和 Emergence 解释了为什么这个简单机制规模变大后会涌现推理、翻译、写代码等复杂能力。

下一篇继续从 Chatbot、Prompt Engineering、Context Engineering 讲起，看这个会说话的大脑如何一步步变成能行动的 Agent。

---

## 参考资料

- OpenAI: 《Scaling Laws for Neural Language Models》 (2020)
- OpenAI: 《Language Models are Few-Shot Learners》 (GPT-3, 2020)
- Google: 《Emergent Abilities of Large Language Models》 (2022)
- Google DeepMind: Chinchilla 研究 (2022)
- 百度研究院: 《Deep Learning Scaling is Predictable, Empirically》 (2017)
- 原文：微信公众号文章《从 LLM 到 Agent Harness》

---

*本文基于微信公众号文章整理，补充第一性原理分析和技术背景说明。*