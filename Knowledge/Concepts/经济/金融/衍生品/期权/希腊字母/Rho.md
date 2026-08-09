---
type: concept
schema_version: 1
name: Rho
status: completed
completion_status: completed
created_from: Option Volatility and Pricing 第7章
created_at: 2026-08-10
updated_at: 2026-08-10
tags:
  - 期权
  - Greeks
  - 利率风险
domain: 经济
subdomain: 金融
product_domain: 衍生品
instrument: 期权
concept_group: 希腊字母
---

# Rho

## 定义

Rho（$\rho$）衡量期权理论价值对利率变化的局部敏感度。

$$
\rho=\frac{\partial V}{\partial r}
$$

实务中，Rho 通常表示利率变动一个百分点时，期权理论价值预计变化多少。使用具体数值前，应确认系统采用的是“每一个百分点”还是其他利率单位。

## 核心解释

Rho 的方向不能脱离标的工具和结算方式来判断。利率变化不仅影响贴现，也会改变融资或持有期权所产生的现金流成本；不同合约的现金流时点不同，因此 Rho 的符号和大小也可能不同。

第 7 章给出的主要规律如下：

| 标的与结算方式 | Rho 特征 | 原因或直觉 |
| --- | --- | --- |
| 标的与期权均采用期货型结算 | Rho 为 0 | 交易标的或期权时都不产生初始现金流 |
| 期货期权采用股票型结算 | 看涨、看跌期权的 Rho 均为负 | 利率上升会提高持有期权的资金成本，从而降低期权价值 |
| 股票看涨期权 | Rho 为正 | 利率上升时，相比直接买入股票，买入看涨期权的资金占用优势更明显 |
| 股票看跌期权 | Rho 为负 | 利率上升时，相比直接卖出股票，买入看跌期权的相对吸引力下降 |
| 需要实际交割货币的外汇期权 | 同时存在两种利率敏感度 | Rho 1 衡量本国利率风险；Rho 2 衡量外国利率风险，后者有时记作 Phi（$\Phi$） |

在第 7 章采用的风险度量框架下，直接持有标的合约的 Rho 记为 0；标的头寸只有 Delta 暴露，其 Gamma、Theta、Vega 和 Rho 均记为 0。

## 局部近似

若 Rho 按“利率变动一个百分点”报价，则小幅利率变化下：

$$
\Delta V\approx \rho\,\Delta r_{\mathrm{pp}}
$$

例如，某期权的 Rho 为 $0.12$，利率上升一个百分点时，在其他条件不变且局部近似有效的前提下，期权理论价值约增加 $0.12$；若 Rho 为负，则价值变化方向相反。

组合 Rho 具有可加性：先按每条期权腿的合约数量和多空方向调整其 Rho，再加总为组合的净利率暴露。

## 风险管理含义

- 对普通短期限、规模较小的期权头寸，Rho 通常不如 Delta、Gamma、Theta 和 Vega 重要。
- “通常较不重要”不等于可以永远忽略。期限较长、头寸规模很大、融资成本敏感或涉及外汇双利率的头寸仍需监控 Rho。
- Rho 是当前位置附近的局部近似。利率发生较大变化时，应重新定价，而不应只用单一 Rho 线性外推。
- 比较不同系统的 Rho 前，必须统一利率单位、币种、合约乘数和结算方式。

## 关联概念

- [[无风险利率]]：Rho 衡量定价利率输入变化对期权价值的局部影响。
- [[Delta]]：直接持有标的在本章框架下只保留 Delta 风险度量。
- [[Vega]]：Vega 与 Rho 都是对模型输入的局部一阶敏感度，但分别对应波动率与利率。
- [[期权]]：Rho 是期权的主要风险敏感度之一。

## 相关问题

- 为什么股票期权与期货期权的 Rho 符号可能不同？
- 为什么外汇期权需要同时观察本国利率和外国利率？
- 在长期限组合中，收益率曲线变化为何不能完全由单一 Rho 表示？

## 来源

- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/风险度量（一） Risk Measurement I#Rho（利率敏感度） / The Rho|《Option Volatility and Pricing》第7章：Rho（利率敏感度）]]
- [[Rho（Natenberg）|Natenberg 期权知识图谱：Rho]]
