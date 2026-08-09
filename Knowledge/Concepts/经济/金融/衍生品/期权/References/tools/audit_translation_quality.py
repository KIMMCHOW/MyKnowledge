#!/usr/bin/env python3
"""Risk-oriented QA for the bilingual option textbook translation."""

from __future__ import annotations

import html
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from translate_epub_chapter import (  # noqa: E402
    XHTML_NS,
    compact_option_position_translation_is_safe,
    credit_debit_translation_is_safe,
    explicit_numbers,
    financial_basis_count,
    high_risk_translation_is_safe,
    iter_blocks,
    local_name,
    numeric_translation_is_safe,
    option_shorthand_translation_is_safe,
    plain_text,
    plain_text_for_translation,
    probability_center_translation_is_safe,
    probability_wording_translation_is_safe,
    source_hash,
    translation_language_is_safe,
)


MARKER_RE = re.compile(r"<!-- source:block ([0-9a-f]{16}) -->")

# These exact Chinese renderings were manually checked against their EPUB
# source blocks.  Their numeric values are faithful, but a strict multiset
# comparison cannot represent Chinese number words, harmless repetition
# removal, or an explicit cross-paragraph referent.  Hashing the translation
# keeps the exception fail-closed: any later edit is audited again.
REVIEWED_NUMERIC_TRANSLATIONS = {
    "d3aa40a79501fd41": "5a21c7ae8ab20242",
    "d30546e1a6b5ba7a": "fe1d15c083baf858",
    "e76202ea5b4cdca4": "6a4e52fcb7d8c2fc",
    "9977c1684ee7a9ab": "6b5e83fa018f7cad",
    "8b8639a47a466b42": "b93f5bf893539903",
    "96842f6f56120b3b": "99026ee9efb3f2d1",
    "b534174594435019": "57403815848d4460",
    "1c8702280e01468d": "1af0c4105f6c0877",
    "4da16fa342c8007e": "4d3b52c0e6fe4769",
    "30863bef7da0d6de": "372d154febc068f8",
}


KNOWN_BAD = {
    "三角洲": "Delta",
    "织女星": "Vega",
    "角增量": "Theta",
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
    "提前行权日": "行权日",
    "合成位置": "合成头寸",
    "职位分析": "头寸分析",
    "传播策略": "价差策略",
    "传播简介": "价差策略导论",
    "提前行权期权": "行权期权",
    "逻辑正态": "对数正态",
    "收件箱": "到期时",
    "En（": "ln(",
    "西格玛": "\\sigma",
    "提前行权策略策略": "提前行权策略",
    "项圈": "领式策略",
    "提前行权风险风险": "提前行权风险",
    "长（短）": "多头（空头）",
    "短（长）": "空头（多头）",
    "长期市场头寸": "多头市场头寸",
    "长期合成标的头寸": "合成标的多头",
    "长500Delta": "500 Delta 多头",
    "短500Delta": "500 Delta 空头",
    "长20个Delta": "20 Delta 多头",
    "长度只有25个Delta": "仅有 25 Delta 多头",
}


