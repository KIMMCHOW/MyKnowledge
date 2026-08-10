# SOP — 概念笔记与知识图谱规范

> 适用：`Knowledge/Concepts/` 下的概念笔记、知识图谱与生成/审计脚本。
> 关联：`docs/SOP_笔记整理.md`（Notes 专题笔记）、根目录 `AGENTS.md`（概念模板与 IStart-Note-AI 插件约定）、`ERROR_RETROSPECTIVE.md`（错误回溯）。

## 1. 概念笔记禁止序号

- 本节只约束 `Knowledge/Concepts/`。`Knowledge/Notes/` 是课程与阅读笔记区，可按 `docs/SOP_笔记整理.md` 使用两位系列编号。
- 概念笔记的**文件名、frontmatter、任意层级 Markdown 标题、wikilink 目标/别名、mermaid 节点标签**一律禁止把序号作为身份或结构标签（如 `C01`、`C34`、`01-`、`第N章`）；自写的正文导航同样不编号。
- 教材正文与知识图谱文件同样不使用序号前缀：章节文件名为纯 `中文 English.md`（如 `金融合约 Financial Contracts.md`）；章节顺序由 `tools/chapter_files.py` 的 `CHAPTER_STEMS` 清单集中维护，frontmatter 用机器字段 `chapter: NN`（如 `chapter: 01`），禁止写「第N章」文本。
- 辅助/审计文件（`完整性审计.md`、`知识图谱审计.md` 等）命名同样不带序号前缀；脚注 ID 内部前缀 `ovpNN` 是机器标识，不属于用户可见序号。
- 知识图谱的层级 MOC（`合约与损益语义.md` 等）与总图（`期权知识图谱.md`）的文件名和标题同样不加序号；层级关系由图结构与构建清单维护，不写「第N层」。
- 教材正文内的自然语言引用（如「在第 8 章中，我们表明」）是准确出处，保留；有语义的数字、公式参数与年份也不属于概念序号。标题、frontmatter、文件名、链接目标/别名、mermaid 标签中的结构序号一律清除。
- 反例（禁止）：`# C34 垂直价差与牛熊价差`、frontmatter `concept_id: C34` / `section: 第25章`、`[[Delta（Natenberg）|C26 Delta]]`、mermaid `C26["C26 Delta"]`、文件名 `C01-标的资产与现价.md` / `25-波动率合约 Volatility Contracts.md`。
- 自动审计：`powershell -NoProfile -ExecutionPolicy Bypass -File scripts/audit-concept-numbering.ps1`。脚本只检查 Concepts 文件名、`name` / `title` / `aliases` / `concept_id` / `section`、所有 Markdown 标题、mermaid 标签，以及 Concepts 内 wikilink 的目标和别名；当前基线为 0，不扫描 Notes 的合法系列编号。

## 2. 重名概念处理

- 概念与库内已有页面重名时，保留出处后缀：`Delta（Natenberg）`、`隐含波动率（Natenberg）`。
- 引用时目标用带后缀文件名，显示别名用短名：`[[Delta（Natenberg）|Delta]]`。
- 生成脚本中的重名映射维护在 `NOTE_NAME_OVERRIDES`。

## 3. 知识图谱生成与审计脚本

- 生成器：`Knowledge/Concepts/经济/金融/衍生品/期权/References/tools/build_option_knowledge_graph.py`
- 审计：`tools/audit_knowledge_graph.py`（输出 `知识图谱审计.md`）
- 修改生成器后必须先到临时目录重生成、与现状 diff（差异只能包含预期内容），确认后再写入真实目录；脚本会删除带 `generated_by` 标记的过期文件。
- 生成器、审计脚本与手改文件必须同批同步：禁止只手改文件而不同步生成器，反之亦然（见 E-012）。

## 4. 空概念页处理

