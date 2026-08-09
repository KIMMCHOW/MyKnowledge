# MyKnowledge

个人 Obsidian 知识库：以数学、经济、金融与衍生品为核心的概念卡片、专题笔记和原始素材库。

## 目录结构

- `Knowledge/Concepts/<领域>/<子领域>/` — 概念笔记；领域总索引负责导航，子领域索引按基础、机制、应用与跨域接口组织
- `Knowledge/Concepts/数学/` — 博弈论、概率统计、分析与优化
- `Knowledge/Concepts/经济/` — 微观、宏观、劳动、制度行为、国际政治经济、能源、产业与金融
- `Knowledge/Concepts/经济/金融/衍生品/期权/` — 衍生品与期权的唯一专题入口，包含概念、Greeks、数学、策略、练习和资料
- `Knowledge/Notes/Finance/` — 金融与交易研究专题（如 `Knowledge/Notes/Finance/Market Making/` 做市研究），索引见 `Knowledge/Notes/Finance/Market Making/_索引_做市.md`
- `Knowledge/Notes/Game Theory/` — Game Theory 课程系列笔记（01–29），按专题文件夹分类
- `Knowledge/Notes/` — 课程/阅读笔记，按专题子文件夹分类（`Knowledge/Notes/<专题>/`），索引见 `Knowledge/Notes/_索引_笔记.md`
- `Raw Materials/` — 原始素材，只读、禁止改动，不纳入 git 跟踪

总入口见 `Knowledge/Concepts/_索引_Concept.md`。每个主题只保留一个规范索引，避免平行目录和重复知识入口。

## PR / 贡献规则

- 禁止在 PR 中修改或新增 `Knowledge/Concepts/` 目录下的任何文件（概念笔记与索引由知识库维护流程统一管理）。
- 笔记类新内容按 `docs/SOP_笔记整理.md` 归入 `Knowledge/Notes/<专题>/`，不在根目录或 `Knowledge/Concepts/` 散落新文件夹。
- `Raw Materials/` 为只读原始素材，不纳入 git；`.obsidian/` 为本机配置，一律不提交。
- 提交前请先阅读根目录 `AGENTS.md`、`docs/SOP_笔记整理.md` 与 `ERROR_RETROSPECTIVE.md`。