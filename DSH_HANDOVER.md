# 科研知识学习中心｜dsh 项目交付文档

交付日期：2026-10-27。交付对象：接手本工作区的 dsh / AI Agent。

本文基于当前磁盘文件、配置、构建目录、Git 状态和项目日志整理。本次仅编写交接文档，未重新构建、提交、推送或部署；不把历史验收报告视为本次实测结果。

## 1. 项目目标与入口

项目将教材、科研技能教程、配套代码、Notebook、图片、课件及外部教学视频集中整理为可持续维护的知识网站。主要使用场景是按分类找课程、按章节阅读教材、阅读公式与代码、下载配套资源，以及查看部分机器人教材的交互图。

- 本机工作区：`D:\Userdata\Desktop\公共知识\mkdocstutorial`
- 网站项目根目录：`D:\Userdata\Desktop\公共知识\mkdocstutorial\ebook-reader`
- Python 环境：`D:\Userdata\Desktop\公共知识\mkdocstutorial\.venv`
- GitHub：<https://github.com/Nitgomare/ebook-reader>
- 生产站点：<https://research-knowledge-hub.pages.dev/>
- Cloudflare Pages 项目：`research-knowledge-hub`，生产分支为 `main`。

以上线上地址是项目已配置入口；本次没有登录云平台重新核验在线状态。

## 2. 接手时先做什么

1. 完整阅读 `AGENTS.md`、本文和 `AUTHENTICATION.md`。
2. 查看 `git status --short`、`git diff --stat`、`git log -5 --oneline`、`git worktree list`，保留所有已有改动。
3. 阅读 `CHANGELOG.md` 最新记录，区分“已部署”“本地构建”“待验收”。
4. 核对 `books.json` 与 `content/books/`；不要只依赖旧交接文档中的数量。
5. 收到明确任务后再修改。交接本身不授权恢复暂停事项、发布积压改动或更改账号配置。

旧 `PROJECT_HANDOFF.md` 仍有架构和交互图细节可参考，但其 2026-09-24 的课程数量、分类数量及工作区描述已经过时。当前状态以本文、配置和实际检查为准。

## 3. 当前状态与最重要的风险

### 3.1 本地内容快照

本次读取到：

| 对象 | 状态 |
| --- | --- |
| `books.json` | 24 套内容、8 个分类 |
| `dist/data/catalog.json` | 24 套内容、314 个阅读页面、216 个代码/数据文件 |
| `tmp/changelog-release-20261026/data/catalog.json` | 23 套内容、294 个阅读页面、216 个代码/数据文件 |
| 最新日志中的正式发布 | 2026-10-26 的更新日志入口发布，23 套内容、294 个页面 |

**目录数量不代表验收或部署成功。** 当前 `dist/` 比最近一次日志记录的发布包多了《机械原理》。不能直接上传 `dist/` 并声称只是部署交接文档。

八类分别是：管理科学与运筹优化、科研工具与实践、Python 编程、Python 数据分析、机器学习与人工智能、智能机器人、风电技术、工程系统与技术文档。ID 与顺序见 `books.json` 的 `site.categories`。

### 3.2 Git 不是干净状态

本次读取的本地 `main` HEAD 为 `106fbc6`，本地已缓存的 `origin/main` 为 `3c0ab4d`。二者不是同一个提交；远程引用尚不能代替一次最新联网核验。

存在大量已修改及未跟踪文件，包括：

- `books.json`、`build.py`、`CHANGELOG.md`。
- `public/app.js`、`public/index.html`、`public/styles.css`。
- `public/reader-mode.js`、PPT 资源库与日志页面等未跟踪文件。
- 管理运筹学、SolidWorks、《机械原理》的内容目录、导入工具和清点报告。
- 科研汇报 PPT 的正文、课件和幻灯片产物。
- 大量 `dist/` 内容、`tmp/`、PRD 与演示讲稿。

部分“未提交”内容可能已经部署上线。不得用 Git 状态判断它们可以删除，也不得一键暂存所有改动。

另有 worktree：`D:\Userdata\Desktop\dataanalysis\reading-publish`，分支 `publish/immersive-reading-20261014`。不得当作本次临时文件清理。

禁止执行 `git reset --hard`、`git clean -fd`、整库覆盖、强制推送或未经核对的 pull/rebase。先联网 fetch、比较双方历史并确定发布基线；需要隔离工作时使用新的分支/worktree，明确复制哪些改动。Windows 路径较长，完整 checkout 可能失败，可用经过核对的稀疏 worktree；不能把初始化未完成的空索引误当成全库删除。

### 3.3 两项明确待办

