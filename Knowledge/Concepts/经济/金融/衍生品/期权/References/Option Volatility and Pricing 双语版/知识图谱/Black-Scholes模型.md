---
title: "Black-Scholes模型 / Black-Scholes Model"
graph_layer: 4
tags: [期权知识图谱, 核心概念]
generated_by: "tools/build_option_knowledge_graph.py"
---

# Black-Scholes模型 / Black-Scholes Model

> [!definition] 定义
> 在连续交易、对数正态扩散及确定利率和波动率等假设下，通过动态复制给出欧式期权价值和 Greeks。

## 核心关系

### 向下游传导

- **计算 →** [[期望值与理论价值|期望值与理论价值]]：Black–Scholes 把输入映射为理论价值。
- **提供反解机制 →** [[隐含波动率（Natenberg）|隐含波动率]]：隐波是模型依赖的报价坐标。
- **导出局部敏感度 →** [[Delta（Natenberg）|Delta]]：模型对标的价格求一阶敏感度。
- **导出局部敏感度 →** [[Gamma（Natenberg）|Gamma]]：模型对标的价格求二阶敏感度。
- **导出局部敏感度 →** [[Theta（Natenberg）|Theta]]：模型衡量时间流逝的局部影响。
- **导出局部敏感度 →** [[Vega（Natenberg）|Vega]]：模型衡量波动率输入变化的局部影响。
- **导出局部敏感度 →** [[Rho|Rho]]：模型衡量利率输入变化的局部影响。

### 受上游约束

- [[波动率预测|波动率预测]] **—提供波动率假设→ 本概念**：预测波动率可作为正向估值输入。

## 关键公式

$$C=S_0e^{-qT}N(d_1)-Ke^{-rT}N(d_2)$$\n$$d_1=\frac{\ln(S_0/K)+(r-q+\tfrac12\sigma^2)T}{\sigma\sqrt T},\quad d_2=d_1-\sigma\sqrt T$$

## 风险经理检查

- 逐项记录假设偏离：跳空、随机波动率、交易成本、离散对冲、利率曲线和美式行权。
- 把模型数值与可成交价格、压力情景和头寸规模一起复核。

## 主要章节

- [[05-理论定价模型 Theoretical Pricing Models|第5章 理论定价模型]]
- [[18-Black–Scholes 模型 The Black-Scholes Model|第18章 Black–Scholes 模型]]
- [[23-模型与现实世界 Models and the Real World|第23章 模型与现实世界]]
- [[24-波动率偏斜 Volatility Skews|第24章 波动率偏斜]]
