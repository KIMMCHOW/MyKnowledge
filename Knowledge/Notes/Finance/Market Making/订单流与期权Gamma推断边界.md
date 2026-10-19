---
type: note
domain: 经济
subdomain: 金融
topic: 做市
status: distilled
tags:
  - 订单流
  - 期权
  - 做市
created: 2026-10-19
---

# 订单流与期权Gamma推断边界

> [!summary] 摘要
> 订单流工具能显示挂单、成交和流动性变化，但不能仅凭图形外观推断“主力意图”。Dealer Gamma Exposure 依赖客户与做市商净头寸的模型假设，公开未平仓量不足以确定对冲方向。

## 订单流工具

DOM/Footprint/Heatmap/MBO/CVD 分别呈现挂单深度、成交流、历史流动性及更细的订单事件等信息。Absorption、sweep、iceberg 应有可复现的事件定义；图形外观本身不足以证明“主力意图”。

## Dealer Gamma 推断边界

Dealer Gamma Exposure (GEX) 涉及客户和做市商的净头寸推断，不能单看公开 OI 确定对冲方向。Call Wall / Put Wall / Zero Gamma 是特定模型下的衍生输出，不是交易所统一公布的必然支撑阻力位。MOC imbalance 不能单独证明 dealer hedge 的方向与规模。

## 研究判准

研究需区分预测、解释及可执行性，且验证扣成本后的增量收益。

## 关联笔记

- [[_索引_做市|做市研究索引]]
- [[Avellaneda–Stoikov模型]]
- [[流动性]]

## 相关问题

- 哪些订单流事件可以被严格定义和复现？
- 公开 OI 能支持哪些 GEX 结论，不能支持哪些？
- 订单流信号扣成本后是否仍有增量收益？
