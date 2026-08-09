#!/usr/bin/env python3
"""Audit Obsidian navigation links in the bilingual edition."""

from __future__ import annotations

import re
import sys
from pathlib import Path


EDITION_NAME = "Option Volatility and Pricing 双语版"
NAVIGATION_FILE = "90-阅读导航.md"
CONTENTS_FILE = "00-04-原书目录 Contents.md"
REPORT_FILE = "96-导航链接审计.md"

NAV_ROW_RE = re.compile(r"^\|\s*(\d{2})\s*\|", re.M)
VALID_NAV_ROW_RE = re.compile(
    r"^\|\s*(\d{2})\s*\|\s*([^|]+?)\s*\|\s*"
    r"\[\[([^\]\n]+?)\\\|([^\]\n]+?)\]\]\s*\|\s*([^|]+?)\s*\|$"
)
CONTENTS_ITEM_RE = re.compile(
    r"^> \[!quote\]- English (\d+)\n> (.+)\n\n([^\n]+)$", re.M
)
WIKILINK_RE = re.compile(
    r"^(?P<prefix>##\s+|-\s+)?\[\[(?P<target>[^\]|]+)\|(?P<alias>[^\]]+)\]\]$"
)


def normalize_english(text: str) -> str:
    """Normalize source/Markdown styling without changing semantic words."""
    text = text.casefold()
    text = re.sub(r"[`*_~$\\{}]", "", text)
    text = text.replace("–", "-").replace("—", "-").replace("’", "'")
    return re.sub(r"\s+", " ", text).strip()


def target_parts(target: str) -> tuple[str, str | None]:
    file_part, marker, heading = target.partition("#")
    return file_part, heading if marker else None


def validate_target(
    edition: Path,
    target: str,
    failures: list[str],
    label: str,
) -> bool:
    file_part, heading = target_parts(target)
    path = edition / f"{file_part}.md"
    if not path.exists():
        failures.append(f"{label}: 目标文件不存在 `{file_part}.md`")
        return False
    if heading is not None:
        headings = re.findall(r"^#{1,6} (.+)$", path.read_text(encoding="utf-8"), re.M)
        if heading not in headings:
            failures.append(f"{label}: 标题锚点不存在 `{target}`")
            return False
    return True


def expected_context(edition: Path, number: int, english: str, current: Path | None):
    chapter = re.match(r"^(\d{1,2})\s+(.+)$", english)
    if chapter and 1 <= int(chapter.group(1)) <= 25:
        current = next(edition.glob(f"{int(chapter.group(1)):02d}-*.md"))
        return current, current.stem, False

    special = {
        1: "00-05-前言 Preface",
        156: "26-结语 A Final Thought",
        157: "27-附录A-期权术语表 Glossary of Option Terminology",
        158: "28-附录B-实用数学 Some Useful Math",
        162: "29-索引 Index",
    }
    if number in special:
        path = edition / f"{special[number]}.md"
        if number == 158:
            current = path
        return current, special[number], False

    if current is None:
        raise RuntimeError(f"Contents item {number} has no chapter context")
    headings = re.findall(r"^#{1,6} (.+)$", current.read_text(encoding="utf-8"), re.M)
    matches = [
        heading
        for heading in headings
        if " / " in heading
        and normalize_english(heading.rsplit(" / ", 1)[1])
        == normalize_english(english)
    ]
    if len(matches) != 1:
        raise RuntimeError(
            f"Contents item {number} maps to {len(matches)} headings in {current.name}: {english}"
        )
    return current, f"{current.stem}#{matches[0]}", True


