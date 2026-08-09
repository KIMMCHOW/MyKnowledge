---
title: 第11章 波动率价差策略 / Volatility Spreads
tags:
  - 期权
  - 双语阅读
section: 第11章
translation_status: 腾讯云机器初译，公式已转 LaTeX，待复核
created: 2026-08-03
---

# 第11章 波动率价差策略 / Volatility Spreads

[[00-阅读导航|← 返回阅读导航]] · [[00-翻译说明与术语表|术语表]]

> [!warning] 翻译状态
> 本章为机器初译，并使用本地术语表校验。英文原文、数字、公式和图表用于核对；中文将在后续复核中继续修订。

<!-- chapter-toc:start -->
## 本章目录 / Chapter Outline

> [!abstract] 结构导航
> 以下标题按原书顺序保留；点击可直接跳转。

- [[#跨式策略 / Straddle|跨式策略 / Straddle]]
- [[#宽跨式策略 / Strangle|宽跨式策略 / Strangle]]
- [[#蝶式价差 / Butterfly|蝶式价差 / Butterfly]]
- [[#鹰式价差 / Condor|鹰式价差 / Condor]]
- [[#比率价差 / Ratio Spread|比率价差 / Ratio Spread]]
- [[#圣诞树价差 / Christmas Tree|圣诞树价差 / Christmas Tree]]
- [[#日历价差 / Calendar Spread|日历价差 / Calendar Spread]]
- [[#时间蝶式价差 / Time Butterfly|时间蝶式价差 / Time Butterfly]]
- [[#利率与股息变化的影响 / Effect of Changing Interest Rates and Dividends|利率与股息变化的影响 / Effect of Changing Interest Rates and Dividends]]
- [[#对角价差 / Diagonal Spreads|对角价差 / Diagonal Spreads]]
- [[#选择合适的策略 / Choosing an Appropriate Strategy|选择合适的策略 / Choosing an Appropriate Strategy]]
- [[#调整 / Adjustments|调整 / Adjustments]]
- [[#提交价差委托 / Submitting a Spread Order|提交价差委托 / Submitting a Spread Order]]
<!-- chapter-toc:end -->
<!-- chapter-nav:start -->
> [!tip] 章节导航（章首）
> [[10-价差策略导论 Introduction to Spreading|← 上一章]] · [[00-阅读导航|全书导航]] · [[12-牛市与熊市价差 Bull and Bear Spreads|下一章 →]]
<!-- chapter-nav:end -->
<!-- source:block 0a5c9d9e96e209c8 -->

> [!quote]- English 1
> In Chapter 8, we showed that it is possible, at least in theory, to capture an option’s mispricing in the marketplace by employing a dynamic hedging strategy. The first step in this process involves hedging the option position, delta neutral, by taking an opposing market position in the underlying contract. But the underlying contract is not the only way in which we can hedge an option position. We might instead take our opposing delta position with other options.

在第8章中，我们表明，至少在理论上，通过采用动态对冲策略来捕捉市场上期权的错误定价是可能的。此过程的第一步涉及通过在标的合约中采取相反的市场头寸来对冲期权头寸（Delta中性）。但标的合约并不是我们对冲期权头寸的唯一方式。相反，我们可能会采取相反的Delta头寸，并采取其他选择。

<!-- source:block be5795f0c9e13351 -->

> [!quote]- English 2
> Consider a call with a delta of 50 that appears to be underpriced in the marketplace. If we buy 10 calls, resulting in a delta position of +500, we might hedge the position in any of the following ways:

考虑一个Delta为50的看涨期权，但市场上似乎定价过低。如果我们购买10个看涨期权，导致Delta头寸为+500，我们可能会通过以下任何一种方式对冲头寸：

<!-- source:block 1592cc9c40720e3c -->

> [!quote]- English 3
> Sell five underlying contracts.

卖出五份标的合约。

<!-- source:block 84684aaa398b7090 -->

> [!quote]- English 4
> Buy puts with a total delta of –500.

购买总Delta为-500的看跌期权。

<!-- source:block b0ff955d8cf11425 -->

> [!quote]- English 5
> Sell calls, different from those that we purchased, with a total delta of –500.

卖出看涨期权，与我们购买的看涨期权不同，总Delta为-500。

<!-- source:block 9805961178b63350 -->

> [!quote]- English 6
> Do a combination of any of the preceding such that we create a total delta of –500.

组合执行上述任何操作，以便创建总Delta为-500。

<!-- source:block f86a23da75ae9826 -->

> [!quote]- English 7
> There are clearly many different ways of hedging our 10 calls. Regardless of which method we choose, each spread will have certain features in common:

显然，有很多不同的方法可以对冲我们的10个看涨期权。无论我们选择哪种方法，每个价差都会有某些共同特征：

<!-- source:block 52a43b74ea1a8a88 -->

> [!quote]- English 8
> Each spread will be approximately delta neutral.

每个价差将大致为Delta中性。

<!-- source:block 0df6b98f1d0ecc08 -->

> [!quote]- English 9
> Each spread will be sensitive to changes in the price of the underlying instrument.

每个价差都对标的工具价格的变化敏感。

<!-- source:block b738b3ab0d69904e -->

> [!quote]- English 10
> Each spread will be sensitive to changes in implied volatility.

每个价差都对隐含波动率的变化敏感。

<!-- source:block ec14e08de6a7d9fc -->

> [!quote]- English 11
> Each spread will be sensitive to the passage of time.

每次价差都会对时间的推移很敏感。

<!-- source:block 9bc56f2c536a899b -->

> [!quote]- English 12
> Spreads with the foregoing characteristics fall under the general heading of *volatility spreads*. In this chapter, we will look at the most common types of volatility spreads, initially by examining their expiration values and then by considering their delta, gamma, theta, vega, and rho characteristics.

具有上述特征的价差属于波动率价差的一般标题。在本章中，我们将研究最常见的波动率价差类型，首先检查它们的到期值，然后考虑它们的Delta、Gamma、Theta、Vega和Rho特征。

<!-- source:block 643323c2a901536d -->

## 跨式策略 / Straddle

<!-- source:block 16755027126a1761 -->

> [!quote]- English 13
> A *straddle* consists of a call and a put where both options have the same exercise price and expiration date. In a straddle, both options are either purchased (a *long straddle*) or sold (a *short straddle*). Examples of long and short straddles, with their expiration profit-and-loss (P&L) graphs, are shown in Figures 11-1 and 11-2.

跨式期权由看涨期权和看跌期权组成，两种期权具有相同的行权价和到期日期。在跨式中，两种选择要么购买（多头跨式），要么出售（空头跨式）。图11-1和11-2显示了多头和空头跨式的示例及其到期损益（P & L）图。

<!-- source:block 78812e6d9e1b15de -->

*Figure 11-1 Long straddle as time passes or volatility declines. / Figure 11-1 Long straddle as time passes or volatility declines.*

<!-- source:block 1c92a23e2a4e8202 -->

![原书图表](assets/ch11/f0170-01.jpg)

<!-- source:block 33969c1437fdd224 -->

*Figure 11-2 Short straddle as time passes or volatility declines. / Figure 11-2 Short straddle as time passes or volatility declines.*

<!-- source:block bbd3b376ad5c5d86 -->

![原书图表](assets/ch11/f0171-01.jpg)

<!-- source:block c37befbcfb9f067e -->

> [!quote]- English 16
> At expiration, the value of a straddle can be expressed as a simple parity graph. But what about its value prior to expiration? As with all option positions, some changes in market conditions will help the strategy and some changes will hurt. From Figure 11-1, we can see that a long straddle becomes more valuable when the underlying market moves away from the exercise price and less valuable as time passes if no movement occurs. At the same time, any increase in volatility will help, while any decline will hurt. These characteristics are indicated by the risk measures associated with the position:

到期时，跨式的值可以表示为简单的平价图。但到期前的价值又如何呢？与所有期权头寸一样，市场条件的一些变化将有助于策略，而一些变化则会造成伤害。从图11-1可以看出，当标的市场远离行权价时，多头跨式变得更有价值，而如果没有发生波动，则随着时间的推移，多头跨式变得更有价值。与此同时，波动率的任何增加都会有所帮助，而波动率的任何下降都会造成伤害。这些特征由与头寸相关的风险指标指示：

<!-- source:block 627fe716fa74a683 -->

> [!quote]- English 17
> +Gamma (desire for movement in the underlying contract)

$$
+\text{Gamma} (\text{desire for movement in the underlying contract})
$$

<!-- source:block 37b8e0cd6758e266 -->

> [!quote]- English 18
> –Theta (the value of the position declines as time passes)

$$
-\text{Theta} (\text{the value of the position declines as time passes})
$$

<!-- source:block 80f314da47f45caa -->

> [!quote]- English 19
> +Vega (the value of the position increases as implied volatility rises)

$$
+\text{Vega} (\text{the value of the position increases as implied volatility rises})
$$

<!-- source:block e7e43e45822d9cff -->

> [!quote]- English 20
> The characteristics of a short straddle are shown in Figure 11-2:

空头跨式的特征如图11-2所示：

<!-- source:block 6bc56be4a50f2667 -->

> [!quote]- English 21
> –Gamma (movement in the underlying contract will hurt the position)

$$
-\text{Gamma} (\text{movement in the underlying contract will hurt the position})
$$

<!-- source:block e38566b5e38cb52f -->

> [!quote]- English 22
> +Theta (the value of the position increases as time passes)

$$
+\text{Theta} (\text{the value of the position increases as time passes})
$$

<!-- source:block 2fee66ee2d486baa -->

> [!quote]- English 23
> –Vega (the value of the position increases as implied volatility falls)

$$
-\text{Vega} (\text{the value of the position increases as implied volatility falls})
$$

<!-- source:block 97aec6fd88b9e3ca -->

> [!quote]- English 24
> Straddles are most often executed one to one (one call for each put) using at-the-money options. When this is done, the spread will be approximately delta neutral because the delta values of the call and put will be close to 50 and –50. A straddle can also be done with options that are either in the money or out of the money. For example, with the underlying contract trading at 100, we might buy the September 95 straddle. If the September 95 calls, which are in the money, have a delta of 75 and the September 95 puts, which are out of the money, have a delta of –25, the total delta will be 75 – 25 = 50, resulting in a *bull straddle*. If we want the straddle to be delta neutral, we will need to adjust the number of contracts by purchasing three puts for every call:

跨式最常使用ATM期权一对一执行（每次看跌期权一次）。完成此操作后，价差将大致为Delta中性，因为看涨期权和看跌期权的Delta值将接近50和-50。 跨式也可以使用ITM或OTM期权来完成。例如，当标的合约的交易价格为100,时，我们可以购买9月的95跨式期权。 如果9月95看涨期权（为ITM）的Delta为75，而9月95看跌期权（为OTM）的Delta为-25,，则总Delta将为75 - 25 = 50,，从而导致牛市跨式。 如果我们希望跨式保持Delta中性，我们需要通过为每次看涨期权购买三个看跌期权来调整合约数量：

<!-- source:block a798317356fb8946 -->

> [!quote]- English 25
> Buy 1 September 95 call (delta = 75).

$$
\text{Buy} 1 \text{September} 95 \text{call} (\text{delta} = 75)
$$

<!-- source:block fe5958f316edf90a -->

> [!quote]- English 26
> Buy 3 September 95 puts (delta = –25).

$$
\text{Buy} 3 \text{September} 95 \text{puts} (\text{delta} = -25)
$$

<!-- source:block 99d9855d685b3635 -->

> [!quote]- English 27
> This spread still qualifies as a straddle because we are buying calls and puts at the same exercise price. But, more specifically, this is a *ratio straddle* because the number of long market contracts (the calls) and the number of short market contracts (the puts) are unequal.

这种价差仍然符合跨式标准，因为我们以相同的行权价购买看涨期权和看跌期权。但更具体地说，这是一个跨比例，因为多头市场合约（看涨期权）的数量和空头市场合约（看跌期权）的数量是不平等的。

<!-- source:block 43fdda4002528c12 -->

## 宽跨式策略 / Strangle

<!-- source:block 8a31640a0241e992 -->

> [!quote]- English 28
> Like a straddle, a *strangle* consists of a long call and a long put (a long strangle) or a short call and a short put (a short strangle), where both options expire at the same time. But in a strangle the options have different exercise prices. Typical long and short strangles are shown in Figures 11-3 and 11-4.

就像跨式一样，宽跨式由多头看涨和多头看跌（多头宽跨式）或空头看涨和空头看跌（空头宽跨式）组成，两种选择同时到期。但在宽跨式中，这些期权有不同的行权价。典型的长颈和短颈宽跨式如图11-3和11-4所示。

<!-- source:block 58c8e642b9fa877c -->

*图11-3随着时间的推移或波动率的下降，多头宽跨式。 / Figure 11-3 Long strangle as time passes or volatility declines.*

<!-- source:block aa6e07c43353e69a -->

![原书图表](assets/ch11/f0172-01.jpg)

<!-- source:block fb7569cc269a6289 -->

*图11-4随着时间的推移或波动率的下降，空头宽跨式。 / Figure 11-4 Short strangle as time passes or volatility declines.*

<!-- source:block e0b13f371478028b -->

![原书图表](assets/ch11/f0173-01.jpg)

<!-- source:block 60ca4a3e29c66c5e -->

> [!quote]- English 31
> As with a straddle, strangles are most often done one to one (one call for each put). In order to ensure that the position is delta neutral, exercise prices are usually chosen so that the call and put deltas are approximately equal.

与跨式一样，宽跨式通常是一对一完成的（每次看跌期权一次看涨期权）。为了确保头寸的Delta中性，通常选择行权价以使看涨和看跌Delta大致相等。

<!-- source:block 6a5e065c5c52d804 -->

> [!quote]- English 32
> If a strangle is identified only by its expiration month and exercise prices, there may be some confusion as to the specific options involved. A March 90/110 strangle might consist of a March 90 put and a March 110 call. But it might also consist of a March 90 call and a March 110 put. Both strategies are consistent with the definition of a strangle. To avoid confusion, a strangle is commonly assumed to consist of out-of-the-money options. If the underlying market is currently at 100 and a trader wants to purchase the March 90/110 strangle, everyone will assume that he wants to purchase a March 90 put and a March 110 call. Although both strangles have essentially the same P&L profile, in-the-money options tend to be less actively traded than their out-of-the-money counterparts. A strangle consisting of in-the-money options is sometimes referred to as a *guts*.

如果仅通过到期月份和行权价格来识别Strangle，那么所涉及的具体期权可能会出现一些混乱。3月90/110宽跨式可能包括3月90 看跌期权和3月110 看涨期权。但它也可能由3月90 看涨期权和3月110看跌看跌期权组成。 这两种策略都与宽跨式的定义一致。为了避免混淆，Strangle通常被认为由OTM期权组成。 如果标的市场当前为100，并且交易员想要购买March 90/110 Strangle，则每个人都会认为他想要购买March 90 看跌期权和March 110 看涨期权。 尽管两种Strangle的损益状况基本相同，但ITM期权的交易往往不如OTM期权活跃。由ITM期权组成的宽跨式有时被称为胆量。

<!-- source:block f35545fc5b9f4dde -->

> [!quote]- English 33
> Note that the risk characteristics of a strangle are similar to those of a straddle:

请注意，宽跨式的风险特征与跨式的风险特征相似：

<!-- source:block 87af43f1b6c1c8ea -->

> [!quote]- English 34
> Long strangle: +gamma/–theta/+vega

$$
\text{Long strangle}: +\text{gamma}/-\text{theta}/+\text{vega}
$$

<!-- source:block 27acfaa75787cb08 -->

> [!quote]- English 35
> Long straddle: +gamma/–theta/+vega

$$
\text{Long straddle}: +\text{gamma}/-\text{theta}/+\text{vega}
$$

<!-- source:block 0afa34302c4375f6 -->

> [!quote]- English 36
> A new option trader often finds long straddles and strangles attractive because strategies with limited risk and unlimited profit potential offer great appeal, especially when the profit is unlimited in both directions. However, if the hoped-for movement fails to materialize, a trader will find that losing money, even a limited amount, can also be a painful experience. This is not an endorsement of either long or short straddles. Under the right conditions, either strategy may be sensible. But an intelligent trader needs to consider not only whether the risk and reward is limited or unlimited but also the likelihood of the various outcomes. This, of course, is one important reason for using a theoretical pricing model.

新的期权交易员通常会发现长跨和宽跨式有吸引力，因为风险有限和利润潜力无限的策略具有很大的吸引力，尤其是当利润在两个方向上都是无限的时候。然而，如果所希望的走势未能实现，交易者会发现赔钱，即使是有限的金额，也可能是一种痛苦的经历。这并不是对长跨或短跨的认可。在适当的条件下，任何一种策略都可能是明智的。但聪明的交易者不仅需要考虑风险和回报是否有限或无限，还需要考虑各种结果的可能性。当然，这是使用理论定价模型的一个重要原因。

<!-- source:block ca63d829cb5eadde -->

## 蝶式价差 / Butterfly

<!-- source:block b6690a23534cda3d -->

> [!quote]- English 37
> Thus far we have looked at spreads that involve buying or selling two different option contracts. However, we can also construct spreads consisting of three, four, or even more different options. A *butterfly* is a common three-sided spread consisting of options with equally spaced exercise prices, where all options are of the same type (either all calls or all puts) and expire at the same time. In a long butterfly, the outside exercise prices are purchased and the inside exercise price is sold, and vice versa for a short butterfly. Moreover, the ratio of a butterfly never varies. It is always 1 × 2 × 1, with two of each inside exercise price traded for each one of the outside exercise prices. Typical long and short butterflies are shown in Figures 11-5 and 11-6.

到目前为止，我们已经研究了涉及购买或出售两种不同期权合约的价差。然而，我们也可以构建由三个、四个甚至更多不同期权组成的价差。蝴蝶是一种常见的三面价差，由行权价等间隔的期权组成，所有期权类型相同（所有看涨期权或所有看跌期权）并且同时到期。在多头蝶式价差中，买入外部行权价，卖出内部行权价，反之亦然，对于空头蝶式价差。而且，蝴蝶的比例永远不会改变。它始终是1 × 2 × 1，每个内部行权价中有两个交易为每个外部行权价。典型的多头蝶式价差和空头蝶式价差如图11-5和11-6所示。

<!-- source:block 252171a7d74e5527 -->

*图11-5随着时间的推移或波动率下降，多头蝶式价差。 / Figure 11-5 Long butterfly as time passes or volatility declines.*

<!-- source:block 6fb61bcd24eb4f0a -->

![原书图表](assets/ch11/f0174-01.jpg)

<!-- source:block 0cd303c5a8c87c2f -->

*Figure 11-6 Short butterfly as time passes or volatility declines. / Figure 11-6 Short butterfly as time passes or volatility declines.*

<!-- source:block 4d27823315dccdec -->

![原书图表](assets/ch11/f0174-02.jpg)

<!-- source:block 72ed0d9637dd0b57 -->

> [!quote]- English 40
> To a new trader, a butterfly may look quite complex since it involves three different options in different quantities. But butterflies have very simple and well-defined characteristics that make them popular trading strategies. To understand these characteristics, let’s consider the value of a long butterfly at expiration:

对于新交易者来说，蝴蝶可能看起来相当复杂，因为它涉及三种不同数量的不同期权。但蝴蝶具有非常简单且明确的特征，使它们成为流行的交易策略。为了了解这些特征，让我们考虑一下多头蝶式价差在到期时的价值：

<!-- source:block ef094586df4af8e8 -->

![原书图表](assets/ch11/t0175-01.jpg)

<!-- source:block abd4c94adc4698e3 -->

> [!quote]- English 41
> If the underlying price is below 90 at expiration, all the calls will expire worthless, and the value of the position will be 0. If the underlying contract is above 120 at expiration, the combined value of the 90 and 110 calls will equal the value of the two 100 calls. Again, the value of the butterfly will be 0. Now suppose that the underlying contract is between 90 and 110 at expiration, specifically, right at the inside exercise price of 100. The 90 call will be worth 10.00, while the 100 and 110 calls will be worthless. The position will be worth exactly 10.00. If the underlying moves away from 100, the value of the butterfly will decline, but its value can never fall below 0. Summarizing, at expiration, a butterfly is worthless if the underlying contract is above or below the outside exercise prices (sometimes referred to as the *wings* of the butterfly). It has its maximum value at expiration when the underlying contract is right at the inside exercise price (sometimes referred to as the *body* of the butterfly). And the maximum value is always equal to the amount between exercise prices, in our example 10.00.

如果到期时标的价格低于90，则所有看涨期权到期时将一文不值，并且头寸价值将为0。如果标的合约到期时高于120，则90和110看涨期权的总价值将等于两个100看涨期权的价值。同样，蝶式价差的值将为0。现在假设标的合约到期时在90至110之间，具体来说，内部行权价为100。90看涨期权将价值10.00，而100和110看涨期权将一文不值。该头寸的价值恰好为10.00。如果基础远离100，蝶式价差的价值就会下降，但它的价值永远不能跌破0。总而言之，到期时，如果标的合约高于或低于外部行权价（有时称为蝶式价差的翅膀），蝶式价差就毫无价值。当标的合约处于内部行权价（有时称为蝶式价差体）时，它在到期时具有最大价值。最大值始终等于行权价之间的金额，在我们的示例中为10.00。

<!-- source:block 4227e8e0ced62e2c -->

> [!quote]- English 42
> Because a butterfly at expiration always has a value between 0 and the amount between exercise prices, in our example, a trader should be willing to pay some amount between 0 and 10.00 for the position. The exact amount depends on the likelihood of the underlying contract finishing close to the inside price at expiration. If there is a high probability of this occurring, a trader might be willing to pay as much as 8.00 for the butterfly since it might very well expand to its full value of 10.00. If, however, there is a low probability of this occurring and, consequently, a high probability that the underlying contract will finish outside the extreme exercise prices, a trader may only be willing to pay 1.00 or 2.00 because he may very well lose his entire investment. This also explains why our example position is a *long* butterfly. Because the position can never be worth less than 0, a trader will always be required to pay some amount for the position. Otherwise, there would be a riskless profit opportunity. When a position requires an outlay of cash, a trader has bought, or is long, the position.

因为蝴蝶在到期时总是有一个介于0和行权价之间的值，在我们的例子中，交易者应该愿意为这个头寸支付介于0和10.00之间的金额。确切的金额取决于标的合约在到期时接近内部价格的可能性。如果这种情况发生的概率很高，交易者可能愿意为蝴蝶支付高达8.00的价格，因为它很可能会膨胀到10.00的全部价值。然而，如果这种情况发生的可能性很低，因此，标的合约在极端行权价之外完成的可能性很高，交易者可能只愿意支付1.00或2.00，因为他很可能会失去他的全部投资。这也解释了为什么我们的示例头寸是多头蝶式价差。因为头寸的价值永远不会低于0，交易者总是需要为头寸支付一定的金额。否则，就有无风险的获利机会。当一个头寸需要现金支出时，交易者已经买入或做多了这个头寸。

<!-- source:block 8e3ec7bebce1e205 -->

> [!quote]- English 43
> A butterfly will tend to be delta neutral when the inside exercise price is approximately at the money. Under these conditions, a long butterfly will tend to act like a short straddle, while a short butterfly will tend to act like a long straddle. With either a long butterfly or a short straddle, a trader wants the underlying market to sit still (–gamma, +theta) and implied volatility to fall (–vega). With either a short butterfly or a long straddle, a trader wants the underlying market to make a large move (+gamma, –theta) and implied volatility to rise (+vega). But there is one important difference. While a straddle is open-ended in terms of either profit potential or risk, a butterfly is strictly limited. It can never be worth less than 0 nor more than the amount between exercise prices. This is important for a trader who might want to sell straddles but who is uncomfortable with the possibility of unlimited loss. Of course, there is always a risk-reward tradeoff. If a long butterfly has reduced risk when the trader is wrong, it will also have increased profit when the trader is right. For this reason, butterflies tend to be executed in much larger sizes than straddles. A trader may find that buying 300 butterflies (300 × 600 × 300) is actually less risky than selling 100 straddles. In option trading, size and risk do not always correlate. Some strategies done in large sizes can have a relatively small risk, while other strategies, even when done in small sizes, can have a relatively large risk. Risk depends not only on the size in which a strategy is executed but also on the characteristics of the strategy.

当内部行权价约为ATM时，蝶式价差往往是Delta中性的。在这些条件下，多头蝶式价差往往表现得像空头跨式，而空头蝶式价差往往表现得像多头跨式。 无论是做多Butterfly还是做多跨，交易员都希望标的市场保持静止（-Gamma，+Theta），并使隐含波动率下降（-Vega）。 无论是做空Butterfly还是做多头跨式，交易员都希望标的市场大幅波动（+Gamma，-Theta）并隐含波动率上升（+Vega）。但有一个重要的区别。 虽然跨式式飞机在利润潜力或风险方面是开放式的，但Butterfly飞机受到严格限制。其价值永远不能低于0，也不能超过行权价格之间的金额。 这对于可能想要出售Straddle但对无限损失的可能性感到不安的交易者来说非常重要。当然，风险与回报总是存在权衡。 如果做多蝶式价差在交易者错误时降低了风险，那么当交易者正确时，做多蝶式价差也会增加利润。因此，Butterfly的执行尺寸往往比Straddle大得多。 交易者可能会发现购买300 Butterfly（300 × 600 × 300）的风险实际上低于出售100 Straddle。在期权交易中，规模和风险并不总是相关的。 一些大规模的策略可能有相对较小的风险，而其他策略，即使是小规模的策略，也可能有相对较大的风险。风险不仅取决于执行策略的规模，还取决于策略的特征。

<!-- source:block eb09bf9b9dd07d4c -->

> [!quote]- English 44
> We know that a butterfly at expiration is worth its maximum when the underlying contract is right at the inside exercise price. If we assume that all options are European, with no possibility of early exercise, both a call and a put butterfly with the same exercise prices and the same expiration dates desire exactly the same outcome and therefore have identical characteristics. Both the March 90/100/110 call butterfly and the March 90/100/110 put butterfly will be worth a maximum of 10.00 with the underlying price exactly at 100 at expiration and a minimum of 0 with the underlying price below 90 or above 110. If both butterflies are not trading at the same price, there is a sure profit opportunity available by purchasing the cheaper and selling the more expensive.<sup>1</sup>

我们知道，当标的合约处于内部行权价时，到期的蝶式价差价值最大。 如果我们假设所有期权都是欧洲期权，不可能提前行权，那么具有相同行权价格和相同到期日的看涨期权和看跌期权蝶式价差都希望得到完全相同的结果，因此具有相同的特征。 3月90/100/110 看涨期权 Butterfly和3月90/100/110 看跌期权 Butterfly的最高价值为10.00，到期时标的价格恰好为100，最低价值为0，到期时标的价格低于90或高于110。 如果两个Butterfly的交易价格不同，那么通过购买更便宜的并出售更贵的，就有一定的利润机会。 [^ovp11-1]

<!-- source:block e55e59b5a60d17e3 -->

## 鹰式价差 / Condor

<!-- source:block 05cdbf2dd4ae5a04 -->

> [!quote]- English 45
> Just as a butterfly can be thought of as a straddle with limited risk or reward, a *condor* can be thought of as a strangle with limited risk or reward. A condor consists of four options, two inside exercise prices (the body of the condor) and two outside exercise prices (the wings of the condor).<sup>2</sup> The ratio of a condor is always 1 × 1 × 1 × 1. Although the amount between the two inside exercise prices can vary, there must be an equal amount between the two lowest exercise prices and the two highest exercise prices. As with a butterfly, all options must expire at the same time and be of the same type (either all calls or all puts). In a long condor, the two outside exercise prices are purchased and the two inside exercise prices are sold, and vice versa for a short condor. Typical long and short condors are shown in Figures 11-7 and 11-8.

正如蝶式价差可以被认为是风险或回报有限的跨式者一样，鹰式价差可以被认为是风险或回报有限的宽跨式者。鹰式价差由四个期权组成，两个内部行权价格（鹰式价差的身体）和两个外部行权价格（鹰式价差的翅膀）。 鹰式价差的比例始终是1 × 1 × 1 × 1。尽管两个内部行权价格之间的金额可能有所不同，但两个最低行权价格和两个最高行权价格之间的金额必须相等。 与Butterfly一样，所有期权必须同时到期并且类型相同（所有看涨期权或所有看跌期权）。在多头鹰式价差中，两个外部行权价格被买入，两个内部行权价格被卖出，反之亦然。 典型的长鹰式价差和短鹰式价差如图11-7和11-8所示。 [^ovp11-2]

<!-- source:block 84bebcddeac09c34 -->

*图11-7随着时间的推移或波动率下降的长秃鹰。 / Figure 11-7 Long condor as time passes or volatility declines.*

<!-- source:block afb38a0986465082 -->

![原书图表](assets/ch11/f0177-01.jpg)

<!-- source:block f5507e9cb841cfcc -->

*图11-8随着时间的推移或波动率下降，空头秃鹰。 / Figure 11-8 Short condor as time passes or volatility declines.*

<!-- source:block 6b1c079422c21809 -->

![原书图表](assets/ch11/f0177-02.jpg)

<!-- source:block 9aa16609e475e8f0 -->

> [!quote]- English 48
> The value of a condor at expiration can never be less than 0 nor more than the amount between the two higher or the two lower exercise prices. A trader who buys a condor will pay some amount between these values, expecting that the underlying contract will finish between the two intermediate exercise prices, where the condor will be worth its maximum. A trader who sells a condor will take in some amount, expecting that the underlying contract will finish outside the extreme exercise prices, where the condor will be worthless.

秃鹰到期时的价值永远不能小于0，也不能大于两个较高或两个较低行权价之间的金额。购买秃鹰的交易员将支付这些价值之间的一定金额，预计标的合约将在两个中间行权价之间完成，此时秃鹰将达到最大价值。出售秃鹰的交易员将接受一定数量的交易，预计标的合约将在极端行权价之外完成，此时秃鹰将一文不值。

<!-- source:block ca2ff4046bcbc7dd -->

> [!quote]- English 49
> A condor will be approximately delta neutral when the underlying contract is midway between the two inside exercise prices. When all options are European, the value and characteristics of a call condor and put condor will be identical.

当标的合约处于两个内部行权价之间的中间位置时，秃鹰将大致处于Delta中性状态。当所有期权都是欧洲期权时，看涨秃鹰和看跌秃鹰的价值和特征将相同。

<!-- source:block d634ddee717f73b0 -->

> [!quote]- English 50
> The four volatility spreads that we just described—straddles, strangles, butterflies, and condors—all have symmetrical P&L graphs. When executed delta neutral, as is most common, these strategies have no preference as to the direction of movement in the underlying market. Long straddles and strangles and short butterflies and condors prefer movement in the underlying market and an increase in implied volatility (+gamma, –theta, +vega). Short straddles and strangles and long butterflies and condors prefer no movement in the underlying market and a decline in implied volatility (–gamma, +theta, –vega). These characteristics are summarized in Figure 11-9.

我们刚刚描述的四种波动率价差——跨式、宽跨式、蝶式价差和鹰式价差——都具有对称的损益图。当以Delta中性执行时（这是最常见的），这些策略对标的市场的走势方向没有偏好。多头跨式和宽跨式以及空头蝶式价差和鹰式价差更喜欢标的市场的波动和隐含波动率（+Gamma、-Theta、+Vega）的增加。空头的跨式和宽跨式以及多头蝶式价差和鹰式价差更喜欢标的市场没有波动和隐含波动率（-Gamma、+Theta、-Vega）下降。这些特征总结在图11-9中。

<!-- source:block 4111f318a51c6f02 -->

*图11-9对称策略。 / Figure 11-9 Symmetrical strategies.*

<!-- source:block 447260c0c2b05774 -->

![原书图表](assets/ch11/f0178-01.jpg)

<!-- source:block 8b38a01d9804f501 -->

## 比率价差 / Ratio Spread

<!-- source:block 30a34debced11c79 -->

> [!quote]- English 52
> In a volatility spread, a trader need not be totally indifferent to the direction of movement in the underlying market. The trader may believe that movement in one direction is more likely than movement in the other direction. Given this, the trader may wish to construct a spread that either maximizes his profit or minimizes his loss when movement occurs in one direction rather than the other. In order to achieve this, a trader can construct a *ratio spread*—buying and selling unequal numbers of options where all options are the same type and expire at the same time. As with other volatility positions, the spread is typically delta neutral.

在波动价差中，交易者不必对标的市场的走势方向完全漠不关心。交易者可能认为，朝一个方向移动的可能性比朝另一个方向移动的可能性更大。鉴于此，交易者可能希望构建一个价差，当移动发生在一个方向而不是另一个方向时，既可以最大化利润，也可以最大化损失。为了实现这一目标，交易者可以构建一个价差比例，买入和卖出不等数量的期权，其中所有期权都是相同的类型并且同时到期。与其他波动率头寸一样，价差通常为Delta中性。

<!-- source:block 6795b90b1c9868bf -->

> [!quote]- English 53
> Consider the following delta-neutral position with the underlying contract trading at 100 (delta values are in parentheses):

考虑以下Delta中性头寸，标的合约交易为100（Delta值在括号中）：

<!-- source:block b0d2a6a8fa7a2225 -->

![原书图表](assets/ch11/t0179-01.jpg)

<!-- source:block f26aac1882d1e78b -->

> [!quote]- English 54
> Now let’s consider three possible prices for the underlying contract at expiration:

现在让我们考虑标的合约到期时的三种可能价格：

<!-- source:block c9888b14a5a91489 -->

![原书图表](assets/ch11/t0179-02.jpg)

<!-- source:block 5b1fc114de536b07 -->

> [!quote]- English 55
> If the underlying contract makes a very big move in either direction, the position will show a profit. Of course, the profit will be much larger if the move is upward. If the underlying sits at 100 until expiration, the position will show a loss. This *call ratio spread*, where more calls are purchased than sold, wants movement in the underlying contract but clearly prefers upward movement, where the potential profit is unlimited. The P&L diagram for this type of strategy is shown in Figure 11-10.

如果标的合约在任何一个方向上做出非常大的变动，该头寸将显示盈利。当然，如果向上移动，利润就会大得多。如果标的在到期前处于100，则该头寸将显示亏损。这种看涨比率价差（买入看涨期权多于卖出期权）希望标的合约的变动，但显然更喜欢向上变动，因为潜在利润是无限的。此类策略的损益图如图11-10所示。

<!-- source:block bc6a0c96527e5c49 -->

*图11-10随着时间的推移或波动率下降的看涨比率价差（买入多于卖出）。 / Figure 11-10 Call ratio spread (buy more than sell) as time passes or volatility declines.*

<!-- source:block d697c80f4d76a933 -->

![原书图表](assets/ch11/f0180-01.jpg)

<!-- source:block 2d0986cb3c34e88b -->

> [!quote]- English 57
> The same type of position can be created using puts. A *put ratio spread*, where more puts are purchased than sold, also prefers movement in the underlying contract. But now there is a preference for downward movement because the profit potential on the downside will be unlimited. This is shown in Figure 11-11.

可以使用看跌期权创建相同类型的头寸。看跌比率价差（买入的看跌期权多于卖出的看跌期权）也更倾向于标的合约的变动。但现在人们倾向于下行，因为下行的利润潜力将是无限的。如图11-11所示。

<!-- source:block a8e399e0e4fa8758 -->

*图11-11随着时间的推移或波动率下降，看跌比率价差（买入多于卖出）。 / Figure 11-11 Put ratio spread (buy more than sell) as time passes or volatility declines.*

<!-- source:block 4184a2ddecdf8b92 -->

![原书图表](assets/ch11/f0180-02.jpg)

<!-- source:block cf9b8c388da0c000 -->

> [!quote]- English 59
> A ratio spread where more options are purchased than sold is sometimes referred to as *backspread*. Regardless of whether the spread consists of calls or puts, this type of spread always wants movement in the underlying market (+gamma, –theta) and/or an increase in implied volatility (+vega).

购买期权多于出售期权的比例价差有时被称为回价差。无论价差是由看涨还是看跌组成，这种类型的价差总是希望标的市场的变动（+Gamma，-Theta）和/或隐含波动率的增加（+Vega）。

<!-- source:block f1508d76f0795ba1 -->

> [!quote]- English 60
> In a ratio spread where more options are purchased than sold, the spread will be worthless if the underlying contract makes a large enough downward move in the case of calls or a large enough upward move in the case of puts. For either spread to result in a profit, it must be executed initially for a credit, and this is a typical characteristic of these types of spreads. Indeed, under the assumptions of a traditional theoretical pricing model, a delta-neutral ratio spread where more options are purchased than sold should always result in a credit.

在购买期权多于出售期权的比率价差中，如果标的合约在看涨期权的情况下向下移动足够大，或者在看跌期权的情况下向上移动足够大，那么价差将毫无价值。对于任何一种价差要产生利润，首先必须为 credit 执行，这是这些类型价差的典型特征。事实上，在传统理论定价模型的假设下，Delta中性比率价差（购买的期权多于出售的期权）应该总是会产生 credit。

<!-- source:block 52a651009cc28975 -->

> [!quote]- English 61
> Ratio spreads are often used to limit the risk in one direction. If we sell more calls than we buy, the spread will act like a short straddle (–gamma, +theta, –vega) but with limited downside risk. If we sell more puts than we buy, the spread will have limited upside risk. The P&L diagrams for these types of spreads are shown Figures 11-12 and 11-13.

比率价差通常用于限制一个方向的风险。如果我们卖出的看涨期权多于买入的看涨期权，那么价差就像一个空头跨式（-Gamma，+Theta，-Vega），但下行风险有限。如果我们卖出的看跌期权多于买入的看跌期权，那么价差的上行风险将是有限的。图11-12和图11-13显示了这些类型价差的损益图。

<!-- source:block d50e4677fd618684 -->

*图11-12随着时间的推移或波动率下降，看涨比率价差（卖出多于买入）。 / Figure 11-12 Call ratio spread (sell more than buy) as time passes or volatility declines.*

<!-- source:block 4765258a9277dc48 -->

![原书图表](assets/ch11/f0181-01.jpg)

<!-- source:block ce6766b56ef5ee0f -->

*图11-13随着时间的推移或波动率下降，看跌比率价差（卖出多于买入）。 / Figure 11-13 Put ratio spread (sell more than buy) as time passes or volatility declines.*

<!-- source:block 05f1f75941c9c7bf -->

![原书图表](assets/ch11/f0181-02.jpg)

<!-- source:block 357ae62ad0f576b4 -->

> [!quote]- English 64
> A ratio spread where more options are sold than purchased is sometimes referred to as *frontspread*.<sup>3</sup> Using calls, the position will be worthless at expiration if the underlying contract is below the lower exercise price. Using puts, the position will be worthless at expiration if the underlying contract is above the higher exercise price. The fact that the value of the position cannot fall below 0 limits the downside risk if more calls are sold than purchased and the upside risk if more puts are sold than purchased.

出售的期权多于购买的期权的比例价差有时称为前价差。[^ovp11-3]使用看涨期权，如果标的合约低于较低的行权价，那么头寸在到期时将毫无价值。使用看跌期权，如果标的合约高于较高的行权价，那么该头寸在到期时将毫无价值。头寸价值不能跌破0这一事实限制了卖出看涨期权多于买入期权的下行风险，以及卖出看跌期权多于买入期权的上行风险。

<!-- source:block 6151e938e1883cbe -->

> [!quote]- English 65
> When executed as a single trade, ratio spreads are usually submitted using simple ratios, the most common being 2 to 1. However, other ratios—3 to 1, 4 to 1, or 3 to 2—are also relatively common.

当作为单笔交易执行时，比率价差通常使用简单的比率提交，最常见的是2比1。然而，其他比例——3比1、4比1或3比2——也相对常见。

<!-- source:block ee3b5d1fb6ce5c26 -->

## 圣诞树价差 / Christmas Tree

<!-- source:block b522e7f776b6ae91 -->

> [!quote]- English 66
> Ratio spreads tend to mimic straddles, but with the risk or reward limited in one direction. We can also construct strategies that mimic strangles, but again with limited risk or reward in one direction. Such spreads are known as either *Christmas trees* or *ladders*.<sup>4</sup>

比率价差往往类似于跨式投资，但风险或回报限于一个方向。我们也可以构建模仿宽跨式的策略，但同样在一个方向上具有有限的风险或回报。这种价差被称为圣诞树或梯子。 [^ovp11-4]

<!-- source:block 3534184a026096c4 -->

> [!quote]- English 67
> A call Christmas tree involves buying (selling) a call at a lower exercise price and selling (buying) one call each at two higher exercise prices. A put Christmas tree involves buying (selling) a put at a higher exercise price and selling (buying) one put each at two lower exercise prices. All options must be the same type and expire at the same time, with exercise prices most often chosen so that the entire position is delta neutral. When one option is bought and two options sold (a long Christmas tree), the position acts like a short strangle but with limited risk in one direction. When one option is sold and two options bought (a short Christmas tree), the position acts like a long strangle but with limited profit potential in one direction. P&L diagrams for typical Christmas trees are shown in Figures 11-14 through 11-17.

看涨圣诞树涉及以较低的行权价购买（出售）一个看涨期权，并以两个较高的行权价出售（购买）一个看涨期权。看跌期权圣诞树涉及以更高的行权价购买（出售）一份看跌期权，并以两个较低的行权价出售（购买）一份看跌期权。所有期权必须是相同类型且同时到期，最常选择的行权价，以便整个头寸是Delta中性的。当购买一个期权并出售两个期权（一棵长长的圣诞树）时，该头寸就像一个短暂的宽跨式，但一个方向的风险有限。当一个期权被出售并两个期权被购买（一棵短圣诞树）时，该头寸就像一个长期的宽跨式，但在一个方向上的利润潜力有限。典型圣诞树的损益图如图11-14至11-17所示。

<!-- source:block 3fab60f3d716c5dc -->

*Figure 11-14 Long call Christmas tree as time passes or volatility declines. / Figure 11-14 Long call Christmas tree as time passes or volatility declines.*

<!-- source:block bd147b5d574bc47d -->

![原书图表](assets/ch11/f0183-01.jpg)

<!-- source:block c09560a64d99698b -->

*Figure 11-15 Short call Christmas tree as time passes or volatility declines. / Figure 11-15 Short call Christmas tree as time passes or volatility declines.*

<!-- source:block 866f4d2eeafc22e2 -->

![原书图表](assets/ch11/f0183-02.jpg)

<!-- source:block 42a2fbdcf782e8ee -->

*Figure 11-16 Long put Christmas tree as time passes or volatility declines. / Figure 11-16 Long put Christmas tree as time passes or volatility declines.*

<!-- source:block 5844b791070ba83e -->

![原书图表](assets/ch11/f0184-01.jpg)

<!-- source:block 54661752a3fe2831 -->

*Figure 11-17 Short put Christmas tree as time passes or volatility declines. / Figure 11-17 Short put Christmas tree as time passes or volatility declines.*

<!-- source:block a9fd667eb4509e3c -->

![原书图表](assets/ch11/f0184-02.jpg)

<!-- source:block 45ec74dacbae541d -->

> [!quote]- English 72
> Although ratio spreads and Christmas trees have nonsymmetrical P&L graphs, their volatility characteristics tend to mimic straddles and strangles. A spread in which more options are purchased than sold will prefer movement in the underlying market and/or an increase in implied volatility (+gamma, –theta, +vega). A spread in which more options are sold than purchased will prefer no movement in the underlying market and/or a decline in implied volatility (–gamma, +theta, –vega). The characteristics of nonsymmetrical spreads are summarized in Figure 11-18.

尽管比率价差和圣诞树具有非对称的损益图，但它们的波动率特征往往模仿跨跨和宽跨式。购买期权多于出售期权的价差将更倾向于标的市场的变动和/或隐含波动率（+Gamma、-Theta、+Vega）的增加。出售的期权多于购买的期权的价差将倾向于标的市场没有变动和/或隐含波动率（-Gamma，+Theta，-Vega）下降。图11-18总结了非对称价差的特征。

<!-- source:block 1313e4bc8f6c4d2f -->

*图11-18非对称策略。 / Figure 11-18 Nonsymmetrical strategies.*

<!-- source:block 50b4a1b8cfec4202 -->

![原书图表](assets/ch11/f0185-01.jpg)

<!-- source:block c0e2cde5b848d0f9 -->

## 日历价差 / Calendar Spread

<!-- source:block 33c0d24789d68ac0 -->

> [!quote]- English 74
> If all options in a spread expire at the same time, the value of the spread at expiration depends solely on the underlying price. If, however, the spread consists of options that expire at different times, the spread’s value depends not only on where the underlying market is when the short-term option expires but also on what will happen between that date and the date on which the long-term option expires. Calendar spreads, sometimes referred to as *time spreads* or *horizontal spreads*,<sup>5</sup> consist of option positions that expire in different months.

如果价差中的所有期权同时到期，则到期时价差的价值仅取决于标的价格。然而，如果价差由不同时间到期的期权组成，那么价差的价值不仅取决于短期期权到期时标的市场的头寸，还取决于该日期和长期期权到期之日之间会发生什么。日历价差，有时称为时间价差或水平价差，[^ovp11-5]由不同月份到期的期权头寸组成。

<!-- source:block 0559b8b6f308f860 -->

> [!quote]- English 75
> The most common type of calendar spread consists of opposing positions in two options of the same type (either both calls or both puts) where both options have the same exercise price. When the long-term option is purchased and the short-term option is sold, a trader is long the calendar spread; when the short-term option is purchased and the long-term option is sold, the trader is short the calendar spread. Because a long-term option will typically be worth more than a short-term option, this is consistent with the practice of referring to any strategy that is executed at a debit as a long position and any spread that is executed for a credit as a short position.

最常见的日历价差类型由相同类型的两个期权（两个看涨期权或两个看跌期权）的相反头寸组成，其中两个期权具有相同的行权价。当购买长期期权并出售短期期权时，交易者做空日历价差;当购买短期期权并出售长期期权时，交易者做空日历价差。由于长期期权的价值通常高于短期期权，因此这与将 debit 处执行的任何策略称为多头头寸以及将 credit 处执行的任何价差称为空头头寸的做法是一致的。

<!-- source:block b513eacdcd514b27 -->

> [!quote]- English 76
> Although calendar spreads are most commonly executed one to one (one contract purchased for each contract sold), a trader may ratio a calendar spread to reflect a bullish, bearish, or neutral market sentiment. For purposes of discussion, we will focus on one-to-one calendar spreads (one long-term option for each short-term option) that are approximately delta neutral. Because at-the-money options have delta values close to 50, the most common calendar spreads consist of long and short at-the-money options.<sup>6</sup>

尽管日历价差最常见的是一对一执行（每售出一份合约购买一份合约），但交易员可能会对日历价差进行比例，以反映看涨、看跌或中性的市场情绪。出于讨论的目的，我们将重点关注大约为Delta中性的一对一日历价差（每个短期期权一个长期期权）。由于平值期权的Delta值接近50，因此最常见的日历价差包括多头和空头平值期权。[^ovp11-6]

<!-- source:block 562c672b7035d7cb -->

> [!quote]- English 77
> The value of a calendar spread depends not only on movement in the underlying market but also on the marketplace’s expectations about future market movement as reflected in the implied volatility. Because of this, a calendar spread has characteristics that differ from the other spreads we have discussed. If we assume that the options making up a calendar spread are approximately at the money, calendar spreads have two important characteristics:

日历价差的价值不仅取决于标的市场的走势，还取决于市场对隐含波动率所反映的未来市场走势的预期。 因此，日历价差具有不同于我们讨论过的其他价差的特征。如果我们假设构成日历价差的期权大约是ATM，则日历价差具有两个重要特征：

<!-- source:block 0f87f9caa394353c -->

> [!quote]- English 78
> 1. A calendar spread will increase in value if time passes with no movement in the underlying contract.

1.如果标的合约没有变动，则日历价差的价值将增加。

<!-- source:block 40fa1633038360c2 -->

> [!quote]- English 79
> 2. A calendar spread will increase in value if implied volatility rises and decline in value if implied volatility falls.

2.如果隐含波动率上升，日历价差的价值将增加，如果隐含波动率下降，日历价差的价值将下降。

<!-- source:block 1474963290470e23 -->

> [!quote]- English 80
> Why should a calendar spread become more valuable as time passes? Consider the following spread, where the underlying contract, which is currently trading at 100, is the same for both options:

为什么随着时间的推移，日历价差会变得越来越有价值？考虑以下价差，其中标的合约（目前交易价为100）对于两种期权来说都是相同的：

<!-- source:block b843959eb1978849 -->

> [!quote]- English 81
> +1 June 100 call

$$
+1 \text{June} 100 \text{call}
$$

<!-- source:block 92cfd62f9f758089 -->

> [!quote]- English 82
> –1 April 100 call

$$
-1 \text{April} 100 \text{call}
$$

<!-- source:block 37d6ba09137791c3 -->

> [!quote]- English 83
> Suppose that there are four months remaining to June expiration and two months remaining to April expiration. If we assume a constant underlying price of 100 and a constant volatility of 20 percent, the value of the individual options as time passes, as well as the value of the spread, is shown in Figure 11-19.

假设距离6月到期还有四个月，距离4月到期还有两个月。如果我们假设固定标的价格为100，固定波动率为20%，则随着时间的推移，各个期权的价值以及价差的价值如图11-19所示。

<!-- source:block f76ae6b2bea524b9 -->

*图11-19随着时间的推移日历价差的价值。 / Figure 11-19 The value of a calendar spread as time passes.*

<!-- source:block f381d7f4d95f7f27 -->

![原书图表](assets/ch11/t0187-01.jpg)

<!-- source:block 4deeb8482d223547 -->

> [!quote]- English 85
> The spread is initially worth 1.34, but as time passes, both options begin to decay. However the April option, with less time remaining to expiration, decays more rapidly than the June option. Over the first month, the April option loses 0.96, while the June option loses only 0.61. The spread has increased to 1.69.

价差最初为1.34，但随着时间的推移，这两种选择都开始减弱。然而，四月期权距离到期的剩余时间更短，因此比六月期权衰退得更快。第一个月，4月期权损失0.96，而6月期权仅损失0.61。价差已增加至1.69。

<!-- source:block 55c2acee17c69c34 -->

> [!quote]- English 86
> Over the next month, with the underlying contract still at 100, the April option, because it is at the money, must give up its entire value of 2.30. The June option will also continue to decay, and at a slightly greater rate, losing 0.73. But the calendar spread has still increased to 3.26.

在下个月，标的合约仍为100,，四月期权由于是ATM，必须放弃其全部价值2.30。六月期权也将继续衰退，并且以稍大的速度下跌0.73。但日历价差仍然增加到了3.26。

<!-- source:block 0dc00b6e067ca2a2 -->

> [!quote]- English 87
> The increase in value of the calendar spread as time passes is the result of an important characteristic of theta that was noted in Chapter 8: as time to expiration grows shorter, the theta of an at-the-money option increases. A short-term at-the-money option decays more rapidly than a long-term at-the-money option.

随着时间的推移，日历价差的价值增加是第8章指出的Theta的一个重要特征的结果：随着到期时间越来越短，平值期权的Theta也会增加。短期平值的期权比长期平值的期权衰退得更快。

<!-- source:block c4ac4a163e718bb4 -->

> [!quote]- English 88
> What will happen if the underlying contract does not sit still but instead makes a large upward or downward move? The value of a calendar spread depends on the long-term option retaining as much time value as possible while the short-term option decays. This will be true if both options remain at the money because an at-the-money option always has the greatest amount of time value. As an option moves either into the money or out of the money, its time value will disappear. A long-term option will always have greater time value than a short-term option. But, if the movement in the underlying contract is large enough and the option moves very deeply into the money or very far out of the money, even a long-term option will eventually lose almost all or its time value. This will cause the calendar spread to collapse, as shown in Figure 11-20.

如果标的合约不是静止不动，而是大幅上涨或下跌，会发生什么？日历价差的价值取决于长期期权在短期期权衰减时保留尽可能多的时间价值。 如果两个期权都是ATM，这将是正确的，因为ATM期权总是具有最大的时间价值。随着期权进入货币或OTM，其时间价值就会消失。 长期期权总是比短期期权具有更大的时间价值。但是，如果标的合约的变动足够大，并且期权非常深入地进入货币或非常远的OTM，那么即使是长期期权最终也会失去几乎所有或其时间价值。 这将导致日历价差崩溃，如图11-20所示。

<!-- source:block ac44dac8954e0dee -->

*图11-20随着标的价格变化的日历价差的价值。 / Figure 11-20 The value of a calendar spread as the underlying price changes.*

<!-- source:block 194e9ec2d1a75e57 -->

![原书图表](assets/ch11/t0187-02.jpg)

<!-- source:block 6b7557e1891e90b1 -->

> [!quote]- English 90
> Now let’s consider the effect of changing volatility on a calendar spread. The value of the April/June 100 call calendar spread at different volatilities is shown in Figure 11-21.

现在让我们考虑波动率变化对日历价差的影响。不同波动率下的4月/6月100看涨日历价差值如图11-21所示。

<!-- source:block 7c6636c002a249a3 -->

*图11-21随着波动率变化的日历价差的价值。 / Figure 11-21 The value of a calendar spread as volatility changes.*

<!-- source:block bd35764ad15aca24 -->

![原书图表](assets/ch11/t0188-01.jpg)

<!-- source:block a37e79bb90bb399f -->

> [!quote]- English 92
> As we raise or lower volatility, both options rise or fall in value, but the June option changes more quickly than the April option. We touched on this characteristic in Chapter 6, where we noted that a change in volatility will have a greater effect on a long-term option than on an equivalent short-term option. In other words, long-term options have greater vega values than short-term options. This difference in sensitivity to a change in volatility causes the calendar spread to widen if we increase volatility and to narrow if we reduce volatility.

随着我们提高或降低波动率，两种期权的价值都会上涨或下跌，但六月期权的变化比四月期权更快。我们在第6章中谈到了这一特征，其中我们指出，波动率的变化对长期期权的影响比对同等短期期权的影响更大。换句话说，长期期权比短期期权具有更大的Vega值。这种对波动率变化敏感性的差异导致日历价差如果我们增加波动率就会扩大，如果我们减少波动率就会缩小。

<!-- source:block 90c295f60110b14e -->

> [!quote]- English 93
> A trader who is long a calendar spread wants two apparently contradictory conditions in the marketplace. First, he wants the underlying contract to sit still in order to take advantage of the greater time decay for the short-term option. Second, he wants everyone to think that the market is going to move so that implied volatility will rise, causing the long-term option to rise in price more quickly than the short-term option. Can this happen? Can the market remain unchanged yet everyone think that it will move? In fact, it happens quite often because events that do not have an immediate effect on the underlying contract may be perceived to have a future effect on the underlying.

日历价差做多的交易者希望市场上出现两种明显矛盾的情况。首先，他希望标的合约保持不变，以便利用短期期权更大的时间衰减。其次，他希望每个人都认为市场将会变动，从而导致隐含波动率上升，从而导致长期期权价格上涨速度快于短期期权。这会发生吗？难道市场保持不变，但每个人都认为它会动吗？事实上，这种情况经常发生，因为对标的合约没有立即影响的事件可能会被认为对标的合约产生未来影响。

<!-- source:block 578997f4f073a195 -->

> [!quote]- English 94
> The most common example occurs when news is pending that is likely to affect the underlying contract but whose exact effect is unknown. Consider a company that announces that its CEO will make an important statement one week from today. If no one knows the content of the statement, there is unlikely to be any significant change in the company’s stock price prior to the statement. But traders will assume that the statement, when it is made, will have an effect, perhaps a dramatic one, on the stock price. The possibility of future movement in the stock price will cause implied volatility to rise. This combination of conditions—the lack of movement in the underlying stock together with rising implied volatility—will cause calendar spreads to widen.

最常见的例子发生在可能影响标的合约但具体影响尚不清楚的消息悬而未决时。假设一家公司宣布其首席执行官将在今天一周后发表重要声明。如果没有人知道该声明的内容，那么该公司股价在该声明之前不太可能发生任何重大变化。但交易员会认为，当该声明发表时，将对股价产生影响，也许是戏剧性的影响。股价未来走势的可能性将导致隐含波动率上升。这些条件的结合——标的股票缺乏波动率加上隐含波动率上升——将导致日历价差扩大。

<!-- source:block 7f252c3199957db7 -->

> [!quote]- English 95
> Of course, the assumption of future stock movement as a result of the CEO’s statement is just that—an assumption. If the statement turns out to be irrelevant to the company’s fortunes (the CEO wanted to announce that he and his wife just became grandparents), any presumption of future volatility is removed. The result will be a decline in implied volatility, causing calendar spreads to narrow.

当然，首席执行官的声明对未来股票走势的假设只是假设。如果事实证明该声明与公司的命运无关（首席执行官想宣布他和妻子刚刚成为祖父母），那么任何对未来波动的假设都将被删除。结果将是隐含波动率下降，导致日历价差缩小。

<!-- source:block bcda9ca5dae6834d -->

> [!quote]- English 96
> The effect of implied volatility is what distinguishes time spreads from the other types of spreads we have discussed. Long straddles, long strangles, and short butterflies all want the volatility of the underlying contract as well as implied volatility to rise (+gamma, +vega). Short straddles, short strangles, and long butterflies all want the volatility of the underlying contract as well as implied volatility to fall (–gamma, –vega). But with calendar spreads underlying volatility and implied volatility have opposite effects. A quiet market or an increase in implied volatility will help a long calendar spread (–gamma, +vega), while a big move in the underlying market or a decline in implied volatility will help a short calendar spread (+gamma, –vega). This opposite effect is what gives calendar spreads their unique characteristics.

隐含波动率的影响是时间价差与我们讨论过的其他类型价差的区别。多头跨式期权、多头宽跨式期权和空头蝶式价差期权都希望标的合约的波动率和隐含波动率上升（+Gamma，+Vega）。跨式空头、宽跨式式空头和蝶式价差式多头都希望标的合约的波动率和隐含波动率下降（-Gamma，-Vega）。但对于日历价差，基础波动率和隐含波动率具有相反的影响。市场平静或隐含波动率的增加将有助于长日历价差（-Gamma，+Vega），而标的市场的大幅波动或隐含波动率的下降将有助于短日历价差（+Gamma，-Vega）。这种相反的效果是日历价差具有独特特征的原因。

<!-- source:block 5ced4be8054a6f8c -->

> [!quote]- English 97
> Figures 11-22 and 11-23 show the value of long and short calendar spreads as time passes. Figures 11-24 and 11-25 show the value as volatility changes.

图11-22和11-23显示了随着时间的推移，长短日历价差的价值。图11-24和11-25显示了波动率变化时的值。

<!-- source:block 16d96c802b01d7c3 -->

*Figure 11-22 Long calendar spread as time passes. / Figure 11-22 Long calendar spread as time passes.*

<!-- source:block 877c50d0bcfe10e3 -->

![原书图表](assets/ch11/f0189-01.jpg)

<!-- source:block 0302b95ed06e5f6e -->

*Figure 11-23 Short calendar spread as time passes. / Figure 11-23 Short calendar spread as time passes.*

<!-- source:block 5f2997be434a8a22 -->

![原书图表](assets/ch11/f0189-02.jpg)

<!-- source:block eca3fef0df5956ce -->

*图11-24随着波动率下降，长日历价差。 / Figure 11-24 Long calendar spread as volatility declines.*

<!-- source:block 6e849084987b5fe1 -->

![原书图表](assets/ch11/f0190-01.jpg)

<!-- source:block eb02d1b7e1999e2d -->

*图11-25波动率下降时的短期价差 / Figure 11-25 Short calendar spread as volatility declines.*

<!-- source:block 6aa9efaf841e795b -->

![原书图表](assets/ch11/f0190-02.jpg)

<!-- source:block 0699a3d8eab79f56 -->

> [!quote]- English 102
> Although the effects of time and volatility apply to calendar spreads in all markets, there may be other considerations, depending on the specific underlying market. In the foregoing examples, we assumed that the underlying contract for both the short- and long-term option was the same. In the stock option market, this will always be true. The underlying contract for General Electric (GE) options, regardless of the expiration month, is always GE stock. And GE stock can only have a single price at any one time. But in a futures market the underlying for a futures option is a specific futures contract, and different option expirations can have different underlying futures contracts.

尽管时间和波动率的影响适用于所有市场的日历价差，但根据特定的标的市场，可能还有其他考虑因素。在前面的例子中，我们假设短期和长期期权的标的合约是相同的。在股票期权市场中，这永远是正确的。通用电气（GE）期权的标的合约，无论到期月份如何，始终是通用电气股票。而且通用电气股票在任何时候都只能有一个价格。但在期货市场中，期货期权的标的是特定的期货合约，不同的期权互换可以有不同的标的期货合约。

<!-- source:block a736dc323cb700f7 -->

> [!quote]- English 103
> Consider a futures market where there are four futures months: March, June, September, and December. If serial months are available, an April/June calendar spread will have the same underlying contract, June futures. But a March/June calendar spread will have one underlying contract for March options, a March future, and a different underlying contract for June options, a June future. Although one might expect March futures and June futures to move together, there is no guarantee that they will. Particularly in commodity markets, short-term supply and demand considerations can cause futures contracts on the same commodity to move in different directions. In addition to volatility considerations, a trader who buys a June/March call calendar spread must also consider the possibility that March futures will rise relative to June futures.

考虑一个期货市场，其中有四个期货月份：三月、六月、九月和十二月。如果有连续月份，则4月/6月日历价差将具有相同的标的合约，即6月期货。但3月/6月日历价差将有一份3月期权（3月期货）的标的合约，以及一份不同的6月期权（6月期货）的标的合约。尽管人们可能预计3月期货和6月期货会一起变动，但不能保证它们会发生。特别是在大宗商品市场，短期供需考虑可能会导致同一大宗商品的期货合约走向不同的方向。除了波动率考虑之外，购买6月/3月看涨日历价差的交易员还必须考虑3月期货相对于6月期货上涨的可能性。

<!-- source:block 5e33a2a6c299923a -->

> [!quote]- English 104
> In order to offset the risk of futures contracts moving against a calendar-spread position, it is common in commodity futures markets for a trader to offset a calendar spread with an opposing position in the futures market. In our example, if a trader buys the March/June call calendar spread, he can offset the position by purchasing March futures and selling June futures.

为了抵消期货合约与日历价差头寸变动的风险，在大宗商品期货市场中，交易员在期货市场上用相反头寸抵消日历价差的情况很常见。在我们的示例中，如果交易员购买3月/6月看涨日历价差，他可以通过购买3月期货并出售6月期货来抵消头寸。

<!-- source:block 29709085bafe09d8 -->

> [!quote]- English 105
> How many futures spreads should the trader execute? If he wants a position that is sensitive only to volatility, he ought to trade the number of futures spreads required to be delta neutral. If both calls are at the money, with deltas of approximately 50, a trader who buys 10 call calendar spreads (buy 10 June calls, sell 10 March calls) will be long 500 deltas in June and short 500 deltas in March. Therefore, he should buy 5 March futures contracts and sell 5 June futures contracts. The entire position will be (delta values are in parentheses)

交易员应该执行多少个期货价差？如果他想要只对波动率敏感的头寸，他应该交易Delta中性所需的期货价差数量。 如果两个看涨期权都是ATM，Delta约为50,，购买10 看涨期权日历价差（买入10六月看涨期权，卖出10三月看涨期权）的交易员在六月将是500 Delta 多头，在三月将是500 Delta 空头。因此，他应该购买5三月期货合约并出售5六月期货合约。 整个头寸将是（Delta值在括号中）

<!-- source:block 48bdfabd8827bf5f -->

> [!quote]- English 106
> +10 June calls (+500), – June futures (–500)

$$
+10 \text{June calls} (+500), - \text{June futures} (-500)
$$

<!-- source:block 0b59e6477a3c43b7 -->

> [!quote]- English 107
> –10 March calls (–500), +5 March futures (+500)

$$
-10 \text{March calls} (-500), +5 \text{March futures} (+500)
$$

<!-- source:block 359306288761e3e1 -->

> [!quote]- English 108
> This type of balancing is not necessary—indeed, not possible—in stock options because the underlying for all months is identical.

这种类型的平衡在股票期权中是不必要的——事实上，不可能的，因为所有月份的标的都是相同的。

<!-- source:block 843fa0cafd0f4c75 -->

## 时间蝶式价差 / Time Butterfly

<!-- source:block cb5074bf7b7414b5 -->

> [!quote]- English 109
> In futures markets, as opposed to option markets, a butterfly is a position in three futures months. A trader will buy (sell) one each of a short- and long-term futures contract and sell (buy) two intermediate-term futures contracts. A similar type of strategy can be done in option markets. A traditional option butterfly consists of options at three different exercise prices but with the same expiration date. A time butterfly (sometimes shortened to *time fly*) consists of options at the same exercise price but with three different expiration dates. All options must be the same type (either all calls or all puts), with approximately the same amount of time between expirations. The outside expiration months are usually referred to as the *wings* and the inside expiration month as the *body*. Some typical time butterflies might be

在期货市场（与期权市场相反）中，蝶式价差是指三个期货月内的头寸。交易员将购买（出售）一份短期和长期期货合约，并出售（购买）两份中期期货合约。类似类型的策略也可以在期权市场中进行。传统的期权蝶式价差由三种不同行权价但到期日相同的期权组成。时间蝶式价差（有时缩写为时间飞行）由行权价相同但到期日期不同的期权组成。所有期权必须是相同类型（所有看涨期权或所有看跌期权），两次期权之间的时间大致相同。外部到期月份通常称为翅膀，内部到期月份称为身体。一些典型的时间蝶式价差可能是

<!-- source:block 66b717286fd58f16 -->

![原书图表](assets/ch11/e0192-01.jpg)

<!-- 原 EPUB 中此公式为图片，已原样保留 -->

<!-- source:block f62476310ae7c88a -->

> [!quote]- English 110
> Note that a time butterfly consists of simultaneously buying or selling a long-term calendar spread and taking an opposing position in a short-term calendar spread, where each spread has one common expiration month. The example May/June/July 100 call time butterfly consists of buying the May 100 call and selling the June 100 call (selling the May/June calendar spread) and simultaneously selling the June 100 call and buying the July 100 call (buying the June/July calendar spread).

请注意，时间蝶式价差包括同时购买或出售长期日历价差并在短期日历价差中采取相反的头寸，其中每个价差都有一个共同的到期月份。5月/6月/7月100看涨时间蝶式价差示例包括购买5月100看涨时间和出售6月100看涨时间（出售5月/6月日历价差）以及同时出售6月100看涨时间和购买7月100看涨时间（购买6月/7月日历价差）。

<!-- source:block fc9c9bfec4227640 -->

> [!quote]- English 111
> If all options remain at the money, as time passes, the value of a calendar spread will increase. The short-term spread must therefore be worth more than the long-term spread. Consequently, if we buy the short-term calendar spread and sell the long-term calendar spread (buying the body and selling the wings), in total, we will pay more than we receive. Because the entire position will result in a debit, we are *long* the time butterfly. If we do the opposite, selling the short-term calendar spread and buying the long-term spread (selling the body and buying the wings), we are *short* the time butterfly.<sup>7</sup> This can be somewhat confusing because in a traditional butterfly consisting of different exercise prices, the combination of buying the wings and selling the body results in a debit. But in a time butterfly consisting of different expiration months, buying the wings and selling the body results in a credit.

若所有期权始终处于 ATM，随着时间流逝，日历价差的价值会增加，因此短期限日历价差应比长期限日历价差更有价值。若买入短期限日历价差、卖出长期限日历价差（买入蝶身、卖出蝶翼），总支付金额将大于总收入；整个头寸产生 `debit`，所以这是多头时间蝶式价差。若反向操作，即卖出短期限日历价差、买入长期限日历价差（卖出蝶身、买入蝶翼），则是空头时间蝶式价差。这里容易混淆：在由不同行权价构成的传统蝶式价差中，买入蝶翼、卖出蝶身会产生 `debit`；而在由不同到期月份构成的时间蝶式价差中，同样的买翼卖身组合却会产生 `credit`。 [^ovp11-7]

<!-- source:block 6ae9c5477503ea03 -->

> [!quote]- English 112
> The value of a long time butterfly as time passes and as volatility falls is shown in Figures 11-26 and 11-27. The value of the spread will tend to collapse as the underlying contract moves away from the exercise price, implying that the spread has a negative gamma. Consequently, the spread must also have a positive theta. Finally, the value of the spread falls as volatility declines, implying that the spread has a positive vega. In sum, a long time butterfly has characteristics similar to those of a long calendar spread.

随着时间的推移和波动率的下降，多头时间蝶式价差的价值如图11-26和11-27所示。随着标的合约远离行权价，价差的价值往往会崩溃，这意味着价差具有负的Gamma。因此，价差也必须具有正的Theta。最后，价差的价值随着波动率的下降而下降，这意味着价差具有正的Vega。总而言之，多头时间蝶式价差的特征与长日历价差的特征相似。

<!-- source:block 3c6170d036e3ec73 -->

*图11-26随着时间的推移，多头时间蝶式价差。 / Figure 11-26 Long time butterfly as time passes.*

<!-- source:block 6b2c29ce42bb37da -->

![原书图表](assets/ch11/f0193-01.jpg)

<!-- source:block fec594b57d5c9ec0 -->

*Figure 11-27 Long time butterfly as volatility declines. / Figure 11-27 Long time butterfly as volatility declines.*

<!-- source:block b8a395f80272a35c -->

![原书图表](assets/ch11/f0193-02.jpg)

<!-- source:block c1f63e7a2cc37f6c -->

## 利率与股息变化的影响 / Effect of Changing Interest Rates and Dividends

<!-- source:block 0c7f20a106c8bdb8 -->

> [!quote]- English 115
> Thus far we have considered only the effects of changes in underlying price, time, and volatility on the value of a volatility spread. What about changes in interest rates and, in the case of stocks, dividends?

到目前为止，我们仅考虑了标的价格、时间和波动率的变化对波动率价差价值的影响。利率的变化又如何？就股票而言，股息的变化又如何？

<!-- source:block 15d687f91a29bef7 -->

> [!quote]- English 116
> Because there is no carrying cost associated with the purchase or sale of a futures contract, interest rates have only a minor impact on futures options and, consequently, a relatively minor effect on the value of all futures option volatility spreads.<sup>8</sup> However, in a stock option market, a change in interest rates will cause the forward price of stocks to change. If all options in a spread expire at the same time, the change in forward price is likely to affect all options equally, causing only small changes in the value of the spread. However, if we have a stock option position involving two different expiration dates, we must consider two different forward prices. And these two forward prices may not be equally sensitive to a change in interest rates.

由于不存在与期货合约的购买或出售相关的持有成本，因此利率对期货期权的影响较小，因此对所有期货期权波动率价差的价值的影响相对较小。[^ovp11-8]然而，在股票期权市场中，利率的变化将导致股票的远期价格发生变化。如果价差中的所有期权同时到期，则远期价格的变化可能会平等地影响所有期权，只会导致价差价值的微小变化。然而，如果我们的股票期权头寸涉及两个不同的到期日，我们必须考虑两个不同的远期价格。这两种远期价格对利率变化可能不一样敏感。

<!-- source:block 055c88454602d80e -->

> [!quote]- English 117
> Consider the following situation:

考虑以下情况：

<!-- source:block 02c711dcee53d17c -->

> [!quote]- English 118
> Stock price = 100 interest rate = 8.00% dividend = 0

$$
\text{Stock price} = 100 \text{interest rate} = 8.00\% \text{dividend} = 0
$$

<!-- source:block bab88cacdc233037 -->

> [!quote]- English 119
> Suppose that a trader buys a call calendar spread:

假设交易员购买了看涨日历价差：

<!-- source:block b72cd0e9ca686afe -->

> [!quote]- English 120
> +10 June 100 calls–10 March 100 calls

+10六月100看涨期权-10三月100看涨期权

<!-- source:block 52556e843f04103c -->

> [!quote]- English 121
> If there are three months remaining to March expiration and six months remaining to June expiration, the forward prices for March stock and June stock are 102.00 and 104.00, respectively. If interest rates rise to 10 percent, the forward price for March will be 102.50 and the forward price for June will be 105. With more time remaining to June expiration, the June forward price is more sensitive to a change in interest rates. Assuming that the deltas of both options are approximately equal, the June option will be more affected by the increase in interest rates than the March option, and the calendar spread will expand. In the same way, if interest rates decline, the calendar spread will narrow because the June forward price will fall more quickly than the March forward price. A long call calendar spread in the stock option market must therefore have a positive rho, and a short call calendar spread must have a negative rho.

如果距离3月到期还剩三个月，距离6月到期还剩六个月，则3月股票和6月股票的远期价格分别为102.00和104.00。如果利率升至10%，3月份的远期价格将为102.50，6月份的远期价格将为105。由于距离6月到期还有更多时间，6月远期价格对利率变化更加敏感。假设两种期权的Delta大致相等，那么六月期权将比三月期权更受利率上涨的影响，日历价差将会扩大。同样，如果利率下降，日历价差将缩小，因为6月远期价格下跌速度将比3月远期价格更快。因此，股票期权市场中的多头看涨日历价差必须具有正的Rho，而空头看涨日历价差必须具有负的Rho。

<!-- source:block 04402f7950df3356 -->

> [!quote]- English 122
> Changes in interest rates have the opposite effect on stock option puts. In our example, if interest rates rise from 8 to 10 percent, the June forward price will rise more than the March forward price. If we assume, again, that the deltas of both options are approximately equal, and recalling that puts have negative deltas, the June put will show a greater decline in value than the March put. The put calendar spread will therefore narrow. In the same way, if interest rates decline, the put calendar spread will expand. A long put calendar spread in the stock option market must therefore have a negative rho, and a short put calendar spread must have a positive rho.

利率变化对股票期权看跌期权产生相反的影响。在我们的例子中，如果利率从8%上升到10%，则6月远期价格的涨幅将超过3月远期价格。如果我们再次假设两种期权的Delta大致相等，并回顾看跌期权的Delta为负，那么6月看跌期权的价值跌幅将大于3月看跌期权。因此，看跌日历价差将缩小。同样，如果利率下降，看跌日历价差将会扩大。因此，股票期权市场上的多头日历价差必须具有负的Rho，而空头日历价差必须具有正的Rho。

<!-- source:block 97a6a455b85dabca -->

> [!quote]- English 123
> The degree to which stock option calendar spreads are affected by changes in interest rates depends primarily on the amount of time between expirations. If there are six months between expirations (e.g., March/September), the effect will be much greater than if there is only one month between expirations (e.g., March/April).

股票期权日历价差受利率变化影响的程度主要取决于期权之间的时间长度。如果间隔六个月（例如，三月/九月），其影响将比两次分娩之间只有一个月大得多（例如，三月/四月）。

<!-- source:block 835dbb968a367aa5 -->

> [!quote]- English 124
> Changes in dividends can also affect the value of stock option calendar spreads because it may change the forward price of the stock. Dividends, however, have the opposite effect on stock options as changes in interest rates. An increase in the dividend lowers the forward price of stock, while a cut in the dividend raises the forward price. If all options expire at the same time, the change in the forward price for the stock will have an equal effect on all options, and the change in the value of a spread will be negligible. But in a calendar spread, if at least one dividend payment is expected between the expiration dates, an increase in dividends will cause a call calendar spread to narrow and put calendar spread to expand. A decrease in dividends will have the opposite effect, causing a call calendar spread to widen and a put calendar spread to narrow. Even though there is no Greek letter associated with dividend risk, we might say that a call calendar spread has negative dividend risk (its value falls as dividends rise) and a put calendar spread has positive dividend risk (its value rises as dividends rise). Examples of the effects of changing interest rates and dividends on stock option calendar spreads are shown in Figure 11-28.

股息的变化也会影响股票期权日历价差的价值，因为它可能会改变股票的远期价格。然而，股息对股票期权的影响与利率变化相反。股息的增加会降低股票的远期价格，而股息的减少会提高股票的远期价格。如果所有期权同时到期，股票远期价格的变化将对所有期权产生同等影响，价差价值的变化将可以忽略不计。但在日历价差中，如果预计在到期日之间至少有一次股息支付，则股息的增加将导致看涨日历价差缩小并导致日历价差扩大。股息的减少将产生相反的效果，导致看涨日历价差扩大，看跌日历价差缩小。尽管没有与股息风险相关的希腊字母，但我们可能会说看涨日历价差具有负股息风险（其价值随着股息上涨而下降），而看跌日历价差具有正股息风险（其价值随着股息上涨而上升）。利率和股息变化对股票期权日历价差的影响示例如图11-28所示。

<!-- source:block 82947987c8eb524c -->

*图11-28利率变化和股息变化对股票期权日历价差的影响。 / Figure 11-28 Effect of changing interest rates and changing dividends on stock option calendar spreads.*

<!-- source:block 3e998a0a21880c41 -->

![原书图表](assets/ch11/f0195-01.jpg)

<!-- source:block f45e38fdd0fef486 -->

![原书图表](assets/ch11/f0196-01.jpg)

<!-- source:block f622973ad80f940f -->

> [!quote]- English 126
> In Figure 11-28, we can see that an increase in interest rates will reduce the value of a put calendar spread and an increase in dividends will reduce the value of a call calendar spread. Indeed, if we raise interest rates high enough, the put calendar spread can take on a negative value, with the long-term put having a lower value than the short-term put. The same will be true for a call calendar spread if we increase dividends enough. If a stock pays no dividends, the value of a call calendar spread should always have some value greater than 0. Even if volatility is very low, the spread should still be worth a minimum of the cost of carry on the stock between expiration months. This is only true, however, if a trader can carry a short stock position between expiration months. If a situation arises where no stock can be borrowed, the trader who owns a call calendar spread may be forced to exercise his long-term option, thereby losing the time value associated with the option. This is sometimes referred to as a *short squeeze*.

在图11-28中，我们可以看到，利率的上升将减少看跌日历价差的价值，股息的增加将减少看涨日历价差的价值。事实上，如果我们将利率提高到足够高，看跌期权日历价差可能会呈负值，长期看跌期权的价值低于短期看跌期权。如果我们增加足够的股息，看涨日历价差也会如此。如果股票不支付股息，则看涨日历价差的价值应该始终具有大于0的值。即使波动率非常低，价差仍应相当于到期月份之间股票结转成本的最低值。然而，只有当交易员可以在到期月份之间持有空头头寸时，这才成立。如果出现无法借入股票的情况，拥有看涨日历价差的交易员可能会被迫行权其长期期权，从而失去与期权相关的时间价值。这有时被称为短暂挤压。

<!-- source:block 2449fec734fef42f -->

## 对角价差 / Diagonal Spreads

<!-- source:block 2637737255807d4e -->

> [!quote]- English 127
> A *diagonal spread* is similar to a calendar spread except that the options have different exercise prices. Although many diagonal spreads are executed one to one (one long-term option for each short-term option), diagonal spreads can also be ratioed, with unequal numbers of long and short market contracts. With the large number of variations in diagonal spreads, it is almost impossible to generalize about their characteristics. Each diagonal spread must be analyzed separately to determine the risks and rewards associated with the spread.

对角线价差与日历价差类似，只是期权具有不同的行权价。尽管许多对角线价差是一对一执行的（每个短期期权一个长期期权），但对角线价差也可以按比例进行，多头和空头市场合约的数量不等。由于对角线价差存在大量变化，几乎不可能对其特征进行概括。必须单独分析每个对角线价差，以确定与价差相关的风险和回报。

<!-- source:block 43aa4348622b79b0 -->

> [!quote]- English 128
> There is, however, one type of diagonal spread about which we can generalize. If a diagonal spread is done one to one and both options are of the same type and have approximately the same delta, the diagonal spread will act very much like a conventional calendar spread. Examples of this type of diagonal spread are shown in Figure 11-29 (delta values are in parentheses).

然而，有一种我们可以概括的对角价差类型。如果对角线价差是一对一的，并且两个期权的类型相同并且具有大致相同的Delta，那么对角线价差的作用将非常像传统的日历价差。图11-29显示了这种类型的对角线扩展的示例（Delta值在括号中）。

<!-- source:block 1b72bda19fb03283 -->

*Figure 11-29 Diagonal spreads. / Figure 11-29 Diagonal spreads.*

<!-- source:block 74de1d0069e6e980 -->

![原书图表](assets/ch11/f0196-02.jpg)

<!-- source:block 4b5bc4bc8774df0c -->

> [!quote]- English 130
> Even though there are many different volatility spreads, traders tend to classify spreads in terms of their basic volatility characteristics. While some volatility spreads may prefer movement in one direction rather than the other, a trader who initiates a volatility spread is concerned primarily with the magnitude of movement in the underlying contract and only secondarily with the direction of movement. Therefore, all volatility spreads tend to be approximately delta neutral. If a trader has a large positive or negative delta such that directional considerations become more important than volatility considerations, the position can no longer be considered a volatility spread.

尽管存在许多不同的波动率价差，但交易员倾向于根据其基本波动率特征对价差进行分类。虽然一些波动率价差可能更喜欢一个方向而不是另一个方向的移动，但发起波动率价差的交易员主要关心标的合约的移动幅度，其次才关心移动方向。因此，所有波动率价差往往大致为Delta中性。如果交易者有很大的正或负的Delta，使得方向性考虑变得比波动率考虑更重要，则该头寸不能再被视为波动率价差。

<!-- source:block c039d94688f9f741 -->

> [!quote]- English 131
> All spreads that are helped by movement in the underlying market have a positive gamma. All spreads that are hurt by movement in the underlying market have a negative gamma. A trader who has a positive gamma position is said to be *long premium* and is hoping for a volatile market with large moves in the underlying contract. A trader who has a negative gamma is said to be *short premium* and is hoping for a quiet market with only small moves in the underlying market.

所有受标的市场变动影响的价差都具有正的Gamma。所有因标的市场变动而受到损害的价差都具有负Gamma。持有正Gamma头寸的交易员据说是多头溢价，并希望市场波动较大，标的合约波动较大。具有负Gamma的交易者被认为是空头溢价，并希望市场平静，标的市场只有小幅波动。

<!-- source:block 3ba1e524085db497 -->

> [!quote]- English 132
> Because the effect of market movement and the effect of time decay always work in opposite directions, any spread with a positive gamma will necessarily have a negative theta, and any spread with a negative gamma will necessarily have a positive theta. If market movement helps, the passage of time hurts, and if market movement hurts, the passage of time helps. An option trader cannot have it both ways.

由于市场运动的影响和时间衰变的影响总是朝着相反的方向发挥作用，因此任何具有正Gamma的价差都必然具有负的Theta，而任何具有负Gamma的价差也必然具有正的Theta。如果市场运动有所帮助，时间的流逝就会受到伤害;如果市场运动有所伤害，时间的流逝就会有所帮助。期权交易者不能两全其美。

<!-- source:block ab39900f8929be11 -->

> [!quote]- English 133
> Finally, spreads that are helped by rising volatility have a positive vega. Spreads that are helped by falling volatility have a negative vega. In theory, the vega refers to the sensitivity of a theoretical value to a change in the volatility of the underlying contract over the life of the option. In practice, however, traders associate the vega with the sensitivity of an option’s price to a change in implied volatility. Spreads with a positive vega will be helped by any increase in implied volatility and hurt by any decline; spreads with a negative vega will be helped by any decline in implied volatility and hurt by any increase. The delta, gamma, theta, and vega characteristics of the primary types of volatility spreads are summarized in Figure 11-30.

最后，受波动率上升影响的价差具有正的Vega。受到波动率下降帮助的价差具有负的Vega。理论上，Vega是指理论价值对期权有效期内标的合约波动率变化的敏感性。然而，在实践中，交易员将Vega与期权价格对隐含波动率变化的敏感性联系在一起。隐含波动率的任何增加都会帮助具有正Vega的价差，但隐含波动率的任何下降都会受到损害;隐含波动率的任何下降都会帮助具有负Vega的价差，但隐含波动率的任何增加都会受到损害。图11-30总结了主要波动率价差类型的Delta、Gamma、Theta和Vega特征。

<!-- source:block ed3370c3e713f8c8 -->

*图11-30常见波动率价差摘要。 / Figure 11-30 Summary of common volatility spreads.*

<!-- source:block d5687133d1aaffbe -->

![原书图表](assets/ch11/f0198-01.jpg)

<!-- source:block 8db40b416ace60c3 -->

> [!quote]- English 135
> Because volatility spreads tend to be delta neutral and the theta and gamma are always of opposite sign, we can place volatility spreads into one of four categories depending on the effect of movement in the underlying contract (positive or negative gamma) and the effect of changes in implied volatility (positive or negative vega):

由于波动率价差往往是Delta中性的，并且Theta和Gamma总是相反的符号，因此我们可以根据标的合约变动的影响（正或负Gamma）和隐含波动率变化的影响（正或负Vega）将波动率价差分为四种类型之一：

<!-- source:block cd9cbf4bf9b7e90f -->

![原书图表](assets/ch11/f0197-01.jpg)

<!-- source:block 0caa2927b08f1779 -->

> [!quote]- English 136
> Of course, within each of these categories, some spreads will have larger gamma or vega values and some spreads will have smaller values. Of these, straddles and strangles tend to have the largest gamma and vega values and therefore the greatest risk. They will result in the greatest profit when the trader is correct in his assessment of market conditions, but they will result in the greatest loss when the trader is wrong. Butterflies and condors are at the other end of the spectrum. These spreads yield smaller profits when the trader is right but also result in smaller losses when the trader is wrong. Ratio spreads and Christmas trees fall somewhere in between.

当然，在这些类别中，一些价差的Gamma或Vega值较大，而一些价差的值较小。其中，跨式和宽跨式往往具有最大的Gamma和Vega值，因此风险最大。当交易者对市场状况的评估正确时，它们将带来最大的利润，但当交易者对市场状况的评估错误时，它们将带来最大的损失。蝶式价差和鹰式价差处于光谱的另一端。当交易者正确时，这些价差产生的利润较小，但当交易者错误时，这些价差也会产生较小的损失。比率蔓延，圣诞树落在两者之间。

<!-- source:block 33a53d48b455d584 -->

> [!quote]- English 137
> Volatility spreads can be further distinguished by their limited or unlimited risk-reward characteristics, both on the upside and on the downside. These characteristics are also summarized in Figure 11-30.

波动率价差可以通过其有限或无限的风险回报特征进一步区分，无论是在上行还是下行。图11-30也总结了这些特征。

<!-- source:block b5c835fd8593c4c6 -->

> [!quote]- English 138
> Figure 11-31 is an evaluation table with the theoretical value, delta, gamma, theta, vega, and rho of several different options. Following this table are examples of volatility spreads of the types discussed in this chapter, along with their total delta, gamma, theta, vega, and rho. (Although the examples in Figure 11-31 assume that the underlying is stock, except for the rho, the characteristics of each type of spread will tend to be the same for options on futures.) The reader will see that each spread does indeed have the positive or negative sensitivities summarized in Figure 11-30. Note also that a volatility spread need not be exactly delta neutral. (Indeed, as we saw in Chapter 7, no trader can say with absolute certainty whether a position is really delta neutral.) In practice, a volatility spread should have a delta that is small enough that the directional considerations are less important than the volatility considerations. This is often a subjective judgment.

图11-31是一个评估表，其中包含了几个不同期权的理论值、Delta、Gamma、Theta、Vega和Rho。下表是本章讨论的波动率价差类型的例子，以及它们的总Delta、Gamma、Theta、Vega和Rho。（尽管图11-31中的例子假设标的是股票，但除了ρ之外，期货期权的每种价差特征都是相同的。）读者可以看到，每一个价差都有正或负的灵敏度，如图11-30所示。另请注意，波动率价差不一定完全是Delta中性的。（事实上，正如我们在第7章中看到的那样，没有交易员能够绝对确定地说某个头寸是否真的是Delta中性。）在实践中，波动率价差的Delta应该足够小，以便方向性考虑不如波动率考虑重要。这往往是一种主观判断。

<!-- source:block 962b654bcff4a2cf -->

*图11-31常见波动率价差示例。 / Figure 11-31 Examples of common volatility spreads.*

<!-- source:block eb972e2c35061857 -->

![原书图表](assets/ch11/f0200-01.jpg)

<!-- source:block e0c227751b1db045 -->

> [!quote]- English 140
> Also included in Figure 11-31 is the theoretical value of each spread. This is simply the cash flow that results if each spread is executed at theoretical value. Purchases of options result in a cash debit (indicated with a negative sign), and sales represent a cash credit (indicated with a positive sign). In common terminology, a trader is said to be long the spread if it results in a cash debit and short the spread if it results in a cash credit.

图 11-31 还列出了每种价差的理论价值，即各价差按理论价值成交时产生的现金流。买入期权产生 `cash debit`（以负号表示），卖出期权产生 `cash credit`（以正号表示）。按市场惯例，产生 `cash debit` 的价差称为多头价差，产生 `cash credit` 的价差称为空头价差。

<!-- source:block 691e6e7da96231d5 -->

> [!quote]- English 141
> Note that no price is given for any of the option contracts in Figure 11-31, and therefore, no theoretical edge can be calculated for any of the spreads. The prices at which a spread is executed may be good or bad, resulting in a positive or negative theoretical edge. But, once the spread has been established, the market conditions that will help or hurt the spread are determined by its characteristics, not by the initial prices. Like all traders, an option trader must not let his previous trading activity affect his current judgment. A trader’s primary concern should not be what happened yesterday but what can be done today to make the most of the current situation, whether attempting to maximize a potential profit or minimize a potential loss.

请注意，图11-31中的任何期权合约都没有给出价格，因此，无法计算任何价差的理论优势。行权价差的价格可能好坏，从而导致理论优势正或负。但是，一旦价差确定，有助于或损害价差的市场条件就取决于其特征，而不是取决于初始价格。与所有交易者一样，期权交易者不得让他之前的交易活动影响他当前的判断。交易者的主要担忧不应该是昨天发生的事情，而应该是今天可以做些什么来充分利用当前情况，无论是试图最大限度地提高潜在利润还是最大限度地减少潜在损失。

<!-- source:block 097bcc4b3590ac7f -->

## 选择合适的策略 / Choosing an Appropriate Strategy

<!-- source:block b4ff2d7ef898ab8a -->

> [!quote]- English 142
> With so many spreads available, how can we decide which type of spread is best? First and foremost, we will want to choose spreads that have a positive theoretical edge to ensure that if we are right about market conditions, we have a reasonable expectation of showing a profit. Ideally, we want to construct a spread by purchasing options that are underpriced (too cheap) and selling options that are overpriced (too expensive). If we can do this, the resulting spread, whatever its type, will always have a positive theoretical edge.

有如此多的价差，我们如何决定哪种类型的价差是最好的？首先，我们希望选择具有积极理论优势的价差，以确保如果我们对市场状况的判断正确，我们就有合理的利润预期。理想情况下，我们希望通过购买定价过低（太便宜）的期权并出售定价过高（太贵）的期权来构建价差。如果我们能做到这一点，那么由此产生的价差，无论其类型如何，都将始终具有积极的理论优势。

<!-- source:block e920e1d14ba7d210 -->

> [!quote]- English 143
> More often, however, our opinion about volatility will result in all options appearing either overpriced or underpriced. When this happens, it will be impossible to both buy and sell options at advantageous prices. Such a market can be easily identified by comparing our volatility estimate with the implied volatility in the option marketplace. If implied volatility is lower than the volatility estimate, options will be underpriced. If implied volatility is higher than our estimate, options will be overpriced. This leads to the following principle:

然而，更常见的情况是，我们对波动率的看法会导致所有期权显得定价过高或定价过低。当这种情况发生时，就不可能以有利的价格买卖期权。通过将我们的波动率估计与期权市场的隐含波动率进行比较，可以轻松识别这样的市场。如果隐含波动率低于波动率估计，期权将被低估。如果隐含波动率高于我们的估计，期权就会被高估。这导致了以下原则：

<!-- source:block f9370ad87ca3d939 -->

> [!quote]- English 144
> *If implied volatility is low, such that options generally appear underpriced, look for spreads with a positive vega. If implied volatility is high, such that options generally appear overpriced, look for spreads with a negative vega*.

如果隐含波动率较低，使得期权通常显得定价过低，请寻找具有正Vega的价差。如果隐含波动率很高，使得期权通常显得定价过高，请寻找具有负Vega的价差。

<!-- source:block 08e83ff6ee1fdbfd -->

> [!quote]- English 145
> The theoretical values and deltas in Figure 11-31 have been reproduced in Figures 11-32 and 11-33, but now prices have been included, reflecting implied volatilities that differ from the volatility input of 20 percent. The prices in Figure 11-32 reflect an implied volatility of 17 percent. In this case, only spreads with a positive vega will have a positive theoretical edge:

图11-31中的理论值和Delta已在图11-32和11-33中再现，但现在价格已被包括在内，反映了与20%的波动率输入不同的隐含波动率。图11-32中的价格反映了17%的隐含波动率。在这种情况下，只有具有正Vega的价差才会具有正的理论优势：

<!-- source:block 4599503a7c516be6 -->

> [!quote]- English 146
> Long straddles and strangles

长长的跨式和宽跨式

<!-- source:block 848d105d597051f4 -->

> [!quote]- English 147
> Short butterflies and condors

空头蝶式价差和秃鹰

<!-- source:block abfba94401925698 -->

> [!quote]- English 148
> Ratio spreads—long more than short (including short Christmas trees)

比率价差——多头合约数大于空头合约数（包括空头圣诞树价差）

<!-- source:block 403d2cc6cb6af904 -->

> [!quote]- English 149
> Long calendar spreads

漫长的日历价差

<!-- source:block 2a31bfd6e862594f -->

*图11-32 / Figure 11-32*

<!-- source:block e99006e0865eade8 -->

![原书图表](assets/ch11/f0205-01.jpg)

<!-- source:block 461520d82ac3e314 -->

*图11-33 / Figure 11-33*

<!-- source:block 0ec5f85b442b4fd6 -->

![原书图表](assets/ch11/f0205-02.jpg)

<!-- source:block 41166213fbe883e9 -->

![原书图表](assets/ch11/f0206-01.jpg)

<!-- source:block be951d7b07d296ba -->

![原书图表](assets/ch11/f0206-02.jpg)

<!-- source:block e3df5712e16025d9 -->

![原书图表](assets/ch11/f0207-01.jpg)

<!-- source:block 9828b498403ccb88 -->

![原书图表](assets/ch11/f0207-02.jpg)

<!-- source:block a8c4572cde8c43a5 -->

![原书图表](assets/ch11/f0208-01.jpg)

<!-- source:block 8d42ea0cacaaa53b -->

![原书图表](assets/ch11/f0209-01.jpg)

<!-- source:block abf979ea69d53ea8 -->

> [!quote]- English 152
> The prices in Figure 11-33 reflect an implied volatility of 23 percent. Now only spreads with a negative vega will have a positive theoretical edge:

图11-33中的价格反映了23%的隐含波动率。现在只有负Vega的价差才会具有正的理论优势：

<!-- source:block 223bfa0d05a88360 -->

> [!quote]- English 153
> Short straddles and strangles

短跨和宽跨式

<!-- source:block a0bc41308e74d2fe -->

> [!quote]- English 154
> Long butterflies and condors

多头蝶式价差和秃鹰

<!-- source:block becf41dee3c2247f -->

> [!quote]- English 155
> Ratio spreads—short more than long (including long Christmas trees)

比率价差——空头合约数多于多头合约数（包括多头圣诞树价差）

<!-- source:block 277abb27aa5d3f8e -->

> [!quote]- English 156
> Short calendar spreads

短期日历价差

<!-- source:block 6378fc492f81a71b -->

> [!quote]- English 157
> It may seem that if one encounters a market where all options are either underpriced or overpriced, the sensible strategies are either long straddles and strangles or short straddles and strangles. Such strategies will enable a trader to take a position with a positive theoretical edge on both sides of the spread. Straddles and strangles are certainly possible strategies when all options are too cheap or too expensive. But we will see in Chapter 13 that straddles and strangles, while often having a large positive theoretical edge, can also be among the riskiest of all strategies. For this reason, a trader will often want to consider other spreads such as ratio spreads and butterflies, even if such spreads entail buying some overpriced options or selling some underpriced options.

看起来，如果一个人遇到一个所有期权要么定价过低要么定价过高的市场，明智的策略要么是多头跨式和宽跨式，要么是空头跨式和宽跨式。这样的策略将使交易者能够在价差的两边都有积极的理论优势。当所有选择都太便宜或太昂贵时，跨式和宽跨式当然是可能的策略。我们将在第13章看到，跨式式和宽跨式式策略虽然经常具有很大的积极理论优势，但也可能是所有策略中风险最大的策略之一。出于这个原因，交易员通常会考虑其他价差，例如比率价差和蝶式价差，即使此类价差需要购买一些定价过高的期权或出售一些定价过低的期权。

<!-- source:block f0621dec3fb2d994 -->

> [!quote]- English 158
> An important assumption in traditional theoretical pricing models is that volatility is constant over the life of an option. The volatility input into the model is assumed to be the one volatility that best describes price fluctuations in the underlying instrument over the life of the option. When all options expire at the same time, it is this one volatility that will, in theory, determine whether a spread is profitable or unprofitable. But a trader may also believe that implied volatility will rise or fall over time.

传统理论定价模型中的一个重要假设是，波动率在期权的有效期内是恒定的。假设模型中的波动率输入是最能描述期权有效期内标的工具价格波动的一种波动率。当所有期权同时到期时，理论上，正是这种波动率将决定价差是有利可图还是无利可图。但交易员也可能相信隐含波动率会随着时间的推移而上升或下降。

<!-- source:block 3ce73e1358953af1 -->

> [!quote]- English 159
> Because calendar spreads are particularly sensitive to changes in implied volatility, rising or falling implied volatility will often affect the profitability of calendar spreads. Consequently, we can add this corollary to the other spread guidelines:

由于日历价差对隐含波动率的变化特别敏感，隐含波动率的上升或下降往往会影响日历价差的盈利能力。因此，我们可以将这个推论添加到其他价差准则中：

<!-- source:block 5e5e12a93616bc07 -->

> [!quote]- English 160
> *Long calendar spreads are likely to be profitable when implied volatility is low but is expected to rise; short calendar spreads are likely to be profitable when implied volatility is high but is expected to fall*.

当隐含波动率较低但预计会上升时，长日历价差可能会盈利;当隐含波动率较高但预计会下降时，短日历价差可能会盈利。

<!-- source:block a350636ae2e2d0a3 -->

> [!quote]- English 161
> These are only general guidelines, and an experienced trader may decide to violate them if he has reason to believe that the implied volatility will not correlate with the volatility of the underlying contract. A long calendar spread might still be desirable in a high-implied-volatility market, but the trader must make a prediction of how implied volatility might change with changes in realized volatility. If the market stagnates, with no movement in the underlying contract, but the trader feels that implied volatility will remain high, a long calendar spread is a sensible strategy. The short-term option will decay, while the long-term option will retain its value. In the same way, a short calendar spread might still be desirable in a low-implied-volatility market if the trader feels that the underlying contract is likely to make a large move with no commensurate increase in implied volatility.

这些只是一般指导方针，如果经验丰富的交易员有理由相信隐含波动率与标的合约的波动率无关，他可能会决定违反这些指导方针。在高隐含波动率市场中，较长的日历价差可能仍然是可取的，但交易员必须预测隐含波动率可能如何随着已实现波动率的变化而变化。如果市场停滞，标的合约没有变动，但交易员认为隐含波动率将保持在高位，那么长的日历价差是一个明智的策略。短期期权将会衰退，而长期期权将保留其价值。同样，如果交易员认为标的合约可能会大幅变动而隐含波动率没有相应增加，那么在低隐含波动率市场中，短期日历价差可能仍然是可取的。

<!-- source:block 4587732aa3ff7b6b -->

## 调整 / Adjustments

<!-- source:block 1cf847a93c12baeb -->

> [!quote]- English 162
> A volatility spread may be delta neutral initially, but the delta of the position will change as market conditions change—as the price of the underlying contract rises or falls, as volatility changes, and as time passes. A spread that is delta neutral today is unlikely to be delta neutral tomorrow. The use of a theoretical pricing model requires a trader to continuously maintain a delta-neutral position throughout the life of the spread. Continuous adjustments are neither possible nor practical in the real world of trading, so when a trader initiates a spread, he ought to give some thought as to how he will adjust the position. There are essentially four possibilities:

波动率价差最初可能是Delta中性的，但头寸的Delta将随着市场条件的变化而变化——随着标的合约价格的上涨或下跌、波动率的变化以及随着时间的推移。今天Delta中性的价差明天不太可能成为Delta中性的。理论定价模型的使用要求交易员在整个价差生命周期内持续保持Delta中性头寸。在现实的交易世界中，连续调整既不可能也不切实际，因此当交易者发起价差时，他应该考虑如何调整头寸。本质上有四种可能性：

<!-- source:block ad16839bf69344f1 -->

> [!quote]- English 163
> 1. *Adjust at regular intervals*. In theory, the adjustment process is assumed to be continuous because volatility is assumed to be a continuous measure of the speed of the market. In practice, however, volatility is measured over regular time intervals, so a reasonable approach is to adjust a position at similar regular intervals. If a trader’s volatility estimate is based on daily price changes, the trader might adjust daily. If the estimate is based on weekly price changes, he might adjust weekly. By doing this, the trader is making the best attempt to emulate the assumptions built into the theoretical pricing model.

1.定期调整。理论上，调整过程被假设是连续的，因为波动率被假设是市场速度的连续衡量标准。然而，在实践中，波动率是在固定的时间间隔内衡量的，因此合理的方法是以类似的固定时间间隔调整头寸。如果交易者的波动率估计基于每日价格变化，则交易者可能会每日调整。如果估计是基于每周的价格变化，他可能会每周调整。通过这样做，交易员正在尽最大努力模仿理论定价模型中的假设。

<!-- source:block 4a925bcbd3d85f53 -->

> [!quote]- English 164
> 2. *Adjust when the position becomes a predetermined number of deltas long or short*. Very few traders insist on being delta neutral all the time. Most traders accept that this is not a realistic approach both because a continuous adjustment process is physically impossible and because no one can be certain that all the assumptions and inputs in a theoretical pricing model, from which the delta is calculated, are correct. Even if one could be certain that all delta calculations were accurate, a trader might still be willing to take on some directional risk. But a trader ought to know just how much directional risk he is willing to accept. If he wants to pursue delta-neutral strategies but believes that he can comfortably live with a position that is up to 500 deltas long or short, then he can adjust the position any time his delta position reaches this limit. Unlike the trader who adjusts at regular intervals, a trader who adjusts based on a fixed number of deltas cannot be sure how often he will need to adjust his position. In some cases, he may have to adjust very frequently; in other cases, he may go for long periods of time without adjusting.

2.当头寸变成预定数量的长或短Delta时进行调整。很少有交易者坚持始终保持Delta中性。大多数交易员都承认这不是一个现实的方法，因为连续的调整过程在物理上是不可能的，而且没有人可以确定计算Delta的理论定价模型中的所有假设和输入都是正确的。即使可以确定所有Delta计算都是准确的，交易员可能仍然愿意承担一些方向性风险。但交易者应该知道他愿意接受多少方向性风险。如果他想追求Delta中性策略，但相信自己可以轻松接受高达500个Delta多头或空头的头寸，那么他可以随时调整头寸，当Delta头寸达到此限制时。与定期调整的交易者不同，根据固定数量的Delta进行调整的交易者无法确定他需要调整头寸的频率。在某些情况下，他可能不得不频繁地调整;在其他情况下，他可能会很长一段时间不调整。

<!-- source:block 0cfcbd66eaacb9a3 -->

> [!quote]- English 165
> The number of deltas, either long or short, that a trader is willing to accept without adjusting depends on many factors—the typical size of the trader’s positions, his capitalization, and his trading experience. A new independent trader may find that he is uncomfortable with a position that is only 200 deltas long or short. A large trading firm may consider a position that is several thousand deltas long or short as being approximately delta neutral.

交易者愿意接受而不进行调整的Delta数量（无论是多头还是空头）取决于许多因素——交易者头寸的典型规模、他的资本金和他的交易经验。一位新的独立交易者可能会发现他对只有200个Delta的多头或空头头寸感到不舒服。大型贸易公司可能会将数千个Delta多头或空头的头寸视为大致Delta中性。

<!-- source:block a2d22ac93dfebe85 -->

> [!quote]- English 166
> 3. *Adjust by feel*. This suggestion is not made facetiously. Some traders have good market feel. They can sense when the market is about to move in one direction or another. If a trader has this ability, there is no reason why he shouldn’t make use of it. Suppose that the underlying market is at 50.00 and a trader is delta neutral with a gamma of –200. If the market falls to 48.00, the trader can estimate that he is approximately 400 deltas long. If 400 deltas is the limit of the risk he is willing to accept, he might decide to adjust at this point. If, however, he is also aware that 48.00 represents strong support for the market, he might choose not to adjust under the assumption that the market is likely to rebound from the support level. If he is right, he will have avoided an unprofitable adjustment. Of course, if he is wrong and the market continues downward through the support level, he will regret not having adjusted. But if the trader is right more often than not, there is no reason why he shouldn’t take advantage of this skill.

3. **凭盘感调整。** 这并非戏言。有些交易员具有良好的市场感觉，能够察觉市场是否即将向某一方向移动；若交易员确有这种能力，就没有理由不加以利用。假设标的市场位于 50.00，交易员的头寸为 Delta 中性、Gamma 为 $-200$。若市场跌至 48.00，他可以估计头寸约为 400 Delta 多头。若 400 Delta 正是其可接受的风险上限，他可能决定此时调整。不过，若他同时认为 48.00 是强支撑位，也可能基于市场大概率从支撑位反弹的判断而暂不调整。判断正确时，他就避免了一次不利调整；判断错误、市场继续跌破支撑位时，他则会后悔没有调整。只要正确判断多于错误判断，就没有理由不利用这种能力。

<!-- source:block 155a0cc265463dca -->

> [!quote]- English 167
> 4. *Don’t adjust at all*. This is really an extension of the second possibility, adjusting by the number of deltas. A trader who does not adjust at all is willing to accept a directional risk equal to the maximum number of deltas that the position can take on. If the trader sells five straddles, the position can take on a maximum delta of ±500. The appeal of this approach is that it eliminates all subsequent transaction costs. But, if the position takes on a large delta, the directional considerations may become more important than the volatility considerations. If the position was initiated because of an opinion about volatility, does it make sense for a trader to subsequently change to an opinion about direction? Usually not. If the trader does not want to adjust the position but he also does not want directional considerations to dominate, the only choice left is to close out the position. If the trader decides not to adjust, when he initiates the position, he must decide under what conditions he will be willing to hold the position and under what conditions he will close the position.

4。根本不要调整。这实际上是第二种可能性的扩展，通过Delta的数量进行调整。根本不进行调整的交易者愿意接受与头寸可以承担的最大Delta数量相等的方向风险。 如果交易者出售五个跨式，该头寸的最大Delta为±500。这种方法的吸引力在于它消除了所有后续交易成本。 但是，如果头寸出现较大的Delta，方向性考虑可能会变得比波动率考虑更重要。如果头寸是因为对波动率的看法而启动的，那么交易员随后改变对方向的看法是否有意义？ 通常不会。如果交易者不想调整头寸，但也不想以方向性考虑为主，那么剩下的唯一选择就是平仓。 如果交易者决定不调整，当他开始头寸时，他必须决定在什么条件下他愿意持有头寸，在什么条件下他将关闭头寸。

<!-- source:block 1ff1aca54b602a4d -->

## 提交价差委托 / Submitting a Spread Order

<!-- source:block ae868f42d0d119da -->

> [!quote]- English 168
> We noted in Chapter 10 that a spread order can often be executed all at one time and at one single price. This is particularly common in option markets, where spreads are quoted with a single bid price and a single offer price regardless of the complexity of the spread. Suppose that a trader is interested in buying a straddle and receives a quote from a market maker of 6.25/6.75. If the trader wants to sell the straddle, he will have to do so at a price of 6.25 (the bid price); if he wants to buy the straddle, he will have to pay 6.75 (the ask price). If the trader decides that he is willing to pay 6.75, neither he nor the market maker really cares whether the trader pays 3.75 for the call and 3.00 for the put or 2.00 for the call and 4.75 for the put or some other combination of call and put prices. The only consideration is that the prices of the call and put taken together add up to 6.75.

我们在第10章中指出，价差订单通常可以以一个价格一次性执行。这在期权市场中尤其常见，无论价差的复杂性如何，价差都以单一买入价和单一卖出价报价。假设一名交易员有兴趣购买跨式，并收到做市商6.25/6.75的报价。如果交易者想要出售跨式交易，他必须以6.25（买入价）的价格出售;如果他想购买跨式交易，他必须支付6.75（卖出价）。如果交易者决定愿意支付6.75，那么他和做市商都不真正关心交易者是为看涨期权支付3.75，为看跌期权支付3.00，还是为看涨期权支付2.00，为看跌期权支付4.75，还是看涨期权和看跌期权价格的其他组合。唯一考虑的是看涨和看跌的价格加起来为6.75。

<!-- source:block 415c34e7e1a6b221 -->

> [!quote]- English 169
> A market maker will always endeavor to give one bid price and one ask price for an entire spread. If the spread is a common type, such as a straddle, strangle, butterfly, or calendar spread, a bid and ask can usually be given very quickly. But market makers are only human. If a spread is very complex, involving several different options in unusual ratios, it may take a market maker several minutes to calculate the value of the spread. Regardless of the complexity of a spread, however, the market maker will make an effort to give his best two-sided (bid and ask) market.

做市商将始终努力为整个价差给出一个买入价和一个卖出价。如果价差是常见类型，例如跨式、宽跨式、蝶式价差或日历价差，则通常可以很快给出竞价。但做市商只是人。如果价差非常复杂，涉及几种比例不寻常的不同期权，则做市商可能需要几分钟时间才能计算价差的价值。然而，无论价差的复杂性如何，做市商都会努力提供最佳的双边（买卖）市场。

<!-- source:block 9028ab3ab15581df -->

> [!quote]- English 170
> Spread orders are common in almost all option markets, whether electronic or open outcry. Depending on the trading platform, an electronic exchange will usually allow traders to submit bids or offers for the most common types of spreads—simple call or put spreads, straddles, strangles, and calendar spreads. More complex spreads—butterflies, Christmas trees, and spreads with unusual ratios—must either be executed piecemeal or submitted to a broker for execution on an open-outcry exchange where an exact description of the spread can be communicated directly to one or more market makers.

价差订单在几乎所有期权市场中都很常见，无论是电子还是公开竞价。根据交易平台的不同，电子交易所通常允许交易员提交最常见类型的价差（简单看涨或看跌价差、跨式、宽跨式和日历价差）的出价或报价。更复杂的价差——蝶式价差、圣诞树和具有异常比率的价差——必须零碎执行或提交给经纪人在公开呼喊交易所执行，在那里价差的准确描述可以直接传达给一个或多个做市商。

<!-- source:block 3d6e74963a3ad4e9 -->

> [!quote]- English 171
> Option spread orders may often be submitted with specific instructions as to how the spread is to be executed. Most commonly, a spread will be submitted as either a market order (an order to be filled at the current market price) or a limit order (an order to be filled only at a specified price). But the spread may also be submitted as a *contingency order* with special execution instructions. The following contingency orders, all of which are defined in Appendix A, are often used in option markets:

期权价差订单通常可能会提交并附有有关如何行权价差的具体说明。最常见的是，价差将作为市场订单（以当前市场价格填写的订单）或限额订单（仅以指定价格填写的订单）提交。但价差也可以作为带有特殊执行指示的应急令提交。以下应急订单（所有这些订单均在附录A中定义）经常用于期权市场：

<!-- source:block a50786f3968d0301 -->

> [!quote]- English 172
> All or none

全部或没有

<!-- source:block ff5f8f4799597697 -->

> [!quote]- English 173
> Fill or kill

填充或杀死

<!-- source:block d4b2b5149b707a31 -->

> [!quote]- English 174
> Immediate or cancel

立即或取消

<!-- source:block 2a54f498c6379dc1 -->

> [!quote]- English 175
> Market if touched

如果触及市场

<!-- source:block d0b9b275334f857d -->

> [!quote]- English 176
> Market on close

市场收盘

<!-- source:block b2b9b144ee8866f1 -->

> [!quote]- English 177
> Not held

并非持

<!-- source:block fe0acd67ddf02781 -->

> [!quote]- English 178
> One cancels the other

一个抵消另一个

<!-- source:block fc9b05f6468c9d05 -->

> [!quote]- English 179
> Stop limit order

停止限制令

<!-- source:block d1e344323ae2698a -->

> [!quote]- English 180
> Stop loss order

止损单

<!-- source:block 26f64e65f8731fef -->

> [!quote]- English 181
> A broker executing a spread order is responsible for adhering to any special instructions that accompany the order. Unless a trader is fully knowledgeable about market conditions or has a great deal of confidence in the broker who will be executing the order, it may be wise to submit specific instructions with the order as to how it is to be executed. Additionally, when one considers all the information that must be communicated with a spread order (i.e., the quantity, the expiration months, the exercise prices, the type of option, and whether the order is a buy or sell), it is easy to see how incorrect information might inadvertently be transmitted with the order. For this reason, it is also wise to double-check all orders before submitting them for execution. Option trading can be difficult enough without the additional problems of miscommunication.

行权价差订单的经纪商负责遵守订单附带的任何特殊指示。除非交易员完全了解市场状况或对将执行订单的经纪商非常有信心，否则明智的做法是与订单一起提交有关如何执行的具体指示。此外，当考虑必须与价差订单沟通的所有信息时（即，数量、到期月份、行权价、期权类型以及订单是买入还是卖出），很容易看出错误的信息可能如何无意中与订单一起传输。因此，在提交所有订单以供执行之前仔细检查也是明智的。如果没有沟通不畅的额外问题，期权交易可能已经够困难了。

<!-- source:block 6f8672742afc7c18 -->

> [!note] Footnote 182
> <sup>1</sup> This is not necessarily true for butterflies consisting of American options, where early exercise is a possibility. A sure profit would exist only if one could be certain of carrying the position to expiration.

[^ovp11-1]: 对于由美式期权组成的蝶式价差来说，这不一定是正确的，因为提前行权是可能的。只有当一个人能够确定将头寸持有至到期时，确定的利润才会存在。

<!-- source:block cdb24b7ed6633735 -->

> [!note] Footnote 183
> <sup>2</sup> Butterflies and condors fall under the general category of strategies known as wingspreads.

[^ovp11-2]: 蝶式价差和鹰式价差属于称为翼展的一般策略类别。

<!-- source:block daa1128558802082 -->

> [!note] Footnote 184
> <sup>3</sup> The terms backspread and frontspread date from the early days of option trading in the United States but are now used infrequently except by some older traders. Most traders simply refer to these strategies as ratio spreads, specifying whether more options are purchased or sold and the ratio of long to short options.

[^ovp11-3]: 价差和前期价差这一术语可以追溯到美国期权交易的早期，但现在除了一些年长的交易员外，很少使用。大多数交易员只是将这些策略称为比率价差，指定是否购买或出售更多期权以及多头与空头期权的比率。

<!-- source:block 32db5d158541bd57 -->

> [!note] Footnote 185
> <sup>4</sup> The term *ladder* may also refer to a type of exotic option.

[^ovp11-4]: “阶梯”一词也可能指的是一种奇异的期权。

<!-- source:block 7d103fd659de5617 -->

> [!note] Footnote 186
> <sup>5</sup> In the early days of floor trading on option exchanges, expiration months were listed horizontally on the exchange display boards—hence the term *horizontal spread* for strategies consisting of options with different expiration months.

[^ovp11-5]: 在期权交易所场内交易的早期，到期月份在交易所显示板上水平列出-因此术语“水平价差”是指由不同到期月份的期权组成的策略。

<!-- source:block d6660440d303fc82 -->

> [!note] Footnote 187
> <sup>6</sup> To be more exact, at-the-forward options tend to have deltas closest to 50. For this reason, a trader might prefer a calendar spread that consists of at-the-forward options.

[^ovp11-6]: 更准确地说，远期期权的Delta往往接近50。因此，交易者可能更喜欢由远期期权组成的日历价差。

<!-- source:block 016f97a67facff1f -->

> [!note] Footnote 188
> <sup>7</sup> We are making the assumption here that the implied volatility of all expirations is the same. If the implied volatility differs across expiration months, a long time butterfly might in fact result in a credit.

[^ovp11-7]: 我们在这里假设所有折旧的隐含波动率都是相同的。如果隐含波动率在到期月份有所不同，那么长期Butterfly实际上可能会导致 credit。

<!-- source:block 4eafef3c2b641734 -->

> [!note] Footnote 189
> <sup>8</sup> Interest rates can, of course, affect the relative value of different futures months. As noted, we can offset this risk by trading a futures spread along with the futures option calendar spread.

[^ovp11-8]: 当然，利率会影响不同期货月份的相对价值。如前所述，我们可以通过交易期货价差和期货期权日历价差来抵消此风险。

---

[[00-阅读导航|← 返回阅读导航]]

<!-- chapter-nav:start -->
> [!tip] 章节导航（章末）
> [[10-价差策略导论 Introduction to Spreading|← 上一章]] · [[00-阅读导航|全书导航]] · [[12-牛市与熊市价差 Bull and Bear Spreads|下一章 →]]
<!-- chapter-nav:end -->
