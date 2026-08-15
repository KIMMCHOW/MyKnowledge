---
type: concept
schema_version: 1
name: Charm
aliases:
  - Delta decay
  - DdeltaDtime
status: completed
completion_status: completed
created_from: Option Volatility and Pricing 第9章
created_at: 2026-08-15
updated_at: 2026-08-15
tags:
  - 期权
  - Greeks
  - 时间价值
domain: 经济
subdomain: 金融
product_domain: 衍生品
instrument: 期权
concept_group: 希腊字母
---

# Charm

> [!definition] 定义
> Charm 又称 Delta decay，衡量当前时间 $t$ 向前推进时 Delta 的局部变化率。

## 数学表示

令 $t$ 表示当前时间，到期日 $T$ 固定，剩余期限为 $\tau=T-t$：

$$
\boxed{
\mathrm{Charm}
=\frac{\partial\Delta}{\partial t}
=\frac{\partial\Theta}{\partial S}
=\frac{\partial^2V}{\partial S\,\partial t}
=-\frac{\partial\Delta}{\partial\tau}
}
$$

对应的局部 Delta 漂移为

$$
d\Delta\approx\mathrm{Charm}\,dt
=\frac{\partial\Delta}{\partial\tau}\,d\tau,
\qquad d\tau=-dt.
$$

## 典型形态

- Charm 具有正负波瓣，改变时间导数口径会使整体符号反转。
- 在简单模型中，Charm 通常在看涨 Delta 约 $0.50$、看跌 Delta 约 $-0.50$ 的平值区域接近 $0$。
- 绝对值峰值常在看涨 Delta 约 $0.15$–$0.20$ 与 $0.80$–$0.85$ 的区域；看跌期权对应负 Delta 区域。
- 临近到期时，Delta 随时间的漂移通常更快，因此 $|\mathrm{Charm}|$ 更值得监控。

## 风险管理含义

即使标的价格与波动率不变，Delta 中性头寸也会随时间失去中性：

$$
\Delta_{\text{tomorrow}}
\approx
\Delta_{\text{today}}
+\mathrm{Charm}\,\Delta t.
$$

临近到期时，应把 Charm 纳入次日开盘对冲量和周末风险估计，而不是假设 Delta 静止不变。

## 关联概念

- [[Delta]]：Charm 描述 Delta 的时间漂移。
- [[Theta]]：Charm 也可写为 $\partial\Theta/\partial S$。
- [[Color]]：Color 是 Charm 对标的价格的敏感度。
- [[动态Delta对冲]]：时间推移会改变下一次再平衡所需的标的数量。

## 来源

- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/风险度量（二） Risk Measurement II#Delta / Delta|《Option Volatility and Pricing》第9章：Charm]]
