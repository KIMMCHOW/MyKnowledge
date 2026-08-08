#!/usr/bin/env python3
"""Extract one EPUB chapter and create an Obsidian bilingual Markdown note."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import time
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter
from decimal import Decimal, InvalidOperation
from pathlib import Path

from tencent_tmt_translate import translate


XHTML_NS = "{http://www.w3.org/1999/xhtml}"
BLOCK_TAGS = {"h1", "h2", "h3", "h4", "p"}
IMAGE_TAGS = {"img", "image"}

# Titles and section headings are navigation-critical and too short for a
# general-purpose translation model to disambiguate reliably. These controlled
# translations are also applied to the EPUB table of contents.
CONTROLLED_TRANSLATIONS = {
    "Preface": "前言",
    "Financial Contracts": "金融合约",
    "Buying and Selling": "买入与卖出",
    "Notional Value of a Forward Contract": "远期合约的名义价值",
    "Settlement Procedures": "结算程序",
    "Market Integrity": "市场健全性",
    "Forward Pricing": "远期定价",
    "Physical Commodities (Grains, Energy Products, Precious Metals, etc.)": "实物商品（谷物、能源产品、贵金属等）",
    "Stock": "股票",
    "Bonds and Notes": "债券与票据",
    "Foreign Currencies": "外币",
    "Stock and Futures Options": "股票期权与期货期权",
    "Arbitrage": "套利",
    "Dividends": "股息",
    "Short Sales": "卖空",
    "Contract Specifications and Option Terminology": "合约规格与期权术语",
    "Contract Specifications": "合约规格",
    "Option Price Components": "期权价格的组成",
    "Expiration Profit and Loss": "到期损益",
    "Parity Graphs": "平价图",
    "Theoretical Pricing Models": "理论定价模型",
    "The Importance of Probability": "概率的重要性",
    "A Simple Approach": "一种简单方法",
    "The Black-Scholes Model": "Black–Scholes 模型",
    "Volatility": "波动率",
    "Random Walks and Normal Distributions": "随机游走与正态分布",
    "Mean and Standard Deviation": "均值与标准差",
    "Forward Price as the Mean of a Distribution": "作为分布均值的远期价格",
    "Volatility as a Standard Deviation": "作为标准差的波动率",
    "Scaling Volatility for Time": "按时间缩放波动率",
    "Volatility and Observed Price Changes": "波动率与观察到的价格变化",
    "A Note on Interest-Rate Products": "关于利率产品的说明",
    "Lognormal Distributions": "对数正态分布",
    "Interpreting Volatility Data": "解读波动率数据",
    "Risk Measurement I": "风险度量（一）",
    "The Delta": "Delta（标的价格敏感度）",
    "The Gamma": "Gamma（Delta 变化率）",
    "The Theta": "Theta（时间敏感度）",
    "The Vega": "Vega（波动率敏感度）",
    "The Rho": "Rho（利率敏感度）",
    "Interpreting the Risk Measures": "解读风险指标",
    "Dynamic Hedging": "动态对冲",
    "Original Hedge": "初始对冲",
    "Risk Measurement II": "风险度量（二）",
    "Delta": "Delta",
    "Theta": "Theta",
    "Vega": "Vega",
    "Gamma": "Gamma",
    "Lambda (Λ)": "Lambda（Λ，杠杆率）",
    "Introduction to Spreading": "价差策略导论",
    "What Is a Spread?": "什么是价差？",
    "Option Spreads": "期权价差",
    "Volatility Spreads": "波动率价差策略",
    "Straddle": "跨式策略",
    "Strangle": "宽跨式策略",
    "Butterfly": "蝶式价差",
    "Condor": "鹰式价差",
    "Ratio Spread": "比率价差",
    "Christmas Tree": "圣诞树价差",
    "Calendar Spread": "日历价差",
    "Time Butterfly": "时间蝶式价差",
    "Effect of Changing Interest Rates and Dividends": "利率与股息变化的影响",
    "Diagonal Spreads": "对角价差",
    "Choosing an Appropriate Strategy": "选择合适的策略",
    "Adjustments": "调整",
    "Submitting a Spread Order": "提交价差委托",
    "Bull and Bear Spreads": "牛市与熊市价差",
    "Naked Positions": "裸头寸",
    "Bull and Bear Ratio Spreads": "牛市与熊市比率价差",
    "Bull and Bear Butterflies and Calendar Spreads": "牛市与熊市蝶式及日历价差",
    "Vertical Spreads": "垂直价差",
    "Risk Considerations": "风险考量",
    "Volatility Risk": "波动率风险",
    "Practical Considerations": "实务考量",
    "How Much Margin for Error?": "应预留多大的误差空间？",
    "Dividends and Interest": "股息与利息",
    "What Is a Good Spread?": "什么是好的价差？",
    "Synthetics": "合成头寸",
    "Synthetic Underlying": "合成标的头寸",
    "Synthetic Options": "合成期权",
    "Using Synthetics in a Spreading Strategy": "在价差策略中使用合成头寸",
    "Iron Butterflies and Iron Condors": "铁蝶式与铁鹰式",
    "Option Arbitrage": "期权套利",
    "Options on Futures": "期货期权",
    "Locked Futures Markets": "涨跌停的期货市场",
    "Options on Stock": "股票期权",
    "Arbitrage Risk": "套利风险",
    "Early Exercise of American Options": "美式期权的提前行权",
    "Arbitrage Boundaries": "套利边界",
    "Early Exercise of Call Options on Stock": "股票看涨期权的提前行权",
    "Early Exercise of Put Options on Stock": "股票看跌期权的提前行权",
    "Impact of Short Stock on Early Exercise": "股票空头对提前行权的影响",
    "Early Exercise of Options on Futures": "期货期权的提前行权",
    "Protective Value and Early Exercise": "保护价值与提前行权",
    "Pricing of American Options": "美式期权定价",
    "Early Exercise Strategies": "提前行权策略",
    "Early Exercise Risk": "提前行权风险",
    "Hedging with Options": "使用期权进行对冲",
    "Protective Calls and Puts": "保护性看涨期权与看跌期权",
    "Covered Writes": "备兑卖出",
    "Collars": "领式策略",
    "Complex Hedging Strategies": "复杂对冲策略",
    "Hedging to Reduce Volatility": "通过对冲降低波动率",
    "Portfolio Insurance": "投资组合保险",
    "n(x) and N(x)": "n(x) 与 N(x)",
    "A Useful Approximation": "一个实用的近似式",
    "Maximum Gamma, Theta, and Vega": "Gamma、Theta 与 Vega 的最大值",
    "Binomial Option Pricing": "二叉树期权定价",
    "A Risk-Neutral World": "风险中性世界",
    "Valuing an Option": "期权估值",
    "Vega and Rho": "Vega 与 Rho",
    "The Values of u and d": "u 与 d 的取值",
    "Gamma Rent": "Gamma 租金",
    "American Options": "美式期权",
    "Volatility Revisited": "再论波动率",
    "Historical Volatility": "历史波动率",
    "Volatility Forecasting": "波动率预测",
    "Implied Volatility as a Predictor of Future Volatility": "以隐含波动率预测未来波动率",
    "Forward Volatility": "远期波动率",
    "Position Analysis": "头寸分析",
    "Some Thoughts on Market Making": "关于做市的一些思考",
    "Stock Splits": "股票拆分",
    "Stock Index Futures and Options": "股票指数期货与期权",
    "What Is an Index?": "什么是指数？",
    "Stock Index Futures": "股票指数期货",
    "Stock Index Options": "股票指数期权",
    "Models and the Real World": "模型与现实世界",
    "Markets Are Frictionless": "市场无摩擦",
    "Interest Rates Are Constant over the Life of an Option": "期权存续期内利率不变",
    "Volatility Is Constant over the Life of the Option": "期权存续期内波动率不变",
    "Trading Is Continuous": "交易是连续的",
    "Expiration Straddles": "到期跨式策略",
    "Volatility Is Independent of the Price of the Underlying Contract": "波动率独立于标的合约价格",
    "Underlying Prices at Expiration Are Lognormally Distributed": "到期时标的价格服从对数正态分布",
    "Skewness and Kurtosis": "偏度与峰度",
    "Volatility Skews": "波动率偏斜",
    "Modeling the Skew": "波动率偏斜建模",
    "Skewed Risk Measures": "偏斜下的风险指标",
    "Shifting the Volatility": "平移波动率",
    "Skewness and Kurtosis Strategies": "偏度与峰度策略",
    "Implied Distributions": "隐含分布",
    "Volatility Contracts": "波动率合约",
    "Realized Volatility Contracts": "已实现波动率合约",
    "Implied Volatility Contracts": "隐含波动率合约",
    "Trading the VIX": "交易 VIX",
    "Replicating a Volatility Contract": "复制波动率合约",
    "Volatility Contract Applications": "波动率合约的应用",
    "Afterword: A Final Thought": "结语：最后的思考",
    "A Glossary of Option Terminology": "A 期权术语表",
    "B Some Useful Math": "B 实用数学",
    "Rate-of-Return Calculations": "收益率计算",
    "Normal Distributions and Standard Deviation": "正态分布与标准差",
    "Index": "索引",
    "Example": "示例",
    "Type": "类型",
    "Underlying": "标的资产",
    "Expiration Date or Expiry": "到期日",
    "Exercise Price or Strike Price": "行权价",
    "Exercise and Assignment": "行权与指派",
    "Settlement into the Physical Underlying": "以实物标的结算",
    "Settlement into a Futures Position": "结算为期货头寸",
    "Settlement into Cash": "现金结算",
    "Exercise Style": "行权方式",
    "In the Money, At the Money, and Out of the Money": "价内、平值与价外",
    "Automatic Exercise": "自动行权",
    "Option Margining": "期权保证金制度",
    "Slope": "斜率",
    "Expected Value": "期望值",
    "Theoretical Value": "理论价值",
    "A Word on Models": "关于模型的补充说明",
    "Exercise Price": "行权价",
    "Time to Expiration": "距到期时间",
    "Underlying Price": "标的价格",
    "Interest Rates": "利率",
    "Realized Volatility": "已实现波动率",
    "Implied Volatility": "隐含波动率",
    "Rate of Change": "变化率",
    "Hedge Ratio": "对冲比率",
    "Theoretical or Equivalent underlying Position": "理论或等价标的头寸",
    "Probability": "概率",
    "Interest Lost on the Option Position": "期权头寸的利息成本",
    "Interest earned on the Stock Position": "股票头寸赚取的利息",
    "Interest on the Adjustments": "调仓产生的利息",
    "Efficiency": "效率",
    "A Question of Style": "风格问题",
    "Liquidity": "流动性",
    "An Approximation for Stock Options": "股票期权的近似计算",
    "Execution Risk": "执行风险",
    "Pin Risk": "钉住风险",
    "Settlement Risk": "结算风险",
    "Interest and Dividend Risk": "利率与股息风险",
    "Boxes": "箱式价差",
    "Rolls": "滚动价差",
    "Time boxes": "时间箱式价差",
    "Using Synthetics in Volatility Spreads": "在波动率价差中使用合成头寸",
    "A Three-Period Example": "三期示例",
    "Binomial Notation": "二叉树符号",
    "Some Volatility Characteristics": "波动率的一些特征",
    "The Term structure of Implied Volatility": "隐含波动率期限结构",
    "Calculating an Index": "指数计算",
    "The Index Divisor": "指数除数",
    "Total-Return Indexes": "总回报指数",
    "Impact of Individual Stock price Changes on an Index": "个股价格变化对指数的影响",
    "Volume-Weighted Average Price": "成交量加权平均价（VWAP）",
    "Index Arbitrage": "指数套利",
    "Replicating an Index": "复制指数",
    "Bias in the Futures Market": "期货市场中的偏差",
    "Stock Index options": "股票指数期权",
    "Options on Stock Index Futures": "股票指数期货期权",
    "Options on a Cash Index": "现货指数期权",
    "Some VIX Characteristics": "VIX 的一些特征",
    "VIX Futures": "VIX 期货",
    "VIX Options": "VIX 期权",
    "A Final Thought": "最后的思考",
    "Glossary of Option Terminology": "期权术语表",
    "Some Useful Math": "实用数学",
    "About the Author": "关于作者",
    "You exercise one January 110 call on stock.": "你对一份 1 月到期、行权价为 110 的股票看涨期权行权。",
    "You are assigned on six April 40 calls on stock.": "你被指派履行六份 4 月到期、行权价为 40 的股票看涨期权。",
    "You exercise two July 60 puts on stock.": "你对两份 7 月到期、行权价为 60 的股票看跌期权行权。",
    "You are assigned on three October 95 puts on stock.": "你被指派履行三份 10 月到期、行权价为 95 的股票看跌期权。",
    "You exercise one February 80 call.": "你对一份 2 月到期、行权价为 80 的看涨期权行权。",
    "You are assigned on six May 75 calls.": "你被指派履行六份 5 月到期、行权价为 75 的看涨期权。",
    "You exercise four August 100 puts.": "你对四份 8 月到期、行权价为 100 的看跌期权行权。",
    "You are assigned on two November 95 puts.": "你被指派履行两份 11 月到期、行权价为 95 的看跌期权。",
    "You exercise three March 250 calls.": "你对三份 3 月到期、行权价为 250 的看涨期权行权。",
    "You are assigned on seven June 275 calls.": "你被指派履行七份 6 月到期、行权价为 275 的看涨期权。",
    "You exercise two September 320 puts.": "你对两份 9 月到期、行权价为 320 的看跌期权行权。",
    "You are assigned on four December 340 puts.": "你被指派履行四份 12 月到期、行权价为 340 的看跌期权。",
    "Long a call": "多头看涨期权",
    "Short a call": "空头看涨期权",
    "Long a put": "多头看跌期权",
    "Short a put": "空头看跌期权",
    "Long an underlying contract": "标的合约多头",
    "Short an underlying contract": "标的合约空头",
    "Long a deeply in-the-money call": "多头深度价内看涨期权",
    "Short a deeply in-the-money put": "空头深度价内看跌期权",
    "Note the difference between an option and a futures contract. A futures contract requires delivery at a fixed price. The buyer and seller of a futures contract both have clearly defined obligations that they must meet. The seller must make delivery, and the buyer must take delivery. The buyer of an option, however, has a choice. He can choose to take delivery (a call) or make delivery (a put). If the buyer of an option chooses to either make or take delivery, the seller of the option is obligated to take the other side. In option trading, all rights lie with the buyer and all obligations with the seller.": "请注意期权与期货合约的区别。期货合约要求按固定价格交割；买卖双方都负有明确的履约义务：卖方必须交付标的，买方必须接受标的。期权买方则拥有选择权：看涨期权买方可选择接受标的，看跌期权买方可选择交付标的。期权买方一旦选择交付或接受标的，期权卖方必须承担对应的另一边义务。在期权交易中，权利归买方，义务归卖方。",
    "Thus far we have made no mention of the prices at which any of the contracts are traded. The prices will of course be important when deciding whether to create a synthetic position, and we will eventually address this question. But for the present we are considering only the characteristics of a synthetic position, and these are independent of the prices at which the contracts are traded. In Figures 14-2a and 14-3a the underlying position was taken at a price different than the exercise price. What gives the position its characteristics is not the prices of the contracts, but the slopes of the contracts. And the combined slopes are equivalent to a long call (Figure 14-2b) and a long put (Figure 14-3b).": "到目前为止，我们尚未讨论各合约的交易价格。在决定是否构建合成头寸时，价格当然很重要，稍后我们会讨论这个问题。但现在我们只考察合成头寸的特征，这些特征与合约的交易价格无关。在图 14-2a 和图 14-3a 中，标的头寸的建仓价格与行权价不同。决定头寸特征的不是合约价格，而是各合约损益线的斜率。合并后的斜率分别等价于多头看涨期权（图 14-2b）和多头看跌期权（图 14-3b）。",
    "Summarizing, there are six basic synthetic contracts—long and short an underlying contract, long and short a call, and long and short a put. If all options expire in June, using the 100 exercise price we have:": "总结起来，基本合成合约共有六种：标的合约多头与空头、看涨期权多头与空头，以及看跌期权多头与空头。若所有期权均于 6 月到期，并采用 100 的行权价，则有：",
    "A long put and a long underlying contract is a synthetic long call. The entire position is again a long straddle:": "多头看跌期权加上标的合约多头，等价于合成多头看涨期权。因此，整个头寸同样是多头跨式策略：",
    "The terms long and short, when applied to collars, typically refer to the underlying position. A long underlying position together with a protective put and covered call is a long collar. A short underlying position together with a protective call and covered put is a short collar. The characteristics of a collar are shown in Figures 17-5 and 17-6. Because every contract can be expressed as a synthetic equivalent, we can see that a long collar (Figure 17-5) is simply a bull vertical spread, while a short collar (Figure 17-6) is simply a bear vertical spread. Both strategies have limited risk and limited reward.": "在领式策略中，“多头”和“空头”通常指标的头寸的方向。标的多头加保护性看跌期权和备兑看涨期权，构成多头领式（long collar）；标的空头加保护性看涨期权和备兑看跌期权，构成空头领式（short collar）。领式策略的特征见图 17-5 和图 17-6。由于每一份合约都可以表示为其合成等价头寸，多头领式（图 17-5）本质上是牛市垂直价差，空头领式（图 17-6）本质上是熊市垂直价差。两种策略的风险和收益都是有限的。",
    "Instinctively, it seems that one would rather be long this security at a price of 100 than short the security at the same price. After all, the security can go up 20 but down only 10.": "直觉上，人们似乎更愿意在价格为 100 时做多该证券，而不是在同一价格做空。毕竟，该证券可能上涨 20，却只可能下跌 10。",
    "There are now three possible prices for the underlying at expiration—Suu, Sud, and Sdd. There is only one path that will lead to either Suu or Sdd. But there are two possible paths to the middle price Sud. The underlying can go up and then down or down and then up. The theoretical value of a call in the two-period example is": "现在，标的在到期时有三种可能价格：$S_{uu}$、$S_{ud}$ 和 $S_{dd}$。到达 $S_{uu}$ 或 $S_{dd}$ 的路径各只有一条，而到达中间价格 $S_{ud}$ 的路径有两条：标的可以先涨后跌，也可以先跌后涨。两期示例中看涨期权的理论价值为：",
    "If a skew trade is not hedged, the position will clearly have a positive delta (long calls and short puts) or negative delta (long puts and short calls). A trader who wants to focus solely on “buying skew” or “selling skew” must offset the delta position, most commonly with an opposing delta position in the underlying contract. When this is done, the entire strategy is usually referred to as a risk reversal. With the underlying contract trading at a price close to 100, the following are typical risk reversals (delta values are in parentheses):": "如果偏斜交易未进行对冲，该头寸显然会带有正 Delta（多头看涨期权加空头看跌期权）或负 Delta（多头看跌期权加空头看涨期权）。若交易者只想暴露于“买入偏斜”或“卖出偏斜”，就必须抵消该 Delta 头寸，最常见的方法是在标的合约中建立反向 Delta 头寸。完成这一对冲后，整体策略通常称为风险反转（risk reversal）。当标的合约价格接近 100 时，以下是典型的风险反转（括号内为 Delta）：",
    "2 There are, of course, investors and traders who take short stock positions, but they are relatively small in number compared with those who are long stock.": "2 当然，也有投资者和交易者持有股票空头，但与持有股票多头的人相比，他们的数量相对较少。",
    "Graphs similar to those in Figures 20-6 through 20-8 are often used to illustrate the term structure of volatility—the likelihood of volatility falling within a given range over a specified period of time. The term-structure graph typically has a conic shape, with greater variations over short periods of time and smaller variations over long periods.5 Because of the term structure of volatility, it is often easier to predict long-term volatility than short-term volatility. This may seem counterintuitive because we tend to expect greater variability over long periods of time than over short periods. However, volatility can be thought of as an average variability. Over long periods of time, the large and small price fluctuations tend to offset each other, resulting in more stable results.": "与图 20-6 至图 20-8 类似的图形，经常用来说明波动率的期限结构，即在特定时间段内，波动率落在某一范围内的可能性。期限结构图通常呈锥形：短期的变化范围较大，长期的变化范围较小。由于波动率存在期限结构，长期波动率往往比短期波动率更容易预测。这似乎违反直觉，因为我们通常预期长时间内的价格变动幅度会大于短时间。然而，波动率可以理解为平均变动程度；在较长时间内，较大和较小的价格波动往往相互抵消，因而产生更稳定的结果。",
}

CONTROLLED_TRANSLATIONS_CASEFOLD = {
    source.casefold(): target for source, target in CONTROLLED_TRANSLATIONS.items()
}

CONTROLLED_BLOCK_TRANSLATIONS = {
    "4ec8fdfedc5da513": "为了估算每周标准差，可以用年化波动率除以 7.2。将 20% 的年化波动率除以 52 的平方根（约为 7.2），得到 20% / 7.2 ≈ 2.78。对于价格为 100 的合约，我们预计每三周中有两周的价格变动不超过 2.78；每 20 周中有 19 周的价格变动不超过 5.56；而每 20 周中仅有一周预计会超过 5.56。",
    "731f8bde7faff54e": "到期时，若两份期权都为价外，看涨或看跌垂直价差的最小价值为 0；若两份期权都为价内，其最大价值等于两个行权价之差。若到期时标的合约低于 100，6 月 100/105 看涨价差中的两份期权均无价值，因而该价差也无价值。若标的合约高于 105，该价差价值为 5.00，因为 6 月 100 看涨期权的价值恰好比 6 月 105 看涨期权高五点。同理，若到期时标的市场高于 105，3 月 95/105 看跌价差毫无价值；若市场低于 95，其价值为 10.00。",
    "63098f3d70231760": "一般而言，若所有期权同时到期且均接近平值，行权价间距越大，价差的 Delta 也越大。95/110 牛市价差比 95/105 牛市价差更偏多，而后者又比 95/100 牛市价差更偏多。此外，扩大行权价间距还会提高价差的最大潜在利润或亏损，如图 12-7 所示。",
    "c98bc347b08ca54a": "首先考察图 13-2 中的三种策略：按 4:3 比率构建、使其更接近 Delta 中性的空头跨式（价差 1）；比率看涨价差（价差 2）；以及多头看跌蝶式价差（价差 3）。每个价差都大致保持 Delta 中性，并且如预期一样具有正的理论优势。我们应如何评估各价差的相对优劣？",
    "b77c03612e698f5d": "价差 4（空头看跌日历价差）和价差 5（对角看涨价差）都具有正 Gamma，因此都会从市场的大幅变动中获利。但与价差 4 在两个方向上的利润大致相等不同，价差 5 在上涨时利润更大，在下跌时利润较小。",
    "1c8964ce4dbf7f81": "若先关注六月 100 看跌期权与六月 105 看涨期权，该头寸可视为一个空头宽跨式（六月 100/105 宽跨式），再加上一份较低行权价的看跌期权多头（六月 95 看跌期权）。若关注六月 95 与六月 100 看跌期权，该头寸可视为一个牛市看跌价差（六月 100/105 看跌价差），再加上一份较高行权价的看涨期权空头（六月 105 看涨期权）。两种分解都表明：该头寸的下行风险有限，而上行风险无限。",
    "52e34edad74c2d85": "假设一家美国公司预计在六个月后接收价值 100 万欧元的德国商品。若合约要求在交付时以欧元付款，该公司就建立了欧元兑美元的空头敲口。未来六个月若欧元对美元升值，商品的美元成本将上升；若欧元贬值，成本则下降。若欧元当前为 1.35（每欧元 \\$1.35），且六个月后仍保持该水平，公司的成本为 \\$1,350,000。若交付时欧元上升至 1.45（每欧元 \\$1.45），成本将增至 \\$1,450,000。",
    "1aebc0010e0c325d": "标普 500 收益率分布的峰度异常高，达到 10.415。为了看出该分布尾部异常肥厚的程度，可以用标准差表示最大涨跌幅，再在正态分布假设下考察这些变动的发生概率。10 年期间标普指数的最大上涨为 11.58%。在标准差为 1.31% 时，这相当于一次 8.84 个标准差的变动，其概率约为 2,000,000,000,000,000,000 分之 1（即 2 quintillion）。最大下跌为 9.03%，相当于 6.75 个标准差，其概率约为 350,000,000,000 分之 1（即 350 billion）。简而言之，两种情形的理论概率都小到几乎不可能发生。",
    "fb73f31b875a368e": "假设交易员在波动率为 20% 时卖出一份已实现方差合约，对应的方差为 $20^2 = 400$。若合约存续期内的实际已实现波动率高于 20%，交易员亏损；若低于 20%，交易员获利。如何对冲该头寸？方差头寸可以通过购买横跨所有行权价的一系列期权来复制。为了建立方差敞口保持不变的头寸，对每个行权价 $X$ 都需购买 $1/X^2$ 份期权。随后，在方差互换的整个存续期内对全部头寸进行动态对冲，以维持 Delta 中性，则策略总价值将与方差合约的实际已实现方差完全匹配。",
    "cb6917c1ffd8a666": "Gamma 是二阶敏感度——即 Delta 对标的价格变化的敏感度——因此，Gamma 对市场条件变化的敏感度属于三阶敏感度。关于部分高阶敏感度，参见 Espen Gaarder Haug，The Complete Guide to Option Pricing Formulas（New York: McGraw-Hill, 2007）；Espen Gaarder Haug，“Know Your Weapon, Part 1,” Wilmott Magazine，2003 年 5 月：49–57，亦可查阅 http://www.wilmott.com/pdfs/050527_haug.pdf；以及 Espen Gaarder Haug，“Know Your Weapon, Part 2,” Wilmott Magazine，2003 年 7–8 月：50–56，亦可查阅 http://www.nuclearphynance.com/User percent20Files/2552/0307_haug.pdf。",
    "abfba94401925698": "比率价差——多头合约数大于空头合约数（包括空头圣诞树价差）",
    "223952028fe8c7f7": "这实质上等同于买入平值跨式期权组合。",
    "56494dcdd16ce2b2": "**Leg（组合腿）**：价差头寸的一边。",
}


def financial_basis_count(source: str) -> int:
    """Count commodity/forward ``basis`` uses, not ordinary 'basis' phrases."""
    trigger = re.search(
        r"\brefer to the basis\b|\bthe basis (?:is|will|should)\b|"
        r"\bbasis will\b|\bbasis turns?\b",
        source,
        re.I,
    )
    return len(re.findall(r"\bbasis\b", source, re.I)) if trigger else 0


OPTION_MONTH_NUMBERS = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12,
}
OPTION_SHORTHAND_RE = re.compile(
    rf"\b({'|'.join(OPTION_MONTH_NUMBERS)})\s+"
    r"(\d+(?:\.\d+)?)\s+(calls?|puts?)\b",
    re.I,
)
COMPACT_OPTION_POSITION_RE = re.compile(
    rf"\b(?:long|short)\s+(?:a\s+)?(?:\d+\s+)?"
    rf"(?:(?:{'|'.join(OPTION_MONTH_NUMBERS)})\s+)?"
    r"\d+(?:[½⅓⅔]|\.\d+)?\s+(?:calls?|puts?)\b",
    re.I,
)


def option_shorthand_translation_is_safe(source: str, target: str) -> bool:
    """Reject treating an option strike as a calendar day.

    In names such as ``October 90 call``, October is the expiration month and
    90 is the strike.  Literal MT frequently emits “10月90日看涨期权”.
    """
    for match in OPTION_SHORTHAND_RE.finditer(source):
        month = OPTION_MONTH_NUMBERS[match.group(1).lower()]
        strike = re.escape(match.group(2))
        if re.search(rf"{month}\s*月\s*{strike}\s*日", target):
            return False
    return True


def normalize_option_shorthand_translation(source: str, target: str) -> str:
    """Make expiry month and strike explicit when MT invents a day-of-month."""
    text = target
    for match in OPTION_SHORTHAND_RE.finditer(source):
        month = OPTION_MONTH_NUMBERS[match.group(1).lower()]
        strike = match.group(2)
        text = re.sub(
            rf"{month}\s*月\s*{re.escape(strike)}\s*日",
            f"{month} 月到期、行权价为 {strike} 的",
            text,
        )
    return text.replace("的的", "的")


def compact_option_position_translation_is_safe(source: str, target: str) -> bool:
    """Require compact position descriptions to remain verbatim English."""
    for match in COMPACT_OPTION_POSITION_RE.finditer(source):
        if not re.search(re.escape(match.group(0)), target, re.I):
            return False
    return True


def credit_debit_translation_is_safe(source: str, target: str) -> bool:
    """Keep cash-flow direction words in English to avoid accounting ambiguity."""
    for term in ("credit", "debit"):
        if re.search(rf"\b{term}s?\b", source, re.I) and not re.search(
            rf"(?<![A-Za-z]){term}(?![A-Za-z])", target, re.I
        ):
            return False
    return True


def probability_wording_translation_is_safe(source: str, target: str) -> bool:
    """Preserve distinctions when the author compares probability wording.

    In the Chapter 5 meta-language example, generic MT collapsed ``likely``,
    ``good chance``, ``possible``, and ``probable`` into repeated “可能”.  The
    English labels make the intended contrast explicit and auditable.
    """
    comparison = re.search(
        r"words such as\s+likely\s*,\s*good chance\s*,\s*possible\s*,\s*and\s+probable",
        re.sub(r"[*_]", "", source),
        re.I,
    )
    if not comparison:
        return True
    return all(
        re.search(rf"(?<![A-Za-z]){re.escape(term)}(?![A-Za-z])", target, re.I)
        for term in ("likely", "good chance", "possible", "probable")
    )


def probability_center_translation_is_safe(source: str, target: str) -> bool:
    """Reject reversal of the old and new centers of a probability distribution."""
    cleaned_source = re.sub(r"[*_]", "", source)
    match = re.search(
        r"instead of assigning the probabilities symmetrically around\s+\$?"
        r"(\d+(?:\.\d+)?)\s*,\s*we may want to assign them symmetrically "
        r"around\s+\$?(\d+(?:\.\d+)?)",
        cleaned_source,
        re.I,
    )
    if not match:
        return True
    old_center, new_center = map(re.escape, match.groups())
    old_then_new = re.search(
        rf"(?:不再|不是|并非)[^。；]*{old_center}[^。；]*"
        rf"(?:而是|改为|转而)[^。；]*{new_center}",
        target,
    )
    new_then_old = re.search(
        rf"{new_center}[^。；]*(?:而不是|而非|取代|替代)[^。；]*{old_center}",
        target,
    )
    return bool(old_then_new or new_then_old)


def normalize_credit_debit_terms(source: str, target: str) -> str:
    """Normalize option cash-flow direction words to explicit English."""
    text = target
    has_credit = bool(re.search(r"\bcredits?\b", source, re.I))
    has_debit = bool(re.search(r"\bdebits?\b", source, re.I))
    if has_credit and has_debit:
        for bad, preferred in (
            ("贷方或贷方", "credit 或 debit"),
            ("贷方和贷方", "credit 与 debit"),
            ("贷记或借记", "credit 或 debit"),
            ("信用或借记", "credit 或 debit"),
            ("信贷或借记", "credit 或 debit"),
            ("贷项或借项", "credit 或 debit"),
        ):
            text = text.replace(bad, preferred)
    if has_credit:
        for bad, preferred in (
            ("变动结算额信用", "variation credit"),
            ("变动结算贷记", "variation credit"),
            ("变化信用", "variation credit"),
            ("变更抵免", "variation credit"),
            ("现金抵免", "cash credit"),
            ("现金信用", "cash credit"),
            ("现金信贷", "cash credit"),
            ("现金贷项", "cash credit"),
            ("现金贷方", "cash credit"),
            ("信用价差", "credit spread"),
            ("信贷价差", "credit spread"),
            ("信用余额", "credit 余额"),
            ("贷记金额", "credit 金额"),
            ("总信用额", "credit 总额"),
            ("总信贷", "credit 总额"),
            ("总积分", "credit 总额"),
            ("总学分", "credit 总额"),
            ("学分", "credit"),
        ):
            text = text.replace(bad, preferred)
        text = re.sub(r"(?<![A-Za-z])(?:贷记|贷项|贷方|抵免|信贷|信用)(?![A-Za-z])", "credit", text)
    if has_debit:
        for bad, preferred in (
            ("变动结算额借记", "variation debit"),
            ("变化借记", "variation debit"),
            ("变更借记", "variation debit"),
            ("现金借记", "cash debit"),
            ("现金借项", "cash debit"),
            ("现金借方", "cash debit"),
            ("借记价差", "debit spread"),
            ("借记余额", "debit 余额"),
            ("总借记额", "debit 总额"),
        ):
            text = text.replace(bad, preferred)
        text = re.sub(r"(?<![A-Za-z])(?:借记|借项|借方)(?![A-Za-z])", "debit", text)
    text = re.sub(r"(?<=[\u3400-\u9fff])(?=(?:credit|debit)\b)", " ", text)
    text = re.sub(r"(?<=credit)(?=[\u3400-\u9fff])", " ", text, flags=re.I)
    text = re.sub(r"(?<=debit)(?=[\u3400-\u9fff])", " ", text, flags=re.I)
    text = re.sub(r"(?<=credit)(?=\d)", " ", text, flags=re.I)
    text = re.sub(r"(?<=debit)(?=\d)", " ", text, flags=re.I)
    return text


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\u00a0", " ")).strip()


def plain_text_for_translation(node: ET.Element) -> str:
    """Extract prose without EPUB footnote backlinks.

    The old extractor folded superscript footnote numbers into the sentence.
    TMT then produced corrupt strings such as ``Figure 9-10.4``.  The English
    callout still preserves the original superscript, while the Chinese prose
    is translated from the actual sentence only.
    """

    def is_footnote_sup(current: ET.Element) -> bool:
        if local_name(current.tag) != "sup":
            return False
        for descendant in current.iter():
            if local_name(descendant.tag) != "a":
                continue
            href = descendant.attrib.get("href", "")
            anchor_id = descendant.attrib.get("id", "")
            if "fn" in href or anchor_id.startswith("r"):
                return True
        return False

    def render(current: ET.Element) -> str:
        pieces: list[str] = []
        if current.text:
            pieces.append(current.text)
        for child in current:
            if not is_footnote_sup(child):
                content = render(child)
                if local_name(child.tag) == "sup" and content:
                    # Preserve mathematical superscripts.  A superscript
                    # followed by a slash is a printed mixed fraction such as
                    # 2 13/32; otherwise retain exponent notation.
                    pieces.append(
                        f" {content}" if (child.tail or "").lstrip().startswith("/")
                        else f"^{content}"
                    )
                else:
                    pieces.append(content)
            if child.tail:
                pieces.append(child.tail)
        return "".join(pieces)

    return clean_text(render(node))


def normalize_translation(text: str, source_text: str = "") -> str:
    """Apply book-specific terminology and typography corrections."""
    if source_text.startswith(
        "Time Box A long call and short put with the same exercise price"
    ):
        return (
            "时间箱式价差（Time Box）：在某一行权价和到期日上，"
            "同时建立看涨期权多头与看跌期权空头；再在另一行权价和"
            "到期日上，同时建立看涨期权空头与看跌期权多头。它本质上是"
            "一种使用不同行权价的展期价差，也称对角展期（diagonal roll）。"
        )
    if source_text.startswith("Theta (Θ) The sensitivity of an option’s theoretical value"):
        return "Theta（Θ）：期权理论价值对剩余到期时间变化的敏感度。"
    if source_text.startswith("Chooser Option A straddle where the owner must decide"):
        return (
            "选择式期权（Chooser Option）：一种跨式期权，其持有人必须在"
            "预先确定的日期前，决定保留看涨期权还是看跌期权。"
        )
    if source_text.startswith("In our discussion of synthetics, we noted that for European stock options"):
        return (
            "在讨论合成头寸时，我们注意到：对于行权价和到期日相同的欧式股票期权，"
            "看涨期权与看跌期权的 Delta 之和始终为 100。但对美式期权而言，两者 Delta 之和"
            "可能超过 100。这是因为美式价内期权的 Delta 比同等欧式期权更快趋近 100，"
            "而对应的价外期权仍保留一定 Delta。因此，用美式看涨期权多头加看跌期权空头"
            "构造合成标的头寸时，看涨期权 Delta 减去看跌期权 Delta 后的结果会大于 100。"
            "图 16-12 给出了与前例相同条件下、行权价为 100 的合成头寸所对应的美式 Delta："
        )
    replacements = {
        "Farmer Smith": "史密斯农夫",
        "法默·史密斯": "史密斯农夫",
        "法默史密斯": "史密斯农夫",
        "农民史密斯": "史密斯农夫",
        "Jerry": "杰里",
        "杰瑞": "杰里",
        "远期合同": "远期合约",
        "期货合同": "期货合约",
        "期权合同": "期权合约",
        "衍生品合同": "衍生合约",
        "标的合同": "标的合约",
        "基础合同": "标的合约",
        "基础工具": "标的工具",
        "基础价格": "标的价格",
        "基础市场": "标的市场",
        "基础头寸": "标的头寸",
        "基础位置": "标的头寸",
        "合同规范": "合约规格",
        "基础资产": "标的资产",
        "基础指数": "标的指数",
        "基础合约": "标的合约",
        "执行价格": "行权价",
        "执行价": "行权价",
        "行使价格": "行权价",
        "变更付款": "变动结算款",
        "最终变更": "最终变动结算",
        "变更要求": "变动结算要求",
        "变化的要求": "变动结算要求",
        "变异": "变动结算额",
        "求婚": "提议",
        "波动性": "波动率",
        "历史波幅": "历史波动率",
        "风险衡量": "风险度量",
        "风险措施": "风险指标",
        "提前行使": "提前行权",
        "早期练习": "提前行权",
        "早期锻炼": "提前行权",
        "早期运动": "提前行权",
        "原始对冲": "初始对冲",
        "解决程序": "结算程序",
        "市场诚信": "市场健全性",
        "三角洲": "Delta",
        "角增量": "Theta",
        "织女星": "Vega",
        "伽玛": "Gamma",
        "西塔": "Theta",
        "提前锻炼": "提前行权",
        "裸体姿势": "裸头寸",
        "提前练习": "提前行权",
        "保护性呼吁和承诺": "保护性看涨期权与看跌期权",
        "涵盖的写作": "备兑卖出",
        "项圈": "领式策略",
        "提前行权习": "提前行权",
        "提前运动": "提前行权",
        "提前锻炼": "提前行权",
        "传播策略": "价差策略",
        "传播简介": "价差策略导论",
        "合成位置": "合成头寸",
        "基础位置": "标的头寸",
        "提前行权价格": "行权价",
        "提前行权日": "行权日",
        "提前行权期": "行权期",
        "log正态": "对数正态",
        "逻辑正态": "对数正态",
        "西格玛（Sigma）": "σ（sigma）",
        "西格玛": "σ",
        "波动率合同": "波动率合约",
        "入金期权": "价内期权",
        "出金期权": "价外期权",
        "物内期权": "价内期权",
        "物外期权": "价外期权",
        "跨期期权": "跨式期权",
        "卖空跨式": "空头跨式",
        "ATM跨": "ATM 跨式",
        "En（": "ln(",
        "--": "——",
    }
    for source, target in replacements.items():
        text = text.replace(source, target)

    source_lower = source_text.lower()
    if re.search(r"(?<!in )\btime to maturity\b", source_text, re.I):
        # In derivatives pricing, "time to maturity" is the remaining time
        # until the contract expires.  Literal MT such as “成熟时间” describes
        # personal/biological maturity and is financially incorrect here.
        if re.match(r"^\s*time to maturity\b", source_text, re.I):
            text = re.sub(
                r"(?:至|到|距(?:离)?)?(?:成熟时间|到期时间)",
                "距离到期时间",
                text,
                count=1,
            )
        else:
            text = text.replace("成熟时间", "到期时间")
    if re.search(r"\bbrokerage firms?\b", source_text, re.I):
        text = text.replace("证券经纪公司", "券商").replace("经纪公司", "券商")
    text = normalize_option_shorthand_translation(source_text, text)
    text = normalize_credit_debit_terms(source_text, text)
    if financial_basis_count(source_text):
        # In forward/commodity pricing, basis is the cash/spot versus
        # forward/futures price difference. Generic MT often emits “基础” or
        # “基数”, both of which change the finance meaning.
        text = text.replace("基数", "基差").replace("基础", "基差")
    if re.search(r"\bvolatilit(?:y|ies)\b", source_lower):
        text = re.sub(
            r"(?<![A-Za-z])volatilit(?:y|ies)(?![A-Za-z])",
            "波动率",
            text,
            flags=re.I,
        )
    if re.search(r"\bcontracts?\b", source_lower):
        text = text.replace("合同", "合约")
    if re.search(r"\boptions?\b", source_lower):
        text = text.replace("选项", "期权").replace("购股权", "期权")
    if re.search(r"\bcalls?\b", source_lower):
        for bad in ("电话", "通话", "呼吁", "赎回", "认购期权", "呼叫", "调用"):
            text = text.replace(bad, "看涨期权")
        text = re.sub(
            r"(?<![A-Za-z])call(?![A-Za-z])",
            "看涨期权",
            text,
            flags=re.I,
        )
    if re.search(r"\bputs?\b", source_lower):
        for bad in ("推杆", "承诺", "放置期权"):
            text = text.replace(bad, "看跌期权")
        text = re.sub(
            r"(?<![A-Za-z])put(?![A-Za-z])",
            "看跌期权",
            text,
            flags=re.I,
        )
    if re.search(r"\b(?:calls?|puts?)\b", source_lower):
        text = re.sub(
            r"(\d{1,2})月(\d+(?:\.\d+)?)日(?=(?:的)?(?:看涨|看跌))",
            r"\1 月到期、行权价为 \2 的",
            text,
        )
    if re.search(r"\b(?:exercise|exercised|exercising)\b", source_lower):
        text = re.sub(r"(?<!执)行使", "行权", text)
        text = text.replace("练习", "行权").replace("锻炼", "行权")
        text = text.replace("执行期权", "行权").replace("执行了", "行权了")
        text = re.sub(r"执行(?=和|或|该|此|一|两|二|三|四|五|六|七|八|九|\d|期权)", "行权", text)
        text = text.replace("被执行", "被行权")
    if re.search(r"\bassignment\b|\bassigned on\b", source_lower):
        text = text.replace("分配", "指派").replace("被分派", "被指派")
        text = text.replace("转让", "指派")
    if re.search(r"\bunderlying\b", source_lower):
        text = re.sub(
            r"基础(?=市场|合同|合约|价格|工具|资产|证券|股票|期货|指数|商品|位置|头寸|物)",
            "标的",
            text,
        )
        text = re.sub(r"基础(?=[，。；;:]|$)", "标的", text)
        text = text.replace("基础是", "标的是").replace("基本立场", "标的头寸")
        text = text.replace("基础交易价", "标的交易价")
        text = text.replace("底层", "标的").replace("基础交易", "标的交易")
        text = text.replace("基础VIX", "标的 VIX").replace("基础股价", "标的股价")
        text = re.sub(
            r"(?<![A-Za-z])underlying(?![A-Za-z])",
            "标的",
            text,
            flags=re.I,
        )
    if re.search(r"\bpositions?\b", source_lower):
        text = text.replace("合成位置", "合成头寸").replace("头部位置", "头寸")
        text = re.sub(r"(?<!地理)位置", "头寸", text)
        text = text.replace("职位", "头寸").replace("立场", "头寸")
    if re.search(r"\bspreads?\b|\bspreading\b", source_lower):
        text = (
            text.replace("传播", "价差")
            .replace("范围", "价差")
            .replace("点差", "价差")
            .replace("利差", "价差")
            .replace("跨页", "价差")
            .replace("比率分布", "比率价差")
            .replace("日历分布", "日历价差")
        )
        text = text.replace("比例差价", "比率价差").replace("垂直传播", "垂直价差")
    if re.search(r"\bstraddles?\b", source_lower):
        for bad in ("跨骑", "跨坐", "跨盘", "跨接", "跨交", "跨持", "跨越"):
            text = text.replace(bad, "跨式")
        text = text.replace("长跨式", "多头跨式").replace("短跨式", "空头跨式")
        text = text.replace("跨写", "跨式卖出")
        text = text.replace("空头交叉", "空头跨式").replace("长交叉", "多头跨式")
        text = text.replace("长跨", "多头跨式").replace("短跨", "空头跨式")
    if re.search(r"\bstrangles?\b", source_lower):
        for bad in ("勒死", "扼杀", "绞杀", "长颈勒死"):
            text = text.replace(bad, "宽跨式")
        text = text.replace("长宽跨式", "多头宽跨式").replace("短宽跨式", "空头宽跨式")
        text = text.replace("长脖子和短脖子", "多头宽跨式与空头宽跨式")
    if re.search(r"\bbutterfl(?:y|ies)\b", source_lower):
        text = text.replace("长时间蝴蝶", "多头时间蝶式价差")
        text = text.replace("长长的蝴蝶", "多头蝶式价差")
        text = text.replace("长蝴蝶", "多头蝶式价差").replace("短蝴蝶", "空头蝶式价差")
        text = text.replace("蝴蝶指数", "蝶式价差")
        text = text.replace("蝴蝶", "蝶式价差")
        text = text.replace("蝶形", "蝶式价差")
    if re.search(r"\bcondors?\b", source_lower):
        text = text.replace("秃鹰", "鹰式价差").replace("神鹰", "鹰式价差")
    if re.search(r"\bat[- ]the[- ]money\b", source_lower):
        for bad in ("按价", "以价", "物超所值", "最接近资金"):
            text = text.replace(bad, "平值")
        if not re.search(r"\b(?:in[- ]the[- ]money|out[- ]of[- ]the[- ]money)\b", source_lower):
            text = text.replace("物有所值", "平值")
            text = text.replace("实值期权", "平值期权")
        for bad in ("平值购买期权", "平值出售期权", "平值计算的期权"):
            text = text.replace(bad, "平值期权")
    if re.search(r"\bin[- ]the[- ]money\b", source_lower):
        for bad in ("钱内", "金钱内", "深入货币", "深入金钱", "在货币中", "货币中"):
            text = text.replace(bad, "价内")
        if not re.search(r"\b(?:at[- ]the[- ]money|out[- ]of[- ]the[- ]money)\b", source_lower):
            text = text.replace("物有所值", "价内")
    if re.search(r"\bout[- ]of[- ]the[- ]money\b", source_lower):
        for bad in ("钱外", "金钱外", "远离货币", "远离金钱", "货币之外", "在货币之外"):
            text = text.replace(bad, "价外")
        if not re.search(r"\b(?:in[- ]the[- ]money|at[- ]the[- ]money)\b", source_lower):
            text = text.replace("物有所值", "价外")
    source_money_terms: list[str] = []
    for match in re.finditer(
        r"\b(?:in[- ]the[- ]money|at[- ]the[- ]money|out[- ]of[- ]the[- ]money)\b",
        source_text,
        re.I,
    ):
        lowered = match.group(0).lower()
        if lowered.startswith("in"):
            source_money_terms.append("价内")
        elif lowered.startswith("at"):
            source_money_terms.append("平值")
        else:
            source_money_terms.append("价外")
    ambiguous_money = list(re.finditer(r"物有所值|现付|物超", text))
    if source_money_terms and len(ambiguous_money) == len(source_money_terms):
        iterator = iter(source_money_terms)
        text = re.sub(r"物有所值|现付|物超", lambda _: next(iterator), text)
    target_money_terms = list(
        re.finditer(r"价内|实值|平值|价外|虚值|物有所值|物超|现付", text)
    )
    if source_money_terms and len(target_money_terms) == len(source_money_terms):
        iterator = iter(source_money_terms)
        text = re.sub(
            r"价内|实值|平值|价外|虚值|物有所值|物超|现付",
            lambda _: next(iterator),
            text,
        )
    text = text.replace("物有所实值", "价内").replace("物虚值", "价外")
    text = text.replace("物有所虚值", "价外")
    text = text.replace("虚值期权", "价外期权").replace("虚值的", "价外的")
    text = text.replace("的实值", "的内在价值").replace("正实值", "正的内在价值")
    if re.search(r"\bin[- ]the[- ]money\b", source_lower):
        text = text.replace("实值期权", "价内期权").replace("是实值的", "是价内的")
        text = text.replace("为了实值", "要成为价内")
        text = text.replace("深度货币期权", "深度价内期权").replace("深度货币", "深度价内")
        text = text.replace("非常划算的选择", "深度价内期权")
        text = text.replace("划算的选择", "价内期权")
    if re.search(r"\bout[- ]of[- ]the[- ]money\b", source_lower):
        text = text.replace("极高价期权", "深度价外期权")
    if re.search(r"\bdeltas?\b", source_lower):
        text = text.replace("增量", "Delta").replace("三角形", "Delta")
        text = text.replace("德尔塔", "Delta")
        text = re.sub(r"(?<![A-Za-z])delta(?![A-Za-z])", "Delta", text, flags=re.I)
    if re.search(r"\bgammas?\b", source_lower):
        text = text.replace("伽马", "Gamma").replace("伽玛", "Gamma")
        text = re.sub(r"(?<![A-Za-z])gamma(?![A-Za-z])", "Gamma", text, flags=re.I)
    if re.search(r"\bthetas?\b", source_lower):
        text = text.replace("西塔", "Theta")
        text = re.sub(r"(?<![A-Za-z])theta(?![A-Za-z])", "Theta", text, flags=re.I)
    if re.search(r"\bvegas?\b", source_lower):
        text = text.replace("维加", "Vega").replace("维嘎", "Vega")
        text = text.replace("维加斯", "Vega").replace("维嘎斯", "Vega")
        text = re.sub(r"(?<![A-Za-z])vega(?![A-Za-z])", "Vega", text, flags=re.I)
        text = text.replace("变得越来越负面", "Vega 变得越来越负")
    if re.search(r"\brhos?\b", source_lower):
        text = re.sub(r"(?<![A-Za-z])rho(?![A-Za-z])", "Rho", text, flags=re.I)
    if re.search(r"\bcharm\b", source_lower):
        text = text.replace("魅力", "Charm")
    if re.search(r"\bcolor\b", source_lower):
        text = text.replace("颜色", "Color")
    if re.search(r"\bparity\b", source_lower):
        text = text.replace("宇称", "平价").replace("看跌看涨平价", "看涨-看跌平价")
    if re.search(r"\bslopes?\b", source_lower):
        text = text.replace("斜坡", "斜率").replace("倾斜度", "斜率")
    if re.search(r"\bcovered calls?\b", source_lower):
        for bad in ("担保看涨期权", "承保看涨期权", "有保障看涨", "担保看涨"):
            text = text.replace(bad, "备兑看涨期权")
    if re.search(r"\bcovered[- ]writes?\b", source_lower):
        for bad in ("覆盖写", "承保写", "备兑写", "覆盖式卖出"):
            text = text.replace(bad, "备兑卖出")
    if re.search(r"\bat[- ]the[- ]forward\b", source_lower):
        text = text.replace("正向看涨期权", "远期平值看涨期权")
        text = text.replace("向前跨式", "远期平值跨式")
    if re.search(r"\bcompanion puts?\b", source_lower):
        text = text.replace("同伴看跌期权", "对应的看跌期权").replace("同伴看跌", "对应的看跌期权")
    if re.search(r"\bvolatility component\b", source_lower):
        text = text.replace("挥发性成分", "波动率成分")
    text = text.replace("gamma（Term）", "Gamma（Γ）").replace("theta（eta）", "Theta（θ）")
    if re.search(r"\bmargin(?:ing)?\b", source_lower):
        text = text.replace("边距", "保证金")
    if re.search(r"\blong (?:position|stock|futures?|contracts?|options?|calls?|puts?|underlying|market|volatility|delta|gamma|vega|straddles?|strangles?|spreads?|butterfl(?:y|ies)|collars?)\b|\bgo long\b", source_lower) and not re.search(
        r"\blong[- ]term\b", source_lower
    ):
        text = text.replace("长期头寸", "多头头寸")
        text = re.sub(r"长期(?=看涨|看跌|期权|头寸|跨式|宽跨式|波动|伽马|Delta|Vega)", "多头", text)
        text = re.sub(r"长(?=看涨|看跌|跨式|宽跨式|蝶式|领式)", "多头", text)
        text = text.replace("长期标的", "多头标的")
        text = re.sub(r"长\s*Call", "看涨期权多头", text, flags=re.I)
        text = re.sub(r"长\s*Put", "看跌期权多头", text, flags=re.I)
        if re.search(r"\blong call calendar spread\b", source_lower):
            text = text.replace("看涨期权日历价差", "多头看涨期权日历价差", 1)
    if re.search(r"\bshort (?:position|stock|futures?|contracts?|options?|calls?|puts?|underlying|market|volatility|delta|gamma|vega|straddles?|strangles?|spreads?|butterfl(?:y|ies)|collars?)\b|\bgo short\b", source_lower) and not re.search(
        r"\bshort[- ]term\b", source_lower
    ):
        text = text.replace("短期头寸", "空头头寸")
        text = re.sub(r"短期(?=看涨|看跌|期权|头寸|跨式|宽跨式|波动|伽马|Delta|Vega)", "空头", text)
        text = re.sub(r"短(?=看涨|看跌|跨式|宽跨式|蝶式|领式)", "空头", text)
        text = text.replace("短期标的", "空头标的")
        text = re.sub(r"短\s*Call", "看涨期权空头", text, flags=re.I)
        text = re.sub(r"短\s*Put", "看跌期权空头", text, flags=re.I)
        if re.search(r"\bshort put calendar spread\b", source_lower):
            text = text.replace("看跌期权日历价差", "空头看跌期权日历价差", 1)
    text = re.sub(r"(?<=\d)，(?=\d{3}(?:\D|$))", ",", text)
    text = re.sub(r"(?<=\d),\s+(?=\d{3}(?:\D|$))", ",", text)
    text = re.sub(r"(?<=\d)\s+x\s+(?=\d)", " × ", text)
    text = re.sub(r"ln\(([^）]+)）", r"ln(\1)", text)
    return text.replace("$", r"\$")


def high_risk_translation_is_safe(source: str, target: str) -> bool:
    """Fail closed when a machine translation drops a trading-critical term.

    The English source remains the authoritative fallback. This is preferable
    to displaying fluent Chinese that reverses a position or changes an
    option's rights and obligations.
    """
    checks = [
        (r"\blong (?:position|stock|futures?|contracts?|options?|calls?|puts?|underlying|volatility)\b|\bgo long\b", r"多头|做多|买入|持有"),
        (r"\bshort (?:position|stock|futures?|contracts?|options?|calls?|puts?|underlying|volatility)\b|\bgo short\b", r"空头|做空|卖出|卖空"),
        (
            r"\bcall options?\b|\b(?:long|short) calls?\b|"
            r"\bcalls?\s+(?:and|or)\s+puts?\b|"
            r"\b(?:buy|sell|bought|sold|purchase|purchased)\s+(?:a|the|\d+)?\s*calls?\b",
            r"看涨|Call",
        ),
        (
            r"\bput options?\b|\b(?:long|short) puts?\b|"
            r"\bputs?\s+(?:and|or)\s+calls?\b|"
            r"\b(?:buy|sell|bought|sold|purchase|purchased)\s+(?:a|the|\d+)?\s*puts?\b",
            r"看跌|Put",
        ),
        (r"\b(?:exercise|exercised|exercising)\b", r"行权|行使"),
        (r"\bassignment\b|\bassigned on\b|\bgets? assigned\b", r"指派|被行权"),
        (r"\bunderlying\b", r"标的"),
        (r"\bvolatilit(?:y|ies)\b", r"波动率"),
        (
            r"\b(?:option|calendar|vertical|horizontal|diagonal|ratio|volatility|"
            r"bull|bear|credit|debit|time) spreads?\b|\bspread (?:position|strategy|order)\b",
            r"价差|利差",
        ),
        (r"\bstraddles?\b", r"跨式|Straddle"),
        (r"\bcovered[- ]writes?\b", r"备兑卖出|covered write"),
        (r"\bstrangles?\b", r"宽跨式|Strangle"),
        (r"\bbutterfl(?:y|ies)\b", r"蝶式|蝶形|Butterfly"),
        (r"\bin[- ]the[- ]money\b", r"价内|实值|ITM"),
        (r"\bat[- ]the[- ]money\b", r"平值|ATM"),
        (r"\bout[- ]of[- ]the[- ]money\b", r"价外|虚值|OTM"),
        (r"\bdelta\b", r"Delta"),
        (r"\bgamma\b", r"Gamma|伽马|伽玛"),
        (r"\btheta\b", r"Theta"),
        (r"\bvega\b", r"Vega"),
        (r"\brho\b", r"Rho"),
        (r"\bbasis points?\b", r"基点"),
        (r"\bbasis for\b", r"基础|依据|构成|根基"),
        (r"(?<!in )\btime to maturity\b", r"到期时间|剩余期限"),
        (r"\bbrokerage firms?\b", r"券商|证券经纪公司"),
        (r"\blong\s+\d+\s*deltas?\b|\b\d+\s*deltas?\s+long\b", r"多头|做多|long"),
        (r"\bshort\s+\d+\s*deltas?\b|\b\d+\s*deltas?\s+short\b", r"空头|做空|short"),
    ]
    for source_pattern, target_pattern in checks:
        if re.search(source_pattern, source, re.I) and not re.search(target_pattern, target):
            return False
    if any(term in target for term in ("物有所值", "钱内", "钱外", "远离货币", "深入金钱")):
        return False
    if target.count("基差") < financial_basis_count(source):
        return False
    if not option_shorthand_translation_is_safe(source, target):
        return False
    if not compact_option_position_translation_is_safe(source, target):
        return False
    if not credit_debit_translation_is_safe(source, target):
        return False
    if not probability_wording_translation_is_safe(source, target):
        return False
    if not probability_center_translation_is_safe(source, target):
        return False
    return True


def translation_language_is_safe(source: str, target: str) -> bool:
    """Reject untranslated or mostly-English prose, including mixed fallbacks."""
    source_words = len(re.findall(r"[A-Za-z]+(?:['’-][A-Za-z]+)?", source))
    if source_words < 12:
        return True
    chinese_chars = len(re.findall(r"[\u3400-\u9fff]", target))
    target_words = len(re.findall(r"[A-Za-z]+(?:['’-][A-Za-z]+)?", target))
    return (
        chinese_chars >= max(8, source_words // 3)
        and target_words <= max(12, source_words // 2)
    )


def explicit_numbers(text: str) -> Counter[str]:
    """Return explicit numeric literals for fail-closed semantic QA."""
    # Obsidian footnote identifiers are navigation metadata, not financial
    # numerals from the source paragraph.
    text = re.sub(r"\[\^[^\]]+\]", "", text)
    text = re.sub(r"<sup>.*?</sup>", "", text)
    text = re.sub(r"<[^>]+>", "", text).replace("*", "")
    # TeX uses {,} to keep a thousands separator from acquiring punctuation
    # spacing in math mode (for example, 61{,}200).
    text = re.sub(r"(?<=\d)\{,\}(?=\d{3}\b)", ",", text)
    text = text.replace("⅓", "1/3").replace("⅔", "2/3")
    text = re.sub(r"\bthe(?=\d)", "the ", text, flags=re.I)
    text = re.sub(
        r"\b(january|february|march|april|may|june|july|august|september|october|november|december)(?=\d)",
        r"\1 ",
        text,
        flags=re.I,
    )
    magnitudes = {"thousand": 1000, "million": 1000000, "billion": 1000000000}
    for word, factor in magnitudes.items():
        text = re.sub(
            rf"(\d+(?:\.\d+)?)\s+{word}\b",
            lambda match, multiplier=factor: str(
                Decimal(match.group(1)) * multiplier
            ),
            text,
            flags=re.I,
        )
    text = re.sub(
        r"(\d+(?:\.\d+)?)百万",
        lambda match: str(Decimal(match.group(1)) * 1000000),
        text,
    )
    text = re.sub(
        r"(\d+(?:\.\d+)?)亿",
        lambda match: str(Decimal(match.group(1)) * 100000000),
        text,
    )
    text = re.sub(
        r"(\d+(?:\.\d+)?)\s*万",
        lambda match: str(Decimal(match.group(1)) * 10000),
        text,
    )
    text = re.sub(r"(?<=\d)\s+(?=\d{3}(?:\D|$))", "", text)
    # Subscripts on model variables are labels, not financial amounts.  TMT
    # often inserts a space (C0,0 -> C 0,0), which must not invent a number.
    text = re.sub(
        r"(?<![A-Za-z])(?:Rho|[COVSt])\s*\d+(?:[,，]\d+)?",
        "",
        text,
        flags=re.I,
    )
    found = re.findall(r"(?<![A-Za-z])(?:\d[\d,]*(?:\.\d+)?|\.\d+)", text)
    normalized: list[str] = []
    for item in found:
        try:
            item = format(Decimal(item.replace(",", "")).normalize(), "f")
        except InvalidOperation:
            item = item.replace(",", "")
        normalized.append(item)
    return Counter(normalized)


def numeric_translation_is_safe(source_markdown: str, target: str) -> bool:
    source_numbers = explicit_numbers(source_markdown)
    target_numbers = explicit_numbers(target)
    for marker in re.findall(r"<sup>(\d+)</sup>", source_markdown):
        # Old cached translations sometimes copied a footnote marker into the
        # sentence, while protected translations intentionally omit it.  Only
        # remove an actual surplus; subtracting an equal, legitimate figure or
        # strike number created false failures.
        if target_numbers[marker] > source_numbers[marker]:
            target_numbers[marker] -= 1
            if not target_numbers[marker]:
                del target_numbers[marker]
    months = {
        "january": "1", "february": "2", "march": "3", "april": "4",
        "may": "5", "june": "6", "july": "7", "august": "8",
        "september": "9", "october": "10", "november": "11", "december": "12",
    }
    for month, value in months.items():
        for _ in re.finditer(rf"\b{month}\b", source_markdown, re.I):
            if target_numbers[value] > source_numbers[value]:
                target_numbers[value] -= 1
                if not target_numbers[value]:
                    del target_numbers[value]
    number_words = {
        "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4",
        "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9",
        "ten": "10", "eleven": "11", "twelve": "12",
        "twenty": "20", "thirty": "30", "forty": "40", "fifty": "50",
        "sixty": "60", "seventy": "70", "eighty": "80", "ninety": "90",
    }
    for word, value in number_words.items():
        for _ in re.finditer(rf"\b{word}\b", source_markdown, re.I):
            if target_numbers[value] > source_numbers[value]:
                target_numbers[value] -= 1
                if not target_numbers[value]:
                    del target_numbers[value]
    chinese_small = {
        "0": "零", "1": "[一两]", "2": "[二两]", "3": "三", "4": "四",
        "5": "五", "6": "六", "7": "七", "8": "八", "9": "九", "10": "十",
    }
    units = r"(?:个|份|周|章|次|点|项|种|天|月|年|期|步|方|边|年期)"
    for value, numeral in chinese_small.items():
        occurrences = len(re.findall(rf"(?:第)?{numeral}{units}", target))
        surplus = max(0, source_numbers[value] - target_numbers[value])
        if occurrences and surplus:
            source_numbers[value] -= min(occurrences, surplus)
            if not source_numbers[value]:
                del source_numbers[value]
    return source_numbers == target_numbers


def plain_text(node: ET.Element) -> str:
    return clean_text("".join(node.itertext()))


def inline_markdown(node: ET.Element) -> str:
    pieces: list[str] = []
    if node.text:
        pieces.append(node.text)
    for child in node:
        tag = local_name(child.tag)
        content = inline_markdown(child)
        if tag in {"em", "i"} and content:
            pieces.append(f"*{content}*")
        elif tag in {"strong", "b"} and content:
            pieces.append(f"**{content}**")
        elif tag == "sup" and content:
            pieces.append(f"<sup>{content}</sup>")
        elif tag != "img":
            pieces.append(content)
        if child.tail:
            pieces.append(child.tail)
    # A bare dollar sign is an Obsidian inline-math delimiter. Currency signs in
    # the source must therefore be escaped unless they are emitted by the
    # dedicated LaTeX renderer below.
    return clean_text("".join(pieces)).replace("$", r"\$")


def source_hash(node: ET.Element) -> str:
    """Stable fingerprint used by the completeness audit."""
    payload = ET.tostring(node, encoding="utf-8")
    return hashlib.sha256(payload).hexdigest()[:16]


def formula_source(node: ET.Element) -> str:
    """Extract formula text while preserving EPUB sub/superscript structure."""
    def render(current: ET.Element) -> str:
        pieces: list[str] = []
        if current.text:
            pieces.append(current.text)
        for child in current:
            tag = local_name(child.tag)
            href = child.attrib.get("href", "")
            # Superscript footnote backlinks are not part of an equation.
            if tag == "a" and ("fn" in href or child.attrib.get("id", "").startswith("r")):
                pass
            elif tag == "sub":
                content = clean_text("".join(child.itertext()))
                if content:
                    pieces.append(f"_{{{content}}}")
            elif tag == "sup":
                content = clean_text(
                    "".join(
                        text
                        for descendant in child.iter()
                        if local_name(descendant.tag) != "a"
                        for text in ([descendant.text] if descendant.text else [])
                    )
                )
                if content:
                    pieces.append(f"^{{{content}}}")
            elif tag in {"em", "i"}:
                content = render(child)
                if content:
                    # Preserve the author's explicit variable markup across the
                    # later prose-token pass.
                    pieces.append(f"\ue100{content}\ue101")
            elif tag != "img":
                pieces.append(render(child))
            if child.tail:
                pieces.append(child.tail)
        return "".join(pieces)

    return clean_text(render(node))


def is_formula_block(css_class: str, text: str) -> bool:
    """Recognize the EPUB's displayed equations without translating them."""
    if css_class.startswith("eqcenter"):
        return True
    if css_class.startswith("eqhang"):
        return bool(re.search(r"(?:=|>>|[+×−–≤≥≈]|\d\s*/\s*\d)", text))
    # A handful of equations (notably one in a footnote) have no equation CSS
    # class. Catch formula-only lines by structure, while leaving prose that
    # merely mentions a symbol to the normal bilingual path.
    word_count = len(re.findall(r"[A-Za-z]{2,}", text))
    strong_operators = len(re.findall(r"(?:=|>>|×|≤|≥|≈)", text))
    if word_count <= 6 and strong_operators >= 2:
        return True
    return False


