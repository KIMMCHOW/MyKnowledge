#!/usr/bin/env python3
"""Generate bilingual Markdown for every non-chapter item in the EPUB spine."""

from __future__ import annotations

import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


SECTIONS = [
    ("cover", "00-00-封面 Cover.md", 90, "封面", "Cover", "封面", "cover", None),
    ("title", "00-01-书名页 Title Page.md", 91, "书名页", "Title Page", "书名页", "title-page", None),
    (
        "copyright",
        "00-02-版权与使用条款 Copyright and Terms of Use.md",
        92,
        "版权与使用条款",
        "Copyright and Terms of Use",
        "版权页",
        "copyright",
        None,
    ),
    ("dedication", "00-03-献词 Dedication.md", 93, "献词", "Dedication", "献词", "dedication", None),
    ("contents", "00-04-原书目录 Contents.md", 94, "原书目录", "Contents", "目录", "contents", None),
    ("afterword", "26-结语 A Final Thought.md", 26, "结语", "A Final Thought", "结语", "afterword", None),
    (
        "appendixa",
        "27-附录A-期权术语表 Glossary of Option Terminology.md",
        27,
        "期权术语表",
        "Glossary of Option Terminology",
        "附录 A",
        "appendix-a",
        "A",
    ),
    (
        "appendixb",
        "28-附录B-实用数学 Some Useful Math.md",
        28,
        "实用数学",
        "Some Useful Math",
        "附录 B",
        "appendix-b",
        "B",
    ),
    ("index", "29-索引 Index.md", 29, "索引", "Index", "索引", "index", None),
    (
        "aboutauthor",
        "30-关于作者 About the Author.md",
        30,
        "关于作者",
        "About the Author",
        "作者简介",
        "about-author",
        None,
    ),
]


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    epubs = list(root.glob("*.epub"))
    if len(epubs) != 1:
        raise RuntimeError(f"expected one EPUB, found {len(epubs)}")
    output_dir = root / "Option Volatility and Pricing 双语版"
    worker = root / "tools" / "translate_epub_chapter.py"

    def run(section: tuple[str, str, int, str, str, str, str, str | None]):
        source, filename, number, chinese, english, label, key, source_label = section
        command = [
            sys.executable,
            str(worker),
            str(epubs[0]),
            f"ops/{source}.html",
            str(output_dir / filename),
            "--chapter-number",
            str(number),
            "--chinese-title",
            chinese,
            "--english-title",
            english,
            "--section-label",
            label,
            "--asset-key",
            key,
        ]
        if source_label:
            command.extend(["--source-label", source_label])
        if source == "index":
            command.append("--preserve-english")
        subprocess.run(command, cwd=root, check=True)
        return label, english

    print("running front and back matter with up to 3 workers", flush=True)
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {pool.submit(run, section): section for section in SECTIONS}
        for future in as_completed(futures):
            label, english = future.result()
            print(f"[{label} completed] {english}", flush=True)

    # Rebuilding the EPUB contents produces plain translated paragraphs.
    # Restore the Obsidian chapter/section links and verify every target.
    linker = root / "tools" / "link_book_contents.py"
    link_audit = root / "tools" / "audit_navigation_links.py"
    subprocess.run([sys.executable, str(linker)], cwd=root, check=True)
    subprocess.run([sys.executable, str(link_audit)], cwd=root, check=True)
    for script in (
        "repair_untranslated_prose.py",
        "normalize_visible_option_terms.py",
        "repair_latex_formulas.py",
    ):
        subprocess.run(
            [sys.executable, str(root / "tools" / script)],
            cwd=root,
            check=True,
        )
    subprocess.run(
        [sys.executable, str(root / "tools" / "build_option_knowledge_graph.py")],
        cwd=root,
        check=True,
    )
    subprocess.run(
        [sys.executable, str(root / "tools" / "audit_knowledge_graph.py")],
        cwd=root,
        check=True,
    )
    subprocess.run(
        [sys.executable, str(root / "tools" / "audit_translation_quality.py")],
        cwd=root,
        check=True,
    )
    subprocess.run(
        [sys.executable, str(root / "tools" / "audit_untranslated_prose.py")],
        cwd=root,
        check=True,
    )
    subprocess.run(
        [sys.executable, str(root / "tools" / "audit_bilingual_edition.py")],
        cwd=root,
        check=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
