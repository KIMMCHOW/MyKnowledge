---
type: concept
schema_version: 1
name: Color
aliases:
  - Gamma decay
  - DgammaDtime
status: completed
completion_status: completed
created_from: Option Volatility and Pricing 第9章
created_at: 2026-08-15
updated_at: 2026-08-15
tags:
  - 期权
  - Greeks
  - 时间价值
  - 凸性
domain: 经济
subdomain: 金融
product_domain: 衍生品
instrument: 期权
concept_group: 希腊字母
---

# Color

> [!definition] 定义
> Color 衡量 Gamma 对时间变量的敏感度。它是专有风险指标名称，通常直接保留英文。

## 数学表示

本目录用 $\tau$ 表示距到期时间：

$$
\boxed{
\mathrm{Color}_{\tau}
=\frac{\partial\Gamma}{\partial\tau}
=\frac{\partial\mathrm{Charm}_{\tau}}{\partial S}
=\frac{\partial^3V}{\partial S^2\,\partial\tau}
}
$$

若 $u$ 表示向前推进的日历时间，则

$$
\boxed{
\mathrm{Color}_{\text{calendar}}
=\frac{\partial\Gamma}{\partial u}
=-\mathrm{Color}_{\tau}
}
$$

Gamma 的局部时间漂移为

$$
d\Gamma
\approx
\mathrm{Color}_{\tau}\,d\tau
=\mathrm{Color}_{\text{calendar}}\,du.
$$

期权价值中的对应三阶项为

$$
dV_{S,S,\tau}^{(3)}
\approx
\frac{1}{2}\mathrm{Color}_{\tau}(dS)^2d\tau.
$$

## 典型形态

- 以距到期时间 $\tau$ 求导时，平值期权的 Color 通常为负：增加剩余期限会使集中的 Gamma 降低；时间流逝则会使平值 Gamma 上升。
- 看涨 Delta 接近 $0.05$ 或 $0.95$、看跌 Delta 接近 $-0.05$ 或 $-0.95$ 的区域可出现较大的正 Color 波瓣。
- 看涨 Delta 接近 $0.15$ 或 $0.85$、看跌 Delta 接近 $-0.15$ 或 $-0.85$ 时，Color 常接近 $0$。
- $|\mathrm{Color}|$ 通常在平值、临近到期且低波动率时最显著。

## 风险管理含义

当前 Gamma 不会在时间推进后保持不变：

$$
\Gamma_{\text{future}}
\approx
\Gamma_{\text{now}}
+\mathrm{Color}_{\text{calendar}}\,\Delta u.
$$

临近到期的平值头寸即使隔夜没有价格变化，也可能在下一交易日呈现显著不同的 Gamma 与再对冲需求。

## 关联概念

- [[Gamma]]：Color 是 Gamma 的时间敏感度。
- [[Charm]]：Color 也可写为 Charm 对标的价格的敏感度。
- [[Speed]]：Gamma 对标的价格的敏感度。
- [[Zomma]]：Gamma 对波动率的敏感度。
- [[Theta]]：所有时间导数都必须先统一 $\tau$ 与日历时间口径。

## 来源

- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/风险度量（二） Risk Measurement II#Gamma / Gamma|《Option Volatility and Pricing》第9章：Color]]
