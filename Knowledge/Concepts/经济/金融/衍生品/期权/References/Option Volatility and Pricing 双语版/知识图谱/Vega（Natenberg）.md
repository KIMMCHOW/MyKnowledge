---
title: "Vega / Vega"
concept_id: C29
graph_layer: 5
tags: [期权知识图谱, 核心概念]
generated_by: "tools/build_option_knowledge_graph.py"
---

# Vega / Vega

> [!definition] 定义
> Vega 衡量模型波动率变化对期权价值的局部敏感度，是隐含波动率头寸的主要尺度。

## 核心关系

### 向下游传导

- **汇总为组合暴露 →** [[组合Greeks与头寸分析|C32 组合Greeks与头寸分析]]：各腿 Vega 形成波动率风险。

### 受上游约束

- [[Black-Scholes模型|C22 Black-Scholes模型]] **—导出局部敏感度→ 本概念**：模型衡量波动率输入变化的局部影响。
- [[隐含波动率（Natenberg）|C17 隐含波动率]] **—变化时经由Vega传导→ 本概念**：隐波平移首先表现为 Vega 损益。
- [[跨式与宽跨式（Natenberg）|C35 跨式与宽跨式]] **—多头通常形成正波动率暴露→ 本概念**：隐波上升通常提高多头结构价值。
- [[波动率合约方差掉期与VIX|C45 波动率合约方差掉期与VIX]] **—提供直接波动率暴露→ 本概念**：波动率和方差产品减少逐期权管理但仍有波动率敏感度。

## 关键公式

$$\mathrm{Vega}=\frac{\partial V}{\partial\sigma}$$

## 风险经理检查

- 统一按 1 个波动率点还是 100% 变动报价；单一 Vega 不能描述偏斜、期限和波动率凸性。
- 把模型数值与可成交价格、压力情景和头寸规模一起复核。

## 主要章节

- [[风险度量（一） Risk Measurement I|第7章 风险度量（一）]]
- [[风险度量（二） Risk Measurement II|第9章 风险度量（二）]]
- [[风险考量 Risk Considerations|第13章 风险考量]]
- [[二叉树期权定价 Binomial Option Pricing|第19章 二叉树期权定价]]
- [[再论波动率 Volatility Revisited|第20章 再论波动率]]
- [[头寸分析 Position Analysis|第21章 头寸分析]]
- [[波动率偏斜 Volatility Skews|第24章 波动率偏斜]]
- [[波动率合约 Volatility Contracts|第25章 波动率合约]]
