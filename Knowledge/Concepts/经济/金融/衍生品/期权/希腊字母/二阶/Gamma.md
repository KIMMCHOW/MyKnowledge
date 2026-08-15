---
type: concept
schema_version: 1
name: Gamma
status: completed
completion_status: completed
created_from: user-material-refactor
created_at: 2026-08-09
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

# Gamma

> [!definition] 定义
> Gamma（$\Gamma$）衡量 Delta 对标的价格的敏感度，也就是期权理论价值对标的价格的局部曲率。

## 数学表示

$$
\boxed{
\Gamma
=\frac{\partial\Delta}{\partial S}
=\frac{\partial^2V}{\partial S^2}
}
$$

标的价格小幅变化时，Delta 的变化近似为

$$
d\Delta\approx\Gamma\,dS.
$$

加入 Gamma 后，期权价值的二阶近似为

$$
dV\approx
\Delta\,dS
+\frac{1}{2}\Gamma(dS)^2.
$$

## 头寸 Gamma

若持有 $n$ 张期权，每张合约乘数为 $M$，则

$$
\Gamma_{\text{position}}=nM\Gamma.
$$

当标的变动 $\Delta S$ 时，组合 Delta 的近似漂移为

$$
\Delta_{\text{position,new}}
-\Delta_{\text{position,old}}
\approx\Gamma_{\text{position}}\Delta S.
$$

## 典型形态

- 普通看涨与看跌期权多头的 Gamma 通常为正，空头通常为负。
- $|\Gamma|$ 通常在平值、临近到期且低波动率时最集中。
- 在相同价内外程度下，平值期权的 Gamma 通常与行权价近似成反比；同样 $1$ 点价格变化在较低价格水平上代表更大的百分比变化。
- 正 Gamma 头寸受益于凸性，但通常承担负日历 Theta；负 Gamma 头寸则暴露于跳空与频繁再对冲风险。

## Gamma 如何漂移

$$
d\Gamma\approx
\mathrm{Speed}\,dS
+\mathrm{Color}_{\tau}\,d\tau
+\mathrm{Zomma}\,d\sigma.
$$

其中

$$
\mathrm{Speed}=\frac{\partial\Gamma}{\partial S},
\qquad
\mathrm{Color}_{\tau}=\frac{\partial\Gamma}{\partial\tau},
\qquad
\mathrm{Zomma}=\frac{\partial\Gamma}{\partial\sigma}.
$$

## 关联概念

- [[Delta]]：Gamma 决定 Delta 随标的价格变化的速度。
- [[Theta]]：Gamma 与日历 Theta 常形成凸性与持有成本的权衡。
- [[Speed]]：Gamma 对标的价格的敏感度。
- [[Color]]：Gamma 对距到期时间的敏感度。
- [[Zomma]]：Gamma 对波动率的敏感度。
- [[动态Delta对冲]]：Gamma 越高，维持 Delta 中性所需的调整通常越频繁。

## 来源

- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/风险度量（二） Risk Measurement II#Gamma / Gamma|《Option Volatility and Pricing》第9章：Gamma]]
- [[Gamma（Natenberg）|Natenberg 期权知识图谱：Gamma]]
