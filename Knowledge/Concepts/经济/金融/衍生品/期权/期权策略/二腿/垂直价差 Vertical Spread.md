---
type: option-strategy
schema_version: 1
name: 垂直价差
aliases:
  - Vertical Spread
  - Vertical Call
  - Vertical Put
  - Call Vertical Spread
  - Put Vertical Spread
  - 看涨垂直价差
  - 看跌垂直价差
  - 看涨期权垂直价差
  - 看跌期权垂直价差
leg_count: 2
option_leg_count: 2
underlying_leg_count: 0
strategy_family: 垂直价差
status: completed
completion_status: completed
created_from: merged-call-put-pages
created_at: 2026-08-15
updated_at: 2026-08-15
tags: [期权, 期权策略, 二腿策略, 垂直价差]
domain: 经济
subdomain: 金融
product_domain: 衍生品
instrument: 期权
---

# 垂直价差 / Vertical Spread

## 定义与命名

垂直价差由**同一标的、同一期权类型、同一到期日、不同执行价**的两条期权腿组成，数量通常为 $1:1$。它可以全部使用看涨期权，也可以全部使用看跌期权。

> [!important] Call／Put 不是方向
> “看涨期权垂直价差”与“看跌期权垂直价差”只说明采用 Call 还是 Put，不等于策略一定看多或看空。方向必须写成**牛市／熊市**，现金流则另写成**净支出（debit）／净收入（credit）**。

统一记号：$K_L<K_H$，翼宽 $w=K_H-K_L$，$x^+=\max(x,0)$。持仓数量 $q_i$ 以多头为正、空头为负；有符号初始净支出为

$$
D=\sum_i q_iV_i(t_0),
$$

其中 $D>0$ 表示支付净权利金，$D<0$ 表示收到净权利金。任一时点的每股损益为

$$
\Pi_t=\sum_i q_iV_i(t)-D.
$$

## 四种基本构造

| 方向 | 期权类型 | 组合 | 常见现金流 |
| --- | --- | --- | --- |
| 牛市 | Call | $+C(K_L)-C(K_H)$ | 净支出 |
| 熊市 | Call | $-C(K_L)+C(K_H)$ | 净收入 |
| 熊市 | Put | $+P(K_H)-P(K_L)$ | 净支出 |
| 牛市 | Put | $-P(K_H)+P(K_L)$ | 净收入 |

同一方向的 Call 与 Put 构造具有对应的到期风险形状，但建仓现金流、融资项、Rho、Theta 以及美式提前行权管理可能不同。

## 到期损益

### 牛市看涨价差

设净支出 $d>0$：

$$
\Pi_T=(S_T-K_L)^+-(S_T-K_H)^+-d
$$

$$
\Pi_T=
\begin{cases}
-d, & S_T\le K_L,\\
S_T-K_L-d, & K_L<S_T<K_H,\\
w-d, & S_T\ge K_H.
\end{cases}
$$

- 最大亏损：$d$。
- 最大盈利：$w-d$。
- 盈亏平衡点：$K_L+d$。

其反向头寸是熊市看涨价差。若收到净收入 $c>0$，最大盈利为 $c$，最大亏损为 $w-c$，盈亏平衡点为 $K_L+c$。

### 熊市看跌价差

设净支出 $d>0$：

$$
\Pi_T=(K_H-S_T)^+-(K_L-S_T)^+-d
$$

$$
\Pi_T=
\begin{cases}
w-d, & S_T\le K_L,\\
K_H-S_T-d, & K_L<S_T<K_H,\\
-d, & S_T\ge K_H.
\end{cases}
$$

- 最大盈利：$w-d$。
- 最大亏损：$d$。
- 盈亏平衡点：$K_H-d$。

其反向头寸是牛市看跌价差。若收到净收入 $c>0$，最大盈利为 $c$，最大亏损为 $w-c$，盈亏平衡点为 $K_H-c$。

上述固定边界要求两腿保持完整并持有至共同到期；提前指派、分腿处置和交易成本会改变实际路径损益。

## Greeks 与波动率

组合任一 Greek 都是逐腿相加：

$$
G_{\text{spread}}=\sum_i q_iG_i.
$$

牛市结构的 Delta 通常为正，熊市结构通常为负。Gamma、Theta 与 Vega 的净符号会随标的相对两个执行价的位置、期限及波动率曲面变化，不能仅凭“借记”或“贷记”永久定号。两腿会抵消部分时间与波动率风险，但接近某个执行价或临近到期时，局部 Gamma、Theta 与偏斜风险仍可能很大。

## 执行与风险

- 使用组合限价单，并按整组价格核对净支出或净收入。
- 美式短腿可能提前被指派；看涨短腿在派息前、看跌短腿在深度实值且时间价值很少时尤其需要检查。
- 到期价格贴近任一执行价时存在夹点风险（pin risk），可能留下意外股票头寸。
- “盈亏均有限”只描述完整两腿的到期经济结果，不消除分腿成交、融资、保证金、结算与流动性风险。

## 盈亏曲线（到期与到期前）

### Call 构造：牛市看涨价差

![[../assets/看涨垂直价差 Vertical Call 盈亏曲线.svg]]

### Call 构造：熊市看涨价差

![[../assets/熊市看涨垂直价差 Bear Call Spread 盈亏曲线.svg]]

### Put 构造：熊市看跌价差

![[../assets/看跌垂直价差 Vertical Put 盈亏曲线.svg]]

### Put 构造：牛市看跌价差

![[../assets/牛市看跌垂直价差 Bull Put Spread 盈亏曲线.svg]]

> [!note] 读图口径
> 四图覆盖 Call 与 Put 的牛市、熊市构造；实线表示到期损益，虚线表示尚余 30 天时的理论损益。更换执行价、期限或波动率曲面后需重新估值。

## 来源

- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/牛市与熊市价差 Bull and Bear Spreads#垂直价差 / Vertical Spreads|《期权波动率与定价》：垂直价差]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/价差策略导论 Introduction to Spreading|《期权波动率与定价》：价差策略导论]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/风险考量 Risk Considerations|《期权波动率与定价》：风险考量]]
