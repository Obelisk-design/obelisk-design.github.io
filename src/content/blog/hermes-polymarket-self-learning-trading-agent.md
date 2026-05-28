---
title: "Hermes + Polymarket：搭建自学习 BTC 交易代理的完整指南"
pubDate: 2026-05-28
description: "从 100 美元起步，用 Hermes + Atomic + Claude Opus 搭建能持续复盘、持续调参、具备自学习能力的 BTC 交易代理。"
heroImage: '../../assets/hermes-polymarket-self-learning-trading-agent-hero.webp'
tags: ["AI Agent", "Polymarket", "Trading Bot", "Hermes", "Markov Chain", "Kelly Criterion"]
---

## 开篇：为什么是 BTC Up/Down？

2025-2026 年，Polymarket 上的交易 bot 创造了超过 **6000 万美元** 利润。其中 **77%** 来自同一个市场类型：

> **BTC Up/Down** — 5 分钟短周期加密市场

这不是靠情绪交易。不是跟新闻。不是凭感觉。

真正赚钱的 bot，在看一件事：**BTC 价格状态背后的转移概率**。

当 BTC 进入一个明确的方向状态时，这个状态是否会继续？是可以被数学模型测量出来的。

人群还在根据感觉下注时，**Markov 转移矩阵** 已经能提前识别状态持续性。

数学模型给出的概率，和市场当前价格之间的差，就是 **edge**。

而且这个 edge 不是一次性的，它可以被重复捕捉、放大、自动化执行。

---

## 第一层：理解市场结构

### 为什么 BTC Up/Down 存在结构性低效？

Polymarket 的 BTC 5 分钟 Up/Down 市场，是预测市场里结构性低效最明显的板块之一。

**原因很简单**：

1. **参与者依赖情绪**：新闻来了跟，社交媒体热了跟，K 线突然波动凭感觉下注
2. **时间窗口极短**：5 分钟内价格方向判断，大多数人根本来不及理性分析
3. **信息不对称**：真正有模型的人，和凭直觉的人，在同一市场博弈

这三点叠加，产生了一个可被数学捕捉的低效缝隙：

> **当 BTC 进入明确方向状态后，状态持续性是可预测的**

这不是预测 BTC 会涨还是跌。而是预测：**当前状态会不会持续**。

---

### Markov 转移矩阵的核心逻辑

假设 BTC 价格状态可以简化为 3 类：

- `UP`：上升趋势
- `DOWN`：下降趋势
- `NEUTRAL`：震荡/无明显方向

Markov 转移矩阵测量的是：**从状态 A 转移到状态 B 的概率**。

```
         UP    DOWN   NEUTRAL
UP      0.87   0.08    0.05
DOWN    0.10   0.85    0.05
NEUTRAL 0.15   0.15    0.70
```

这个矩阵告诉我们：

- 如果当前是 UP 状态，有 **87%** 概率下一个周期仍为 UP
- 如果当前是 DOWN 状态，有 **85%** 概率继续 DOWN
- NEUTRAL 状态转移概率较低，不进场

**edge 在哪里？**

假设市场当前 BTC Up 合约价格是 $0.75（市场认为 75% 概率涨）。

如果你的 Markov 模型计算出 p(UP, UP) = 0.87，那么：

> **edge = 0.87 - 0.75 = 0.12（12%）**

这 12% 的概率差，就是可被捕捉的套利空间。

---

## 第二层：技术架构设计

### 为什么选择 Hermes？

Hermes 是 NousResearch 推出的开源 agent 框架。

**关键背景**：
- NousResearch 背后有 **Paradigm 的 7000 万美元** 支持
- 专注 AI agent + crypto 交叉领域
- Hermes 设计目标：让 agent 能持续运行、持续复盘、持续调参

**为什么不用其他框架？**

| 框架 | 问题 |
|------|------|
| LangChain | 适合单次任务，不适合持续运行的交易代理 |
| AutoGPT | 缺乏明确的 crypto 生态集成路径 |
| CrewAI | 多 agent 协作，但单 agent 深度不够 |

