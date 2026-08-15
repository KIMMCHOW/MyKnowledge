# SOP — 笔记整理规范（知识库标准）

> 本文件是 MyKnowledge 知识库**笔记整理的唯一标准**，适用于 AI 助手、手动整理与 PR 贡献。
> 关联规则：根目录 `AGENTS.md`（任务执行规则）、`README.md`（PR / 贡献规则）、`ERROR_RETROSPECTIVE.md`（错误回溯）。
> 概念笔记（`Knowledge/Concepts/`）另有插件约定（IStart-Note-AI v2.0.1）与 `docs/SOP_概念与知识图谱.md`，不适用本 SOP。

## 1. 目录结构

- 所有课程/阅读/研究专题笔记统一放在 `Knowledge/Notes/` 下，**每个专题一个子文件夹**：

```
Knowledge/Notes/
├── Game Theory/
│   ├── Game Theory 01 The Dating Game.md
│   └── Game Theory 29 Final Examination.md
├── Finance/
│   └── Market Making/
│       ├── _索引_做市.md
│       └── References/            # 该专题的 PDF 等资料
└── _索引_笔记.md                   # 唯一总索引
```

- 禁止在 `Knowledge/Notes/` 平铺散放笔记；禁止在根目录新建专题文件夹（旧 `Finance/` 等已迁入 `Knowledge/Notes/`）。
- 专题内部如需再分层（如 `Finance/Market Making/`），用一层子文件夹表达子专题；资料统一放该层 `References/`。

## 2. 文件夹与文件命名

- 专题文件夹：使用该专题的稳定名称（英文原名或中文名），如 `Game Theory`、`Finance`。
- 笔记文件：`<专题> NN <标题>.md`，其中 `NN` 是**两位数字编号**（`01`、`02` … `29`）。
  - 禁止使用单个数字（`Game Theory 7 America's Game` → `Game Theory 07 America's Game`）。
  - 系列编号在文件名中保留（如 `Game Theory 05 The World Game.md`），标题不含编号。
- 索引文件：`_索引_<分类名>.md`（如 `_索引_做市.md`、`_索引_笔记.md`），禁止裸 `_索引.md`。
- 非系列单篇笔记：`<主题名>.md` 直接放入对应专题文件夹，不强制编号。

## 3. 索引维护

- `Knowledge/Notes/_索引_笔记.md` 是笔记区唯一总入口，按专题分区（如 `## 课程：Game Theory`、`## 金融与交易专题`）。
- 每个专题可在其文件夹内维护 `_索引_<专题>.md`，总索引用短链指向它（如 `[[_索引_做市|做市研究]]`）。
- **新增/移动笔记后必须同步索引**：在对应分区追加 `- [[笔记名]]`；删除笔记时同步删除索引行。
- 同一主题只保留一个规范索引，不建立平行入口。

## 4. Wikilink 规范

- 优先短链 `[[笔记名]]`：库内名称唯一时不用路径前缀。
- 库内重名时才用路径链：`[[专题/笔记名]]` 或 `[[Knowledge/.../笔记名]]`。
- 别名显示用管道：`[[_索引_做市|做市研究]]`。
- Obsidian 已开启 `alwaysUpdateLinks`，移动/重命名笔记时链接会自动更新；本仓库内迁移仍须手动核对（见 §6）。

## 5. Frontmatter

- 笔记索引文件必须含 frontmatter：
  ```yaml
  ---
  type: notes-index
  domain: 经济        # 可选：专题归属领域
  subdomain: 金融      # 可选
  topic: 做市          # 可选：专题名
  ---
  ```
- 笔记本体不强求 frontmatter；需要时用 `type: note` + `tags`（2–5 个）。
- 概念笔记（`Knowledge/Concepts/`）的 frontmatter 遵循插件模板（`type: concept` 等），与本 SOP 无关。

## 6. 双链与移动完整性检查

移动、重命名或新增笔记后，按以下清单核对：

1. `git status` 确认移动范围正确、无意外文件。
2. 全局搜索旧路径残留：`rg "Knowledge/Notes/Game Theory 0"` 等（旧路径链接在新位置会失效）。
3. 核对总索引 `_索引_笔记.md` 与专题索引：新增/删除/移动的笔记均已同步。
4. 核对引用本专题的跨区文档：`README.md` 目录结构、`Knowledge/Concepts/_说明_关系图谱颜色组.md` 路径、相关概念索引；若目录负责关系图颜色，还要同步根目录 `.obsidian/graph.json`。
5. 确认 `Raw Materials/`、`AGENTS.md` 与 `.obsidian/` 本机状态文件未出现在改动中；唯一允许的 Obsidian 配置例外是根目录 `.obsidian/graph.json` 的共享颜色分组。

## 7. 整理流程（标准步骤）

1. 新建/接收笔记 → 放入 `Knowledge/Notes/<专题>/`，按 §2 命名。
2. 如属系列，检查编号连续性；新增专题则创建文件夹与 `_索引_<专题>.md`。
3. 更新 `Knowledge/Notes/_索引_笔记.md` 对应分区。
4. 检查并修正双链（§6）。
5. 提交：`git add` 精确文件 → commit（`reorganize:` / `docs:` / `cleanup:` 中文简述）→ push。

## 8. 注意事项

- `Raw Materials/` 只读（改动需用户明确确认）；`.Trash/`、`.claudian/` 及 `.obsidian/` 本机状态一律不提交。只有根目录 `.obsidian/graph.json` 的共享关系图颜色分组可以随相应笔记结构变更提交，主题、外观、工作区和插件状态不属于该例外。
- 本仓库位于 iCloud Drive：批量移动文件优先用资源管理器/PowerShell `Move-Item`，避免用 `git mv` 触发同步回滚；操作后立刻 `git status` 验证。
- 不删除有内容的笔记；合并/删除前先全局搜索引用并改指。
