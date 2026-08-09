---
title: "Rho / Rho"
concept_id: C30
graph_layer: 5
tags: [期权知识图谱, 核心概念]
generated_by: "tools/build_option_knowledge_graph.py"
---

# Rho / Rho

> [!definition] 定义
> Rho 衡量利率变化对期权价值的局部敏感度，在长期限、外汇和融资敏感头寸中更重要。

## 核心关系

### 向下游传导

- **汇总为组合暴露 →** [[组合Greeks与头寸分析|C32 组合Greeks与头寸分析]]：各腿 Rho 形成利率风险。

### 受上游约束

- [[Black-Scholes模型|C22 Black-Scholes模型]] **—导出局部敏感度→ 本概念**：模型衡量利率输入变化的局部影响。
- [[利率与融资成本|C08 利率与融资成本]] **—变化时经由Rho传导→ 本概念**：利率变化影响贴现和远期。

## 关键公式

$$\rho=\frac{\partial V}{\partial r}$$

## 风险经理检查

- 不要只平移单一利率；压力测试收益率曲线形变、融资利差和股息—利率联动。
- 把模型数值与可成交价格、压力情景和头寸规模一起复核。

## 主要章节

- [[07-风险度量（一） Risk Measurement I|第7章 风险度量（一）]]
- [[13-风险考量 Risk Considerations|第13章 风险考量]]
- [[19-二叉树期权定价 Binomial Option Pricing|第19章 二叉树期权定价]]
- [[21-头寸分析 Position Analysis|第21章 头寸分析]]
