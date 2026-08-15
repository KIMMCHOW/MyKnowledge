---
type: option-strategy
schema_version: 1
name: 看涨垂直价差
aliases:
  - Vertical Call
  - Call Vertical Spread
  - 看涨期权垂直价差
leg_count: 2
option_leg_count: 2
underlying_leg_count: 0
strategy_family: 垂直价差
status: completed
created_at: 2026-08-15
updated_at: 2026-08-15
tags:
  - 期权
  - 期权策略
  - 二腿策略
  - 垂直价差
domain: 经济
subdomain: 金融
---

# 看涨垂直价差 / Vertical Call

## 定义

看涨垂直价差由**同一标的、同一到期日、不同执行价**的两份看涨期权组成。两腿数量相等，因此到期损益被限制在两个执行价之间；选择买低执行价还是买高执行价，决定策略是看多还是看空。

以下记号中，$K_1<K_2$，$c_1,c_2$ 是建仓时每股期权费，$S_T$ 是到期标的价格，且 $x^+=\max(x,0)$。所有损益均为**每股、未计佣金和滑点**的结果；一份标准股票期权合约通常还需乘以合约乘数。

## 标准腿结构

常见的看涨牛市价差（debit call spread）为：

| 腿 | 操作 | 执行价 | 到期日 |
| --- | --- | --- | --- |
| 1 | 买入 1 份看涨期权 | $K_1$ | $T$ |
| 2 | 卖出 1 份看涨期权 | $K_2$ | $T$ |

净借记为 $D=c_1-c_2>0$。

## 损益公式

看涨牛市价差的到期损益为：

$$
\Pi_T=(S_T-K_1)^+-(S_T-K_2)^+-D
$$

等价的分段形式为：

$$
\Pi_T=
\begin{cases}
-D, & S_T\le K_1,\\
S_T-K_1-D, & K_1<S_T<K_2,\\
K_2-K_1-D, & S_T\ge K_2.
\end{cases}
$$

## 方向与变体

- **看多／净借记**：买入 $K_1$、卖出 $K_2$，以有限风险换取标的温和上涨时的收益。
- **看空／净贷记**：卖出 $K_1$、买入 $K_2$，即上述头寸的反向，也称看涨熊市价差。收到净权利金 $C=c_1-c_2>0$。

实际报价可能使建仓价格偏离理论上的借记或贷记；分类应以两腿方向和实际净现金流为准。

## 最大盈亏与盈亏平衡

对于看多／净借记变体：

- 最大亏损：$D$，发生在 $S_T\le K_1$。
- 最大盈利：$(K_2-K_1)-D$，发生在 $S_T\ge K_2$。
- 到期盈亏平衡点：$K_1+D$。

对于看空／净贷记变体：

- 最大盈利：净贷记 $C$，发生在 $S_T\le K_1$。
- 最大亏损：$(K_2-K_1)-C$，发生在 $S_T\ge K_2$。
- 到期盈亏平衡点：$K_1+C$。

这些边界以持有至共同到期日、两腿数量相等且不发生提前行权为前提。

## Greeks、波动率与时间

看多变体的 Delta 通常为正；各 Greeks 都是低执行价多头看涨与高执行价空头看涨的差值。Gamma、Vega 和 Theta 的净符号会随 $S$、剩余期限和波动率曲面改变，不能仅凭“借记价差”永久判定。接近某一执行价和临近到期时，Gamma 与时间衰减会更集中；隐含波动率变化对两腿的影响会部分抵消，但并非完全为零。

## 执行与风险

- 优先使用组合限价单，避免分别成交造成方向敞口和额外滑点。
- 美式期权的空头 $K_2$ 腿可能提前被指派；深度实值、临近除息日且剩余时间价值很少时风险更高。
- 若空头腿被指派而多头腿仍在，应及时处理股票头寸；不要默认券商会按理想顺序自动平仓。
- 临近到期且标的靠近执行价时存在 pin risk，最终指派结果可能到收盘后才明确。
- 宽买卖价差、不同腿成交深度不足，以及佣金，都可能显著侵蚀有限的理论利润。

## 盈亏曲线（到期与到期前）

![[../assets/看涨垂直价差 Vertical Call 盈亏曲线.svg]]

> [!note] 读图口径
> 图中展示牛市借记看涨价差。实线为到期损益，虚线为尚余 30 天时的 Black–Scholes 理论损益。信用方向、其他行权价间距及波动率曲面需要单独重估。

## 来源

- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/牛市与熊市价差 Bull and Bear Spreads#垂直价差 / Vertical Spreads|《期权波动率与定价》：垂直价差]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/价差策略导论 Introduction to Spreading|《期权波动率与定价》：价差策略导论]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/风险考量 Risk Considerations|《期权波动率与定价》：风险考量]]
