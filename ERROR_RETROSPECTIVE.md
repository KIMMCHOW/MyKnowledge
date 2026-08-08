# ERROR_RETROSPECTIVE.md — 知识库错误回溯

本文记录 AI 助手处理本知识库（MyKnowledge vault）时曾经犯过、且可能复发的重复错误：批量整理、索引/关系图维护、概念补全、git 提交、iCloud 同步与 Raw Materials 保护等。开始整库审计、批量重命名/移动、关系图重构、概念批量补全或 git 清理前，必须先阅读本文。

## 执行规则

- 文档与仓库实际文件、git 跟踪状态或已验证事实冲突时，以实际文件和已验证状态为准，然后更新或删除过期文档；不要为迎合旧文档而改动内容。
- `Raw Materials/` 默认只读：任何修改、移动、删除、重命名都必须先获得用户明确确认，未经确认不得改动。
- 绝不打印或提交密钥、本机路径配置、iCloud 内部状态；只汇报脱敏状态（`set` / `missing` / `存在` / `缺失` 等）。
- `AGENTS.md`、`.obsidian/workspace*.json`、`.obsidian/graph*.json`、`.obsidian/plugins/*/data.json`、`.Trash/`、`Raw Materials/` 不得进入任何 commit。

## 错误回溯 SOP

任何任务中发现新的重复错误、过期规则、文档/文件冲突、批量操作失败模式、iCloud 同步差异或 agent 行为错误时，必须执行：

1. 先搜索本文，判断是否命中现有 `E-XXX` 条目。
2. 新问题则在错误记录表追加下一个 `E-XXX` 条目。
3. 记录三项：过期假设、当前文件/事实、修复或防复发防线。
4. 不写入密钥、token、真实隐私路径。
5. 未修复的问题必须把防线标为「未完成」，并列出下一步精确验证动作。
6. 最终汇报必须说明新增/更新的条目；不需要时写 `Error Retrospective Updated: Not needed` 并说明原因。

## 错误记录

| ID | 错误 | 当前事实 | 已修复或已加防线 |
| --- | --- | --- | --- |
| E-001 | 批量关系图/双链替换时用一次性脚本直接写盘，映射错误导致部分 `[[双链]]` 与边标签被误改。 | 关系图、索引、双链必须以 Obsidian 实际文件（frontmatter、`[[wikilink]]`、`_索引_*.md`）为准；批量替换前必须先生成映射清单并核对，再执行写盘。 | 批量改动前先 `git status` / `git diff --stat` 并抽样核对；复杂替换用两段式脚本（先生成清单、再执行），完成后抽查双链完整性。 |
| E-002 | 在 iCloud 同步目录（`iCloud~md~obsidian`，含 reparse point）下用 `os.walk` / `Copy-Item` 递归遍历或复制，导致遍历失败或嵌套目录被重复复制。 | 该目录由 iCloud 管理，文件可能带 reparse 属性；递归操作必须限定明确子目录白名单，写文件优先 `[System.IO.File]::WriteAllText`（UTF-8 无 BOM）。 | 批量文件操作只针对明确白名单目录；每次写盘后抽查数量与路径；禁止对整库递归移动/复制。 |

| E-003 | 用 Windows PowerShell 5.1 的 `Get-Content` 查看含中文的 UTF-8 文件时，控制台按 ANSI/GBK 解码导致中文显示成乱码，曾因此误判 iCloud 同步产生的 `xxx 2.md` 副本为损坏文件并删除。 | iCloud 同步冲突会生成 `xxx 2.md` 重复副本，内容为有效 UTF-8 且与 git HEAD 逐字节一致；判断文件是否损坏必须先做字节级 UTF-8 校验（`[System.IO.File]::ReadAllText` 或严格 `UTF8Encoding`），不能依赖 PS 5.1 控制台显示。 | 查看中文文件用 `Get-Content -Encoding UTF8`；删除任何副本前先与 git 版本逐字节比对；发现 `xxx 2.md` 先比对 HEAD 再处理。 |
## 检索清单

声称清理/整理完成前，对以下模式做定向检索：

```powershell
# 旧索引命名残留（应为 _索引_<分类>.md）
rg -n --glob "*.md" "\[\[[^\]|]*_索引\.md" Knowledge
# 未补全的空概念
rg -n --glob "*.md" "status: empty|completion_status: pending" Knowledge/Concepts
# 可能误引用/误改原始素材的地方（Raw Materials 只读）
rg -n --glob "*.md" "Raw Materials" . --glob "!AGENTS.md" --glob "!ERROR_RETROSPECTIVE.md"
# 单数字编号残留（应补零为两位数，仅作线索，需人工判断）
rg -n --glob "*.md" "第[1-9][^0-9]|[^0-9][1-9]号|[^0-9][1-9]\.md" Knowledge
```

## 后续防线

- 所有索引文件使用 `_索引_<分类>.md` 命名；禁止裸 `_索引.md`；总索引为 `Knowledge/Concepts/_索引_Concept.md`。
- 编号一律两位数补零（`01`–`99`），禁止单个数字（如 `Game Theory 7` → `Game Theory 07`）。
- 关系图边标签只用 11 类规范标签（因果/影响/实例/对比/同义/包含/工具/背景/支撑/约束/相关），不发明自定义碎标签。
- `Raw Materials/` 任何改动必须先获得用户明确确认。
- 概念补全后手动执行与插件一致的一步：更新 frontmatter → 移动文件到 domain → 更新 `_索引_<domain>.md` 与总索引。
- 查看/校验含中文的 markdown 一律用 `Get-Content -Encoding UTF8` 或 `[System.IO.File]::ReadAllText`；判断「乱码」必须先做字节级 UTF-8 校验，禁止仅凭控制台显示删除文件。
- 提交前检查 `git status` / `git diff --stat`；`AGENTS.md`、`Raw Materials/`、`.obsidian` 状态文件绝不出现在提交中。

## 相关文档

- [AGENTS.md](AGENTS.md)（仓库规则，不入 git）
- [README.md](README.md)