"""Ordered stems of the 25 bilingual chapter files (no serial prefixes)."""

CHAPTER_STEMS = (
    "金融合约 Financial Contracts",
    "远期定价 Forward Pricing",
    "合约规格与期权术语 Contract Specifications and Option Terminology",
    "到期盈亏 Expiration Profit and Loss",
    "理论定价模型 Theoretical Pricing Models",
    "波动率 Volatility",
    "风险度量（一） Risk Measurement I",
    "动态对冲 Dynamic Hedging",
    "风险度量（二） Risk Measurement II",
    "价差策略导论 Introduction to Spreading",
    "波动率价差策略 Volatility Spreads",
    "牛市与熊市价差 Bull and Bear Spreads",
    "风险考量 Risk Considerations",
    "合成头寸 Synthetics",
    "期权套利 Option Arbitrage",
    "美式期权的提前行权 Early Exercise of American Options",
    "使用期权进行对冲 Hedging with Options",
    "Black–Scholes 模型 The Black-Scholes Model",
    "二叉树期权定价 Binomial Option Pricing",
    "再论波动率 Volatility Revisited",
    "头寸分析 Position Analysis",
    "股票指数期货与期权 Stock Index Futures and Options",
    "模型与现实世界 Models and the Real World",
    "波动率偏斜 Volatility Skews",
    "波动率合约 Volatility Contracts",
)


# Footnote id prefixes (ovpNN) used by convert/audit footnote scripts.
# Ordered stems give chapters 1..25; retained appendices keep their legacy numbers.
FOOTNOTE_PREFIX_OVERRIDES = {
    "附录A-期权术语表 Glossary of Option Terminology": "ovp27",
    "附录B-实用数学 Some Useful Math": "ovp28",
}


def footnote_prefix(path) -> str:
    """Return the ovpNN footnote prefix for a book file (frontmatter chapter first)."""
    import re as _re
    try:
        text = path.read_text(encoding="utf-8")
        m = _re.search(r"^chapter:\s*(\d{1,2})\s*$", text, _re.M)
        if m:
            return f"ovp{int(m.group(1)):02d}"
    except Exception:
        pass
    override = FOOTNOTE_PREFIX_OVERRIDES.get(path.stem)
    if override:
        return override
    m2 = _re.match(r"(\d{2})", path.name)
    return f"ovp{m2.group(1)}" if m2 else "ovp"
