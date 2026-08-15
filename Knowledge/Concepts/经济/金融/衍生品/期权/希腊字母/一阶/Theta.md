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
> Theta（$\Theta$）衡量其他条件不变时，期权理论价值随当前时间 $t$ 推进的局部变化率。

## 数学表示

令 $t$ 表示当前时间，到期日 $T$ 固定，剩余期限为 $\tau=T-t$。本目录统一使用市场常用的 Theta 符号：

$$
\boxed{
\Theta
=\frac{\partial V}{\partial t}
=-\frac{\partial V}{\partial\tau}
}
$$

局部近似为

$$
dV\approx\Theta\,dt
=\frac{\partial V}{\partial\tau}\,d\tau,
\qquad d\tau=-dt.
$$

## 报价口径

若模型输出按年计的时间导数，粗略的自然日 Theta 为

$$
\Theta_{\text{day}}\approx\frac{\Theta_{\text{annual}}}{365}.
$$

有些系统使用交易日或自定义节假日权重，因此实际换算不一定是 $365$。使用数值前必须确认：时间变量、正负号、自然日或交易日口径。

## 典型形态

- 普通期权多头通常有 $\Theta<0$，因为当前时间推进会消耗时间价值；空头通常相反。
- Theta 的绝对值通常在平值附近最大，并在临近到期时更集中。
- 深度价内和深度价外期权的时间价值较少，Theta 的绝对值通常较低。
- 正 Theta 不是无风险收益；它通常伴随负 Gamma、跳空风险与尾部风险。

## 与高阶指标的关系

$$
\frac{\partial\Theta}{\partial S}
=\mathrm{Charm},
\qquad
\frac{\partial^2\Theta}{\partial S^2}
=\mathrm{Color},
\qquad
\frac{\partial\Theta}{\partial\sigma}
=\mathrm{VegaDecay}.
$$

## 关联概念

- [[Gamma]]：正 Gamma 与负 Theta 常形成风险收益权衡。
- [[Charm]]：Delta 随当前时间推进的变化。
- [[Vega Decay|Vega decay]]：Vega 随当前时间推进的变化。
- [[Color]]：Gamma 随当前时间推进的变化。
- [[Knowledge/Concepts/经济/金融/衍生品/期权/期权策略/二腿/跨式 Straddle|跨式]]：跨式具有显著的时间衰减暴露。

## 来源

- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/风险度量（二） Risk Measurement II#Theta / Theta|《Option Volatility and Pricing》第9章：Theta]]
- [[Theta（Natenberg）|Natenberg 期权知识图谱：Theta]]
