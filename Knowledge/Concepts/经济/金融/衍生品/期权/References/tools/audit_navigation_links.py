#!/usr/bin/env python3
"""Audit the 25 retained chapter rows in the bilingual reading navigation."""

from __future__ import annotations

import re
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from chapter_files import CHAPTER_STEMS  # noqa: E402


EDITION_NAME = "Option Volatility and Pricing 双语版"
NAVIGATION_FILE = "阅读导航.md"
NAV_ROW_RE = re.compile(r"^\|\s*(\d{2})\s*\|", re.M)
VALID_NAV_ROW_RE = re.compile(
    r"^\|\s*(\d{2})\s*\|\s*([^|]+?)\s*\|\s*"
    r"\[\[([^\]\n]+?)\\\|([^\]\n]+?)\]\]\s*\|\s*([^|]+?)\s*\|$"
)


def target_parts(target: str) -> tuple[str, str | None]:
    file_part, marker, heading = target.partition("#")
    return file_part, heading if marker else None


def validate_target(
    edition: Path,
    target: str,
    expected_stem: str,
    failures: list[str],
    label: str,
) -> bool:
    file_part, heading = target_parts(target)
    if file_part != expected_stem:
        failures.append(
            f"{label}: 应链接 `{expected_stem}`，实际 `{file_part}`"
        )
        return False
    path = edition / f"{file_part}.md"
    if not path.exists():
        failures.append(f"{label}: 目标文件不存在 `{file_part}.md`")
        return False
    if heading is not None:
        headings = re.findall(
            r"^#{1,6} (.+)$", path.read_text(encoding="utf-8"), re.M
        )
        if heading not in headings:
            failures.append(f"{label}: 标题锚点不存在 `{target}`")
            return False
    return True


def audit_navigation(edition: Path, failures: list[str]) -> tuple[int, int]:
    navigation = edition / NAVIGATION_FILE
    if not navigation.exists():
        failures.append(f"阅读导航: 缺少 `{NAVIGATION_FILE}`")
        return 0, 0
    text = navigation.read_text(encoding="utf-8")
    row_numbers = NAV_ROW_RE.findall(text)
    expected_numbers = [f"{number:02d}" for number in range(1, 26)]
    if row_numbers != expected_numbers:
        failures.append(
            "阅读导航: 章节行必须按顺序且仅包含 01–25；"
            f"实际为 {', '.join(row_numbers) or '无'}"
        )

    valid = 0
    for line in text.splitlines():
        number_match = re.match(r"^\|\s*(\d{2})\s*\|", line)
        if not number_match:
            continue
        number = number_match.group(1)
        match = VALID_NAV_ROW_RE.match(line)
        if not match:
            failures.append(
                f"阅读导航 {number}: 表格内 wikilink 必须使用 `\\|` 而不是 `|`"
            )
            continue
        chapter = int(number)
        if not 1 <= chapter <= 25:
            failures.append(f"阅读导航 {number}: 章节编号超出 01–25")
            continue
        target = match.group(3)
        if validate_target(
            edition,
            target,
            CHAPTER_STEMS[chapter - 1],
            failures,
            f"阅读导航 {number}",
        ):
            valid += 1
    return valid, len(row_numbers)


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    edition = root / EDITION_NAME
    failures: list[str] = []
    valid, total = audit_navigation(edition, failures)
    if failures:
        print(f"navigation link audit: FAIL (navigation {valid}/{total})")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("navigation link audit: PASS (navigation 25/25)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
