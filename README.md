# MyKnowledge

个人 Obsidian 知识库：以数学、经济、金融与衍生品为核心的概念卡片、专题笔记和原始素材库。

## 目录结构

- `Knowledge/Concepts/<领域>/<子领域>/` — 概念笔记；领域总索引负责导航，子领域索引按基础、机制、应用与跨域接口组织
- `Knowledge/Concepts/数学/` — 博弈论、概率统计、分析与优化
- `Knowledge/Concepts/经济/` — 微观、宏观、劳动、制度行为、国际政治经济、能源、产业与金融
- `Knowledge/Concepts/经济/金融/衍生品/期权/` — 衍生品与期权的唯一专题入口，包含概念、Greeks、数学、策略、练习和资料
- `Finance/` — 根目录研究专题（如 `Finance/Market Making/` 做市研究），索引见 `Finance/Market Making/_索引_做市.md`
- `Knowledge/Notes/` — 课程/阅读笔记（Game Theory 系列等），索引见 `Knowledge/Notes/_索引_笔记.md`
- `Raw Materials/` — 原始素材，只读、禁止改动，不纳入 git 跟踪

总入口见 `Knowledge/Concepts/_索引_Concept.md`。每个主题只保留一个规范索引，避免平行目录和重复知识入口。

## PR / 贡献规则

- 禁止在 PR 中修改或新增 `Knowledge/` 目录下的任何文件（概念笔记、索引、课程笔记等一律不允许改动）。
- 新内容只允许放在**根目录新建的文件夹**内（如 `新增主题/`），不得写入 `Knowledge/`、`Raw Materials/` 或 `.obsidian/`。
- `Raw Materials/` 为只读原始素材，不纳入 git；`.obsidian/` 为本机配置，一律不提交。
- 提交前请先阅读根目录 `AGENTS.md` 与 `ERROR_RETROSPECTIVE.md`。