#!/usr/bin/env python3
"""Generate the retained conclusion and two bilingual appendices."""

from __future__ import annotations

import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


SECTIONS = [
    ("afterword", "结语 A Final Thought.md", 26, "结语", "A Final Thought", "结语", "afterword", None),
    (
        "appendixa",
        "附录A-期权术语表 Glossary of Option Terminology.md",
        27,
        "期权术语表",
        "Glossary of Option Terminology",
        "附录 A",
        "appendix-a",
        "A",
    ),
    (
        "appendixb",
        "附录B-实用数学 Some Useful Math.md",
        28,
        "实用数学",
        "Some Useful Math",
        "附录 B",
        "appendix-b",
        "B",
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
        subprocess.run(command, cwd=root, check=True)
        return label, english

    print("generating retained back matter with up to 3 workers", flush=True)
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {pool.submit(run, section): section for section in SECTIONS}
        for future in as_completed(futures):
            label, english = future.result()
            print(f"[{label} completed] {english}", flush=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
