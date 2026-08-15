---
type: concept
schema_version: 1
name: Phi
aliases:
  - Rho-f
  - Rhof
  - Rho 2
status: completed
completion_status: completed
created_from: Option Volatility and Pricing 第7章
created_at: 2026-08-15
updated_at: 2026-08-15
tags:
  - 期权
  - Greeks
  - 外汇期权
  - 利率风险
domain: 经济
subdomain: 金融
product_domain: 衍生品
instrument: 期权
concept_group: 希腊字母
---

# Rho-f / Phi

> [!definition] 定义
> Rho-f（$\rho_f$）或 Phi（$\Phi$）衡量期权理论价值对外国利率变化的局部敏感度。

## 数学表示

对于外汇期权，

$$
\boxed{
\Phi
=\rho_f
=\frac{\partial V}{\partial r_f}
}
$$

局部近似为

$$
dV\approx\Phi\,dr_f.
$$

若股票模型把连续股息率 $q$ 作为持有收益输入，则相应敏感度直接写作

$$
\frac{\partial V}{\partial q}.
$$

两者都会影响持有标的相对于持有现金的成本收益关系，但 $r_f$ 与 $q$ 不是同一个变量，本目录也不把 $\partial V/\partial q$ 称为 Phi。

## 双利率结构

实物交割外汇期权通常同时具有两种利率敏感度：

$$
dV\approx
\rho_d\,dr_d
+\rho_f\,dr_f.
$$

其中

$$
\rho_d=\frac{\partial V}{\partial r_d},
\qquad
\rho_f=\Phi=\frac{\partial V}{\partial r_f}.
$$

因此，仅观察一个总 Rho 可能掩盖本国与外国利率方向相反的暴露。

## 典型形态

- $|\Phi|$ 通常随期限增加而增大，并在深度价内期权中更显著。
- Phi 的符号取决于报价币种、看涨或看跌方向、结算方式及系统定义。
- 外汇期权应明确哪一种货币是本国货币、哪一种是外国货币，再解释 $\rho_d$ 与 $\rho_f$。

## 单位

$$
\Phi_{1\text{ percentage point}}
=0.01\frac{\partial V}{\partial r_f},
\qquad
\Phi_{1\text{ bp}}
=0.0001\frac{\partial V}{\partial r_f}.
$$

## 关联概念

- [[Rho]]：本国利率或主要定价利率敏感度。
- [[期权]]：Phi 是含外国利率输入的期权风险指标。
- [[无风险利率]]：本国与外国利率共同决定外汇远期关系。

## 来源

- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/风险度量（一） Risk Measurement I#Rho（利率敏感度） / The Rho|《Option Volatility and Pricing》第7章：Rho 1、Rho 2 与 Phi]]
