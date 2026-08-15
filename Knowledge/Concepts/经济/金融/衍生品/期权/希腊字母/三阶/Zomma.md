---
type: concept
schema_version: 1
name: Zomma
aliases:
  - DgammaDvol
status: completed
completion_status: completed
created_from: Option Volatility and Pricing 第9章
created_at: 2026-08-15
updated_at: 2026-08-15
tags:
  - 期权
  - Greeks
  - 波动率
  - 凸性
domain: 经济
subdomain: 金融
product_domain: 衍生品
instrument: 期权
concept_group: 希腊字母
---

# Zomma

> [!definition] 定义
> Zomma 衡量 Gamma 对波动率的敏感度。它是专有风险指标名称，不应译成普通的“波动率”。

## 数学表示

$$
\boxed{
\mathrm{Zomma}
=\frac{\partial\Gamma}{\partial\sigma}
=\frac{\partial\mathrm{Vanna}}{\partial S}
=\frac{\partial^3V}{\partial S^2\,\partial\sigma}
}
$$

波动率小幅变化时，Gamma 的漂移为

$$
d\Gamma\approx\mathrm{Zomma}\,d\sigma.
$$

期权价值中的对应三阶项为

$$
dV_{S,S,\sigma}^{(3)}
\approx
\frac{1}{2}\mathrm{Zomma}(dS)^2d\sigma.
$$

## 典型形态

- 平值期权的 Zomma 通常为负：波动率上升会使集中的 Gamma 降低，波动率下降会使其 Gamma 上升。
- 看涨 Delta 接近 $0.05$ 或 $0.95$、看跌 Delta 接近 $-0.05$ 或 $-0.95$ 的区域可出现较大的正 Zomma 波瓣。
- 看涨 Delta 接近 $0.15$ 或 $0.85$、看跌 Delta 接近 $-0.15$ 或 $-0.85$ 时，Zomma 常接近 $0$。
- $|\mathrm{Zomma}|$ 通常在平值、临近到期且低波动率时最显著。

## 风险管理含义

当前 Gamma 中性或 Gamma 风险可控，不代表波动率变化后仍然如此：

$$
\Gamma_{\text{new}}
\approx
\Gamma_{\text{old}}
+\mathrm{Zomma}\,\Delta\sigma.
$$

对于临近到期的平值组合，隐含波动率下降可能快速放大 Gamma，进而增加 Delta 漂移和动态对冲压力。

## 关联概念

- [[Gamma]]：Zomma 是 Gamma 对波动率的敏感度。
- [[Vanna]]：Zomma 也可写为 Vanna 对标的价格的敏感度。
- [[Speed]]：Gamma 对标的价格的敏感度。
- [[Color]]：Gamma 对距到期时间的敏感度。
- [[隐含波动率]]：波动率变化会通过 Zomma 改变 Gamma 风险。

## 来源

- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/风险度量（二） Risk Measurement II#Gamma / Gamma|《Option Volatility and Pricing》第9章：Zomma]]
