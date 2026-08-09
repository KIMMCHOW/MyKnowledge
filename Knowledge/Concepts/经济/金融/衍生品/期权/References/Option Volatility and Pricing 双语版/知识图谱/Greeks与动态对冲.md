---
title: "Greeks与动态对冲 / Greeks and Dynamic Hedging"
graph_layer: 5
tags: [期权知识图谱, 层级]
generated_by: "tools/build_option_knowledge_graph.py"
---

# 第5层：Greeks与动态对冲 / Greeks and Dynamic Hedging

> [!question] 价值变化如何传导到头寸？
> 用局部敏感度汇总风险，并通过再平衡管理方向暴露。

## 本层核心概念

- [[Delta（Natenberg）|Delta]] — Delta 衡量期权价值对标的价格的局部一阶敏感度，也常作为等价标的头寸和动态对冲比率。
- [[Gamma（Natenberg）|Gamma]] — Gamma 衡量 Delta 对标的价格的变化率，是头寸凸性以及再平衡需求的核心指标。
- [[Theta（Natenberg）|Theta]] — Theta 衡量其他条件不变时，日历时间流逝对期权价值的局部影响，通常与 Gamma 暴露形成权衡。
- [[Vega（Natenberg）|Vega]] — Vega 衡量模型波动率变化对期权价值的局部敏感度，是隐含波动率头寸的主要尺度。
- [[Rho|Rho]] — Rho 衡量利率变化对期权价值的局部敏感度，在长期限、外汇和融资敏感头寸中更重要。
- [[Lambda|Lambda]] — Lambda 是期权价值对标的百分比变化的弹性，反映单位资本上的方向杠杆。
- [[组合Greeks与头寸分析|组合Greeks与头寸分析]] — 把各合约按数量、乘数和币种汇总为组合风险，并结合情景全重估形成做市账簿的风险视图。
- [[动态Delta对冲（Natenberg）|动态Delta对冲]] — 根据模型 Delta 买卖标的并持续再平衡，使头寸在局部保持方向中性，并把价格路径转化为调整现金流。

## 本层关系图

```mermaid
flowchart LR
    Delta["Delta"]
    Gamma["Gamma"]
    Theta["Theta"]
    Vega["Vega"]
    Rho["Rho"]
    Lambda["Lambda"]
    PortfolioGreeksandPositionAnalysis["组合Greeks与头寸分析"]
    DynamicDeltaHedging["动态Delta对冲"]
    Delta -->|"决定对冲数量"| DynamicDeltaHedging
    Gamma -->|"决定Delta漂移速度"| Delta
    Gamma -->|"提高再平衡需求"| DynamicDeltaHedging
    Gamma -->|"通常伴随反向暴露"| Theta
    Delta -->|"与价格共同定义"| Lambda
    Lambda -->|"汇总为百分比杠杆"| PortfolioGreeksandPositionAnalysis
    Delta -->|"汇总为组合暴露"| PortfolioGreeksandPositionAnalysis
    Gamma -->|"汇总为组合暴露"| PortfolioGreeksandPositionAnalysis
    Theta -->|"汇总为组合暴露"| PortfolioGreeksandPositionAnalysis
    Vega -->|"汇总为组合暴露"| PortfolioGreeksandPositionAnalysis
    Rho -->|"汇总为组合暴露"| PortfolioGreeksandPositionAnalysis
    DynamicDeltaHedging -->|"局部中和"| Delta
```

## 跨层接口