Hermes 的核心能力：
- **持久化 session**：交易日志、参数调整历史、复盘记录都能持久保存
- **工具集成**：原生支持 terminal、browser、file 等工具
- **cron job**：定时任务支持，适合每日复盘/参数调整
- **Telegram/微信集成**：实时通知交易结果

---

### 完整技术栈

```
┌─────────────────────────────────────────────────────┐
│                    Trading Agent                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │   Hermes    │  │   Atomic    │  │ Claude Opus │  │
│  │  (框架层)   │→ │  (调度层)   │→ │   (决策层)  │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│                  Execution Layer                     │
│  ┌─────────────────────────────────────────────────┐│
│  │         py_clob_client_v2 (Polymarket CLOB)     ││
│  │  • SAFE_ADDRESS 支持                            ││
│  │  • collateral balance 术语                      ││
│  │  • fee-aware trade evaluation                   ││
│  └─────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│                   Data Sources                       │
│  • BTC 实时价格（CEX API）                           │
│  • Polymarket 市场订单簿                            │
│  • Markov 状态转移概率（历史数据训练）               │
└─────────────────────────────────────────────────────┘
```

**各层职责**：

| 层级 | 工具 | 核心职责 |
|------|------|----------|
| 决策层 | Claude Opus 4.7 | 判断是否进场、仓位大小 |
| 调度层 | Atomic | 接收 Hermes 指令，调用 Claude，管理 session |
| 框架层 | Hermes | 持久化状态、定时复盘、Telegram 通知 |
| 执行层 | py_clob_client_v2 | 与 Polymarket CLOB v2 交互，下单/撤单 |

---

## 第三层：参数配置与实战

### 核心参数清单

```
# .env 配置
PRIVATE_KEY=your_wallet_key        # 钱包私钥（绝不暴露在聊天/日志）
SAFE_ADDRESS=your_safe_address     # Polymarket Safe 地址
CLOB_HOST=https://clob.polymarket.com

# 策略参数
DRY_RUN=true                       # 默认模拟模式
MIN_EDGE=0.05                      # 5% 最小套利 gap
MIN_PROB=0.87                      # Markov 持续性阈值
MIN_BET=1.00                       # $1 最小测试仓位
MAX_BET=50.00                      # 上限保守起步
BANKROLL=100.00                    # 初始本金 $100

# Claude 配置（Atomic → Settings → AI Models → Anthropic）
Model: claude-opus-4-7-20261001
Max tokens: 4096
Temperature: 0.2                   # 低温度 = 更一致决策
```

**参数解释**：

| 参数 | 含义 | 推荐值 |
|------|------|--------|
| `MIN_PROB` | Markov 状态持续性阈值 | 0.87（低于此不进场） |
| `MIN_EDGE` | 最小概率差（edge） | 0.05（至少 5% 套利空间） |
| `DRY_RUN` | 模拟模式开关 | `true`（实盘前必须跑 24h） |
| `Temperature` | Claude 决策随机性 | 0.2（低=更稳定） |

---

### Kelly Criterion 仓位管理

进场后，仓位大小不是随便定的。使用 **Kelly 公式**：

```
f* = p - (1-p)/b
```

其中：
- `p` = 你的模型概率（如 0.87）
- `b` = 赔率（市场价格倒数）
- `f*` = 最佳仓位比例

**示例计算**：

假设模型概率 p = 0.87，市场 Up 合约价格 $0.75，赔率 b = 3：

```
f* = 0.87 - (1-0.87)/3 = 0.87 - 0.043 = 0.827
```

Kelly 建议仓位 = **82.7%** 的本金。

实际操作中用 **Half Kelly**（减半）降低风险：

> 实际仓位 = 41% 本金 = $41（假设 BANKROLL=$100）

---

## 第四层：自学习闭环

### 为什么需要自学习？

静态策略必死。市场在变化：
- BTC 波动特征会变
- Polymarket 参者行为会变
- 其他 bot 的策略会进化

