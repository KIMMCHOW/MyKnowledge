---
type: option-strategy
schema_version: 1
name: 时间蝶式价差
aliases:
  - Time Butterfly
  - Time Fly
  - Call Time Butterfly
  - Put Time Butterfly
  - Long Time Butterfly
  - Short Time Butterfly
  - 时间蝶式
  - 时间蝶式价差
  - 看涨时间蝶式
  - 看跌时间蝶式
leg_count: 3
option_leg_count: 3
underlying_leg_count: 0
strategy_family: 时间蝶式价差
status: completed
completion_status: completed
created_from: Option Volatility and Pricing 第11章
created_at: 2026-08-15
updated_at: 2026-08-15
tags: [期权, 期权策略, 三腿策略, 时间蝶式, 日历价差, 波动率期限结构]
domain: 经济
subdomain: 金融
product_domain: 衍生品
instrument: 期权
---

# 时间蝶式价差 / Time Butterfly

## 定义与腿数

**时间蝶式价差**（time butterfly，简称 **time fly**）由**同一标的、同一期权类型、同一执行价**，但三个不同到期日的期权组成。三个到期日通常大致等距：

$$
T_1<T_2<T_3,
\qquad
T_2-T_1\approx T_3-T_2.
$$

$T_1$ 与 $T_3$ 是**蝶翼**（wings），$T_2$ 是**蝶身**（body）。三个系列必须全部使用 Call，或全部使用 Put，不混用两种期权。

> [!note] 三腿不等于三张
> 本笔记按**不同合约系列**计腿：$T_1$、$T_2$、$T_3$ 共 3 腿，所以归入三腿策略；蝶身数量为 2，整组实际共有 4 张期权，数量比为 $1:2:1$。

记 $V_j(S,K,T)$ 为类型 $j\in\{C,P\}$ 的期权价值，买入数量记正、卖出数量记负。

## 多头、空头与本书的命名

| 方向 | $T_1$ 近月蝶翼 | $T_2$ 蝶身 | $T_3$ 远月蝶翼 | 整组数量 | 常见初始现金流 |
| --- | ---: | ---: | ---: | ---: | --- |
| **多头时间蝶式** | 卖出 1 | 买入 2 | 卖出 1 | $-1:+2:-1$ | 通常净借记（debit） |
| **空头时间蝶式** | 买入 1 | 卖出 2 | 买入 1 | $+1:-2:+1$ | 通常净贷记（credit） |

多头时间蝶式可拆成两个方向相反、共享 $T_2$ 的相邻日历价差：

$$
\underbrace{[-V_j(T_1)+V_j(T_2)]}_{\text{买入 }T_1/T_2\text{ 日历价差}}
+
\underbrace{[+V_j(T_2)-V_j(T_3)]}_{\text{卖出 }T_2/T_3\text{ 日历价差}}
=-V_j(T_1)+2V_j(T_2)-V_j(T_3).
$$

> [!important] 命名与传统蝶式正好相反
> 在本书的命名中，**卖出两翼、买蝶身**才是多头时间蝶式；**买入两翼、卖蝶身**则是空头时间蝶式。这与按执行价排列的传统蝶式相反。上表的 debit／credit 依赖“各到期月隐含波动率相同”等假设；实际期限结构可使现金流反转，不应只凭借记或贷记判断方向。

## Call 与 Put 腿式

### 看涨时间蝶式

$$
\begin{aligned}
\text{多头 Call Time Butterfly}
&=-C(K,T_1)+2C(K,T_2)-C(K,T_3),\\
\text{空头 Call Time Butterfly}
&=+C(K,T_1)-2C(K,T_2)+C(K,T_3).
\end{aligned}
$$

### 看跌时间蝶式

$$
\begin{aligned}
\text{多头 Put Time Butterfly}
&=-P(K,T_1)+2P(K,T_2)-P(K,T_3),\\
\text{空头 Put Time Butterfly}
&=+P(K,T_1)-2P(K,T_2)+P(K,T_3).
\end{aligned}
$$

Call／Put 只说明使用的期权类型，不代表多空方向。因为三个到期日不同，Call 与 Put 构造也不能像同到期的等距蝶式那样无条件视为等价。

## 估值时点：没有共同到期损益线

令多头时间蝶式的有符号初始净支出为

$$
D=-V_j(t_0;K,T_1)+2V_j(t_0;K,T_2)-V_j(t_0;K,T_3).
$$

$D>0$ 表示净借记，$D<0$ 表示净贷记。在任意 $t<T_1$ 时整组平仓，其理论损益为

$$
\Pi_t=-V_j(t;K,T_1)+2V_j(t;K,T_2)-V_j(t;K,T_3)-D.
$$

以上采用每股名义损益，并忽略融资、手续费与滑点；若计入资金时间价值，应将初始现金流 $D$ 滚存至评估日后再相减。

若选择近月到期日 $T_1$ 作为评估时点，并假定当日同时处理所有腿，则

$$
\begin{aligned}
\Pi_{T_1}(S)
=&-h_j(S,K)
+2V_j\!\left(S,K,T_2-T_1;\Sigma_{T_1}^{(T_2)},r,y\right)\\
&-V_j\!\left(S,K,T_3-T_1;\Sigma_{T_1}^{(T_3)},r,y\right)-D,
\end{aligned}
$$

其中

$$
h_C(S,K)=(S-K)^+,
\qquad
h_P(S,K)=(K-S)^+,
$$

$\Sigma_{T_1}^{(T_i)}$ 表示 $T_1$ 时对应到期日的隐含波动率曲面，$r$ 为利率，$y$ 为连续股息率。空头时间蝶式在同一估值口径下是整组反向。