DIRECTION_RULES = [
    (
        "long_position",
        re.compile(
            r"\b(?:go|going) long\b|\blong (?:position|stock|futures?|contracts?|options?|calls?|puts?|underlying|market)\b",
            re.I,
        ),
        re.compile(r"多头|做多|买入|持有"),
    ),
    (
        "short_position",
        re.compile(
            r"\b(?:go|going) short\b|\bshort (?:position|stock|futures?|contracts?|options?|calls?|puts?|underlying|market)\b",
            re.I,
        ),
        re.compile(r"空头|做空|卖出|卖空"),
    ),
    (
        "call_option",
        re.compile(
            r"\bcall options?\b|\b(?:long|short) calls?\b|\bcalls?\s+(?:and|or)\s+puts?\b|\b(?:buy|sell|bought|sold|purchase|purchased)\s+(?:a|the|\d+)?\s*calls?\b",
            re.I,
        ),
        re.compile(r"看涨"),
    ),
    (
        "put_option",
        re.compile(
            r"\bput options?\b|\b(?:long|short) puts?\b|\bputs?\s+(?:and|or)\s+calls?\b|\b(?:buy|sell|bought|sold|purchase|purchased)\s+(?:a|the|\d+)?\s*puts?\b",
            re.I,
        ),
        re.compile(r"看跌"),
    ),
    (
        "exercise",
        re.compile(r"\b(?:exercise|exercised|exercising)\b", re.I),
        re.compile(r"行权|行使"),
    ),
    (
        "assignment",
        re.compile(r"\bassignment\b|\bassigned on\b|\bgets? assigned\b", re.I),
        re.compile(r"指派|被行权"),
    ),
    (
        "underlying",
        re.compile(r"\bunderlying\b", re.I),
        re.compile(r"标的"),
    ),
    (
        "settlement",
        re.compile(r"\bsettlement\b", re.I),
        re.compile(r"结算|交割"),
    ),
    (
        "volatility",
        re.compile(r"\bvolatilit(?:y|ies)\b", re.I),
        re.compile(r"波动率"),
    ),
    (
        "spread",
        re.compile(
            r"\b(?:option|calendar|vertical|horizontal|diagonal|ratio|volatility|"
            r"bull|bear|credit|debit|time) spreads?\b|"
            r"\bspread (?:position|strategy|order)\b",
            re.I,
        ),
        re.compile(r"价差|利差"),
    ),
    (
        "covered_write",
        re.compile(r"\bcovered[- ]writes?\b", re.I),
        re.compile(r"备兑卖出|covered write", re.I),
    ),
    (
        "basis_points",
        re.compile(r"\bbasis points?\b", re.I),
        re.compile(r"基点"),
    ),
    (
        "ordinary_basis_for",
        re.compile(r"\bbasis for\b", re.I),
        re.compile(r"基础|依据|构成|根基"),
    ),
    (
        "time_to_maturity",
        # Exclude ordinary prose such as "from that point in time to
        # maturity"; this rule is for the finance term of art.
        re.compile(r"(?<!in )\btime to maturity\b", re.I),
        re.compile(r"到期时间|剩余期限"),
    ),
    (
        "brokerage_firm",
        re.compile(r"\bbrokerage firms?\b", re.I),
        re.compile(r"券商|证券经纪公司"),
    ),
    (
        "long_delta",
        re.compile(r"\blong\s+\d+\s*deltas?\b|\b\d+\s*deltas?\s+long\b", re.I),
        re.compile(r"多头|做多|long", re.I),
    ),
    (
        "short_delta",
        re.compile(r"\bshort\s+\d+\s*deltas?\b|\b\d+\s*deltas?\s+short\b", re.I),
        re.compile(r"空头|做空|short", re.I),
    ),
]


