---
title: "Lambda / Lambda"
graph_layer: 5
tags: [期权知识图谱, 核心概念]
generated_by: "tools/build_option_knowledge_graph.py"
---

# Lambda / Lambda

> [!definition] 定义
> Lambda 是期权价值对标的百分比变化的弹性，反映单位资本上的方向杠杆。

## 核心关系

### 向下游传导

- **汇总为百分比杠杆 →** [[组合Greeks与头寸分析|组合Greeks与头寸分析]]：Lambda 为组合提供资本敏感的方向暴露视角。
- **约束资本与头寸规模 →** [[策略选择与调整|策略选择与调整]]：高弹性头寸需与最大损失、保证金和可退出性一起决定规模。

### 受上游约束

- [[Delta（Natenberg）|Delta]] **—与价格共同定义→ 本概念**：Lambda 将绝对 Delta 转为百分比弹性。

## 关键公式

$$\Lambda=\frac{\partial V/V}{\partial S/S}=\Delta\frac{S}{V}$$

## 风险经理检查

- 当期权价格很小时 Lambda 会失真或爆炸；资本、保证金和最大损失不能仅由弹性衡量。
- 把模型数值与可成交价格、压力情景和头寸规模一起复核。

## 主要章节

- [[风险度量（二） Risk Measurement II|风险度量（二）]]
