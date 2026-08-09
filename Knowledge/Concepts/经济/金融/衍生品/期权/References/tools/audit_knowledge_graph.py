#!/usr/bin/env python3
"""Audit the generated concept-first option knowledge graph."""

from __future__ import annotations

import importlib.util
import re
import sys
from collections import deque
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EDITION = ROOT / "Option Volatility and Pricing 双语版"
GRAPH = EDITION / "知识图谱"
REPORT = EDITION / "知识图谱审计.md"
GENERATOR = ROOT / "tools" / "build_option_knowledge_graph.py"
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
FORBIDDEN = (
    "封面",
    "书名页",
    "版权与使用条款",
    "献词",
    "原书目录",
    "阅读导航",
    "翻译说明与术语表",
    "结语",
    "附录A-期权术语表",
    "附录B-实用数学",
    "索引",
    "关于作者",
    "知识图谱审计",
    "导航链接审计",
    "章节与标题结构审计",
    "翻译质量与风险审计",
    "完整性审计",
    "脚注链接审计",
    "未翻译正文审计",
)


def load_generator():
    spec = importlib.util.spec_from_file_location("option_graph_generator", GENERATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load graph generator")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def resolve_target(target: str, graph_stems: set[str]) -> Path | None:
    if target in graph_stems:
        return GRAPH / f"{target}.md"
    direct = EDITION / f"{target}.md"
    if direct.exists():
        return direct
    matches = list(EDITION.rglob(f"{target}.md"))
    return matches[0] if len(matches) == 1 else None


def audit() -> tuple[list[str], dict[str, int]]:
    generator = load_generator()
    failures: list[str] = []
    files = sorted(GRAPH.glob("*.md"))
    stems = {path.stem for path in files}
    expected_stems = {"期权知识图谱"}
    expected_stems.update(layer.stem for layer in generator.LAYERS)
    expected_stems.update(concept.stem for concept in generator.CONCEPTS)
    if stems != expected_stems:
        failures.append(
            f"图谱文件集不一致：应有 {len(expected_stems)}，实际 {len(stems)}"
        )

    link_graph: dict[str, set[str]] = {stem: set() for stem in stems}
    link_count = 0
    formula_notes = 0
    for path in files:
        text = path.read_text(encoding="utf-8")
        if text.count("$$") % 2:
            failures.append(f"{path.name}: LaTeX 块界定符不成对")
        if "$$" in text:
            formula_notes += 1
        for target in WIKILINK_RE.findall(text):
            link_count += 1
            if any(target.startswith(prefix) for prefix in FORBIDDEN):
                failures.append(f"{path.name}: 链接了排除节点 `{target}`")
            resolved = resolve_target(target, stems)
            if resolved is None:
                failures.append(f"{path.name}: 链接目标不存在或不唯一 `{target}`")
            if target in stems:
                link_graph[path.stem].add(target)
                link_graph[target].add(path.stem)

    root = GRAPH / "期权知识图谱.md"
    root_targets = set(WIKILINK_RE.findall(root.read_text(encoding="utf-8")))
    layer_stems = {layer.stem for layer in generator.LAYERS}
    if root_targets != layer_stems:
        failures.append("总图必须且只能链接 7 个层级 MOC")

    ids: list[str] = []
    for concept in generator.CONCEPTS:
        path = GRAPH / f"{concept.stem}.md"
        if not path.exists():
            failures.append(f"{concept.stem}: 概念页缺失")
            continue
        ids.append(concept.cid)
        text = path.read_text(encoding="utf-8")
        for heading in ("## 核心关系", "## 风险经理检查", "## 主要章节"):
            if heading not in text:
                failures.append(f"{path.name}: 缺少 `{heading}`")
        relation_lines = [line for line in text.splitlines() if line.startswith("- ") and "→" in line]
        if len(relation_lines) < 2:
            failures.append(f"{path.name}: 语义关系少于 2 条")
        if concept.formula and "## 关键公式" not in text:
            failures.append(f"{path.name}: 应有公式但未生成")

    if len(ids) != 45:
        failures.append("概念页必须完整存在（45 页）")

    edge_checks = 0
    cmap = {concept.cid: concept for concept in generator.CONCEPTS}
    for edge in generator.EDGES:
        source_text = (GRAPH / f"{cmap[edge.source].stem}.md").read_text(encoding="utf-8")
        target_text = (GRAPH / f"{cmap[edge.target].stem}.md").read_text(encoding="utf-8")
        expected_target = f"[[{cmap[edge.target].stem}|"
        expected_source = f"[[{cmap[edge.source].stem}|"
        if edge.verb not in source_text or expected_target not in source_text:
            failures.append(f"语义边缺失：{edge.source} —{edge.verb}→ {edge.target}")
            continue
        if edge.verb not in target_text or expected_source not in target_text:
            failures.append(f"反向追溯缺失：{edge.source} —{edge.verb}→ {edge.target}")
            continue
        edge_checks += 1

    reached: set[str] = set()
    queue: deque[str] = deque(["期权知识图谱"])
    while queue:
        current = queue.popleft()
        if current in reached:
            continue
        reached.add(current)
        queue.extend(link_graph.get(current, set()) - reached)
    if reached != stems:
        failures.append(f"图谱存在 {len(stems - reached)} 个从总图不可达的孤立节点")

    stats = {
        "files": len(files),
        "layers": len(generator.LAYERS),
        "concepts": len(ids),
        "edges": edge_checks,
        "expected_edges": len(generator.EDGES),
        "links": link_count,
        "formula_notes": formula_notes,
        "excluded_links": sum("\u94fe\u63a5\u4e86\u6392\u9664\u8282\u70b9" in failure for failure in failures),
    }
    return failures, stats


def write_report(failures: list[str], stats: dict[str, int]) -> None:
    ok = not failures
    lines = [
        "---",
        "title: Option Volatility and Pricing 知识图谱审计",
        "tags: [期权, 双语阅读, 知识图谱审计]",
        f"status: {'通过' if ok else '待处理'}",
        "created: 2026-08-03",
        "---",
        "",
        "# 知识图谱审计",
        "",
        "> [!summary] 结论",
        "> 图谱以概念因果关系而非文件导航为边；封面、版权、献词、作者与审计文件被排除。",
        "",
        "| 检查项 | 结果 |",
        "|---|---:|",
        f"| Markdown 节点 | {stats['files']} / 53 |",
        f"| 知识层 | {stats['layers']} / 7 |",
        f"| 核心概念 | {stats['concepts']} / 45 |",
        f"| 语义关系 | {stats['edges']} / {stats['expected_edges']} |",
        f"| 内部与章节链接 | {stats['links']} |",
        f"| 含 LaTeX 的概念页 | {stats['formula_notes']} |",
        f"| 不应进入图谱的链接 | {stats['excluded_links']} |",
    ]
    if failures:
        lines.extend(["", "## 待处理（前 50 项）", ""])
        lines.extend(f"- {failure}" for failure in failures[:50])
    lines.extend(["", "[[阅读导航|← 返回阅读导航]]", ""])
    REPORT.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    failures, stats = audit()
    write_report(failures, stats)
    if failures:
        print("knowledge graph audit: FAIL")
        for failure in failures[:30]:
            print(f"- {failure}")
        return 1
    print(
        "knowledge graph audit: PASS "
        f"({stats['layers']} layers, {stats['concepts']} concepts, "
        f"{stats['edges']} semantic edges, {stats['excluded_links']} excluded-file links)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
