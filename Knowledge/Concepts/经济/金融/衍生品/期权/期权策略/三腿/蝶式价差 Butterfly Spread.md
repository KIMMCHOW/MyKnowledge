---
type: option-strategy
schema_version: 1
name: 蝶式价差
aliases:
  - Butterfly Spread
  - Call Butterfly
  - Put Butterfly
  - Butterfly Call
  - Butterfly Put
  - 看涨蝶式
  - 看跌蝶式
  - 看涨期权蝶式价差
  - 看跌期权蝶式价差
leg_count: 3
option_leg_count: 3
underlying_leg_count: 0
strategy_family: 蝶式价差
status: completed
completion_status: completed
created_from: merged-call-put-pages
created_at: 2026-08-15
updated_at: 2026-08-15
tags: [期权, 期权策略, 三腿策略, 蝶式价差]
domain: 经济
subdomain: 金融
product_domain: 衍生品
instrument: 期权
---

# 蝶式价差 / Butterfly Spread

## 定义与腿数

蝶式价差由**同一标的、同一期权类型、同一到期日、三个不同执行价**的期权组成。标准结构的数量比固定为 $1:2:1$。

> [!note] 三腿不等于三张
> 本策略有 3 个不同合约系列，因此归入三腿；中间腿数量为 2，整组实际共有 4 张期权。Call／Put 只说明使用哪类期权，方向还必须写明多头或空头。

记 $K_1<K_2<K_3$。标准等距蝶式满足

$$
K_2-K_1=K_3-K_2=w.
$$

若不等距，则为断翼蝶式（broken-wing butterfly），不能直接套用下文的对称分段和最大盈亏公式。

## 多头与空头结构

| 方向 | $K_1$ 外翼 | $K_2$ 蝶身 | $K_3$ 外翼 |
| --- | ---: | ---: | ---: |
| 多头蝶式 | 买入 1 | 卖出 2 | 买入 1 |
| 空头蝶式 | 卖出 1 | 买入 2 | 卖出 1 |

三腿必须全部为 Call 或全部为 Put。多头蝶式通常支付净支出 $d>0$；空头蝶式通常收到净收入 $c>0$。

## 到期损益

令

$$
C_i=(S_T-K_i)^+,
\qquad
P_i=(K_i-S_T)^+.
$$

多头 Call 蝶式与多头 Put 蝶式分别为

$$
\Pi_T^{C}=C_1-2C_2+C_3-d,
$$

$$
\Pi_T^{P}=P_1-2P_2+P_3-d.
$$

在执行价等距时，两者的到期损益形状相同：

$$
\Pi_T=
\begin{cases}
-d, & S_T\le K_1,\\
S_T-K_1-d, & K_1<S_T\le K_2,\\
K_3-S_T-d, & K_2<S_T\le K_3,\\
-d, & S_T>K_3.
\end{cases}
$$

当 $0<d<w$：

- 最大盈利：$w-d$，发生在 $S_T=K_2$。
- 最大亏损：$d$，发生在 $S_T\le K_1$ 或 $S_T\ge K_3$。
- 盈亏平衡点：$K_1+d$ 与 $K_3-d$。

空头蝶式是完整头寸的反向。在 $0<c<w$ 时，最大盈利为 $c$（两侧尾部），最大亏损为 $w-c$（$S_T=K_2$），盈亏平衡点为 $K_1+c$ 与 $K_3-c$。

> [!important] Call 与 Put 的等价范围
> 只有在执行价等距、到期日相同并按相同经济口径比较时，Call 与 Put 蝶式才具有相同到期形状。断翼结构中 $K_1-2K_2+K_3\ne0$，两类构造不能继续无条件视为相同；美式提前行权和到期前市值风险也始终可能不同。

## Greeks 与波动率

当 $K_2$ 附近平值、临近到期时，多头蝶式通常接近 Delta 中性，并局部呈现

$$
-\Gamma,\qquad +\Theta,\qquad -\mathrm{Vega}.
$$

它偏好标的到期靠近蝶身并常受益于隐含波动率下降；空头蝶式在同一位置大致相反。靠近两翼或远离目标区域时，局部 Greek 符号可能改变。蝶式交易的是跨三个执行价的波动率曲率，不能用单一 Vega 完整描述。

## 执行、指派与到期风险

- 两张蝶身短腿可能分别被提前指派；Call 在派息前、Put 在深度实值且时间价值很少时尤其需要检查。
- 到期价格靠近 $K_2$ 时，理论收益最高但短腿是否被行权也最不确定，可能留下意外股票头寸。
- 有限到期损失要求所有腿保持完整并正确结算；分腿成交、融资、行权成本和交割物调整不在静态公式内。
- 只写 “Butterfly” 不足以提交订单，必须列明 Call／Put、多头／空头、三个执行价、数量比和到期日。

## 盈亏曲线（到期与到期前）

### Call 多头蝶式

![[../assets/看涨蝶式 Butterfly Call 盈亏曲线.svg]]

### Call 空头蝶式

![[../assets/空头看涨蝶式 Short Call Butterfly 盈亏曲线.svg]]

### Put 多头蝶式

![[../assets/看跌蝶式 Butterfly Put 盈亏曲线.svg]]

### Put 空头蝶式

![[../assets/空头看跌蝶式 Short Put Butterfly 盈亏曲线.svg]]

> [!note] 读图口径
> 四图覆盖 Call／Put 与多头／空头等距蝶式。实线为到期损益，虚线为三条合约腿尚余 30 天时的理论损益。Call 与 Put 构造在到期前可能存在定价差异；断翼结构需单独重估。

## 来源

- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/波动率价差策略 Volatility Spreads#蝶式价差 / Butterfly|《期权波动率与定价》：蝶式价差]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/知识图谱/蝶式与鹰式|知识图谱：蝶式与鹰式]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/风险考量 Risk Considerations|《期权波动率与定价》：风险考量]]
