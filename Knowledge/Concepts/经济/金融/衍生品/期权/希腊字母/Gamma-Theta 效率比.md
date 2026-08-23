---
type: concept
schema_version: 1
name: Gamma-Theta 效率比
aliases:
  - Gamma Theta Ratio
  - Gamma Theta Efficiency
  - Gamma Theta 比率
status: completed
completion_status: completed
created_from: Option Volatility and Pricing 第13章
created_at: 2026-08-23
updated_at: 2026-08-23
tags: [期权, Greeks, Gamma, Theta, 策略评估]
domain: 经济
subdomain: 金融
product_domain: 衍生品
instrument: 期权
concept_group: 希腊字母
---

# Gamma-Theta 效率比

> [!definition] 它想衡量什么
> Gamma-Theta 效率比用来比较：头寸为获得曲率收益或 Theta 收入，承担了多少相反方向的 Gamma/Theta 代价。它是一个**局部风险交换指标**，不是完整的风险收益率。

## 从局部损益展开出发

令 $t$ 为当前时间，且 Theta 按日历时间定义为

$$
\Theta=\frac{\partial V}{\partial t}.
$$

对一个近似 Delta 中性的头寸，小变动下可写成

$$
\Delta V
\approx
\frac{1}{2}\Gamma(\Delta S)^2
+\Theta\,\Delta t.
$$

- $\Gamma$ 表示标的价格变动带来的局部凸性损益。
- $\Theta$ 表示在其他条件近似不变时，时间流逝带来的局部损益。
- 对常见的多头凸性头寸，$\Gamma>0$、$\Theta<0$；对常见的空头凸性头寸，$\Gamma<0$、$\Theta>0$。

## 两种方向必须分开解读

### 正 Gamma、负 Theta

对正 Gamma 头寸，可定义

$$
E_{+\Gamma}
=
\frac{\Gamma}{-\Theta},
\qquad
\Gamma>0,\ \Theta<0.
$$

在单位一致、其他风险可比的前提下，$E_{+\Gamma}$ **越大**，表示每承担一单位 Theta 流失，获得的 Gamma 越多。

### 负 Gamma、正 Theta

对负 Gamma 头寸，直接使用

$$
R_{-\Gamma}
=
\left|\frac{\Gamma}{\Theta}\right|
=
\frac{-\Gamma}{\Theta},
\qquad
\Gamma<0,\ \Theta>0.
$$

此时 $R_{-\Gamma}$ 衡量的是“每单位 Theta 收入承担多少负 Gamma”，因此应当**越小越好**。若想统一为“越大越好”的效率值，应改用其倒数：

$$
E_{+\Theta}
=
\frac{\Theta}{-\Gamma}.
$$

| 头寸类型 | 回报来源 | 主要代价 | 建议指标 | 更优方向 |
| --- | --- | --- | --- | --- |
| $\Gamma>0,\Theta<0$ | 标的变动与凸性 | 时间价值流失 | $\Gamma/(-\Theta)$ | 越大越好 |
| $\Gamma<0,\Theta>0$ | 时间价值流入 | 大幅变动风险 | $(-\Gamma)/\Theta$ | 越小越好 |
| $\Gamma<0,\Theta>0$ | 时间价值流入 | 大幅变动风险 | $\Theta/(-\Gamma)$ | 越大越好 |

> [!warning] 原书表述的内在矛盾
> 原书先说 $|\Gamma/\Theta|$ 越大越有效，随后在负 Gamma、正 Theta 的例子中却正确地选择了该比值最小的头寸。这两种方向不能用同一条“越大越好”的规则；必须先确认 Gamma 和 Theta 分别是收益还是代价。

## Natenberg 的例子

原书比较了三个均为负 Gamma、正 Theta 的价差：

| 价差 | Gamma | Theta | $|\Gamma/\Theta|$ |
| --- | ---: | ---: | ---: |
| Spread 1 | $-406.0$ | $0.4235$ | $959$ |
| Spread 2 | $-165.5$ | $0.1365$ | $1{,}212$ |
| Spread 3 | $-370.0$ | $0.4000$ | $925$ |

因为这里的 Gamma 是风险、Theta 是收入，所以应当选择 $|\Gamma/\Theta|$ 最小的 Spread 3，而不是数值最大的 Spread 2。

## 更直观的补充：Theta 损益的打平变动

若忽略 Delta、Vega 和更高阶项，令上述局部损益等于 0，可得到在 $\Delta t$ 时间内覆盖 Theta 损益所需的对称标的变动幅度：

$$
|\Delta S_{\mathrm{BE}}|
\approx
\sqrt{\frac{-2\Theta\,\Delta t}{\Gamma}},
\qquad
\Gamma\Theta<0.
$$

- 对正 Gamma、负 Theta 头寸，它表示为抵消时间流失，标的大约需要移动多少。
- 对负 Gamma、正 Theta 头寸，它表示标的变动多大之后，局部 Gamma 亏损会抵消 Theta 收入。

该公式比单纯的 Gamma/Theta 比值更容易转化为实际的价格情景，但它仍然只是局部二阶近似。

## 适用前提

该比率适合快速比较下列头寸：

1. 各头寸的合约乘数、Gamma 标度、Theta 时间单位和币种完全一致。
2. 头寸的初始 Delta 相近，或已在同一口径下进行 Delta 对冲。
3. 各腿具有相同到期日，且各候选策略的理论优势、资金规模和市场情景具有可比性。
4. 仅用于当前价格和当前波动率附近的小变动比较。

## 局限与常见误用

- **它不是无量纲指标**：Gamma 和 Theta 的报价单位会直接影响比值。不同标的、不同乘数或不同 Theta 时间口径不可直接比较。
- **它不是大幅行情损益**：Gamma 和 Theta 会随标的价格、时间和波动率变化，近期到期、跳空或大幅行情应使用完整重定价。
- **它忽略 Vega 与曲面风险**：跨到期日组合、日历价差和对角价差必须另外检查 Vega、期限结构与波动率偏斜。
- **它不包含实务风险**：最大亏损、保证金、流动性、买卖价差、提前指派和交易成本都不在此比率中。
- **不要跨符号机械排名**：先判断 Gamma 和 Theta 各自是收益还是代价，再选择正确方向的效率定义。

## 实盘使用顺序

1. 统一所有候选头寸的 Greek 单位和合约乘数。
2. 检查 $\Gamma$ 与 $\Theta$ 的符号，确认哪一项是预期收益、哪一项是代价。
3. 按相同方向的指标排名，并计算 $|\Delta S_{\mathrm{BE}}|$。
4. 对标的价格、隐含波动率、时间和偏斜做联合压力测试。
5. 最后再加入保证金、流动性、成交和提前指派风险，决定头寸规模。

## 相关概念

- [[二阶/Gamma|Gamma]]
- [[一阶/Theta|Theta]]
- [[凸性|期权凸性]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/期权策略/_索引_期权策略|期权策略]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/风险考量 Risk Considerations#效率 / Efficiency|Natenberg：效率]]
