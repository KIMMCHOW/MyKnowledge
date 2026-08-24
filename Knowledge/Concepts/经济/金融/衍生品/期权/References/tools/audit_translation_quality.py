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
from collections import defaultdict
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
    # Chapter 13: the reviewed prose preserves every financial value while
    # avoiding mechanical repetition of spread labels and writing zero in words.
    "55e7961011852666": "ba22c75bd712812e",
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
    # Chapter 18's reviewed LaTeX rewrite makes variable subscripts and
    # equivalent fraction/percentage notation visible to the strict numeric
    # tokenizer.  These exact translations preserve the source values.
    "b52da4ca5341aa85": "d6e9fef711165568",
    "d6deefd147559064": "63b2c0982354fd83",
    "51b99bb7c793b866": "ad6f910c684a1cf9",
    "df5db672a68d292e": "3627fb9bc5d1e211",
    "7edefeca75d2093c": "45bc0ce7fbcc33d0",
    "40adefe6452fd054": "32ec4a957f58d153",
    "f7f318553f4d2078": "cb3200d86cbba95e",
    "bfa079c2547c2e97": "aaafd42da2d809ed",
}

# Chapters 10 and 11 were subsequently reviewed by hand and several long
# paragraphs were split into prose, display equations, and follow-up prose.
# The ordinary checker intentionally inspects the first Chinese prose line,
# so it cannot see numbers moved into the rest of the rendering.  These
# exceptions hash the *entire* Markdown rendering up to the next source marker
# (not merely that first line), and therefore fail closed if any continuation
# paragraph, equation, or translator note changes.
REVIEWED_NUMERIC_RENDERINGS = {
    # Chapter 10: mixed-number Treasury quotes and three-leg spread arithmetic.
    "d09b5e771ef66561": "5e9e7cac1d20a972",
    "3fe93b9813a2d096": "8a50046c99ed3a2c",
    "6ebe363f8dbcc682": "ef7485d1cce04161",
    # Chapter 11: reviewed strategy explanations and formula extractions.
    "97aec6fd88b9e3ca": "c1a54737e000c512",
    "6a5e065c5c52d804": "7e14d5f117c50f13",
    "abd4c94adc4698e3": "b19e79a4b6167dc1",
    "4227e8e0ced62e2c": "a380a3baee43ade6",
    "8e3ec7bebce1e205": "97f3e676791d3610",
    "eb09bf9b9dd07d4c": "cb82275f5ad959f9",
    "05cdbf2dd4ae5a04": "629d372d50c190e9",
    "9aa16609e475e8f0": "af098dcd3a07a79d",
    "d634ddee717f73b0": "608f97b34ad32b5b",
    "52a651009cc28975": "a382c42390053767",
    "3534184a026096c4": "0fff27e0edc0d959",
    "b513eacdcd514b27": "ea471e04820830d8",
    "4deeb8482d223547": "5a7fde268d423a53",
    "55c2acee17c69c34": "3e8274b5b3868301",
    "a37e79bb90bb399f": "b7b014b25d4751aa",
    "f62476310ae7c88a": "d79bc5d72da7efd6",
    "fc9c9bfec4227640": "fa05d9ce5ea37b26",
    "4a925bcbd3d85f53": "a7a2de2e562e9ef2",
    "0cfcbd66eaacb9a3": "283d24a07561f7d6",
    "a2d22ac93dfebe85": "07defce8191de15d",
    "155a0cc265463dca": "6b65edac08f2e0e6",
    # English spells out “one to one”; Chinese renders the reviewed ratio 1:1.
    "60ca4a3e29c66c5e": "ecc867a50e30f0de",
    # Repeated figure references and an equivalent “positive value” wording.
    "f622973ad80f940f": "7f7840beb4a211ad",
    "b5c835fd8593c4c6": "cec27101518a6578",
}

# These Chapter 18 translations were manually checked after formula images
# became LaTeX.  Formula symbols and the accepted synonym “执行价” trigger
# lexical heuristics even though the financial direction is preserved.  The
# translation hash keeps each exception fail-closed on future edits.
REVIEWED_SEMANTIC_TRANSLATIONS = {
    "51b99bb7c793b866": "ad6f910c684a1cf9",
    "bfa079c2547c2e97": "aaafd42da2d809ed",
    "48585a5ea2698e3e": "e0729a6af7e1c8ae",
    "701316ab10279c47": "bb6927e1f2f4b31a",
    "c3fda6547af739bd": "2be4588bf6fbdcea",
}

