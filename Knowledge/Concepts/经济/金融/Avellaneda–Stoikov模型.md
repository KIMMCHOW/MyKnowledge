---
type: concept
schema_version: 1
name: Avellaneda–Stoikov模型
status: completed
completion_status: completed
created_from: finance-refactor
created_at: 2026-08-09
updated_at: 2026-08-09
aliases:
  - AS model
  - Avellaneda–Stoikov Model
  - AS 做市模型
tags:
  - 金融
  - 做市
  - 随机控制
domain: 经济
subdomain: 金融
---

# Avellaneda–Stoikov 模型

## 定义
Avellaneda–Stoikov 模型是通过随机控制联合决定做市报价中心与价差宽度，以平衡成交收益和库存风险的库存型做市模型。

## 核心解释
模型用库存调整后的保留价格平移报价中心，并用风险厌恶、价格波动率、剩余期限和成交强度决定报价宽度。它是理解库存型做市的基准框架，不是可直接上线的完整策略，因为原始模型没有充分描述 tick、队列、延迟、费用、部分成交、订单流毒性和多资产对冲。

## 关联概念
- [[做市]]：AS 模型是做市报价的经典形式化模型。
- [[流动性]]：成交强度刻画报价距离与流动性需求的关系。
- [[波动率]]：价格波动率决定库存风险惩罚。
- [[效用函数]]：原始模型采用 CARA 指数效用。

## 深入笔记

- [[Knowledge/Notes/Finance/Market Making/Avellaneda–Stoikov 做市模型|AS 库存型做市模型]]
- [[Knowledge/Notes/Finance/Market Making/Avellaneda–Stoikov 研究资料|AS 模型研究资料]]

## 相关问题
- 有限期限近似与长时稳态解有什么区别？
- 真实订单簿的队列和逆向选择应如何加入模型？