- [[历史与已实现波动率|历史与已实现波动率]] **—相对入场隐波决定波动捕获→** [[动态Delta对冲（Natenberg）|动态Delta对冲]]：实现路径与入场定价的差异通过再平衡损益体现。
- [[隐含波动率（Natenberg）|隐含波动率]] **—设定波动交易盈亏平衡基准→** [[动态Delta对冲（Natenberg）|动态Delta对冲]]：入场隐波决定时间价值与预期调整收入的平衡。
- [[Black-Scholes模型|Black-Scholes模型]] **—导出局部敏感度→** [[Delta（Natenberg）|Delta]]：模型对标的价格求一阶敏感度。
- [[Black-Scholes模型|Black-Scholes模型]] **—导出局部敏感度→** [[Gamma（Natenberg）|Gamma]]：模型对标的价格求二阶敏感度。
- [[Black-Scholes模型|Black-Scholes模型]] **—导出局部敏感度→** [[Theta（Natenberg）|Theta]]：模型衡量时间流逝的局部影响。
- [[Black-Scholes模型|Black-Scholes模型]] **—导出局部敏感度→** [[Vega（Natenberg）|Vega]]：模型衡量波动率输入变化的局部影响。
- [[Black-Scholes模型|Black-Scholes模型]] **—导出局部敏感度→** [[Rho|Rho]]：模型衡量利率输入变化的局部影响。
- [[二叉树与风险中性估值|二叉树与风险中性估值]] **—以节点差分估计→** [[Delta（Natenberg）|Delta]]：树上价值变化可估计 Delta。
- [[二叉树与风险中性估值|二叉树与风险中性估值]] **—以节点差分估计→** [[Gamma（Natenberg）|Gamma]]：相邻 Delta 变化可估计 Gamma。
- [[模型假设与模型风险|模型假设与模型风险]] **—造成敏感度误差→** [[组合Greeks与头寸分析|组合Greeks与头寸分析]]：模型误设会让组合 Greeks 低估或错配真实风险。
- [[到期时间与行权方式|到期时间与行权方式]] **—通过时间流逝实现→** [[Theta（Natenberg）|Theta]]：剩余期限减少会改变期权价值。
- [[隐含波动率（Natenberg）|隐含波动率]] **—变化时经由Vega传导→** [[Vega（Natenberg）|Vega]]：隐波平移首先表现为 Vega 损益。
- [[利率与融资成本|利率与融资成本]] **—变化时经由Rho传导→** [[Rho|Rho]]：利率变化影响贴现和远期。
- [[Lambda|Lambda]] **—约束资本与头寸规模→** [[策略选择与调整|策略选择与调整]]：高弹性头寸需与最大损失、保证金和可退出性一起决定规模。
- [[组合Greeks与头寸分析|组合Greeks与头寸分析]] **—约束→** [[策略选择与调整|策略选择与调整]]：组合风险限额决定可选策略、规模和调整。
- [[动态Delta对冲（Natenberg）|动态Delta对冲]] **—通过换手产生→** [[流动性执行与结算风险|流动性执行与结算风险]]：每次再平衡消耗价差、费用和市场冲击。
- [[流动性执行与结算风险|流动性执行与结算风险]] **—造成离散对冲误差→** [[动态Delta对冲（Natenberg）|动态Delta对冲]]：跳空、滑点和市场关闭使理论对冲无法连续执行。
- [[垂直价差与牛熊价差|垂直价差与牛熊价差]] **—主要形成方向暴露→** [[Delta（Natenberg）|Delta]]：垂直价差用有界损益表达看多或看空观点。
- [[跨式与宽跨式（Natenberg）|跨式与宽跨式]] **—多头通常形成正凸性→** [[Gamma（Natenberg）|Gamma]]：多头跨式和宽跨式受益于大幅运动。
- [[跨式与宽跨式（Natenberg）|跨式与宽跨式]] **—多头通常形成正波动率暴露→** [[Vega（Natenberg）|Vega]]：隐波上升通常提高多头结构价值。
- [[跨式与宽跨式（Natenberg）|跨式与宽跨式]] **—多头通常承担时间衰减→** [[Theta（Natenberg）|Theta]]：若运动不足，权利金随时间损耗。
- [[蝶式与鹰式|蝶式与鹰式]] **—表达局部曲率→** [[Gamma（Natenberg）|Gamma]]：多执行价结构把 Gamma 集中在特定区间。
- [[比率价差与圣诞树|比率价差与圣诞树]] **—可能形成非对称尾部凸性→** [[Gamma（Natenberg）|Gamma]]：不等数量使一侧远端风险突出。
- [[保护性备兑与领式|保护性备兑与领式]] **—变换标的方向风险→** [[Delta（Natenberg）|Delta]]：保护、备兑和领式改变组合 Delta。
- [[垂直价差与牛熊价差|垂直价差与牛熊价差]] **—汇总成风险画像→** [[组合Greeks与头寸分析|组合Greeks与头寸分析]]：策略必须还原为组合 Greeks 与情景损益。
- [[跨式与宽跨式（Natenberg）|跨式与宽跨式]] **—汇总成风险画像→** [[组合Greeks与头寸分析|组合Greeks与头寸分析]]：波动率策略不能只用名称判断风险。
- [[蝶式与鹰式|蝶式与鹰式]] **—汇总成风险画像→** [[组合Greeks与头寸分析|组合Greeks与头寸分析]]：曲率结构的风险随标的和期限变化。
- [[日历与对角价差|日历与对角价差]] **—汇总成风险画像→** [[组合Greeks与头寸分析|组合Greeks与头寸分析]]：跨期风险需要期限分桶。
- [[比率价差与圣诞树|比率价差与圣诞树]] **—汇总成风险画像→** [[组合Greeks与头寸分析|组合Greeks与头寸分析]]：尾部裸露必须进入全重估情景。
- [[保护性备兑与领式|保护性备兑与领式]] **—汇总成风险画像→** [[组合Greeks与头寸分析|组合Greeks与头寸分析]]：保护头寸仍保留残余方向与波动率风险。
- [[合成与箱式套利|合成与箱式套利]] **—汇总成风险画像→** [[组合Greeks与头寸分析|组合Greeks与头寸分析]]：套利结构也占用融资、保证金和流动性限额。
- [[波动率合约方差掉期与VIX|波动率合约方差掉期与VIX]] **—提供直接波动率暴露→** [[Vega（Natenberg）|Vega]]：波动率和方差产品减少逐期权管理但仍有波动率敏感度。

## 风险经理阅读顺序

1. 统一单位后汇总 Greeks。
2. 用全重估情景检查局部近似和动态对冲失效。
