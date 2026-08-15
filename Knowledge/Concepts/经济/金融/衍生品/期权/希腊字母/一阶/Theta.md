---
type: concept
schema_version: 1
name: Theta
status: completed
completion_status: completed
created_from: user-material-refactor
created_at: 2026-08-09
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

# Theta

> [!definition] 定义
> Theta（$\Theta$）衡量其他条件不变时，期权理论价值对时间变量的局部敏感度。

## 数学表示

本目录用 $\tau$ 表示距到期时间：

$$
\boxed{\Theta_{\tau}=\frac{\partial V}{\partial\tau}}
$$

若 $u$ 表示向前推进的日历时间，且 $\tau=T-u$，则市场通常所说的时间衰减为

$$
\boxed{
\Theta_{\text{calendar}}
=\frac{\partial V}{\partial u}
=-\frac{\partial V}{\partial\tau}
=-\Theta_{\tau}
}
$$

局部近似为

$$
dV\approx\Theta_{\tau}\,d\tau
=\Theta_{\text{calendar}}\,du.
$$

## 报价口径

若模型输出按年计的时间导数，粗略的自然日 Theta 为

$$
\Theta_{\text{day}}\approx\frac{\Theta_{\text{annual}}}{365}.
$$

有些系统使用交易日或自定义节假日权重，因此实际换算不一定是 $365$。使用数值前必须确认：时间变量、正负号、自然日或交易日口径。

## 典型形态

- 普通期权多头通常有 $\Theta_{\text{calendar}}<0$，因为日历时间推进会消耗时间价值；空头通常相反。
- Theta 的绝对值通常在平值附近最大，并在临近到期时更集中。
- 深度价内和深度价外期权的时间价值较少，Theta 的绝对值通常较低。
- 正 Theta 不是无风险收益；它通常伴随负 Gamma、跳空风险与尾部风险。

## 与高阶指标的关系

$$
\frac{\partial\Theta_{\tau}}{\partial S}
=\mathrm{Charm}_{\tau},
\qquad
\frac{\partial^2\Theta_{\tau}}{\partial S^2}
=\mathrm{Color}_{\tau},
\qquad
\frac{\partial\Theta_{\tau}}{\partial\sigma}
=\mathrm{VegaDecay}_{\tau}.
$$

## 关联概念

- [[Gamma]]：正 Gamma 与负日历 Theta 常形成风险收益权衡。
- [[Charm]]：Delta 随距到期时间的变化。
- [[Vega Decay|Vega decay]]：Vega 随距到期时间的变化。
- [[Color]]：Gamma 随距到期时间的变化。
- [[Knowledge/Concepts/经济/金融/衍生品/期权/期权策略/二腿/跨式 Straddle|跨式]]：跨式具有显著的时间衰减暴露。

## 来源

- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/风险度量（二） Risk Measurement II#Theta / Theta|《Option Volatility and Pricing》第9章：Theta]]
- [[Theta（Natenberg）|Natenberg 期权知识图谱：Theta]]