def formula_to_latex(text: str) -> str:
    """Conservatively turn the book's equation text into KaTeX-safe LaTeX.

    Prose inside a verbal equation is wrapped in ``\\text{}``; mathematical
    symbols and variables remain math. This deliberately favors faithful,
    renderable output over speculative algebraic rewriting.
    """
    text = clean_text(text).strip(" .")
    marked_variables: list[str] = []

    def protect_marked_variable(match: re.Match[str]) -> str:
        marked_variables.append(match.group(1))
        return chr(0xE200 + len(marked_variables) - 1)

    text = re.sub("\ue100(.*?)\ue101", protect_marked_variable, text)
    # Private-use placeholders cannot be mistaken for English words by the
    # prose wrapper below.
    placeholders = {
        ">>": "\ue000",
        "×": "\ue001",
        "≥": "\ue002",
        "≤": "\ue003",
        "≈": "\ue004",
        "…": "\ue005",
        "½": "\ue006",
        "⅓": "\ue007",
        "⅔": "\ue008",
        "¼": "\ue009",
        "¾": "\ue00a",
    }
    for source, target in placeholders.items():
        text = text.replace(source, target)
    text = text.replace("–", "-").replace("−", "-").replace("—", "-")

    # Words in an equation are labels, not variables. Keep single-letter
    # variables, short all-caps symbols, and standard function names in math.
    def wrap_words(match: re.Match[str]) -> str:
        phrase = match.group(0)
        words = phrase.split()
        functions = {"ln", "log", "exp", "max", "min", "sin", "cos"}
        composite_variables = {"Su", "Sd", "pu", "pd", "ud", "du", "rt"}

        def is_variable(word: str) -> bool:
            return (
                len(word) == 1
                or (word.isupper() and len(word) <= 4)
                or word in composite_variables
            )

        if len(words) == 1:
            word = words[0]
            if is_variable(word):
                return word
            if word in functions:
                return f"\\{word}"
        elif all(is_variable(word) for word in words):
            # Explicit spacing is required in math mode; ordinary spaces are
            # discarded by KaTeX/LaTeX.
            return r"\,".join(words)

        escaped = phrase.replace("&", r"\&")
        return rf"\text{{{escaped}}}"

    word = r"[A-Za-z]+(?:[’'][A-Za-z]+)?(?:-[A-Za-z]+)*"
    text = re.sub(
        rf"{word}(?:\s+{word})*",
        wrap_words,
        text,
    )
    text = re.sub(
        r"[\u3400-\u9fff]+",
        lambda match: rf"\text{{{match.group(0)}}}",
        text,
    )
    replacements = {
        "\ue000": r"\Rightarrow",
        "\ue001": r"\times",
        "\ue002": r"\ge",
        "\ue003": r"\le",
        "\ue004": r"\approx",
        "\ue005": r"\ldots",
        "\ue006": r"\frac{1}{2}",
        "\ue007": r"\frac{1}{3}",
        "\ue008": r"\frac{2}{3}",
        "\ue009": r"\frac{1}{4}",
        "\ue00a": r"\frac{3}{4}",
        "σ": r"\sigma",
        "Σ": r"\Sigma",
        "δ": r"\delta",
        "Δ": r"\Delta",
        "γ": r"\gamma",
        "Γ": r"\Gamma",
        "θ": r"\theta",
        "Θ": r"\Theta",
        "μ": r"\mu",
        "π": r"\pi",
    }
    for source, target in replacements.items():
        text = text.replace(source, target)
    for index, variable in enumerate(marked_variables):
        token = chr(0xE200 + index)
        text = text.replace(f" {token}", rf"\,{variable}")
        text = text.replace(f"{token} ", rf"{variable}\,")
        text = text.replace(token, variable)
    text = text.replace("%", r"\%").replace("$", r"\$")
    text = re.sub(r"(?<=\d),(?=\d{3}(?:\D|$))", r"{,}", text)
    # Convert only symbolic ratios such as ``\Gamma/2`` or ``a/I``.  The old
    # numeric-token rule also matched the tail of decimal divisions and turned
    # ``297.4/24.13`` into ``297.\frac{4}{24}.13``, changing the mathematics.
    # Plain numeric ``/`` is valid LaTeX and is therefore left untouched.
    text = re.sub(
        r"(?<![\\\w}.])((?:\\[A-Za-z]+|[A-Za-z]+))\s*/\s*"
        r"((?:\\[A-Za-z]+|[A-Za-z]+|\d+))(?![\w{.])",
        lambda match: rf"\frac{{{match.group(1)}}}{{{match.group(2)}}}",
        text,
    )
    text = re.sub(r"\s+", " ", text).strip()
    return text


