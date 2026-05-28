---
title: '中台蜕变：从代码供应商到 AI 积木供应商'
description: '把中台改造成 AI Agent 的积木库，做三件事：积木说明书（Tool Description）+ 拼装规则（约束声明化）+ 参考图纸（样板间），让搭积木这个十年愿景第一次真正成立'
pubDate: '2026-05-20'
heroImage: '../../assets/middle-platform-ai-building-blocks-hero.webp'
tags: ['AI', '中台', 'Agent', '架构', 'Spec驱动开发']
---

## 开篇：为什么中台需要蜕变？

上篇聊了"何去何从"，本篇聊"明天就能开干"。

核心结论三句话：

| 结论 | 内容 |
|------|------|
| 第一句 | AI 把"造积木"的成本压低一个数量级，中台靠"帮你省造积木的钱"撑不住了 |
| 第二句 | 10 个团队用 AI 造出 10 套用户系统，比没有中台更糟——不一致的扩散速度也被 AI 放大 |
| 第三句 | 中台不是该拆，是该蜕皮——从"代码供应商"进化为"积木工厂 + 拼装规则" |

**本篇回答的问题：怎么把你的中台改造成 AI 能用的积木库**

---

## 第一层：新定位——中台 = AI 的积木供应商

天猫在 AI Coding 实践中构建了一套四层物料体系，代码采纳率从 50% 提升到 97.9%。

### 四层物料体系

| 物料层 | AI Agent 视角 | 中台视角 | 加载方式 |
|--------|--------------|---------|---------|
| 任务规格 | "这次做什么" | 业务方提供 | 动态生成 |
| 积木库 | "用什么搭" | 原子能力 + CLI/Tool Description | 静态注入 |
| 拼装规则 | "怎么搭不塌" | 约束契约（声明式） | 静态注入 |
| 参考图纸 | "照着谁搭" | 样板代码 + 领域知识 | 动态检索 |

**新定位：不再是"帮你写代码"的乙方，而是"给 AI 供积木和图纸"的物料供应商**

---

## 第二层：积木说明书——用 CLI 哲学改造原子能力

### 为什么是 CLI 哲学？

MCP、Function Calling、A2A——协议在快速演进，今天的标准半年后可能过时。

但有一个设计哲学已经经过 **50 年验证**：Unix CLI 哲学

```
每个命令做一件事，可组合，自描述
```

把原子能力改造成"CLI 风格的命令"，底层传输层用 MCP 还是 Function Calling 都行——设计原则不变。

### API 文档 vs CLI 命令：本质区别

| 维度 | 传统 API 文档（给人看） | CLI 命令（给 AI 看） |
|------|------------------------|---------------------|
| 核心信息 | 接口地址、参数类型 | 功能语义：什么时候该用、什么时候绝不能用 |
| 示例 | 请求/响应 JSON | 前置条件 + 副作用声明 |
| 错误处理 | 错误码表 | 补偿命令：出错了怎么回滚 |
| 缺失 | — | 约束引用 + 组合建议 |

**给 AI 看的文档，重点是"什么时候该调"和"什么时候绝不能调"**

### Tool Description 模板（可直接 copy）

```yaml
tool:
  name: "create_order"
  description: "创建交易订单，含商品明细、价格计算和库存预扣"

  # CLI 哲学：when_to_use / when_not_to_use 比参数说明重要 10 倍
  when_to_use: "用户确认购买意图，且已完成风控审核"
  when_not_to_use: "仅浏览或加购场景不应调用"

  parameters:
    - {name: user_id, type: string, required: true, desc: "已实名认证的用户 ID"}
    - {name: items, type: array, required: true, desc: "商品明细（sku_id + quantity）"}
    - {name: promotion_id, type: string, required: false, desc: "营销活动 ID"}

  preconditions:
    - "用户状态 = active"
    - "所有 SKU 库存 >= 请求数量"
    - "已通过 risk_check（顺序约束）"

  side_effects:
    - "库存预扣（30min 未支付自动释放）"
    - "生成订单，状态 = pending_payment"

  constraints:
    - {ref: "rule://payment_sequence", desc: "创建后 30min 内必须调用 initiate_payment"}
    - {ref: "rule://promo_conflict", desc: "不可叠加其他折扣类活动"}

  error_handling:
    - {error: "E_STOCK_LOW", compensate: "调用 release_inventory，回滚预扣"}
    - {error: "E_RISK_FAIL", compensate: "返回风控原因，不创建订单"}
```

