---
title: "波动率合约方差掉期与VIX / Volatility Contracts, Variance Swaps, and VIX"
concept_id: C45
graph_layer: 7
tags: [期权知识图谱, 核心概念]
generated_by: "tools/build_option_knowledge_graph.py"
---

# 波动率合约方差掉期与VIX / Volatility Contracts, Variance Swaps, and VIX

> [!definition] 定义
> 已实现波动率或方差合约直接按观察期结果结算；VIX 及其期货期权提供基于期权条带的隐含波动率暴露。

## 核心关系

### 向下游传导

- **提供直接波动率暴露 →** [[Vega（Natenberg）|C29 Vega]]：波动率和方差产品减少逐期权管理但仍有波动率敏感度。
- **承担结算与复制风险 →** [[流动性执行与结算风险|C43 流动性执行与结算风险]]：观察窗口、公式与流动性影响最终实现。

### 受上游约束

- [[历史与已实现波动率|C15 历史与已实现波动率]] **—作为结算基础→ 本概念**：已实现波动率或方差合约按观察结果结算。
- [[隐含波动率（Natenberg）|C17 隐含波动率]] **—作为定价基础→ 本概念**：VIX 及隐含波动率产品来自期权价格。
- [[看涨与看跌期权|C03 看涨与看跌期权]] **—通过跨行权价组合复制→ 本概念**：期权条带可近似复制方差暴露。
- [[期限结构与远期波动率|C18 期限结构与远期波动率]] **—塑造期货期限结构→ 本概念**：VIX 期货反映不同到期的波动率定价。

## 关键公式

$$\mathrm{Payoff}_{\mathrm{variance}}=N_{\mathrm{var}}\left(\sigma^2_{\mathrm{real}}-K_{\mathrm{var}}\right)$$

## 风险经理检查

- 区分波动率与方差名义金额；核对结算窗口、VIX 现货与期货基差、期限结构、凸性和复制误差。
- 把模型数值与可成交价格、压力情景和头寸规模一起复核。

## 主要章节

- [[25-波动率合约 Volatility Contracts|第25章 波动率合约]]