def iter_blocks(node: ET.Element):
    for child in node:
        tag = local_name(child.tag)
        if tag in BLOCK_TAGS or tag in IMAGE_TAGS:
            yield child
        else:
            yield from iter_blocks(child)


def load_cache(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_cache(path: Path, cache: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(cache, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )


PROTECTED_TERM_PATTERNS = [
    (r"\bcredits\b", "credits"),
    (r"\bdebits\b", "debits"),
    (r"\bcredit\b", "credit"),
    (r"\bdebit\b", "debit"),
    (r"\bout[- ]of[- ]the[- ]money\b", "价外"),
    (r"\bin[- ]the[- ]money\b", "价内"),
    (r"\bat[- ]the[- ]money\b", "平值"),
    (r"\bautomatic exercise\b", "自动行权"),
    (r"\bearly exercise\b", "提前行权"),
    (r"\bexercise notice\b", "行权通知"),
    (r"\bexercise price\b", "行权价"),
    (r"\bunexercised\b", "未行权"),
    (r"\bexercising\b", "行权"),
    (r"\bexercised\b", "已行权"),
    (r"\bexercise\b", "行权"),
    (r"\bassigned\b", "被指派"),
    (r"\bassignment\b", "指派"),
    (r"\blong calls?\b", "看涨期权多头"),
    (r"\bshort calls?\b", "看涨期权空头"),
    (r"\blong puts?\b", "看跌期权多头"),
    (r"\bshort puts?\b", "看跌期权空头"),
    (r"\bcalls?\s+(?:and|or)\s+puts?\b", "看涨期权与看跌期权"),
    (r"\bputs?\s+(?:and|or)\s+calls?\b", "看跌期权与看涨期权"),
    (r"\bcall options?\b", "看涨期权"),
    (r"\bput options?\b", "看跌期权"),
    (r"\blong positions?\b", "多头头寸"),
    (r"\bshort positions?\b", "空头头寸"),
    (r"\blong volatility\b", "做多波动率"),
    (r"\bshort volatility\b", "做空波动率"),
    (r"\bunderlying contracts?\b", "标的合约"),
    (r"\bunderlying positions?\b", "标的头寸"),
    (r"\bunderlying assets?\b", "标的资产"),
    (r"\bunderlying instruments?\b", "标的工具"),
    (r"\bunderlying securit(?:y|ies)\b", "标的证券"),
    (r"\bunderlying stocks?\b", "标的股票"),
    (r"\bunderlying indexes?\b|\bunderlying indices\b", "标的指数"),
    (r"\bunderlying prices?\b", "标的价格"),
    (r"\bunderlying markets?\b", "标的市场"),
    (r"\bunderlying\b", "标的"),
    (r"\bstraddles?\b", "跨式策略"),
    (r"\bstrangles?\b", "宽跨式策略"),
    (r"\bbutterfl(?:y|ies)\b", "蝶式价差"),
    (r"\bcondors?\b", "鹰式价差"),
    (r"\bdelta\b", "Delta"),
    (r"\bgamma\b", "Gamma"),
    (r"\btheta\b", "Theta"),
    (r"\bvega\b", "Vega"),
    (r"\brho\b", "Rho"),
    (r"\bvolatility\b", "波动率"),
]


def domain_abbreviation_source(text: str) -> str:
    """Use stable option abbreviations without changing sentence language."""
    replacements = [
        (r"\bout[- ]of[- ]the[- ]money\b", "OTM"),
        (r"\bin[- ]the[- ]money\b", "ITM"),
        (r"\bat[- ]the[- ]money\b", "ATM"),
        (r"\bstraddles?\b", "Straddle"),
        (r"\bstrangles?\b", "Strangle"),
        (r"\bbutterfl(?:y|ies)\b", "Butterfly"),
        (r"\blong calls?\b", "看涨期权多头"),
        (r"\bshort calls?\b", "看涨期权空头"),
        (r"\blong puts?\b", "看跌期权多头"),
        (r"\bshort puts?\b", "看跌期权空头"),
    ]
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text, flags=re.I)
    return text


def prepare_protected_translation(
    text: str,
    *,
    protect_numbers: bool = True,
    protect_terms: bool = True,
    plain_number_tokens: bool = False,
) -> tuple[str, list[str], list[str]]:
    """Protect numbers and option terms from machine-translation drift."""
    numbers: list[str] = []
    terms: list[str] = []

    def protect_number(match: re.Match[str]) -> str:
        numbers.append(match.group(0))
        index = len(numbers) - 1
        return f"{{{index}}}" if plain_number_tokens else f"{{N{index}}}"

    if protect_numbers:
        protected = re.sub(
            r"(?<![A-Za-z])(?:\d+\s+\d+/\d+|\d[\d,]*(?:\.\d+)?(?:/\d+)?|\.\d+)",
            protect_number,
            text,
        )
    else:
        protected = text

    if protect_terms:
        number_token = r"\{(?:N)?\d+\}"
        protected_position_pattern = (
            rf"\b(?:long|short)\s+(?:a\s+)?(?:{number_token}\s+)?"
            rf"(?:(?:{'|'.join(OPTION_MONTH_NUMBERS)})\s+)?"
            rf"{number_token}[½⅓⅔]?\s+(?:calls?|puts?)\b"
        )

        def protect_compact_position(match: re.Match[str]) -> str:
            terms.append(match.group(0))
            return f"{{T{len(terms) - 1}}}"

        protected = re.sub(
            protected_position_pattern,
            protect_compact_position,
            protected,
            flags=re.I,
        )
        for pattern, chinese in PROTECTED_TERM_PATTERNS:
            def protect_term(match: re.Match[str], value: str = chinese) -> str:
                terms.append(value)
                return f"{{T{len(terms) - 1}}}"

            protected = re.sub(pattern, protect_term, protected, flags=re.I)
    return protected, numbers, terms


def restore_protected_translation(
    text: str,
    numbers: list[str],
    terms: list[str],
    *,
    plain_number_tokens: bool = False,
) -> str:
    """Restore placeholders and fail if TMT dropped or invented one."""
    for prefix, values in (("T", terms), ("N", numbers)):
        seen: Counter[int] = Counter()

        def restore(match: re.Match[str]) -> str:
            index = int(match.group(1))
            if index >= len(values):
                raise RuntimeError(f"unexpected translation placeholder {prefix}{index}")
            seen[index] += 1
            return values[index]

        if prefix == "N" and plain_number_tokens:
            pattern = r"\{\s*(\d+)\s*\}"
        else:
            pattern = rf"\{{\s*{prefix}\s*(\d+)\s*\}}"
        text = re.sub(pattern, restore, text, flags=re.I)
        missing = [index for index in range(len(values)) if seen[index] != 1]
        if missing:
            raise RuntimeError(
                f"translation dropped or duplicated {prefix} placeholders: {missing[:8]}"
            )
    residual_pattern = (
        r"\{\s*(?:[TN]\s*)?\d+\s*\}"
        if plain_number_tokens
        else r"\{\s*[TN]\s*\d+\s*\}"
    )
    if re.search(residual_pattern, text, re.I):
        raise RuntimeError("unresolved translation placeholder")
    return text


def translate_protected_cached(
    text: str,
    cache: dict[str, str],
    cache_path: Path,
    cache_namespace: str = "tmt-protected-glossary-v2",
) -> str:
    """Translate unsafe prose with protected numbers and finance terms."""
    if cache_namespace.endswith(("v6", "v8", "v9")):
        chunk_limit = 300
    elif cache_namespace.endswith("v3"):
        chunk_limit = 600
    elif cache_namespace.endswith(("v4", "v5")):
        chunk_limit = 1200
    else:
        chunk_limit = 1800
    if len(text) > chunk_limit:
        sentences = re.split(r"(?<=[.!?])\s+", text)
        chunks: list[str] = []
        current = ""
        for sentence in sentences:
            if current and len(current) + len(sentence) + 1 > chunk_limit:
                chunks.append(current)
                current = sentence
            else:
                current = f"{current} {sentence}".strip()
        if current:
            chunks.append(current)
        if any(len(chunk) > chunk_limit for chunk in chunks):
            chunks = []
            current = ""
            for word in text.split():
                if current and len(current) + len(word) + 1 > chunk_limit:
                    chunks.append(current)
                    current = word
                else:
                    current = f"{current} {word}".strip()
            if current:
                chunks.append(current)
        return " ".join(
            translate_protected_cached(
                chunk,
                cache,
                cache_path,
                cache_namespace=cache_namespace,
            )
            for chunk in chunks
        )

    key = hashlib.sha256(
        (cache_namespace + "\0" + text).encode("utf-8")
    ).hexdigest()
    if key in cache:
        return normalize_translation(cache[key], text)

    machine_source = domain_abbreviation_source(text) if cache_namespace.endswith("v9") else text
    protected, numbers, terms = prepare_protected_translation(
        machine_source,
        protect_numbers=not cache_namespace.endswith("v5"),
        protect_terms=not cache_namespace.endswith(("v4", "v5", "v6", "v8", "v9")),
        plain_number_tokens=cache_namespace.endswith(("v8", "v9")),
    )
    for attempt in range(4):
        try:
            result = translate(protected, use_glossary=True).get("Response", {})
            if "Error" in result:
                error = result["Error"]
                raise RuntimeError(f"{error.get('Code')}: {error.get('Message')}")
            raw = clean_text(result.get("TargetText", ""))
            if not raw:
                raise RuntimeError("empty protected translation")
            target = restore_protected_translation(
                raw,
                numbers,
                terms,
                plain_number_tokens=cache_namespace.endswith(("v8", "v9")),
            )
            target = normalize_translation(target, text)
            cache[key] = target
            save_cache(cache_path, cache)
            return target
        except Exception:
            if attempt == 3:
                raise
            time.sleep(1.5 * (attempt + 1))
    raise AssertionError("unreachable")


def translate_cached(text: str, cache: dict[str, str], cache_path: Path) -> str:
    if text.casefold() in CONTROLLED_TRANSLATIONS_CASEFOLD:
        return CONTROLLED_TRANSLATIONS_CASEFOLD[text.casefold()]
    numbered = re.fullmatch(r"(\d+)\s+(.+)", text)
    if numbered and numbered.group(2).casefold() in CONTROLLED_TRANSLATIONS_CASEFOLD:
        return (
            f"{numbered.group(1)} "
            f"{CONTROLLED_TRANSLATIONS_CASEFOLD[numbered.group(2).casefold()]}"
        )
    if len(text) > 1800:
        sentences = re.split(r"(?<=[.!?])\s+", text)
        chunks: list[str] = []
        current = ""
        for sentence in sentences:
            if current and len(current) + len(sentence) + 1 > 1800:
                chunks.append(current)
                current = sentence
            else:
                current = f"{current} {sentence}".strip()
        if current:
            chunks.append(current)
        return " ".join(
            translate_cached(chunk, cache, cache_path) for chunk in chunks
        )
    key = hashlib.sha256(("tmt-noglossary-v1\0" + text).encode("utf-8")).hexdigest()
    if key in cache:
        return normalize_translation(cache[key], text)
    for attempt in range(4):
        try:
            result = translate(text, use_glossary=False).get("Response", {})
            if "Error" in result:
                error = result["Error"]
                raise RuntimeError(f"{error.get('Code')}: {error.get('Message')}")
            target = normalize_translation(clean_text(result.get("TargetText", "")), text)
            if not target:
                raise RuntimeError("empty translation")
            cache[key] = target
            save_cache(cache_path, cache)
            return target
        except Exception:
            if attempt == 3:
                raise
            time.sleep(1.5 * (attempt + 1))
    raise AssertionError("unreachable")


def quote_callout(number: int, english: str) -> list[str]:
    return [f"> [!quote]- English {number}", f"> {english}", ""]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("epub", type=Path)
    parser.add_argument("chapter", help="EPUB chapter path, e.g. ops/ch1.html")
    parser.add_argument("output", type=Path)
    parser.add_argument("--chapter-number", required=True)
    parser.add_argument("--chinese-title", required=True)
    parser.add_argument("--english-title", required=True)
    parser.add_argument(
        "--section-label",
        help="Visible label such as '附录 A'; defaults to '第N章'",
    )
    parser.add_argument(
        "--source-label",
        help="Source heading label to skip, such as A or B",
    )
    parser.add_argument(
        "--asset-key",
        help="Filesystem-safe asset/cache key; defaults to chNN",
    )
    parser.add_argument(
        "--preserve-english",
        action="store_true",
        help="Keep ordinary source paragraphs visible in English instead of machine translating them",
    )
    args = parser.parse_args()

    section_label = args.section_label or f"第{int(args.chapter_number)}章"
    asset_key = args.asset_key or f"ch{int(args.chapter_number):02d}"
    output_dir = args.output.parent
    assets_dir = output_dir / "assets" / asset_key
    cache_path = output_dir / ".translation-cache" / f"{asset_key}.json"
    cache = load_cache(cache_path)

    with zipfile.ZipFile(args.epub) as archive:
        root = ET.fromstring(archive.read(args.chapter))
        body = root.find(f"{XHTML_NS}body")
        if body is None:
            raise RuntimeError("chapter has no XHTML body")

        lines = [
            "---",
            f"title: {section_label} {args.chinese_title} / {args.english_title}",
            "tags:",
            "  - 期权",
            "  - 双语阅读",
            f"section: {section_label}",
            "translation_status: 腾讯云机器初译，公式已转 LaTeX，待复核",
            "created: 2026-08-03",
            "---",
            "",
            f"# {section_label} {args.chinese_title} / {args.english_title}",
            "",
            "[[00-阅读导航|← 返回阅读导航]] · [[00-翻译说明与术语表|术语表]]",
            "",
            "> [!warning] 翻译状态",
            "> 本章为机器初译，并使用本地术语表校验。英文原文、数字、公式和图表用于核对；中文将在后续复核中继续修订。",
            "",
        ]
        paragraph_number = 0
        skipped_title = False

        for block in iter_blocks(body):
            tag = local_name(block.tag)
            css_class = block.attrib.get("class", "")
            images = [
                node for node in block.iter() if local_name(node.tag) in IMAGE_TAGS
            ]
            if images:
                lines.extend([f"<!-- source:block {source_hash(block)} -->", ""])
                assets_dir.mkdir(parents=True, exist_ok=True)
                for image in images:
                    source = image.attrib.get("src", "") or image.attrib.get(
                        "{http://www.w3.org/1999/xlink}href", ""
                    )
                    if not source:
                        continue
                    chapter_parent = Path(args.chapter).parent
                    epub_image = str(chapter_parent / source)
                    destination = assets_dir / Path(source).name
                    with archive.open(epub_image) as source_file, destination.open("wb") as target:
                        shutil.copyfileobj(source_file, target)
                    relative = destination.relative_to(output_dir)
                    lines.extend([f"![原书图表]({relative.as_posix()})", ""])
                if css_class.startswith("eq"):
                    lines.extend(["<!-- 原 EPUB 中此公式为图片，已原样保留 -->", ""])
                continue

            english_plain = plain_text(block)
            if not english_plain:
                continue
            english_markdown = inline_markdown(block)
            english_for_translation = plain_text_for_translation(block)

            if tag == "h2" and english_plain == args.chapter_number:
                continue
            if tag == "h2" and args.source_label and english_plain == args.source_label:
                continue
            if tag == "h2" and english_plain == args.english_title and not skipped_title:
                skipped_title = True
                continue
            if tag in {"h1", "h2", "h3", "h4"}:
                chinese_heading = translate_cached(
                    english_plain, cache, cache_path
                )
                level = 2 if tag in {"h1", "h2", "h3"} else 3
                lines.extend(
                    [
                        f"<!-- source:block {source_hash(block)} -->",
                        "",
                        f"{'#' * level} {chinese_heading} / {english_plain}",
                        "",
                    ]
                )
                continue

            paragraph_number += 1
            lines.extend([f"<!-- source:block {source_hash(block)} -->", ""])
            if is_formula_block(css_class, english_plain):
                # Equations are never sent to machine translation: translating
                # variables caused errors such as p becoming the Chinese word
                # "假名". The source is retained for checking and a clean
                # LaTeX rendering is shown in the visible note.
                lines.extend(quote_callout(paragraph_number, english_markdown))
                lines.extend(["$$", formula_to_latex(formula_source(block)), "$$", ""])
                continue

            if args.preserve_english:
                # Some reference matter (especially the alphabetical index) is
                # safer and more useful when left in English. Translating terse
                # entries without sentence context produced false finance terms
                # such as "inbox spread" and "physical settlement".
                lines.extend(quote_callout(paragraph_number, english_markdown))
                lines.extend([english_markdown, ""])
                continue

            chinese = CONTROLLED_BLOCK_TRANSLATIONS.get(source_hash(block))
            if chinese is None:
                chinese = translate_cached(english_plain, cache, cache_path)
            if (
                not high_risk_translation_is_safe(english_plain, chinese)
                or not numeric_translation_is_safe(english_for_translation, chinese)
                or not translation_language_is_safe(english_plain, chinese)
            ):
                chinese = translate_protected_cached(
                    english_for_translation,
                    cache,
                    cache_path,
                    cache_namespace="tmt-domain-glossary-v9",
                )
            if (
                not high_risk_translation_is_safe(english_plain, chinese)
                or not numeric_translation_is_safe(english_for_translation, chinese)
                or not translation_language_is_safe(english_plain, chinese)
            ):
                chinese = translate_protected_cached(
                    english_for_translation,
                    cache,
                    cache_path,
                    cache_namespace="tmt-direct-glossary-v5",
                )
            if (
                not high_risk_translation_is_safe(english_plain, chinese)
                or not numeric_translation_is_safe(english_for_translation, chinese)
                or not translation_language_is_safe(english_plain, chinese)
            ):
                raise RuntimeError(
                    "unsafe translation after protected retry for source block "
                    f"{source_hash(block)}"
                )
            if css_class in {"fcaption"}:
                lines.extend([f"*{chinese} / {english_markdown}*", ""])
            elif css_class.startswith("footnote"):
                lines.extend(
                    [
                        f"> [!note] Footnote {paragraph_number}",
                        f"> {english_markdown}",
                        f"> {chinese}",
                        "",
                    ]
                )
            else:
                lines.extend(quote_callout(paragraph_number, english_markdown))
                lines.extend([chinese, ""])

    lines.extend(["---", "", "[[00-阅读导航|← 返回阅读导航]]", ""])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {args.output} with {paragraph_number} translated text blocks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
