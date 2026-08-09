---
title: "跨式与宽跨式 / Straddles and Strangles"
concept_id: C35
graph_layer: 6
tags: [期权知识图谱, 核心概念]
generated_by: "tools/build_option_knowledge_graph.py"
---

# 跨式与宽跨式 / Straddles and Strangles

> [!definition] 定义
> 同时持有相同或不同执行价的看涨和看跌，主要表达实际波动相对入场隐含波动的观点。

## 核心关系

### 向下游传导

- **多头通常形成正凸性 →** [[Gamma（Natenberg）|C27 Gamma]]：多头跨式和宽跨式受益于大幅运动。
- **多头通常形成正波动率暴露 →** [[Vega（Natenberg）|C29 Vega]]：隐波上升通常提高多头结构价值。
- **多头通常承担时间衰减 →** [[Theta（Natenberg）|C28 Theta]]：若运动不足，权利金随时间损耗。
- **汇总成风险画像 →** [[组合Greeks与头寸分析|C32 组合Greeks与头寸分析]]：波动率策略不能只用名称判断风险。

## 关键公式

$$\Pi_{\mathrm{long\ straddle}}=|S_T-K|-(C_0+P_0)$$

## 风险经理检查

- 不能只判断方向幅度；要比较隐含波动率、时间衰减、偏斜、再对冲成本和达到盈亏平衡所需路径。
- 把模型数值与可成交价格、压力情景和头寸规模一起复核。

## 主要章节

- [[11-波动率价差策略 Volatility Spreads|第11章 波动率价差策略]]
- [[23-模型与现实世界 Models and the Real World|第23章 模型与现实世界]]
