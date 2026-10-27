# 科研知识学习中心

> 把科研工具、编程、人工智能、机器人与工程资料整理成一条可持续扩展的学习路径。

一个长期运营的**静态**知识网站：课程与教材以 Markdown 维护，构建成纯 HTML / CSS / JavaScript / JSON，由 Cloudflare Worker 在返回任何文件之前做登录校验。没有数据库、没有运行时框架，克隆仓库即可离线重建整站。

| 项目 | 说明 |
| --- | --- |
| 线上站点 | <https://research-knowledge-hub.pages.dev>（未登录自动跳转登录页） |
| 仓库 | <https://github.com/Nitgomare/ebook-reader>（Public：源码与教材公开，站点受登录保护） |
| 当前规模 | 9 个知识领域 · 24 套内容 · 314 个阅读页面 · 216 个代码 / 数据文件 · 5,519 个静态资源 |
| 构建栈 | Python 3 + Markdown + pymdown-extensions（Pygments 高亮） |
| 前端 | 原生 JavaScript 单页应用 + MathJax 3，无打包器 |
| 托管 | Cloudflare Pages（Direct Upload） + `_worker.js` 访问控制 + Supabase Auth |

## 目录

- [站点速览](#站点速览)
- [内容版图](#内容版图)
- [站点功能](#站点功能)
- [架构总览](#架构总览)
- [内容模型](#内容模型)
- [构建流水线](#构建流水线)
- [前端运行时](#前端运行时)
- [认证与访问控制](#认证与访问控制)
- [本地开发](#本地开发)
- [内容维护](#内容维护)
- [发布与部署](#发布与部署)
- [质量约定](#质量约定)
- [目录结构](#目录结构)
- [常见问题](#常见问题)
- [相关文档](#相关文档)

## 站点速览

一句话概括数据流：

```text
content/books/<slug>/docs/*.md  ──build.py──▶  dist/data/docs/*.json  ──app.js──▶  浏览器
        （Markdown + 图片）        （渲染）        （预渲染 HTML + 目录）     （SPA）       │
                                                                                        │
dist/_worker.js  ── 每个请求先验 Cookie / Supabase JWT ─────────────────────────────────┘
```

三条设计取舍，决定了整个项目的形态：

1. **预渲染而不是前端渲染**：Markdown 在构建期转成 HTML 片段存进 JSON，浏览器只负责取JSON、插 DOM、排公式。首屏快，服务端零依赖。
2. **`dist/` 全量入库**：发布包和源文件躺在同一个仓库里，任何一次上线都能从某个提交精确复现，也不依赖 CI 产物缓存。
3. **导航与内容分离**：`mkdocs.yml` 只提供章节顺序，`books.json` 只提供站点层面的展示信息，正文里不写任何站点级配置。

## 内容版图

首页按 `books.json` 中 `site.categories` 的顺序分区，每个领域下的书目再按 `order` 排序。

| 知识领域 | 英文标识 | 内容 | 书目 |
| --- | --- | --- | --- |
| 管理科学与运筹优化 | `management-science` | 运筹建模、优化方法与管理决策 | 管理运筹学（第5版） |
| 科研工具与实践 | `research-skills` | 文献检索、Zotero、格式转换、知识库、实验复现 | 科研工具与实践（含 PPT 资源库） |
| Python 编程 | `python` | 语言基础到工程实践 | Python 入门 |
| Python 数据分析 | `data-analysis` | NumPy / Pandas / Matplotlib / Seaborn 与练习数据 | Python 数据分析实战 |
| 机器学习与人工智能 | `artificial-intelligence` | 经典机器学习到深度学习 | 动手学深度学习、机器学习 |
| 智能机器人 | `robotics` | 机械、硬件、嵌入式、控制、感知与导航 | 10 套：轮腿式智能安保巡逻机器人项目实战、机器人学导论（第3版）、机器人技术基础（第三版）、ROS 机器人编程、ROS 实战、机器人仿真与编程技术、机器视觉入门与实战、SolidWorks 智能机器人建模、ABB 实验台指导书、教育机器人教材 |
| 机械工程基础 | `mechanical-engineering` | 机构学与机械动力学 | 机械原理（第四版） |
| 风电技术 | `wind-energy` | 风资源、空气动力学、载荷、控制、整机与风电场 | 5 套：Wind Energy Handbook、风能技术（第二版）、风力发电机组理论与设计、大模型在故障预测与健康管理中的应用、风电 SCADA 数据分析与智能建模 |
| 工程系统与技术文档 | `engineering-systems` | 装备诊断与寿命预测的技术资料 | 智能分析与装备寿命预测系统使用手册 / 技术文档 |

## 站点功能

- **首页分区**：知识领域卡片、领域内书目卡片、站点统计（章节数、代码文件数由 `catalog.json` 动态给出，页面内不写死数字）。
- **左侧目录**：`课程 → 章节` 两级树，支持即时过滤；阅读页、代码页、首页各自有独立的搜索范围。
- **本文目录**：构建期收集 H2–H4 生成页内目录，桌面端常驻右栏，移动端抽屉展开。
- **阅读体验**：滚动阅读与逐页阅读两种模式；沉浸阅读支持点击左右翻页、滚轮、方向键、Esc 退出；字号（14–32）、字体（宋 / 黑 / 楷）、页边距、背景（米色 / 白色 / 护眼绿 / 夜间）写入 `localStorage` 持久化。
- **代码库**：`#/code` 集中浏览全部 `.py` / `.ipynb` / `.csv` / `.json`，支持语法高亮与 Notebook 单元格预览；超过 256 KB 只显示摘要并保留下载。
- **资源页**：每本书的 `#/resources/<slug>` 汇总教材正文、课件、视频、下载资料，表格化呈现。
- **PPT 资源库**：独立页面 `ppt-library.html`，真实封面 + 逐页 WebP 预览 + 原文件下载。
- **在线课件**：`slide-viewer.html?book=&deck=` 逐页翻阅教研课件。
- **更新日志**：`CHANGELOG.md` 在构建时渲染成站点内可读的 `changelog.html`，带日期导航。
- **公式**：Markdown 阶段由 `pymdownx.arithmatex` 输出 `<span/div class="arithmatex">`，浏览器端由 MathJax 3 排版。
- **交互图**：教材中的交互式图形以 iframe 内嵌，通过 `postMessage({type:'textbook:figure-height'})` 自适应高度。

## 架构总览

### 分层

| 层 | 位置 | 职责 |
| --- | --- | --- |
| 内容层 | `content/books/<slug>/` | Markdown 正文、图片、可选源码 / 课件目录 |
| 配置层 | `books.json`、各书 `mkdocs.yml` | 站点标题与领域、书目元信息、章节顺序 |
| 构建层 | `manage.py` → `build.py` → `verify.py` | 渲染正文、复制资源、生成目录、校验产物 |
| 产物层 | `dist/` | 可直接部署的全量静态站点 |
| 运行时层 | `public/app.js`、`reader-mode.js`、`styles.css` | 路由、目录、搜索、阅读模式、公式排版 |
| 认证层 | `public/_worker.js` | 登录、会话、Cookie、访问控制 |
| 发布层 | `tools/release.ps1` | 构建 → 测试 → 提交 → 推送 → 部署 → 核对 |

### 关键文件

| 文件 | 作用 |
| --- | --- |
| `manage.py` | 唯一入口：`build` / `check` / `preview`，先构建再校验，`preview` 额外起本地静态服务器 |
| `build.py` | 真正的构建器，约 860 行，负责渲染、资源改写、目录与代码预览生成 |
| `verify.py` | 产物校验器，约 120 行，构建后立即运行，任一错误即非零退出 |
| `books.json` | 站点标题、领域定义、24 套内容元信息 |
| `public/` | 前端源码，构建时整体复制到 `dist/`（`_worker.js` 随之上线） |
| `dist/` | 构建产物，整体入库，部署时原样上传 |
| `tools/` | 导入脚本、专项核验、Bilibili 同步、一键发布 |
| `resource-inventory/` | 每本书的来源、图片清单与导入报告 |
| `CHANGELOG.md` | 面向使用者的更新日志，同时是站点日志页的数据源 |

### 为什么不用 mkdocs / 静态框架

`mkdocs.yml` 在本项目里**只当章节顺序文件**，不执行 `mkdocs build`：站点需要阅读模式、代码联动、课件浏览、登录保护这些自有能力，直接渲染 Markdown 更可控。因此不要把 `mkdocs.yml` 当构建配置来改主题、插件或 `site_dir`。

## 内容模型

### 一本书的目录

```text
content/books/mechanism-principles-4e/
├─ mkdocs.yml                     # 章节顺序（必填）
└─ docs/                          # docs_dir
   ├─ 00-front-matter/index.md
   ├─ chapters/01/index.md … chapters/15/index.md
   ├─ appendices/01/index.md
   ├─ references/index.md
   └─ images/*.jpg                # 正文引用的图片
```

可选目录（存在即生效）：

```text
code/                              # 配套源码，按 chapter-XX/ 与章节自动关联
slides/manifest.json + <deck>/*.webp # 在线课件与 PPT 资源库
docs/interactive/*.html            # 内嵌交互图（构建时内联样式与脚本）
```

### `mkdocs.yml`

```yaml
site_name: 机械原理（第四版）
docs_dir: docs
nav:
  - 前置内容: 00-front-matter/index.md
  - 第1章 绪论: chapters/01/index.md
```

`nav` 支持两级列表折叠成分组；未列入 `nav` 的 `.md` 仍会被收录，归入「其他」分组。

### `books.json`

顶层只有三部分：`site`（标题、副标题、`categories`）、`books`（书目数组）、以及构建期派生的展示数据。

`categories` 顺序即首页分区顺序：

```json
{ "id": "mechanical-engineering", "title": "机械工程基础",
  "eyebrow": "MECHANICAL ENGINEERING",
  "description": "机构分析与设计、机械效率与自锁、机械平衡与运转速度波动的理论基础。" }
```

`books` 常用字段：

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `slug` | ✅ | 目录名 = 路由标识，唯一 |
| `title` / `author` | ✅ | 卡片与页头标题、作者 |
| `description` / `tags` | | 简介与标签 |
| `category` | ✅ | 必须匹配某个 `categories[].id` |
| `order` | | 领域内排序，缺省 1000 |
| `type` | | 展示类型（如 `reference`） |
| `coverSource` / `homePage` | | 封面来源、原书主页 |
| `docAuthors` / `contentProvider` | | 作者分工与内容提供者，显示在书目卡片 |
| `resourceLinks` / `localVideos` | | 外部资源入口、本地视频与文档的映射 |
| `slides` | | 由 `slides/manifest.json` 派生，一般手写不必要 |

### Markdown 约定

- **标题层级**：章内用 `##` / `###` / `####`，`build.py` 会把章节标题归一成「第X章」并在页内目录里按层级收集。
- **图与图注**：图片行与图注行之间**必须有空行**，或给图注段落加 `{: .figure-caption }`；构建器也会识别「图片段落紧跟以 `图 X-X` 开头的段落」并自动补样式。
- **公式**：行内 `$...$`，独立 `$$` 块。**定界符必须独占一行，且块内不能有空行**——空行会把公式切成普通段落，构建守卫会直接报错。
- **图片路径**：正文写相对路径（`images/xxx.jpg`），构建时统一改写到 `files/<slug>/…`，不要写绝对路径。
- **链接**：正文引用其他章节写相对 `.md` 路径，构建时转成 `#/doc/<id>`；外链原样保留。
- **表格**：Markdown 表格与原始 `<table>` 均受支持，构建时统一包一层 `.table-wrapper` 以支持横向滚动。

## 构建流水线

```powershell
..\.venv\Scripts\python.exe manage.py build     # 构建
..\.venv\Scripts\python.exe manage.py check     # 构建 + 校验（发布前必跑）
..\.venv\Scripts\python.exe manage.py preview   # 构建 + 校验 + 本地预览
..\.venv\Scripts\python.exe manage.py build --book mechanism-principles-4e   # 只构建一本书
```

`build.py` 的主流程：

1. 复制 `public/` 到 `dist/`（`_worker.js`、`app.js`、`styles.css`、`reader-mode.js`、`ppt-library.*`、`slide-viewer.*`、`changelog.html` 模板）。
2. 读取 `CHANGELOG.md`，渲染成 `dist/changelog.html`。
3. 逐本处理书目：读 `mkdocs.yml` → 收集文档 → 渲染 Markdown → 改写链接与图片 → 统一图表样式 → 收集页内目录 → 收集代码与下载资源 → 复制课件页图。
4. 汇总 `dist/data/catalog.json`（`site` / `stats` / `books` / `docs` / `code`）。
5. 生成 `404.html`（复用首页）与 `.nojekyll`。

产物结构：

```text
dist/
├─ index.html  app.js  reader-mode.js  styles.css  _worker.js
├─ changelog.html  ppt-library.html  slide-viewer.html
├─ data/
│  ├─ catalog.json          # 站点目录 + 统计
│  ├─ docs/<id>.json         # 正文 HTML、页内目录、上下篇、关联代码
│  └─ code/<id>.json         # 源码 / Notebook 预览与下载地址
├─ files/<slug>/…            # 图片、下载资料、内嵌交互图
├─ slides/<slug>/<deck>/…    # 课件逐页 WebP
└─ 404.html  .nojekyll
```

`verify.py` 在构建后检查：

- 文档 ID、代码 ID 唯一；每个 `data/docs/*.json`、`data/code/*.json` 都存在且标题一致。
- 正文里的 `#/doc/…` 链接与 `files/…` 资源确实存在。
- 章节关联的代码文件、课件页图、课程封面、首篇内容都存在。
- **正文段落里不得残留块公式定界符 `$$`**（排除代码示例），防止公式退化成源码上线。
- 产物中不得出现旧站定位「电子书阅读器」。
- 单文件不得 ≥ 100 MB（GitHub 限制）。

## 前端运行时

`public/app.js` 是一个约 900 行的原生单页应用，路由基于 hash：

| 路由 | 页面 |
| --- | --- |
| `#/` | 首页：知识领域分区与书目卡片，支持全局搜索 |
| `#/doc/<id>` | 阅读页：正文、页内目录、上下篇、本章代码 |
| `#/code` | 代码与数据总览 |
| `#/code/<id>` | 单个源码 / Notebook 预览 |
| `#/resources/<slug>` | 某本书的资源页（正文、课件、下载） |
| `#/book/<slug>` | 兼容旧链接，重定向到资源页 |

数据契约：

- `catalog.json`：`site`（标题、副标题、领域）、`stats`（books / docs / code）、`books`、`docs`（摘要数组）、`code`。
- `docs/<id>.json`：`id`、`bookSlug`、`relPath`、`title`、`sections`、`excerpt`、`chapterNumber`、`order`、`previousId`、`nextId`、`html`、`headings`（页内目录）、`codeFiles`。
- `code/<id>.json`：`id`、`bookSlug`、`path`、`name`、`kind`、`language`、`size`、`downloadUrl`、`content`、`truncated`。

`reader-mode.js` 负责阅读体验：滚动 / 逐页模式、沉浸阅读、翻页手势与键盘、字号字体边距背景（存 `localStorage`）、以及分页时的缩放重排。它用 `MutationObserver` 观察正文变化重排，并通过 `takeRecords()` 丢弃自己写入的内联样式，避免自激抖动。

## 认证与访问控制

`public/_worker.js`（构建后即 `dist/_worker.js`）在 Cloudflare Pages 上拦截**每一个**请求：

1. 未配置 Supabase 时回落到共享密码（HTTP Basic），可用 `ALLOW_LEGACY_BASIC=true` 与账号模式并存以便迁移。
2. 配置 `SUPABASE_URL` + `SUPABASE_PUBLISHABLE_KEY` 后启用账号模式：`/__auth/login` 登录、`/__auth/logout` 退出、`/__auth/status` 返回当前账号。
3. 会话只存 `HttpOnly + Secure + SameSite=Lax` 的 `__Host-rkh_access` / `__Host-rkh_refresh` Cookie（7 天），前端 JS 读不到令牌。
4. 访问令牌优先用 JWKS 本地验签，失败回落到 Supabase 鉴权服务器校验。
5. 可选 Cloudflare Turnstile 人机验证（`TURNSTILE_SITE_KEY` + `TURNSTILE_SECRET_KEY` 同时配置才启用）。
6. 所有受保护响应带 `Cache-Control: private, no-store` 与安全响应头，退出后旧页面不会从公共缓存恢复。

角色取自 JWT 的 `app_metadata.role`（`admin` / `teacher` / `student`，缺省 `student`），当前三个阶段均可读全部课程。完整配置步骤见 [AUTHENTICATION.md](AUTHENTICATION.md)。

## 本地开发

首次准备（工作区根目录）：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r .\ebook-reader\requirements.txt
```

依赖只有四个包：`Markdown`、`Pygments`、`PyYAML`、`pymdown-extensions`。

进入 `ebook-reader` 后：

```powershell
..\.venv\Scripts\python.exe manage.py preview     # 构建 + 校验 + http://127.0.0.1:8010
..\.venv\Scripts\python.exe manage.py preview --port 8099
```

也可以双击 `preview.cmd`。本地预览没有 Worker，因此**不做登录校验**，用于检查排版、导航与资源。

## 内容维护

新增一本书的完整流程：

1. 在 `content/books/<slug>/docs/` 放 Markdown 与图片，写 `mkdocs.yml` 定义 `nav`。
2. 需要在线源码时放 `code/`（按 `chapter-XX/` 与章节自动关联）；需要课件时放 `slides/` 并生成 `manifest.json`。
3. 在 `books.json` 的 `books` 里追加条目，`category` 选已存在的领域；新领域则在 `site.categories` 里加一项。
4. 在 `CHANGELOG.md` 当天条目下写清楚新增内容与验收数据。
5. `manage.py check` 全绿后按[发布流程](#发布与部署)上线。

已有教材来自扫描件、PDF、EPUB、PPT，`tools/` 下的 `import_*.py` 是各书的导入脚本（如 `import_mechanism_principles.py`、`import_management_operations_research.py`、`import_ppt_library.py`），把原始材料整理成符合上述约定的 Markdown；`sync_*.py` 用于同步 Bilibili 分 P 目录；`check_*.cjs`、`worker-auth.test.mjs` 是专项核验与认证测试。导入脚本通常不可重跑（目标目录存在即停止），保留它们是为了让整理规则可追溯。

## 发布与部署

本项目是 **Direct Upload**：GitHub 推送只更新仓库，**不会**自动更新线上；线上只在执行 `wrangler pages deploy dist` 后变化。

### 一键发布

```powershell
.\tools\release.ps1 -Message "本次更新说明"
.\tools\release.ps1 -DryRun            # 只打印将执行的步骤
.\tools\release.ps1 -Message "…" -NoDeploy   # 只提交推送，不上线
```

脚本按顺序执行：当天 CHANGELOG 检查 → 清理 `dist` 只读属性 → `manage.py check` → `node --test tools/worker-auth.test.mjs` → 按明确范围 `git add`（绝不用 `git add .`）→ 提交 → 推送 → 解析凭证 → `wrangler pages deploy dist` → 核对部署记录 → 检查未登录跳转。

| 参数 | 作用 |
| --- | --- |
| `-Message` | 提交信息；避免使用中文引号“”，PowerShell 会把它当字符串分隔符 |
| `-TokenFile` | 指定 Cloudflare API Token 文件 |
| `-AccountId` | 指定 Cloudflare 账户 ID |
| `-Yes` | 跳过交互确认 |
| `-DryRun` | 只展示步骤 |
| `-SkipBuild` | 复用现有 `dist` |
| `-NoPush` / `-NoDeploy` | 分步执行 |

### 凭证

- `CLOUDFLARE_API_TOKEN`：环境变量优先；否则脚本依次尝试 `-TokenFile`、`D:\Userdata\Desktop\.cloudflare_api_token`、`$HOME\Desktop\.cloudflare_api_token`。**令牌不写入仓库**。
- `CLOUDFLARE_ACCOUNT_ID`：环境变量或 `.wrangler/cache/wrangler-account.json`。若令牌没有 `User → Memberships` 权限，wrangler 无法自动推断账户，必须显式提供，否则报 `Authentication error [code: 10000]`。

### 手动部署

```powershell
..\.venv\Scripts\python.exe manage.py check
$env:CLOUDFLARE_API_TOKEN = (Get-Content -Raw D:\Userdata\Desktop\.cloudflare_api_token).Trim()
$env:CLOUDFLARE_ACCOUNT_ID = "<账户 ID>"
$env:CI = 'true'
npx --yes wrangler@4.37.0 pages deploy dist --project-name research-knowledge-hub --branch main --commit-dirty=true
```

`--account-id` **不是** `pages deploy` 的合法参数（会被忽略），必须用环境变量。`--commit-dirty=true` 是因为工作区可能留有未跟踪草稿。

### 回滚

Cloudflare 控制台 → Pages → `research-knowledge-hub` → Deployments，选择历史部署即可回滚；仓库侧用 `git revert` 生成新提交，不要 force push。

## 质量约定

- 每次提交、推送或部署前必须更新 `CHANGELOG.md`：按日期倒序，分类（新增 / 优化 / 修复 / 安全 / 部署），面向使用者描述，不写密码、令牌与隐私信息。
- 发布前必须跑完整 `manage.py check` 与认证测试。
- `dist/` 与源文件一起提交，保证线上可复现。
- 禁止 `git reset --hard`、`git clean -fd`、整库覆盖、force push；禁止用 `git add .` 掩盖混杂工作区。
- 工作区中的 `PRD.md`、`notebook-preview/`、`tmp/` 属草稿或历史发布包，不纳入提交范围。
- 构建会整体重写 `dist/`，因此发布前不要手工修改产物。

## 目录结构

```text
ebook-reader/
├─ manage.py                  # 统一入口：build / check / preview
├─ build.py                   # 构建器
├─ verify.py                  # 产物校验
├─ books.json                 # 站点与书目配置
├─ CHANGELOG.md               # 更新日志（同时渲染成站点日志页）
├─ AUTHENTICATION.md          # 登录与角色配置
├─ AGENTS.md                  # 维护约定（提交前必读）
├─ DSH_HANDOVER.md            # 交接说明与操作红线
├─ content/books/<slug>/      # 24 套内容：docs/ + 可选 code/、slides/
├─ public/                    # 前端源码与 _worker.js
├─ dist/                      # 构建产物（入库，部署对象）
├─ tools/                     # 导入、核验、同步、发布脚本
├─ resource-inventory/        # 各书来源与导入报告
└─ requirements.txt / preview.cmd
```

## 常见问题

**构建报 `PermissionError: [WinError 5]`（拒绝访问）**
`dist/` 里有只读文件导致无法整体删除。`release.ps1` 会自动清除只读属性；手动构建时先确认没有别的进程占用，再清属性后重跑。

**某个公式在页面上显示成源码**
多半是 `$$` 块内多了空行，或定界符没有独占一行。构建守卫会直接失败并指出「文章 X 的段落里残留块公式定界符」，按提示修那一处即可。

**图注变成了正文的一段**
图注需要独立成段：图片行、图注行之间留空行，或者给图注段落加 `{: .figure-caption }`。

**首页少了某个领域 / 书**
检查 `books.json`：`category` 必须与 `site.categories[].id` 完全一致；`order` 只影响同领域内顺序。

**推送后线上没变化**
正常现象。Direct Upload 不会因 push 触发构建，必须跑一次部署。

**单文件 ≥ 100 MB 导致校验失败**
拆分或压缩资源；GitHub 单文件上限与构建校验都会拦。

## 相关文档

| 文档 | 内容 |
| --- | --- |
| [AGENTS.md](AGENTS.md) | 维护与提交约定（部署前必读） |
| [AUTHENTICATION.md](AUTHENTICATION.md) | Supabase 账号、Turnstile、角色与迁移顺序 |
| [CHANGELOG.md](CHANGELOG.md) | 完整更新历史，按日期倒序 |
| [DSH_HANDOVER.md](DSH_HANDOVER.md) | 交接说明、操作红线与已知待办 |
| [PROJECT_HANDOFF.md](PROJECT_HANDOFF.md) | 项目背景、里程碑与发布记录 |
| [INTERACTIVE_FIGURES_INVENTORY.md](INTERACTIVE_FIGURES_INVENTORY.md) | 交互图清单与实现状态 |

---

内容来自公开教材、课程与自建讲义，仅用于学习与研究；引用书目保留原书作者与出版信息。站点由 Cloudflare Pages 提供托管，登录与账号由 Supabase Auth 管理。