---

## 第三层：拼装规则——约束声明化

### 为什么约束不能留在代码里？

传统约束散落在：
- API 里的 if-else 判断
- 数据库触发器
- 文档里的"注意事项"段落

**AI 读不到这些隐形知识**，会踩同样的坑。

### 约束声明化格式

```yaml
rule://payment_sequence:
  domain: "交易"
  name: "支付时序"
  declaration: "订单创建 30min 内必须发起支付"
  rationale: "库存预扣 30min 自动释放，超时未支付将导致库存回滚"
  enforcement:
    - {tool: create_order, trigger: "on_complete", action: "timer_start(30min)"}
    - {tool: initiate_payment, trigger: "on_call", action: "timer_cancel()"}
  violation:
    - {event: timeout, consequence: "订单状态 = cancelled, 库存释放"}
```

### 约束分类

| 类型 | 示例 | AI 处理 |
|------|------|---------|
| 硬约束 | 支付时序、资金合规 | 强制校验，违规禁止执行 |
| 软约束 | 性能建议、最佳实践 | 提示但不阻断 |
| 上下文约束 | 营销互斥 | 动态计算后注入 |

---

## 第四层：参考图纸——样板间与知识库

### 样板间（Reference）

```
reference/
├── order-service/          # 订单域标准实现
│   ├── src/
│   ├── tests/
│   └── AGENTS.md           # 注入 Tool Description + 约束
├── payment-service/
└── inventory-service/
```

**AGENTS.md 结构：**

```markdown
# Order Service

## Tools
- create_order: 创建订单
- cancel_order: 取消订单

## Constraints
- rule://payment_sequence: 支付时序约束
- rule://promo_conflict: 营销互斥约束

## Patterns
- 标准下单流程: risk_check → create_order → initiate_payment
```

---

## 第五层：三种 Agent 搭法

### 5.1 CLI Agent：运营的"自然语言 CLI"

**适用场景：运营等非技术人员**

```
运营输入: "创建一个满 200 减 30 的活动，618 当天有效"

Agent 执行:
1. 读取 rule://promo_conflict → 确认互斥关系
2. 调用 create_promotion(...)
3. 调用 set_schedule(...)
4. 返回确认 → 等待人工审核
```

**效果：中台 API 调用量放大一个数量级**

### 5.2 Spec 驱动模式：多 Agent 协作循环

**适用场景：有开发团队的业务线**

```
开发者写 Spec → Code Agent 生成 → CR Agent 校验 → Test Agent 测试 → 循环直到通过
```

**关键比例：90% 抄物料，10% 写差异**

### 5.3 Multi-Agent：新业务线冷启动

**适用场景：全新业务线从零搭建**

```
Input:  "我要做一个拼团业务"

Output: 完整应用脚手架
        ├── src/services/
        ├── src/rules/
        ├── tests/
        └── deploy/
```

**代码覆盖率从 30% 提升到 80%+**

---

## 第六层：落地路线图——4 个里程碑

| 阶段 | 目标 | 验收标准 |
|------|------|---------|
| M0 | 体检+瘦身 | 代码量 -40% |
| M1 | 建物料 | P0 域 100% 覆盖 |
| M2 | 首个 Agent | 约束违规率 < 5% |
| M3 | 乘法效应 | 冷启动月级→天级 |

### 三条铁律

1. **M0 不依赖 AI**：先整理原子能力和约束
2. **M1 是卡点**：Tool Description 质量决定 Agent 上限
3. **M3 要建反馈闭环**：失败→分析→补充约束→持续提升

---

## 总结

把中台从"被调用的代码库"改造成"AI Agent 的积木供应商"，做三件事：

| 物料 | 作用 |
|------|------|
| 积木说明书 | 让 AI 知道"用什么搭" |
| 拼装规则 | 让 AI 知道"怎么搭不塌" |
| 参考图纸 | 让 AI 知道"照着谁搭" |

**公式：**

```
原子中台（积木 + 规则 + 图纸） × AI Agent（Spec 驱动循环） = 搭积木十年愿景第一次真正成立
```

**立即行动：先把最核心的 5 个原子能力写上 Tool Description**