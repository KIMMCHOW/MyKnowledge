#!/usr/bin/env python3
"""Generate bilingual Markdown drafts for chapters 2 through 25."""

from __future__ import annotations

import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


CHAPTERS = [
    (2, "远期定价", "Forward Pricing"),
    (3, "合约规格与期权术语", "Contract Specifications and Option Terminology"),
    (4, "到期盈亏", "Expiration Profit and Loss"),
    (5, "理论定价模型", "Theoretical Pricing Models"),
    (6, "波动率", "Volatility"),
    (7, "风险度量（一）", "Risk Measurement I"),
    (8, "动态对冲", "Dynamic Hedging"),
    (9, "风险度量（二）", "Risk Measurement II"),
    (10, "价差策略导论", "Introduction to Spreading"),
    (11, "波动率价差策略", "Volatility Spreads"),
    (12, "牛市与熊市价差", "Bull and Bear Spreads"),
    (13, "风险考量", "Risk Considerations"),
    (14, "合成头寸", "Synthetics"),
    (15, "期权套利", "Option Arbitrage"),
    (16, "美式期权的提前行权", "Early Exercise of American Options"),
    (17, "使用期权进行对冲", "Hedging with Options"),
    (18, "Black–Scholes 模型", "The Black-Scholes Model"),
    (19, "二叉树期权定价", "Binomial Option Pricing"),
    (20, "再论波动率", "Volatility Revisited"),
    (21, "头寸分析", "Position Analysis"),
    (22, "股票指数期货与期权", "Stock Index Futures and Options"),
    (23, "模型与现实世界", "Models and the Real World"),
    (24, "波动率偏斜", "Volatility Skews"),
    (25, "波动率合约", "Volatility Contracts"),
]


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    epubs = list(root.glob("*.epub"))
    if len(epubs) != 1:
        raise RuntimeError(f"expected one EPUB, found {len(epubs)}")
    output_dir = root / "Option Volatility and Pricing 双语版"
    worker = root / "tools" / "translate_epub_chapter.py"

    pending = [chapter for chapter in CHAPTERS if chapter[0] >= 2]

    def run_chapter(chapter: tuple[int, str, str]) -> tuple[int, str]:
        number, chinese, english = chapter
        output = output_dir / f"{chinese} {english}.md"
        subprocess.run(
            [
                sys.executable,
                str(worker),
                str(epubs[0]),
                f"ops/ch{number}.html",
                str(output),
                "--chapter-number",
                str(number),
                "--chinese-title",
                chinese,
                "--english-title",
                english,
            ],
            cwd=root,
            check=True,
        )
        return number, english

    print("running up to 3 chapters in parallel", flush=True)
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {pool.submit(run_chapter, chapter): chapter for chapter in pending}
        for future in as_completed(futures):
            number, english = future.result()
            print(f"[{number:02d}/25 completed] {english}", flush=True)
    # Rebuild the visible Obsidian outline after regenerating chapter files;
    # otherwise a translation refresh would silently remove chapter TOCs.
    subprocess.run(
        [sys.executable, str(root / "tools" / "add_chapter_navigation.py")],
        cwd=root,
        check=True,
    )
    # Rebuild the concept-first knowledge graph and fail fast on broken structure.
    for script in (
        "repair_untranslated_prose.py",
        "normalize_visible_option_terms.py",
        "repair_latex_formulas.py",
        "build_option_knowledge_graph.py",
        "audit_heading_structure.py",
        "audit_navigation_links.py",
        "audit_knowledge_graph.py",
        "audit_untranslated_prose.py",
        "audit_translation_quality.py",
        "audit_bilingual_edition.py",
    ):
        subprocess.run(
            [sys.executable, str(root / "tools" / script)],
            cwd=root,
            check=True,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
