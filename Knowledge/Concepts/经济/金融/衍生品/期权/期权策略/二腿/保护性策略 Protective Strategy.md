---
type: option-strategy
schema_version: 1
name: 保护性策略
aliases:
  - Protective Strategy
  - Protective Put
  - 保护性看跌 Protective Put
  - Married Put
  - 保护性看跌
  - Protective Call
  - 保护性看涨 Protective Call
  - Married Call
  - 保护性看涨
leg_count: 2
option_leg_count: 1
underlying_leg_count: 1
strategy_family: 保护性策略
status: completed
completion_status: completed
created_from: merged-call-put-pages
created_at: 2026-08-15
updated_at: 2026-08-15
tags: [期权, 期权策略, 二腿策略, 保护性策略]
domain: 经济
subdomain: 金融
product_domain: 衍生品
instrument: 期权
---

# 保护性策略 / Protective Strategy

## 定义与命名

保护性策略由一条标的头寸与一条**多头期权**组成，用于把标的头寸在不利方向上的价格损失封顶。若一份期权对应 $m$ 单位标的，标的数量必须按合约乘数匹配，否则只有部分头寸受到保护。

- **保护性看跌（protective put）**：多头标的 $+$ 多头 Put。
- **保护性看涨（protective call）**：空头标的 $+$ 多头 Call。

> [!important] Call／Put 是构造，不是策略方向
> 名称中的 Call 或 Put 只说明买入了哪种期权。方向暴露由标的腿与期权腿共同决定：保护性 Put 保留上涨潜力并封住下跌侧损失；保护性 Call 保留下跌获利空间并封住上涨侧损失。

设建仓时标的价格为 $S_0$，到期价格为 $S_T$，行权价为 $K$，Call 和 Put 的建仓权利金分别为 $c>0$ 与 $p>0$，并记

$$
x^+=\max(x,0).
$$

以下均按每单位标的计算，忽略利息、股息、借券费、税费和交易成本。

## 两种标准构造

| 构造 | 标的腿 | 期权腿 | 到期前的组合损益 |
| --- | ---: | ---: | --- |
| 保护性看跌 | $+S$ | $+P(K,T)$ | $\Pi_t=(S_t+P_t)-(S_0+p)$ |
| 保护性看涨 | $-S$ | $+C(K,T)$ | $\Pi_t=(-S_t+C_t)-(-S_0+c)$ |

Married Put／Married Call 通常强调标的腿与保护期权同时建立。若期权是在既有头寸之后加入，后续的方向风险相同，但总持仓的税务成本基础与真实损益起点可能不同。

## 保护性看跌 / Protective Put

### 到期损益与价值下限

$$
\Pi_T^{\mathrm{PP}}
=S_T-S_0-p+(K-S_T)^+
=\max(S_T,K)-S_0-p.
$$

$$
\Pi_T^{\mathrm{PP}}=
\begin{cases}
K-S_0-p, & S_T<K,\\
S_T-S_0-p, & S_T\ge K.
\end{cases}
$$

- 上涨侧最大盈利：无上限。
- 最小到期损益：$K-S_0-p$；在常见 $S_0+p\ge K$ 时，最大亏损为 $S_0+p-K$。
- 盈亏平衡点：在 $S_0+p\ge K$ 时为 $S_T=S_0+p$。
- 到期组合价值下限：$\max(S_T,K)\ge K$，即标的可以不低于 $K$ 的价格退出。

若 $K>S_0+p$，简化公式会显示一个正的到期损益下限；此时必须把已含内在价值的权利金、融资与股息放回同一估值时点，不应把简化结果解释为无风险套利。

### Greeks

$$
\Delta_{\mathrm{PP}}=1+\Delta_P,
\qquad
\Gamma_{\mathrm{PP}}=\Gamma_P,
$$

$$
\Theta_{\mathrm{PP}}=\Theta_P,
\qquad
\mathrm{Vega}_{\mathrm{PP}}=\mathrm{Vega}_P.
$$

由于 $-1<\Delta_P<0$，该组合通常为正 Delta、正 Gamma、负日历 Theta、正 Vega。标的价格越深入 Put 保护区，组合 Delta 越接近 $0$。

### 行权与到期管理

