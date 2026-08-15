---
type: option-strategy
schema_version: 1
name: 看跌期权 Put
aliases:
  - Put
  - Long Put
  - Short Put
  - 买入看跌期权
  - 卖出看跌期权
leg_count: 1
option_leg_count: 1
underlying_leg_count: 0
strategy_family: 单腿期权
status: completed
created_at: 2026-08-15
updated_at: 2026-08-15
tags: [期权, 期权策略, 一腿策略, 看跌期权]
domain: 经济
subdomain: 金融
---

# 看跌期权 / Put

## 定义

看跌期权赋予买方在到期日或到期日前按行权价 $K$ 卖出标的的权利；卖方收取权利金并承担被行权或指派后按 $K$ 买入标的的义务。本页的一腿是一个看跌期权合约系列；多头与空头是同一合约的相反头寸，不另计为两项策略。

## 标准腿结构

设建仓时每股看跌期权权利金为 $p>0$，到期标的价格为 $S_T\ge0$：

| 变体 | 数量 | 操作 | 合约 |
| --- | ---: | --- | --- |
| 多头看跌 | 1 | 买入 | Put，行权价 $K$、到期日 $T$ |
| 空头看跌 | 1 | 卖出 | Put，行权价 $K$、到期日 $T$ |

下列公式均按每股计算，未计手续费、滑点、利息、股息和税费；实际金额还需乘以合约乘数。

## 多头看跌到期损益

$$
\Pi_T^{\mathrm{long}}
=\max(K-S_T,0)-p
=
\begin{cases}
K-S_T-p, & 0\le S_T<K,\\
-p, & S_T\ge K.
\end{cases}
$$

- 最大亏损：$p$，发生在 $S_T\ge K$。
- 到期最高损益：$K-p$，在 $S_T=0$ 时达到；常见的 $0<p<K$ 情况下，这也是最大盈利。
- 到期盈亏平衡点：$S_T=K-p$，仅当 $K-p\ge0$ 时在可行价格域内存在。若 $p\ge K$，多头在忽略融资等因素的这组到期现金流下没有正盈利区间。

多头看跌通常为负 [[Delta]]、正 [[Gamma]]、负日历 [[Theta]]、正 [[Vega]]、负 [[Rho]]。标的接近行权价和临近到期时，Gamma 与 Delta 可能快速变化；看跌偏斜也会使其 Vega 风险不能用单一平行波动率变化概括。

## 空头看跌到期损益

$$
\Pi_T^{\mathrm{short}}
=p-\max(K-S_T,0)
=
\begin{cases}
S_T-K+p, & 0\le S_T<K,\\
p, & S_T\ge K.
\end{cases}
$$

- 最大盈利：$p$，发生在 $S_T\ge K$。
- 到期最低损益：$p-K$，在 $S_T=0$ 时发生；常见的 $0<p<K$ 情况下，最大亏损金额为 $K-p$。
- 到期盈亏平衡点：$S_T=K-p$，仅当 $K-p\ge0$ 时存在。

空头看跌的局部 Greeks 通常与多头相反：正 Delta、负 Gamma、正日历 Theta、负 Vega、正 Rho。股票价格下界使其单份到期损失在数学上有限，但相对于收到的权利金仍可能极大，并伴随跳空、波动率飙升和保证金追加风险。

## 行权、指派与裸卖风险

- 美式看跌期权可提前行权。深度价内、剩余时间价值很少且提前取得行权资金有利时，多头可能选择提前行权；卖出期权是否更经济应结合利率、股息和成交价判断。
- 裸卖 Put 可能被提前指派并按 $K$ 买入标的。账户需准备合约乘数对应的资金或融资能力；标的暴跌、停牌或归零时，静态公式之外还会叠加流动性、融资和执行风险。
- 现金担保只能解决部分履约资金问题，不会改变 $K-p$ 的下跌经济风险；保证金账户还可能在最不利时被强制减仓。
- 到期价格接近 $K$ 时存在夹点风险。自动行权、持有人放弃行权和结算时点可能造成预期外的多头股票。

## 与单纯持股的区别

- 多头看跌不是卖空股票：它的最大到期盈利受标的价格下界限制为端点损益 $K-p$，会到期并承受时间衰减，但没有借券、召回或无限上涨损失。
- 裸空看跌也不是直接持有股票：其上涨收益封顶在权利金 $p$；只有跌破 $K$ 后，损益才以近似一比一的斜率随标的下跌，经济上的到期买入成本为 $K-p$。
- 若多头 Put 与股票多头配合，应改用[[保护性看跌 Protective Put|保护性看跌]]分析；传统[[备兑看跌 Covered Put (Sell-Write)|备兑看跌]]则是空头股票与空头 Put，不能和现金担保裸卖 Put 混为一谈。

## 盈亏曲线（到期与到期前）

![[../assets/看跌期权 Put 盈亏曲线.svg]]

> [!note] 读图口径
> 图中展示多头看跌的代表构造。实线为到期损益，虚线为尚余 30 天时的 Black–Scholes 理论损益；虚线假设隐含波动率、利率和股息率不变，并非收益预测。空头看跌是同一组腿的反向损益。

## 来源

- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/知识图谱/看涨与看跌期权|看涨与看跌期权]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/到期盈亏 Expiration Profit and Loss|到期盈亏]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/合约规格与期权术语 Contract Specifications and Option Terminology|合约规格与期权术语]]
- [[Knowledge/Concepts/经济/金融/衍生品/期权/References/Option Volatility and Pricing 双语版/风险考量 Risk Considerations|风险考量]]
