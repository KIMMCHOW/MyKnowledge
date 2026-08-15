#!/usr/bin/env python3
"""Generate reproducible payoff charts for the option-strategy notes.

The script intentionally uses only the Python standard library.  Each chart
compares a strategy's model value before expiry with its value at the relevant
expiry date.  Premiums are Black--Scholes values at entry, so every curve is a
profit/loss curve rather than a raw payoff curve.

Conventions
-----------
* Values are per share and exclude fees, financing, early exercise and changes
  in implied volatility.
* Same-expiry strategies are opened with 90 calendar days remaining, observed
  with 30 days remaining, and then valued at expiry.
* Calendar and diagonal spreads use a 90-day near leg and a 180-day far leg.
  Time butterflies use equally spaced 90-, 120- and 150-day legs.  Multi-expiry
  strategies are observed when the near leg has 30 days left; the solid curve
  is the near-leg expiry date.
* Stock legs use ``quantity * (S - S0)``.  Option legs use the change from the
  entry model value to the evaluation model value.

Run from anywhere with::

    python3 scripts/generate_option_strategy_payoff_charts.py
"""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
import math
from pathlib import Path
import xml.etree.ElementTree as ET


S0 = 100.0
RATE = 0.02
DIVIDEND_YIELD = 0.0
VOLATILITY = 0.25
DAYS_PER_YEAR = 365.0

ENTRY_DAYS = 90
OBSERVATION_ELAPSED_DAYS = 60
KEY_ELAPSED_DAYS = 90
FAR_DAYS = 180
TIME_FLY_MIDDLE_DAYS = 120
TIME_FLY_FAR_DAYS = 150

X_MIN = 50.0
X_MAX = 150.0
SAMPLE_COUNT = 401


@dataclass(frozen=True)
class OptionLeg:
    kind: str
    quantity: float
    strike: float
    maturity_days: int = ENTRY_DAYS

    def __post_init__(self) -> None:
        if self.kind not in {"call", "put"}:
            raise ValueError(f"unsupported option kind: {self.kind}")
        if self.maturity_days <= 0:
            raise ValueError("maturity_days must be positive")


@dataclass(frozen=True)
class Strategy:
    asset_stem: str
    title: str
    construction: str
    option_legs: tuple[OptionLeg, ...]
    stock_quantity: float = 0.0

    @property
    def has_multiple_expiries(self) -> bool:
        return len({leg.maturity_days for leg in self.option_legs}) > 1


def call(quantity: float, strike: float, maturity_days: int = ENTRY_DAYS) -> OptionLeg:
    return OptionLeg("call", quantity, strike, maturity_days)


def put(quantity: float, strike: float, maturity_days: int = ENTRY_DAYS) -> OptionLeg:
    return OptionLeg("put", quantity, strike, maturity_days)


