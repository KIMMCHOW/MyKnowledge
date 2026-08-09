---
title: "Theta / Theta"
graph_layer: 5
tags: [期权知识图谱, 核心概念]
generated_by: "tools/build_option_knowledge_graph.py"
---

# Theta / Theta

> [!definition] 定义
> Theta 衡量其他条件不变时，日历时间流逝对期权价值的局部影响，通常与 Gamma 暴露形成权衡。

## 核心关系

### 向下游传导

- **汇总为组合暴露 →** [[组合Greeks与头寸分析|组合Greeks与头寸分析]]：各腿 Theta 形成时间衰减预算。

### 受上游约束

- [[Black-Scholes模型|Black-Scholes模型]] **—导出局部敏感度→ 本概念**：模型衡量时间流逝的局部影响。
- [[Gamma（Natenberg）|Gamma]] **—通常伴随反向暴露→ 本概念**：同一模型条件下正 Gamma 通常伴随负 Theta。
- [[到期时间与行权方式|到期时间与行权方式]] **—通过时间流逝实现→ 本概念**：剩余期限减少会改变期权价值。
- [[跨式与宽跨式（Natenberg）|跨式与宽跨式]] **—多头通常承担时间衰减→ 本概念**：若运动不足，权利金随时间损耗。

## 关键公式

$$\Theta=\frac{\partial V}{\partial t}$$

## 风险经理检查

- 确认按自然日还是交易日表达及符号约定；正 Theta 不是无风险收益，常伴随负凸性或尾部风险。
- 把模型数值与可成交价格、压力情景和头寸规模一起复核。

## 主要章节

- [[07-风险度量（一） Risk Measurement I|第7章 风险度量（一）]]
- [[09-风险度量（二） Risk Measurement II|第9章 风险度量（二）]]
- [[13-风险考量 Risk Considerations|第13章 风险考量]]
- [[18-Black–Scholes 模型 The Black-Scholes Model|第18章 Black–Scholes 模型]]
- [[19-二叉树期权定价 Binomial Option Pricing|第19章 二叉树期权定价]]
- [[21-头寸分析 Position Analysis|第21章 头寸分析]]
