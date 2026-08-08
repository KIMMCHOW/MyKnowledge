# MyKnowledge

个人 Obsidian 知识库：课程笔记 + 概念卡片 + 原始素材。

## 目录结构

- `Knowledge/Concepts/<分类>/` — 概念笔记，统一使用 `type: concept` 模板并带 `domain` 字段；每个分类一个 `_索引.md`，总览见 `Knowledge/Concepts/索引.md`
- `Knowledge/Notes/` — 课程/阅读笔记（Game Theory 系列等），索引见 `Knowledge/Notes/_索引.md`
- `Raw Materials/` — 原始素材（Game Theory 中英文全文、词汇等），**只读、禁止改动**，且不纳入 git 跟踪
- `.Trash/`、`.claudian/`、`.obsidian/` 状态文件 — 本机使用，不提交

## 使用规则

- `Raw Materials/` 内容禁止修改、移动、删除或重命名
- `AGENTS.md` 禁止提交到 git
- 新建概念先归入已有分类；只有 `_索引.md` 或概念过少的分类再考虑合并/新建

详见根目录 `AGENTS.md`。
