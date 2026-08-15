#!/usr/bin/env python3
"""Audit EPUB-to-Markdown coverage, images, and displayed LaTeX formulas."""

from __future__ import annotations

import hashlib
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from translate_epub_chapter import (
    IMAGE_TAGS,
    XHTML_NS,
    is_formula_block,
    iter_blocks,
    local_name,
    plain_text,
    source_hash,
)
from translate_remaining_chapters import CHAPTERS


@dataclass(frozen=True)
class Section:
    source: str
    output: str
    number: str
    english_title: str
    source_label: str | None = None
    manual: bool = False


CH18_CONVERTED_IMAGES = frozenset(
    {
        "e0339-01.jpg",
        "e0340-01.jpg",
        "e0340-02.jpg",
        "e0340-03.jpg",
        "e0341-01.jpg",
        "e0341-02.jpg",
        "e0341-03.jpg",
        "e0342-01.jpg",
        "e0342-02.jpg",
        "e0346-01.jpg",
        "e0347-01.jpg",
        "e0347-02.jpg",
        "e0348-01.jpg",
        "e0349-01.jpg",
        "e0351-01.jpg",
        "e0352-01.jpg",
        "e0352-02.jpg",
        "e0353-01.jpg",
        "e0353-02.jpg",
        "e0353-03.jpg",
        "e0353-04.jpg",
        "e0354-01.jpg",
        "e0355-01.jpg",
        "f0350-01.jpg",
        "f0351-01.jpg",
        "qroot.jpg",
        "t0349-01.jpg",
        "t0356-01.jpg",
    }
)
CH18_DISPLAY_FORMULA_IMAGES = frozenset(
    name
    for name in CH18_CONVERTED_IMAGES
    if name.startswith(("e", "f"))
)

# Chapters 10 and 11 were manually copy-edited after their translation audit.
# A few source prose/table passages were deliberately rewritten as displayed
# LaTeX so that mixed-number quotes and multi-leg arithmetic remain legible.
# The exception is deliberately fail-closed: source count, generated count,
# and the digest of every displayed LaTeX block must all match the reviewed
# rendering.  Any later formula edit is audited again instead of inheriting a
# chapter-wide allowance.
REVIEWED_FORMULA_REWRITES = {
    "ch10": (8, 10, "a66f3b26cf5cd993"),
    "ch11": (15, 23, "01737ce91fc6d09b"),
}


def displayed_latex_digest(text: str) -> str:
    """Hash the exact ordered contents of all balanced display-math blocks."""
    blocks: list[str] = []
    current: list[str] | None = None
    for line in text.splitlines():
        if line.strip() == "$$":
            if current is None:
                current = []
            else:
                blocks.append("\n".join(current).strip())
                current = None
        elif current is not None:
            current.append(line)
    return hashlib.sha256("\n\n".join(blocks).encode("utf-8")).hexdigest()[:16]


def section_list() -> list[Section]:
    sections = [
        Section(
            "ch1",
            "金融合约 Financial Contracts.md",
            "1",
            "Financial Contracts",
            manual=True,
        ),
    ]
    sections.extend(
        Section(
            f"ch{number}",
            f"{chinese} {english}.md",
            str(number),
            english,
        )
        for number, chinese, english in CHAPTERS
    )
    sections.extend(
        (
            Section(
                "afterword",
                "结语 A Final Thought.md",
                "26",
                "A Final Thought",
            ),
            Section(
                "appendixa",
                "附录A-期权术语表 Glossary of Option Terminology.md",
                "27",
                "Glossary of Option Terminology",
                "A",
            ),
            Section(
                "appendixb",
                "附录B-实用数学 Some Useful Math.md",
                "28",
                "Some Useful Math",
                "B",
            ),
        )
    )
    return sections


def source_metrics(archive: zipfile.ZipFile, section: Section) -> dict[str, object]:
    root = ET.fromstring(archive.read(f"ops/{section.source}.html"))
    body = root.find(f"{XHTML_NS}body")
    if body is None:
        raise RuntimeError(f"{section.source}: missing body")
    hashes: list[str] = []
    image_names: list[str] = []
    formulas = 0
    text_blocks = 0
    skipped_title = False
    for block in iter_blocks(body):
        tag = local_name(block.tag)
        css_class = block.attrib.get("class", "")
        block_images = [
            node for node in block.iter() if local_name(node.tag) in IMAGE_TAGS
        ]
        if block_images:
            hashes.append(source_hash(block))
            image_names.extend(
                Path(node.attrib.get("src", "")).name for node in block_images
            )
            continue
        text = plain_text(block)
        if not text:
            continue
        if tag == "h2" and text == section.number:
            continue
        if tag == "h2" and section.source_label and text == section.source_label:
            continue
        if tag == "h2" and text == section.english_title and not skipped_title:
            skipped_title = True
            continue
        hashes.append(source_hash(block))
        text_blocks += int(tag == "p")
        formulas += int(tag == "p" and is_formula_block(css_class, text))
    return {
        "hashes": hashes,
        "image_names": image_names,
        "formulas": formulas,
        "text_blocks": text_blocks,
    }