STRATEGIES: tuple[Strategy, ...] = (
    Strategy(
        "看涨期权 Call",
        "多头看涨期权 / Long Call",
        "代表构造：多头看涨（买入 1 份 K=100 Call）",
        (call(+1, 100),),
    ),
    Strategy(
        "看跌期权 Put",
        "多头看跌期权 / Long Put",
        "代表构造：多头看跌（买入 1 份 K=100 Put）",
        (put(+1, 100),),
    ),
    Strategy(
        "空头看涨期权 Short Call",
        "空头看涨期权 / Short Call",
        "代表构造：空头看涨（卖出 1 份 K=100 Call）",
        (call(-1, 100),),
    ),
    Strategy(
        "空头看跌期权 Short Put",
        "空头看跌期权 / Short Put",
        "代表构造：空头看跌（卖出 1 份 K=100 Put）",
        (put(-1, 100),),
    ),
    Strategy(
        "看涨垂直价差 Vertical Call",
        "牛市看涨垂直价差 / Bull Call Spread",
        "代表构造：牛市借记价差（买 K=95 Call，卖 K=105 Call）",
        (call(+1, 95), call(-1, 105)),
    ),
    Strategy(
        "看跌垂直价差 Vertical Put",
        "熊市看跌垂直价差 / Bear Put Spread",
        "代表构造：熊市借记价差（买 K=105 Put，卖 K=95 Put）",
        (put(+1, 105), put(-1, 95)),
    ),
    Strategy(
        "熊市看涨垂直价差 Bear Call Spread",
        "熊市看涨垂直价差 / Bear Call Spread",
        "代表构造：熊市信用价差（卖 K=95 Call，买 K=105 Call）",
        (call(-1, 95), call(+1, 105)),
    ),
    Strategy(
        "牛市看跌垂直价差 Bull Put Spread",
        "牛市看跌垂直价差 / Bull Put Spread",
        "代表构造：牛市信用价差（卖 K=105 Put，买 K=95 Put）",
        (put(-1, 105), put(+1, 95)),
    ),
    Strategy(
        "看涨日历价差 Calendar Call",
        "多头看涨日历价差 / Long Call Calendar Spread",
        "代表构造：卖近月 K=100 Call，买远月 K=100 Call",
        (call(-1, 100, ENTRY_DAYS), call(+1, 100, FAR_DAYS)),
    ),
    Strategy(
        "看跌日历价差 Calendar Put",
        "多头看跌日历价差 / Long Put Calendar Spread",
        "代表构造：卖近月 K=100 Put，买远月 K=100 Put",
        (put(-1, 100, ENTRY_DAYS), put(+1, 100, FAR_DAYS)),
    ),
    Strategy(
        "空头看涨日历价差 Short Call Calendar Spread",
        "空头看涨日历价差 / Short Call Calendar Spread",
        "代表构造：买近月 K=100 Call，卖远月 K=100 Call",
        (call(+1, 100, ENTRY_DAYS), call(-1, 100, FAR_DAYS)),
    ),
    Strategy(
        "空头看跌日历价差 Short Put Calendar Spread",
        "空头看跌日历价差 / Short Put Calendar Spread",
        "代表构造：买近月 K=100 Put，卖远月 K=100 Put",
        (put(+1, 100, ENTRY_DAYS), put(-1, 100, FAR_DAYS)),
    ),
    Strategy(
        "多头看涨时间蝶式 Long Call Time Butterfly",
        "多头看涨时间蝶式 / Long Call Time Butterfly",
        "代表构造（同 K=100）：−May Call +2 June Call −July Call",
        (
            call(-1, 100, ENTRY_DAYS),
            call(+2, 100, TIME_FLY_MIDDLE_DAYS),
            call(-1, 100, TIME_FLY_FAR_DAYS),
        ),
    ),
    Strategy(
        "空头看涨时间蝶式 Short Call Time Butterfly",
        "空头看涨时间蝶式 / Short Call Time Butterfly",
        "代表构造（同 K=100）：+May Call −2 June Call +July Call",
        (
            call(+1, 100, ENTRY_DAYS),
            call(-2, 100, TIME_FLY_MIDDLE_DAYS),
            call(+1, 100, TIME_FLY_FAR_DAYS),
        ),
    ),
    Strategy(
        "多头看跌时间蝶式 Long Put Time Butterfly",
        "多头看跌时间蝶式 / Long Put Time Butterfly",
        "代表构造（同 K=100）：−May Put +2 June Put −July Put",
        (
            put(-1, 100, ENTRY_DAYS),
            put(+2, 100, TIME_FLY_MIDDLE_DAYS),
            put(-1, 100, TIME_FLY_FAR_DAYS),
        ),
    ),
    Strategy(
        "空头看跌时间蝶式 Short Put Time Butterfly",
        "空头看跌时间蝶式 / Short Put Time Butterfly",
        "代表构造（同 K=100）：+May Put −2 June Put +July Put",
        (
            put(+1, 100, ENTRY_DAYS),
            put(-2, 100, TIME_FLY_MIDDLE_DAYS),
            put(+1, 100, TIME_FLY_FAR_DAYS),
        ),
    ),
    Strategy(
        "看涨对角价差 Diagonal Call",
        "多头看涨对角价差 / Long Call Diagonal Spread",
        "代表构造：卖近月 K=105 Call，买远月 K=95 Call",
        (call(-1, 105, ENTRY_DAYS), call(+1, 95, FAR_DAYS)),
    ),
    Strategy(
        "看跌对角价差 Diagonal Put",
        "多头看跌对角价差 / Long Put Diagonal Spread",
        "代表构造：卖近月 K=95 Put，买远月 K=105 Put",
        (put(-1, 95, ENTRY_DAYS), put(+1, 105, FAR_DAYS)),
    ),
    Strategy(
        "空头看涨对角价差 Short Call Diagonal Spread",
        "空头看涨对角价差 / Short Call Diagonal Spread",
        "代表构造：买近月 K=105 Call，卖远月 K=95 Call",
        (call(+1, 105, ENTRY_DAYS), call(-1, 95, FAR_DAYS)),
    ),
    Strategy(
        "空头看跌对角价差 Short Put Diagonal Spread",
        "空头看跌对角价差 / Short Put Diagonal Spread",
        "代表构造：买近月 K=95 Put，卖远月 K=105 Put",
        (put(+1, 95, ENTRY_DAYS), put(-1, 105, FAR_DAYS)),
    ),
    Strategy(
        "看涨比率价差 Ratio Call",
        "看涨正向比率价差 / Call Ratio Spread",
        "代表构造：1×2（买 1 份 K=95 Call，卖 2 份 K=110 Call）",
        (call(+1, 95), call(-2, 110)),
    ),
    Strategy(
        "看跌比率价差 Ratio Put",
        "看跌正向比率价差 / Put Ratio Spread",
        "代表构造：1×2（买 1 份 K=105 Put，卖 2 份 K=90 Put）",
        (put(+1, 105), put(-2, 90)),
    ),
    Strategy(
        "看涨反向比率价差 Call Ratio Backspread",
        "看涨反向比率价差 / Call Ratio Backspread",
        "代表构造：1×2（卖 1 份 K=95 Call，买 2 份 K=110 Call）",
        (call(-1, 95), call(+2, 110)),
    ),
    Strategy(
        "看跌反向比率价差 Put Ratio Backspread",
        "看跌反向比率价差 / Put Ratio Backspread",
        "代表构造：1×2（卖 1 份 K=105 Put，买 2 份 K=90 Put）",
        (put(-1, 105), put(+2, 90)),
    ),
    Strategy(
        "备兑看涨 Covered Call (Buy-Write)",
        "备兑看涨 / Covered Call (Buy/Write)",
        "代表构造：买入标的 + 卖出 1 份 K=105 Call",
        (call(-1, 105),),
        stock_quantity=+1,
    ),
    Strategy(
        "备兑看跌 Covered Put (Sell-Write)",
        "备兑看跌 / Covered Put (Sell/Write)",
        "代表构造：卖空标的 + 卖出 1 份 K=95 Put",
        (put(-1, 95),),
        stock_quantity=-1,
    ),
    Strategy(
        "保护性看涨 Protective Call",
        "保护性看涨 / Protective Call",
        "代表构造：卖空标的 + 买入 1 份 K=105 Call",
        (call(+1, 105),),
        stock_quantity=-1,
    ),
    Strategy(
        "保护性看跌 Protective Put",
        "保护性看跌 / Protective Put",
        "代表构造：买入标的 + 买入 1 份 K=95 Put",
        (put(+1, 95),),
        stock_quantity=+1,
    ),
    Strategy(
        "跨式 Straddle",
        "多头跨式 / Long Straddle",
        "代表构造：多头跨式（买入 K=100 Call 与 K=100 Put）",
        (call(+1, 100), put(+1, 100)),
    ),
    Strategy(
        "宽跨式 Strangle",
        "多头宽跨式 / Long Strangle",
        "代表构造：多头宽跨式（买入 K=90 Put 与 K=110 Call）",
        (put(+1, 90), call(+1, 110)),
    ),
    Strategy(
        "空头跨式 Short Straddle",
        "空头跨式 / Short Straddle",
        "代表构造：卖出 K=100 Call 与 K=100 Put",
        (call(-1, 100), put(-1, 100)),
    ),
    Strategy(
        "空头宽跨式 Short Strangle",
        "空头宽跨式 / Short Strangle",
        "代表构造：卖出 K=90 Put 与 K=110 Call",
        (put(-1, 90), call(-1, 110)),
    ),
    Strategy(
        "看涨蝶式 Butterfly Call",
        "多头看涨蝶式 / Long Call Butterfly",
        "代表构造：多头 1:−2:1（K=90/100/110 Call）",
        (call(+1, 90), call(-2, 100), call(+1, 110)),
    ),
    Strategy(
        "看跌蝶式 Butterfly Put",
        "多头看跌蝶式 / Long Put Butterfly",
        "代表构造：多头 1:−2:1（K=90/100/110 Put）",
        (put(+1, 90), put(-2, 100), put(+1, 110)),
    ),
    Strategy(
        "空头看涨蝶式 Short Call Butterfly",
        "空头看涨蝶式 / Short Call Butterfly",
        "代表构造：空头 −1:2:−1（K=90/100/110 Call）",
        (call(-1, 90), call(+2, 100), call(-1, 110)),
    ),
    Strategy(
        "空头看跌蝶式 Short Put Butterfly",
        "空头看跌蝶式 / Short Put Butterfly",
        "代表构造：空头 −1:2:−1（K=90/100/110 Put）",
        (put(-1, 90), put(+2, 100), put(-1, 110)),
    ),
    Strategy(
        "圣诞树价差 Christmas Tree Spread",
        "多头看涨圣诞树 / Long Call Christmas Tree",
        "多头看涨圣诞树：+C(90)−C(100)−C(110)；上涨端净空 1 份 Call，亏损无上限",
        (call(+1, 90), call(-1, 100), call(-1, 110)),
    ),
    Strategy(
        "空头看涨圣诞树 Short Call Christmas Tree",
        "空头看涨圣诞树 / Short Call Christmas Tree",
        "代表构造：−C(90)+C(100)+C(110)；上涨端净多 1 份 Call",
        (call(-1, 90), call(+1, 100), call(+1, 110)),
    ),
    Strategy(
        "多头看跌圣诞树 Long Put Christmas Tree",
        "多头看跌圣诞树 / Long Put Christmas Tree",
        "代表构造：+P(110)−P(100)−P(90)；下跌端净空 1 份 Put",
        (put(-1, 90), put(-1, 100), put(+1, 110)),
    ),
    Strategy(
        "空头看跌圣诞树 Short Put Christmas Tree",
        "空头看跌圣诞树 / Short Put Christmas Tree",
        "代表构造：−P(110)+P(100)+P(90)；下跌端净多 1 份 Put",
        (put(+1, 90), put(+1, 100), put(-1, 110)),
    ),
    Strategy(
        "看涨鹰式 Condor Call",
        "多头看涨鹰式 / Long Call Condor",
        "代表构造：多头 1:−1:−1:1（K=85/95/105/115 Call）",
        (call(+1, 85), call(-1, 95), call(-1, 105), call(+1, 115)),
    ),
    Strategy(
        "看跌鹰式 Condor Put",
        "多头看跌鹰式 / Long Put Condor",
        "代表构造：多头 1:−1:−1:1（K=85/95/105/115 Put）",
        (put(+1, 85), put(-1, 95), put(-1, 105), put(+1, 115)),
    ),
    Strategy(
        "空头看涨鹰式 Short Call Condor",
        "空头看涨鹰式 / Short Call Condor",
        "代表构造：空头 −1:1:1:−1（K=85/95/105/115 Call）",
        (call(-1, 85), call(+1, 95), call(+1, 105), call(-1, 115)),
    ),
    Strategy(
        "空头看跌鹰式 Short Put Condor",
        "空头看跌鹰式 / Short Put Condor",
        "代表构造：空头 −1:1:1:−1（K=85/95/105/115 Put）",
        (put(-1, 85), put(+1, 95), put(+1, 105), put(-1, 115)),
    ),
    Strategy(
        "铁鹰式 Iron Condor",
        "铁鹰式 / Iron Condor",
        "代表构造：信用铁鹰（买 P85、卖 P95、卖 C105、买 C115）",
        (put(+1, 85), put(-1, 95), call(-1, 105), call(+1, 115)),
    ),
    Strategy(
        "反向铁鹰式 Reverse Iron Condor",
        "反向铁鹰式 / Reverse Iron Condor",
        "代表构造：借记铁鹰（卖 P85、买 P95、买 C105、卖 C115）",
        (put(-1, 85), put(+1, 95), call(+1, 105), call(-1, 115)),
    ),
)


def normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def option_value(kind: str, spot: float, strike: float, years: float) -> float:
    """European Black--Scholes value with continuous dividend yield."""
    if years <= 0.0:
        return max(spot - strike, 0.0) if kind == "call" else max(strike - spot, 0.0)
    if spot <= 0.0:
        return 0.0 if kind == "call" else strike * math.exp(-RATE * years)

    root_t = math.sqrt(years)
    d1 = (
        math.log(spot / strike)
        + (RATE - DIVIDEND_YIELD + 0.5 * VOLATILITY**2) * years
    ) / (VOLATILITY * root_t)
    d2 = d1 - VOLATILITY * root_t
    discounted_spot = spot * math.exp(-DIVIDEND_YIELD * years)
    discounted_strike = strike * math.exp(-RATE * years)
    if kind == "call":
        return discounted_spot * normal_cdf(d1) - discounted_strike * normal_cdf(d2)
    return discounted_strike * normal_cdf(-d2) - discounted_spot * normal_cdf(-d1)


def entry_option_value(leg: OptionLeg) -> float:
    return option_value(leg.kind, S0, leg.strike, leg.maturity_days / DAYS_PER_YEAR)


def strategy_profit(strategy: Strategy, spot: float, elapsed_days: int) -> float:
    profit = strategy.stock_quantity * (spot - S0)
    for leg in strategy.option_legs:
        remaining_days = max(leg.maturity_days - elapsed_days, 0)
        current_value = option_value(
            leg.kind,
            spot,
            leg.strike,
            remaining_days / DAYS_PER_YEAR,
        )
        profit += leg.quantity * (current_value - entry_option_value(leg))
    return profit


