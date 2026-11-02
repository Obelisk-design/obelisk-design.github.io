---
title: "拆解医疗数据中台：采集服务的公理与现代化"
description: "以一个真实生产级 Spring Cloud 数据采集微服务为标本，用第一性原则提炼数据平台的设计公理，逐项对照开源方案，给出 2026 年的现代化路线。"
tags: [数据中台, 第一性原理, 开源方案, Flink, 数据治理]
pubDate: 2026-11-01
heroImage: '../../assets/data-sjcj-first-principles-hero.webp'
---

# 拆解医疗数据中台：采集服务的公理与现代化

> 标本：某市级医疗数据平台的"数据生成/采集"微服务（Spring Cloud 技术栈，生产运行中）。
> 60+ 张表、17 种异构数据源、17 个监控 Controller、80+ 告警项、三套调度体系并存。
> 本文不评价好坏，只回答三个问题：**它为什么长这样？每个自研轮子对应什么开源方案？2026 年重做该怎么做？**

## 核心论断 (Core Claims)

1. **数据平台的第一复杂度不是搬运，是状态**：4 把 Redis 锁、5 态任务状态机、跨阶段队列表、自愈重启（≤3 次放弃）——这套系统用"MySQL 中间表 + Redis 锁 + XXL-Job"手工实现了一个工作流引擎。这是所有采集平台的宿命。
2. **对账是一等公民，不是日志附属**：独立的比对任务域（行数差值 `differenceValue` / 差异率 `differenceRatio`）+ 小时级"消费量 vs 入库量"对账表 + 无主键告警——因为上游不可信，同步的可信度只能靠验证建立。
3. **标准域才是业务核心**：标准码表、原字典、对照关系、转码审核流共 14 张表；v1→v2 的重构方向就是把"对照关系"升为一等公民。医疗数据互联互通的瓶颈在语义翻译，不在管道吞吐。
4. **三套调度并存是演进化石**：Quartz（任务触发）+ XXL-Job（监控告警）+ @Scheduled+ShedLock（内部清理）各管一摊——每次加功能选了当时最顺手的工具，没有谁错了，但复杂度是复利的。
5. **半成品是诚实的信号**：SQLFlow 血缘解析已引入 gsqlparser 但只有注释代码、短信告警的发送循环体为空——血缘与告警"最后一公里"，恰是下一阶段的正确方向。

## 第一性原理：医疗数据平台为什么长这样

**公理一：医院信息系统是异构孤岛——这是政策与采购决定的，不是技术决定的。**
一家三甲的 HIS 跑 Oracle，社区医院用 MySQL，老系统是达梦或 InterSystems Cache，还有人大金仓。推论：平台必须有一层"统一元数据抽象"，对上层隐藏 17 种数据库的 DDL/DML 差异。该系统的 `dms/` 模块用"Switch-on-DbType 路由器"实现了它——每种库一套 Catalog/Schema/Table/Column/Select 五件套 Service。能用，但新增一种库要改 5+ 处 switch。这是所有 connector 框架（SeaTunnel/Airbyte/DataX）要解决的同一个问题。

**公理二：同步即复制，复制的可信度等于可验证性。**
数据从源库到目标库的每一次搬运都可能丢、重、错。推论：对账不能是"出问题再查"的事后行为，必须是常设任务域。该系统把它做成了独立模块（比对任务 + 按表日志 + 差异率排序接口），甚至给"目标表无主键"单设了告警——因为无主键意味着无法幂等重放。这是整个系统最值得抄的设计。

**公理三：增量是常态，全量是例外。**
全量重抽是昂贵的（TRUNCATE + 重导），所以每次增量都靠水位线：`updateTimestamp` 记录增量起点，目标表自动附加 `SJGT_CJ_TIME`（采集时间）/ `SJGT_SYNC_TIME`（同步时间）虚拟字段。推论：水位线管理必须显式建模——该系统甚至有"标准化 SQL 变更后清空水位线强制重抽"的联动 Job（`TranscodeChangeFullSyncJob`），因为标准变了，旧数据全部作废。这是多数教程不会告诉你的一环：**schema/标准变更会击穿增量假设**。

**公理四：标准翻译是语义问题，不是数据问题。**
"原值 1 → 标准值 A"的映射没有算法解，只有"标准码表 + 原字典 + 对照关系 + 人工审核流"的组织解。该系统的 v1→v2 重构（物理建表式 → 字典项逻辑式 + 对照关系独立表 + 版本化 + Excel 对照导入）本质是在为"语义映射"这一稀缺资源降低维护成本。