> [!warning] 不存在预先锁定的最大盈亏与 BE
> 三个到期日不同，因此没有像垂直价差那样的共同到期折线。任一“最大盈利”、“最大亏损”或盈亏平衡点（BE）都必须先指定估值日、各期限隐含波动率、利率、股息与平仓规则，再数值计算。若让近月腿先到期而不同时平仓，后续结果还取决于逐次到期、行权或指派及管理动作的路径。

## Greeks 与波动率期限结构

对任一组合 Greek $G$，多头时间蝶式的净暴露为

$$
G_{\mathrm{long}}=-G(T_1)+2G(T_2)-G(T_3),
\qquad
G_{\mathrm{short}}=-G_{\mathrm{long}}.
$$

在各腿都接近 ATM、到期间隔大致相等、各期限隐含波动率相近的局部条件下，本书给出的典型特征为：

| 方向 | Delta | Gamma | Theta | Vega |
| --- | --- | --- | --- | --- |
| 多头时间蝶式 | 通常接近中性，但不保证为 0 | $-$ | $+$ | $+$ |
| 空头时间蝶式 | 与多头相反 | $+$ | $-$ | $-$ |

多头组合的价值在标的远离 $K$ 时往往收缩，对应局部负 Gamma；时间流逝通常有利，对应正 Theta；平行上移波动率在本书的基准情形中通常有利，对应正 Vega。这些都是**指定位置与参数下的局部性质**，不是全域不变的符号。

这一组合也不只是交易单一 Vega：

- 多头时间蝶式买入两张 $T_2$ 蝶身，同时卖出 $T_1$ 与 $T_3$ 两翼，实际上在交易隐含波动率**期限结构的曲率**。
- $T_2$ 的隐含波动率单独上升通常有利于多头；$T_1$ 或 $T_3$ 单独上升则通常不利。实际影响还要按三腿各自的 Vega 加权。
- 期限结构倒挂、中间月供需失衡或非平行波动率变化，都可以使典型 Vega 表现或初始 debit／credit 失效。

## 利率、股息与 Call／Put 差异

三个到期日对利率和股息的敏感度不同。多头时间蝶式的净 Rho 为

$$
\rho_{\mathrm{long}}=-\rho(T_1)+2\rho(T_2)-\rho(T_3),
$$

股息敏感度也有相同的二阶差分形式。因此，组合层面的 Rho 和股息方向**没有不依赖参数的固定符号**，应逐腿估值。

对欧式期权，令 $\tau_i=T_i-t$ 为各腿在估值时点 $t$ 的剩余期限。若使用连续股息率 $y$ 的 Put–Call parity，多头 Call 与多头 Put 时间蝶式的价值差为

$$
\begin{aligned}
B_C-B_P
=&-\left(Se^{-y\tau_1}-Ke^{-r\tau_1}\right)
+2\left(Se^{-y\tau_2}-Ke^{-r\tau_2}\right)\\
&-\left(Se^{-y\tau_3}-Ke^{-r\tau_3}\right).
\end{aligned}
$$

这一利率与股息贴现项通常不为零，说明 Call 与 Put 时间蝶式在到期前不是无条件等价的替代品。对美式期权，还必须另行考虑提前行权权利。

## 执行、指派与路径风险

- **多头**时间蝶式在 $T_1$ 与 $T_3$ 持有空头蝶翼；**空头**时间蝶式在 $T_2$ 持有两张空头蝶身。任一美式空头腿都可能被提前指派。
- 美式 Call 在除息前、美式 Put 深度实值且剩余时间价值很少时，应重点检查提前行权与指派概率。
- 每过一个到期日，组合的腿数与风险性质都会改变。若不同时平仓，行权或指派可留下标的头寸，还可能使后续空头腿变成未备兑暴露。
- 到期价格靠近 $K$ 时存在夹点风险；部分行权、部分指派或盘后标的波动，都可以使实际仓位偏离理论的 $1:2:1$。
- 三个到期月的流动性、买卖价差和波动率曲面可同时不同。下单时应使用组合限价单，并明确 Call／Put、多头／空头、共同执行价、三个到期日及 $1:2:1$ 数量比。

## 理论损益曲线

### 多头看涨时间蝶式 / Long Call Time Butterfly

![[../assets/多头看涨时间蝶式 Long Call Time Butterfly 盈亏曲线.svg]]

### 空头看涨时间蝶式 / Short Call Time Butterfly

![[../assets/空头看涨时间蝶式 Short Call Time Butterfly 盈亏曲线.svg]]

### 多头看跌时间蝶式 / Long Put Time Butterfly

![[../assets/多头看跌时间蝶式 Long Put Time Butterfly 盈亏曲线.svg]]

### 空头看跌时间蝶式 / Short Put Time Butterfly

![[../assets/空头看跌时间蝶式 Short Put Time Butterfly 盈亏曲线.svg]]

> [!note] 读图口径
> 时间蝶式的曲线是指定估值日与指定波动率期限结构下的**理论损益情景**，不是所有腿在同一天到期的 payoff。阅读曲线时必须同时核对估值日、剩余期限、各到期月 IV、利率和股息假设。

## 来源

- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/波动率价差策略 Volatility Spreads#时间蝶式价差 / Time Butterfly|《期权波动率与定价》第 11 章：时间蝶式（English 109–112）]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/期权策略/二腿/日历价差 Calendar Spread|日历价差 / Calendar Spread]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/期权策略/三腿/蝶式价差 Butterfly Spread|蝶式价差 / Butterfly Spread]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/美式期权的提前行权 Early Exercise of American Options|《期权波动率与定价》：美式期权的提前行权]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/风险考量 Risk Considerations|《期权波动率与定价》：风险考量]]