def initial_net_option_cashflow(strategy: Strategy) -> float:
    """Positive means an option-premium outflow; negative means an inflow."""
    return sum(leg.quantity * entry_option_value(leg) for leg in strategy.option_legs)


def sample_curve(strategy: Strategy, elapsed_days: int) -> list[tuple[float, float]]:
    return [
        (
            X_MIN + (X_MAX - X_MIN) * index / (SAMPLE_COUNT - 1),
            strategy_profit(
                strategy,
                X_MIN + (X_MAX - X_MIN) * index / (SAMPLE_COUNT - 1),
                elapsed_days,
            ),
        )
        for index in range(SAMPLE_COUNT)
    ]


def nice_step(span: float, target_ticks: int = 6) -> float:
    raw = max(span / target_ticks, 1e-9)
    power = 10.0 ** math.floor(math.log10(raw))
    fraction = raw / power
    if fraction <= 1.0:
        nice_fraction = 1.0
    elif fraction <= 2.0:
        nice_fraction = 2.0
    elif fraction <= 5.0:
        nice_fraction = 5.0
    else:
        nice_fraction = 10.0
    return nice_fraction * power


def chart_y_bounds(*curves: list[tuple[float, float]]) -> tuple[float, float, float]:
    values = [value for curve in curves for _, value in curve]
    raw_min = min(min(values), 0.0)
    raw_max = max(max(values), 0.0)
    span = max(raw_max - raw_min, 1.0)
    padded_min = raw_min - 0.10 * span
    padded_max = raw_max + 0.10 * span
    step = nice_step(padded_max - padded_min)
    y_min = math.floor(padded_min / step) * step
    y_max = math.ceil(padded_max / step) * step
    if math.isclose(y_min, y_max):
        y_min -= step
        y_max += step
    return y_min, y_max, step


def format_number(value: float) -> str:
    if abs(value) < 5e-10:
        return "0"
    sign = "−" if value < 0 else ""
    absolute = abs(value)
    if absolute >= 100 or math.isclose(absolute, round(absolute), abs_tol=1e-9):
        return f"{sign}{absolute:.0f}"
    return f"{sign}{absolute:.1f}"


def cashflow_text(strategy: Strategy) -> str:
    cashflow = initial_net_option_cashflow(strategy)
    if abs(cashflow) < 0.005:
        premium = "初始净期权权利金≈0.00"
    elif cashflow > 0:
        premium = f"初始净期权权利金：支出 {cashflow:.2f}"
    else:
        premium = f"初始净期权权利金：收入 {-cashflow:.2f}"
    if strategy.stock_quantity > 0:
        return premium + "；另以 S₀ 买入 1 单位标的"
    if strategy.stock_quantity < 0:
        return premium + "；另以 S₀ 卖空 1 单位标的"
    return premium


