---
type: concept
schema_version: 1
name: 波动率偏斜（Skew）
aliases:
  - 波动率偏斜
  - 隐含波动率偏斜
  - Volatility Skew
  - Implied Volatility Skew
  - Skew
status: completed
completion_status: completed
created_from: Option Volatility and Pricing 第24章
created_at: 2026-08-15
updated_at: 2026-08-15
tags:
  - 期权
  - 隐含波动率
  - 波动率曲面
  - 相对价值
domain: 经济
subdomain: 金融
product_domain: 衍生品
instrument: 期权
---

# 波动率偏斜（Skew）

> [!definition] 定义
> 波动率偏斜是**同一标的、同一到期日**的期权隐含波动率随行权价、远期价内外程度或 Delta 改变而形成的横截面形状。每个到期日对应一条偏斜切片；把多个期限切片组合起来，才得到波动率曲面。

> [!important] 不要与统计偏度混淆
> [[偏度|统计偏度（skewness）]]是概率分布的标准化三阶中心矩；波动率偏斜（volatility skew）是期权报价曲线。两者在风险中性分布解释上有关联，但不是同一个量，也不能用同一公式或同一单位互换。

## 坐标与期限切片

一条固定期限 $T$ 的偏斜可以写成

$$
\sigma_{\mathrm{imp}}(K,T),
$$

但直接用绝对行权价 $K$ 比较不同时间或不同标的并不稳健。常见横轴还包括远期对数价内外程度

$$
k=\ln\!\left(\frac{K}{F_T}\right),
$$

以及期权 Delta。完整波动率曲面可写为

$$
\Sigma:(k,T)\longmapsto\sigma_{\mathrm{imp}}(k,T).
$$

因此，“三个月偏斜变陡”和“六个月整体波动率上升”是两个不同的曲面变化：前者改变单一期限的横截面斜率，后者可能主要改变期限或整体水平。

## Skew、Smile 与 Smirk

- **Skew（偏斜）**：泛指跨行权价的隐含波动率不平坦，也常特指带有明显方向斜率的形状。
- **Smile（微笑）**：两侧翼部隐含波动率均高于平值附近，曲线近似 U 形；外汇和部分商品市场常见较对称的微笑。
- **Smirk（歪笑／偏斜微笑）**：一侧翼部明显抬高、另一侧较平，形成不对称的单边形状。股票与股指期权常见低执行价一侧隐含波动率较高的下行偏斜。

这些词是形状描述，不是严格互斥的模型类别。陈述偏斜方向时，应明确横轴是行权价、Delta 还是价内外程度，并说明使用的是看涨还是看跌 Delta 约定。

## 常用度量

### 25 Delta 风险逆转

外汇市场常用的 25 Delta 风险逆转报价为（看跌腿的带符号 Delta 约为 $-0.25$）：

$$
\mathrm{RR}_{25}
=\sigma_{\mathrm{imp}}(+25\Delta\ \mathrm{call})
-\sigma_{\mathrm{imp}}(-25\Delta\ \mathrm{put}).
$$

$\mathrm{RR}_{25}<0$ 表示 25 Delta 看跌翼的隐含波动率高于看涨翼。在股票市场和部分研究资料中，也常报告相反顺序的“下行偏斜”指标：

$$
\mathrm{DownsideSkew}_{25}
=\sigma_{\mathrm{imp}}(-25\Delta\ \mathrm{put})
-\sigma_{\mathrm{imp}}(+25\Delta\ \mathrm{call})
=-\mathrm{RR}_{25}.
$$

> [!warning] 先写公式，再报正负
> “25 Delta risk reversal”并没有跨市场完全统一的正负号、现货 Delta／远期 Delta、premium-adjusted 与否等约定。比较数据前必须核对定义。

### 25 Delta 蝶式与局部斜率

常见的翼部曲率度量为

$$
\mathrm{BF}_{25}
=\frac{
\sigma_{\mathrm{imp}}(+25\Delta\ \mathrm{call})
+\sigma_{\mathrm{imp}}(-25\Delta\ \mathrm{put})
}{2}
-\sigma_{\mathrm{imp}}(\mathrm{ATM}).
$$

也可在固定期限上用有限差分估计局部斜率和曲率：

$$
\mathrm{SkewSlope}
\approx
\frac{\sigma_{\mathrm{imp}}(k_2,T)-\sigma_{\mathrm{imp}}(k_1,T)}{k_2-k_1},
$$

$$
\mathrm{SkewCurvature}
\approx
\frac{\sigma_{\mathrm{imp}}(k+h,T)-2\sigma_{\mathrm{imp}}(k,T)+\sigma_{\mathrm{imp}}(k-h,T)}{h^2}.
$$

这是常用的简单蝶式度量；经纪商的市场蝶式（market strangle）报价可能采用不同反解规则。不同插值、Delta 约定和数据清洗方法也会给出不同结果，数值只有在同一报价口径下才可比较。

