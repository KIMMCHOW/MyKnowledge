#!/usr/bin/env python3
"""Convert retained EPUB footnotes into linked Obsidian Markdown footnotes."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

from audit_translation_quality import epub_source_blocks


ROOT = Path(__file__).resolve().parents[1]
EDITION = ROOT / "Option Volatility and Pricing 双语版"
NOTE_RE = re.compile(r"^> \[!note\] Footnote \d+")
MARKER_RE = re.compile(r"<sup>(\d+)</sup>")
SOURCE_BLOCK_RE = re.compile(r"<!-- source:block ([0-9a-f]{16}) -->")


def prefix_for(path: Path) -> str:
    from chapter_files import footnote_prefix
    return footnote_prefix(path)


def number_spans(text: str, number: str) -> list[tuple[int, int]]:
    pattern = re.compile(rf"(?<![\d]){re.escape(number)}(?![\d])")
    return [match.span() for match in pattern.finditer(text)]


def add_reference(
    target: str,
    source_display: str,
    translation_source: str,
    marker_match: re.Match[str],
    footnote_id: str,
) -> str:
    reference = f"[^{footnote_id}]"
    if reference in target:
        return target
    marker = marker_match.group(1)
    source_count = len(number_spans(translation_source, marker))
    candidates = number_spans(target, marker)
    if len(candidates) > source_count:
        source_ratio = marker_match.start() / max(1, len(source_display))
        start, end = min(
            candidates,
            key=lambda span: abs(span[0] / max(1, len(target)) - source_ratio),
        )
        return target[:start] + reference + target[end:]
    spacer = "" if target.endswith((" ", "\t")) else " "
    return f"{target}{spacer}{reference}"


def strip_old_marker(text: str, marker: str) -> str:
    text = text.removeprefix("> ").strip()
    return re.sub(
        rf"^(?:<sup>{re.escape(marker)}</sup>|\[{re.escape(marker)}\]|{re.escape(marker)}\.?)\s*",
        "",
        text,
    )


def marker_before(lines: list[str], index: int) -> str | None:
    for cursor in range(index - 1, -1, -1):
        match = SOURCE_BLOCK_RE.fullmatch(lines[cursor])
        if match:
            return match.group(1)
    return None


def convert(
    path: Path, source_blocks: dict[str, tuple[str, str, tuple[str, ...]]]
) -> int:
    lines = path.read_text(encoding="utf-8").splitlines()
    prefix = prefix_for(path)
    defined_markers: set[str] = set()
    for index, line in enumerate(lines[:-2]):
        if not NOTE_RE.match(line):
            continue
        marker_match = MARKER_RE.search(lines[index + 1])
        if not marker_match:
            continue
        marker = marker_match.group(1)
        defined_markers.add(marker)

    changed = 0
    index = 0
    while index < len(lines):
        if not lines[index].startswith("> [!quote]- English "):
            index += 1
            continue
        cursor = index + 1
        source_lines: list[str] = []
        while cursor < len(lines) and lines[cursor].startswith("> "):
            source_lines.append(lines[cursor][2:])
            cursor += 1
        while cursor < len(lines) and not lines[cursor].strip():
            cursor += 1
        if cursor >= len(lines):
            index = cursor + 1
            continue
        if lines[cursor].strip() == "$$":
            digest = marker_before(lines, index)
            source_markers = (
                source_blocks.get(digest, ("", "", ()))[2] if digest else ()
            )
            close = cursor + 1
            while close < len(lines) and lines[close].strip() != "$$":
                close += 1
            references = [
                f"[^{prefix}-{marker}]"
                for marker in source_markers
                if marker in defined_markers
            ]
            if references:
                reference_line = " ".join(references)
                following = lines[close + 1] if close + 1 < len(lines) else ""
                if reference_line not in following:
                    lines.insert(close + 1, reference_line)
                    changed += 1
            index = close + 2
            continue
        source = " ".join(source_lines)
        target = re.sub(
            rf"\[\^{re.escape(prefix)}-(\d+)\]", r"\1", lines[cursor]
        )
        digest = marker_before(lines, index)
        if digest and digest in source_blocks:
            _english, translation_source, source_markers = source_blocks[digest]
        else:
            translation_source, source_markers = source, ()
        marker_occurrence: Counter[str] = Counter()
        for marker in source_markers:
            marker_occurrence[marker] += 1
            candidates = [
                match for match in MARKER_RE.finditer(source) if match.group(1) == marker
            ]
            if candidates:
                occurrence = min(marker_occurrence[marker] - 1, len(candidates) - 1)
                # Footnote backlinks usually follow any mathematical use of
                # the same digit, so select from the end when ambiguous.
                marker_match = candidates[-1 - occurrence]
            else:
                marker_match = re.search(f"({re.escape(marker)})", source)
                if marker_match is None:
                    continue
            target = add_reference(
                target,
                source,
                translation_source,
                marker_match,
                f"{prefix}-{marker}",
            )
        if target != lines[cursor]:
            lines[cursor] = target
            changed += 1
        index = cursor + 1

    note_targets: dict[str, tuple[int, str]] = {}
    for index, line in enumerate(lines[:-2]):
        if not NOTE_RE.match(line):
            continue
        marker_match = MARKER_RE.search(lines[index + 1])
        if not marker_match:
            continue
        marker = marker_match.group(1)
        cursor = index + 2
        while cursor < len(lines) and not lines[cursor].strip():
            cursor += 1
        if cursor < len(lines):
            note_targets[marker] = (cursor, strip_old_marker(lines[cursor], marker))

    for marker, (target_index, chinese) in sorted(
        note_targets.items(), key=lambda item: item[1][0], reverse=True
    ):
        footnote_id = f"{prefix}-{marker}"
        if lines[target_index].startswith(f"[^{footnote_id}]:"):
            continue
        lines[target_index : target_index + 1] = ["", f"[^{footnote_id}]: {chinese}"]
        changed += 1

    if changed:
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return changed


def main() -> int:
    epubs = list(ROOT.glob("*.epub"))
    if len(epubs) != 1:
        raise RuntimeError(f"expected one EPUB, found {len(epubs)}")
    source_blocks = epub_source_blocks(epubs[0])
    files = 0
    changes = 0
    for path in sorted(EDITION.glob("*.md")):
        count = convert(path, source_blocks)
        if count:
            files += 1
            changes += count
    print(f"converted Obsidian footnotes: {changes} changes in {files} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
