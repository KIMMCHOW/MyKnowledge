---
type: option-strategy
schema_version: 1
name: 看涨鹰式
aliases:
  - Condor Call
  - Call Condor
  - 看涨期权鹰式价差
leg_count: 4
option_leg_count: 4
underlying_leg_count: 0
strategy_family: 鹰式价差
status: completed
created_at: 2026-08-15
updated_at: 2026-08-15
tags:
  - 期权
  - 期权策略
  - 鹰式价差
  - 多腿策略
domain: 经济
subdomain: 金融
---

# 看涨鹰式 / Condor Call

## 定义

看涨鹰式以同一标的、同一到期日、四个不同行权价的看涨期权构造。标准多头看涨鹰式可以视为一个较低行权价的牛市看涨价差，加上一个更高行权价的熊市看涨价差；它在两个中间行权价之间取得平坦的最高到期收益区间。

## 统一符号

- $S_T$：到期时标的价格。
- $K_1<K_2<K_3<K_4$。
- 标准等翼鹰式满足

  $$
  K_2-K_1=K_4-K_3=w,
  $$

  但中间区间 $K_3-K_2$ 不必等于 $w$。
- $x^+=\max(x,0)$。
- $D>0$：多头鹰式的每股净支出（net debit）。
- $R>0$：空头鹰式的每股净收入（net credit）。
- 下列结果均为每股、到期时的损益，未计交易与行权成本。

## 标准腿结构：多头看涨鹰式

| 数量 | 操作 | 合约 |
| ---: | --- | --- |
| 1 | 买入 | $K_1$ 看涨期权 |
| 1 | 卖出 | $K_2$ 看涨期权 |
| 1 | 卖出 | $K_3$ 看涨期权 |
| 1 | 买入 | $K_4$ 看涨期权 |

到期损益为：

$$
\Pi_T=(S_T-K_1)^+-(S_T-K_2)^+-(S_T-K_3)^++(S_T-K_4)^+-D.
$$

等翼时分段写为：

$$
\Pi_T=
\begin{cases}
-D, & S_T\le K_1,\\
S_T-K_1-D, & K_1<S_T\le K_2,\\
w-D, & K_2<S_T\le K_3,\\
K_4-S_T-D, & K_3<S_T\le K_4,\\
-D, & S_T>K_4.
\end{cases}
$$

在 $0<D<w$ 时：

- 最大盈利：$w-D$，发生在 $K_2\le S_T\le K_3$。
- 最大亏损：$D$，发生在 $S_T\le K_1$ 或 $S_T\ge K_4$。
- 下方盈亏平衡点：$K_1+D$。
- 上方盈亏平衡点：$K_4-D$。

## 空头看涨鹰式

空头看涨鹰式将四腿全部反向：卖出 $K_1$、买入 $K_2$、买入 $K_3$、卖出 $K_4$ 看涨期权，并收取净权利金 $R$。

$$
\Pi_T=-(S_T-K_1)^++(S_T-K_2)^++(S_T-K_3)^+-(S_T-K_4)^++R.
$$

在 $0<R<w$ 时：

- 最大盈利：$R$，发生在 $S_T\le K_1$ 或 $S_T\ge K_4$。
- 最大亏损：$w-R$，发生在 $K_2\le S_T\le K_3$。
- 盈亏平衡点：$K_1+R$ 与 $K_4-R$。

多头鹰式与空头鹰式的收益区域相反。只写 “Condor Call” 而不说明多空，无法判断其风险方向。

## 非等翼结构

若 $K_2-K_1\ne K_4-K_3$，左右尾部的到期价值不同，策略属于断翼鹰式。此时必须直接使用完整损益公式逐段计算，不能用单一翼宽 $w$ 推导最大盈亏和两个对称盈亏平衡点。

## Greeks 与波动率

- 多头看涨鹰式在标的位于中间盈利区间时通常接近 Delta 中性，并常表现为负 [[Gamma]]、正 [[Theta]]、负 [[Vega]]。
- 标的接近两翼时，各腿的局部敏感度会快速变化，Gamma、Theta 与 Vega 的净符号可能翻转。
- 空头看涨鹰式在相同位置的局部 Greeks 大致相反。
- 四个执行价使策略直接暴露于波动率偏斜与曲率；“隐含波动率下降必然盈利”并不是对所有标的位置和剩余期限都成立。

## 执行、指派与到期风险

- $K_2$ 与 $K_3$ 两张短看涨期权均可能被提前指派，派息前尤其需要检查剩余时间价值。
- 若到期价格位于某个短行权价附近，是否自动行权可能不确定；错误预判可能留下净多头或净空头股票。
- 即使到期经济风险有限，提前指派后用长腿覆盖也可能产生隔夜借券、融资或交割时间差。
- 四腿组合的理论中间价通常无法同时成交；分腿成交会暴露方向、波动率和数量错配风险。

## 盈亏曲线（到期与到期前）

![[../assets/看涨鹰式 Condor Call 盈亏曲线.svg]]

> [!note] 读图口径
> 图中展示等翼 $1:-1:-1:1$ 多头看涨鹰式。实线为到期损益，虚线为四条腿尚余 30 天时的理论损益；中间两执行价之间形成到期最大盈利平台。空头或不等翼结构需要重新估值。

## 来源

- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/知识图谱/蝶式与鹰式|蝶式与鹰式]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/波动率价差策略 Volatility Spreads|波动率价差策略]]
- [Options Industry Council：Long Call Condor](https://www.optionseducation.org/strategies/all-strategies/long-call-condor)
