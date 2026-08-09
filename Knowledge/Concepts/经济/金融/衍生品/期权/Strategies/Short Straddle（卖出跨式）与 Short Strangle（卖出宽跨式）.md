---
type: strategy-note
topic: 期权
status: active
created_at: 2026-05-25
updated_at: 2026-08-09
tags:
  - 期权
  - 卖出波动率
  - 跨式
  - 宽跨式
---

# Short Straddle（卖出跨式）与 Short Strangle（卖出宽跨式）

> [!summary] 摘要
> 两者都是收取权利金的短波动率结构，通常具有负 [[Gamma]]、正 [[Theta]] 和负 [[Vega]]。收益上限有限，双侧尾部损失可能很大。

## 共同风险结构

- 负 Gamma：标的大幅运动时，组合 Delta 会朝不利方向快速变化。
- 正 Theta：其他条件不变时，时间流逝通常有利。
- 负 Vega：[[隐含波动率]]上升通常不利。
- 尾部风险：收益分布可能呈负偏和肥尾，不能把平均 [[隐含波动率|IV]]–[[已实现波动率|RV]] 差异视为确定收益。

## Short Straddle（卖出跨式）

- 卖出同一到期日、同一平值行权价的 Call 与 Put。
- 到期时标的恰好位于行权价附近，组合保留的权利金最多。
- 平值且临近到期时 Gamma 可能高度集中，[[Delta]] 会快速漂移。

## Short Strangle（卖出宽跨式）

- 卖出同一到期日的一份价外 Call 和一份价外 Put，行权价不同。
- 最大盈利区间比跨式更宽，收到的权利金通常更少。
- 初始局部 Gamma 通常低于相近跨式，但突破任一侧后仍可能形成显著尾部损失。

## 风险管理

- 用[[动态Delta对冲]]控制局部方向暴露，但对冲无法消除跳空、交易成本和波动率曲面风险。
- 控制仓位和保证金缓冲，不以“高胜率”代替最大损失分析。
- 可用更远端期权构造有限风险结构，例如[[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/知识图谱/蝶式与鹰式|铁鹰式]]，但保护成本会降低权利金收入。

## 关联概念

- [[跨式与宽跨式]]：策略结构的概念卡片。
- [[Knowledge/Concepts/经济/金融/衍生品/期权/Notes/Volatility Trading|波动率交易]]：策略所处的分析框架。
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/知识图谱/偏度峰度与隐含分布|偏度、峰度与肥尾]]：解释卖方收益分布的非正态特征。

## 来源

- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/波动率价差策略 Volatility Spreads|第11章：波动率价差策略]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/风险考量 Risk Considerations|第13章：风险考量]]
