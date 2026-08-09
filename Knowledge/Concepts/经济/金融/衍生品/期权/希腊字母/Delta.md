---
type: concept
schema_version: 1
name: Delta
status: completed
completion_status: completed
created_from: user-material-refactor
created_at: 2026-08-09
updated_at: 2026-08-09
tags:
  - 期权
  - Greeks
  - 对冲
domain: 经济
subdomain: 金融
product_domain: 衍生品
instrument: 期权
concept_group: 希腊字母
---

# Delta

## 定义
Delta（$\Delta$）衡量期权价值对标的价格的局部一阶敏感度，也常被解释为局部等价标的头寸或对冲比率。

$$
\Delta=\frac{\partial V}{\partial S}
$$

## 核心解释
Delta 表示在其他条件不变、标的价格发生小幅变化时，期权价值预计变化多少。看涨期权 Delta 通常为正，看跌期权 Delta 通常为负。Delta 只是当前点附近的线性近似，会因标的价格、时间和波动率变化而改变。

## 示例
- Delta 为 $0.40$ 的看涨期权，在局部近似下，标的上涨 1 元时价值约上涨 0.40 元。
- 组合净 Delta 为 100，可用卖出约 100 单位标的进行局部方向对冲。

## 关联概念
- [[Gamma]]：Gamma 决定 Delta 的变化速度。
- [[动态Delta对冲]]：动态对冲通过交易标的控制组合净 Delta。
- [[期权]]：Delta 是期权的主要风险敏感度之一。

## 相关问题
- 现货 Delta、期货 Delta 和经乘数调整后的组合 Delta 有何区别？
- 为什么 Delta 中性不等于无风险？

## 来源
- [[C26-Delta|Natenberg 期权知识图谱：Delta]]