# Exact full-rendering counterparts for manually reviewed Chapter 11 prose.
# These cover false positives caused by moving terminology, positions, or
# cash-flow labels into a continuation paragraph or LaTeX block.  Accepted
# “执行价” wording in the retained glossary is also pinned to its exact source
# and translation rendering rather than weakening the global exercise rule.
REVIEWED_SEMANTIC_RENDERINGS = {
    "97aec6fd88b9e3ca": "c1a54737e000c512",
    "6a5e065c5c52d804": "7e14d5f117c50f13",
    "b6690a23534cda3d": "9417617af00d4551",
    "abd4c94adc4698e3": "b19e79a4b6167dc1",
    "4227e8e0ced62e2c": "a380a3baee43ade6",
    "8e3ec7bebce1e205": "97f3e676791d3610",
    "eb09bf9b9dd07d4c": "cb82275f5ad959f9",
    "d634ddee717f73b0": "608f97b34ad32b5b",
    "30a34debced11c79": "ba0f6130e746c8cf",
    "3534184a026096c4": "0fff27e0edc0d959",
    "cb5074bf7b7414b5": "6a3830d33a7f0e87",
    "fc9c9bfec4227640": "fa05d9ce5ea37b26",
    "52556e843f04103c": "3e430af98a3c9b86",
    "04402f7950df3356": "032003804aa38d83",
    "4a925bcbd3d85f53": "a7a2de2e562e9ef2",
    "0cfcbd66eaacb9a3": "283d24a07561f7d6",
    "a2d22ac93dfebe85": "07defce8191de15d",
    # +500/-500 is the exact signed rendering of long/short 500 deltas.
    "29709085bafe09d8": "7fa95ffcc38960db",
    "dccfc7826850c994": "5b8e04caa7f1588b",
    "43e4e933ebffc302": "20279ae543679f56",
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
    "导致看涨价值上升并使价值下降": "使看涨期权价值上升、看跌期权价值下降",
    "希腊人": "Greeks（希腊字母风险指标）",
    "偏衍生品": "偏导数",
    "没有希腊语": "没有对应的 Greek（希腊字母风险指标）",
    "Rho（P）": "Rho（ρ）",
    "phy（Pi）": "Phi（Φ）",
    "Lambda（Á）": "Lambda（Λ）",
    "拉姆达（Á）": "Lambda（Λ）",
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


def reviewed_numeric_translation(
    digest: str | None, target: str, rendering: str
) -> bool:
    if digest is None:
        return False
    expected = REVIEWED_NUMERIC_TRANSLATIONS.get(digest)
    actual = hashlib.sha256(target.encode("utf-8")).hexdigest()[:16]
    if expected == actual:
        return True
    expected_rendering = REVIEWED_NUMERIC_RENDERINGS.get(digest)
    actual_rendering = hashlib.sha256(rendering.encode("utf-8")).hexdigest()[:16]
    return expected_rendering == actual_rendering


def reviewed_semantic_translation(
    digest: str | None, target: str, rendering: str
) -> bool:
    if digest is None:
        return False
    expected = REVIEWED_SEMANTIC_TRANSLATIONS.get(digest)
    actual = hashlib.sha256(target.encode("utf-8")).hexdigest()[:16]
    if expected == actual:
        return True
    expected_rendering = REVIEWED_SEMANTIC_RENDERINGS.get(digest)
    actual_rendering = hashlib.sha256(rendering.encode("utf-8")).hexdigest()[:16]
    return expected_rendering == actual_rendering


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


def rendering_until_next_source(lines: list[str], start: int) -> str:
    """Return the exact target rendering governed by the preceding marker."""
    cursor = start
    while cursor < len(lines) and not MARKER_RE.fullmatch(lines[cursor]):
        cursor += 1
    return "\n".join(lines[start:cursor]).strip()


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
                yield (
                    index + 2,
                    marker_before(lines, index),
                    "prose",
                    english,
                    chinese,
                    rendering_until_next_source(lines, cursor),
                )
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
                yield (
                    index + 2,
                    marker_before(lines, index),
                    "footnote",
                    english,
                    chinese,
                    rendering_until_next_source(lines, cursor),
                )


NON_BOOK_FILES = {"阅读导航.md"}


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
        if path.name not in NON_BOOK_FILES
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

        for (
            line_no,
            digest,
            kind,
            callout_english,
            chinese,
            rendering,
        ) in bilingual_pairs(text):
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
            semantic_reviewed = reviewed_semantic_translation(
                digest, target_for_audit, rendering
            )
            for name, source_pattern, target_pattern in DIRECTION_RULES:
                if source_pattern.search(english) and not target_pattern.search(target_for_audit):
                    # Avoid treating temporal uses such as "short-term" as a
                    # position direction.
                    if name == "short_position" and re.search(r"short[- ]term|short period|short time", english, re.I):
                        continue
                    if semantic_reviewed:
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
            if (
                expected_basis
                and target_for_audit.count("基差") < expected_basis
                and not semantic_reviewed
            ):
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
            if not shorthand_safe and not semantic_reviewed:
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
            if not compact_position_safe and not semantic_reviewed:
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
            if not cashflow_terms_safe and not semantic_reviewed:
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
            if not probability_wording_safe and not semantic_reviewed:
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
            if not probability_center_safe and not semantic_reviewed:
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
                and not semantic_reviewed
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
                if reviewed_numeric_translation(
                    digest, target_for_audit, rendering
                ):
                    item["issue"] = "人工复核通过：数字值一致，仅表达形式或重复次数不同"
                    reviewed_numeric_hits.append(item)
                else:
                    numeric_hits.append(item)
            if is_bibliographic_reference(english):
                preserved_reference_count += 1
            elif (
                not semantic_reviewed
                and not translation_language_is_safe(english, target_for_audit)
            ):
                language_hits.append(
                    {
                        "file": path.name,
                        "line": line_no,
                        "english": english[:220],
                        "chinese": target_for_audit[:220],
                    }
                )

    # A pair may be reported by both a named direction rule and the shared
    # fail-closed high-risk checker. Keep only one row per file/line/rule.
    direction_hits = list(
        {
            (item["file"], item["line"], item["rule"]): item
            for item in direction_hits
        }.values()
    )
    has_failures = bool(
        known_bad_hits
        or direction_hits
        or numeric_hits
        or language_hits
        or source_mapping_hits
        or formula_hits
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
    summary = {
        "pairs": checked_pairs,
        "known_bad": len(known_bad_hits),
        "direction": len(direction_hits),
        "numeric": len(numeric_hits),
        "numeric_reviewed": len(reviewed_numeric_hits),
        "language": len(language_hits),
        "source_mapping": len(source_mapping_hits),
        "preserved_references": preserved_reference_count,
        "formula": len(formula_hits),
    }
    print(f"translation quality audit: {'FAIL' if has_failures else 'PASS'}")
    print(json.dumps(summary, ensure_ascii=False))
    return 1 if has_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
