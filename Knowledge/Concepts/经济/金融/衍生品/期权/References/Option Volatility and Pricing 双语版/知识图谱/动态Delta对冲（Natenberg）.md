---
title: "动态Delta对冲 / Dynamic Delta Hedging"
graph_layer: 5
tags: [期权知识图谱, 核心概念]
generated_by: "tools/build_option_knowledge_graph.py"
---

# 动态Delta对冲 / Dynamic Delta Hedging

> [!definition] 定义
> 根据模型 Delta 买卖标的并持续再平衡，使头寸在局部保持方向中性，并把价格路径转化为调整现金流。

## 核心关系

### 向下游传导

- **局部中和 →** [[Delta（Natenberg）|Delta]]：再平衡把净 Delta 拉回目标区间。
- **通过换手产生 →** [[流动性执行与结算风险|流动性执行与结算风险]]：每次再平衡消耗价差、费用和市场冲击。

### 受上游约束

- [[历史与已实现波动率|历史与已实现波动率]] **—相对入场隐波决定波动捕获→ 本概念**：实现路径与入场定价的差异通过再平衡损益体现。
- [[隐含波动率（Natenberg）|隐含波动率]] **—设定波动交易盈亏平衡基准→ 本概念**：入场隐波决定时间价值与预期调整收入的平衡。
- [[Delta（Natenberg）|Delta]] **—决定对冲数量→ 本概念**：Delta 是局部等价标的头寸。
- [[Gamma（Natenberg）|Gamma]] **—提高再平衡需求→ 本概念**：高 Gamma 使对冲更快失衡。
- [[流动性执行与结算风险|流动性执行与结算风险]] **—造成离散对冲误差→ 本概念**：跳空、滑点和市场关闭使理论对冲无法连续执行。

## 关键公式

$$n_{\mathrm{hedge}}=-\Delta_{\mathrm{option}}$$\n$$dV\approx\Delta\,dS+\tfrac12\Gamma(dS)^2+\Theta\,dt+\mathrm{Vega}\,d\sigma$$

## 风险经理检查

- 设定时间或 Delta 阈值并计入滑点；Delta 中性不消除 Gamma、Vega、跳空、模型和流动性风险。
- 把模型数值与可成交价格、压力情景和头寸规模一起复核。

## 主要章节

- [[08-动态对冲 Dynamic Hedging|第8章 动态对冲]]
- [[13-风险考量 Risk Considerations|第13章 风险考量]]
- [[25-波动率合约 Volatility Contracts|第25章 波动率合约]]
