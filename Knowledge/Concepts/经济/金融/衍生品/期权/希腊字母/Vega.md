---
type: concept
schema_version: 1
name: Vega
status: completed
completion_status: completed
created_from: user-material-refactor
created_at: 2026-08-09
updated_at: 2026-08-09
tags:
  - 期权
  - Greeks
  - 波动率
domain: 经济
subdomain: 金融
product_domain: 衍生品
instrument: 期权
concept_group: 希腊字母
---

# Vega

## 定义
Vega 衡量期权价值对定价模型中波动率输入的局部敏感度。

$$
\mathrm{Vega}=\frac{\partial V}{\partial\sigma}
$$

## 核心解释
多头普通期权通常具有正 Vega，隐含波动率上升会提高其模型价值；空头则通常为负。Vega 必须连同单位一起解释：有的系统表示波动率变化 1 个百分点的价值变化，有的表示波动率变化 100% 的变化。单一 Vega 也不能完整描述偏斜和期限结构变化。

## 示例
- Vega 为 0.12 且按一个波动率点报价时，隐含波动率上升 1 个百分点，期权价值局部约增加 0.12。
- 日历价差可能总 Vega 接近中性，但仍暴露于不同期限隐含波动率的相对变化。

## 关联概念
- [[隐含波动率]]：隐含波动率变化通过 Vega 影响期权估值。
- [[波动率]]：Vega 衡量的是模型波动率输入风险。
- [[跨式与宽跨式]]：多头跨式和宽跨式通常具有正 Vega。
- [[期权]]：Vega 是期权的主要风险敏感度之一。

## 相关问题
- Vega 为什么会随期限和价内外程度变化？
- 为什么 Vega 中性不等于波动率曲面中性？

## 来源
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/知识图谱/C29-Vega|Natenberg 期权知识图谱：Vega]]
