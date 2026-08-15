---
type: option-strategy
schema_version: 1
name: 圣诞树价差
aliases:
  - Christmas Tree Spread
  - Christmas Tree
  - Ladder Spread
  - 阶梯价差
  - 看涨圣诞树
  - 看跌圣诞树
leg_count: 3
option_leg_count: 3
underlying_leg_count: 0
strategy_family: 圣诞树价差
status: completed
completion_status: completed
created_from: Option Volatility and Pricing 第11章
created_at: 2026-08-15
updated_at: 2026-08-15
tags: [期权, 期权策略, 三腿策略, 圣诞树价差, 阶梯价差, 裸空风险]
domain: 经济
subdomain: 金融
product_domain: 衍生品
instrument: 期权
---

# 圣诞树价差 / Christmas Tree Spread

## 定义与命名边界

圣诞树价差（Christmas tree），也称**阶梯价差**（ladder spread），由**同一标的、同一期权类型、同一到期日、三个不同执行价**的期权组成。每个系列各 1 张，数量比为 $1:1:1$；执行价不要求等距，通常选择为使建仓 Delta 接近中性。

> [!warning] 本页采用 Natenberg 第 11 章定义
> 市场资料对 Christmas Tree／Ladder 的数量比和 long／short 命名并不完全统一。本文严格采用本书口径：**多头圣诞树＝买入 1 份、卖出 2 份；空头圣诞树＝卖出 1 份、买入 2 份**。实际下单时必须列出每条腿，不能只报策略名。

记 $K_1<K_2<K_3$，

$$
w_L=K_2-K_1,
\qquad
w_R=K_3-K_2.
$$

用 $B$ 表示建仓净现金流：$B>0$ 为收到净权利金，$B<0$ 为支付净权利金。每股到期损益统一为

$$
\Pi_T=G(S_T)+B,
$$

其中 $G$ 是组合到期内在价值。

## 四种腿结构

$$
\begin{aligned}
\text{多头看涨圣诞树：}&\quad +C(K_1)-C(K_2)-C(K_3),\\
\text{空头看涨圣诞树：}&\quad -C(K_1)+C(K_2)+C(K_3),\\
\text{多头看跌圣诞树：}&\quad +P(K_3)-P(K_2)-P(K_1),\\
\text{空头看跌圣诞树：}&\quad -P(K_3)+P(K_2)+P(K_1).
\end{aligned}
$$

Call／Put 说明采用的期权类型；多头／空头则按本书定义的整体策略方向，不能按净买入张数或 debit／credit 猜测。

## 多头看涨圣诞树

其到期内在价值为

$$
G_{LC}(S_T)=(S_T-K_1)^+-(S_T-K_2)^+-(S_T-K_3)^+,
$$

分段写为

$$
G_{LC}(S_T)=
\begin{cases}
0, & S_T\le K_1,\\
S_T-K_1, & K_1<S_T\le K_2,\\
w_L, & K_2<S_T\le K_3,\\
w_L+K_3-S_T, & S_T>K_3.
\end{cases}
$$

- 下跌侧损益被限制为 $B$。
- 中间平台损益为 $w_L+B$。
- 上涨侧因净空 1 份 Call 而亏损无上限。
- 上方候选盈亏平衡点为 $K_3+w_L+B$；其他候选根须按 $B$ 所落分段逐一验证。

它的风险形状类似空头宽跨式，但限制了下跌侧风险。

## 多头看跌圣诞树

其到期内在价值为

$$
G_{LP}(S_T)=(K_3-S_T)^+-(K_2-S_T)^+-(K_1-S_T)^+,
$$

分段写为

$$
G_{LP}(S_T)=
\begin{cases}
w_R+S_T-K_1, & 0\le S_T<K_1,\\
w_R, & K_1\le S_T<K_2,\\
K_3-S_T, & K_2\le S_T<K_3,\\
0, & S_T\ge K_3.
\end{cases}
$$

- 上涨侧损益被限制为 $B$。
- 中间平台损益为 $w_R+B$。
- 下跌侧净空 1 份 Put；对股票类标的，$S_T\ge0$ 使数学损失有下界，但损失仍可能巨大。
- 下方候选盈亏平衡点为 $K_1-w_R-B$；其他候选根同样必须验证所在分段。

它的风险形状类似空头宽跨式，但限制了上涨侧风险。

## 空头圣诞树

空头看涨与空头看跌圣诞树分别是上述完整头寸的反向。它们类似多头宽跨式，通常受益于标的大幅运动，但其中一个方向的盈利潜力被封顶：

- 空头看涨圣诞树：下跌侧盈利受限，上涨侧盈利开放。
- 空头看跌圣诞树：上涨侧盈利受限；股票类标的的下跌侧盈利因价格下界而有限。

最大盈亏与盈亏平衡点取决于实际 $B$、$w_L$、$w_R$ 及标的价格下界，不能像等距蝶式一样给出一组无条件通用数值。

## Greeks 与波动率

在接近 Delta 中性的局部区域，本书的多头圣诞树通常类似空头宽跨式：

$$
-\Gamma,\qquad +\Theta,\qquad -\mathrm{Vega}.
$$

空头圣诞树局部方向大致相反：$+\Gamma$、$-\Theta$、$+\mathrm{Vega}$。这些符号并非全局恒定；价格越过任一执行价、期限缩短或偏斜变化时，净 Greeks 都可能显著改变。

## 执行与风险

- 订单必须明确 Call／Put、多头／空头、三个执行价、每腿买卖方向和到期日。
- 一侧仍有净裸空尾部，不能因名称像“有限风险宽跨式”就认为整体风险有限。
- 两条短腿可能被部分或分时提前指派，造成股票与剩余期权数量错配。
- 组合限价、保证金、压力情景、夹点风险与退出顺序都应在建仓前确定。

## 盈亏曲线（到期与到期前）

### 多头看涨圣诞树

![[../assets/圣诞树价差 Christmas Tree Spread 盈亏曲线.svg]]

### 空头看涨圣诞树

![[../assets/空头看涨圣诞树 Short Call Christmas Tree 盈亏曲线.svg]]

### 多头看跌圣诞树

![[../assets/多头看跌圣诞树 Long Put Christmas Tree 盈亏曲线.svg]]

### 空头看跌圣诞树

![[../assets/空头看跌圣诞树 Short Put Christmas Tree 盈亏曲线.svg]]

> [!note] 读图口径
> 四图覆盖本书定义下 Call／Put 与多头／空头的全部方向。实线为到期损益，虚线为尚余 30 天时的理论损益。注意“多头圣诞树”按本书命名为买一卖二，不等于“净买入期权更多”。

## 来源

- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/波动率价差策略 Volatility Spreads#圣诞树价差 / Christmas Tree|《期权波动率与定价》：圣诞树价差]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/知识图谱/比率价差与圣诞树|知识图谱：比率价差与圣诞树]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/风险考量 Risk Considerations|《期权波动率与定价》：风险考量]]
