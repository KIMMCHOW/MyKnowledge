---
type: option-strategy
schema_version: 1
name: 日历价差
aliases:
  - Calendar Spread
  - Time Spread
  - Horizontal Spread
  - Calendar Call
  - Calendar Put
  - Call Calendar Spread
  - Put Calendar Spread
  - 时间价差
  - 水平价差
  - 看涨日历价差
  - 看跌日历价差
  - 看涨期权日历价差
  - 看跌期权日历价差
leg_count: 2
option_leg_count: 2
underlying_leg_count: 0
strategy_family: 日历价差
status: completed
completion_status: completed
created_from: merged-call-put-pages
created_at: 2026-08-15
updated_at: 2026-08-15
tags: [期权, 期权策略, 二腿策略, 日历价差, 时间价差, 水平价差]
domain: 经济
subdomain: 金融
product_domain: 衍生品
instrument: 期权
---

# 日历价差 / Calendar Spread

## 定义与同义词

**日历价差**（calendar spread），也称**时间价差**（time spread）或**水平价差**（horizontal spread），由**同一标的、同一期权类型、同一执行价、不同到期月份**的两条反向期权腿组成。它可以全部使用 Call，也可以全部使用 Put。

> [!note] “水平价差”的由来
> 早期期权交易所的报价板把到期月份横向排列，因此跨不同到期月份的组合被称为 horizontal spread。现代中文以“日历价差”最常用，三者指向同一策略家族。

记近月到期日为 $T_N$、远月到期日为 $T_F$，且 $T_N<T_F$，共同执行价为 $K$。多头数量记正、空头数量记负；有符号初始净支出为

$$
D=\sum_iq_iV_i(t_0),
$$

$D>0$ 为净支出，$D<0$ 为净收入。

## 多头与空头

| 方向 | 近月腿 | 远月腿 | 常见现金流 |
| --- | --- | --- | --- |
| 多头日历 | 卖出 $V_j(K,T_N)$ | 买入 $V_j(K,T_F)$ | 通常净支出 |
| 空头日历 | 买入 $V_j(K,T_N)$ | 卖出 $V_j(K,T_F)$ | 通常净收入 |

其中 $j\in\{C,P\}$。Call／Put 只说明期权类型，不是多空方向。期限结构倒挂、利率、股息或特殊供需可能改变现金流，因此应以腿方向为命名依据，而不是只看 debit／credit。

## 评估公式：不是共同到期折线

在近月到期日 $T_N$，远月腿仍有剩余期限。多头日历的每股损益为

$$
\Pi_{T_N}(S)=V_j\!\left(S,K,T_F-T_N;\,\Sigma_{T_N}^{(T_F)},r,q\right)-h_j(S,K)-D,
$$

其中

$$
h_C(S,K)=(S-K)^+,
\qquad
h_P(S,K)=(K-S)^+,
$$

$\Sigma_{T_N}^{(T_F)}$ 表示 $T_N$ 时远月期权所在的隐含波动率曲面。远月腿的价值还受剩余期限、利率、股息与市场流动性影响。

因此，日历价差没有由执行价与初始权利金唯一决定的“共同到期损益线”。平台展示的最大盈利、最大亏损与盈亏平衡点，都是在指定评估日及一组波动率、利率和股息假设下计算的情景值。

## Call 与 Put 构造

### 看涨期权日历价差

$$
-C(K,T_N)+C(K,T_F)
$$

标准多头结构卖出近月 Call、买入远月 Call。无股息股票的常规模型下，多头 Call 日历通常具有正 Rho 倾向；股息上升通常不利于其价值。

### 看跌期权日历价差

$$
-P(K,T_N)+P(K,T_F)
$$

标准多头结构卖出近月 Put、买入远月 Put。常规模型下，多头 Put 日历通常具有负 Rho 倾向；股息上升通常有利于其价值。上述方向依赖标的、合约条款和评估假设，不能替代逐腿计算。

> [!important] Call 与 Put 的 Rho 方向不能混用
> 对“空近月、多远月”的标准多头日历价差，并在两腿 Delta 约略相当的局部条件下：Call 构造通常 $\rho>0$，Put 构造通常 $\rho<0$；空头日历的方向全部反转。股息敏感度通常与上述利率敏感度方向相反。

## 时间、波动率与 Greeks

在两腿接近平值、数量 $1:1$ 且初始 Delta 近似中性时，多头日历通常表现为：

$$
-\Gamma,\qquad +\Theta,\qquad +\mathrm{Vega}.
$$

- 近月平值期权通常比远月平值期权衰减得更快，因此时间流逝可能使多头日历扩大。
- 远月 Vega 通常更大，隐含波动率上升可能使远月多头升值更多。
- 标的大幅远离 $K$ 时，两腿时间价值都可能减少，价差可能收缩甚至“塌缩”。
- 这些只是局部性质。标的位置、两个期限的波动率独立变化、偏斜、利率与股息都可能改变净 Greeks。

空头日历在相同局部条件下的风险方向大致相反：$+\Gamma$、$-\Theta$、$-\mathrm{Vega}$。

## 最大盈亏与盈亏平衡

- 在给定 $T_N$ 的远月估值参数后，盈亏平衡点必须数值求解 $\Pi_{T_N}(S)=0$，可能有两个、一个或没有交点。
- 标准多头日历在 $T_N$ 的情景峰值通常靠近 $K$，但金额不是合约预先锁定的。
- 若两腿在 $T_N$ 同步处理且不发生路径事件，初始净支出通常是自然的损失参考；提前指派、错腿、近月到期后继续持仓、交易费用及特殊持有成本都可能突破简单情景图的边界。

## 执行与特殊风险

- 美式近月空腿可能提前被指派；到期价格靠近 $K$ 时存在夹点风险。
- 近月腿结束后若不处理，原组合会变成单独的远月期权，或股票加远月期权的不同策略。
- 两个到期月份的隐含波动率可独立变化；不能把期限结构风险简化为单一平行 Vega。
- 股票期权各月份通常对应同一股票；期货期权的不同月份却可能对应不同期货合约，因而额外包含跨期基差风险。需要时应使用相反方向的期货跨期价差按 Delta 对冲。
- 使用组合限价单，并分别核对两个到期月份的流动性、合约乘数与交割物。

## 盈亏曲线（近月到期日与更早评估日）

### Call 多头日历价差

![[../assets/看涨日历价差 Calendar Call 盈亏曲线.svg]]

### Call 空头日历价差

![[../assets/空头看涨日历价差 Short Call Calendar Spread 盈亏曲线.svg]]

### Put 多头日历价差

![[../assets/看跌日历价差 Calendar Put 盈亏曲线.svg]]

### Put 空头日历价差

![[../assets/空头看跌日历价差 Short Put Calendar Spread 盈亏曲线.svg]]

> [!important] 读图口径
> 四图覆盖 Call／Put 与多头／空头方向。实线表示**近月腿到期日**的组合理论损益，此时远月腿仍剩余期限；虚线表示更早评估日的理论损益。所有曲线都依赖当时的波动率期限结构，不是最终到期收益承诺。

## 来源

- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/波动率价差策略 Volatility Spreads#日历价差 / Calendar Spread|《期权波动率与定价》：日历价差]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/风险考量 Risk Considerations|《期权波动率与定价》：风险考量]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/知识图谱/日历与对角价差|知识图谱：日历与对角价差]]