**《机械原理（第四版）》：本地已录入，尚不能声称已部署。**

- 用户要求部署，内容提供者：熊忠帅；原书主编：潘存云、赵又红。两者不能混写。
- slug：`mechanism-principles-4e`，分类：`robotics`。
- 源目录：`D:\Userdata\Desktop\公共知识\扫描书籍\机械原理_中南第4版_熊忠帅_v01\机械原理_中南第4版_熊忠帅_v01\02_MD`。
- 已有 `content/books/mechanism-principles-4e/`、`books.json` 注册项及本地 `dist/` 产物。
- 导航为前置内容、15 章、两个附录、参考文献、作者简介，共 20 个页面。
- 导入工具：`tools/import_mechanism_principles.py`；报告：`resource-inventory/mechanism-principles-4e/import-report.json`。
- 现存报告记录源图片 1064 个、引用图片 578 个、缺图 0、图题标记 474 个。这些是报告数据，不等同于本次逐页验收。
- 用户随后改为要求项目交接，本次未继续发布。下一位应先确认是否恢复此任务，再完成全站检查、公式/表格/图片和移动端验收、日志、提交与部署。
- 不要直接重新运行导入脚本覆盖已有内容；先看脚本参数、报告和已有文件差异。

**《Jupyter Notebook 使用与应用》ZIP：用户明确暂停。**

- 内容提供者：王楷。
- ZIP 来源：`D:\18066\Documents\xwechat_files\wxid_xktvqdqc6uuj22_e10c\msg\file\2026-10\Jupyter Notebook 使用与应用(1).zip`。
- 用户原话：“暂停部署，别挂了”。未经重新要求，不录入、不上线。
- 2026-10-23 已给旧“科研计算基础与环境搭建”课程添加的 Jupyter 补充视频是另一项已记录工作，不要因暂停 ZIP 而删除该入口。

## 4. 实际技术架构

这是自定义构建的静态网站，**不是直接运行 MkDocs 的网站，也不是已有 FastAPI/Flask 业务后端的系统**。

```text
books.json + 每本书 mkdocs.yml + Markdown / 图片 / 代码 / 课件
                              ↓
                     build.py（Python）
                              ↓
        HTML 正文 JSON + 目录 JSON + 下载文件 + 前端静态文件
                              ↓
        原生 JavaScript 页面 + Cloudflare Worker 访问控制
                              ↓
                   Cloudflare Pages
```

- `mkdocs.yml` 只提供书名、文档根目录与导航顺序；正式构建不要使用 `mkdocs build`。
- 前端：`public/app.js`、`styles.css`、`index.html`；沉浸阅读：`reader-mode.js`。
- 正文：Python Markdown、Pygments、pymdown-extensions；公式由前端 MathJax 渲染。
- 浏览器实际读取 `data/docs/<id>.json` 内预渲染的 HTML，而非直接打开源码 Markdown。
- GitHub 用于版本管理；Cloudflare 发布目前使用 Wrangler 命令。不要在未核对配置前假设 push 后必然自动发布。
- 当前页面的 MathJax 脚本引用 CDN，因此不能承诺整站离线可用；交互图有独立的无外网依赖要求。

## 5. 目录与修改入口

| 路径（相对项目根目录） | 用途 |
| --- | --- |
| `books.json` | 分类、课程元数据、作者、内容提供者、视频和资源配置 |
| `content/books/<slug>/mkdocs.yml` | 章节顺序，增删章节必须同步 |
| `content/books/<slug>/docs/` | Markdown、图片、交互 HTML、下载资源 |
| `content/books/<slug>/code/` | Python、Notebook、配套数据 |
| `public/` | 前端与 Worker 源文件，不能只修改 dist 中的副本 |
| `build.py` | 正式构建、链接重写、资源复制及日志页生成 |
| `verify.py` | 构建结果、路径与资源检查 |
| `manage.py` | 构建、检查、本地预览入口 |
| `tools/` | 内容导入、交互图生成、验收及认证测试 |
| `resource-inventory/` | 来源清点、导入报告与追溯信息 |
| `dist/` | 可部署产物，不是内容源目录；2026-10-27 起已不再入库（`.gitignore`），发布时现场构建 |
| `tmp/` | 历史发布快照，已移出仓库并整体忽略；需要追溯时用 `_backup/` 里的还原点 |

正文 ID 由书籍 slug 和 Markdown 相对路径生成。改路径会改变章节 URL，应先考虑旧链接兼容。主要前端路由为 `#/resources/<slug>` 和 `#/doc/<id>`；从生成的 catalog 取得实际 ID，不要猜。

