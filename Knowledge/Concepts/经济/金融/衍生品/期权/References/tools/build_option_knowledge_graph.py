#!/usr/bin/env python3
"""Build the curated option knowledge graph for the bilingual Natenberg edition.

The graph is intentionally concept-first.  Reading navigation, translation notes,
audit reports, and other technical files are not part of the semantic graph.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
EDITION = ROOT / "Option Volatility and Pricing 双语版"
OUT = EDITION / "知识图谱"
GENERATOR = "tools/build_option_knowledge_graph.py"


@dataclass(frozen=True)
class Layer:
    number: int
    title: str
    english: str
    question: str
    summary: str

    @property
    def stem(self) -> str:
        return self.title


NOTE_NAME_OVERRIDES = {
    # 库内已有同名概念页时，知识图谱侧保留教材出处后缀，避免双链歧义；键为 cid，值为目标文件名（不含序号）
    "C17": "隐含波动率（Natenberg）",
    "C26": "Delta（Natenberg）",
    "C27": "Gamma（Natenberg）",
    "C28": "Theta（Natenberg）",
    "C29": "Vega（Natenberg）",
    "C30": "Rho（Natenberg）",
    "C33": "动态Delta对冲（Natenberg）",
    "C35": "跨式与宽跨式（Natenberg）",
}


@dataclass(frozen=True)
class Concept:
    cid: str
    layer: int
    title: str
    english: str
    definition: str
    chapters: tuple[int, ...]
    formula: str
    risk_check: str

    @property
    def stem(self) -> str:
        if self.cid in NOTE_NAME_OVERRIDES:
            return NOTE_NAME_OVERRIDES[self.cid]
        safe = self.title.replace("/", "与").replace("：", "-")
        return safe


@dataclass(frozen=True)
class Edge:
    source: str
    verb: str
    target: str
    detail: str


LAYERS = (
    Layer(1, "合约与损益语义", "Contracts and Payoffs", "交易的究竟是什么？", "从合约条款、权利金和结算方式还原实际现金流。"),
    Layer(2, "无套利与持有成本", "No-Arbitrage and Carry", "不同合约价格为什么互相约束？", "用融资、股息、远期价格和平价关系建立相对价格边界。"),
    Layer(3, "概率分布与波动率", "Distributions and Volatility", "不确定性如何观察、预测和交易？", "区分已实现、预测与隐含波动率，并理解期限结构和偏斜。"),
    Layer(4, "估值模型与模型风险", "Valuation and Model Risk", "如何把假设转化为理论价值？", "比较期望值、Black–Scholes、二叉树和美式期权估值。"),
    Layer(5, "Greeks与动态对冲", "Greeks and Dynamic Hedging", "价值变化如何传导到头寸？", "用局部敏感度汇总风险，并通过再平衡管理方向暴露。"),
    Layer(6, "策略与风险形状", "Strategies and Risk Shapes", "如何组合合约得到目标暴露？", "按方向、凸性、期限、偏斜和保护需求组织策略。"),
    Layer(7, "市场实施与专门产品", "Implementation and Products", "现实市场如何改变理论结果？", "纳入事件、流动性、执行、指数和波动率产品风险。"),
)


CHAPTERS = {
    1: ("01-金融合约 Financial Contracts", "第1章 金融合约"),
    2: ("02-远期定价 Forward Pricing", "第2章 远期定价"),
    3: ("03-合约规格与期权术语 Contract Specifications and Option Terminology", "第3章 合约规格与期权术语"),
    4: ("04-到期盈亏 Expiration Profit and Loss", "第4章 到期盈亏"),
    5: ("05-理论定价模型 Theoretical Pricing Models", "第5章 理论定价模型"),
    6: ("06-波动率 Volatility", "第6章 波动率"),
    7: ("07-风险度量（一） Risk Measurement I", "第7章 风险度量（一）"),
    8: ("08-动态对冲 Dynamic Hedging", "第8章 动态对冲"),
    9: ("09-风险度量（二） Risk Measurement II", "第9章 风险度量（二）"),
    10: ("10-价差策略导论 Introduction to Spreading", "第10章 价差策略导论"),
    11: ("11-波动率价差策略 Volatility Spreads", "第11章 波动率价差策略"),
    12: ("12-牛市与熊市价差 Bull and Bear Spreads", "第12章 牛市与熊市价差"),
    13: ("13-风险考量 Risk Considerations", "第13章 风险考量"),
    14: ("14-合成头寸 Synthetics", "第14章 合成头寸"),
    15: ("15-期权套利 Option Arbitrage", "第15章 期权套利"),
    16: ("16-美式期权的提前行权 Early Exercise of American Options", "第16章 美式期权的提前行权"),
    17: ("17-使用期权进行对冲 Hedging with Options", "第17章 使用期权进行对冲"),
    18: ("18-Black–Scholes 模型 The Black-Scholes Model", "第18章 Black–Scholes 模型"),
    19: ("19-二叉树期权定价 Binomial Option Pricing", "第19章 二叉树期权定价"),
    20: ("20-再论波动率 Volatility Revisited", "第20章 再论波动率"),
    21: ("21-头寸分析 Position Analysis", "第21章 头寸分析"),
    22: ("22-股票指数期货与期权 Stock Index Futures and Options", "第22章 股票指数期货与期权"),
    23: ("23-模型与现实世界 Models and the Real World", "第23章 模型与现实世界"),
    24: ("24-波动率偏斜 Volatility Skews", "第24章 波动率偏斜"),
    25: ("25-波动率合约 Volatility Contracts", "第25章 波动率合约"),
}


CONCEPTS = (
    Concept("C01", 1, "标的资产与现价", "Underlying and Spot Price", "期权与远期价值所依附的资产及其当前可交易价格，通常记为 $S_0$。现价是方向风险、价内外程度和复制头寸的共同基准。", (1, 3, 5, 22), "", "确认使用的是可成交现价、指数值还是估值价格；检查停牌、跳空、公司行动和标的—对冲工具基差。"),
    Concept("C02", 1, "远期与期货合约", "Forwards and Futures", "约定在未来日期按约定价格交换标的的线性合约。它把持有成本、融资和股息压缩为一个未来交割价格。", (1, 2, 15, 22), r"$$F_{0,T}=S_0e^{(r-q)T}$$", "区分远期与逐日盯市期货；核对基差、交割品、最后交易日、现金或实物结算以及保证金流动性。"),
    Concept("C03", 1, "看涨与看跌期权", "Calls and Puts", "看涨期权赋予按行权价买入标的的权利，看跌期权赋予卖出标的的权利；买方拥有权利，卖方承担或有义务。", (3, 4, 5), r"$$\text{Call payoff}=(S_T-K)^+,\qquad \text{Put payoff}=(K-S_T)^+$$", "先确认方向、合约乘数、期权类型和多空；卖方风险不能只用收到的权利金衡量。"),
    Concept("C04", 1, "行权价与价内外程度", "Strike and Moneyness", "行权价 $K$ 是非线性损益的折点；价内外程度描述现价或远期价相对行权价的位置，是偏斜和相对价值比较的坐标。", (3, 4, 24), r"$$m=\frac{S}{K},\qquad k=\ln\!\left(\frac{K}{F}\right)$$", "跨到期比较应优先使用远期价内外程度；检查拆股等公司行动后的行权价调整。"),
    Concept("C05", 1, "到期时间与行权方式", "Time to Expiry and Exercise Style", "剩余期限决定不确定性累积和时间价值；欧式期权仅到期行权，美式期权可在到期前行权。", (3, 5, 16), r"$$\tau=T-t$$", "核对具体到期时刻、节假日、停止交易时间和行权截止时间；不能把美式头寸直接当作欧式头寸管理。"),
    Concept("C06", 1, "权利金与价值构成", "Premium and Value Components", "权利金是期权的市场成交价格，可分为内在价值与时间价值；它不是理论价值，也不必等于中间价。", (3, 4, 5, 8), r"$$\text{Premium}=\text{Intrinsic Value}+\text{Time Value}$$", "以可执行买价或卖价估算退出价值；检查陈旧报价、价差、费用和理论中间价造成的虚假优势。"),
    Concept("C07", 1, "到期收益与损益曲线", "Expiration Payoff and P&L", "把各腿到期现金流与初始权利金相加，得到头寸在不同到期标的价格下的静态损益形状。", (4, 10, 11, 12, 17), r"$$\Pi_{\text{long call}}(S_T)=(S_T-K)^+-C_0$$", "到期图忽略路径、隐含波动率、提前行权和持有期间盯市；不能把静态图当作止损或资金占用预测。"),

    Concept("C08", 2, "利率与融资成本", "Rates and Funding", "资金的时间价值影响远期价格、期权现值、持仓融资以及提前行权机会成本；实际融资常与无风险利率不对称。", (2, 5, 8, 13, 23), r"$$PV(X_T)=X_Te^{-rT}$$", "使用匹配币种和期限的利率曲线；同时检查借款、放款、保证金利率和抵押品成本的差异。"),
    Concept("C09", 2, "股息与持有成本", "Dividends and Cost of Carry", "股息或持有收益降低持有标的的净成本，并改变远期价格、看涨看跌相对价值和美式行权边界。", (2, 5, 8, 13, 19), r"$$F_{0,T}=S_0e^{(r-q)T}$$", "离散股息应按除息日期建模；检查股息预测误差、特别股息和借券费用。"),
    Concept("C10", 2, "远期价格与期货基差", "Forward Price and Basis", "远期价格是无套利持有成本关系给出的未来交割价格；本书将基差定义为现货价格减去远期或期货价格，它不是对未来现货价格的预测。", (2, 6, 22), r"$$b_{0,T}=S_0-F_{0,T}$$", "先确认市场采用的基差符号约定；指数产品还要计入成分股股息、复制误差和篮子成交成本。"),
    Concept("C11", 2, "无套利定价与套利边界", "No-Arbitrage Pricing and Bounds", "如果两组未来现金流相同，其当前价格在可执行市场中应一致；边界刻画期权价格不能长期越过的范围。", (2, 15, 16), r"$$C\geq\max\!\left(0,S_0e^{-qT}-Ke^{-rT}\right)$$", "先验证所有腿能同时成交且可持有至结算；借券、涨跌停、保证金和结算差异会使理论套利不可执行。"),
    Concept("C12", 2, "看涨看跌平价与合成头寸", "Put-Call Parity and Synthetics", "同一标的、行权价和期限的看涨、看跌、标的及债券可通过现金流复制互相转换，是合成头寸和套利的核心恒等关系。", (14, 15, 16), r"$$C-P=S_0e^{-qT}-Ke^{-rT}$$", "平价式需匹配欧式条款和股息处理；美式行权、借券限制与交易成本会改变现实等价关系。"),
    Concept("C13", 2, "结算行权与指派", "Settlement, Exercise, and Assignment", "行权把期权权利转成现金、标的或期货头寸；指派把对应义务分配给卖方，结算规则决定最终风险落点。", (1, 3, 15, 16), "", "逐合约确认现金/实物结算、行权截止、自动行权阈值、交割货币、指派流程和结算价来源。"),

    Concept("C14", 3, "概率分布", "Probability Distributions", "概率分布描述未来价格或收益的可能范围；经典模型常从随机游走、正态收益或对数正态价格出发。", (5, 6, 23), r"$$\ln\!\left(\frac{S_T}{S_0}\right)\sim\mathcal N\!\left((\mu-\tfrac12\sigma^2)T,\sigma^2T\right)$$", "用压力情景补充连续分布；重点检查跳空、厚尾、波动率聚集和价格—波动率相关性。"),
    Concept("C15", 3, "历史与已实现波动率", "Historical and Realized Volatility", "历史波动率由过去收益估计，已实现波动率描述指定观察期实际发生的价格变化；二者都依赖采样与年化规则。", (6, 20, 25), r"$$\sigma_{\mathrm{ann}}=\sqrt{A\,\frac{1}{n-1}\sum_{i=1}^{n}(r_i-\bar r)^2}$$", "记录窗口、频率、年化天数、缺失值和异常收益；合约结算公式可能使用总体方差而非样本方差。"),
    Concept("C16", 3, "波动率预测", "Volatility Forecasting", "利用历史特征、制度信息和市场状态估计未来持有期可能实现的波动率，预测值是交易观点而非可观察事实。", (20,), "", "保留预测区间和情景，不只保留点估计；检查结构突变、事件日、均值回归假设和模型外数据。"),
    Concept("C17", 3, "隐含波动率", "Implied Volatility", "在给定模型及其他输入后，使模型价格等于市场权利金的波动率参数；它是价格的模型化表达，不等于未来已实现波动率。", (6, 8, 20, 24, 25), r"$$C_{\mathrm{mkt}}=BS(S,K,T,r,q,\sigma_{\mathrm{imp}})$$", "隐波依赖模型和报价质量；使用买卖两侧隐波，并核对深度价内外期权的数值稳定性。"),
    Concept("C18", 3, "期限结构与远期波动率", "Term Structure and Forward Volatility", "不同到期的隐含波动率构成期限结构；远期波动率是由两个期限的总方差差额推导出的未来区间波动率。", (20,), r"$$\sigma^2_{0,T_2}T_2=\sigma^2_{0,T_1}T_1+\sigma^2_{T_1,T_2}(T_2-T_1)$$", "用总方差而非波动率直接相减；检查日历套利、一致的日计数和重大事件跨期影响。"),
    Concept("C19", 3, "波动率偏斜与曲面", "Volatility Skew and Surface", "隐含波动率随行权价和期限变化形成偏斜、微笑及完整曲面，反映尾部定价、供需和模型局限。", (24,), r"$$\sigma_{\mathrm{imp}}(K)=a+bK+cK^2+dK^3+\cdots$$", "插值与外推必须保持价格单调性和凸性；明确使用粘性行权价、粘性 Delta 或其他曲面动态。"),
    Concept("C20", 3, "偏度峰度与隐含分布", "Skewness, Kurtosis, and Implied Distribution", "偏度刻画分布非对称性，峰度刻画尾部与尖峭程度；期权跨行权价价格可反推出风险中性隐含分布。", (23, 24), r"$$\gamma_1=\frac{E[(X-\mu)^3]}{\sigma^3},\qquad \gamma_2=\frac{E[(X-\mu)^4]}{\sigma^4}-3$$", "尾部统计量样本不稳定；风险中性隐含分布不是现实世界概率预测，不能直接当作违约频率。"),

    Concept("C21", 4, "期望值与理论价值", "Expected and Theoretical Value", "理论价值是在一组概率和市场假设下对未来现金流进行风险调整或风险中性贴现得到的模型结果。", (5, 8), r"$$V_0=e^{-rT}\,E^{\mathbb Q}[\mathrm{Payoff}(S_T)]$$", "理论价值不是可成交价格；报告模型、输入、报价侧、参数时点和不确定区间。"),
    Concept("C22", 4, "Black-Scholes模型", "Black-Scholes Model", "在连续交易、对数正态扩散及确定利率和波动率等假设下，通过动态复制给出欧式期权价值和 Greeks。", (5, 18, 23, 24), r"$$C=S_0e^{-qT}N(d_1)-Ke^{-rT}N(d_2)$$\n$$d_1=\frac{\ln(S_0/K)+(r-q+\tfrac12\sigma^2)T}{\sigma\sqrt T},\quad d_2=d_1-\sigma\sqrt T$$", "逐项记录假设偏离：跳空、随机波动率、交易成本、离散对冲、利率曲线和美式行权。"),
    Concept("C23", 4, "二叉树与风险中性估值", "Binomial and Risk-Neutral Valuation", "把期限拆成离散节点，在风险中性概率下由未来节点价值向后递推，能自然处理路径节点和提前行权判断。", (19,), r"$$V=e^{-r\Delta t}[pV_u+(1-p)V_d],\qquad p=\frac{e^{(r-q)\Delta t}-d}{u-d}$$", "检查步数收敛、树参数、股息节点和负概率；模型精度不应通过不透明的过度校准掩盖。"),
    Concept("C24", 4, "美式期权与提前行权价值", "American Option and Early-Exercise Value", "美式期权在每个可行权时点比较立即行权价值与继续持有价值，其价值至少不低于对应欧式期权。", (16, 19), r"$$V_t=\max\{\text{Intrinsic}_t,\ \text{Continuation}_t\}$$", "特别检查除息日前看涨期权、深度价内看跌期权、借券成本和剩余时间价值；边界应接受情景测试。"),
    Concept("C25", 4, "模型假设与模型风险", "Model Assumptions and Model Risk", "模型风险来自分布、参数、市场摩擦和动态假设与现实不一致，表现为理论价值、Greeks 和对冲结果系统性偏差。", (8, 23, 24, 25), "", "至少并行比较基础模型、曲面模型和压力情景；对无法对冲的模型误差设置限额，而不是只扩大数值精度。"),

    Concept("C26", 5, "Delta", "Delta", "Delta 衡量期权价值对标的价格的局部一阶敏感度，也常作为等价标的头寸和动态对冲比率。", (7, 8, 9, 18, 19, 21, 24), r"$$\Delta=\frac{\partial V}{\partial S}$$", "Delta 只在当前点局部有效；统一现货/期货 Delta、合约乘数、币种和正负方向。"),
    Concept("C27", 5, "Gamma", "Gamma", "Gamma 衡量 Delta 对标的价格的变化率，是头寸凸性以及再平衡需求的核心指标。", (7, 9, 13, 18, 19, 21, 24), r"$$\Gamma=\frac{\partial^2V}{\partial S^2}=\frac{\partial\Delta}{\partial S}$$", "临近到期和平值附近 Gamma 可急剧集中；对大幅跳空使用全重估，不能只依赖二阶近似。"),
    Concept("C28", 5, "Theta", "Theta", "Theta 衡量其他条件不变时，日历时间流逝对期权价值的局部影响，通常与 Gamma 暴露形成权衡。", (7, 9, 13, 18, 19, 21), r"$$\Theta=\frac{\partial V}{\partial t}$$", "确认按自然日还是交易日表达及符号约定；正 Theta 不是无风险收益，常伴随负凸性或尾部风险。"),
    Concept("C29", 5, "Vega", "Vega", "Vega 衡量模型波动率变化对期权价值的局部敏感度，是隐含波动率头寸的主要尺度。", (7, 9, 13, 19, 20, 21, 24, 25), r"$$\mathrm{Vega}=\frac{\partial V}{\partial\sigma}$$", "统一按 1 个波动率点还是 100% 变动报价；单一 Vega 不能描述偏斜、期限和波动率凸性。"),
    Concept("C30", 5, "Rho", "Rho", "Rho 衡量利率变化对期权价值的局部敏感度，在长期限、外汇和融资敏感头寸中更重要。", (7, 13, 19, 21), r"$$\rho=\frac{\partial V}{\partial r}$$", "不要只平移单一利率；压力测试收益率曲线形变、融资利差和股息—利率联动。"),
    Concept("C31", 5, "Lambda", "Lambda", "Lambda 是期权价值对标的百分比变化的弹性，反映单位资本上的方向杠杆。", (9,), r"$$\Lambda=\frac{\partial V/V}{\partial S/S}=\Delta\frac{S}{V}$$", "当期权价格很小时 Lambda 会失真或爆炸；资本、保证金和最大损失不能仅由弹性衡量。"),
    Concept("C32", 5, "组合Greeks与头寸分析", "Portfolio Greeks and Position Analysis", "把各合约按数量、乘数和币种汇总为组合风险，并结合情景全重估形成做市账簿的风险视图。", (7, 9, 13, 21), r"$$G_{\mathrm{portfolio}}=\sum_i n_i\,m_i\,G_i$$", "净额可能掩盖单腿流动性、集中度、跨品种基差和尾部风险；同时查看净暴露与总暴露。"),
    Concept("C33", 5, "动态Delta对冲", "Dynamic Delta Hedging", "根据模型 Delta 买卖标的并持续再平衡，使头寸在局部保持方向中性，并把价格路径转化为调整现金流。", (8, 13, 25), r"$$n_{\mathrm{hedge}}=-\Delta_{\mathrm{option}}$$\n$$dV\approx\Delta\,dS+\tfrac12\Gamma(dS)^2+\Theta\,dt+\mathrm{Vega}\,d\sigma$$", "设定时间或 Delta 阈值并计入滑点；Delta 中性不消除 Gamma、Vega、跳空、模型和流动性风险。"),

    Concept("C34", 6, "垂直价差与牛熊价差", "Vertical, Bull, and Bear Spreads", "同到期、不同执行价期权的多空组合，用有限成本换取有界方向性收益。", (10, 12), r"$$\Pi=(S_T-K_1)^+-(S_T-K_2)^+-\text{Net Premium}$$", "核对最大盈亏、盈亏平衡点、腿间流动性和提前指派；有界到期损失不代表持有期保证金不变。"),
    Concept("C35", 6, "跨式与宽跨式", "Straddles and Strangles", "同时持有相同或不同执行价的看涨和看跌，主要表达实际波动相对入场隐含波动的观点。", (11, 23), r"$$\Pi_{\mathrm{long\ straddle}}=|S_T-K|-(C_0+P_0)$$", "不能只判断方向幅度；要比较隐含波动率、时间衰减、偏斜、再对冲成本和达到盈亏平衡所需路径。"),
    Concept("C36", 6, "蝶式与鹰式", "Butterflies and Condors", "由多个执行价构造的局部曲率头寸，可表达到期价格区间、偏斜曲率或中间执行价相对价值。", (11, 12, 14), r"$$\Pi_{\mathrm{butterfly}}=(S_T-K_1)^+-2(S_T-K_2)^++(S_T-K_3)^+-\text{Cost}$$", "检查翼宽、执行价间距、远端报价和结算跳点；多腿中间价收益常无法同时成交。"),
    Concept("C37", 6, "日历与对角价差", "Calendar and Diagonal Spreads", "使用不同到期、必要时也使用不同执行价的期权，交易期限结构、远期波动率和不同期限时间衰减。", (11,), "", "不同期限 Vega 不能简单相减；压力测试近月事件、曲面非平行移动、展期和近月 Gamma 集中。"),
    Concept("C38", 6, "比率价差与圣诞树", "Ratio Spreads and Christmas Trees", "以不等数量组合不同执行价期权，形成非对称、通常带尾部暴露的损益与 Greeks 形状。", (11, 12), "", "明确远端裸卖腿和最大尾部损失；检查指派、保证金跃升、偏斜变化与极端行情流动性。"),
    Concept("C39", 6, "保护性备兑与领式", "Protective Options, Covered Writes, and Collars", "保护性看跌为多头标的设置下行地板，备兑看涨用上行权利换取权利金，领式把两者组合成区间保护。", (17, 24), r"$$S_T+(K-S_T)^+=\max(S_T,K)$$", "计入上行封顶、股息、税务、提前指派和展期成本；“备兑”不等于下跌风险已被覆盖。"),
    Concept("C40", 6, "合成与箱式套利", "Synthetics, Boxes, and Rolls", "利用看涨看跌平价把期权组合复制为标的、债券或固定到期现金流，并交易相对价格偏离。", (14, 15), r"$$\text{Box payoff}=K_2-K_1,\qquad \text{Fair box price}=(K_2-K_1)e^{-rT}$$", "先做可执行四腿价格和资金占用；重点检查腿风险、借券、提前行权、钉住和结算价。"),
    Concept("C41", 6, "策略选择与调整", "Strategy Selection and Adjustment", "在预期收益、Greeks、尾部情景、流动性和风险承受能力之间选择头寸，并随市场变化调整，而非仅追求最大理论优势。", (11, 12, 13, 21), "", "要求策略前记录退出条件、调整规则、最坏情景、成本预算和不可对冲风险；避免事后改变交易论点。"),

    Concept("C42", 7, "提前行权指派与钉住风险", "Exercise, Assignment, and Pin Risk", "美式持有人可能提前行权，卖方可能被指派；临近执行价到期时，最终标的头寸和指派数量可能不确定。", (3, 15, 16), r"$$\text{Exercise when Intrinsic Value}>\text{Continuation Value}$$", "除息日前、深度价内和到期附近逐腿检查；为隔夜意外标的头寸、借券和保证金预留容量。"),
    Concept("C43", 7, "流动性执行与结算风险", "Liquidity, Execution, and Settlement Risk", "买卖价差、冲击成本、费用、保证金、腿风险和结算规则决定理论优势能否转化为可实现利润。", (3, 8, 13, 15, 23, 25), r"$$\text{Net Edge}=\text{Theoretical Edge}-\text{Spread}-\text{Fees}-\text{Impact}-\text{Funding}$$", "用可成交深度而非屏幕中间价；压力测试流动性消失、涨跌停、经纪商提高保证金和结算争议。"),
    Concept("C44", 7, "指数期货期权与指数套利", "Index Futures, Options, and Arbitrage", "指数产品把成分股篮子风险转化为期货和期权暴露，期货公允价值、篮子复制和指数基差构成指数套利框架。", (22,), r"$$F_{\mathrm{index}}=S_{\mathrm{index}}e^{(r-q)T},\qquad b=S-F$$", "核对指数除数、成分调整、股息预测、篮子成交、跟踪误差、现货与期货交易时间差。"),
    Concept("C45", 7, "波动率合约方差掉期与VIX", "Volatility Contracts, Variance Swaps, and VIX", "已实现波动率或方差合约直接按观察期结果结算；VIX 及其期货期权提供基于期权条带的隐含波动率暴露。", (25,), r"$$\mathrm{Payoff}_{\mathrm{variance}}=N_{\mathrm{var}}\left(\sigma^2_{\mathrm{real}}-K_{\mathrm{var}}\right)$$", "区分波动率与方差名义金额；核对结算窗口、VIX 现货与期货基差、期限结构、凸性和复制误差。"),
)


EDGES = (
    Edge("C01", "作为标的", "C02", "远期和期货是标的资产的线性未来交割合约。"),
    Edge("C10", "提供无套利交割基准", "C02", "远期价格把现货和持有成本映射为合约的理论交割价。"),
    Edge("C02", "作为指数线性工具", "C44", "指数期货为篮子替代、基差和指数套利提供可交易载体。"),
    Edge("C01", "作为标的", "C03", "期权价值依附于标的价格。"),
    Edge("C04", "定义价格层级", "C03", "行权价决定权利生效的价格门槛。"),
    Edge("C05", "定义期限与权利", "C03", "到期时间和行权方式限定可执行权利。"),
    Edge("C13", "定义履约方式", "C03", "结算与指派规则决定期权如何转成现金或头寸。"),
    Edge("C01", "共同决定到期价值", "C07", "到期标的价格进入每一腿的收益函数。"),
    Edge("C04", "设置损益折点", "C07", "执行价是非线性收益曲线的折点。"),
    Edge("C05", "确定结算时点", "C07", "期限决定静态损益图的观察终点。"),
    Edge("C06", "作为初始现金流平移", "C07", "权利金把收益曲线变为净损益曲线。"),
    Edge("C13", "转化为实际现金流", "C07", "结算方式决定最终现金或标的头寸。"),

    Edge("C01", "提供现货输入", "C10", "远期价格从现货和持有成本出发。"),
    Edge("C08", "通过融资成本决定", "C10", "资金成本抬高持有标的至未来的成本。"),
    Edge("C09", "通过持有收益调整", "C10", "股息或便利收益降低净持有成本。"),
    Edge("C11", "约束", "C10", "可复制现金流限制远期偏离公允持有成本。"),
    Edge("C11", "约束", "C12", "平价关系来自相同到期现金流的无套利等价。"),
    Edge("C12", "提供复制恒等式", "C40", "合成和箱式结构由平价关系构造。"),
    Edge("C11", "偏离时触发", "C40", "只有可执行价格越过成本调整后的边界才形成套利机会。"),
    Edge("C13", "产生事件风险", "C42", "指派和结算时点造成不确定头寸。"),
    Edge("C08", "改变机会成本", "C42", "利率改变提前支付行权价的成本。"),
    Edge("C09", "改变持有收益", "C42", "除息事件可能改变看涨期权提前行权判断。"),
    Edge("C43", "放宽可执行边界", "C11", "摩擦使小幅理论偏离无法锁定利润。"),
    Edge("C43", "把恒等式转成实施风险", "C40", "多腿成交、融资和结算会破坏理论锁定。"),

    Edge("C14", "提供概率结构", "C21", "理论价值依赖未来状态及其权重。"),
    Edge("C14", "定义统计度量框架", "C15", "收益分布、均值和方差是历史与已实现波动率的统计基础。"),
    Edge("C14", "假设偏离传导为", "C25", "跳空、厚尾与非对称分布会使连续对数正态模型产生结构误差。"),
    Edge("C15", "提供统计样本", "C16", "历史与近期实现路径是预测输入而非预测本身。"),
    Edge("C16", "提供波动率假设", "C22", "预测波动率可作为正向估值输入。"),
    Edge("C16", "提供波动率假设", "C23", "树模型的节点幅度需要波动率假设。"),
    Edge("C22", "计算", "C21", "Black–Scholes 把输入映射为理论价值。"),
    Edge("C23", "计算", "C21", "风险中性回溯生成节点理论价值。"),
    Edge("C23", "通过节点回溯估计", "C24", "每个节点比较行权价值与继续持有价值。"),
    Edge("C24", "加入提前行权选择权", "C21", "美式价值包含最优停止权。"),
    Edge("C06", "经模型反解为", "C17", "市场权利金在给定其他输入后映射成隐含波动率。"),
    Edge("C22", "提供反解机制", "C17", "隐波是模型依赖的报价坐标。"),
    Edge("C17", "沿到期日排列形成", "C18", "同一标的不同期限的隐波构成期限结构。"),
    Edge("C17", "沿行权价排列形成", "C19", "同一期限跨执行价隐波构成偏斜。"),
    Edge("C19", "编码尾部形状", "C20", "偏斜和曲率对应风险中性分布的非对称与尾部。"),
    Edge("C20", "揭示假设偏离", "C25", "偏度和峰度说明单一对数正态分布不足。"),
    Edge("C25", "使估值带有不确定性", "C21", "理论价值随模型选择和参数误差变化。"),
    Edge("C15", "相对入场隐波决定波动捕获", "C33", "实现路径与入场定价的差异通过再平衡损益体现。"),
    Edge("C17", "设定波动交易盈亏平衡基准", "C33", "入场隐波决定时间价值与预期调整收入的平衡。"),
    Edge("C18", "提供期限相对价值维度", "C37", "日历和对角价差交易不同区间的总方差。"),
    Edge("C19", "提供跨行权价相对价值维度", "C36", "蝶式和鹰式对曲面曲率敏感。"),
    Edge("C19", "提供尾部定价维度", "C38", "比率结构常暴露于远端偏斜。"),
    Edge("C39", "通过对冲供需塑造", "C19", "保护性看跌买盘和备兑看涨供给影响股票偏斜。"),
    Edge("C15", "作为结算基础", "C45", "已实现波动率或方差合约按观察结果结算。"),
    Edge("C17", "作为定价基础", "C45", "VIX 及隐含波动率产品来自期权价格。"),
    Edge("C03", "通过跨行权价组合复制", "C45", "期权条带可近似复制方差暴露。"),

    Edge("C22", "导出局部敏感度", "C26", "模型对标的价格求一阶敏感度。"),
    Edge("C22", "导出局部敏感度", "C27", "模型对标的价格求二阶敏感度。"),
    Edge("C22", "导出局部敏感度", "C28", "模型衡量时间流逝的局部影响。"),
    Edge("C22", "导出局部敏感度", "C29", "模型衡量波动率输入变化的局部影响。"),
    Edge("C22", "导出局部敏感度", "C30", "模型衡量利率输入变化的局部影响。"),
    Edge("C23", "以节点差分估计", "C26", "树上价值变化可估计 Delta。"),
    Edge("C23", "以节点差分估计", "C27", "相邻 Delta 变化可估计 Gamma。"),
    Edge("C25", "造成敏感度误差", "C32", "模型误设会让组合 Greeks 低估或错配真实风险。"),
    Edge("C26", "决定对冲数量", "C33", "Delta 是局部等价标的头寸。"),
    Edge("C27", "决定Delta漂移速度", "C26", "Gamma 把标的变动传导为 Delta 变化。"),
    Edge("C27", "提高再平衡需求", "C33", "高 Gamma 使对冲更快失衡。"),
    Edge("C27", "通常伴随反向暴露", "C28", "同一模型条件下正 Gamma 通常伴随负 Theta。"),
    Edge("C05", "通过时间流逝实现", "C28", "剩余期限减少会改变期权价值。"),
    Edge("C17", "变化时经由Vega传导", "C29", "隐波平移首先表现为 Vega 损益。"),
    Edge("C08", "变化时经由Rho传导", "C30", "利率变化影响贴现和远期。"),
    Edge("C26", "与价格共同定义", "C31", "Lambda 将绝对 Delta 转为百分比弹性。"),
    Edge("C31", "汇总为百分比杠杆", "C32", "Lambda 为组合提供资本敏感的方向暴露视角。"),
    Edge("C31", "约束资本与头寸规模", "C41", "高弹性头寸需与最大损失、保证金和可退出性一起决定规模。"),
    Edge("C26", "汇总为组合暴露", "C32", "各腿 Delta 按数量和乘数相加。"),
    Edge("C27", "汇总为组合暴露", "C32", "各腿 Gamma 形成组合凸性。"),
    Edge("C28", "汇总为组合暴露", "C32", "各腿 Theta 形成时间衰减预算。"),
    Edge("C29", "汇总为组合暴露", "C32", "各腿 Vega 形成波动率风险。"),
    Edge("C30", "汇总为组合暴露", "C32", "各腿 Rho 形成利率风险。"),
    Edge("C32", "约束", "C41", "组合风险限额决定可选策略、规模和调整。"),
    Edge("C33", "局部中和", "C26", "再平衡把净 Delta 拉回目标区间。"),
    Edge("C33", "通过换手产生", "C43", "每次再平衡消耗价差、费用和市场冲击。"),
    Edge("C43", "造成离散对冲误差", "C33", "跳空、滑点和市场关闭使理论对冲无法连续执行。"),

    Edge("C34", "主要形成方向暴露", "C26", "垂直价差用有界损益表达看多或看空观点。"),
    Edge("C34", "塑造有界到期损益", "C07", "两个执行价限定最大收益与损失。"),
    Edge("C35", "多头通常形成正凸性", "C27", "多头跨式和宽跨式受益于大幅运动。"),
    Edge("C35", "多头通常形成正波动率暴露", "C29", "隐波上升通常提高多头结构价值。"),
    Edge("C35", "多头通常承担时间衰减", "C28", "若运动不足，权利金随时间损耗。"),
    Edge("C36", "表达局部曲率", "C27", "多执行价结构把 Gamma 集中在特定区间。"),
    Edge("C37", "交易期限结构", "C18", "不同到期腿比较不同区间总方差。"),
    Edge("C38", "可能形成非对称尾部凸性", "C27", "不等数量使一侧远端风险突出。"),
    Edge("C39", "变换标的方向风险", "C26", "保护、备兑和领式改变组合 Delta。"),
    Edge("C40", "承担多腿执行风险", "C43", "理论锁定仍依赖同时成交和持仓能力。"),
    Edge("C34", "汇总成风险画像", "C32", "策略必须还原为组合 Greeks 与情景损益。"),
    Edge("C35", "汇总成风险画像", "C32", "波动率策略不能只用名称判断风险。"),
    Edge("C36", "汇总成风险画像", "C32", "曲率结构的风险随标的和期限变化。"),
    Edge("C37", "汇总成风险画像", "C32", "跨期风险需要期限分桶。"),
    Edge("C38", "汇总成风险画像", "C32", "尾部裸露必须进入全重估情景。"),
    Edge("C39", "汇总成风险画像", "C32", "保护头寸仍保留残余方向与波动率风险。"),
    Edge("C40", "汇总成风险画像", "C32", "套利结构也占用融资、保证金和流动性限额。"),
    Edge("C43", "限制可交易性", "C41", "成本和深度决定理论策略能否实施。"),
    Edge("C42", "施加事件约束", "C41", "临近到期和除息时策略可能被指派拆解。"),

    Edge("C10", "提供基差框架", "C44", "指数期货公允价值来自现货、融资和股息。"),
    Edge("C11", "约束指数相对价格", "C44", "篮子、期货和指数期权由复制关系联系。"),
    Edge("C44", "暴露于跟踪与篮子执行", "C43", "复制指数需要真实成分股成交。"),
    Edge("C45", "提供直接波动率暴露", "C29", "波动率和方差产品减少逐期权管理但仍有波动率敏感度。"),
    Edge("C18", "塑造期货期限结构", "C45", "VIX 期货反映不同到期的波动率定价。"),
    Edge("C45", "承担结算与复制风险", "C43", "观察窗口、公式与流动性影响最终实现。"),
)


MAIN_NODES = (
    ("A", "合约条款与现金流"),
    ("B", "远期与持有成本"),
    ("C", "无套利与合成复制"),
    ("D", "分布与已实现波动率"),
    ("E", "隐含波动率与曲面"),
    ("F", "理论估值"),
    ("G", "模型风险"),
    ("H", "Greeks与组合暴露"),
    ("I", "动态对冲"),
    ("J", "策略风险形状"),
    ("K", "策略选择与调整"),
    ("L", "市场摩擦与事件风险"),
    ("M", "指数衍生品"),
    ("N", "波动率产品"),
)

MAIN_EDGES = (
    ("A", "提供现货和合约输入", "B"),
    ("B", "建立相对价格基准", "C"),
    ("D", "提供未来波动率假设", "F"),
    ("A", "提供条款输入", "F"),
    ("B", "提供贴现与远期输入", "F"),
    ("F", "经市场价格反解", "E"),
    ("E", "揭示分布偏离", "G"),
    ("F", "导出局部敏感度", "H"),
    ("G", "造成敏感度误差", "H"),
    ("H", "决定再平衡数量", "I"),
    ("D", "经价格路径产生对冲损益", "I"),
    ("E", "形成波动率相对价值", "J"),
    ("C", "提供合成和套利结构", "J"),
    ("J", "汇总为组合风险", "H"),
    ("H", "施加风险限额", "K"),
    ("L", "限制可交易性", "K"),
    ("L", "造成离散对冲误差", "I"),
    ("B", "提供指数基差", "M"),
    ("E", "提供隐含波动率基准", "N"),
    ("D", "提供到期结算", "N"),
)


def concept_map() -> dict[str, Concept]:
    return {c.cid: c for c in CONCEPTS}


def c_link(cid: str, label: str | None = None) -> str:
    concept = concept_map()[cid]
    return f"[[{concept.stem}|{label or concept.title}]]"


def chapter_link(number: int) -> str:
    stem, label = CHAPTERS[number]
    return f"[[{stem}|{label}]]"


def yaml_escape(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def render_root() -> str:
    lines = [
        "---",
        f"title: {yaml_escape('期权知识图谱 / Option Knowledge Graph')}",
        "tags: [期权知识图谱, 总图]",
        f"generated_by: {yaml_escape(GENERATOR)}",
        "---",
        "",
        "# 期权知识图谱 / Option Knowledge Graph",
        "",
        "> [!abstract] 使用方法",
        "> 这不是章节目录，而是从合约定义到风险落地的因果地图。先选择一个层级，再沿带有关系动词的概念链接向上追溯输入、向下追踪风险传导。",
        f"> 全图包含 7 个知识层、45 个核心概念和 {len(EDGES)} 条语义关系；封面、版权、献词、作者、导航与审计文件不进入本网络。",
        "",
        "> [!tip] Obsidian 局部关系图",
        "> 打开本页的“局部关系图”，在搜索过滤器输入 `path:\"Option Volatility and Pricing 双语版/知识图谱\"`：深度 2 显示“总图 → 知识层 → 概念”。概念页中的“主要章节”可直接跳转到教材；封面、版权、导航和审计页不会进入该过滤结果。",
        "",
        "## 七层入口",
        "",
    ]
    for layer in LAYERS:
        lines.append(f"{layer.number}. [[{layer.stem}|{layer.title} / {layer.english}]] — {layer.question}")
    lines += [
        "",
        "## 主因果图",
        "",
        "```mermaid",
        "flowchart TB",
    ]
    for node, label in MAIN_NODES:
        lines.append(f'    {node}["{label}"]')
    for source, verb, target in MAIN_EDGES:
        lines.append(f'    {source} -->|"{verb}"| {target}')
    lines += [
        "```",
        "",
        "## 六条风险传导主链",
        "",
        "1. 现货、利率与股息 → 远期价格 → 无套利边界 → 平价与合成 → 套利实施。",
        "2. 概率分布与波动率预测 → 估值模型 → 理论价值 → 市场价格差异 → 策略。",
        "3. 市场权利金与模型 → 隐含波动率 → 期限结构与偏斜 → 相对价值策略。",
        "4. 标的变动 → Delta → Gamma 导致 Delta 漂移 → 动态再对冲 → 对冲损益。",
        "5. 隐含波动率变化 → Vega → 组合风险 → 波动率价差与调整。",
        "6. 模型假设失效 → Greeks 偏差 → 离散对冲误差 → 流动性和执行损失。",
        "",
        "## 曲面因子与主要策略表达",
        "",
        "| 曲面因子 | 主要策略表达 | 核心风险传导 | 不能忽略的剩余风险 |",
        "|---|---|---|---|",
        "| 整体水平 Level | 跨式、宽跨式、Delta 对冲期权组合 | Vega → 盯市损益；Gamma → 再平衡损益 | Theta、实现波动率、交易成本 |",
        "| 偏斜 Skew | 比率价差、风险逆转、保护性结构 | 翼部隐波 → 非对称 Vega/Gamma | 尾部跳空、翼部流动性 |",
        "| 曲率 Curvature | 蝶式、鹰式 | 中间与翼部相对价值 → 局部 Gamma | 厚尾、插值和多腿成交 |",
        "| 期限结构 Term | 日历价差、对角价差 | 总方差差额 → 远期波动率 | 近月 Gamma/Theta、事件日、展期 |",
        "| 已实现方差 | Delta 对冲跨式、方差/波动率合约 | 价格路径 → 调整现金流或结算 | 采样频率、跳空、复制误差 |",
        "",
        "## 组合损益归因骨架",
        "",
        "$$",
        "\\Delta V \\approx \\Delta\\,\\Delta S + \\frac{1}{2}\\Gamma(\\Delta S)^2 + \\Theta\\,\\Delta t + \\mathrm{Vega}\\,\\Delta\\sigma + \\rho\\,\\Delta r - TC + \\varepsilon",
        "$$",
        "",
        "其中 $TC$ 是价差、手续费与市场冲击，$\\varepsilon$ 是模型、曲面、跳空、离散对冲和数据误差等无法解释残差。",
        "",
        "> [!warning] 解释边界",
        "> 远期价格不是未来现货预测；隐含波动率不决定未来已实现波动率；Delta 中性也不等于无风险。",
        "",
    ]
    return "\n".join(lines)


def mermaid_id(cid: str) -> str:
    concept = concept_map()[cid]
    return "".join(re.findall(r"[A-Za-z0-9]+", concept.english))


def render_layer(layer: Layer) -> str:
    cmap = concept_map()
    local = [c for c in CONCEPTS if c.layer == layer.number]
    local_ids = {c.cid for c in local}
    internal = [e for e in EDGES if e.source in local_ids and e.target in local_ids]
    boundary = [e for e in EDGES if (e.source in local_ids) ^ (e.target in local_ids)]
    lines = [
        "---",
        f"title: {yaml_escape(layer.title + ' / ' + layer.english)}",
        f"graph_layer: {layer.number}",
        "tags: [期权知识图谱, 层级]",
        f"generated_by: {yaml_escape(GENERATOR)}",
        "---",
        "",
        f"# 第{layer.number}层：{layer.title} / {layer.english}",
        "",
        f"> [!question] {layer.question}",
        f"> {layer.summary}",
        "",
        "## 本层核心概念",
        "",
    ]
    for concept in local:
        lines.append(f"- {c_link(concept.cid)} — {concept.definition.split('。')[0]}。")
    lines += ["", "## 本层关系图", "", "```mermaid", "flowchart LR"]
    for concept in local:
        lines.append(f'    {mermaid_id(concept.cid)}["{concept.title}"]')
    if internal:
        for edge in internal:
            lines.append(f'    {mermaid_id(edge.source)} -->|"{edge.verb}"| {mermaid_id(edge.target)}')
    else:
        lines.append("    %% 本层概念主要通过下方跨层接口形成依赖。")
    lines += ["```", "", "## 跨层接口", ""]
    for edge in boundary:
        lines.append(f"- {c_link(edge.source)} **—{edge.verb}→** {c_link(edge.target)}：{edge.detail}")
    lines += ["", "## 风险经理阅读顺序", ""]
    if layer.number == 1:
        lines += ["1. 先核对条款和结算，再看权利金与到期损益。", "2. 把静态损益图与持有期风险分开。"]
    elif layer.number == 2:
        lines += ["1. 先建立可交易的远期和融资基准。", "2. 再判断平价偏离是否覆盖全部实施成本。"]
    elif layer.number == 3:
        lines += ["1. 严格区分历史、未来实现、预测和隐含波动率。", "2. 再沿期限与行权价两个维度检查曲面。"]
    elif layer.number == 4:
        lines += ["1. 记录模型输入与假设。", "2. 用替代模型和压力情景量化模型误差。"]
    elif layer.number == 5:
        lines += ["1. 统一单位后汇总 Greeks。", "2. 用全重估情景检查局部近似和动态对冲失效。"]
    elif layer.number == 6:
        lines += ["1. 把策略名称还原成腿、Greeks 和到期损益。", "2. 用成本、尾部和调整规则筛选策略。"]
    else:
        lines += ["1. 用真实成交和结算规则重算理论优势。", "2. 为事件、流动性和不可复制风险设置独立限额。"]
    lines.append("")
    return "\n".join(lines)


def render_concept(concept: Concept) -> str:
    outgoing = [e for e in EDGES if e.source == concept.cid]
    incoming = [e for e in EDGES if e.target == concept.cid]
    lines = [
        "---",
        f"title: {yaml_escape(concept.title + ' / ' + concept.english)}",
        f"graph_layer: {concept.layer}",
        "tags: [期权知识图谱, 核心概念]",
        f"generated_by: {yaml_escape(GENERATOR)}",
        "---",
        "",
        f"# {concept.title} / {concept.english}",
        "",
        f"> [!definition] 定义",
        f"> {concept.definition}",
        "",
        "## 核心关系",
        "",
    ]
    if outgoing:
        lines.append("### 向下游传导")
        lines.append("")
        for edge in outgoing:
            lines.append(f"- **{edge.verb} →** {c_link(edge.target)}：{edge.detail}")
        lines.append("")
    if incoming:
        lines.append("### 受上游约束")
        lines.append("")
        for edge in incoming:
            lines.append(f"- {c_link(edge.source)} **—{edge.verb}→ 本概念**：{edge.detail}")
        lines.append("")
    if concept.formula:
        lines += ["## 关键公式", "", concept.formula, ""]
    lines += [
        "## 风险经理检查",
        "",
        f"- {concept.risk_check}",
        "- 把模型数值与可成交价格、压力情景和头寸规模一起复核。",
        "",
        "## 主要章节",
        "",
    ]
    for chapter in concept.chapters:
        lines.append(f"- {chapter_link(chapter)}")
    lines.append("")
    return "\n".join(lines)


def validate() -> None:
    cmap = concept_map()
    if len(CONCEPTS) != 45 or set(cmap) != {f"C{i:02d}" for i in range(1, 46)}:
        raise ValueError("Concept IDs must be exactly C01..C45")
    if len(LAYERS) != 7 or {layer.number for layer in LAYERS} != set(range(1, 8)):
        raise ValueError("Graph must contain exactly seven layers")
    if len(MAIN_NODES) > 20:
        raise ValueError("Main Mermaid graph must stay below 20 aggregate nodes")
    for concept in CONCEPTS:
        if concept.layer not in range(1, 8):
            raise ValueError(f"Invalid layer for {concept.cid}")
        missing = set(concept.chapters) - set(CHAPTERS)
        if missing:
            raise ValueError(f"Unknown chapters for {concept.cid}: {sorted(missing)}")
    for edge in EDGES:
        if edge.source not in cmap or edge.target not in cmap:
            raise ValueError(f"Unknown concept in edge: {edge}")
        if not edge.verb or edge.verb in {"相关", "参见", "链接"}:
            raise ValueError(f"Non-semantic edge verb: {edge}")
    forbidden = ("封面", "版权", "献词", "作者", "阅读导航", "翻译说明", "原书目录", "审计")
    rendered = [render_root()]
    rendered.extend(render_layer(layer) for layer in LAYERS)
    rendered.extend(render_concept(concept) for concept in CONCEPTS)
    wiki_target = re.compile(r"\[\[([^\]|#]+)")
    for text in rendered:
        for target in wiki_target.findall(text):
            if any(word in target for word in forbidden):
                raise ValueError(f"Forbidden graph target: {target}")
    root_targets = set(wiki_target.findall(rendered[0]))
    expected_layers = {layer.stem for layer in LAYERS}
    if root_targets != expected_layers:
        raise ValueError(f"Root must link only seven layer notes: {root_targets}")


def write_files() -> list[Path]:
    validate()
    OUT.mkdir(parents=True, exist_ok=True)
    documents: dict[str, str] = {"期权知识图谱.md": render_root()}
    documents.update({f"{layer.stem}.md": render_layer(layer) for layer in LAYERS})
    documents.update({f"{concept.stem}.md": render_concept(concept) for concept in CONCEPTS})
    expected = set(documents)
    for path in OUT.glob("*.md"):
        if path.name not in expected and f'generated_by: "{GENERATOR}"' in path.read_text(encoding="utf-8"):
            path.unlink()
    written = []
    for name, body in sorted(documents.items()):
        path = OUT / name
        path.write_text(body.rstrip() + "\n", encoding="utf-8")
        written.append(path)
    actual = list(OUT.glob("*.md"))
    if len(actual) != 53:
        raise RuntimeError(f"Expected 53 Markdown files, found {len(actual)}")
    return written


def main() -> None:
    files = write_files()
    print(f"knowledge graph generated: {len(files)} Markdown files")
    print("  root: 1")
    print("  layer MOCs: 7")
    print("  concept notes: 45")
    print(f"  semantic edges: {len(EDGES)}")
    print(f"  output: {OUT}")


if __name__ == "__main__":
    main()