**公理五：分布式环境下，任何任务都可能重复执行或半途而废。**
推论：每把锁都有 TTL（初始化 30 分钟、抽取任务 7 天），每次启动前查锁，失败自愈但设上限（`restart_count ≤ 3`），通知去重（`notice_flag` 防骚扰）。这些细节繁琐却致命——少一把锁，就是半夜重复跑批；少一个上限，就是无限重启风暴。

## 一条数据的旅程：五层架构解构

```
接入层  DbInfo/DbFolder/Actuator/FileManage —— 17 种数据源 + Flink jar 管理
   ↓
任务层  抽取(增量/中心同步) / 初始化(分片) / 比对 / 推送 —— 状态机 + 锁
   ↓
执行层  Flink Session Cluster —— Java 端只做调度, 真搬数据的是 Flink jar
   ↓        (CDC: OGG/Debezium → Kafka → 消费 → StarRocks)
标准层  标准码表 / 原字典 / 对照关系 / 物化视图标化 —— v1+v2 双轨
   ↓
监控层  17 个 Controller, 5 类告警 80+ 项, Grafana webhook 反向接入
```

几个值得驻留的工程决策：

- **Java 端与执行解耦**：比对任务的实际逻辑在 Flink jar 里，Java 只管理状态字段（排队/运行/停止/取消/未运行）。控制面和数据面分离——这正是现代存算分离思想的微缩版。
- **执行器模型**：Flink 集群被抽象为"Actuator"，上传 jar 拿 jarId、REST 提交、按剩余 slot 挑最空闲节点（`getLeatLoadedActuator`）。一个 Actuator 绑一个 jar 的强约束，牺牲灵活性换确定性。
- **初始化分片**：百万行大表按主键/时间等分 N 片 + 1 片 NULL 补漏，每 100 张表拆一个子任务。冷启动搬雪的工程化解法。
- **多租户**：所有请求走 Header `spaceId`，未绑定空间返回 HTTP 402（不是 401/403——历史约定，前端要知道）。医院空间 / 中心空间（spaceId=1000）两级。

## 自研轮子 vs 开源方案（逐项对照）

| 该系统自研 | 规模/痛点 | 开源等价物 | 替换收益 |
|---|---|---|---|
| dms 多库适配（17+ DB 手写五件套） | 新增 DB 改 5+ 处 switch | **Apache SeaTunnel** / Airbyte / DataX connector 生态 | 新增数据源=写配置；连接器社区维护 |
| Flink jar 手工提交（Actuator+REST+JSON 参数文件） | jar 版本、slot 分配、参数装配全手工 | **Flink CDC 3.x** pipeline（整库同步+Schema Evolution）、SeaTunnel Zeta | 免去自研参数协议；自动 schema 变更 |
| 三套调度并存 | Quartz+XXL-Job+@Scheduled 各管一摊 | **Apache DolphinScheduler**（DAG 可视化）或 Temporal（代码化工作流） | 单一事实源；依赖编排、重试、告警内置 |
| DataCompareTask 比对 | SQL 逻辑在 Flink jar 里黑盒 | **dbt tests** / Great Expectations / Soda Core / data-diff | 对账规则 SQL 化、版本化、可复用 |
| DataPushTask（Kafka→StarRocks 的 Flink jar） | 自研 OGG/Debezium 双模板解析 | **StarRocks Routine Load**（原生消费 Kafka） | 少一个 Flink 作业、少一层运维 |
| t_data_standardization 标化视图 | 物化视图 SQL + 审核流 | **dbt models**（SQL 版本化+测试+文档一体） | 审核流=PR review 的等价物，开源已解 |
| 标准码表+对照关系 | 14 张表，v2 刚理顺 | OpenMetadata / DataHub 的 Glossary（**只到元数据层，值域映射无开源解**） | 这是机会不是替代 |
| SQLFlow 血缘（gsqlparser 引入未挂线） | 半成品 | **OpenLineage** + sqllineage/SQLGlot | 事件驱动血缘，随任务自动采集 |
| 监控大盘（17 Controller + t_stat_*） | 自研统计表 22 张 | OpenMetadata + Prometheus/Grafana | 资源告警已在用 Grafana，补元数据层即可 |

**关键结论**：该系统真正不可替代的自研资产只有两个——**标准域的业务模型**（码表/对照/审核）和**对账体系的状态设计**。其余轮子，2026 年都有成熟开源答案。

