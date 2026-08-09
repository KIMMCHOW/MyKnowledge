---
type: study-note
topic: 期权
status: active
created_at: 2026-05-25
updated_at: 2026-08-09
tags:
  - 期权
  - 波动率交易
---

# 波动率交易（Volatility Trading）

> [!summary] 摘要
> 波动率交易以价格运动幅度和隐含波动率变化为主要风险来源。交易者常通过[[动态Delta对冲]]降低方向暴露，再管理 [[Gamma]]、[[Theta]]、[[Vega]]、交易成本与尾部风险。

## 核心区分

- [[隐含波动率]]（IV）是由期权市场价格反解的模型输入。
- [[已实现波动率]]（RV）来自实际价格路径。
- IV 高于 RV 的历史现象不是无风险收益保证；差异可能补偿跳空、肥尾、流动性、保证金和卖方尾部风险。
- 在风险中性测度 $Q$ 下进行定价，不代表真实世界测度 $P$ 下不存在风险溢价。

## Delta 中性后的主要暴露

- [[Gamma]]：标的价格的二阶敏感度，决定 Delta 漂移和再平衡需求。
- [[Theta]]：时间流逝带来的局部价值变化。
- [[Vega]]：隐含波动率变化带来的局部价值变化。
- 曲面风险：不同执行价与期限的隐含波动率不会总是平行移动。

> [!warning] 中性不等于无风险
> Delta 中性只是控制当前点附近的一阶方向风险。跳空、Gamma、Vega、期限结构、交易成本和模型误差仍然存在。

## 常见策略表达

- [[跨式与宽跨式]]：可表达对实际运动与隐含波动率的观点。
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/知识图谱/C36-蝶式与鹰式|蝶式与鹰式]]：表达波动率曲面的局部曲率。
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/知识图谱/C37-日历与对角价差|日历与对角价差]]：表达期限结构和远期波动率观点。
- [[Knowledge/Concepts/经济/金融/衍生品/期权/Strategies/Short Straddle（卖出跨式）与 Short Strangle（卖出宽跨式）|卖出跨式与卖出宽跨式]]：典型的做空波动率结构。

## 风险特征

许多卖方策略可能长期获得波动率风险溢价，但收益分布往往呈负偏、肥尾和高峰度。关键不是把平均 IV–RV 差异直接视为利润，而是识别系统性二阶风险，并控制仓位、保证金、尾部保护和退出条件。

## 来源

- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing - 教材结构提取报告|Option Volatility and Pricing 教材结构提取报告]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/知识图谱/00-期权知识图谱|期权知识图谱]]
