#!/usr/bin/env python3
"""Audit EPUB-to-Markdown coverage, images, and displayed LaTeX formulas."""

from __future__ import annotations

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
from translate_epub_front_and_back_matter import SECTIONS
from translate_remaining_chapters import CHAPTERS


@dataclass(frozen=True)
class Section:
    source: str
    output: str
    number: str
    english_title: str
    source_label: str | None = None
    manual: bool = False


def section_list() -> list[Section]:
    sections = [
        Section("preface", "00-前言 Preface.md", "00", "Preface", manual=True),
        Section(
            "ch1",
            "01-金融合约 Financial Contracts.md",
            "1",
            "Financial Contracts",
            manual=True,
        ),
    ]
    sections.extend(
        Section(
            f"ch{number}",
            f"{number:02d}-{chinese} {english}.md",
            str(number),
            english,
        )
        for number, chinese, english in CHAPTERS
    )
    sections.extend(
        Section(source, filename, str(number), english, source_label)
        for source, filename, number, _chinese, english, _label, _key, source_label in SECTIONS
    )
    # Match the EPUB spine rather than filename order.
    order = {
        "cover": 0,
        "title": 1,
        "copyright": 2,
        "dedication": 3,
        "contents": 4,
        "preface": 5,
        **{f"ch{number}": 5 + number for number in range(1, 26)},
        "afterword": 31,
        "appendixa": 32,
        "appendixb": 33,
        "index": 34,
        "aboutauthor": 35,
    }
    return sorted(sections, key=lambda item: order[item.source])


def source_metrics(archive: zipfile.ZipFile, section: Section) -> dict[str, object]:
    root = ET.fromstring(archive.read(f"ops/{section.source}.html"))
    body = root.find(f"{XHTML_NS}body")
    if body is None:
        raise RuntimeError(f"{section.source}: missing body")
    hashes: list[str] = []
    images = 0
    formula_images = 0
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
            images += len(block_images)
            formula_images += int(css_class.startswith("eq"))
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
        "images": images,
        "formula_images": formula_images,
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
        "latex_blocks": latex_delimiters // 2,
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

    rows: list[str] = []
    failures: list[str] = []
    total_source_blocks = total_generated_blocks = 0
    total_source_images = total_generated_images = 0
    total_formulas = total_formula_images = 0

    with zipfile.ZipFile(epubs[0]) as archive:
        for section in section_list():
            output = output_dir / section.output
            if not output.exists():
                failures.append(f"{section.source}: 缺少 {section.output}")
                rows.append(f"| {section.source} | — | — | — | — | ❌ 缺少文件 |")
                continue
            source = source_metrics(archive, section)
            generated = markdown_metrics(output)
            source_counter = Counter(source["hashes"])
            generated_counter = Counter(generated["hashes"])
            if section.manual:
                coverage = "人工稿计数核对"
                # Manual files predate hash annotations; compare source paragraph
                # count with retained English callouts and verify all images.
                english_count = (
                    int(generated["quotes"])
                    + int(generated["footnotes"])
                    + int(generated["figure_captions"])
                )
                text_ok = english_count == int(source["text_blocks"])
            else:
                coverage = f"{sum((source_counter & generated_counter).values())}/{sum(source_counter.values())}"
                text_ok = source_counter == generated_counter
            images_ok = len(generated["images"]) == int(source["images"])
            formula_ok = (
                int(generated["latex_blocks"]) == int(source["formulas"])
                and bool(generated["latex_balanced"])
                and not bool(generated["bad_latex_tokens"])
            )
            currency_ok = int(generated["bare_currency"]) == 0 or section.manual
            ok = text_ok and images_ok and formula_ok and currency_ok
            if not ok:
                failures.append(
                    f"{section.source}: text={text_ok}, images={images_ok}, "
                    f"formula={formula_ok}, currency={currency_ok}"
                )
            status = "✅ 通过" if ok else "❌ 待处理"
            rows.append(
                f"| {section.source} | {len(source['hashes'])} | {coverage} | "
                f"{len(generated['images'])}/{source['images']} | "
                f"{generated['latex_blocks']}/{source['formulas']} + 图片 {source['formula_images']} | {status} |"
            )
            total_source_blocks += len(source["hashes"])
            total_generated_blocks += (
                len(generated["hashes"])
                if not section.manual
                else (
                    int(generated["quotes"])
                    + int(generated["footnotes"])
                    + int(generated["figure_captions"])
                )
            )
            total_source_images += int(source["images"])
            total_generated_images += len(generated["images"])
            total_formulas += int(source["formulas"])
            total_formula_images += int(source["formula_images"])

    overall = "通过" if not failures else "待处理"
    report = [
        "---",
        "title: Option Volatility and Pricing 双语版完整性审计",
        "tags:",
        "  - 期权",
        "  - 双语阅读",
        "  - 完整性审计",
        "created: 2026-08-03",
        f"status: {overall}",
        "---",
        "",
        "# 完整性审计 / Completeness Audit",
        "",
        "> [!summary] 审计范围",
        "> 按 EPUB 书脊顺序核对封面、书名页、版权页、献词、目录、前言、25 章正文、结语、两个附录、索引和作者简介。",
        "> 机器初译文件使用源块指纹逐块校验；前言和第 1 章为早期人工稿，使用英文段落数与图像数核对。",
        "",
        "| EPUB 部分 | 源块 | 文本覆盖 | 图像 | LaTeX 公式 + 公式图 | 结果 |",
        "|---|---:|---:|---:|---:|---|",
        *rows,
        "",
        "## 汇总",
        "",
        f"- EPUB 可处理源块：{total_source_blocks}",
        f"- Markdown 已核对块：{total_generated_blocks}",
        f"- 原书图像：{total_generated_images}/{total_source_images}",
        f"- 文本公式转 LaTeX：{total_formulas}",
        f"- 原 EPUB 以图片存储的公式（原样保留）：{total_formula_images}",
        "",
        "## 公式规则",
        "",
        "- 独立公式使用 `$$...$$`。",
        "- 变量、上下标、希腊字母和运算符不送入翻译接口。",
        "- `>>` 推导符转为 `\\Rightarrow`，Unicode 分数转为 `\\frac{...}{...}`。",
        "- 原 EPUB 中只有图片、无可靠公式文本的项目保留原图，不猜测转写。",
    ]
    if failures:
        report.extend(["", "## 待处理项", ""] + [f"- {item}" for item in failures])
    report.extend(["", "[[00-阅读导航|← 返回阅读导航]]", ""])
    report_path = output_dir / "99-完整性审计.md"
    report_path.write_text("\n".join(report), encoding="utf-8")
    print(f"wrote {report_path}")
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
