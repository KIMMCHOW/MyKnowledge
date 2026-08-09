---
type: concept
schema_version: 1
name: Theta
status: completed
completion_status: completed
created_from: user-material-refactor
created_at: 2026-08-09
updated_at: 2026-08-09
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

## 定义
Theta（$\Theta$）衡量其他条件不变时，日历时间流逝对期权价值的局部影响。

$$
\Theta=\frac{\partial V}{\partial t}
$$

## 核心解释
多头期权通常具有负 Theta，因为在其他条件不变时，剩余时间减少会消耗时间价值；空头期权通常相反。但正 Theta 不是无风险收益，往往伴随负 Gamma、跳空和尾部风险。实务中必须确认 Theta 按自然日还是交易日表达，以及软件采用的符号约定。

## 示例
- 临近到期的平值期权可能同时具有快速时间衰减和较高 Gamma。
- 卖出跨式每天可能获得正 Theta，但标的大幅运动可能产生更大的损失。

## 关联概念
- [[Gamma]]：Gamma 与 Theta 通常形成风险收益权衡。
- [[跨式与宽跨式]]：跨式和宽跨式具有明确的时间衰减暴露。
- [[期权]]：Theta 描述期权价值随时间的局部变化。

## 相关问题
- 周末和节假日应如何理解 Theta？
- 为什么临近到期时不同价内外程度的 Theta 表现不同？

## 来源
- [[Theta（Natenberg）|Natenberg 期权知识图谱：Theta]]