注册内容时使用已有字段：`slug`、`title`、`author`、`contentProvider`、`description`、`tags`、`category`、`order`、`type`。其他课程已有 `docAuthors`、`resourceLinks`、`localVideos`、`homePage` 等扩展，修改前阅读对应现有实例与构建/前端消费逻辑。

## 6. 已确定的产品要求

- 首页简洁、保留分类与课程卡片，不写“不是……而是……”等空泛宣传文案。
- 点击课程先看到资源或课程介绍，不要未经要求直接跳第一章；保留已有课程的首页例外配置。
- 只给读者展示必要信息。缺件清点、发布过程、内部技术说明放维护文档，不堆在阅读页面。
- 署名准确区分原作者、主编、教程作者和内容提供者；不能擅自替换或补造姓名。
- 文丽机器人资料的本地视频不上传。新视频通常使用用户提供的 B 站链接；未经要求不上传本地 MP4。
- 保留下载入口，明确缺资源；不要制造空下载链接和未完成的占位文件。
- 图题居中；正文段落按现有阅读样式首行两格缩进，不让标题、列表、公式、图题跟着缩进。
- 代码块保持现有接近 PyCharm 的可读配色、较大字号与复制功能。
- 长右侧目录应可独立滚动；锚点跳转后标题不能被固定顶栏挡住。
- 原始书稿只读保留；清理 OCR 可以修排版和明确识别错误，不能根据猜测重推数学结论。

## 7. 电子书录入与验收

现有 skill：`C:\Users\18066\.codex\skills\ebook-ingestion\SKILL.md`。新书录入或替换时先完整阅读，再按它的路由阅读必要 references。交接到其他电脑时此 skill 不一定随仓库存在，应额外交付该 skill 文件夹；缺失时明确告知，不要声称已经调用。

标准流程：源文件清点 → 检查正文与图片 → 整理章节与资源 → 注册分类及署名 → 独立完整构建 → 静态检查 → 浏览器验收 → 更新日志 → 明确范围的提交/推送与部署。

尤其检查：

- 合并分卷时避免同名图片覆盖，重写路径后逐项核对，不删除原图。
- 章节导航完整，目录、前言、附录与参考文献不被误当章节或遗漏。
- 代码块中的 LaTeX、裸露数学定界符、HTML 表格内公式需单独检查；构建通过不证明公式已经渲染。
- 保留源书的 GitHub、视频、课件链接；大文件不要绕过限制硬塞进仓库。
- 图片加载、下载文件、公式错误、图题、桌面与手机布局均需实测。必要时对照原稿，记录未确认的 OCR 问题，不宣称整本数学内容正确。

## 8. 机器人交互图专项

主要涉及 `craig-introduction-to-robotics` 与 `robot-technology-basics`。先读 `INTERACTIVE_FIGURES_CONTINUATION.md`、`INTERACTIVE_FIGURES_INVENTORY.md` 和 `INTERACTIVE_FIGURES_AGENT_PROMPT.md`，再核对当前源码。

- 原图保留，提供“原图 / 可交互”切换，不用交互图永久替掉原图。
- 公共底座为两书各自的 `docs/interactive/figure-kit.js`，修改后核对两份一致性。
- 图规格位于 `docs/interactive/specs/`；通过 `tools/build_interactive_figures.py` 生成 HTML，不能只改最终内联产物。
- 曾发生重绘图元挂在 SVG 根节点、没有随图层清空而累积的拖影。检查 grid/vector 等绘图调用是否传入正确父图层，确认多次重绘后 DOM 节点不持续增长。
- 生成后需重新构建站点；可用 `tools/check_svg_layer_leaks.py` 检测，并实测拖动、缩放、滑块、开关、标签切换、自动旋转和重置。
- 拖动方向应符合直觉；禁用浏览器原生图片拖动及误选文本，做好指针捕获和触摸处理。

## 9. 构建和本地验证

以下 PowerShell 命令均在项目根目录执行。

```powershell
Set-Location 'D:\Userdata\Desktop\公共知识\mkdocstutorial\ebook-reader'
..\.venv\Scripts\python.exe -X utf8 manage.py check
..\.venv\Scripts\python.exe -X utf8 manage.py preview
```

`manage.py check` 和 `preview` 都会构建，默认重建 `dist/`；`build.py` 会先删除指定输出目录，因此不能把输出设为仓库根目录、内容目录或其他现有资料目录。单书 `--book` 构建也不是完整发布包，不能拿去覆盖生产站。

工作区产物需保留时，使用全新、明确的独立输出目录，例如：

