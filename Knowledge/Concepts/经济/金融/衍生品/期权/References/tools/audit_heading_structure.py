#!/usr/bin/env python3
"""Verify EPUB chapter headings and visible Obsidian chapter outlines."""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from chapter_files import CHAPTER_STEMS  # noqa: E402


XHTML_NS = "{http://www.w3.org/1999/xhtml}"
TOC_START = "<!-- chapter-toc:start -->"
TOC_END = "<!-- chapter-toc:end -->"


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def source_headings(archive: zipfile.ZipFile, chapter: int) -> list[tuple[str, str]]:
    root = ET.fromstring(archive.read(f"ops/ch{chapter}.html"))
    body = root.find(f"{XHTML_NS}body")
    if body is None:
        raise RuntimeError(f"ch{chapter}: missing body")
    result: list[tuple[str, str]] = []
    for element in body.iter():
        tag = element.tag.rsplit("}", 1)[-1]
        text = clean("".join(element.itertext()))
        if tag in {"h1", "h2", "h3", "h4"} and text and text != str(chapter):
            result.append((tag, text))
    return result


def markdown_headings(text: str) -> list[tuple[int, str]]:
    without_toc = re.sub(
        rf"{re.escape(TOC_START)}.*?{re.escape(TOC_END)}\n?",
        "",
        text,
        flags=re.S,
    )
    return [
        (len(match.group(1)), match.group(2).strip())
        for match in re.finditer(r"^(#{1,6}) (.+)$", without_toc, re.M)
    ]


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    edition = root / "Option Volatility and Pricing 双语版"
    epubs = list(root.glob("*.epub"))
    if len(epubs) != 1:
        raise RuntimeError(f"expected one EPUB, found {len(epubs)}")

    failures: list[str] = []
    rows: list[str] = []
    with zipfile.ZipFile(epubs[0]) as archive:
        for chapter in range(1, 26):
            path = edition / f"{CHAPTER_STEMS[chapter - 1]}.md"
            text = path.read_text(encoding="utf-8")
            source = source_headings(archive, chapter)
            generated = markdown_headings(text)
            if not generated or generated[0][0] != 1:
                failures.append(f"ch{chapter:02d}: missing chapter H1")
                rows.append(f"| {chapter:02d} | {max(0, len(source) - 1)} | — | — | ❌ |")
                continue

            # The EPUB's first real heading is the chapter title represented
            # by the Markdown H1. Remaining English titles must occur in order.
            expected_sections = [title for _tag, title in source[1:]]
            actual_sections = [
                heading.rsplit(" / ", 1)[-1]
                for level, heading in generated[1:]
                if level >= 2 and " / " in heading
            ]
            if actual_sections != expected_sections:
                failures.append(
                    f"ch{chapter:02d}: source/Markdown section order mismatch "
                    f"({len(expected_sections)} vs {len(actual_sections)})"
                )

            toc_match = re.search(
                rf"{re.escape(TOC_START)}(.*?){re.escape(TOC_END)}",
                text,
                flags=re.S,
            )
            if not toc_match:
                failures.append(f"ch{chapter:02d}: missing visible chapter TOC")
                rows.append(
                    f"| {chapter:02d} | {len(expected_sections)} | "
                    f"{len(actual_sections)} | 0 | ❌ |"
                )
                continue
            toc_targets = re.findall(r"\[\[#([^]|]+)\|", toc_match.group(1))
            actual_titles = [heading for level, heading in generated[1:] if level >= 2]
            if toc_targets != actual_titles:
                failures.append(
                    f"ch{chapter:02d}: TOC does not match headings "
                    f"({len(toc_targets)} vs {len(actual_titles)})"
                )
            ok = actual_sections == expected_sections and toc_targets == actual_titles
            rows.append(
                f"| {chapter:02d} | {len(expected_sections)} | "
                f"{len(actual_sections)} | {len(toc_targets)} | "
                f"{'✅' if ok else '❌'} |"
            )

    report = [
        "---",
        "title: Option Volatility and Pricing 章节与标题结构审计",
        "tags:",
        "  - 期权",
        "  - 双语阅读",
        "  - 结构审计",
        f"status: {'通过' if not failures else '待处理'}",
        "created: 2026-08-03",
        "---",
        "",
        "# 章节与标题结构审计",
        "",
        "> [!summary] 结论",
        "> 逐章比对 EPUB 标题顺序、Markdown `# / ## / ###` 层级与可点击章内目录。",
        "> 每章还包含章首和章末的上一章/下一章导航。",
        "",
        "| 章 | EPUB 小节 | Markdown 小节 | 目录链接 | 结果 |",
        "|---:|---:|---:|---:|---|",
        *rows,
    ]
    if failures:
        report.extend(["", "## 待处理", ""] + [f"- {item}" for item in failures])
    report.extend(["", "[[阅读导航|← 返回阅读导航]]", ""])
    (edition / "章节与标题结构审计.md").write_text(
        "\n".join(report), encoding="utf-8"
    )

    if failures:
        print("heading structure audit: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("heading structure audit: PASS (25/25 chapters)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