因为持有的是多头 Put，这条腿不会被“提前指派”；持有人有权决定是否提前行权。对美式 Put，应先比较剩余时间价值、利息与股息，因为提前行权会放弃未实现的时间价值。到期时 Put 若价内，自动行权可能将标的卖出；若账户希望继续持有标的，应在截止时间前主动处理。

### 盈亏曲线（到期与到期前）

![[../assets/保护性看跌 Protective Put 盈亏曲线.svg]]

> [!note] 读图口径
> 实线为到期损益，虚线为期权尚余 30 天时的理论损益。图中未计股息、融资、提前行权和交易成本。

## 保护性看涨 / Protective Call

### 到期损益与价值下限

$$
\Pi_T^{\mathrm{PC}}
=S_0-S_T-c+(S_T-K)^+
=S_0-c-\min(S_T,K).
$$

$$
\Pi_T^{\mathrm{PC}}=
\begin{cases}
S_0-S_T-c, & S_T\le K,\\
S_0-K-c, & S_T>K.
\end{cases}
$$

- 下跌侧最大盈利：$S_0-c$，在 $S_T=0$ 时达到。
- 最小到期损益：$S_0-K-c$；在常见 $K+c\ge S_0$ 时，最大亏损为 $K+c-S_0$。
- 盈亏平衡点：在 $S_0-c\le K$ 时为 $S_T=S_0-c$。
- 上涨侧损失封顶：标的上涨至 $K$ 之后，Call 的收益抵消空头标的的新增亏损。

### Greeks

$$
\Delta_{\mathrm{PC}}=-1+\Delta_C,
\qquad
\Gamma_{\mathrm{PC}}=\Gamma_C,
$$

$$
\Theta_{\mathrm{PC}}=\Theta_C,
\qquad
\mathrm{Vega}_{\mathrm{PC}}=\mathrm{Vega}_C.
$$

由于 $0<\Delta_C<1$，该组合通常为负 Delta、正 Gamma、负日历 Theta、正 Vega。标的价格越深入 Call 保护区，组合 Delta 越接近 $0$。

### 借券、行权与结算

长 Call 封住了标的上涨造成的价格损失，但不能消除空头股票的借券费、难借费率跳升、召回、强制回补（buy-in）和代付股息。极端情况下，借券头寸可能在期权到期前被强制结束。

多头 Call 不会被提前指派。若需回补空头，可卖出 Call 再直接买入标的，或在符合条件时行权取得标的；直接提前行权通常会放弃剩余时间价值。到期自动行权、股票回补与期权结算时间不匹配时，还可能留下隔夜方向头寸。

### 盈亏曲线（到期与到期前）

![[../assets/保护性看涨 Protective Call 盈亏曲线.svg]]

> [!note] 读图口径
> 实线为到期损益，虚线为期权尚余 30 天时的理论损益。图中未计借券费、召回、代付股息、提前行权和结算错配。

## 实务检查

1. 核对标的数量、期权数量与合约乘数，将未被保护的部分单独识别。
2. 区分“最大价格损失”与操作风险：借券、跳空、流动性、行权截止时间和结算错配可使实际结果偏离到期损益图。
3. 保护到期后若仍需保险，必须把展期支出纳入长期成本。

## 关联概念

- [[备兑策略 Covered Strategy]]：用短期权收取权利金，但放弃标的在一侧的收益。
- [[Knowledge/Concepts/经济/金融/衍生品/期权/希腊字母/一阶/Delta|Delta]]、[[Knowledge/Concepts/经济/金融/衍生品/期权/希腊字母/二阶/Gamma|Gamma]]、[[Knowledge/Concepts/经济/金融/衍生品/期权/希腊字母/一阶/Theta|Theta]]、[[Knowledge/Concepts/经济/金融/衍生品/期权/希腊字母/一阶/Vega|Vega]]：描述组合的局部风险。
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/知识图谱/保护性备兑与领式|保护性、备兑与领式]]

## 来源

- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/使用期权进行对冲 Hedging with Options#保护性看涨期权与看跌期权 / Protective Calls and Puts|《Option Volatility and Pricing》：保护性看涨与看跌]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/风险考量 Risk Considerations|风险考量]]
