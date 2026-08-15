---
type: option-strategy
schema_version: 1
name: 对角价差
aliases:
  - Diagonal Spread
  - Diagonal Call
  - Diagonal Put
  - Call Diagonal Spread
  - Put Diagonal Spread
  - 看涨对角价差
  - 看跌对角价差
  - 看涨期权对角价差
  - 看跌期权对角价差
leg_count: 2
option_leg_count: 2
underlying_leg_count: 0
strategy_family: 对角价差
status: completed
completion_status: completed
created_from: merged-call-put-pages
created_at: 2026-08-15
updated_at: 2026-08-15
tags: [期权, 期权策略, 二腿策略, 对角价差]
domain: 经济
subdomain: 金融
product_domain: 衍生品
instrument: 期权
---

# 对角价差 / Diagonal Spread

## 定义

对角价差由**同一标的、同一期权类型、不同执行价、不同到期日**的两条反向期权腿组成。它同时含有垂直价差的执行价风险与日历价差的期限结构风险，可以全部使用 Call，也可以全部使用 Put。

记近月到期日 $T_N<T_F$（远月到期日），近月、远月执行价分别为 $K_N$、$K_F$，且 $K_N\ne K_F$。有符号初始净支出为

$$
D=\sum_iq_iV_i(t_0),
$$

其中多头数量为正、空头数量为负；$D>0$ 是净支出，$D<0$ 是净收入。

> [!warning] 对角价差没有唯一“标准形状”
> $K_N$ 与 $K_F$ 的高低、两腿数量、Call／Put 类型和期限都可变化。第 11 章的核心结论是：变体太多，几乎不能仅凭名称概括风险，必须逐一分析。只有 $1:1$、同类型且两腿 Delta 大致相等时，它才近似传统日历价差。

## 代表构造

### Call 对角价差

常见多头构造为卖出近月 Call、买入远月 Call：

$$
-C(K_N,T_N)+C(K_F,T_F).
$$

许多偏多构造选择远月较低执行价、近月较高执行价，但这不是定义要求。反向全部买卖方向即为空头构造，近月结束后可能留下裸空远月 Call。

### Put 对角价差

常见多头构造为卖出近月 Put、买入远月 Put：

$$
-P(K_N,T_N)+P(K_F,T_F).
$$

许多偏空或保护型构造选择远月较高执行价、近月较低执行价，同样不是唯一标准。反向结构在近月结束后可能留下裸空远月 Put。

## 近月到期日的估值

在 $T_N$，远月腿仍有时间价值。多头构造的每股损益为

$$
\Pi_{T_N}(S)=V_j\!\left(S,K_F,T_F-T_N;\,\Sigma_{T_N}^{(T_F)},r,q\right)-h_j(S,K_N)-D,
$$

其中 $j\in\{C,P\}$，

$$
h_C(S,K)=(S-K)^+,
\qquad
h_P(S,K)=(K-S)^+.
$$

这是一条**评估日曲线**，不是两个期权共同到期的固定终值折线。远月价值取决于当时的波动率曲面、利率、股息和剩余期限；近月腿结束后继续持仓，损益还会继续变化。

## 最大盈亏与盈亏平衡

- 最大盈利、最大亏损与盈亏平衡点不能仅由 $K_N$、$K_F$ 和初始现金流固定下来。
- 必须指定评估日、远月隐含波动率、利率、股息及管理方式，再数值求解 $\Pi_{T_N}(S)=0$。
- 执行价顺序改变后，曲线峰值、方向暴露和尾部都可能完全不同；不能套用垂直价差的“翼宽减净支出”。
- 提前指派、腿间错配、近月到期后遗留股票或单腿远月期权，会使实际路径风险超出静态图。

## Greeks 与波动率

组合 Greek 一律按实际数量与方向逐腿相加。若近月腿与远月腿的持仓数量分别为 $q_N$ 和 $q_F$（多头为正、空头为负），则

$$
G_{\text{diag}}=q_NG_N+q_FG_F.
$$

仅对本页的 $1:1$ 多头代表结构，$q_N=-1, q_F=+1$，上式才化为 $G_{\text{diag}}=G_F-G_N$。

仅对 $1:1$、同类型且两腿 Delta 接近的“日历型对角价差”，多头结构才常在局部呈现较小 Delta、$-\Gamma$、$+\Theta$、$+\mathrm{Vega}$。一般对角价差不能预设这些符号；执行价偏斜、期限结构及标的穿越任一执行价都可能让净 Greeks 反转。

## 执行与风险

- 使用组合限价单；不同执行价与月份的流动性通常不对称。
- 美式近月空腿可能提前被指派；到期贴近 $K_N$ 时存在夹点风险。
- 展期会改变执行价关系、净成本和全部 Greeks，应视为新交易重新评估。
- 反向 Call 结构可能留下裸空远月 Call 的无限上行风险；反向 Put 结构可能留下裸空远月 Put 的重大下跌风险。
- 期货期权的不同月份可能对应不同期货标的，除波动率与时间风险外还有跨期基差风险。

## 盈亏曲线（近月到期日与更早评估日）

### Call 多头代表构造

![[../assets/看涨对角价差 Diagonal Call 盈亏曲线.svg]]

### Call 空头代表构造

![[../assets/空头看涨对角价差 Short Call Diagonal Spread 盈亏曲线.svg]]

### Put 多头代表构造

![[../assets/看跌对角价差 Diagonal Put 盈亏曲线.svg]]

### Put 空头代表构造

![[../assets/空头看跌对角价差 Short Put Diagonal Spread 盈亏曲线.svg]]

> [!note] 读图口径
> 四图覆盖 Call／Put 与多头／空头代表构造。实线表示近月腿到期、远月腿仍存续时的理论损益；虚线表示更早评估日的理论损益。它们只对应图中注明的执行价和期限组合，不能代表所有对角价差。

## 来源

- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/波动率价差策略 Volatility Spreads#对角价差 / Diagonal Spreads|《期权波动率与定价》：对角价差]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/风险考量 Risk Considerations|《期权波动率与定价》：风险考量]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/知识图谱/日历与对角价差|知识图谱：日历与对角价差]]
