#!/usr/bin/env python3
"""Normalize trading-critical terminology in visible Chinese prose only."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EDITION = ROOT / "Option Volatility and Pricing 双语版"
sys.path.insert(0, str(ROOT / "tools"))

from translate_epub_chapter import (  # noqa: E402
    financial_basis_count,
    normalize_credit_debit_terms,
    normalize_option_shorthand_translation,
)

PROSE_REPLACEMENTS = {
    "三角洲": "Delta",
    "织女星": "Vega",
    "角增量": "Theta",
    "西塔": "Theta",
    "维加斯": "Vega",
    "维嘎斯": "Vega",
    "提前锻炼": "提前行权",
    "早期锻炼": "提前行权",
    "早期练习": "提前行权",
    "早期运动": "提前行权",
    "裸体姿势": "裸头寸",
    "提前行权习": "提前行权",
    "提前行权价格": "行权价",
    "保护性呼吁": "保护性看涨期权",
    "涵盖的写作": "备兑卖出",
    "提前运动": "提前行权",
    "提前练习": "提前行权",
    "原始对冲": "初始对冲",
    "解决程序": "结算程序",
    "市场诚信": "市场健全性",
    "提前行使": "提前行权",
    "基础合同": "标的合约",
    "基础价格": "标的价格",
    "基础工具": "标的工具",
    "基础资产": "标的资产",
    "执行价格": "行权价",
    "行使价格": "行权价",
    "合成位置": "合成头寸",
    "职位分析": "头寸分析",
    "传播策略": "价差策略",
    "传播简介": "价差策略导论",
    "逻辑正态": "对数正态",
    "收件箱": "到期时",
    "项圈": "领式策略",
    "长（短）": "多头（空头）",
    "短（长）": "空头（多头）",
    "长期市场头寸": "多头市场头寸",
    "长期合成标的头寸": "合成标的多头",
    "长500Delta": "500 Delta 多头",
    "短500Delta": "500 Delta 空头",
    "长20个Delta": "20 Delta 多头",
    "长度只有25个Delta": "仅有 25 Delta 多头",
}


def normalize_terms(source: str, target: str) -> str:
    text = target
    for bad, preferred in PROSE_REPLACEMENTS.items():
        text = text.replace(bad, preferred)
    if re.search(r"(?<!in )\btime to maturity\b", source, re.I):
        if re.match(r"^\s*time to maturity\b", source, re.I):
            text = re.sub(
                r"(?:至|到|距(?:离)?)?(?:成熟时间|到期时间)",
                "距离到期时间",
                text,
                count=1,
            )
        else:
            text = text.replace("成熟时间", "到期时间")
        label = re.fullmatch(
            r"\s*time to maturity\s+\*?([A-Za-z])\*?\s*=\s*"
            r"(\d+(?:\.\d+)?)\s+months?\s*",
            source,
            re.I,
        )
        if label:
            variable, months = label.groups()
            text = f"距离到期时间：${variable} = {months}\\ \\text{{个月}}$"
    if re.search(r"\bbrokerage firms?\b", source, re.I):
        text = text.replace("证券经纪公司", "券商").replace("经纪公司", "券商")
    text = normalize_option_shorthand_translation(source, text)
    text = normalize_credit_debit_terms(source, text)
    if financial_basis_count(source):
        text = text.replace("基数", "基差").replace("基础", "基差")

    greek_terms = {
        "delta": "Delta",
        "gamma": "Gamma",
        "theta": "Theta",
        "vega": "Vega",
        "rho": "Rho",
    }
    for lower, canonical in greek_terms.items():
        if re.search(rf"\b{lower}s?\b", source, re.I):
            text = re.sub(
                rf"(?<![A-Za-z]){lower}(?![A-Za-z])",
                canonical,
                text,
                flags=re.I,
            )
    if re.search(r"\brho\b", source, re.I):
        text = re.sub(r"(?<![A-Za-z])Ro(?![A-Za-z])", "Rho", text)
    if re.search(r"\bgammas?\b", source, re.I):
        text = text.replace("伽马", "Gamma").replace("伽玛", "Gamma")
    if re.search(r"\bthetas?\b", source, re.I):
        text = text.replace("θ", "Theta")
    if re.search(r"\bvegas?\b", source, re.I):
        text = text.replace("维加", "Vega").replace("维嘎", "Vega")

    # Frequent legacy phrase from translating "at the money" literally.
    if re.search(r"\bat[- ]the[- ]money\b", source, re.I):
        text = text.replace("处于货币", "处于平值状态")
    return text


def process_file(path: Path) -> int:
    lines = path.read_text(encoding="utf-8").splitlines()
    rewritten = 0
    index = 0
    while index < len(lines):
        is_quote = lines[index].startswith("> [!quote]- English ")
        is_footnote = lines[index].startswith("> [!note] Footnote ")
        if not (is_quote or is_footnote):
            index += 1
            continue
        source_index = index + 1
        source = lines[source_index][2:] if source_index < len(lines) and lines[source_index].startswith("> ") else ""
        if is_footnote:
            target_index = index + 2
            prefix = "> "
        else:
            target_index = index + 2
            while target_index < len(lines) and not lines[target_index].strip():
                target_index += 1
            if target_index < len(lines) and lines[target_index].strip() == "$$":
                index = target_index + 1
                continue
            prefix = ""
        if target_index >= len(lines):
            break
        raw_target = lines[target_index]
        target = raw_target[2:] if prefix and raw_target.startswith(prefix) else raw_target
        if target.startswith(("<!--", "#", "---", "![", "> [!")):
            index = target_index + 1
            continue
        normalized = normalize_terms(source, target)
        replacement = prefix + normalized if prefix else normalized
        if replacement != raw_target:
            lines[target_index] = replacement
            rewritten += 1
        index = target_index + 1
    if rewritten:
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return rewritten


def main() -> int:
    total = 0
    changed_files = 0
    for path in sorted(EDITION.glob("*.md")):
        if path.name == "29-索引 Index.md" or path.name.startswith(("94-", "95-", "96-", "97-", "98-", "99-")):
            continue
        count = process_file(path)
        if count:
            total += count
            changed_files += 1
    print(f"visible terminology normalization: PASS ({total} blocks in {changed_files} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
