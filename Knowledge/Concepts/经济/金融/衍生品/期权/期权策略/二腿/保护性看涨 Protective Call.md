---
type: option-strategy
schema_version: 1
name: 保护性看涨 Protective Call
aliases:
  - Protective Call
  - Married Call
  - 保护性看涨
leg_count: 2
option_leg_count: 1
underlying_leg_count: 1
strategy_family: 备兑与保护性组合
status: completed
completion_status: completed
created_from: user-request
created_at: 2026-08-15
updated_at: 2026-08-15
tags: [期权, 期权策略, 二腿策略, 保护性看涨]
domain: 经济
subdomain: 金融
product_domain: 衍生品
instrument: 期权
---

# 保护性看涨 / Protective Call

## 定义

保护性看涨由**卖空标的**与**买入一份看涨期权**组成。长 Call 为股票空头设置上涨侧回补上限，结构与“保护性看跌”在方向上镜像。

## 标准腿结构

设卖空股票时价格为 $S_0$、买入 Call 的行权价为 $K$、支付权利金为 $c$：

| 腿 | 头寸 |
|---|---:|
| 标的 | $-1$ 单位股票 |
| 看涨期权 | $+1$ Call，行权价 $K$、到期日 $T$ |

## 到期损益

忽略借券费、股息、利息、税费和交易成本，

$$
\Pi_T
=S_0-S_T-c+\max(S_T-K,0).
$$

即

$$
\Pi_T=
\begin{cases}
S_0-S_T-c, & S_T\le K,\\
S_0-K-c, & S_T>K.
\end{cases}
$$

在常见的 $K>S_0$ 保护结构下：

- 最大盈利：$S_0-c$，在标的跌至 $0$ 时达到。
- 最大亏损：$K-S_0+c$，在 $S_T\ge K$ 时达到。
- 盈亏平衡点：$S_T=S_0-c$。

## 收益与风险特征

- 长 Call 将空头股票的上涨损失封顶，同时保留下跌获利空间。
- 保护成本为 $c$，会降低空头股票在下跌时的收益。
- 组合通常为负 Delta、正 Gamma、负日历 Theta、正 Vega；当 Call 深度价内后，净 Delta 会趋近于 $0$。
- 期权层面的最大损失有限，但股票借贷风险仍可能制造额外损失。

## 借券、指派与结算

空头股票可能遭遇借券费上升、召回、强制回补以及代付股息。若保护性 Call 为美式，可以主动行权获得股票用于回补，但提前行权通常会放弃剩余时间价值；多数情况下卖出 Call 后直接回补股票更经济。到期自动行权、股票回补和期权结算的时间错配也可能留下隔夜头寸。

## 适用场景

适合已有股票空头、愿意支付确定成本来限制逼空或跳空上涨风险的账户。若借券极不稳定，单靠长 Call 不能消除操作风险。

## 关联概念

- [[备兑看跌 Covered Put (Sell-Write)]]：同样含股票空头，但卖出 Put 而不是买入 Call。
- [[保护性看跌 Protective Put]]：多头股票的镜像保护结构。
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/知识图谱/保护性备兑与领式|保护性、备兑与领式]]

## 盈亏曲线（到期与到期前）

![[../assets/保护性看涨 Protective Call 盈亏曲线.svg]]

> [!note] 读图口径
> 图中展示卖空标的并买入 1 份看涨期权的代表构造。实线为到期损益，虚线为期权尚余 30 天时的理论损益；期权封住价格上涨损失，但图未计借券费、召回、代付股息与结算错配。

## 来源

- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/使用期权进行对冲 Hedging with Options#保护性看涨期权与看跌期权 / Protective Calls and Puts|《Option Volatility and Pricing》：保护性看涨与看跌]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/风险考量 Risk Considerations|风险考量]]
