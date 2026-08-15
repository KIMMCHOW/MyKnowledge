---
type: option-strategy
schema_version: 1
name: 宽跨式 Strangle
aliases:
  - Strangle
  - Long Strangle
  - Short Strangle
  - 宽跨式
  - 买入宽跨式
  - 卖出宽跨式
leg_count: 2
option_leg_count: 2
underlying_leg_count: 0
strategy_family: 波动率组合
status: completed
completion_status: completed
created_from: merged-existing-notes
created_at: 2026-08-15
updated_at: 2026-08-15
tags: [期权, 期权策略, 二腿策略, 宽跨式, 波动率]
domain: 经济
subdomain: 金融
product_domain: 衍生品
instrument: 期权
---

# 宽跨式 / Strangle

## 定义

宽跨式由同一标的、同一到期日的一份低行权价 Put 与一份高行权价 Call 组成，满足 $K_P<K_C$。两腿同时买入是多头宽跨式，同时卖出是空头宽跨式。

## 标准腿结构

| 腿 | 多头宽跨式 | 空头宽跨式 |
|---|---:|---:|
| Put，行权价 $K_P$ | $+1$ | $-1$ |
| Call，行权价 $K_C$ | $+1$ | $-1$ |

设两腿总权利金为 $D=p+c$。

## 多头宽跨式到期损益

$$
\Pi_T^{\mathrm{long}}
=\max(K_P-S_T,0)
+\max(S_T-K_C,0)-D.
$$

分段为

$$
\Pi_T^{\mathrm{long}}=
\begin{cases}
K_P-S_T-D, & S_T<K_P,\\
-D, & K_P\le S_T\le K_C,\\
S_T-K_C-D, & S_T>K_C.
\end{cases}
$$

- 最大亏损：$D$，在 $K_P\le S_T\le K_C$ 时发生。
- 下方盈亏平衡点：$K_P-D$，仅当该值不小于 $0$ 时在可行价格范围内存在；上方盈亏平衡点：$K_C+D$。
- 上涨侧盈利无上限；$S_T=0$ 时的下跌端点损益为 $K_P-D$。只有当 $D<K_P$ 时，它才是下跌侧的最大盈利；若 $D\ge K_P$，下跌侧不存在盈利区间。

多头宽跨式通常为正 Gamma、正 Vega、负日历 Theta，但标的位于两个行权价之间时，两翼较远，局部 Gamma 与 Vega 往往低于相近的平值跨式。

## 空头宽跨式到期损益

$$
\Pi_T^{\mathrm{short}}
=D-\max(K_P-S_T,0)-\max(S_T-K_C,0).
$$

- 最大盈利：$D$，在 $K_P\le S_T\le K_C$ 时达到。
- 盈亏平衡点同样为 $K_P-D$ 与 $K_C+D$；其中下方盈亏平衡点仅在 $K_P-D\ge 0$ 时经济上存在。
- 上涨侧亏损无上限；下跌侧最大亏损为 $K_P-D$（当 $D<K_P$），在 $S_T=0$ 时发生。

空头宽跨式通常为负 Gamma、负 Vega、正日历 Theta。两个短期权都可能变成裸空尾部风险；经纪商保证金上调、跳空和波动率飙升可能在到达盈亏平衡点前造成显著浮亏或强平。

## 执行与风险管理

美式期权可能提前指派，尤其是深度价内且剩余时间价值很低时。[[动态Delta对冲]]只能控制局部 Delta，不能消除跳跃、偏斜变化、流动性和交易成本。若要限制双侧损失，可在更远端买入保护翼形成[[铁鹰式 Iron Condor]]，但保护成本会降低净收入。

## 与跨式比较

[[跨式 Straddle]]两腿使用同一行权价，通常支付或收取更多权利金，局部 Gamma 更集中。宽跨式的两个行权价之间，是多头的最大亏损区间、空头的最大盈利区间；多头需要更大运动才可能获利，空头则仍承担两侧尾部风险。

## 关联概念

- [[隐含波动率]]与[[已实现波动率]]：决定持有期波动率交易结果。
- [[Gamma]]、[[Theta]]、[[Vega]]：描述多空宽跨式的核心局部风险。
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/知识图谱/跨式与宽跨式（Natenberg）|Natenberg：跨式与宽跨式]]

## 盈亏曲线（到期与到期前）

![[../assets/宽跨式 Strangle 盈亏曲线.svg]]

> [!note] 读图口径
> 图中展示多头宽跨式。实线为到期损益，虚线为两腿尚余 30 天时的理论损益；两个行权价之间是到期最大亏损平台，但到期前仍保留时间价值。空头宽跨式为同一组腿的反向损益。

## 来源

- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/波动率价差策略 Volatility Spreads#宽跨式策略 / Strangle|《Option Volatility and Pricing》：宽跨式策略]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/风险考量 Risk Considerations|风险考量]]