如果你的参数是固定的，edge 会逐渐消失。

**自学习闭环的核心**：

```
交易 → 记录日志 → 每日复盘 → 调整参数 → 新交易
```

---

### Hermes 如何实现自学习？

**每日复盘流程**（通过 cron job 自动执行）：

```
每天午夜运行：
1. 读取昨天的 trade journal
2. 分析：
   - 哪些 Markov states 胜率最高
   - 哪些 entry price ranges 的 EV 最好
   - 当前 MIN_PROB 是否应该上调或下调
   - 当前 Kelly f* 是否适合最近的交易结果

3. 更新 .env config 和策略参数

4. 通过 Telegram 发送总结：
   - 今天的 P/L、胜率、交易次数
   - 策略改变了什么，以及为什么改变
   - 明天更新后的 thresholds
```

---

### 24 小时 Dry Run 测试

**在进入实盘之前，必须先跑 DRY_RUN 模式 24 小时。**

模拟模式下记录：
- 检测到多少个信号
- 入场价格
- 入场时的 Markov state
- 每笔模拟 P/L
- 在当前阈值下的胜率

**判断标准**：

| 指标 | 达标值 | 不达标处理 |
|------|--------|-----------|
| 信号数量 | ≥ 20 个 | 降低 MIN_PROB |
| 模拟胜率 | ≥ 70% | 提高 MIN_EDGE |
| 模拟 P/L | 正收益 | 检查 Markov 模型 |
| 最大单笔亏损 | < 10% 本金 | 降低 MAX_BET |

**只有 dry run 稳定，才能小额实盘。**

---

## 第五层：安全与风控

### 钱包安全

**关键原则**：

1. **绝不暴露 private keys**
   - 不在聊天中讨论
   - 不在日志中打印
   - 只在 `.env` 文件中配置

2. **使用 Polymarket Safe**
   - Safe 是 proxy wallet，资金在 Safe 合约里
   - 即使 agent 被攻击，资金不在 agent 直接控制的地址

3. **最小权限原则**
   - agent 只能访问 collateral balance
   - 不能访问其他钱包资产

---

### 止损机制

虽然策略本身有概率过滤，但仍需硬性止损：

```
MAX_DAILY_LOSS = 0.20   # 单日最大亏损 20% 本金
MAX_SINGLE_LOSS = 0.10  # 单笔最大亏损 10% 本金

当达到日止损线时：
- 停止今日交易
- Telegram 通知 "⚠️ 达到日止损线，交易已暂停"
```

---

## 总结：从 100 美元到自学习系统

搭建一个能自学习的 BTC 交易代理，关键不是某个神奇参数，而是：

1. **理解市场低效的根源**：Markov 状态持续性 vs 情绪交易者
2. **数学模型量化 edge**：概率差不是猜测，是计算
3. **自学习闭环**：每日复盘 → 调参 → 新交易
4. **安全第一**：dry run 24h、不暴露私钥、硬性止损
5. **小额起步**：$100 本金测试，稳定后再放大

Hermes + Atomic + Claude Opus + Polymarket CLOB v2，这套组合的意义不是「某个 bot 赚了多少钱」，而是：

> **提供了可复用的自学习框架** — 你可以用同样的架构，去捕捉其他市场的低效缝隙。

---

## 附录：快速启动命令

```bash
# 1. 克隆 Hermes
git clone https://github.com/nousresearch/hermes
cd hermes

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置 .env
cp .env.example .env
# 编辑填入你的参数（绝不暴露在聊天）

# 4. 启动 dry run
python run_agent.py --mode dry_run --duration 24h

# 5. 检查日志
cat logs/trade_journal_$(date +%Y-%m-%d).json

# 6. 小额实盘（dry run 达标后）
python run_agent.py --mode live --bankroll 100
```

---

**相关资源**：
- Hermes 文档：https://hermes-agent.nousresearch.com/docs
- Polymarket CLOB v2 API：https://docs.polymarket.com
- Claude Opus API：https://docs.anthropic.com