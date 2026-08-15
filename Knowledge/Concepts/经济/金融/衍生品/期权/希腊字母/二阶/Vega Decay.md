---
type: concept
schema_version: 1
name: Vega Decay
aliases:
  - Vega decay
  - DvegaDtime
  - Veta
status: completed
completion_status: completed
created_from: Option Volatility and Pricing 第9章
created_at: 2026-08-15
updated_at: 2026-08-15
tags:
  - 期权
  - Greeks
  - 时间价值
  - 波动率
domain: 经济
subdomain: 金融
product_domain: 衍生品
instrument: 期权
concept_group: 希腊字母
---

# Vega Decay

> [!definition] 定义
> Vega decay（也称 DvegaDtime；部分资料称 Veta）衡量 Vega 对时间变量的敏感度。

## 数学表示

本目录用 $\tau$ 表示距到期时间：

$$
\boxed{
\mathrm{VegaDecay}_{\tau}
=\frac{\partial\mathrm{Vega}}{\partial\tau}
=\frac{\partial\Theta_{\tau}}{\partial\sigma}
=\frac{\partial^2V}{\partial\sigma\,\partial\tau}
}
$$

若 $u$ 表示向前推进的日历时间，则“随时间流逝的 Vega 衰减”为

$$
\boxed{
\mathrm{VegaDecay}_{\text{calendar}}
=\frac{\partial\mathrm{Vega}}{\partial u}
=-\mathrm{VegaDecay}_{\tau}
}
$$

局部 Vega 漂移为

$$
d(\mathrm{Vega})
\approx
\mathrm{VegaDecay}_{\tau}\,d\tau
=\mathrm{VegaDecay}_{\text{calendar}}\,du.
$$

## 典型形态

- 普通期权的 Vega 通常随距到期时间增加而增大，因此 $\mathrm{VegaDecay}_{\tau}$ 常为正，而按日历时间定义的衰减常为负。
- Delta 位于约 $0.10$–$0.90$ 区间的期权，其 Vega 通常对时间更敏感；绝对值峰值常在约 $0.20$ 与 $0.80$ Delta 区域。
- 随临近到期，短期期权的 Vega 变化速度通常快于长期期权。

## 风险管理含义

当前 Vega 中性不代表未来仍然 Vega 中性。即使标的和波动率不动，组合 Vega 也会因时间推进而变化：

$$
\mathrm{Vega}_{\text{future}}
\approx
\mathrm{Vega}_{\text{now}}
+\mathrm{VegaDecay}_{\text{calendar}}\,\Delta u.
$$

期限价差尤其需要观察各到期月份的 Vega decay，而不能只加总当前 Vega。

## 关联概念

- [[Vega]]：Vega decay 描述 Vega 的时间漂移。
- [[Theta]]：同一混合偏导也可写为 $\partial\Theta_{\tau}/\partial\sigma$。
- [[Volga（Vomma）|Volga / Vomma]]：Vega 对波动率的敏感度。
- [[Vanna]]：Vega 对标的价格的敏感度。

## 来源

- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/风险度量（二） Risk Measurement II#Vega / Vega|《Option Volatility and Pricing》第9章：Vega decay]]
