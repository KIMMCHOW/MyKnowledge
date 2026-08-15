---
type: option-strategy
schema_version: 1
name: 鹰式价差
aliases:
  - Condor Spread
  - Call Condor
  - Put Condor
  - Condor Call
  - Condor Put
  - 看涨鹰式
  - 看跌鹰式
  - 看涨期权鹰式价差
  - 看跌期权鹰式价差
leg_count: 4
option_leg_count: 4
underlying_leg_count: 0
strategy_family: 鹰式价差
status: completed
completion_status: completed
created_from: merged-call-put-pages
created_at: 2026-08-15
updated_at: 2026-08-15
tags: [期权, 期权策略, 四腿策略, 鹰式价差]
domain: 经济
subdomain: 金融
product_domain: 衍生品
instrument: 期权
---

# 鹰式价差 / Condor Spread

## 定义

鹰式价差由**同一标的、同一期权类型、同一到期日、四个不同执行价**的期权组成，四腿数量比固定为 $1:1:1:1$。它可以全部使用 Call，也可以全部使用 Put。

记

$$
K_1<K_2<K_3<K_4.
$$

标准等翼鹰式要求

$$
K_2-K_1=K_4-K_3=w,
$$

两个中间执行价之间的主体宽度 $K_3-K_2$ 不必等于 $w$。

> [!important] 规范术语
> 使用“多头／空头鹰式价差”，不用“长／短鹰式”或“秃鹰”。Call／Put 只说明四腿采用的期权类型，不代表策略方向。铁鹰式混合使用 Put 与 Call，是独立策略，见 [[铁鹰式 Iron Condor]]。

## 多头与空头结构

| 方向 | $K_1$ 外翼 | $K_2$ 内腿 | $K_3$ 内腿 | $K_4$ 外翼 |
| --- | ---: | ---: | ---: | ---: |
| 多头鹰式 | 买入 1 | 卖出 1 | 卖出 1 | 买入 1 |
| 空头鹰式 | 卖出 1 | 买入 1 | 买入 1 | 卖出 1 |

多头鹰式通常支付净支出 $d>0$，空头鹰式通常收到净收入 $c>0$。

## 到期损益

令

$$
C_i=(S_T-K_i)^+,
\qquad
P_i=(K_i-S_T)^+.
$$

多头 Call 与 Put 鹰式分别为

$$
\Pi_T^C=C_1-C_2-C_3+C_4-d,
$$

$$
\Pi_T^P=P_1-P_2-P_3+P_4-d.
$$

在两侧翼宽相等时，两者具有相同的到期损益形状：

$$
\Pi_T=
\begin{cases}
-d, & S_T\le K_1,\\
S_T-K_1-d, & K_1<S_T\le K_2,\\
w-d, & K_2<S_T\le K_3,\\
K_4-S_T-d, & K_3<S_T\le K_4,\\
-d, & S_T>K_4.
\end{cases}
$$

当 $0<d<w$：

- 最大盈利：$w-d$，发生在 $K_2\le S_T\le K_3$。
- 最大亏损：$d$，发生在 $S_T\le K_1$ 或 $S_T\ge K_4$。
- 盈亏平衡点：$K_1+d$ 与 $K_4-d$。

空头鹰式是完整头寸的反向。在 $0<c<w$ 时，最大盈利为 $c$（两侧尾部），最大亏损为 $w-c$（中间平台），盈亏平衡点为 $K_1+c$ 与 $K_4-c$。

## 非等翼结构

若 $K_2-K_1\ne K_4-K_3$，则为断翼鹰式。左右尾部的到期常数不同，Call 与 Put 构造也不能再无条件视为同一风险形状。此时必须从完整 payoff 逐段计算并分别报告两侧风险，不能用单一 $w$ 套公式。

## Greeks 与波动率

标的位于两个中间执行价之间时，多头鹰式通常接近 Delta 中性，并局部呈现

$$
-\Gamma,\qquad +\Theta,\qquad -\mathrm{Vega}.
$$

空头鹰式在相同位置大致相反。靠近外翼或内腿时，局部 Gamma、Theta 与 Vega 都可能翻转。四个执行价使策略直接暴露于波动率偏斜和曲率，不能把“波动率下降有利”理解为全局保证。

## 执行、指派与到期风险

- 两条内侧短腿都可能提前被指派；Call 在派息前、Put 在深度实值且时间价值很少时需重点检查。
- 到期价格靠近 $K_2$ 或 $K_3$ 时存在夹点风险，可能留下意外股票头寸。
- 完整组合的到期经济损失有限，但提前指派、分腿成交、融资、借券和结算时间差仍可造成额外损失。
- 下单必须写明 Call／Put、多头／空头、四个执行价和到期日；只报 “Condor” 不足以唯一确定头寸。

## 盈亏曲线（到期与到期前）

### Call 多头鹰式

![[../assets/看涨鹰式 Condor Call 盈亏曲线.svg]]

### Call 空头鹰式

![[../assets/空头看涨鹰式 Short Call Condor 盈亏曲线.svg]]

### Put 多头鹰式

![[../assets/看跌鹰式 Condor Put 盈亏曲线.svg]]

### Put 空头鹰式

![[../assets/空头看跌鹰式 Short Put Condor 盈亏曲线.svg]]

> [!note] 读图口径
> 四图覆盖 Call／Put 与多头／空头等翼鹰式。实线为到期损益，虚线为四腿尚余 30 天时的理论损益。断翼结构及混合 Call／Put 的铁鹰式必须分别估值。

## 来源

- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/波动率价差策略 Volatility Spreads#鹰式价差 / Condor|《期权波动率与定价》：鹰式价差]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/知识图谱/蝶式与鹰式|知识图谱：蝶式与鹰式]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/风险考量 Risk Considerations|《期权波动率与定价》：风险考量]]
