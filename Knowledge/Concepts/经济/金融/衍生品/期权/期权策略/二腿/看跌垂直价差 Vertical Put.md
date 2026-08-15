---
type: option-strategy
schema_version: 1
name: 看跌垂直价差
aliases:
  - Vertical Put
  - Put Vertical Spread
  - 看跌期权垂直价差
leg_count: 2
option_leg_count: 2
underlying_leg_count: 0
strategy_family: 垂直价差
status: completed
created_at: 2026-08-15
updated_at: 2026-08-15
tags:
  - 期权
  - 期权策略
  - 二腿策略
  - 垂直价差
domain: 经济
subdomain: 金融
---

# 看跌垂直价差 / Vertical Put

## 定义

看跌垂直价差由**同一标的、同一到期日、不同执行价**的两份看跌期权组成。两腿数量相等，使持有至到期的盈利与亏损均受两个执行价之差约束。

以下记 $K_1<K_2$，$p_1,p_2$ 为建仓时每股期权费，$S_T$ 为到期标的价格，$x^+=\max(x,0)$。公式均为**每股、未计佣金和滑点**的损益；标准合约还需乘以合约乘数。

## 标准腿结构

常见的看跌熊市价差（debit put spread）为：

| 腿 | 操作 | 执行价 | 到期日 |
| --- | --- | --- | --- |
| 1 | 买入 1 份看跌期权 | $K_2$ | $T$ |
| 2 | 卖出 1 份看跌期权 | $K_1$ | $T$ |

净借记为 $D=p_2-p_1>0$。

## 损益公式

看跌熊市价差的到期损益为：

$$
\Pi_T=(K_2-S_T)^+-(K_1-S_T)^+-D
$$

分段形式为：

$$
\Pi_T=
\begin{cases}
K_2-K_1-D, & S_T\le K_1,\\
K_2-S_T-D, & K_1<S_T<K_2,\\
-D, & S_T\ge K_2.
\end{cases}
$$

## 方向与变体

- **看空／净借记**：买入 $K_2$、卖出 $K_1$，适合预期标的温和下跌且希望限定风险的情形。
- **看多／净贷记**：卖出 $K_2$、买入 $K_1$，即上述头寸的反向，也称看跌牛市价差。收到净权利金 $C=p_2-p_1>0$。

实际订单应按两腿方向及成交后的净现金流确认是借记还是贷记。

## 最大盈亏与盈亏平衡

对于看空／净借记变体：

- 最大亏损：$D$，发生在 $S_T\ge K_2$。
- 最大盈利：$(K_2-K_1)-D$，发生在 $S_T\le K_1$。
- 到期盈亏平衡点：$K_2-D$。

对于看多／净贷记变体：

- 最大盈利：净贷记 $C$，发生在 $S_T\ge K_2$。
- 最大亏损：$(K_2-K_1)-C$，发生在 $S_T\le K_1$。
- 到期盈亏平衡点：$K_2-C$。

这些边界以持有至共同到期日、两腿数量相等且不发生提前行权为前提。

## Greeks、波动率与时间

看空变体的 Delta 通常为负；其他 Greeks 等于高执行价多头看跌与低执行价空头看跌的净值。Gamma、Vega、Theta 的符号取决于标的相对两个执行价的位置、期限与波动率曲面，可能随行情翻转。两腿的波动率和时间价值风险会部分抵消，但临近执行价或到期时，局部 Gamma、Theta 与偏斜风险仍可能很大。

## 执行与风险

- 使用组合限价单并核对净借记／净贷记，减少逐腿成交风险。
- 美式空头看跌腿可能提前被指派，尤其在深度实值、利率较高且剩余时间价值很少时。
- 被指派后可能形成多头股票及相应融资需求；多头保护腿不会保证被券商自动行权或同步处理。
- 到期时标的贴近执行价会带来 pin risk 和不确定的隔夜股票头寸。
- 流动性较差、报价宽、保证金规则与交易费用都可能改变实际风险收益比。

## 盈亏曲线（到期与到期前）

![[../assets/看跌垂直价差 Vertical Put 盈亏曲线.svg]]

> [!note] 读图口径
> 图中展示熊市借记看跌价差。实线为到期损益，虚线为尚余 30 天时的 Black–Scholes 理论损益。信用方向、其他行权价间距及波动率曲面需要单独重估。

## 来源

- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/牛市与熊市价差 Bull and Bear Spreads#垂直价差 / Vertical Spreads|《期权波动率与定价》：垂直价差]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/价差策略导论 Introduction to Spreading|《期权波动率与定价》：价差策略导论]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/风险考量 Risk Considerations|《期权波动率与定价》：风险考量]]
