# MyKnowledge

个人 Obsidian 知识库：以数学、经济、金融与衍生品为核心的概念卡片、专题笔记和原始素材库。

## 目录结构

- `Knowledge/Concepts/<领域>/<子领域>/` — 概念笔记；领域总索引负责导航，子领域索引按基础、机制、应用与跨域接口组织
- `Knowledge/Concepts/数学/` — 博弈论、概率统计、分析与优化
- `Knowledge/Concepts/经济/` — 微观、宏观、劳动、制度行为、国际政治经济、能源、产业与金融
- `Knowledge/Concepts/经济/金融/衍生品/期权/` — 衍生品与期权的唯一专题入口，包含概念、Greeks、策略、练习和资料；通用数学概念统一归入 `Knowledge/Concepts/数学/`
- `Knowledge/Notes/Finance/` — 金融与交易研究专题（如 `Knowledge/Notes/Finance/Market Making/` 做市研究），索引见 `Knowledge/Notes/Finance/Market Making/_索引_做市.md`
- `Knowledge/Notes/Game Theory/` — 博弈论课程与应用笔记；不同来源的课程使用独立子专题和索引，禁止混入同一序列
- `Knowledge/Notes/` — 课程/阅读笔记，按专题子文件夹分类（`Knowledge/Notes/<专题>/`），索引见 `Knowledge/Notes/_索引_笔记.md`
- `Raw Materials/` — 原始素材，只读、禁止改动，不纳入 git 跟踪

总入口见 `Knowledge/Concepts/_索引_Concept.md`。每个主题只保留一个规范索引，避免平行目录和重复知识入口。

## PR / 贡献规则

- 默认不接受直接修改或新增 `Knowledge/Concepts/` 中概念笔记、领域索引的 PR；只有维护者明确提出或事先确认的知识库维护任务，才可在约定范围内修改，并须在 PR 说明授权背景与实际影响范围。
- 已有资料库可在明确授权下维护，例如 `Knowledge/Concepts/**/References/` 中的双语教材。教材、知识图谱与辅助文件使用无序号的语义化文件名和标题；阅读顺序由专题索引或集中映射清单维护，禁止把 `C01-`、`01-`、`第N章-` 等序号写入用户可见文件名、标题或链接。
- 批量移动或重命名笔记时，必须同时迁移普通、带标题锚点、带别名（含 Markdown 表格中的转义管道）及跨目录路径 wikilink；PR 中应附旧目标残留、悬空链接和相关生成/审计脚本的验证结果。
- 笔记类新内容按 `docs/SOP_笔记整理.md` 归入 `Knowledge/Notes/<专题>/`，不在根目录或 `Knowledge/Concepts/` 散落新文件夹。
- `Knowledge/Concepts/` 下的概念笔记、教材、知识图谱与辅助文件禁止把序号作为身份或结构标签（文件名，frontmatter 的名称、标题、别名、概念 ID 与章节标签，任意层级标题，wikilink 目标/别名，mermaid 标签）；自写的正文导航同样不编号。有语义的数字（如 `5G`、`2型糖尿病`）、公式参数、机器排序字段和准确的文献章节引用不属于概念序号。规范见 `docs/SOP_概念与知识图谱.md`，提交前运行 `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/audit-concept-numbering.ps1`。
- `Knowledge/Notes/` 是课程与阅读笔记区，允许按 `docs/SOP_笔记整理.md` 使用两位系列编号；该例外不得扩展到 `Knowledge/Concepts/`。
- `Raw Materials/` 为只读原始素材，不纳入 git。Obsidian 配置原则上属于本机状态；唯一允许提交的是根目录 `.obsidian/graph.json` 中的共享关系图颜色分组。主题、外观、工作区、插件状态以及其他 `.obsidian/` 文件一律不入库。若修改 `graph.json`，PR 必须说明颜色、查询范围和优先级变化，并确认未夹带主题或工作区设置。
- 提交前请先阅读根目录 `AGENTS.md`、`docs/SOP_笔记整理.md` 与 `ERROR_RETROSPECTIVE.md`。
