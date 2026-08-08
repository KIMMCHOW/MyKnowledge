---
type: concept
schema_version: 1
name: Gamma
status: completed
completion_status: completed
created_from: user-material-refactor
created_at: 2026-08-09
updated_at: 2026-08-09
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

## 定义
Gamma（$\Gamma$）衡量期权 Delta 对标的价格的变化率，也就是期权价值对标的价格的二阶敏感度。

$$
\Gamma=\frac{\partial\Delta}{\partial S}=\frac{\partial^2V}{\partial S^2}
$$

## 核心解释
Gamma 描述头寸的局部凸性以及 Delta 漂移的速度。正 Gamma 头寸会在标的大幅运动时受益，但通常承担负 Theta；负 Gamma 头寸通常赚取时间价值，却暴露于跳空和快速再对冲风险。临近到期且接近平值时，Gamma 往往最集中。

## 示例
- 多头跨式通常具有正 Gamma，标的大幅上涨或下跌都有利。
- 卖出平值短期期权通常具有较高负 Gamma，Delta 会随标的价格迅速变化。

## 关联概念
- [[Delta]]：Gamma 决定 Delta 随标的价格变化的速度。
- [[Theta]]：正 Gamma 通常伴随负 Theta，反之亦然。
- [[动态Delta对冲]]：Gamma 越高，维持 Delta 中性所需的调整越频繁。
- [[跨式与宽跨式]]：跨式和宽跨式是典型的 Gamma 暴露结构。
- [[期权]]：Gamma 是期权的主要风险敏感度之一。

## 相关问题
- 为什么临近到期的平值期权 Gamma 会集中？
- 离散对冲如何把 Gamma 暴露转化为实际盈亏？

## 来源
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/知识图谱/C27-Gamma|Natenberg 期权知识图谱：Gamma]]
