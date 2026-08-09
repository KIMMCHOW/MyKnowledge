---
type: concept
schema_version: 1
name: 动态Delta对冲
status: completed
completion_status: completed
created_from: user-material-refactor
created_at: 2026-08-09
updated_at: 2026-08-09
tags:
  - 期权
  - 对冲
  - 风险管理
domain: 经济
subdomain: 金融
product_domain: 衍生品
instrument: 期权
---

# 动态Delta对冲

## 定义
动态 Delta 对冲是根据组合 Delta 的变化，持续交易标的或线性合约，使净方向暴露维持在目标区间的风险管理方法。

## 核心解释
期权 Delta 会因标的价格、时间和波动率变化而漂移，因此一次性对冲不能永久保持中性。高 Gamma 头寸需要更频繁地调整；提高调整频率能减少局部方向误差，却会增加点差、手续费和市场冲击。离散调整、跳空和模型误差使现实复制无法完全等同于连续模型。

## 示例
- 多头期权组合 Delta 上升后，交易者卖出一部分标的恢复中性。
- 使用固定时间间隔或 Delta 阈值作为再平衡规则。

## 关联概念
- [[Delta]]：Delta 决定当前需要多少标的对冲。
- [[Gamma]]：Gamma 决定 Delta 漂移和再平衡需求。
- [[已实现波动率]]：实际价格路径影响再平衡现金流。
- [[跨式与宽跨式]]：波动率交易常对跨式或宽跨式进行动态 Delta 对冲。

## 相关问题
- 基于时间和基于 Delta 阈值的调整规则如何取舍？
- 交易成本如何改变最优对冲频率？

## 来源
- [[C33-动态Delta对冲|Natenberg 期权知识图谱：动态 Delta 对冲]]
