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
updated_at: 2026-08-23
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

## 隐含波动率与执行价选择

在同一到期日、其他条件相同而执行价不同的一组期权中，平值附近的期权通常具有最大的绝对点数 [[Knowledge/Concepts/经济/金融/衍生品/期权/希腊字母/一阶/Vega|Vega]]。因此，当我们认为整个期限切片的市场 [[Knowledge/Concepts/经济/金融/衍生品/期权/隐含波动率|隐含波动率]] 偏离合理水平时，垂直价差应重点考虑**哪一条腿位于平值附近**：

> [!important] 平值腿选取规则
> - 如果市场隐含波动率**低于自己的合理波动率估计**，平值附近的期权相对低估幅度通常最大，优先让组合**买入平值腿**。
> - 如果市场隐含波动率**高于自己的合理波动率估计**，平值附近的期权相对高估幅度通常最大，优先让组合**卖出平值腿**。

这里的“低”与“高”是相对于交易者对合理波动率的估计，而不是脱离标的、期限和市场环境的固定数值。设标的约为 100、平值执行价为 100，以下构造展示了如何先确定平值腿，再用另一执行价保持所需方向；“$+$”表示买入，“$-$”表示卖出：

| 波动率判断 | 牛市 Call | 熊市 Call | 熊市 Put | 牛市 Put |
| --- | --- | --- | --- | --- |
| 市场 IV 偏低：买入平值腿 | $+C_{100}-C_{105}$ | $+C_{100}-C_{95}$ | $+P_{100}-P_{95}$ | $+P_{100}-P_{105}$ |
| 市场 IV 偏高：卖出平值腿 | $+C_{95}-C_{100}$ | $-C_{100}+C_{105}$ | $+P_{105}-P_{100}$ | $-P_{100}+P_{95}$ |

例如，同为牛市看涨价差：

- 市场 IV 偏低时，可选择 $+C_{100}-C_{105}$，买入平值的 100 Call；
- 市场 IV 偏高时，可选择 $+C_{95}-C_{100}$，卖出平值的 100 Call。

两者都表达看涨方向，但建仓成本、净 Gamma、Theta、Vega，以及标的不动时的表现并不相同。靠近平值且需要标的发生有利移动的一侧通常更偏正 Gamma、负 Theta；包含较深价内腿、标的不动也可能保留价值的一侧则可能更偏负 Gamma、正 Theta。最终符号仍须按实际参数逐腿计算。

> [!note] ATM、ATF 与波动率曲面
> - 严格来说，Vega 峰值通常更接近平远期（ATF）而非平即期（ATM）。期限较短、持有成本较小时两者接近；期限较长、利率或股息影响较大时，应优先参考远期价格。
> - 不同行权价的 IV 往往不同。实际选腿必须结合 [[Knowledge/Concepts/经济/金融/衍生品/期权/波动率偏斜 Skew|波动率偏斜]]，分别比较两条腿的市场 IV 与合理 IV，不能只用一个“整体 IV 高低”覆盖整条曲面。
> - 这条规则用于改善执行价的相对价值选择，不能替代方向判断、期限选择、流动性、交易成本和完整情景估值。

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
