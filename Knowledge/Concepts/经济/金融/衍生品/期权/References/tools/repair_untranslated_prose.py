#!/usr/bin/env python3
"""Replace silent English fallbacks with validated Chinese prose.

Every replacement is joined to the original EPUB by its source-block hash.
Existing cached Chinese is reused when it passes the current terminology and
number checks; otherwise the paragraph is retranslated with protected finance
terms and numeric literals.  An unsafe result is an error, never English UI.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from audit_untranslated_prose import scan_file  # noqa: E402
from translate_epub_chapter import (  # noqa: E402
    CONTROLLED_BLOCK_TRANSLATIONS,
    XHTML_NS,
    high_risk_translation_is_safe,
    inline_markdown,
    iter_blocks,
    normalize_translation,
    numeric_translation_is_safe,
    explicit_numbers,
    plain_text,
    plain_text_for_translation,
    source_hash,
    translation_language_is_safe,
    translate_protected_cached,
)


EDITION = ROOT / "Option Volatility and Pricing 双语版"
CACHE_DIR = EDITION / ".translation-cache"
REPAIR_CACHE = CACHE_DIR / "protected-repair.json"
MARKER_RE = re.compile(r"<!-- source:block ([0-9a-f]{16}) -->")


def source_blocks(epub: Path) -> dict[str, tuple[str, str, str]]:
    result: dict[str, tuple[str, str, str]] = {}
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
                english = plain_text(block)
                if not english:
                    continue
                digest = source_hash(block)
                value = (
                    english,
                    inline_markdown(block),
                    plain_text_for_translation(block),
                )
                previous = result.get(digest)
                if previous is not None and previous != value:
                    raise RuntimeError(f"source hash collision: {digest}")
                result[digest] = value
    return result


def load_old_cache() -> dict[str, str]:
    combined: dict[str, str] = {}
    for path in sorted(CACHE_DIR.glob("*.json")):
        if path == REPAIR_CACHE:
            continue
        combined.update(json.loads(path.read_text(encoding="utf-8")))
    return combined


def chunks(text: str) -> list[str]:
    if len(text) <= 1800:
        return [text]
    result: list[str] = []
    current = ""
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        if current and len(current) + len(sentence) + 1 > 1800:
            result.append(current)
            current = sentence
        else:
            current = f"{current} {sentence}".strip()
    if current:
        result.append(current)
    return result


def old_translation(text: str, cache: dict[str, str]) -> str | None:
    translated: list[str] = []
    for chunk in chunks(text):
        key = hashlib.sha256(
            ("tmt-noglossary-v1\0" + chunk).encode("utf-8")
        ).hexdigest()
        if key not in cache:
            return None
        translated.append(normalize_translation(cache[key], chunk))
    return " ".join(translated)


def marker_before(lines: list[str], one_based_callout: int) -> str | None:
    for index in range(one_based_callout - 1, -1, -1):
        match = MARKER_RE.fullmatch(lines[index])
        if match:
            return match.group(1)
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()

    epubs = list(ROOT.glob("*.epub"))
    if len(epubs) != 1:
        raise RuntimeError(f"expected one EPUB, found {len(epubs)}")
    sources = source_blocks(epubs[0])
    old_cache = load_old_cache()
    protected_cache = (
        json.loads(REPAIR_CACHE.read_text(encoding="utf-8"))
        if REPAIR_CACHE.exists()
        else {}
    )

    candidates: list[tuple[Path, dict[str, object]]] = []
    for path in sorted(EDITION.glob("*.md")):
        if path.name in {"29-索引 Index.md", "94-未翻译正文审计.md"}:
            continue
        candidates.extend((path, hit) for hit in scan_file(path))
    if args.limit is not None:
        candidates = candidates[: args.limit]

    reused = 0
    retranslated = 0
    rewritten = 0
    failures: list[str] = []
    by_path: dict[Path, list[str]] = {}

    for position, (path, hit) in enumerate(candidates, 1):
        lines = by_path.setdefault(path, path.read_text(encoding="utf-8").splitlines())
        digest = marker_before(lines, int(hit["callout_line"]))
        if not digest or digest not in sources:
            failures.append(f"{path.name}:{hit['callout_line']}: missing EPUB source")
            continue
        english, english_markdown, translation_source = sources[digest]
        chinese = CONTROLLED_BLOCK_TRANSLATIONS.get(digest)
        if chinese is None:
            chinese = old_translation(english, old_cache)
        if chinese is not None and (
            high_risk_translation_is_safe(english, chinese)
            and numeric_translation_is_safe(translation_source, chinese)
            and translation_language_is_safe(english, chinese)
        ):
            reused += 1
        else:
            try:
                chinese = translate_protected_cached(
                    translation_source,
                    protected_cache,
                    REPAIR_CACHE,
                    cache_namespace="tmt-domain-glossary-v9",
                )
            except Exception as error:
                chinese = None
            if chinese is None or not (
                high_risk_translation_is_safe(english, chinese)
                and numeric_translation_is_safe(translation_source, chinese)
                and translation_language_is_safe(english, chinese)
            ):
                try:
                    chinese = translate_protected_cached(
                        translation_source,
                        protected_cache,
                        REPAIR_CACHE,
                        cache_namespace="tmt-direct-glossary-v5",
                    )
                except Exception as error:
                    failures.append(f"{path.name}:{hit['visible_line']}: {error}")
                    continue
            retranslated += 1

        high_safe = high_risk_translation_is_safe(english, chinese)
        numeric_safe = numeric_translation_is_safe(translation_source, chinese)
        language_safe = translation_language_is_safe(english, chinese)
        if not (high_safe and numeric_safe and language_safe):
            failures.append(
                f"{path.name}:{hit['visible_line']}: unsafe result for {digest} "
                f"(terms={high_safe}, numbers={numeric_safe}, language={language_safe}, "
                f"source_numbers={dict(explicit_numbers(translation_source))}, "
                f"target_numbers={dict(explicit_numbers(chinese))})"
            )
            continue
        visible_index = int(hit["visible_line"]) - 1
        if visible_index >= len(lines):
            failures.append(f"{path.name}:{hit['visible_line']}: line moved")
            continue
        lines[visible_index] = str(hit.get("visible_prefix", "")) + chinese
        rewritten += 1
        if position % 25 == 0:
            print(
                f"[{position}/{len(candidates)}] reused={reused}, "
                f"retranslated={retranslated}",
                flush=True,
            )

    if failures:
        print("untranslated prose repair: FAIL")
        for failure in failures[:40]:
            print(f"- {failure}")
        return 1

    if not args.dry_run:
        for path, lines in by_path.items():
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        f"untranslated prose repair: PASS ({rewritten} rewritten; "
        f"{reused} cache-normalized, {retranslated} protected retranslations; "
        f"dry_run={args.dry_run})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