- 空壳定义：`type: concept` + `status: empty` + `completion_status: pending`，正文为空模板。
- 检测：`rg "status: empty|completion_status: pending" Knowledge/Concepts`；正文过短（定义与核心解释全空）也按空壳处理。
- 当前基线：库内空概念页与 `Knowledge/Concepts/_未分类/` 均应为 0；发现新空壳后按 IStart-Note-AI 插件 JSON 流程补全（definition / explanation / examples / related_concepts / related_questions / tags / domain），完成后按插件步骤：更新 frontmatter → 移动到对应 domain → 更新 `_索引_<domain>.md` 与总索引 `Knowledge/Concepts/_索引_Concept.md`。
- 删除：仅允许删除无内容的重复空壳；删除前全局搜索 `[[概念名]]` 引用并改指；禁止删除非空概念。

## 5. 概念身份与插件匹配

- 概念候选必须同时满足：位于 `Knowledge/Concepts/` 且 frontmatter `type: concept`。索引、教材、模板、审计页不得进入自动双链候选。
- 概念解析按以下顺序执行：精确匹配文件 basename / frontmatter `name` / `aliases` → 对序号异常输入做规范化 → 仅在规范名唯一命中时复用已有页。多个页面命中时必须停止自动创建，不得猜测。
- AI 返回的概念名在生成 wikilink 和文件路径前统一做 NFC 规范化，并清理明确的列表序号前缀，如 `C01-`、`01-`、`1.`、`1）`。只有存在分隔符或空格时才视为序号，禁止误伤 `5G`、`3D打印`、`2型糖尿病`、`C++`。
- 发现 `[[C01-机会成本]]` 已唯一对应 `机会成本.md` 时，必须把链接目标改为实际 basename；只跳过重复创建但保留旧链接，仍会形成悬空节点。
- 插件的普通助手、阅读计划、Q&A、概念补全等入口必须复用同一解析规则；异步创建失败必须显示错误，不得静默丢失。

## 6. Frontmatter 标签完整性

- 概念页 `tags` 使用 YAML 列表，每个标签独占一行；保持 2–5 个标签。
- 禁止把多个标签折叠成单个列表项，例如 `- 政治   - 地缘政治   - 国家`。该写法在 YAML 中只有一个字符串，不是三个标签，会破坏搜索与图谱筛选。
- 审计命令：`rg -n --pcre2 -U '^tags:\r?\n[ \t]+-[^\r\n]+ {3}- [^\r\n]+ {3}- ' Knowledge/Concepts`；当前基线为 0。
- 批量修复前先生成 `before → after` 映射并确认分隔符、标签数量与例外均符合预期；写盘后复跑审计并抽查 frontmatter。

## 7. 未创建概念页（悬空链接）处理

- 先分类链接类型：
  1. 模板占位符（`_模板_*.md` 中的 `[[概念名]]`）→ 保留，不是悬空。
  2. 文件链接（`.pdf` / `.epub` / 带 `.md` 后缀）→ 确认目标文件存在，不是悬空。
  3. 标题/块锚点（`[[文件#标题]]`、`[[#^块ID]]`）→ 目标文件存在且标题匹配即有效，不是悬空。
  4. 真悬空（指向不存在的 Markdown 页且非上述类型）→ 按插件规则在 `Knowledge/Concepts/_未分类/` 创建空壳等待补全，或改指到正式概念。
- 检测：解析 `Knowledge/` 下所有 `[[...]]` 目标，与 `Knowledge/` 实际 `.md` 文件 stem 比对；解析时先处理表格转义 `[[目标\|别名]]`（`\|` 是表格内管道符，不是链接路径），再按 `|` 切分别名；对 `[[文件#标题]]` 需额外验证目标文件内存在该标题。
- 当前基线：`Knowledge/` 内真悬空链接与失效锚点均为 0；每次批量重命名/移动后重跑该检测（见 E-013）。

## 8. 提交校验

- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/audit-concept-numbering.ps1`；必须 PASS，禁止带序号概念回归。
- `git status` / `git diff --stat`；确认 `Raw Materials/`、`.obsidian/`、`AGENTS.md`、`__pycache__/` 未进入提交。
- 提交信息：`reorganize:` / `complete:` / `docs:` / `cleanup:` + 中文简述。
