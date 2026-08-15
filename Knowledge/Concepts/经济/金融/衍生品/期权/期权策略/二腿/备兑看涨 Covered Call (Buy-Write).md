---
type: option-strategy
schema_version: 1
name: 备兑看涨 Covered Call (Buy-Write)
aliases:
  - Covered Call (Buy/Write)
  - Covered Call
  - Buy-Write
  - 备兑看涨
leg_count: 2
option_leg_count: 1
underlying_leg_count: 1
strategy_family: 备兑与保护性组合
status: completed
completion_status: completed
created_from: user-request
created_at: 2026-08-15
updated_at: 2026-08-15
tags: [期权, 期权策略, 二腿策略, 备兑看涨]
domain: 经济
subdomain: 金融
product_domain: 衍生品
instrument: 期权
---

# 备兑看涨 / Covered Call (Buy/Write)

## 定义

备兑看涨由**买入或持有标的**与**卖出一份看涨期权**组成。Buy/Write 指两腿同时建立；若先持有股票后再卖 Call，经济结构相同。

## 标准腿结构

设建仓时标的价格为 $S_0$、卖出 Call 的行权价为 $K$、收到权利金为 $c$：

| 腿 | 头寸 |
|---|---:|
| 标的 | $+1$ 单位股票 |
| 看涨期权 | $-1$ Call，行权价 $K$、到期日 $T$ |

一份期权对应的标的数量必须按合约乘数配足，否则未覆盖部分仍是裸空 Call。

## 到期损益

忽略利息、股息、税费和交易成本，到期损益为

$$
\Pi_T
=S_T-S_0+c-\max(S_T-K,0).
$$

分段写为

$$
\Pi_T=
\begin{cases}
S_T-S_0+c, & S_T\le K,\\
K-S_0+c, & S_T>K.
\end{cases}
$$

- 最大盈利：$K-S_0+c$，在 $S_T\ge K$ 时达到。
- 最大亏损：$S_0-c$，在标的跌至 $0$ 时发生。
- 盈亏平衡点：$S_T=S_0-c$。

## 收益与风险特征

- 收取权利金降低持仓成本，但把 $K$ 以上的上涨收益让给 Call 买方。
- 通常为正 Delta、负 Gamma、正日历 Theta、负 Vega；实际数值随行权价和期限变化。
- 下跌风险仍接近直接持股。权利金只是有限缓冲，不能称为下行保护。
- 除息、借券、税务和股票股息会改变真实现金流；公式中的 $S_0-c$ 不是所有账户口径下的税务成本基础。

## 提前指派与执行

美式 Call 在临近除息日、深度价内且剩余时间价值很低时更可能被提前行权。被指派会卖出股票，可能触发税务、失去股息或使剩余股票数量与期权乘数不匹配。平仓时宜把两腿作为组合报价，避免先后成交造成短暂裸露。

## 适用场景

适合愿意在 $K$ 附近卖出持股、对短期上涨空间判断有限且接受完整下跌风险的投资者。它不是“免费收益”，也不适合不愿失去股票或无法承受大幅回撤的账户。

## 关联概念

- [[保护性看跌 Protective Put]]：保留下行保护和无限上涨，成本结构相反。
- [[Delta]]、[[Gamma]]、[[Theta]]、[[Vega]]：描述组合的局部风险。
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/知识图谱/保护性备兑与领式|保护性、备兑与领式]]

## 盈亏曲线（到期与到期前）

![[../assets/备兑看涨 Covered Call (Buy-Write) 盈亏曲线.svg]]

> [!note] 读图口径
> 图中展示买入标的并卖出 1 份看涨期权的代表构造。实线为到期损益，虚线为期权尚余 30 天时的 Black–Scholes 理论损益；标的腿按 $S-S_0$ 计。图未计股息、融资、提前指派和交易成本。

## 来源

- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/使用期权进行对冲 Hedging with Options#备兑卖出 / Covered Writes|《Option Volatility and Pricing》：备兑卖出]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/风险考量 Risk Considerations|风险考量]]