def curve_labels(strategy: Strategy) -> tuple[str, str, str]:
    expiry_days = sorted({leg.maturity_days for leg in strategy.option_legs})
    if len(expiry_days) == 3:
        near, middle, far = expiry_days
        observation_remaining = (
            near - OBSERVATION_ELAPSED_DAYS,
            middle - OBSERVATION_ELAPSED_DAYS,
            far - OBSERVATION_ELAPSED_DAYS,
        )
        key_remaining = (
            middle - KEY_ELAPSED_DAYS,
            far - KEY_ELAPSED_DAYS,
        )
        timing = (
            f"期限：近/中/远月分别 {near}/{middle}/{far} 天；"
            f"更早观察日各剩 {observation_remaining[0]}/"
            f"{observation_remaining[1]}/{observation_remaining[2]} 天"
        )
        solid = (
            f"近月到期日（中月剩 {key_remaining[0]} 天、"
            f"远月剩 {key_remaining[1]} 天）理论损益"
        )
        dashed = (
            "更早观察日（近/中/远月剩 "
            f"{observation_remaining[0]}/{observation_remaining[1]}/"
            f"{observation_remaining[2]} 天）理论损益"
        )
    elif strategy.has_multiple_expiries:
        timing = "期限：近月 90 天、远月 180 天；观察时近月剩 30 天、远月剩 120 天"
        solid = "近月到期日（远月剩 90 天）理论损益"
        dashed = "到期前（近月剩 30 天）理论损益"
    else:
        timing = "期限：建仓剩 90 天；到期前曲线为剩余 30 天；实线为到期损益"
        solid = "到期损益"
        dashed = "到期前（剩余 30 天）理论损益"
    return timing, solid, dashed


def svg_path(
    curve: list[tuple[float, float]],
    x_map,
    y_map,
) -> str:
    points = [f"{x_map(x):.2f},{y_map(y):.2f}" for x, y in curve]
    return "M " + " L ".join(points)