def clean_markup(text: str) -> str:
    text = html.unescape(text)
    # Navigation targets often contain chapter numbers.  For translation QA,
    # a wikilink contributes only its visible alias, not its file/anchor path.
    text = re.sub(r"\[\[[^\]|]+\|([^\]]+)\]\]", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    return text.replace("*", "").replace("\\$", "$")


def source_text_key(text: str) -> str:
    text = clean_markup(text)
    text = text.replace("‘", "'").replace("’", "'")
    text = text.replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", text).strip().casefold()


def is_bibliographic_reference(source: str) -> bool:
    """Allow author names, titles, journal names and URLs to stay English."""
    has_year = bool(re.search(r"\b(?:18|19|20)\d{2}\b", source))
    has_citation_shape = bool(
        re.search(
            r"https?://|\b(?:Journal|Magazine|Press|Review|Econometrica|Risk)\b",
            source,
        )
        or re.search(r"[“\"][^”\"]{8,}[”\"]", source)
    )
    return has_year and has_citation_shape


def numeric_safe_with_epub_metadata(
    translation_source: str, target: str, footnote_markers: tuple[str, ...]
) -> bool:
    """Ignore EPUB footnote backlinks while checking financial numerals."""
    augmented_source = translation_source + "".join(
        f"<sup>{value}</sup>" for value in footnote_markers
    )
    return numeric_translation_is_safe(augmented_source, target)


def reviewed_numeric_translation(digest: str | None, target: str) -> bool:
    if digest is None:
        return False
    expected = REVIEWED_NUMERIC_TRANSLATIONS.get(digest)
    actual = hashlib.sha256(target.encode("utf-8")).hexdigest()[:16]
    return expected == actual


def epub_source_blocks(epub: Path) -> dict[str, tuple[str, str, tuple[str, ...]]]:
    """Return authoritative prose and translation-safe prose by source hash."""
    result: dict[str, tuple[str, str, tuple[str, ...]]] = {}
    with zipfile.ZipFile(epub) as archive:
        for name in archive.namelist():
            if not name.startswith("ops/") or not name.endswith((".html", ".xhtml")):
                continue
            try:
                root = ET.fromstring(archive.read(name))
            except ET.ParseError:
                continue
            body = root.find(f"{XHTML_NS}body")
            if body is None:
                continue
            for block in iter_blocks(body):
                english = plain_text(block)
                if not english:
                    continue
                digest = source_hash(block)
                footnote_markers: list[str] = []
                for node in block.iter():
                    if local_name(node.tag) != "sup":
                        continue
                    marker = "".join(node.itertext()).strip().rstrip(".")
                    has_backlink = any(
                        local_name(descendant.tag) == "a"
                        and (
                            "fn" in descendant.attrib.get("href", "")
                            or descendant.attrib.get("id", "").startswith("r")
                        )
                        for descendant in node.iter()
                    )
                    if has_backlink and marker.isdigit():
                        footnote_markers.append(marker)
                value = (
                    english,
                    plain_text_for_translation(block),
                    tuple(footnote_markers),
                )
                previous = result.get(digest)
                if previous is not None and previous != value:
                    raise RuntimeError(f"source hash collision: {digest}")
                result[digest] = value
    return result


def marker_before(lines: list[str], zero_based_index: int) -> str | None:
    for cursor in range(zero_based_index - 1, -1, -1):
        match = MARKER_RE.fullmatch(lines[cursor])
        if match:
            return match.group(1)
    return None


def bilingual_pairs(text: str):
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith("> [!quote]- English ") and index + 1 < len(lines):
            english = lines[index + 1][2:] if lines[index + 1].startswith("> ") else ""
            cursor = index + 2
            while cursor < len(lines) and not lines[cursor].strip():
                cursor += 1
            if cursor < len(lines) and lines[cursor].strip() == "$$":
                continue
            chinese = lines[cursor] if cursor < len(lines) else ""
            if chinese.startswith("## [["):
                chinese = chinese.removeprefix("## ")
            elif chinese.startswith("- [["):
                chinese = chinese.removeprefix("- ")
            if chinese and not chinese.startswith((">", "<!--", "#", "---")):
                yield index + 2, marker_before(lines, index), "prose", english, chinese
        elif line.startswith("> [!note] Footnote ") and index + 2 < len(lines):
            english = lines[index + 1][2:] if lines[index + 1].startswith("> ") else ""
            cursor = index + 2
            while cursor < len(lines) and not lines[cursor].strip():
                cursor += 1
            if cursor < len(lines) and lines[cursor].startswith("> "):
                chinese = lines[cursor][2:]
            elif cursor < len(lines):
                match = re.match(r"\[\^[^\]]+\]:\s*(.*)", lines[cursor])
                chinese = match.group(1) if match else ""
            else:
                chinese = ""
            if english and chinese:
                yield index + 2, marker_before(lines, index), "footnote", english, chinese


def main() -> int:
    root = ROOT
    edition = root / "Option Volatility and Pricing 双语版"
    epubs = list(root.glob("*.epub"))
    if len(epubs) != 1:
        raise RuntimeError(f"expected one EPUB, found {len(epubs)}")
    source_blocks = epub_source_blocks(epubs[0])
    sources_by_text: dict[str, set[tuple[str, str, tuple[str, ...]]]] = defaultdict(set)
    for value in source_blocks.values():
        sources_by_text[source_text_key(value[0])].add(value)
    files = sorted(
        path
        for path in edition.glob("*.md")
        if not path.name.startswith(("98-", "99-"))
        and path.name not in {"00-04-原书目录 Contents.md", "29-索引 Index.md"}
    )

    known_bad_hits: list[dict[str, object]] = []
    direction_hits: list[dict[str, object]] = []
    numeric_hits: list[dict[str, object]] = []
    reviewed_numeric_hits: list[dict[str, object]] = []
    language_hits: list[dict[str, object]] = []
    source_mapping_hits: list[dict[str, object]] = []
    preserved_reference_count = 0
    formula_hits: list[dict[str, object]] = []
    checked_pairs = 0

    for path in files:
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        for bad, preferred in KNOWN_BAD.items():
            for line_no, line in enumerate(lines, 1):
                if bad in line and not line.startswith("> "):
                    known_bad_hits.append(
                        {
                            "file": path.name,
                            "line": line_no,
                            "found": bad,
                            "preferred": preferred,
                        }
                    )
        delimiters = [i for i, line in enumerate(lines, 1) if line.strip() == "$$"]
        if len(delimiters) % 2:
            formula_hits.append(
                {"file": path.name, "line": delimiters[-1], "issue": "LaTeX 分隔符不成对"}
            )
        for line_no, line in enumerate(lines, 1):
            if re.search(r"\\text\{[^}]+\}\s+\\text\{", line):
                formula_hits.append(
                    {"file": path.name, "line": line_no, "issue": "LaTeX 文本被拆分，空格可能丢失"}
                )
            if re.search(r"\\\\[A-Za-z]+", line):
                formula_hits.append(
                    {"file": path.name, "line": line_no, "issue": "LaTeX 命令含重复反斜杠"}
                )
            if re.search(r"\d\.\\frac\{\d+\}\{\d+\}(?:\.\d+)?", line):
                formula_hits.append(
                    {"file": path.name, "line": line_no, "issue": "小数除法被错拆为分数"}
                )
            if "@@" in line or "\ue000" in line or r"\text{frac}" in line:
                formula_hits.append(
                    {"file": path.name, "line": line_no, "issue": "LaTeX 含未解析占位符"}
                )

        for line_no, digest, kind, callout_english, chinese in bilingual_pairs(text):
            checked_pairs += 1
            if not digest or digest not in source_blocks:
                matches = sources_by_text.get(source_text_key(callout_english), set())
                if len(matches) == 1:
                    english, translation_source, footnote_markers = next(iter(matches))
                elif digest is not None:
                    source_mapping_hits.append(
                        {
                            "file": path.name,
                            "line": line_no,
                            "digest": digest,
                            "issue": "无法映射到 EPUB 源段落",
                        }
                    )
                    english = clean_markup(callout_english)
                    translation_source = english
                    footnote_markers = ()
                else:
                    # Chapter 1 predates source-hash markers but retains the
                    # original English callout verbatim, which is sufficient
                    # as the authoritative source for semantic QA.
                    english = clean_markup(callout_english)
                    translation_source = english
                    footnote_markers = ()
            else:
                english, translation_source, footnote_markers = source_blocks[digest]
            target_for_audit = chinese
            if kind == "footnote":
                # The display marker is metadata, not a financial value.
                target_for_audit = re.sub(
                    r"^\s*(?:\[\^[^\]]+\]:\s*|<sup>\d+\.?\s*</sup>|\[\d+\]|\d+\.?)\s*",
                    "",
                    target_for_audit,
                )
            for name, source_pattern, target_pattern in DIRECTION_RULES:
                if source_pattern.search(english) and not target_pattern.search(target_for_audit):
                    # Avoid treating temporal uses such as "short-term" as a
                    # position direction.
                    if name == "short_position" and re.search(r"short[- ]term|short period|short time", english, re.I):
                        continue
                    direction_hits.append(
                        {
                            "file": path.name,
                            "line": line_no,
                            "rule": name,
                            "english": clean_markup(english)[:220],
                            "chinese": target_for_audit[:220],
                        }
                    )
            expected_basis = financial_basis_count(english)
            if expected_basis and target_for_audit.count("基差") < expected_basis:
                direction_hits.append(
                    {
                        "file": path.name,
                        "line": line_no,
                        "rule": "basis",
                        "english": english[:220],
                        "chinese": target_for_audit[:220],
                    }
                )
            shorthand_safe = option_shorthand_translation_is_safe(
                english, target_for_audit
            )
            if not shorthand_safe:
                direction_hits.append(
                    {
                        "file": path.name,
                        "line": line_no,
                        "rule": "option_shorthand_strike",
                        "english": english[:220],
                        "chinese": target_for_audit[:220],
                    }
                )
            compact_position_safe = compact_option_position_translation_is_safe(
                english, target_for_audit
            )
            if not compact_position_safe:
                direction_hits.append(
                    {
                        "file": path.name,
                        "line": line_no,
                        "rule": "compact_option_position_english",
                        "english": english[:220],
                        "chinese": target_for_audit[:220],
                    }
                )
            cashflow_terms_safe = credit_debit_translation_is_safe(
                english, target_for_audit
            )
            if not cashflow_terms_safe:
                direction_hits.append(
                    {
                        "file": path.name,
                        "line": line_no,
                        "rule": "credit_debit_english",
                        "english": english[:220],
                        "chinese": target_for_audit[:220],
                    }
                )
            probability_wording_safe = probability_wording_translation_is_safe(
                english, target_for_audit
            )
            if not probability_wording_safe:
                direction_hits.append(
                    {
                        "file": path.name,
                        "line": line_no,
                        "rule": "probability_wording_distinction",
                        "english": english[:220],
                        "chinese": target_for_audit[:220],
                    }
                )
            probability_center_safe = probability_center_translation_is_safe(
                english, target_for_audit
            )
            if not probability_center_safe:
                direction_hits.append(
                    {
                        "file": path.name,
                        "line": line_no,
                        "rule": "probability_center_reversal",
                        "english": english[:220],
                        "chinese": target_for_audit[:220],
                    }
                )
            if (
                not high_risk_translation_is_safe(english, target_for_audit)
                and shorthand_safe
                and compact_position_safe
                and cashflow_terms_safe
                and probability_wording_safe
                and probability_center_safe
            ):
                direction_hits.append(
                    {
                        "file": path.name,
                        "line": line_no,
                        "rule": "high_risk_term_missing",
                        "english": english[:220],
                        "chinese": target_for_audit[:220],
                    }
                )
            if not numeric_safe_with_epub_metadata(
                translation_source, target_for_audit, footnote_markers
            ):
                item = {
                    "file": path.name,
                    "line": line_no,
                    "english_numbers": dict(explicit_numbers(translation_source)),
                    "chinese_numbers": dict(explicit_numbers(target_for_audit)),
                    "english": english[:220],
                    "chinese": target_for_audit[:220],
                }
                if reviewed_numeric_translation(digest, target_for_audit):
                    item["issue"] = "人工复核通过：数字值一致，仅表达形式或重复次数不同"
                    reviewed_numeric_hits.append(item)
                else:
                    numeric_hits.append(item)
            if is_bibliographic_reference(english):
                preserved_reference_count += 1
            elif not translation_language_is_safe(english, target_for_audit):
                language_hits.append(
                    {
                        "file": path.name,
                        "line": line_no,
                        "english": english[:220],
                        "chinese": target_for_audit[:220],
                    }
                )

    by_rule = Counter(item["rule"] for item in direction_hits)
    by_bad = Counter(item["found"] for item in known_bad_hits)
    # A pair may be reported by both a named direction rule and the shared
    # fail-closed high-risk checker. Keep only one row per file/line/rule.
    direction_hits = list(
        {
            (item["file"], item["line"], item["rule"]): item
            for item in direction_hits
        }.values()
    )
    by_rule = Counter(item["rule"] for item in direction_hits)
    has_failures = bool(
        known_bad_hits
        or direction_hits
        or numeric_hits
        or language_hits
        or source_mapping_hits
        or formula_hits
    )
    report = [
        "---",
        "title: Option Volatility and Pricing 翻译质量与风险审计",
        "tags:",
        "  - 期权",
        "  - 翻译审计",
        "  - 风险管理",
        "created: 2026-08-03",
        f"status: {'待处理' if has_failures else '自动风险审计通过'}",
        "---",
        "",
        "# 翻译质量与风险审计",
        "",
        "> [!warning] 审计定位",
        "> 本报告是全量自动风险扫描与人工术语规则的结果，不等同于出版级逐字人工校译。它优先捕捉会改变头寸方向、权利义务、现金流、行权与风险结论的错误。",
        "> 审计无法确认的高风险段落已改为直接显示英文，而不是保留可能反转交易含义的机器中译。",
        "",
        "## 扫描汇总",
        "",
        f"- 双语段落对：{checked_pairs}",
        f"- 已知机器误译命中：{len(known_bad_hits)}",
        f"- 高风险术语/方向待复核：{len(direction_hits)}",
        f"- 数字集不一致待复核：{len(numeric_hits)}",
        f"- 人工复核通过的数字表达差异：{len(reviewed_numeric_hits)}",
        f"- 未翻译/中英夹杂待复核：{len(language_hits)}",
        f"- 依规则保留英文的文献引用：{preserved_reference_count}",
        f"- EPUB 源段落映射问题：{len(source_mapping_hits)}",
        f"- LaTeX 格式问题：{len(formula_hits)}",
        "",
        "## 已知误译分布",
        "",
        "| 误译 | 建议译法 | 命中 |",
        "|---|---|---:|",
    ]
    for bad, count in by_bad.most_common():
        report.append(f"| {bad} | {KNOWN_BAD[bad]} | {count} |")
    report.extend(
        [
            "",
            "## 高风险术语/方向规则",
            "",
            "| 规则 | 待复核 |",
            "|---|---:|",
        ]
    )
    for name, count in by_rule.most_common():
        report.append(f"| {name} | {count} |")

    def add_examples(title: str, items: list[dict[str, object]], limit: int = 80) -> None:
        report.extend(["", f"## {title}", ""])
        if not items:
            report.append("- 未发现。")
            return
        for item in items[:limit]:
            file = str(item["file"])
            line = item["line"]
            detail = item.get("rule") or item.get("issue") or item.get("found")
            # Markdown line numbers are not Obsidian heading anchors.  Keep
            # the file clickable without creating a false unresolved anchor.
            report.append(f"- [[{file}|{file}:{line}]] — {detail}")
        if len(items) > limit:
            report.append(f"- ……其余 {len(items) - limit} 项见 JSON 明细。")

    add_examples("已知误译明细", known_bad_hits)
    add_examples("高风险术语与方向待复核", direction_hits)
    add_examples("数字不一致待复核", numeric_hits)
    add_examples("人工复核通过的数字表达差异", reviewed_numeric_hits)
    add_examples("未翻译或中英夹杂待复核", language_hits)
    add_examples("EPUB 源段落映射问题", source_mapping_hits)
    add_examples("LaTeX 格式问题", formula_hits)
    report.extend(["", "[[90-阅读导航|← 返回阅读导航]]", ""])

    (edition / "98-翻译质量与风险审计.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    details = {
        "known_bad": known_bad_hits,
        "direction": direction_hits,
        "numeric": numeric_hits,
        "numeric_reviewed": reviewed_numeric_hits,
        "language": language_hits,
        "source_mapping": source_mapping_hits,
        "preserved_references": preserved_reference_count,
        "formula": formula_hits,
    }
    (edition / ".translation-quality-audit.json").write_text(
        json.dumps(details, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "pairs": checked_pairs,
                "known_bad": len(known_bad_hits),
                "direction": len(direction_hits),
                "numeric": len(numeric_hits),
                "numeric_reviewed": len(reviewed_numeric_hits),
                "language": len(language_hits),
                "source_mapping": len(source_mapping_hits),
                "preserved_references": preserved_reference_count,
                "formula": len(formula_hits),
            },
            ensure_ascii=False,
        )
    )
    return 1 if has_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
