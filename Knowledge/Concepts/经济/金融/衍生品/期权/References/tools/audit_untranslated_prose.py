#!/usr/bin/env python3
"""Fail when long English source prose is repeated as the visible translation."""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

from translate_epub_chapter import COMPACT_OPTION_POSITION_RE


ROOT = Path(__file__).resolve().parents[1]
EDITION = ROOT / "Option Volatility and Pricing 双语版"
DETAILS = EDITION / ".untranslated-prose-audit.json"
MIN_WORDS = 3


def plain(text: str) -> str:
    text = html.unescape(text)
    text = re.sub(r"\[\[[^\]|]+\|([^\]]+)\]\]", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[*_`~]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def normalized(text: str) -> str:
    text = plain(text).casefold()
    text = text.replace("‘", "'").replace("’", "'")
    text = text.replace("“", '"').replace("”", '"')
    text = text.replace("–", "-").replace("—", "-").replace("−", "-")
    return text


def scan_file(path: Path) -> list[dict[str, object]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    hits: list[dict[str, object]] = []
    index = 0
    while index < len(lines):
        is_quote = lines[index].startswith("> [!quote]- English ")
        is_footnote = lines[index].startswith("> [!note] Footnote ")
        if not (is_quote or is_footnote):
            index += 1
            continue
        callout_line = index + 1
        english_lines: list[str] = []
        cursor = index + 1
        if is_footnote:
            if cursor < len(lines) and lines[cursor].startswith("> "):
                english_lines.append(lines[cursor][2:])
                cursor += 1
            while cursor < len(lines) and not lines[cursor].strip():
                cursor += 1
        else:
            while cursor < len(lines) and lines[cursor].startswith("> "):
                english_lines.append(lines[cursor][2:])
                cursor += 1
            while cursor < len(lines) and not lines[cursor].strip():
                cursor += 1
        if cursor >= len(lines) or lines[cursor].strip() == "$$":
            index = cursor + 1
            continue
        visible_prefix = "> " if is_footnote else ""
        visible = lines[cursor].strip()
        if is_footnote and visible.startswith("> "):
            visible = visible[2:]
        elif is_footnote:
            definition = re.match(r"\[\^[^\]]+\]:\s*(.*)", visible)
            visible = definition.group(1) if definition else visible
        if visible.startswith(("<!--", "![", "> [!")):
            index = cursor + 1
            continue
        visible = re.sub(r"^(?:#{1,6}|-)\s+", "", visible)
        english = " ".join(english_lines)
        # URLs are identifiers, not translatable prose. Keeping them verbatim
        # is necessary for cited resources to remain usable.
        if re.fullmatch(r"https?://\S+", plain(english), re.I):
            index = cursor + 1
            continue
        word_count = len(re.findall(r"[A-Za-z]+(?:['’-][A-Za-z]+)?", plain(english)))
        if word_count >= MIN_WORDS and normalized(english) == normalized(visible):
            # Compact position labels such as "long a June 100 call" are
            # intentionally preserved verbatim: translating `long` as a
            # literal adjective can reverse or garble the trading direction.
            if COMPACT_OPTION_POSITION_RE.fullmatch(plain(english)):
                index = cursor + 1
                continue
            hits.append(
                {
                    "file": path.name,
                    "callout_line": callout_line,
                    "visible_line": cursor + 1,
                    "visible_prefix": visible_prefix,
                    "kind": "footnote" if is_footnote else "prose",
                    "words": word_count,
                    "english": plain(english),
                }
            )
        index = cursor + 1
    return hits


def write_details(hits: list[dict[str, object]]) -> None:
    DETAILS.write_text(json.dumps(hits, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    hits: list[dict[str, object]] = []
    for path in sorted(EDITION.glob("*.md")):
        hits.extend(scan_file(path))
    write_details(hits)
    if hits:
        print(
            f"untranslated prose audit: FAIL "
            f"({len(hits)} long paragraphs in {len({hit['file'] for hit in hits})} files)"
        )
        for hit in hits[:20]:
            print(f"- {hit['file']}:{hit['visible_line']} ({hit['words']} words)")
        return 1
    print("untranslated prose audit: PASS (0 long English fallbacks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
