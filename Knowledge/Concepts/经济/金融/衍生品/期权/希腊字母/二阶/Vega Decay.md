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
> Vega decay（也称 DvegaDtime；部分资料称 Veta）衡量当前时间 $t$ 向前推进时 Vega 的局部变化率。

## 数学表示

令 $t$ 表示当前时间，到期日 $T$ 固定，剩余期限为 $\tau=T-t$：

$$
\boxed{
\mathrm{VegaDecay}
=\frac{\partial\mathrm{Vega}}{\partial t}
=\frac{\partial\Theta}{\partial\sigma}
=\frac{\partial^2V}{\partial\sigma\,\partial t}
=-\frac{\partial\mathrm{Vega}}{\partial\tau}
}
$$

局部 Vega 漂移为

$$
d(\mathrm{Vega})
\approx
\mathrm{VegaDecay}\,dt
=\frac{\partial\mathrm{Vega}}{\partial\tau}\,d\tau,
\qquad d\tau=-dt.
$$

## 典型形态

- 普通期权的 Vega 通常随剩余期限增加而增大，因此随当前时间 $t$ 推进定义的 Vega decay 通常为负。
- Delta 位于约 $0.10$–$0.90$ 区间的期权，其 Vega 通常对时间更敏感；绝对值峰值常在约 $0.20$ 与 $0.80$ Delta 区域。
- 随临近到期，短期期权的 Vega 变化速度通常快于长期期权。

## 风险管理含义

当前 Vega 中性不代表未来仍然 Vega 中性。即使标的和波动率不动，组合 Vega 也会因时间推进而变化：

$$
\mathrm{Vega}_{\text{future}}
\approx
\mathrm{Vega}_{\text{now}}
+\mathrm{VegaDecay}\,\Delta t.
$$

期限价差尤其需要观察各到期月份的 Vega decay，而不能只加总当前 Vega。

## 关联概念

- [[Vega]]：Vega decay 描述 Vega 的时间漂移。
- [[Theta]]：同一混合偏导也可写为 $\partial\Theta/\partial\sigma$。
- [[Volga（Vomma）|Volga / Vomma]]：Vega 对波动率的敏感度。
- [[Vanna]]：Vega 对标的价格的敏感度。

## 来源

- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/风险度量（二） Risk Measurement II#Vega / Vega|《Option Volatility and Pricing》第9章：Vega decay]]
