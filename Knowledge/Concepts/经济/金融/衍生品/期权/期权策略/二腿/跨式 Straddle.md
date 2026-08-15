---
type: option-strategy
schema_version: 1
name: 跨式 Straddle
aliases:
  - Straddle
  - Long Straddle
  - Short Straddle
  - 跨式
  - 买入跨式
  - 卖出跨式
leg_count: 2
option_leg_count: 2
underlying_leg_count: 0
strategy_family: 波动率组合
status: completed
completion_status: completed
created_from: merged-existing-notes
created_at: 2026-08-15
updated_at: 2026-08-15
tags: [期权, 期权策略, 二腿策略, 跨式, 波动率]
domain: 经济
subdomain: 金融
product_domain: 衍生品
instrument: 期权
---

# 跨式 / Straddle

## 定义

跨式由同一标的、同一到期日、同一行权价 $K$ 的一份 Call 与一份 Put 组成。两腿同时买入是多头跨式，同时卖出是空头跨式。

## 标准腿结构

| 腿 | 多头跨式 | 空头跨式 |
|---|---:|---:|
| Call，行权价 $K$ | $+1$ | $-1$ |
| Put，行权价 $K$ | $+1$ | $-1$ |

设 Call 与 Put 权利金分别为 $c,p$，总权利金 $D=c+p$。

## 多头跨式到期损益

$$
\Pi_T^{\mathrm{long}}
=\max(S_T-K,0)+\max(K-S_T,0)-D
=|S_T-K|-D.
$$

- 最大亏损：$D$，在 $S_T=K$ 时发生。
- 上方盈亏平衡点：$K+D$。
- 下方盈亏平衡点：$K-D$；若该值小于 $0$，经济上不存在负价格盈亏平衡点。
- 上涨侧盈利无上限；$S_T=0$ 时的下跌端点损益为 $K-D$。只有当 $D<K$ 时，它才是下跌侧的最大盈利；若 $D\ge K$，下跌侧不存在盈利区间。

多头跨式通常为正 Gamma、正 Vega、负日历 Theta。它交易的是价格运动和波动率，而不只是“看多或看空”。即使最终价格大幅变化，若隐含波动率先下跌、时间损耗过快或路径不利，持有期仍可能亏损。

## 空头跨式到期损益

$$
\Pi_T^{\mathrm{short}}
=D-|S_T-K|.
$$

- 最大盈利：$D$，在 $S_T=K$ 时达到。
- 盈亏平衡点同样为 $K-D$ 与 $K+D$。
- 上涨侧亏损无上限；下跌侧最大亏损为 $K-D$（当 $D<K$），在 $S_T=0$ 时发生。

空头跨式通常为负 Gamma、负 Vega、正日历 Theta。平值且临近到期时 Gamma 可能高度集中，Delta 会快速朝不利方向漂移；“高胜率”不能替代最大损失与保证金分析。

## 持有期风险与动态对冲

到期公式没有反映隐含波动率曲面、期限结构和路径。[[动态Delta对冲]]可以降低局部方向暴露，但无法消除跳空、流动性、滑点、交易成本或离散对冲误差。美式期权还可能提前指派，使一条期权腿变成股票头寸。

## 与宽跨式比较

[[宽跨式 Strangle]]使用不同的 Put 与 Call 行权价，初始权利金通常较低，但需要更大价格运动才穿过盈亏平衡点。两个行权价之间是多头宽跨式的最大亏损区间，也是空头宽跨式的最大盈利区间；跨式对应的区间退化为单一行权价。两者不能只比较收到或支付的权利金，还要比较相同到期、相同 Delta 和尾部保证金下的风险。

## 关联概念

- [[Gamma]]：多头跨式通常正 Gamma，空头跨式通常负 Gamma。
- [[Theta]]：多头支付时间价值，空头收取时间价值。
- [[Vega]]：隐含波动率变化会显著影响持有期价值。
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/知识图谱/跨式与宽跨式（Natenberg）|Natenberg：跨式与宽跨式]]

## 盈亏曲线（到期与到期前）

### 多头跨式

![[../assets/跨式 Straddle 盈亏曲线.svg]]

### 空头跨式

![[../assets/空头跨式 Short Straddle 盈亏曲线.svg]]

> [!note] 读图口径
> 两图分别展示多头与空头跨式。实线为到期损益，虚线为两腿尚余 30 天时的理论损益；虚线直观显示即使标的暂时停在行权价附近，剩余时间价值仍会改变持有期损益。

## 来源

- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/波动率价差策略 Volatility Spreads#跨式策略 / Straddle|《Option Volatility and Pricing》：跨式策略]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/风险考量 Risk Considerations|风险考量]]
