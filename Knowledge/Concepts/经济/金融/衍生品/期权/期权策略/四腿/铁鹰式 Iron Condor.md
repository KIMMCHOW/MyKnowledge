---
type: option-strategy
schema_version: 1
name: 铁鹰式
aliases:
  - Iron Condor
  - Credit Iron Condor
  - Short Iron Condor
  - 铁鹰式价差
leg_count: 4
option_leg_count: 4
underlying_leg_count: 0
strategy_family: 铁鹰式价差
status: completed
created_at: 2026-08-15
updated_at: 2026-08-15
tags:
  - 期权
  - 期权策略
  - 铁鹰式
  - 多腿策略
domain: 经济
subdomain: 金融
---

# 铁鹰式 / Iron Condor

## 定义

铁鹰式由一个看跌价差和一个看涨价差组成，四腿具有同一标的和到期日。市场中不加限定的 “Iron Condor” 通常指收取净权利金、希望标的到期落在两个短行权价之间的信用铁鹰；反向铁鹰则支付净权利金并希望标的大幅突破任一侧。

> [!warning] 命名必须绑定腿结构
> 有些资料把信用铁鹰称为 Short Condor 或 Short Iron Condor。审核时应以四条腿的多空方向为准，不能仅凭 “long/short” 单词判断收益方向。

## 统一符号

- $S_T$：到期时标的价格。
- $K_1<K_2<K_3<K_4$。
- 看跌侧翼宽 $w_P=K_2-K_1$；看涨侧翼宽 $w_C=K_4-K_3$。
- $x^+=\max(x,0)$。
- $R>0$：信用铁鹰的每股净收入（net credit）。
- $D>0$：反向铁鹰的每股净支出（net debit）。
- 下列结果均为每股、到期时的损益，未计手续费、滑点、税费、借券和融资成本。

## 常见结构：信用铁鹰

| 数量 | 操作 | 合约 |
| ---: | --- | --- |
| 1 | 买入 | $K_1$ 看跌期权 |
| 1 | 卖出 | $K_2$ 看跌期权 |
| 1 | 卖出 | $K_3$ 看涨期权 |
| 1 | 买入 | $K_4$ 看涨期权 |

到期损益为：

$$
\Pi_T=(K_1-S_T)^+-(K_2-S_T)^+-(S_T-K_3)^++(S_T-K_4)^++R.
$$

分段写为：

$$
\Pi_T=
\begin{cases}
R-w_P, & S_T\le K_1,\\
S_T-K_2+R, & K_1<S_T<K_2,\\
R, & K_2\le S_T\le K_3,\\
K_3-S_T+R, & K_3<S_T<K_4,\\
R-w_C, & S_T\ge K_4.
\end{cases}
$$

在 $0<R<\min(w_P,w_C)$ 时：

- 最大盈利：$R$，发生在 $K_2\le S_T\le K_3$。
- 下跌侧最大亏损：$w_P-R$。
- 上涨侧最大亏损：$w_C-R$。
- 整体最大亏损：$\max(w_P,w_C)-R$。
- 下方盈亏平衡点：$K_2-R$。
- 上方盈亏平衡点：$K_3+R$。

不等翼时必须分别报告两侧最大亏损；只写“翼宽减净收入”而不说明是哪一侧，会掩盖较宽一侧的真实风险。

## 反向铁鹰

反向铁鹰将四腿全部反向：卖出 $K_1$ 看跌、买入 $K_2$ 看跌、买入 $K_3$ 看涨、卖出 $K_4$ 看涨，并支付净权利金 $D$。

$$
\Pi_T=-(K_1-S_T)^++(K_2-S_T)^++(S_T-K_3)^+-(S_T-K_4)^+-D.
$$

分段写为：

$$
\Pi_T=
\begin{cases}
w_P-D, & S_T\le K_1,\\
K_2-S_T-D, & K_1<S_T<K_2,\\
-D, & K_2\le S_T\le K_3,\\
S_T-K_3-D, & K_3<S_T<K_4,\\
w_C-D, & S_T\ge K_4.
\end{cases}
$$

在 $0<D<\min(w_P,w_C)$ 时：

- 最大亏损：$D$，发生在 $K_2\le S_T\le K_3$。
- 下跌侧最大盈利：$w_P-D$。
- 上涨侧最大盈利：$w_C-D$。
- 整体最大盈利：$\max(w_P,w_C)-D$。
- 盈亏平衡点：$K_2-D$ 与 $K_3+D$。

反向铁鹰的两侧盈利均有限；股票价格在上涨方向无界，并不会使组合利润无界，因为最外侧短看涨期权封住了上方收益。

## Greeks 与波动率

- 信用铁鹰在标的位于两个短行权价之间时通常表现为负 [[Gamma]]、正 [[Theta]]、负 [[Vega]]，并在区间中部附近接近 Delta 中性。
- 标的靠近或越过任一短腿时，Delta 与 Gamma 会快速变化；波动率偏斜、期限和两侧翼宽也会使净 Greeks 不对称。
- 反向铁鹰在区间中部的局部 Greeks 通常相反：正 Gamma、负 Theta、正 Vega。
- “信用铁鹰就是低波动率交易”只是局部描述。到期前的损益还取决于标的位置、曲面各点变化、时间和成交价格。

## 执行、指派与到期风险

- $K_2$ 短看跌和 $K_3$ 短看涨均可能被提前指派；深度实值看跌、派息前看涨和剩余时间价值很低时应重点检查。
- 四腿完整时，到期经济损失受长翼限制；但提前指派可能产生股票、融资、借券或代付股息义务，长翼不会在同一时刻自动替投资者完成平仓。
- 到期价格靠近 $K_2$ 或 $K_3$ 时存在夹点风险。未能确认短腿是否被行权，可能在下一个交易日留下意外的多头或空头股票。
- 最大盈亏公式不包含分腿成交、买卖价差、佣金和压力行情下无法按理论价同时平仓的风险。
- 指数期权可能采用欧式行权与现金结算，股票期权常为美式行权与实物交割；策略卡必须与具体合约规则匹配。

## 盈亏曲线（到期与到期前）

![[../assets/铁鹰式 Iron Condor 盈亏曲线.svg]]

> [!note] 读图口径
> 图中展示信用铁鹰：买入远端保护翼、卖出较近 Put 与 Call。实线为到期损益，虚线为四条腿尚余 30 天时的理论损益；中间区域是到期最大盈利平台。反向铁鹰或不等翼结构需要重新估值。

## 来源

- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/知识图谱/蝶式与鹰式|蝶式与鹰式]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/波动率价差策略 Volatility Spreads|波动率价差策略]]
- [Options Industry Council：Short Condor (Iron Condor)](https://www.optionseducation.org/strategies/all-strategies/short-condor)
