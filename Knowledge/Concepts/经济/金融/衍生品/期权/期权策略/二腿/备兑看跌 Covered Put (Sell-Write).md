---
type: option-strategy
schema_version: 1
name: 备兑看跌 Covered Put (Sell-Write)
aliases:
  - Covered Put (Sell/Write)
  - Covered Put
  - Sell-Write
  - 备兑看跌
leg_count: 2
option_leg_count: 1
underlying_leg_count: 1
strategy_family: 备兑与保护性组合
status: completed
completion_status: completed
created_from: user-request
created_at: 2026-08-15
updated_at: 2026-08-15
tags: [期权, 期权策略, 二腿策略, 备兑看跌]
domain: 经济
subdomain: 金融
product_domain: 衍生品
instrument: 期权
---

# 备兑看跌 / Covered Put (Sell/Write)

## 定义

传统意义上的备兑看跌由**卖空标的**与**卖出一份看跌期权**组成。它不是“现金担保卖出 Put”；名称中的 covered 只表示 Put 的下跌方向风险由空头股票部分对冲。

## 标准腿结构

设卖空股票时价格为 $S_0$、卖出 Put 的行权价为 $K$、收到权利金为 $p$：

| 腿 | 头寸 |
|---|---:|
| 标的 | $-1$ 单位股票 |
| 看跌期权 | $-1$ Put，行权价 $K$、到期日 $T$ |

## 到期损益

忽略借券费、股息、利息、税费和交易成本，

$$
\Pi_T
=S_0-S_T+p-\max(K-S_T,0).
$$

分段写为

$$
\Pi_T=
\begin{cases}
S_0-K+p, & S_T<K,\\
S_0-S_T+p, & S_T\ge K.
\end{cases}
$$

在常见的 $K<S_0$ 结构下：

- 最大盈利：$S_0-K+p$，在 $S_T\le K$ 时达到。
- 最大亏损：上涨侧无上限，因为空头股票可能无限上涨。
- 盈亏平衡点：$S_T=S_0+p$。

## 收益与风险特征

- 该策略牺牲 $K$ 以下的进一步下跌收益，以权利金换取一定缓冲。
- 通常为负 Delta、负 Gamma、正日历 Theta、负 Vega。
- “备兑”不代表有限风险：上涨亏损仍然无界，且保证金可能在上涨时迅速增加。
- Put 被指派后会买入股票，可能恰好用于回补空头；若合约乘数、账户数量或结算时点不匹配，仍会残留方向头寸。

## 借券与提前指派风险

卖空股票还承担借券费、召回、强制回补（buy-in）、难借证券费率跳升以及代付股息。深度价内美式 Put 在利率较高、剩余时间价值较低时可能提前行权。即使期权风险图看似平坦，这些股票借贷风险也不会消失。

## 适用场景

只适合具备稳定借券来源、能承受上涨无界风险，并愿意在标的跌至 $K$ 以下后锁定收益的账户。若意图只是卖出现金担保 Put，应使用不同的风险分析，不能套用本页结构。

## 关联概念

- [[保护性看涨 Protective Call]]：以长 Call 限制空头股票的上涨损失。
- [[Delta]]、[[Gamma]]、[[Theta]]、[[Vega]]：描述组合的局部风险。
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/知识图谱/保护性备兑与领式|保护性、备兑与领式]]

## 盈亏曲线（到期与到期前）

![[../assets/备兑看跌 Covered Put (Sell-Write) 盈亏曲线.svg]]

> [!note] 读图口径
> 图中展示卖空标的并卖出 1 份看跌期权的传统备兑看跌。实线为到期损益，虚线为期权尚余 30 天时的理论损益；标的腿按 $-(S-S_0)$ 计。图未计借券费、召回、代付股息、提前指派和保证金变化。

## 来源

- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/使用期权进行对冲 Hedging with Options#备兑卖出 / Covered Writes|《Option Volatility and Pricing》：备兑卖出]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/风险考量 Risk Considerations|风险考量]]
