#!/usr/bin/env python3
"""Audit Obsidian footnote references against the retained EPUB footnotes."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

from audit_translation_quality import epub_source_blocks


ROOT = Path(__file__).resolve().parents[1]
EDITION = ROOT / "Option Volatility and Pricing 双语版"
DETAILS = EDITION / ".footnote-link-audit.json"
NOTE_RE = re.compile(r"^> \[!note\] Footnote \d+")
MARKER_RE = re.compile(r"<sup>(\d+)</sup>")
REF_RE = re.compile(r"\[\^([^\]]+)\](?!:)")
DEF_RE = re.compile(r"^\[\^([^\]]+)\]:", re.M)
SOURCE_BLOCK_RE = re.compile(r"<!-- source:block ([0-9a-f]{16}) -->")


def prefix_for(path: Path) -> str:
    from chapter_files import footnote_prefix
    return footnote_prefix(path)


def marker_before(lines: list[str], index: int) -> str | None:
    for cursor in range(index - 1, -1, -1):
        match = SOURCE_BLOCK_RE.fullmatch(lines[cursor])
        if match:
            return match.group(1)
    return None


def expected_references(
    lines: list[str],
    defined_markers: set[str],
    prefix: str,
    source_blocks: dict[str, tuple[str, str, tuple[str, ...]]],
) -> Counter[str]:
    expected: Counter[str] = Counter()
    index = 0
    while index < len(lines):
        if not lines[index].startswith("> [!quote]- English "):
            index += 1
            continue
        digest = marker_before(lines, index)
        markers = source_blocks.get(digest, ("", "", ()))[2] if digest else ()
        for marker in markers:
            if marker in defined_markers:
                expected[f"{prefix}-{marker}"] += 1
        index += 1
    return expected


def scan(
    path: Path, source_blocks: dict[str, tuple[str, str, tuple[str, ...]]]
) -> dict[str, object] | None:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    prefix = prefix_for(path)
    defined_markers: set[str] = set()
    for index, line in enumerate(lines[:-1]):
        if NOTE_RE.match(line):
            marker = MARKER_RE.search(lines[index + 1])
            if marker:
                defined_markers.add(marker.group(1))
    if not defined_markers:
        return None
    expected = expected_references(lines, defined_markers, prefix, source_blocks)
    references = Counter(REF_RE.findall(text))
    definitions = Counter(DEF_RE.findall(text))
    relevant_ids = {f"{prefix}-{marker}" for marker in defined_markers}
    references = Counter({key: value for key, value in references.items() if key in relevant_ids})
    definitions = Counter({key: value for key, value in definitions.items() if key in relevant_ids})
    missing_references = expected - references
    extra_references = references - expected
    missing_definitions = Counter({key: 1 for key in expected if definitions[key] == 0})
    duplicate_definitions = Counter({key: value for key, value in definitions.items() if value != 1})
    if not any((missing_references, extra_references, missing_definitions, duplicate_definitions)):
        return None
    return {
        "file": path.name,
        "expected": dict(expected),
        "references": dict(references),
        "definitions": dict(definitions),
        "missing_references": dict(missing_references),
        "extra_references": dict(extra_references),
        "missing_definitions": dict(missing_definitions),
        "duplicate_definitions": dict(duplicate_definitions),
    }


def main() -> int:
    epubs = list(ROOT.glob("*.epub"))
    if len(epubs) != 1:
        raise RuntimeError(f"expected one EPUB, found {len(epubs)}")
    source_blocks = epub_source_blocks(epubs[0])
    failures = [
        result
        for path in sorted(EDITION.glob("*.md"))
        if (result := scan(path, source_blocks)) is not None
    ]
    DETAILS.write_text(json.dumps(failures, ensure_ascii=False, indent=2), encoding="utf-8")
    if failures:
        print(f"footnote link audit: FAIL ({len(failures)} files)")
        for item in failures[:20]:
            print(
                f"- {item['file']}: missing references "
                f"{item['missing_references']}, missing definitions "
                f"{item['missing_definitions']}"
            )
        return 1
    print("footnote link audit: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