## 为什么会出现偏斜

在固定波动率的 [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/Black–Scholes 模型 The Black-Scholes Model|Black–Scholes 模型]]中，同一到期日的所有行权价共用一个 $\sigma$，因此理论隐含波动率切片应当是平的。现实中的偏斜说明“常数波动率、连续对数正态扩散”等假设不足以同时解释所有期权价格，但这并不自动意味着存在无风险套利。

常见机制包括：

- **保护与收益增强需求**：股票投资者集中买入价外保护性看跌、卖出较高行权价备兑看涨，可能抬高下行翼、压低上行翼。
- **现货—波动率相关性**：股票和股指下跌时波动率常上升，形成负 spot–vol correlation；部分商品市场可能呈相反关系。
- **跳跃、肥尾与随机波动率**：极端行情概率和波动率自身的不确定性无法由单一对数正态分布充分刻画。
- **供需、库存与事件风险**：财报、政策、季节性、结构化产品流量和做市商库存会改变特定执行价或期限的相对价格。
- **市场摩擦与模型口径**：买卖价差、流动性、股息／借券假设、提前行权和插值外推都会影响反解出的隐含波动率。

## 对策略估值的影响

多执行价或多期限策略必须使用每条腿自己的隐含波动率，而不能把一个 ATM 波动率复制给所有合约。

- [[垂直价差 Vertical Spread|垂直价差]]直接暴露于同一期限两个行权价之间的偏斜；偏斜变陡或变平会改变相对价值。
- [[比率价差 Ratio Spread|比率价差]]的净期权数量不相等，远端裸露腿对翼部偏斜和尾部流动性尤其敏感。
- [[日历价差 Calendar Spread|日历价差]]除了期限结构，还暴露于两个期限切片各自的偏斜及其不同动态。
- [[蝶式价差 Butterfly Spread|蝶式价差]]与 [[鹰式价差 Condor Spread|鹰式价差]]对跨行权价曲率敏感；单看整体 Vega 可能掩盖翼部风险。
- 25 Delta 看跌与看涨的相对价值常用风险逆转表达；若只想交易偏斜斜率，还需管理头寸的 Delta 与整体 Vega。

## 对 Greeks 与对冲的影响

传统 Greeks 通常假设“其他输入不变”。但当标的变化会带动偏斜移动时，曲面规则也进入实际敏感度。若 $\sigma_{\mathrm{imp}}=\sigma_{\mathrm{imp}}(S,K,T)$，则沿市场路径的总 Delta 可写成

$$
\frac{dV}{dS}
=\underbrace{\frac{\partial V}{\partial S}}_{\text{模型 Delta}}
+\underbrace{\frac{\partial V}{\partial\sigma}
\frac{\partial\sigma_{\mathrm{imp}}}{\partial S}}_{\text{Vega × 曲面移动}}
+\cdots.
$$

因此：

- 仅在固定曲面下计算的 Delta，可能高估或低估真实对冲比率；“粘性行权价”“粘性 Delta”等曲面动态假设会给出不同结果。
- [[Vega]] 只描述所选波动率输入的小幅变化；各腿 Vega 抵消不代表偏斜、曲率或期限风险为零。
- [[Vanna]] 描述标的与波动率的交叉变化，spot–vol 联动强时尤其重要。
- [[Volga（Vomma）|Volga / Vomma]] 描述波动率变化时 Vega 的漂移，但不能单独代替完整的曲面重估。
- [[Gamma]]、Theta 与 Vega 都会随标的穿越偏斜而变化；Delta 中性、Vega 中性的偏斜交易仍需动态管理。

## 风险管理清单

- 明确每个期限切片的横轴、Delta 与风险逆转符号约定。
- 分别压力测试曲面水平、斜率、曲率和期限结构，而不是只做平行波动率冲击。
- 同时测试现货跳空与偏斜跳变，尤其关注翼部报价和保证金。
- 检查插值和外推后的期权价格是否满足单调性、凸性及基本静态无套利条件。
- 用可成交买卖价而非平滑曲面中点复核策略成本、退出损益和尾部流动性。

## 关联概念

- [[隐含波动率]]：偏斜由同一期限不同执行价的隐含波动率组成。
- [[偏度]]：统计分布的不对称性；与波动率偏斜相关但不等同。
- [[对数正态分布]]：固定波动率 BSM 的标的价格分布假设。
- [[凸性|期权凸性]]：偏斜和曲面变化会改变 Gamma、Volga 等局部二阶风险。
- [[保护性策略 Protective Strategy|保护性策略]]、[[备兑策略 Covered Strategy|备兑策略]]：股票市场偏斜的重要供需来源。

## 来源

- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/波动率偏斜 Volatility Skews|《Option Volatility and Pricing》第24章：波动率偏斜]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/知识图谱/波动率偏斜与曲面|教材知识图谱：波动率偏斜与曲面]]
