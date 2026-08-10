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
| E-004 | 笔记索引曾保留一个带尾缀 `1` 的重复条目，但实际文件不存在，形成长期悬空双链。 | 索引不是事实来源，必须逐项核对实际 Markdown 文件；本次已删除不存在的重复条目，并保留真实文件对应的链接。 | 修改索引或重构目录后，对变更范围运行 wikilink 目标检查；只有可解析到实际文件的条目才能进入正式索引。 |
| E-005 | 过去按“材料使用了某个数学模型”分类，把战争、政治策略、制度行为等应用概念放进数学目录。 | 领域应由概念的研究对象决定；数学只保留可跨场景复用的形式模型、分布和分析工具。 | 已把应用概念归还政治、经济、历史、生物学、心理学和哲学；今后移动后必须同步 `domain/subdomain` 与分层索引。 |
| E-006 | 同一期权主题同时存在 `衍生品/期权` 与 `Derivative Instrument/Options` 两套目录和索引，造成入口重复与图谱分裂。 | 金融属于经济、衍生品属于金融；期权的规范路径为 `Knowledge/Concepts/经济/金融/衍生品/期权/`。 | 已合并内容并只保留 `_索引_期权.md`；任何专题只能有一个规范索引，旧路径迁移后必须定向检索残留。 |
| E-007 | zsh 批量移动循环使用变量名 `path`，覆盖了 zsh 与 `$PATH` 绑定的特殊数组，导致后续 `mv` 命令无法解析。 | 该失败发生在数学批量移动段，命令未执行且文件未丢失；改用 `file_path` 并用明确命令路径后完成。 | zsh 脚本禁止把 `path`、`PATH`、`home` 等特殊/系统名称用作任务变量；批量移动后立即核对源目录、目标数量和冲突。 |
| E-008 | 直接修改 `.obsidian/graph.json` 后，只检查磁盘 JSON 就误以为颜色组已在关系图界面生效。 | 已打开的 Obsidian 全局关系图不会自动热加载外部配置，仍可能保留旧的内存状态，并在面板中只显示旧颜色组。 | 修改图谱配置后必须关闭并重新打开全局关系图，再在“颜色组”面板核对组数、查询和实际节点颜色；本次已验证 4 组均加载。 |
| E-009 | 颜色组查询覆盖范围正确，但优先级顺序错误：期权 `Mathematics/` 同时命中衍生品与数学时，会先被染成期权色。 | Obsidian 对重叠查询采用靠前颜色组；路径存在包含关系时，宽泛的父领域会遮蔽更具体的功能领域。 | 颜色组固定按“交易 → 数学 → 衍生品 → 金融”排序；新增或修改重叠查询后必须用代表性路径逐项验证最终颜色。 |
| E-010 | 在 iCloud 管理目录（含 reparse point）下用 `git mv` 批量移动文件：同步回滚了已移动的 29 个 Game Theory 笔记（移回原平铺位置），且 `.git/index` 丢失、残留 `index.lock`，git 一度显示整库未跟踪。 | 文件本身未丢失；`git reset --mixed HEAD` 可从 HEAD 重建索引；改用 PowerShell `Move-Item` 后磁盘状态稳定，`git add -A` 正确识别为 rename。 | 本仓库批量移动一律用 `Move-Item` 不用 `git mv`；每次批量操作后立即 `git status` 并核对源/目标文件数量；index 异常时先确认无 git 进程，清除残留 `index.lock`，再 `git reset --mixed HEAD` 重建。 |
| E-011 | 远端 PR 为期权知识图谱/概念文件批量添加序号前缀（`C01-…C45-`、`01-…07-`、`00-`），违反 Concepts 命名规范。 | 序号属于 PR #2 引入的本地渲染排序；pre-PR（9bd1780）即为无序号命名，且部分概念直接去前缀会与其他概念重名（如 `Delta`），需恢复 pre-PR 命名（含 `（Natenberg）` 后缀）。 | 概念与知识图谱文件名一律不使用序号前缀；批量重命名前先对照 pre-PR 清单生成映射并校验目标集合，恢复既有命名并同步全部 wikilink（短链接、路径式、表格 `\|` 转义管道）；合并此类 PR 后先恢复命名再修内容。 |
| E-012 | 概念去序号只改了文件名与手改正文，生成脚本 `build_option_knowledge_graph.py` 仍输出 `Cxx-` 文件名与 `concept_id`、H1、wikilink 别名、mermaid 标签中的序号；审计脚本仍指向 `00-期权知识图谱`，一旦重新生成会把序号带回来。 | 生成器已改为无序号输出（`Layer.stem`/`Concept.stem` 去前缀、`NOTE_NAME_OVERRIDES` 处理重名、mermaid 用英文 slug、删除 `concept_id`、根文件 `期权知识图谱.md`），审计脚本同步更新，审计 PASS。 | 修改生成器后必须先到临时目录重生成并与现状 diff（差异只能含预期内容），再写入真实目录；生成器、审计脚本与手改文件必须同批同步，禁止只改一边；规范见 `docs/SOP_概念与知识图谱.md`。 |
| E-013 | 教材章节文件去 `NN-` 前缀后，依赖文件名 `{chapter:02d}-*.md` 的脚本未同步：`audit_footnote_links.py` / `convert_obsidian_footnotes.py` 的 `prefix_for()` 仍从文件名提取 `ovpNN`（去前缀后全部退化为 `ovp`），脚注审计全量 FAIL；`translate_epub_chapter.py` 默认仍写 `section: 第N章`。 | 章节顺序已集中维护在 `tools/chapter_files.py` 的 `CHAPTER_STEMS`，frontmatter 统一 `chapter: NN`；共享函数 `footnote_prefix()` 从 frontmatter/映射表取前缀；翻译脚本默认写 `chapter:`，仅显式 `--section-label`（附录）时写 `section:`。 | 所有依赖章节序号的脚本（生成器、审计、转换、翻译）必须引用 `chapter_files.py` 的清单/共享函数，禁止再用文件名 `NN-` 正则提取；批量去前缀后必须重跑全部审计（导航/标题/脚注/翻译质量/知识图谱）。 |
| E-014 | 批量概念补全把三个 YAML 标签写成一个列表项（如 `- 政治   - 地缘政治   - 国家`），表面可读但 Obsidian 只识别为一个长标签。 | 本次确认 136 个概念页命中同一格式错误，均可无歧义拆成三个非空标签；已统一恢复为每行一个 `- 标签`，不改正文。 | SOP 新增折叠标签审计；批量生成/补全后必须检查 `tags` 项数与 2–5 个约束，禁止只凭视觉判断 YAML 结构。 |
| E-015 | IStart-Note-AI 只用 `f.basename === concept` 判断概念存在，并把 Concepts 下的索引、教材和审计页一并当作已知概念；`C01-概念` 与 `概念` 因而被误判为不同页面。 | 当前磁盘上编号概念文件和编号 wikilink 均为 0，用户看到的是插件假阴性而非真实缺页；本机插件已加入序号规范化、`type: concept` 过滤、basename/name/aliases 唯一匹配与链接目标改写。 | 概念解析必须“精确优先、规范名唯一命中、歧义停止”，并覆盖 `C01-`、`01-`、`1.`、`1）` 与 `5G`/`3D打印` 等反例；`.obsidian` 不入库，插件升级或重装后必须复跑这些回归用例并向插件源码仓同步修复。 |
| E-016 | README 仍要求给 `Knowledge/Concepts/**/References` 教材和辅助文件添加编号，与无序号概念/教材 SOP 及当前文件事实冲突，可能在后续整理中重新引入 `00-`、`NN-`、`第N章-`。 | `Knowledge/Concepts/` 内的概念、教材、知识图谱和辅助文件均使用无序号语义名与无序号结构标题；`Knowledge/Notes/` 可按笔记 SOP 使用两位系列编号，两者不得混淆。 | 已删除 README 的旧 Concepts 编号规则，并新增 `scripts/audit-concept-numbering.ps1`；脚本检查 Concepts 的文件名、身份与章节 frontmatter、所有 Markdown 标题、mermaid 与内部 wikilink，基线必须为 0，不误扫 Notes。 |

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
# 概念/知识图谱序号前缀残留（应无 C\d\d- / 0\d- / 00- 前缀）
rg -n --glob "*.md" "\[\[[^\]]*\bC\d\d-" Knowledge
# 教材/图谱 frontmatter 第N章残留（应为 chapter: NN）
rg -n --glob "*.md" "^section: 第" "Knowledge/Concepts/经济/金融/衍生品/期权/References"
# 工具脚本内旧序号依赖残留（文件名 NN- 正则 / 第N章 拼接，应改为 chapter_files.py 共享逻辑）
rg -n --glob "*.py" "\\d\{2\\}|f.第\{int\(args\.chapter_number\)\}章" "Knowledge/Concepts/经济/金融/衍生品/期权/References/tools"
```

## 后续防线

- 所有索引文件使用 `_索引_<分类>.md` 命名；禁止裸 `_索引.md`；总索引为 `Knowledge/Concepts/_索引_Concept.md`。
- 编号一律两位数补零（`01`–`99`），禁止单个数字（如 `Game Theory 7` → `Game Theory 07`）。
- 关系图边标签只用 11 类规范标签（因果/影响/实例/对比/同义/包含/工具/背景/支撑/约束/相关），不发明自定义碎标签。
- `Raw Materials/` 任何改动必须先获得用户明确确认。
- 概念补全后手动执行与插件一致的一步：更新 frontmatter → 移动文件到 domain → 更新 `_索引_<domain>.md` 与总索引。
- 领域总索引只导航子领域；子领域索引按“基础 → 机制/模型 → 应用 → 跨域接口”组织，禁止重新退化为无结构文件名清单。
- 查看/校验含中文的 markdown 一律用 `Get-Content -Encoding UTF8` 或 `[System.IO.File]::ReadAllText`；判断「乱码」必须先做字节级 UTF-8 校验，禁止仅凭控制台显示删除文件。
- iCloud 目录批量移动文件用 `Move-Item` 不用 `git mv`；每次移动后立即 `git status` 核对；index 异常时清除残留 `index.lock` 后 `git reset --mixed HEAD` 重建。
- 提交前检查 `git status` / `git diff --stat`；`AGENTS.md`、`Raw Materials/`、`.obsidian` 状态文件绝不出现在提交中。

## 相关文档

- [AGENTS.md](AGENTS.md)（仓库规则，不入 git）
- [README.md](README.md)
