---
type: option-strategy
schema_version: 1
name: 比率价差
aliases:
  - Ratio Spread
  - Call Ratio Spread
  - Put Ratio Spread
  - Ratio Call
  - Ratio Put
  - Backspread
  - Frontspread
  - 反向比率价差
  - 正向比率价差
  - 看涨比率价差
  - 看跌比率价差
  - 看涨期权比率价差
  - 看跌期权比率价差
leg_count: 2
option_leg_count: 2
underlying_leg_count: 0
strategy_family: 比率价差
status: completed
completion_status: completed
created_from: merged-call-put-pages
created_at: 2026-08-15
updated_at: 2026-08-15
tags: [期权, 期权策略, 二腿策略, 比率价差, 裸空风险]
domain: 经济
subdomain: 金融
product_domain: 衍生品
instrument: 期权
---

# 比率价差 / Ratio Spread

## 定义与数量口径

比率价差使用**同一标的、同一期权类型、同一到期日、不同执行价且数量不等**的期权。Call 与 Put 都可构造。

“二腿”是指两个不同合约系列，并非只有两张合约；$1:2$ 结构实际有 3 张期权。记录比例时必须同时写出买卖方向，例如

$$
+1C(K_L)-2C(K_H),
$$

而不能只写缺少方向的“$1:2$”。以下记 $K_L<K_H$，$x^+=\max(x,0)$，有符号初始净支出为 $D$；$D>0$ 为净支出，$D<0$ 为净收入。每股损益统一写为“到期内在价值组合 $-D$”。

## 两类方向：买多卖少与卖多买少

- **反向比率价差**（backspread，买多卖少）：买入的期权数量多于卖出数量。建仓接近 Delta 中性时，局部通常为 $+\Gamma$、$-\Theta$、$+\mathrm{Vega}$，偏好标的大幅运动或隐含波动率上升。
- **正向比率价差**（frontspread，卖多买少）：卖出的期权数量多于买入数量。局部通常为 $-\Gamma$、$+\Theta$、$-\mathrm{Vega}$，但净卖出的尾部可能包含裸空风险。

backspread／frontspread 是历史术语。实务中最清楚的写法仍是“买多卖少／卖多买少 + Call／Put + 明确数量与执行价”。初始 Delta 中性也只在建仓瞬间近似成立。

## Call 比率价差

### 卖多买少：看涨正向比率价差

代表结构为买入 1 份低执行价 Call、卖出 2 份高执行价 Call：

$$
\Pi_T=(S_T-K_L)^+-2(S_T-K_H)^+-D.
$$

$$
\Pi_T=
\begin{cases}
-D, & S_T\le K_L,\\
S_T-K_L-D, & K_L<S_T\le K_H,\\
-S_T-K_L+2K_H-D, & S_T>K_H.
\end{cases}
$$

- 峰值在 $S_T=K_H$，为 $(K_H-K_L)-D$。
- 上涨尾部亏损无上限，因为净额剩余 1 份裸空 Call。
- 常见 $0\le D\le K_H-K_L$ 时，候选盈亏平衡点为 $K_L+D$ 与 $2K_H-K_L-D$；必须验证根属于相应分段。

### 买多卖少：看涨反向比率价差

将以上头寸整体反向，即

$$
-C(K_L)+2C(K_H).
$$

大幅上涨时盈利不封顶，中间区域可能亏损；标的大幅下跌使所有 Call 归零时，损益只剩初始现金流。

## Put 比率价差

### 卖多买少：看跌正向比率价差

代表结构为买入 1 份高执行价 Put、卖出 2 份低执行价 Put：

$$
\Pi_T=(K_H-S_T)^+-2(K_L-S_T)^+-D.
$$

$$
\Pi_T=
\begin{cases}
S_T+K_H-2K_L-D, & 0\le S_T<K_L,\\
K_H-S_T-D, & K_L\le S_T<K_H,\\
-D, & S_T\ge K_H.
\end{cases}
$$

- 峰值在 $S_T=K_L$，为 $(K_H-K_L)-D$。
- 下跌尾部含 1 份净裸空 Put。股票价格有 $S_T\ge0$ 的下界，因此损失数学上有限，但可能非常巨大。
- 常见情形的候选盈亏平衡点为 $K_H-D$ 与 $2K_L-K_H+D$；每个根都必须验证是否落在相应区间且不低于 0。

### 买多卖少：看跌反向比率价差

将以上头寸整体反向，即

$$
-P(K_H)+2P(K_L).
$$

它偏好大幅下跌；但对股票类标的而言，下跌端利润因 $S_T$ 最低为 0 而有上限，不能笼统写成“无限盈利”。

## Credit 不是定义条件

> [!important] 比率价差不一定以净收入建立
> 是否形成 credit 取决于执行价、数量比、期限、波动率偏斜和实际成交价格。对于 backspread，在“所有期权到期均无价值”的一侧，只有 $D<0$（建仓收到净权利金）时该侧才会盈利；但即使 $D>0$，标的向净多期权所在的有利尾部充分移动时，仍然可以盈利。

在传统模型和近似 Delta 中性的特定构造下，backspread 常可形成净收入，这只是带前提的定价结论，不是比率价差的定义。

## Greeks、执行与风险

- 组合 Greek 为各腿按数量加总；价格穿越执行价后，净符号与 Delta 都可能快速反转。
- Call frontspread 的上涨侧有裸空 Call 无上限风险；Put frontspread 的下跌侧有重大裸空 Put、保证金与追加保证金风险。
- 波动率偏斜会直接改变两执行价的相对价格与 Vega，不能只做平行波动率情景。
- 使用比例组合限价单并反复核对数量。把 $+1:-2$ 下成 $+2:-1$ 会彻底反转尾部风险。
- 美式短腿可能分批、分时被指派；先平掉保护腿或出现部分成交会放大裸露头寸。

## 盈亏曲线（到期与到期前）

### Call：卖多买少代表构造

![[../assets/看涨比率价差 Ratio Call 盈亏曲线.svg]]

### Call：买多卖少反向比率价差

![[../assets/看涨反向比率价差 Call Ratio Backspread 盈亏曲线.svg]]

### Put：卖多买少代表构造

![[../assets/看跌比率价差 Ratio Put 盈亏曲线.svg]]

### Put：买多卖少反向比率价差

![[../assets/看跌反向比率价差 Put Ratio Backspread 盈亏曲线.svg]]

> [!note] 读图口径
> 四图分别覆盖 Call／Put 的 frontspread（卖多买少）与 backspread（买多卖少）。实线为到期损益，虚线为尚余 30 天时的理论损益；实际现金流仍应按成交价重新计算。

## 来源

- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/波动率价差策略 Volatility Spreads#比率价差 / Ratio Spread|《期权波动率与定价》：比率价差]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/牛市与熊市价差 Bull and Bear Spreads#牛市与熊市比率价差 / Bull and Bear ratio Spreads|《期权波动率与定价》：牛熊比率价差]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/风险考量 Risk Considerations|《期权波动率与定价》：风险考量]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/知识图谱/比率价差与圣诞树|知识图谱：比率价差与圣诞树]]
