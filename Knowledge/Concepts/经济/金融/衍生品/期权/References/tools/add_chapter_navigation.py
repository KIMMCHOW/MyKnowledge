#!/usr/bin/env python3
"""Add deterministic visible outlines and previous/next links to chapter notes."""

from __future__ import annotations

import re
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from chapter_files import CHAPTER_STEMS  # noqa: E402


TOC_START = "<!-- chapter-toc:start -->"
TOC_END = "<!-- chapter-toc:end -->"
NAV_START = "<!-- chapter-nav:start -->"
NAV_END = "<!-- chapter-nav:end -->"


def remove_generated_blocks(text: str) -> str:
    for start, end in ((TOC_START, TOC_END), (NAV_START, NAV_END)):
        text = re.sub(
            rf"\n?{re.escape(start)}.*?{re.escape(end)}\n?",
            "\n",
            text,
            flags=re.S,
        )
    return text


def section_headings(text: str) -> list[tuple[int, str]]:
    return [
        (len(match.group(1)), match.group(2).strip())
        for match in re.finditer(r"^(#{2,6}) (.+)$", text, re.M)
    ]


def outline_block(headings: list[tuple[int, str]]) -> str:
    lines = [
        TOC_START,
        "## 本章目录 / Chapter Outline",
        "",
        "> [!abstract] 结构导航",
        "> 以下标题按原书顺序保留；点击可直接跳转。",
        "",
    ]
    base_level = min((level for level, _title in headings), default=2)
    for level, title in headings:
        indent = "  " * max(0, level - base_level)
        lines.append(f"{indent}- [[#{title}|{title}]]")
    lines.extend([TOC_END, ""])
    return "\n".join(lines)


def navigation_block(
    chapter: int,
    chapters: list[Path],
    position: str,
) -> str:
    links: list[str] = []
    if chapter > 1:
        links.append(f"[[{chapters[chapter - 2].stem}|← 上一章]]")
    links.append("[[阅读导航|全书导航]]")
    if chapter < len(chapters):
        links.append(f"[[{chapters[chapter].stem}|下一章 →]]")
    return "\n".join(
        [
            NAV_START,
            f"> [!tip] 章节导航（{position}）",
            f"> {' · '.join(links)}",
            NAV_END,
            "",
        ]
    )


def insertion_point_after_warning(text: str) -> int:
    warning = re.search(
        r"> \[!warning\] 翻译状态\n(?:>[^\n]*\n)+",
        text,
    )
    if warning:
        return warning.end()
    title = re.search(r"^# .+$", text, re.M)
    return title.end() if title else 0


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    edition = root / "Option Volatility and Pricing 双语版"
    chapters = [edition / f"{stem}.md" for stem in CHAPTER_STEMS]

    for chapter, path in enumerate(chapters, 1):
        text = remove_generated_blocks(path.read_text(encoding="utf-8"))
        headings = section_headings(text)
        insert_at = insertion_point_after_warning(text)
        top = (
            "\n\n"
            + outline_block(headings)
            + navigation_block(chapter, chapters, "章首")
        )
        text = text[:insert_at].rstrip() + top + text[insert_at:].lstrip("\n")

        # Keep the existing horizontal rule and return link, then append a
        # clearly visible previous/next navigator at the true end.
        text = text.rstrip() + "\n\n" + navigation_block(chapter, chapters, "章末").rstrip() + "\n"
        path.write_text(text, encoding="utf-8")
        print(f"updated {path.name}: {len(headings)} section headings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
