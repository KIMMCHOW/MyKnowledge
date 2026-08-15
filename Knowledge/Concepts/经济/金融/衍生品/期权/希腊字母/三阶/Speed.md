---
type: concept
schema_version: 1
name: Speed
aliases:
  - DgammaDspot
status: completed
completion_status: completed
created_from: Option Volatility and Pricing 第9章
created_at: 2026-08-15
updated_at: 2026-08-15
tags:
  - 期权
  - Greeks
  - 凸性
domain: 经济
subdomain: 金融
product_domain: 衍生品
instrument: 期权
concept_group: 希腊字母
---

# Speed

> [!definition] 定义
> Speed 衡量 Gamma 对标的价格的敏感度。它是专有风险指标名称，通常直接保留英文。

## 数学表示

$$
\boxed{
\mathrm{Speed}
=\frac{\partial\Gamma}{\partial S}
=\frac{\partial^2\Delta}{\partial S^2}
=\frac{\partial^3V}{\partial S^3}
}
$$

标的价格小幅变化时，Gamma 的漂移为

$$
d\Gamma\approx\mathrm{Speed}\,dS.
$$

与 Delta 的局部展开关系为

$$
d\Delta\approx
\Gamma\,dS
+\frac{1}{2}\mathrm{Speed}(dS)^2.
$$

期权价值中的对应三阶项为

$$
dV_{S}^{(3)}
\approx
\frac{1}{6}\mathrm{Speed}(dS)^3.
$$

## 典型形态

- Gamma 在平值附近达到峰值，因此 Speed 通常在平值附近换号：标的从低价格侧靠近平值时 Speed 多为正，越过峰值后多为负。
- $|\mathrm{Speed}|$ 的峰值常在看涨 Delta 约 $0.15$–$0.20$ 与 $0.80$–$0.85$ 的区域；看跌期权对应负 Delta 区域。
- 在平值点以及深度价内或深度价外区域，Gamma 对价格变化相对不敏感，Speed 通常接近 $0$。
- 临近到期或低波动率时，Gamma 更集中，Speed 的绝对值通常更大。

## 风险管理含义

只用当前 Gamma 预测较大价格变动后的 Delta 漂移，可能忽略 Gamma 自身的变化。加入 Speed 后：

$$
\Delta_{\text{new}}
\approx
\Delta_{\text{old}}
+\Gamma\,\Delta S
+\frac{1}{2}\mathrm{Speed}(\Delta S)^2.
$$

Speed 较大时，固定 Gamma 假设很快失效，应缩短重估区间或直接全重估。

## 关联概念

- [[Gamma]]：Speed 是 Gamma 对标的价格的敏感度。
- [[Delta]]：Speed 影响 Delta 的非线性漂移。
- [[Color]]：Gamma 对距到期时间的敏感度。
- [[Zomma]]：Gamma 对波动率的敏感度。

## 来源

- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/风险度量（二） Risk Measurement II#Gamma / Gamma|《Option Volatility and Pricing》第9章：Speed]]
