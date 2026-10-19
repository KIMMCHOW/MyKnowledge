---
type: concept
schema_version: 1
name: Vega
status: completed
completion_status: completed
created_from: user-material-refactor
created_at: 2026-08-09
updated_at: 2026-10-19
tags:
  - 期权
  - Greeks
  - 波动率
domain: 经济
subdomain: 金融
product_domain: 衍生品
instrument: 期权
concept_group: 希腊字母
---

# Vega

## 定义

Vega 衡量期权理论价值对定价模型中波动率输入的局部敏感度。Vega 并不是一个希腊字母，但属于最常用的 Greeks。

## 核心解释

Vega 衡量期权价值对波动率输入的局部敏感度，常按一个波动率百分点报价。它只描述所选波动率输入的小幅平行变化，不能覆盖偏斜、微笑和期限结构。

## 数学表示

$$
\boxed{\mathrm{Vega}=\frac{\partial V}{\partial\sigma}}
$$

在波动率只发生小幅变化时，

$$
dV\approx\mathrm{Vega}\,d\sigma.
$$

若 $\sigma$ 以小数表示，则一个波动率百分点等于 $d\sigma=0.01$，因此

$$
\mathrm{Vega}_{1\text{ vol point}}
=0.01\frac{\partial V}{\partial\sigma}.
$$

## 典型形态

- 普通期权多头通常具有正 Vega；波动率上升会提高其模型价值，空头通常相反。
- Vega 通常在平值附近最大，并随距到期时间增加而增大。
- 单一 Vega 只描述所选波动率输入的平行小幅变化，不能完整描述偏斜、微笑和期限结构变化。

## Vega 如何漂移

$$
d(\mathrm{Vega})\approx
\mathrm{Vanna}\,dS
+\mathrm{Volga}\,d\sigma
+\mathrm{VegaDecay}\,dt.
$$

其中：

$$
\mathrm{Vanna}=\frac{\partial\mathrm{Vega}}{\partial S},
\qquad
\mathrm{Volga}=\frac{\partial\mathrm{Vega}}{\partial\sigma},
\qquad
\mathrm{VegaDecay}=\frac{\partial\mathrm{Vega}}{\partial t}.
$$

## 示例

若隐含波动率从 $20\%$ 升到 $21\%$，期权理论价值从 $5.00$ 升到 $5.12$，则按一个波动率百分点计的 Vega 约为

$$
\frac{5.12-5.00}{1}=0.12.
$$

持有 $10$ 张、乘数 $100$ 时，波动率上升 $1$ 个百分点约增加 $0.12\times10\times100=120$ 个报价单位。该数值只适用于当前合约和当前曲面位置。

## 关联概念

- [[隐含波动率]]：隐含波动率变化通过 Vega 影响期权估值。
- [[Vanna]]：Vega 对标的价格的敏感度。
- [[Volga（Vomma）|Volga / Vomma]]：Vega 对波动率的敏感度。
- [[Vega Decay|Vega decay]]：Vega 随当前时间推进的变化率。
- [[波动率偏斜 Skew|波动率偏斜（Skew）]]：各腿 Vega 抵消不代表偏斜、曲率或期限风险为零。
- [[Knowledge/Concepts/经济/金融/衍生品/期权/期权策略/二腿/跨式 Straddle|跨式]]、[[Knowledge/Concepts/经济/金融/衍生品/期权/期权策略/二腿/宽跨式 Strangle|宽跨式]]：多头结构通常具有正 Vega。

## 相关问题

- Vega 与 Volga 的区别是什么？
- 偏斜变化为何不能只用 Vega 衡量？
- 不同到期日的 Vega 如何加总？

## 来源

- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/风险度量（二） Risk Measurement II#Vega / Vega|《Option Volatility and Pricing》第9章：Vega]]
- [[Vega（Natenberg）|Natenberg 期权知识图谱：Vega]]