def markdown_metrics(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    visible_text = "\n".join(
        line for line in text.splitlines() if not line.startswith("> ")
    )
    hashes = re.findall(r"<!-- source:block ([0-9a-f]{16}) -->", text)
    image_refs = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)
    latex_delimiters = sum(1 for line in text.splitlines() if line.strip() == "$$")
    bare_currency = 0
    for line in visible_text.splitlines():
        if line.strip() == "$$":
            continue
        # Inline LaTeX such as ``$20^2 = 400$`` is valid mathematics, not an
        # unescaped currency sign. Remove balanced inline math before looking
        # for accidental Markdown dollar delimiters in ordinary prose.
        prose_only = re.sub(r"(?<!\\)\$[^$\n]+(?<!\\)\$", "", line)
        bare_currency += len(re.findall(r"(?<!\\)\$(?=\d)", prose_only))
    return {
        "hashes": hashes,
        "images": image_refs,
        "image_names": [Path(ref).name for ref in image_refs],
        "latex_blocks": latex_delimiters // 2,
        "latex_digest": displayed_latex_digest(text),
        "latex_balanced": latex_delimiters % 2 == 0,
        "bad_latex_tokens": bool(
            re.search(r"\ue000|@@|\\text\{frac\}|(?<!>)>>(?!>)", visible_text)
        ),
        "bare_currency": bare_currency,
        "quotes": len(re.findall(r"^> \[!quote\]-? English ", text, re.M)),
        "footnotes": len(re.findall(r"^> \[!note\] Footnote ", text, re.M)),
        "figure_captions": len(re.findall(r" / Figure \d", text)),
        "signature": int("Sheldon Natenberg" in text),
    }


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    output_dir = root / "Option Volatility and Pricing 双语版"
    epubs = list(root.glob("*.epub"))
    if len(epubs) != 1:
        raise RuntimeError(f"expected one EPUB, found {len(epubs)}")

    failures: list[str] = []
    total_source_blocks = total_generated_blocks = 0
    manual_source_units = manual_generated_units = 0
    total_source_images = total_generated_images = 0
    total_formulas = total_converted_images = 0

    with zipfile.ZipFile(epubs[0]) as archive:
        for section in section_list():
            output = output_dir / section.output
            if not output.exists():
                failures.append(f"{section.source}: 缺少 {section.output}")
                continue
            source = source_metrics(archive, section)
            generated = markdown_metrics(output)
            source_counter = Counter(source["hashes"])
            generated_counter = Counter(generated["hashes"])
            if section.manual:
                # Manual files predate hash annotations; compare source paragraph
                # count with retained English callouts and verify all images.
                english_count = (
                    int(generated["quotes"])
                    + int(generated["footnotes"])
                    + int(generated["figure_captions"])
                )
                text_ok = english_count == int(source["text_blocks"])
                manual_source_units += int(source["text_blocks"])
                manual_generated_units += english_count
            else:
                text_ok = source_counter == generated_counter
                total_source_blocks += len(source["hashes"])
                total_generated_blocks += len(generated["hashes"])
            source_images = Counter(source["image_names"])
            expected_images = source_images
            expected_formula_blocks = int(source["formulas"])
            if section.source == "ch18":
                expected_images = Counter(
                    name
                    for name in source["image_names"]
                    if name not in CH18_CONVERTED_IMAGES
                )
                converted_images = sum(
                    count
                    for name, count in source_images.items()
                    if name in CH18_CONVERTED_IMAGES
                )
                total_converted_images += converted_images
                expected_formula_blocks += sum(
                    count
                    for name, count in source_images.items()
                    if name in CH18_DISPLAY_FORMULA_IMAGES
                )
                formula_count_ok = (
                    int(generated["latex_blocks"]) >= expected_formula_blocks
                )
            else:
                generated_formula_blocks = int(generated["latex_blocks"])
                formula_count_ok = generated_formula_blocks == expected_formula_blocks
                reviewed_rewrite = REVIEWED_FORMULA_REWRITES.get(section.source)
                if not formula_count_ok and reviewed_rewrite is not None:
                    (
                        reviewed_source_count,
                        reviewed_generated_count,
                        reviewed_digest,
                    ) = reviewed_rewrite
                    formula_count_ok = (
                        expected_formula_blocks == reviewed_source_count
                        and generated_formula_blocks == reviewed_generated_count
                        and generated["latex_digest"] == reviewed_digest
                    )
            generated_images = Counter(generated["image_names"])
            images_ok = generated_images == expected_images
            formula_ok = (
                formula_count_ok
                and bool(generated["latex_balanced"])
                and not bool(generated["bad_latex_tokens"])
            )
            currency_ok = int(generated["bare_currency"]) == 0 or section.manual
            ok = text_ok and images_ok and formula_ok and currency_ok
            if not ok:
                failures.append(
                    f"{section.source}: text={text_ok}, images={images_ok}, "
                    f"formula={formula_ok}, currency={currency_ok}; "
                    f"images={sum(generated_images.values())}/{sum(expected_images.values())}, "
                    f"latex={generated['latex_blocks']}/{expected_formula_blocks}"
                )
            total_source_images += sum(expected_images.values())
            total_generated_images += sum(generated_images.values())
            total_formulas += int(source["formulas"])
    if failures:
        print(
            f"bilingual edition audit: FAIL ({len(failures)} retained sections)",
            file=sys.stderr,
        )
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print(
        "bilingual edition audit: PASS "
        f"({len(section_list())} retained files, "
        f"source fingerprints {total_generated_blocks}/{total_source_blocks}, "
        f"chapter 1 manual units {manual_generated_units}/{manual_source_units}, "
        f"non-formula images {total_generated_images}/{total_source_images}, "
        f"chapter 18 converted image occurrences {total_converted_images}, "
        f"source text formulas {total_formulas})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
