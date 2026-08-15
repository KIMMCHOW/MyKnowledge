---
type: concept
schema_version: 1
name: Lambda（期权杠杆率）
aliases:
  - Lambda（弹性）
  - 期权弹性
  - 期权杠杆率
  - 杠杆率
  - Omega
status: completed
completion_status: completed
created_from: Option Volatility and Pricing 第9章
created_at: 2026-08-15
updated_at: 2026-08-15
tags:
  - 期权
  - Greeks
  - 杠杆
domain: 经济
subdomain: 金融
product_domain: 衍生品
instrument: 期权
concept_group: 希腊字母
---

# Lambda（期权杠杆率）

> [!definition] 定义
> Lambda（$\Lambda$，也称 Omega、option leverage 或 elasticity）是期权的局部杠杆率：它衡量标的价格每变动 $1\%$ 时，期权理论价值近似变动多少百分比。数学上，它就是期权价值对标的价格的弹性。

## 数学表示

$$
\boxed{
\Lambda
=\frac{\partial V/V}{\partial S/S}
=\frac{\partial\ln V}{\partial\ln S}
=\frac{S}{V}\frac{\partial V}{\partial S}
=\Delta\frac{S}{V}
}
$$

因此，

$$
\frac{dV}{V}\approx\Lambda\frac{dS}{S}.
$$

Lambda 是无量纲的期权价格弹性，因此称为“期权杠杆率”更贴近交易语境。它不是融资杠杆，也不是每一点价格变化对应的金额风险；金额方向风险仍由 Delta 表示。

## 示例

若

$$
V=4.00,
\qquad
\Delta=0.20,
\qquad
S=100,
$$

则

$$
\Lambda
=0.20\times\frac{100}{4.00}
=5.
$$

局部而言，标的上涨 $1\%$ 时，期权理论价值约上涨 $5\%$。

## 典型形态

- 因 $V$ 出现在分母中，低价价外期权的 $|\Lambda|$ 可能很大。
- $|\Lambda|$ 往往在价外、接近到期且低波动率时较高。
- 看涨期权的 Lambda 通常为正；看跌期权因 Delta 通常为负，其 Lambda 通常为负。讨论“杠杆大小”时通常比较 $|\Lambda|$。
- 当 $V\to0$ 时，$|\Lambda|$ 可能迅速放大，此时买卖价差、最小报价单位和流动性会使模型弹性失去实务意义。

## 风险管理含义

$$
\text{高 }|\Lambda|
\not\Rightarrow
\text{高预期收益或可执行的高杠杆}
$$

Lambda 应与最大损失、权利金、保证金、买卖价差、成交深度和退出能力一起评估。

## 关联概念

- [[Delta]]：Lambda 由 Delta、标的价格与期权价值共同决定。
- [[期权]]：Lambda 描述期权相对标的的百分比方向杠杆。
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/知识图谱/Lambda|Natenberg 期权知识图谱：Lambda]]

## 来源

- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/风险度量（二） Risk Measurement II#Lambda（Λ，杠杆率） / Lambda (Λ)|《Option Volatility and Pricing》第9章：Lambda]]
