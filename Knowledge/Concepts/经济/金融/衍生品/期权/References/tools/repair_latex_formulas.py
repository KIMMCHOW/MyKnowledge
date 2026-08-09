#!/usr/bin/env python3
"""Rebuild every text equation from its original EPUB source block.

This is deliberately translation-free: source hashes pair each Markdown block
with the exact XHTML node, so formulas can be repaired without calling an API
or guessing the author's numbers.
"""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from translate_epub_chapter import (  # noqa: E402
    IMAGE_TAGS,
    XHTML_NS,
    formula_source,
    formula_to_latex,
    is_formula_block,
    iter_blocks,
    local_name,
    plain_text,
    source_hash,
)


EDITION = ROOT / "Option Volatility and Pricing 双语版"
MARKER_RE = re.compile(r"^<!-- source:block ([0-9a-f]{16}) -->$", re.M)


def formula_map(epub: Path) -> dict[str, str]:
    formulas: dict[str, str] = {}
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
                if any(local_name(node.tag) in IMAGE_TAGS for node in block.iter()):
                    continue
                english = plain_text(block)
                css_class = block.attrib.get("class", "")
                if english and is_formula_block(css_class, english):
                    digest = source_hash(block)
                    latex = formula_to_latex(formula_source(block))
                    previous = formulas.get(digest)
                    if previous is not None and previous != latex:
                        raise RuntimeError(f"source hash collision for formula {digest}")
                    formulas[digest] = latex
    return formulas


def repair_file(path: Path, formulas: dict[str, str]) -> tuple[int, list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    repaired = 0
    failures: list[str] = []
    index = 0
    while index < len(lines):
        marker = MARKER_RE.match(lines[index])
        if not marker or marker.group(1) not in formulas:
            index += 1
            continue
        digest = marker.group(1)
        boundary = index + 1
        while boundary < len(lines) and not MARKER_RE.match(lines[boundary]):
            boundary += 1
        delimiters = [
            cursor
            for cursor in range(index + 1, boundary)
            if lines[cursor].strip() == "$$"
        ]
        if len(delimiters) != 2:
            failures.append(
                f"{path.name}:{index + 1}: expected one LaTeX block for {digest}, "
                f"found {len(delimiters)} delimiters"
            )
            index = boundary
            continue
        opening, closing = delimiters
        expected = formulas[digest]
        if lines[opening + 1 : closing] != [expected]:
            lines[opening + 1 : closing] = [expected]
            repaired += 1
            boundary += 1 - (closing - opening - 1)
        index = boundary
    if repaired:
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return repaired, failures


def main() -> int:
    epubs = list(ROOT.glob("*.epub"))
    if len(epubs) != 1:
        raise RuntimeError(f"expected one EPUB, found {len(epubs)}")
    formulas = formula_map(epubs[0])
    repaired = 0
    failures: list[str] = []
    matched_blocks = 0
    for path in sorted(EDITION.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        matched_blocks += sum(
            1
            for digest in MARKER_RE.findall(text)
            if digest in formulas
        )
        count, file_failures = repair_file(path, formulas)
        repaired += count
        failures.extend(file_failures)

    residual: list[str] = []
    bad_patterns = (
        re.compile(r"\\\\[A-Za-z]+"),
        re.compile(r"\d\.\\frac\{\d+\}\{\d+\}(?:\.\d+)?"),
    )
    for path in sorted(EDITION.glob("*.md")):
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if any(pattern.search(line) for pattern in bad_patterns):
                residual.append(f"{path.name}:{line_no}: {line}")

    if failures or residual:
        print("LaTeX source-block repair: FAIL")
        for failure in (failures + residual)[:40]:
            print(f"- {failure}")
        return 1
    print(
        f"LaTeX source-block repair: PASS ({matched_blocks} formulas verified, "
        f"{repaired} rewritten, {len(formulas)} EPUB formula hashes indexed)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
