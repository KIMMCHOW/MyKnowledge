---
type: option-strategy
schema_version: 1
name: 备兑策略
aliases:
  - Covered Strategy
  - Covered Call
  - Covered Call (Buy/Write)
  - 备兑看涨 Covered Call (Buy-Write)
  - Buy-Write
  - 备兑看涨
  - Covered Put
  - Covered Put (Sell/Write)
  - 备兑看跌 Covered Put (Sell-Write)
  - Sell-Write
  - 备兑看跌
leg_count: 2
option_leg_count: 1
underlying_leg_count: 1
strategy_family: 备兑策略
status: completed
completion_status: completed
created_from: merged-call-put-pages
created_at: 2026-08-15
updated_at: 2026-08-15
tags: [期权, 期权策略, 二腿策略, 备兑策略]
domain: 经济
subdomain: 金融
product_domain: 衍生品
instrument: 期权
---

# 备兑策略 / Covered Strategy

## 定义与命名

备兑策略由一条标的头寸与一条**空头期权**组成，标的数量应与期权合约乘数匹配。若一份合约对应 $m$ 单位标的，下文的“$1$ 单位”实际建仓时应同时乘以 $m$。

- **备兑看涨（covered call）**：多头标的 $+$ 空头 Call。
- **备兑看跌（covered put）**：空头标的 $+$ 空头 Put。

> [!important] Call／Put 是构造，不是策略方向
> 名称中的 Call 或 Put 只说明卖出了哪种期权。组合的方向风险必须由两条腿共同判断：备兑看涨通常是有限上涨、保留主要下跌风险；备兑看跌则是有限下跌收益、承担上涨无界风险。

设建仓时标的价格为 $S_0$，到期价格为 $S_T$，行权价为 $K$，Call 和 Put 的建仓权利金分别为 $c>0$ 与 $p>0$，并记

$$
x^+=\max(x,0).
$$

以下均按每单位标的计算，忽略利息、股息、借券费、税费和交易成本。

## 两种标准构造

| 构造 | 标的腿 | 期权腿 | 到期前的组合损益 |
| --- | ---: | ---: | --- |
| 备兑看涨 | $+S$ | $-C(K,T)$ | $\Pi_t=(S_t-C_t)-(S_0-c)$ |
| 备兑看跌 | $-S$ | $-P(K,T)$ | $\Pi_t=(-S_t-P_t)-(-S_0-p)$ |

Buy/Write 表示同时买入标的并卖出 Call；Sell/Write 表示同时卖空标的并卖出 Put。若标的头寸早已存在，其经济风险与对应的两腿组合相同，但税务成本基础可能不同。

## 备兑看涨 / Covered Call

### 到期损益

$$
\Pi_T^{\mathrm{CC}}
=S_T-S_0+c-(S_T-K)^+
=\min(S_T,K)-S_0+c.
$$

$$
\Pi_T^{\mathrm{CC}}=
\begin{cases}
S_T-S_0+c, & S_T\le K,\\
K-S_0+c, & S_T>K.
\end{cases}
$$

- 最大盈利：$K-S_0+c$，在 $S_T\ge K$ 时达到。
- 最小到期损益：$c-S_0$，在 $S_T=0$ 时达到；常见 $c<S_0$ 时，最大亏损为 $S_0-c$。
- 盈亏平衡点：$S_T=S_0-c$。

空头 Call 收取的权利金只提供有限的下跌缓冲，同时把 $K$ 以上的上涨收益让给 Call 持有人。它不是“有下行保护的持股”。

### Greeks

以标的 Delta 为 $1$、忽略标的的 Gamma、Theta 和 Vega，则

$$
\Delta_{\mathrm{CC}}=1-\Delta_C,
\qquad
\Gamma_{\mathrm{CC}}=-\Gamma_C,
$$

$$
\Theta_{\mathrm{CC}}=-\Theta_C,
\qquad
\mathrm{Vega}_{\mathrm{CC}}=-\mathrm{Vega}_C.
$$

对普通未到期 Call，该组合通常为正 Delta、负 Gamma、正日历 Theta、负 Vega。

### 提前指派与股息

空头美式 Call 可被提前指派；在除息日前、Call 深度价内且剩余时间价值很低时，这种风险尤其值得注意。被指派后标的通常会以 $K$ 卖出，可能造成失去股息、税务变化或合约乘数与剩余股数不匹配。