def render_svg(strategy: Strategy) -> str:
    observation_curve = sample_curve(strategy, OBSERVATION_ELAPSED_DAYS)
    key_curve = sample_curve(strategy, KEY_ELAPSED_DAYS)
    y_min, y_max, y_step = chart_y_bounds(observation_curve, key_curve)

    width, height = 960, 600
    left, right, top, bottom = 88, 34, 184, 78
    plot_width = width - left - right
    plot_height = height - top - bottom

    def x_map(value: float) -> float:
        return left + (value - X_MIN) / (X_MAX - X_MIN) * plot_width

    def y_map(value: float) -> float:
        return top + (y_max - value) / (y_max - y_min) * plot_height

    timing, solid_label, dashed_label = curve_labels(strategy)
    param_line = (
        f"示例参数：S₀={S0:.0f}，年化波动率 σ={VOLATILITY:.0%}，"
        f"无风险利率 r={RATE:.0%}，股息率 q={DIVIDEND_YIELD:.0%}；每股损益"
    )

    parts: list[str] = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<svg xmlns="http://www.w3.org/2000/svg" width="960" height="600" '
        'viewBox="0 0 960 600" role="img" aria-labelledby="chart-title chart-desc">',
        f"  <title id=\"chart-title\">{escape(strategy.title)} 盈亏曲线</title>",
        f"  <desc id=\"chart-desc\">{escape(strategy.construction)}。"
        f"{escape(solid_label)}与{escape(dashed_label)}的比较。</desc>",
        "  <style>",
        "    :root { color-scheme: light dark; }",
        "    text { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', "
        "'Noto Sans CJK SC', 'PingFang SC', sans-serif; fill:#172033; }",
        "    .muted { fill:#536176; }",
        "    .grid { stroke:#94a3b8; stroke-opacity:.24; stroke-width:1; }",
        "    .axis { stroke:#172033; stroke-width:1.25; }",
        "    .zero { stroke:#475569; stroke-width:1.6; }",
        "    .strike { stroke:#7c3aed; stroke-width:1; stroke-dasharray:2 5; "
        "stroke-opacity:.48; }",
        "    .strike-label { fill:#7c3aed; }",
        "    .solid { fill:none; stroke:#1d4ed8; stroke-width:3; "
        "stroke-linecap:round; stroke-linejoin:round; }",
        "    .before { fill:none; stroke:#c2410c; stroke-width:2.6; "
        "stroke-dasharray:9 6; stroke-linecap:round; stroke-linejoin:round; }",
        "    .legend-bg { fill:#ffffff; fill-opacity:.92; }",
        "    .plot-bg { fill:#f8fafc; fill-opacity:.65; }",
        "    @media (prefers-color-scheme: dark) {",
        "      text { fill:#e6edf7; }",
        "      .muted { fill:#b2bfd2; }",
        "      .grid { stroke:#64748b; }",
        "      .axis { stroke:#e6edf7; }",
        "      .zero { stroke:#cbd5e1; }",
        "      .strike { stroke:#c4b5fd; }",
        "      .strike-label { fill:#c4b5fd; }",
        "      .solid { stroke:#60a5fa; }",
        "      .before { stroke:#fb923c; }",
        "      .legend-bg { fill:#171b22; }",
        "      .plot-bg { fill:#111827; }",
        "    }",
        "  </style>",
        "  <!-- Generated by scripts/generate_option_strategy_payoff_charts.py; do not edit manually. -->",
        f"  <text x=\"{left}\" y=\"36\" font-size=\"24\" font-weight=\"700\">"
        f"{escape(strategy.title)}</text>",
        f"  <text x=\"{left}\" y=\"64\" font-size=\"15\" class=\"muted\">"
        f"{escape(strategy.construction)}</text>",
        f"  <text x=\"{left}\" y=\"94\" font-size=\"13\" class=\"muted\">"
        f"{escape(param_line)}</text>",
        f"  <text x=\"{left}\" y=\"116\" font-size=\"13\" class=\"muted\">"
        f"{escape(timing)}</text>",
        f"  <text x=\"{left}\" y=\"138\" font-size=\"13\" class=\"muted\">"
        f"{escape(cashflow_text(strategy))}；忽略交易成本、融资与波动率变化</text>",
        "  <rect x=\"506\" y=\"145\" width=\"420\" height=\"36\" rx=\"6\" class=\"legend-bg\"/>",
        "  <line x1=\"520\" y1=\"156\" x2=\"558\" y2=\"156\" class=\"solid\"/>",
        f"  <text x=\"568\" y=\"161\" font-size=\"12.5\">{escape(solid_label)}</text>",
        "  <line x1=\"520\" y1=\"174\" x2=\"558\" y2=\"174\" class=\"before\"/>",
        f"  <text x=\"568\" y=\"179\" font-size=\"12.5\">{escape(dashed_label)}</text>",
        f"  <rect x=\"{left}\" y=\"{top}\" width=\"{plot_width}\" height=\"{plot_height}\" "
        "class=\"plot-bg\"/>",
    ]

    x_ticks = [50, 75, 100, 125, 150]
    for tick in x_ticks:
        x = x_map(tick)
        parts.extend(
            [
                f"  <line x1=\"{x:.2f}\" y1=\"{top}\" x2=\"{x:.2f}\" "
                f"y2=\"{top + plot_height}\" class=\"grid\"/>",
                f"  <text x=\"{x:.2f}\" y=\"{top + plot_height + 24}\" "
                f"font-size=\"12\" text-anchor=\"middle\" class=\"muted\">{tick}</text>",
            ]
        )

    tick = math.ceil(y_min / y_step) * y_step
    while tick <= y_max + y_step * 1e-8:
        y = y_map(tick)
        line_class = "zero" if math.isclose(tick, 0.0, abs_tol=y_step * 1e-6) else "grid"
        parts.extend(
            [
                f"  <line x1=\"{left}\" y1=\"{y:.2f}\" x2=\"{left + plot_width}\" "
                f"y2=\"{y:.2f}\" class=\"{line_class}\"/>",
                f"  <text x=\"{left - 10}\" y=\"{y + 4:.2f}\" font-size=\"12\" "
                f"text-anchor=\"end\" class=\"muted\">{escape(format_number(tick))}</text>",
            ]
        )
        tick += y_step

    for strike in sorted({leg.strike for leg in strategy.option_legs}):
        x = x_map(strike)
        parts.extend(
            [
                f"  <line x1=\"{x:.2f}\" y1=\"{top}\" x2=\"{x:.2f}\" "
                f"y2=\"{top + plot_height}\" class=\"strike\"/>",
                f"  <text x=\"{x:.2f}\" y=\"{top + 14}\" font-size=\"10.5\" "
                f"text-anchor=\"middle\" class=\"strike-label\">K={format_number(strike)}</text>",
            ]
        )

    parts.extend(
        [
            f"  <line x1=\"{left}\" y1=\"{top}\" x2=\"{left}\" "
            f"y2=\"{top + plot_height}\" class=\"axis\"/>",
            f"  <line x1=\"{left}\" y1=\"{top + plot_height}\" x2=\"{left + plot_width}\" "
            f"y2=\"{top + plot_height}\" class=\"axis\"/>",
            f"  <path d=\"{svg_path(observation_curve, x_map, y_map)}\" class=\"before\"/>",
            f"  <path d=\"{svg_path(key_curve, x_map, y_map)}\" class=\"solid\"/>",
            f"  <text x=\"{left + plot_width / 2:.2f}\" y=\"574\" font-size=\"14\" "
            "text-anchor=\"middle\">标的价格 S</text>",
            f"  <text x=\"24\" y=\"{top + plot_height / 2:.2f}\" font-size=\"14\" "
            f"text-anchor=\"middle\" transform=\"rotate(-90 24 {top + plot_height / 2:.2f})\">"
            "每股损益</text>",
            "</svg>",
            "",
        ]
    )
    return "\n".join(parts)


def assert_close(left: float, right: float, tolerance: float = 1e-8) -> None:
    if not math.isclose(left, right, rel_tol=0.0, abs_tol=tolerance):
        raise AssertionError(f"expected {left:.8f} ≈ {right:.8f}")


def assert_inverse_pair(
    by_stem: dict[str, Strategy],
    primary_stem: str,
    inverse_stem: str,
) -> None:
    """Assert two named strategies are exact position-level opposites."""
    primary = by_stem[primary_stem]
    inverse = by_stem[inverse_stem]
    for elapsed_days in (OBSERVATION_ELAPSED_DAYS, KEY_ELAPSED_DAYS):
        for spot in (50.0, 70.0, 90.0, 100.0, 110.0, 130.0, 150.0):
            assert_close(
                strategy_profit(primary, spot, elapsed_days),
                -strategy_profit(inverse, spot, elapsed_days),
            )