def audit_navigation(edition: Path, failures: list[str]) -> tuple[int, int]:
    text = (edition / NAVIGATION_FILE).read_text(encoding="utf-8")
    row_numbers = NAV_ROW_RE.findall(text)
    valid = 0
    for line in text.splitlines():
        number_match = re.match(r"^\|\s*(\d{2})\s*\|", line)
        if not number_match:
            continue
        match = VALID_NAV_ROW_RE.match(line)
        number = number_match.group(1)
        if not match:
            failures.append(
                f"阅读导航 {number}: 表格内 wikilink 必须使用 `\\|` 而不是 `|`"
            )
            continue
        target = match.group(3)
        if validate_target(edition, target, failures, f"阅读导航 {number}"):
            valid += 1
    if len(row_numbers) != 26:
        failures.append(f"阅读导航: 应有 26 行，实际 {len(row_numbers)} 行")
    return valid, len(row_numbers)


def audit_contents(edition: Path, failures: list[str]) -> tuple[int, int]:
    text = (edition / CONTENTS_FILE).read_text(encoding="utf-8")
    items = CONTENTS_ITEM_RE.findall(text)
    if [int(number) for number, _english, _visible in items] != list(range(1, 163)):
        failures.append("原书目录: English 条目应为连续的 1–162")

    current: Path | None = None
    valid = 0
    for number_text, english, visible in items:
        number = int(number_text)
        try:
            current, expected_target, is_section = expected_context(
                edition, number, english, current
            )
        except (RuntimeError, StopIteration) as error:
            failures.append(f"原书目录 {number}: {error}")
            continue
        link = WIKILINK_RE.match(visible.strip())
        if not link:
            failures.append(f"原书目录 {number}: 中文条目不是可点击 wikilink")
            continue
        target = link.group("target")
        if target != expected_target:
            failures.append(
                f"原书目录 {number}: 应连到 `{expected_target}`，实际 `{target}`"
            )
            continue
        if not validate_target(edition, target, failures, f"原书目录 {number}"):
            continue
        if is_section:
            _file, heading = target_parts(target)
            assert heading is not None
            if normalize_english(heading.rsplit(" / ", 1)[-1]) != normalize_english(
                english
            ):
                failures.append(f"原书目录 {number}: 英文条目与目标标题不一致")
                continue
        valid += 1
    return valid, len(items)


def write_report(
    edition: Path,
    nav_result: tuple[int, int],
    contents_result: tuple[int, int],
    failures: list[str],
) -> None:
    nav_valid, nav_total = nav_result
    contents_valid, contents_total = contents_result
    lines = [
        "---",
        "title: Option Volatility and Pricing 导航链接审计",
        "tags:",
        "  - 期权",
        "  - 双语阅读",
        "  - 链接审计",
        f"status: {'通过' if not failures else '待处理'}",
        "created: 2026-08-03",
        "---",
        "",
        "# 导航链接审计",
        "",
        "> [!summary] 结论",
        "> 检查阅读导航表格的 Obsidian 语法，并逐项核对原书目录到章节标题的链接。",
        "",
        "| 范围 | 有效链接 | 应有链接 | 结果 |",
        "|---|---:|---:|---|",
        f"| 阅读导航 | {nav_valid} | {nav_total} | {'✅' if nav_valid == nav_total == 26 else '❌'} |",
        f"| 原书目录 | {contents_valid} | {contents_total} | {'✅' if contents_valid == contents_total == 162 else '❌'} |",
    ]
    if failures:
        lines.extend(["", "## 待处理（前 40 项）", ""])
        lines.extend(f"- {failure}" for failure in failures[:40])
    lines.extend(["", "[[90-阅读导航|← 返回阅读导航]]", ""])
    (edition / REPORT_FILE).write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    edition = root / EDITION_NAME
    failures: list[str] = []
    nav_result = audit_navigation(edition, failures)
    contents_result = audit_contents(edition, failures)
    write_report(edition, nav_result, contents_result, failures)
    if failures:
        print(
            "navigation link audit: FAIL "
            f"(navigation {nav_result[0]}/{nav_result[1]}, "
            f"contents {contents_result[0]}/{contents_result[1]})"
        )
        for failure in failures[:20]:
            print(f"- {failure}")
        if len(failures) > 20:
            print(f"- ... {len(failures) - 20} more")
        return 1
    print("navigation link audit: PASS (navigation 26/26, contents 162/162)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