```powershell
..\.venv\Scripts\python.exe -X utf8 build.py --output tmp/dsh-acceptance-20261027
..\.venv\Scripts\python.exe -X utf8 -c "import verify; from pathlib import Path; verify.DIST=Path('tmp/dsh-acceptance-20261027').resolve(); raise SystemExit(verify.main())"
node --test tools/worker-auth.test.mjs
..\.venv\Scripts\python.exe -m http.server 8027 --bind 127.0.0.1 --directory tmp/dsh-acceptance-20261027
```

若该输出目录已存在，先判断是否可覆盖，或另取新名。独立目录构建后，检查器也要指向同一目录，不可误验旧 dist。

Python 依赖固定在 `requirements.txt`。新机器可建立上一级 `.venv` 后安装依赖；另需 Node.js/npm 用于认证测试和 Wrangler。浏览器验收可使用本机 Chrome 与项目已有工具，但不要假设 `tmp/` 内测试依赖在新机器存在。

## 10. 部署与发布记录

本次用户只要求交付文档，不执行本节操作。将来用户明确要求发布时：

1. 明确本次发布范围及已暂停内容；审查完整包是否夹带不应上线的课程。
2. 先更新 `CHANGELOG.md`，按日期倒序写“新增 / 优化 / 修复 / 安全 / 部署”。
3. 完整构建、内容检查、认证测试和桌面/手机验收通过。
4. 核对 Git 基线与差异，只提交明确文件，不使用 `git add .` 掩盖混杂工作区。
5. 使用已验证的完整输出目录部署，保留访问控制。

```powershell
$env:CI = 'true'
npx --yes wrangler@4.37.0 pages deploy tmp/dsh-acceptance-20261027 --project-name research-knowledge-hub --branch main
npx --yes wrangler@4.37.0 pages deployment list --project-name research-knowledge-hub
```

本机有缓存时可加 `--offline`，新机器不要假设已缓存。凭证通过 Wrangler 登录或平台安全配置获得，不抄写现有令牌；失效时请用户重新授权。`--commit-dirty=true` 只能如实标记已审查的混合工作区，不能替代审查或冒充干净提交。

确认 Production、main、部署编号和源提交/工作区状态；再检查正式域名的登录、正文与资源。未认证请求应仍被拦截，不能把登录页的 HTTP 200 当成正文更新成功。成功后日志记录实际部署编号、验证范围与结果；失败或未部署必须明确写出。

## 11. 安全与交付边界

- GitHub 仓库按用户要求在 2026-10-12 公开。网站登录保护不能保护已公开仓库里的正文、图片和历史；不要承诺“内容绝不泄露”。
- Worker 源码：`public/_worker.js`，构建副本为 `dist/_worker.js`。Supabase Auth 管独立账号，也保留共享密码兼容配置。
- 具体认证配置见 `AUTHENTICATION.md`；生产是否启用某个模式必须在平台核验，不能由说明文档推断。
- 不公开密码、令牌、Cookie、Service Role key，不把真实凭证写入文档、日志、前端或 Git。需要交接权限时由所有者在平台授权。
- 本次未联网扫描仓库历史或核查生产权限，不代表已完成安全审计。
- 交付源码需包含 `content/`、`public/`、构建与检查工具、配置、依赖声明、维护文档，以及本次范围内必要的未跟踪文件。单发 dist 只能交付静态产物，不能完整接管维护。
- 不要把 `.wrangler/`、登录缓存、环境密钥、`.venv/`、`__pycache__/`、全部 tmp 截图或本地大视频打进交付包。保留必需发布报告即可；打包前检查路径长度和敏感内容。

## 12. 可直接交给 dsh 的启动指令

> 请接管 `D:\Userdata\Desktop\公共知识\mkdocstutorial\ebook-reader`。先完整阅读 `AGENTS.md`、`DSH_HANDOVER.md`、`AUTHENTICATION.md`，再只读检查当前配置、Git 分支/worktree 和未提交差异。不要删除、重置或一键提交已有工作。本项目使用 build.py 自定义构建，mkdocs.yml 仅提供导航，不要运行 mkdocs build 替代正式流程。先向我汇报你核验到的项目状态、待办与风险，等待具体任务，不自动部署。《Jupyter Notebook 使用与应用》ZIP 保持暂停；《机械原理》已在本地录入，内容提供者熊忠帅，但不能声称已验收上线。后续新书使用 ebook-ingestion skill；所有发布先更新 CHANGELOG，完成全站检查、浏览器验收及认证测试，再按明确范围提交和部署。不得上传被排除的本地视频，不得泄露凭证。遇到文档与实际文件不一致，以实查为准并说明差异，不继承未经验证的成功结论。
