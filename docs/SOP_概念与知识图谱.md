# SOP — 概念笔记与知识图谱规范

> 适用：`Knowledge/Concepts/` 下的概念笔记、知识图谱与生成/审计脚本。
> 关联：`docs/SOP_笔记整理.md`（Notes 专题笔记）、根目录 `AGENTS.md`（概念模板与 IStart-Note-AI 插件约定）、`ERROR_RETROSPECTIVE.md`（错误回溯）。

## 1. 概念笔记禁止序号

- 概念笔记的**文件名、frontmatter、H1 标题、wikilink 别名、mermaid 节点标签**一律禁止出现序号（如 `C01`、`C34`、`01-`）。
- 序号只允许出现在教材正文文件（`References/...双语版/` 下按书脊顺序编号的 `00-00-封面`、`01-金融合约` 等）与辅助/审计文件（`90-99` 段）；这是唯一例外。
- 知识图谱的层级 MOC（`合约与损益语义.md` 等）与总图（`期权知识图谱.md`）文件名同样不加序号；正文中「第N层」是层级语义描述，不是文件序号。
- 反例（禁止）：`# C34 垂直价差与牛熊价差`、frontmatter `concept_id: C34`、`[[Delta（Natenberg）|C26 Delta]]`、mermaid `C26["C26 Delta"]`、文件名 `C01-标的资产与现价.md`。

## 2. 重名概念处理

- 概念与库内已有页面重名时，保留出处后缀：`Delta（Natenberg）`、`隐含波动率（Natenberg）`。
- 引用时目标用带后缀文件名，显示别名用短名：`[[Delta（Natenberg）|Delta]]`。
- 生成脚本中的重名映射维护在 `NOTE_NAME_OVERRIDES`。

## 3. 知识图谱生成与审计脚本

- 生成器：`Knowledge/Concepts/经济/金融/衍生品/期权/References/tools/build_option_knowledge_graph.py`
- 审计：`tools/audit_knowledge_graph.py`（输出 `95-知识图谱审计.md`）
- 修改生成器后必须先到临时目录重生成、与现状 diff（差异只能包含预期内容），确认后再写入真实目录；脚本会删除带 `generated_by` 标记的过期文件。
- 生成器、审计脚本与手改文件必须同批同步：禁止只手改文件而不同步生成器，反之亦然（见 E-012）。

## 4. 空概念页处理

- 空壳定义：`type: concept` + `status: empty` + `completion_status: pending`，正文为空模板。
- 检测：`rg "status: empty|completion_status: pending" Knowledge/Concepts`；正文过短（定义与核心解释全空）也按空壳处理。
- 补全：按 IStart-Note-AI 插件 JSON 流程（definition / explanation / examples / related_concepts / related_questions / tags / domain），完成后按插件步骤：更新 frontmatter → 移动到对应 domain → 更新 `_索引_<domain>.md` 与总索引 `Knowledge/Concepts/_索引_Concept.md`。
- 删除：仅允许删除无内容的重复空壳；删除前全局搜索 `[[概念名]]` 引用并改指；禁止删除非空概念。

## 5. 未创建概念页（悬空链接）处理

- 先分类链接类型：
  1. 模板占位符（`_模板_*.md` 中的 `[[概念名]]`）→ 保留，不是悬空。
  2. 文件链接（`.pdf` / `.epub` / 带 `.md` 后缀）→ 确认目标文件存在，不是悬空。
  3. 真悬空（指向不存在的 Markdown 页且非模板）→ 按插件规则在 `Knowledge/Concepts/_未分类/` 创建空壳等待补全，或改指到正式概念。
- 检测：解析 `Knowledge/` 下所有 `[[...]]` 目标，与 `Knowledge/` 实际 `.md` 文件 stem 比对；处理 `.md` 后缀与路径式链接。

## 6. 提交校验

- `git status` / `git diff --stat`；确认 `Raw Materials/`、`.obsidian/`、`AGENTS.md`、`__pycache__/` 未进入提交。
- 提交信息：`reorganize:` / `complete:` / `docs:` / `cleanup:` + 中文简述。