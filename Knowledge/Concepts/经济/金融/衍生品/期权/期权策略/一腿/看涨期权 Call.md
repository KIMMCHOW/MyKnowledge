---
type: option-strategy
schema_version: 1
name: 看涨期权 Call
aliases:
  - Call
  - Long Call
  - Short Call
  - 买入看涨期权
  - 卖出看涨期权
leg_count: 1
option_leg_count: 1
underlying_leg_count: 0
strategy_family: 单腿期权
status: completed
completion_status: completed
created_at: 2026-08-15
updated_at: 2026-08-15
tags: [期权, 期权策略, 一腿策略, 看涨期权]
domain: 经济
subdomain: 金融
product_domain: 衍生品
instrument: 期权
---

# 看涨期权 / Call

## 定义

看涨期权赋予买方在到期日或到期日前按行权价 $K$ 买入标的的权利；卖方收取权利金并承担被行权或指派后按 $K$ 卖出标的的义务。本页的一腿是一个看涨期权合约系列；多头与空头是同一合约的相反头寸，不另计为两项策略。

## 标准腿结构

设建仓时每股看涨期权权利金为 $c>0$，到期标的价格为 $S_T$：

| 变体 | 数量 | 操作 | 合约 |
| --- | ---: | --- | --- |
| 多头看涨 | 1 | 买入 | Call，行权价 $K$、到期日 $T$ |
| 空头看涨 | 1 | 卖出 | Call，行权价 $K$、到期日 $T$ |

下列公式均按每股计算，未计手续费、滑点、利息、股息和税费；实际金额还需乘以合约乘数。

## 多头看涨到期损益

$$
\Pi_T^{\mathrm{long}}
=\max(S_T-K,0)-c
=
\begin{cases}
-c, & S_T\le K,\\
S_T-K-c, & S_T>K.
\end{cases}
$$

- 最大亏损：$c$，发生在 $S_T\le K$。
- 最大盈利：上涨侧无上限。
- 到期盈亏平衡点：$S_T=K+c$。

多头看涨通常为正 [[Delta]]、正 [[Gamma]]、负日历 [[Theta]]、正 [[Vega]]、正 [[Rho]]。这些是局部敏感度，实际数值会随标的价格、剩余期限、隐含波动率、利率和股息变化。

## 空头看涨到期损益

$$
\Pi_T^{\mathrm{short}}
=c-\max(S_T-K,0)
=
\begin{cases}
c, & S_T\le K,\\
K+c-S_T, & S_T>K.
\end{cases}
$$

- 最大盈利：$c$，发生在 $S_T\le K$。
- 最大亏损：上涨侧无上限。
- 到期盈亏平衡点：$S_T=K+c$。

空头看涨的局部 Greeks 通常与多头相反：负 Delta、负 Gamma、正日历 Theta、负 Vega、负 Rho。“收取权利金”不等于低风险；标的大涨与隐含波动率上升可能同时扩大损失和保证金需求。

## 行权、指派与裸卖风险

- 美式看涨期权可在到期前行权。多头提前行权通常会放弃剩余时间价值；无股息标的通常先卖出期权更经济，但临近除息日的深度价内 Call 需要比较股息与剩余时间价值。
- 空头看涨可能在任何交易日被指派。若没有足量标的覆盖，指派会形成空头股票，并带来无限上涨风险、借券费、召回、强制回补和代付股息风险。
- 到期价格接近 $K$ 时存在夹点风险；是否行权可能在收盘后仍不确定，账户可能在下一交易日留下意外股票头寸。
- 单张合约的乘数、交割方式和账户保证金规则必须单独核对；现金结算指数期权与实物交割股票期权的操作后果不同。

## 与单纯持股的区别

- 多头看涨以有限权利金换取凸性的上涨敞口，但没有股东投票权，通常不直接获得股息，而且会到期并承受时间衰减；它不是持有股票的等价替代。
- 裸空看涨也不等同于卖空股票：$S_T\le K$ 时其收益被封顶在权利金 $c$，而 $S_T>K$ 后才逐步呈现负方向敞口；它还具有负 Gamma、负 Vega 和指派风险。
- 若空头看涨由足量股票覆盖，应改用[[Knowledge/Concepts/经济/金融/衍生品/期权/期权策略/二腿/备兑策略 Covered Strategy#备兑看涨 / Covered Call|备兑看涨]]的组合风险分析；若多头看涨用于保护空头股票，应参见[[Knowledge/Concepts/经济/金融/衍生品/期权/期权策略/二腿/保护性策略 Protective Strategy#保护性看涨 / Protective Call|保护性看涨]]。

## 盈亏曲线（到期与到期前）

### 多头看涨

![[../assets/看涨期权 Call 盈亏曲线.svg]]

### 空头看涨

![[../assets/空头看涨期权 Short Call 盈亏曲线.svg]]

> [!note] 读图口径
> 两图分别展示多头与空头看涨。实线为到期损益，虚线为尚余 30 天时的 Black–Scholes 理论损益；虚线假设隐含波动率、利率和股息率不变，并非收益预测。

## 来源

- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/知识图谱/看涨与看跌期权|看涨与看跌期权]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/到期盈亏 Expiration Profit and Loss|到期盈亏]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/合约规格与期权术语 Contract Specifications and Option Terminology|合约规格与期权术语]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/风险考量 Risk Considerations|风险考量]]