## 2026 现代化路线（按性价比排序）

**第一步：推送层换 Routine Load（最易，当天见效）。**
Kafka→StarRocks 的自研 Flink jar 消费链路，直接换成 StarRocks Routine Load：少维护一个 jar、一套 OGG/Debezium 模板解析、一份对账逻辑（Routine Load 自带消费位点指标）。推送任务的"自愈重启"语义由 SR 原生承接。

**第二步：增量抽取收敛到 Flink CDC 3.x（中难度）。**
现在每种库配增量字段、手工维护水位线；Flink CDC 的 pipeline 模式支持整库同步 + Schema Evolution，MySQL/Oracle/PG/SQLServer 开箱即用。国产库（达梦/金仓/Cache）保留 JDBC 全量+水位线兜底即可——**不必追求 100% CDC 化**，公理一决定了长尾永远存在。

**第三步：比对规则 dbt 化（高价值）。**
把 Flink jar 里的比对 SQL 抽出来变成 dbt tests：`row_count` 差异、`unique` 主键、`not_null` 关键字段、小时级 `accepted_values`。对账从黑盒 Flink 作业变成版本化的 SQL 资产，告警规则直接复用现有的 5 类×80 项枚举设计。

**第四步：LLM 接入标准域（差异化最大）。**
该系统 v2 已有现成的 human-in-the-loop 骨架：`auto/mapper/task` 自动映射任务 + 人工审核流（待审/通过/驳回）。2026 年的正确姿势：原字典项与标准码表项做 embedding 召回 → LLM 生成候选映射 + 置信度 → 低置信度进人工队列 → 审核结果回流做 few-shot。映射任务从"人肉逐条"变"AI 批量初审 + 人审边界案例"。同理，标化视图的 SQL 审核流也是 LLM review 的天然挂载点。

**第五步（视规模决定）：湖仓层。**
如果中心库分析压力上来，考虑 CDC 直写 Paimon/Iceberg（存算分离、增量可查），StarRocks/Doris 退到查询层。但注意公理二：**先把对账做扎实，湖只是存储形态，不会让数据更可信。**

**明确不做**：调度收敛（DolphinScheduler）值得做但迁移成本最高——三套调度虽丑，却稳定。放在所有业务改造之后。

## 实践推论（可抄 / 该改 / 要建）

- **可抄**：4 把 Redis 锁的 TTL 设计；水位线+标准变更联动重抽；比对差异率排序接口；告警多维去重（fingerprint）；"无主键告警"这种预防性设计。
- **该改**：新功能一律挂 v2 标准域接口（v1 只留转码审批）；监控统计表（22 张 t_stat_*）考虑迁移 OpenMetadata；把短信/工单告警的最后一公里补上（现在循环体是空的）。
- **要建**：对照关系的版本 diff 视图（现在只有变更日志表）；血缘的 OpenLineage 事件流（替代 SQL 解析半成品）；数据契约文档化（码表=契约，schema+值域+SLA）。

## 原文明细（关键事实存档）

- 技术栈：Spring Boot 2.x + Spring Cloud Alibaba、Nacos、MyBatis-Plus、Druid、Kafka、Sentinel、ShedLock、Flyway（形同虚设，表结构跟随实体）、EasyExcel、JSch。
- 端到端链路：源库 →（Flink jar 全量/增量）→ 前置库 StarRocks →（标准化视图/转码）→（中心同步任务）→ 中心库；CDC 侧 OGG/Debezium → Kafka → 推送任务（Flink jar）→ 下游。
- 数据库类型 17+（mysql/oracle/postgresql/sqlserver/dm/dm8/kingbase/cache/starrocks/hive/greenplum/mongodb/kafka/es/api/ftp/sftp/redis...）。
- 状态机：抽取任务 4 态（未运行/运行中/已停止/等待执行），推送任务 5 态（多一个"失败"）；比对任务 5 态执行状态 + 5 种比对结果。
- 告警体系：5 类（服务/系统/数据量/业务指标/基础资源）× 80+ 告警项，医疗业务指标按门诊/急诊/住院/体检/慢病/床位/120 急救 9 大域编码（01xx~09xx）；Grafana webhook 按 fingerprint 去重。
- 历史包袱真实存在：`OraclelColumnDDLService`（多一个 l）、`getCacehSchema`（Cache 拼错）——生产系统不追求洁癖，追求稳定。

---

*分析基于 data-sjcj 仓库 v4.1.0 全源码扫描（commit 03d64436），文内接口/表名均可在源码定位。*
