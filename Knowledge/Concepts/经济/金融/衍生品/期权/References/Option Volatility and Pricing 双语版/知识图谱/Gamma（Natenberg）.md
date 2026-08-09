---
title: "Gamma / Gamma"
concept_id: C27
graph_layer: 5
tags: [期权知识图谱, 核心概念]
generated_by: "tools/build_option_knowledge_graph.py"
---

# Gamma / Gamma

> [!definition] 定义
> Gamma 衡量 Delta 对标的价格的变化率，是头寸凸性以及再平衡需求的核心指标。

## 核心关系

### 向下游传导

- **决定Delta漂移速度 →** [[Delta（Natenberg）|C26 Delta]]：Gamma 把标的变动传导为 Delta 变化。
- **提高再平衡需求 →** [[动态Delta对冲（Natenberg）|C33 动态Delta对冲]]：高 Gamma 使对冲更快失衡。
- **通常伴随反向暴露 →** [[Theta（Natenberg）|C28 Theta]]：同一模型条件下正 Gamma 通常伴随负 Theta。
- **汇总为组合暴露 →** [[组合Greeks与头寸分析|C32 组合Greeks与头寸分析]]：各腿 Gamma 形成组合凸性。

### 受上游约束

- [[Black-Scholes模型|C22 Black-Scholes模型]] **—导出局部敏感度→ 本概念**：模型对标的价格求二阶敏感度。
- [[二叉树与风险中性估值|C23 二叉树与风险中性估值]] **—以节点差分估计→ 本概念**：相邻 Delta 变化可估计 Gamma。
- [[跨式与宽跨式（Natenberg）|C35 跨式与宽跨式]] **—多头通常形成正凸性→ 本概念**：多头跨式和宽跨式受益于大幅运动。
- [[蝶式与鹰式|C36 蝶式与鹰式]] **—表达局部曲率→ 本概念**：多执行价结构把 Gamma 集中在特定区间。
- [[比率价差与圣诞树|C38 比率价差与圣诞树]] **—可能形成非对称尾部凸性→ 本概念**：不等数量使一侧远端风险突出。

## 关键公式

$$\Gamma=\frac{\partial^2V}{\partial S^2}=\frac{\partial\Delta}{\partial S}$$

## 风险经理检查

- 临近到期和平值附近 Gamma 可急剧集中；对大幅跳空使用全重估，不能只依赖二阶近似。
- 把模型数值与可成交价格、压力情景和头寸规模一起复核。

## 主要章节

- [[风险度量（一） Risk Measurement I|第7章 风险度量（一）]]
- [[风险度量（二） Risk Measurement II|第9章 风险度量（二）]]
- [[风险考量 Risk Considerations|第13章 风险考量]]
- [[Black–Scholes 模型 The Black-Scholes Model|第18章 Black–Scholes 模型]]
- [[二叉树期权定价 Binomial Option Pricing|第19章 二叉树期权定价]]
- [[头寸分析 Position Analysis|第21章 头寸分析]]
- [[波动率偏斜 Volatility Skews|第24章 波动率偏斜]]
