---
title: "Delta / Delta"
graph_layer: 5
tags: [期权知识图谱, 核心概念]
generated_by: "tools/build_option_knowledge_graph.py"
---

# Delta / Delta

> [!definition] 定义
> Delta 衡量期权价值对标的价格的局部一阶敏感度，也常作为等价标的头寸和动态对冲比率。

## 核心关系

### 向下游传导

- **决定对冲数量 →** [[动态Delta对冲（Natenberg）|动态Delta对冲]]：Delta 是局部等价标的头寸。
- **与价格共同定义 →** [[Lambda|Lambda]]：Lambda 将绝对 Delta 转为百分比弹性。
- **汇总为组合暴露 →** [[组合Greeks与头寸分析|组合Greeks与头寸分析]]：各腿 Delta 按数量和乘数相加。

### 受上游约束

- [[Black-Scholes模型|Black-Scholes模型]] **—导出局部敏感度→ 本概念**：模型对标的价格求一阶敏感度。
- [[二叉树与风险中性估值|二叉树与风险中性估值]] **—以节点差分估计→ 本概念**：树上价值变化可估计 Delta。
- [[Gamma（Natenberg）|Gamma]] **—决定Delta漂移速度→ 本概念**：Gamma 把标的变动传导为 Delta 变化。
- [[动态Delta对冲（Natenberg）|动态Delta对冲]] **—局部中和→ 本概念**：再平衡把净 Delta 拉回目标区间。
- [[垂直价差与牛熊价差|垂直价差与牛熊价差]] **—主要形成方向暴露→ 本概念**：垂直价差用有界损益表达看多或看空观点。
- [[保护性备兑与领式|保护性备兑与领式]] **—变换标的方向风险→ 本概念**：保护、备兑和领式改变组合 Delta。

## 关键公式

$$\Delta=\frac{\partial V}{\partial S}$$

## 风险经理检查

- Delta 只在当前点局部有效；统一现货/期货 Delta、合约乘数、币种和正负方向。
- 把模型数值与可成交价格、压力情景和头寸规模一起复核。

## 主要章节

- [[07-风险度量（一） Risk Measurement I|第7章 风险度量（一）]]
- [[08-动态对冲 Dynamic Hedging|第8章 动态对冲]]
- [[09-风险度量（二） Risk Measurement II|第9章 风险度量（二）]]
- [[18-Black–Scholes 模型 The Black-Scholes Model|第18章 Black–Scholes 模型]]
- [[19-二叉树期权定价 Binomial Option Pricing|第19章 二叉树期权定价]]
- [[21-头寸分析 Position Analysis|第21章 头寸分析]]
- [[24-波动率偏斜 Volatility Skews|第24章 波动率偏斜]]