def validate_strategy_shapes() -> None:
    """Catch the most consequential direction/ratio mistakes."""
    by_stem = {strategy.asset_stem: strategy for strategy in STRATEGIES}
    key = KEY_ELAPSED_DAYS

    inverse_pairs = (
        ("看涨期权 Call", "空头看涨期权 Short Call"),
        ("看跌期权 Put", "空头看跌期权 Short Put"),
        ("看涨垂直价差 Vertical Call", "熊市看涨垂直价差 Bear Call Spread"),
        ("看跌垂直价差 Vertical Put", "牛市看跌垂直价差 Bull Put Spread"),
        (
            "看涨日历价差 Calendar Call",
            "空头看涨日历价差 Short Call Calendar Spread",
        ),
        (
            "看跌日历价差 Calendar Put",
            "空头看跌日历价差 Short Put Calendar Spread",
        ),
        (
            "多头看涨时间蝶式 Long Call Time Butterfly",
            "空头看涨时间蝶式 Short Call Time Butterfly",
        ),
        (
            "多头看跌时间蝶式 Long Put Time Butterfly",
            "空头看跌时间蝶式 Short Put Time Butterfly",
        ),
        (
            "看涨对角价差 Diagonal Call",
            "空头看涨对角价差 Short Call Diagonal Spread",
        ),
        (
            "看跌对角价差 Diagonal Put",
            "空头看跌对角价差 Short Put Diagonal Spread",
        ),
        ("看涨比率价差 Ratio Call", "看涨反向比率价差 Call Ratio Backspread"),
        ("看跌比率价差 Ratio Put", "看跌反向比率价差 Put Ratio Backspread"),
        ("跨式 Straddle", "空头跨式 Short Straddle"),
        ("宽跨式 Strangle", "空头宽跨式 Short Strangle"),
        ("看涨蝶式 Butterfly Call", "空头看涨蝶式 Short Call Butterfly"),
        ("看跌蝶式 Butterfly Put", "空头看跌蝶式 Short Put Butterfly"),
        (
            "圣诞树价差 Christmas Tree Spread",
            "空头看涨圣诞树 Short Call Christmas Tree",
        ),
        (
            "多头看跌圣诞树 Long Put Christmas Tree",
            "空头看跌圣诞树 Short Put Christmas Tree",
        ),
        ("看涨鹰式 Condor Call", "空头看涨鹰式 Short Call Condor"),
        ("看跌鹰式 Condor Put", "空头看跌鹰式 Short Put Condor"),
        ("铁鹰式 Iron Condor", "反向铁鹰式 Reverse Iron Condor"),
    )
    for primary_stem, inverse_stem in inverse_pairs:
        assert_inverse_pair(by_stem, primary_stem, inverse_stem)

    long_call = by_stem["看涨期权 Call"]
    assert strategy_profit(long_call, 150, key) > strategy_profit(long_call, 100, key)
    long_put = by_stem["看跌期权 Put"]
    assert strategy_profit(long_put, 50, key) > strategy_profit(long_put, 100, key)

    bull_call = by_stem["看涨垂直价差 Vertical Call"]
    assert strategy_profit(bull_call, 130, key) > strategy_profit(bull_call, 70, key)
    bear_put = by_stem["看跌垂直价差 Vertical Put"]
    assert strategy_profit(bear_put, 70, key) > strategy_profit(bear_put, 130, key)

    for stem in ("看涨日历价差 Calendar Call", "看跌日历价差 Calendar Put"):
        strategy = by_stem[stem]
        assert strategy_profit(strategy, 100, key) > strategy_profit(strategy, 70, key)
        assert strategy_profit(strategy, 100, key) > strategy_profit(strategy, 130, key)

    long_time_fly_stems = (
        "多头看涨时间蝶式 Long Call Time Butterfly",
        "多头看跌时间蝶式 Long Put Time Butterfly",
    )
    for stem in long_time_fly_stems:
        strategy = by_stem[stem]
        assert strategy_profit(strategy, 100, key) > strategy_profit(strategy, 70, key)
        assert strategy_profit(strategy, 100, key) > strategy_profit(strategy, 130, key)
        assert strategy_profit(strategy, 100, key) > strategy_profit(
            strategy, 100, OBSERVATION_ELAPSED_DAYS
        )

    short_time_fly_stems = (
        "空头看涨时间蝶式 Short Call Time Butterfly",
        "空头看跌时间蝶式 Short Put Time Butterfly",
    )
    for stem in short_time_fly_stems:
        strategy = by_stem[stem]
        assert strategy_profit(strategy, 100, key) < strategy_profit(strategy, 70, key)
        assert strategy_profit(strategy, 100, key) < strategy_profit(strategy, 130, key)

    call_diagonal = by_stem["看涨对角价差 Diagonal Call"]
    assert strategy_profit(call_diagonal, 130, key) > strategy_profit(
        call_diagonal, 70, key
    )
    put_diagonal = by_stem["看跌对角价差 Diagonal Put"]
    assert strategy_profit(put_diagonal, 70, key) > strategy_profit(
        put_diagonal, 130, key
    )

    covered_call = by_stem["备兑看涨 Covered Call (Buy-Write)"]
    assert_close(
        strategy_profit(covered_call, 130, key),
        strategy_profit(covered_call, 150, key),
    )
    covered_put = by_stem["备兑看跌 Covered Put (Sell-Write)"]
    assert_close(
        strategy_profit(covered_put, 50, key),
        strategy_profit(covered_put, 70, key),
    )
    assert strategy_profit(covered_put, 150, key) < strategy_profit(covered_put, 100, key)

    protective_call = by_stem["保护性看涨 Protective Call"]
    assert_close(
        strategy_profit(protective_call, 130, key),
        strategy_profit(protective_call, 150, key),
    )
    protective_put = by_stem["保护性看跌 Protective Put"]
    assert_close(
        strategy_profit(protective_put, 50, key),
        strategy_profit(protective_put, 70, key),
    )

    ratio_call = by_stem["看涨比率价差 Ratio Call"]
    assert strategy_profit(ratio_call, 150, key) < strategy_profit(ratio_call, 110, key)
    ratio_put = by_stem["看跌比率价差 Ratio Put"]
    assert strategy_profit(ratio_put, 50, key) < strategy_profit(ratio_put, 90, key)

    for stem in ("跨式 Straddle", "宽跨式 Strangle"):
        strategy = by_stem[stem]
        assert strategy_profit(strategy, 70, key) > strategy_profit(strategy, 100, key)
        assert strategy_profit(strategy, 130, key) > strategy_profit(strategy, 100, key)

    for stem in ("看涨蝶式 Butterfly Call", "看跌蝶式 Butterfly Put"):
        strategy = by_stem[stem]
        assert strategy_profit(strategy, 100, key) > strategy_profit(strategy, 70, key)
        assert strategy_profit(strategy, 100, key) > strategy_profit(strategy, 130, key)

    christmas_tree = by_stem["圣诞树价差 Christmas Tree Spread"]
    assert_close(
        sum(
            leg.quantity
            for leg in christmas_tree.option_legs
            if leg.kind == "call"
        ),
        -1.0,
    )
    assert strategy_profit(christmas_tree, 105, key) > strategy_profit(
        christmas_tree, 70, key
    )
    assert strategy_profit(christmas_tree, 105, key) > strategy_profit(
        christmas_tree, 150, key
    )
    assert strategy_profit(christmas_tree, 150, key) < strategy_profit(
        christmas_tree, 130, key
    )

    put_christmas_tree = by_stem["多头看跌圣诞树 Long Put Christmas Tree"]
    assert_close(
        sum(
            leg.quantity
            for leg in put_christmas_tree.option_legs
            if leg.kind == "put"
        ),
        -1.0,
    )
    assert strategy_profit(put_christmas_tree, 95, key) > strategy_profit(
        put_christmas_tree, 50, key
    )
    assert strategy_profit(put_christmas_tree, 95, key) > strategy_profit(
        put_christmas_tree, 130, key
    )

    for stem in ("看涨鹰式 Condor Call", "看跌鹰式 Condor Put"):
        strategy = by_stem[stem]
        assert strategy_profit(strategy, 100, key) > strategy_profit(strategy, 70, key)
        assert strategy_profit(strategy, 100, key) > strategy_profit(strategy, 130, key)

    iron_condor = by_stem["铁鹰式 Iron Condor"]
    assert strategy_profit(iron_condor, 100, key) > strategy_profit(iron_condor, 70, key)
    assert strategy_profit(iron_condor, 100, key) > strategy_profit(iron_condor, 130, key)

    for strategy in STRATEGIES:
        before = sample_curve(strategy, OBSERVATION_ELAPSED_DAYS)
        key_curve = sample_curve(strategy, KEY_ELAPSED_DAYS)
        if not all(math.isfinite(value) for curve in (before, key_curve) for _, value in curve):
            raise AssertionError(f"non-finite curve value: {strategy.asset_stem}")
        max_difference = max(abs(a[1] - b[1]) for a, b in zip(before, key_curve))
        if max_difference < 1e-4:
            raise AssertionError(f"before-expiry curve is indistinguishable: {strategy.asset_stem}")


def main() -> None:
    if len(STRATEGIES) != 46:
        raise AssertionError(f"expected 46 strategies, got {len(STRATEGIES)}")
    stems = [strategy.asset_stem for strategy in STRATEGIES]
    if len(stems) != len(set(stems)):
        raise AssertionError("duplicate SVG asset stem")

    validate_strategy_shapes()

    repo_root = Path(__file__).resolve().parents[1]
    output_dir = (
        repo_root
        / "Knowledge"
        / "Concepts"
        / "经济"
        / "金融"
        / "衍生品"
        / "期权"
        / "期权策略"
        / "assets"
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    generated_paths: list[Path] = []
    for strategy in STRATEGIES:
        path = output_dir / f"{strategy.asset_stem} 盈亏曲线.svg"
        path.write_text(render_svg(strategy), encoding="utf-8")
        ET.parse(path)
        generated_paths.append(path)

    print(f"generated {len(generated_paths)} SVG charts in {output_dir}")
    for path in generated_paths:
        print(path.relative_to(repo_root))


if __name__ == "__main__":
    main()
