---
type: option-strategy
schema_version: 1
name: 保护性看跌 Protective Put
aliases:
  - Protective Put
  - Married Put
  - 保护性看跌
leg_count: 2
option_leg_count: 1
underlying_leg_count: 1
strategy_family: 备兑与保护性组合
status: completed
completion_status: completed
created_from: user-request
created_at: 2026-08-15
updated_at: 2026-08-15
tags: [期权, 期权策略, 二腿策略, 保护性看跌]
domain: 经济
subdomain: 金融
product_domain: 衍生品
instrument: 期权
---

# 保护性看跌 / Protective Put

## 定义

保护性看跌由**买入或持有标的**与**买入一份看跌期权**组成。长 Put 为股票多头设置最低退出价格，同时保留上涨收益。

## 标准腿结构

设买入股票时价格为 $S_0$、买入 Put 的行权价为 $K$、支付权利金为 $p$：

| 腿 | 头寸 |
|---|---:|
| 标的 | $+1$ 单位股票 |
| 看跌期权 | $+1$ Put，行权价 $K$、到期日 $T$ |

## 到期损益

忽略利息、股息、税费和交易成本，

$$
\Pi_T
=S_T-S_0-p+\max(K-S_T,0).
$$

即

$$
\Pi_T=
\begin{cases}
K-S_0-p, & S_T<K,\\
S_T-S_0-p, & S_T\ge K.
\end{cases}
$$

- 最大盈利：上涨侧无上限。
- 最大亏损：$S_0+p-K$，在 $S_T\le K$ 时达到。
- 盈亏平衡点：$S_T=S_0+p$。

若 $K>S_0+p$，结构建立时已含内在价值，上述“最大亏损”应按实际成交现金流重新解释。

## 收益与风险特征

- Put 相当于为股票购买价格保险；保护底线是 $K$，但总成本增加了权利金 $p$。
- 通常为正 Delta、正 Gamma、负日历 Theta、正 Vega。
- 波动率上升通常提高保护性 Put 的价值，但也可能意味着市场下跌风险正在上升，不能只看单一 Greek。
- 若标的派息，实际总回报还应加入股息；除息也会影响 Put 价值与提前行权判断。

## 行权与到期管理

美式 Put 可以提前行权，但通常应先比较剩余时间价值、利息与股息。到期若 Put 价内，自动行权可能卖出股票；若账户希望继续持股，应在截止时间前主动处理。期权乘数必须与股票数量匹配，否则只有部分持仓受到保护。

## 适用场景

适合希望继续持有标的、保留上涨潜力，同时愿意支付固定保险费限制一段时间内最大损失的投资者。保护到期后若仍需保险，展期成本可能显著。

## 关联概念

- [[备兑看涨 Covered Call (Buy-Write)]]：收取权利金但牺牲上涨空间，不提供同等下跌保护。
- [[保护性看涨 Protective Call]]：股票空头的镜像保护结构。
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/知识图谱/保护性备兑与领式|保护性、备兑与领式]]

## 盈亏曲线（到期与到期前）

![[../assets/保护性看跌 Protective Put 盈亏曲线.svg]]

> [!note] 读图口径
> 图中展示买入标的并买入 1 份看跌期权的代表构造。实线为到期损益，虚线为期权尚余 30 天时的理论损益；标的腿按 $S-S_0$ 计。图未计股息、融资、提前行权和交易成本。

## 来源

- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/使用期权进行对冲 Hedging with Options#保护性看涨期权与看跌期权 / Protective Calls and Puts|《Option Volatility and Pricing》：保护性看涨与看跌]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/风险考量 Risk Considerations|风险考量]]
