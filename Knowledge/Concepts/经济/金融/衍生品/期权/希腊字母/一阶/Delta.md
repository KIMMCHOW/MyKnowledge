---
type: concept
schema_version: 1
name: Delta
status: completed
completion_status: completed
created_from: user-material-refactor
created_at: 2026-08-09
updated_at: 2026-08-15
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

> [!definition] 定义
> Delta（$\Delta$）衡量期权理论价值对标的价格的局部敏感度，也常被解释为局部等价标的头寸或对冲比率。

## 数学表示

$$
\boxed{\Delta=\frac{\partial V}{\partial S}}
$$

在标的价格只发生小幅变化时，

$$
dV\approx\Delta\,dS
$$

或写成离散近似：

$$
V(S+\Delta S)-V(S)\approx\Delta\,\Delta S.
$$

## 报价口径

Delta 常见两种显示方式：小数格式与点数格式。

$$
\Delta_{\text{points}}=100\,\Delta_{\text{decimal}}
$$

普通欧式期权通常满足

$$
0\leq\Delta_{\text{call}}\leq1,
\qquad
-1\leq\Delta_{\text{put}}\leq0.
$$

因此，交易界面中的看涨期权 Delta 为 $50$，通常等价于小数格式的 $0.50$。

## 头寸与对冲

若持有 $n$ 张期权，每张合约乘数为 $M$，则组合 Delta 为

$$
\Delta_{\text{position}}=nM\Delta.
$$

用标的建立局部 Delta 中性头寸时，所需标的数量近似为

$$
N_S\approx-\Delta_{\text{position}}.
$$

Delta 中性只消除了当前位置附近的一阶方向暴露；市场变化后，Delta 会继续漂移：

$$
d\Delta\approx
\Gamma\,dS
+\mathrm{Vanna}\,d\sigma
+\mathrm{Charm}\,dt.
$$

## 典型形态

- 看涨期权 Delta 通常为正，看跌期权 Delta 通常为负。
- 深度价外期权的 Delta 绝对值接近 $0$；深度价内看涨期权接近 $1$，深度价内看跌期权接近 $-1$。
- 平值看涨期权常接近 $0.50$，平值看跌期权常接近 $-0.50$，但精确值受期限、利率、股息和波动率影响。

## 关联概念

- [[Gamma]]：Delta 对标的价格的敏感度。
- [[Vanna]]：Delta 对波动率的敏感度。
- [[Charm]]：Delta 随当前时间推进的变化率。
- [[Lambda（期权杠杆率）|Lambda]]：Delta 的百分比标准化形式，即期权的局部价格杠杆。
- [[动态Delta对冲]]：通过交易标的持续控制组合净 Delta。

## 来源

- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/风险度量（二） Risk Measurement II#Delta / Delta|《Option Volatility and Pricing》第9章：Delta]]
- [[Delta（Natenberg）|Natenberg 期权知识图谱：Delta]]
