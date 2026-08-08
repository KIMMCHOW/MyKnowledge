#!/usr/bin/env python3
"""Build working Obsidian links for the reading navigation and book contents."""

from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path


EDITION_NAME = "Option Volatility and Pricing 双语版"
NAVIGATION_FILE = "00-阅读导航.md"
CONTENTS_FILE = "00-04-原书目录 Contents.md"
CONTENTS_ITEM_RE = re.compile(
    r"(^> \[!quote\]- English (?P<number>\d+)\n> (?P<english>.+)\n\n)"
    r"(?P<visible>[^\n]+)$",
    re.M,
)
EXISTING_LINK_RE = re.compile(
    r"^(?:##\s+|-\s+)?\[\[(?P<target>[^\]|]+)\|(?P<alias>[^\]]+)\]\]$"
)


def normalize_english(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).casefold()
    text = re.sub(r"[`*_~$\\{}]", "", text)
    text = text.replace("–", "-").replace("—", "-").replace("’", "'")
    return re.sub(r"\s+", " ", text).strip()


def headings(path: Path) -> list[tuple[int, str]]:
    return [
        (len(match.group(1)), match.group(2).strip())
        for match in re.finditer(
            r"^(#{1,6}) (.+)$", path.read_text(encoding="utf-8"), re.M
        )
    ]


def find_section_target(path: Path, english: str) -> str:
    matches = [
        title
        for level, title in headings(path)
        if level >= 2
        and " / " in title
        and normalize_english(title.rsplit(" / ", 1)[1])
        == normalize_english(english)
    ]
    if len(matches) != 1:
        raise RuntimeError(
            f"expected one heading for {english!r} in {path.name}, found {len(matches)}"
        )
    return f"{path.stem}#{matches[0]}"


def fix_navigation_table(edition: Path) -> int:
    path = edition / NAVIGATION_FILE
    lines = path.read_text(encoding="utf-8").splitlines()
    changed = 0
    result: list[str] = []
    for line in lines:
        if re.match(r"^\|\s*\d{2}\s*\|", line):
            fixed = re.sub(
                r"(\[\[[^\]\n]+?)(?<!\\)\|([^\]\n]+\]\])",
                r"\1\\|\2",
                line,
                count=1,
            )
            if fixed != line:
                changed += 1
            line = fixed
        result.append(line)
    path.write_text("\n".join(result) + "\n", encoding="utf-8")
    return changed


def link_contents(edition: Path) -> tuple[int, int]:
    path = edition / CONTENTS_FILE
    text = path.read_text(encoding="utf-8")
    current: Path | None = None
    linked = 0

    special = {
        1: edition / "00-前言 Preface.md",
        156: edition / "26-结语 A Final Thought.md",
        157: edition / "27-附录A-期权术语表 Glossary of Option Terminology.md",
        158: edition / "28-附录B-实用数学 Some Useful Math.md",
        162: edition / "29-索引 Index.md",
    }

    def replacement(match: re.Match[str]) -> str:
        nonlocal current, linked
        number = int(match.group("number"))
        english = match.group("english")
        visible = match.group("visible").strip()
        existing = EXISTING_LINK_RE.match(visible)
        alias = existing.group("alias") if existing else visible.removeprefix("## ").removeprefix("- ")

        chapter = re.match(r"^(\d{1,2})\s+(.+)$", english)
        is_section = False
        if chapter and 1 <= int(chapter.group(1)) <= 25:
            current = next(edition.glob(f"{int(chapter.group(1)):02d}-*.md"))
            target = current.stem
        elif number in special:
            target_path = special[number]
            if not target_path.exists():
                raise RuntimeError(f"missing contents target: {target_path.name}")
            target = target_path.stem
            if number == 158:
                current = target_path
        else:
            if current is None:
                raise RuntimeError(f"contents item {number} has no chapter context")
            target = find_section_target(current, english)
            is_section = True

        prefix = "- " if is_section else "## "
        linked += 1
        return f'{match.group(1)}{prefix}[[{target}|{alias}]]'

    output, substitutions = CONTENTS_ITEM_RE.subn(replacement, text)
    if substitutions != 162 or linked != 162:
        raise RuntimeError(
            f"expected 162 contents entries, processed {substitutions}/{linked}"
        )
    path.write_text(output, encoding="utf-8")
    return linked, substitutions


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    edition = root / EDITION_NAME
    navigation_changed = fix_navigation_table(edition)
    linked, _substitutions = link_contents(edition)
    print(
        f"Obsidian navigation built: {navigation_changed} table rows repaired, "
        f"{linked} contents entries linked"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