### 盈亏曲线（到期与到期前）

![[../assets/备兑看涨 Covered Call (Buy-Write) 盈亏曲线.svg]]

> [!note] 读图口径
> 实线为到期损益，虚线为期权尚余 30 天时的 Black–Scholes 理论损益。图中未计股息、融资、提前指派和交易成本。

## 备兑看跌 / Covered Put

### 不是现金担保卖 Put

> [!warning] 两种结构不能混用
> 本页的传统 **covered put** 是**卖空标的 $+$ 卖出 Put**。**Cash-secured put（现金担保卖出看跌期权）**则是现金或短期国债 $+$ 卖出 Put：它没有空头股票腿，不承担借券、召回或上涨时的股票空头无界亏损。两者不是同一策略。

### 到期损益

$$
\Pi_T^{\mathrm{CP}}
=S_0-S_T+p-(K-S_T)^+.
$$

$$
\Pi_T^{\mathrm{CP}}=
\begin{cases}
S_0-K+p, & S_T<K,\\
S_0-S_T+p, & S_T\ge K.
\end{cases}
$$

- 下跌侧最大盈利：$S_0-K+p$，在 $S_T\le K$ 时达到；若该数为负，它只是组合的最高到期损益，不是正收益。
- 最大亏损：上涨侧无上限，因为标的空头的亏损不封顶。
- 盈亏平衡点：在 $S_0+p\ge K$ 时为 $S_T=S_0+p$；若不满足该条件，这一忽略融资的简化模型中没有非负损益的平衡点。

空头 Put 把 $K$ 以下的进一步下跌收益让给 Put 持有人，但收取权利金。“备兑”不代表风险有限：标的上涨时，空头股票的损失仍然无界。

### Greeks

$$
\Delta_{\mathrm{CP}}=-1-\Delta_P,
\qquad
\Gamma_{\mathrm{CP}}=-\Gamma_P,
$$

$$
\Theta_{\mathrm{CP}}=-\Theta_P,
\qquad
\mathrm{Vega}_{\mathrm{CP}}=-\mathrm{Vega}_P.
$$

由于 $-1<\Delta_P<0$，该组合通常为负 Delta、负 Gamma、正日历 Theta、负 Vega。

### 提前指派、借券与结算

深度价内、剩余时间价值很低的美式 Put 可能被提前指派。被指派时会以 $K$ 买入标的，理论上可用于回补空头；若乘数、数量、结算时点或账户权限不匹配，仍会残留方向头寸。

标的空头还承担借券费、难借费率跳升、召回、强制回补（buy-in）和代付股息等风险。这些风险不会因 Put 腿“被备兑”而消失。

### 盈亏曲线（到期与到期前）

![[../assets/备兑看跌 Covered Put (Sell-Write) 盈亏曲线.svg]]

> [!note] 读图口径
> 实线为到期损益，虚线为期权尚余 30 天时的理论损益。图中未计借券费、召回、代付股息、提前指派和保证金变化。

## 实务检查

1. 用合约乘数核对标的数量，将未覆盖的短 Call 或未匹配的空头股票单独识别。
2. 同时记录行权价、到期日、权利金、股息日和借券条件，不只看平台的“最大收益”。
3. 组合平仓时优先使用多腿限价单，避免逐腿成交留下短暂裸露。

## 关联概念

- [[保护性策略 Protective Strategy]]：用长期权封住标的头寸的一侧损失。
- [[Knowledge/Concepts/经济/金融/衍生品/期权/希腊字母/一阶/Delta|Delta]]、[[Knowledge/Concepts/经济/金融/衍生品/期权/希腊字母/二阶/Gamma|Gamma]]、[[Knowledge/Concepts/经济/金融/衍生品/期权/希腊字母/一阶/Theta|Theta]]、[[Knowledge/Concepts/经济/金融/衍生品/期权/希腊字母/一阶/Vega|Vega]]：描述组合的局部风险。
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/知识图谱/保护性备兑与领式|保护性、备兑与领式]]

## 来源

- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/使用期权进行对冲 Hedging with Options#备兑卖出 / Covered Writes|《Option Volatility and Pricing》：备兑卖出]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/风险考量 Risk Considerations|风险考量]]
