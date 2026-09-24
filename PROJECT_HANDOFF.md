# 科研知识学习中心：AI Agent 项目接管手册

> 更新日期：2026-09-24  
> 适用仓库：`Nitgomare/ebook-reader`  
> 默认分支：`main`  
> 生产平台：Cloudflare Pages  
> 本地项目目录：`D:\Userdata\Desktop\公共知识\mkdocstutorial\ebook-reader`

## 1. 接管目标

本文档用于让新的 AI Agent 在不重新摸索架构的情况下直接维护、构建、验证和发布本项目。接管者应先完整阅读本文件和根目录的 `AGENTS.md`，再修改任何文件。

项目是一个受访问控制保护的静态知识平台，集中展示课程、教材、Markdown 正文、图片、公式、代码、Notebook、数据文件、下载资源和外部视频链接。

当前线上入口：

- 生产站点：<https://research-knowledge-hub.pages.dev/>
- GitHub 私有仓库：<https://github.com/Nitgomare/ebook-reader>
- Cloudflare Pages 项目：`research-knowledge-hub`

不要在文档、代码、提交信息或聊天回复中写出登录密码、Supabase 密钥、Cloudflare 令牌或用户信息。

## 2. 最重要的事实

### 2.1 当前不是 MkDocs 直接建站

每本书保留一个 `mkdocs.yml`，但它只作为书名、`docs_dir` 和章节顺序的数据来源。真正构建网站的是根目录的 `build.py`。

技术链路如下：

```text
books.json + 各书 mkdocs.yml
              │
              ▼
content/books/<slug>/docs/*.md + images + interactive + code
              │
              ▼
build.py（Python Markdown、自定义目录/链接/资源处理）
              │
              ▼
dist/（原生 HTML + CSS + JavaScript + JSON + Worker）
              │
              ▼
Cloudflare Pages + dist/_worker.js 访问控制
```

不要运行 `mkdocs build` 作为正式构建方式。

### 2.2 源文件与产物必须同时维护

- 源内容：`content/books/`
- 前端源文件：`public/`
- 构建逻辑：`build.py`
- 构建产物：`dist/`

仓库会提交 `dist/`。修改源文件后必须重新构建，使 `dist/` 与源内容同步；不要只修改 `dist/`，否则下次构建会覆盖改动。

### 2.3 每次提交、推送或部署前必须更新日志

根目录 `AGENTS.md` 的硬性要求：

1. 先更新 `CHANGELOG.md`。
2. 再运行完整构建检查。
3. 然后才能提交、推送或部署。
4. 日志中不得出现任何敏感信息。

## 3. 当前项目状态

截至提交 `317240a`：

- 18 套课程/教材内容。
- 223 个章节文档。
- 216 个代码或数据文件。
- 首页按 7 个知识领域分类。
- GitHub 仓库保持私密，未启用 GitHub Pages。
- Cloudflare Pages 负责生产部署。
- Cloudflare Worker 在返回网页、图片、教材和源码前执行登录验证。
- 支持 Supabase 独立账号登录，并保留可配置的共享密码兼容方案。

当前分类由 `books.json` 的 `site.categories` 定义：

1. 科研工具与实践
2. Python 编程
3. Python 数据分析
4. 机器学习与人工智能
5. 智能机器人
6. 风电技术
7. 工程系统与技术文档

## 4. 目录结构

```text
ebook-reader/
├─ AGENTS.md                    强制维护规则
├─ PROJECT_HANDOFF.md           本接管手册
├─ INTERACTIVE_FIGURES_AGENT_PROMPT.md
├─ README.md                    面向普通维护者的项目说明
├─ AUTHENTICATION.md            Supabase/共享密码认证说明
├─ CHANGELOG.md                 每次推送、部署前必须更新
├─ books.json                   网站分类与课程元数据
├─ build.py                     正式构建器
├─ verify.py                    构建产物检查器
├─ manage.py                    build/check/preview 统一入口
├─ requirements.txt             Python 依赖
├─ public/                      前端源文件和 Worker 模板
│  ├─ index.html
│  ├─ app.js
│  ├─ styles.css
│  └─ _worker.js
├─ content/books/
│  └─ <book-slug>/
│     ├─ mkdocs.yml             章节导航顺序
│     ├─ docs/                  Markdown、图片、交互 HTML、下载资源
│     └─ code/                  源码、Notebook、数据（若存在）
└─ dist/                        构建后可直接部署的完整静态站点
   ├─ index.html
   ├─ app.js
   ├─ styles.css
   ├─ _worker.js
   ├─ data/catalog.json
   ├─ data/docs/*.json
   ├─ data/code/*.json
   └─ files/<book-slug>/...
```

## 5. 配置与内容模型

### 5.1 `books.json`

这是站点总配置和课程注册表。一本书至少需要：

```json
{
  "slug": "unique-book-slug",
  "title": "书名",
  "author": "作者",
  "description": "简介",
  "tags": ["标签1", "标签2"],
  "category": "robotics",
  "order": 30,
  "type": "reference"
}
```

`slug` 必须与 `content/books/<slug>/` 完全一致。分类 ID 必须存在于 `site.categories`。

### 5.2 每本书的 `mkdocs.yml`

仅用于读取：

- `site_name`
- `docs_dir`
- `nav`

正式导航顺序以 `nav` 为准。新增、删除或合并章节时必须同步修改它。

### 5.3 Markdown 正文

- 章节源文件通常位于 `docs/chapters/<NN>/index.md`。
- 图片通常位于 `docs/images/`。
- Markdown 中图片路径相对当前章节文件书写，例如 `../../images/example.jpg`。
- 公式使用 `$...$` 或 `$$...$$`，由 `pymdownx.arithmatex` 处理。
- 不要把 LaTeX 公式放进代码围栏。
- 图题使用 `<p class="figure-caption">图 X-X ……</p>`，全站样式负责居中。

### 5.4 课程入口逻辑

首页点击课程后首先进入“课程资源”页，而不是直接进入第一章。不要重新增加复杂课程导读、课程安排、单独文档首页或章节前置视频。

## 6. 前端运行方式

`public/app.js` 是原生 JavaScript 单页应用，使用 Hash 路由：

```text
#/                         首页
#/resources/<book-slug>    课程资源
#/doc/<document-id>        章节正文
#/doc/<id>?anchor=<id>     章节内定位
#/code/<code-id>           代码或数据预览
#/code                     代码库
```

关键前端功能：

- 首页分类和课程卡片。
- 左侧课程/章节目录。
- 右侧页内目录。
- Markdown 预渲染正文。
- MathJax 公式渲染。
- PyCharm 风格代码块和复制按钮。
- 图片与图题样式。
- 原图/可交互教学图切换。
- 课程资源、下载和外部视频入口。

主要样式位于 `public/styles.css`。修改后必须重新构建，不能只修改 `dist/styles.css`。

## 7. 交互图机制

### 7.1 当前实现

章节 Markdown 中使用以下结构：

```html
<div class="interactive-figure"
     data-interactive-src="../../interactive/figure-X-X.html"
     data-interactive-title="图X-X 标题">
  <div class="interactive-figure-toolbar" role="group" aria-label="图X-X显示方式">
    <button type="button" class="is-active"
            data-figure-mode="original" aria-pressed="true">原图</button>
    <button type="button"
            data-figure-mode="interactive" aria-pressed="false">可交互</button>
  </div>
  <div class="interactive-figure-pane" data-figure-pane="original">
    <img src="../../images/original.jpg" alt="原图说明">
  </div>
  <div class="interactive-figure-pane" data-figure-pane="interactive" hidden>
    <div class="interactive-figure-loading">正在载入交互模型…</div>
  </div>
</div>

<p class="figure-caption">图X-X 标题（原图与交互示例）</p>
```

`build.py` 会识别 `data-interactive-src`，把 HTML 复制到 `dist/files/<book-slug>/interactive/` 并重写链接。

`public/app.js` 中的 `enhanceInteractiveFigures()`：

- 默认显示原图。
- 用户点击“可交互”时才创建 iframe。
- iframe 使用 `sandbox="allow-scripts"`。
- 交互内容按需加载。

### 7.2 已完成的交互图

1. 《机器人学导论（第3版）》第 2 章图 2-1：位置矢量。
2. 《机器人学导论（第3版）》第 2 章图 2-19：等效轴角坐标系。
3. 《机器人技术基础（第三版）》第 3 章图 3.10：点绕任意轴旋转。

源文件位置：

```text
content/books/craig-introduction-to-robotics/docs/interactive/figure-2-1.html
content/books/craig-introduction-to-robotics/docs/interactive/figure-2-19.html
content/books/robot-technology-basics/docs/interactive/figure-3-10.html
```

### 7.3 交互图必须遵守的体验约束

- 原图永远保留且默认显示。
- 交互图必须准确表达教材语义，不能只追求视觉相似。
- 不得依赖网络 CDN；优先使用单文件 HTML + 内联 CSS/JS + SVG/Canvas。
- 若确实需要 Three.js，应把依赖放入仓库并使用相对路径，不能依赖公网模块。
- 支持鼠标拖动、触屏拖动和滚轮缩放时，要设置指针捕获。
- 水平拖动方向必须符合直觉。
- 禁止原生图片拖拽和文本误选：`user-select: none`、`touch-action: none`、阻止 `dragstart`。
- 控件必须在桌面端和移动端都可用。
- 复位、开关和滑块必须产生可见效果。
- 不得让交互图覆盖正文或导致页面横向滚动。

## 8. 本地环境与命令

Python 虚拟环境位于项目上一级：

```powershell
cd D:\Userdata\Desktop\公共知识\mkdocstutorial\ebook-reader
..\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

完整构建并检查：

```powershell
..\.venv\Scripts\python.exe manage.py check
```

本地预览：

```powershell
..\.venv\Scripts\python.exe manage.py preview
```

浏览器打开：

```text
http://127.0.0.1:8010
```

仅构建某本书可使用：

```powershell
..\.venv\Scripts\python.exe manage.py build --book craig-introduction-to-robotics
```

但发布前仍必须执行不带 `--book` 的完整 `manage.py check`。

## 9. 验证标准

任何内容变更至少完成以下检查：

1. `manage.py check` 返回退出码 0。
2. `dist/data/catalog.json` 中能找到新增/修改内容。
3. `dist/data/docs/<id>.json` 中图片、下载和交互路径均已重写为 `files/...`。
4. `dist/files/...` 中存在所有引用资源。
5. 首页课程入口、课程资源页、章节导航正常。
6. 右侧页内目录可滚动且定位不会被顶部栏遮挡。
7. 公式正常渲染，没有 LaTeX 源码裸露或被误识别成代码块。
8. 代码块有语言标签和复制按钮。
9. 桌面端和窄屏移动端均无溢出。
10. 交互图逐个检查按钮、滑块、拖动、触控、滚轮和重置逻辑。

可使用本机 Chrome 无界面截图做视觉检查：

```powershell
& 'C:\Program Files\Google\Chrome\Application\chrome.exe' `
  --headless --disable-gpu --no-sandbox `
  --window-size=1200,700 `
  --screenshot='C:\Users\18066\AppData\Local\Temp\page.png' `
  'http://127.0.0.1:8010/目标地址'
```

不要只以“构建成功”代替视觉检查。

## 10. Git 与工作区安全

当前远程仓库：

```text
origin https://github.com/Nitgomare/ebook-reader.git
```

安全规则：

- 工作区可能存在用户尚未提交的文件，不能擅自删除、覆盖或提交。
- 提交前使用 `git status --short` 和 `git diff --check`。
- 只暂存与当前任务相关的明确路径。
- 禁止使用 `git reset --hard`、`git clean -fd`、`git checkout -- .`。
- 使用简洁中文提交信息。
- 推送前更新 `CHANGELOG.md`。

已知需要保留、不要顺手提交或删除的工作区文件包括：

```text
PRD.md
第16页-网站技术架构.md
第17页-内容架构与知识组织.md
```

除非用户明确要求处理它们。

## 11. Cloudflare 部署

构建通过、提交并推送后，使用已验证的固定版本命令：

```powershell
npx --yes wrangler@4.37.0 pages deploy dist `
  --project-name research-knowledge-hub `
  --branch main
```

检查部署状态：

```powershell
npx --yes wrangler@4.37.0 pages deployment list `
  --project-name research-knowledge-hub
```

必须确认最新记录满足：

- `Environment` 为 `Production`
- `Branch` 为 `main`
- `Source` 等于刚提交的 Git commit

生产站启用了登录保护。未携带登录会话的命令行请求可能得到登录页，即使 HTTP 状态是 200；不能仅靠未认证的响应正文判断教材资源是否更新。

## 12. 认证系统

详细配置见 `AUTHENTICATION.md`。

要点：

- 认证入口在 `dist/_worker.js`，源模板在 `public/_worker.js`。
- Supabase 管理独立用户账号。
- JWT 保存在 `HttpOnly + Secure + SameSite=Lax` Cookie。
- 不允许前端 JavaScript读取访问令牌。
- 未完成 Supabase 配置时可回退到共享密码。
- 不得把 Supabase Secret/Service Role key 提交到仓库。
- 不得为了调试临时移除生产访问控制。

## 13. 已确定的产品与内容原则

后续维护必须延续以下用户决策：

- 首页使用分类课程卡片，分类必须保留。
- 删除一切无必要入口。
- 点击课程首先进入课程资源/课程介绍。
- 不要复杂课程导读、课程安排页、独立文档首页。
- 不在每章开头嵌入视频；视频集中放在课程资源或对应教程入口。
- 每本书的课程资源页只做简洁书籍、课程信息和资源列表。
- 代码块采用接近 PyCharm 的风格，字体清晰，并有右上角复制按钮。
- 所有图题居中。
- 右侧目录过长时必须可滚动。
- 首页分类锚点滚动需保留顶部间距，标题不得被顶部导航遮挡。
- 视频文件原则上不提交仓库，优先使用 Bilibili 外链。
- 教材原图不得因增加交互版本而删除。

## 14. 常见陷阱

1. **误把项目当 MkDocs 网站**：正式构建器是 `build.py`。
2. **只改 `dist/`**：下次构建会丢失修改。
3. **忘记更新 `mkdocs.yml`**：章节不会出现在导航中。
4. **修改图片路径**：替换正文时要保留现有图片相对路径。
5. **将公式写入代码围栏**：会显示为代码而不是 MathJax 公式。
6. **交互 HTML 使用公网 CDN**：登录环境或网络限制下可能空白。
7. **SVG 使用 `hidden` 属性控制 `<g>`**：不同浏览器表现不一致，使用 CSS `display:none` 类。
8. **拖拽未使用 pointer capture**：鼠标离开元素后会停止旋转。
9. **忘记移动端测试**：控制面板可能遮挡模型。
10. **命令行请求生产站返回 200 就认为资源正确**：可能实际返回的是登录页。

## 15. 标准任务交付流程

```text
读取 AGENTS.md 和本手册
        ↓
检查 git status，保护用户改动
        ↓
定位源文件与课程配置
        ↓
修改 content/public/build.py 等源文件
        ↓
运行完整 manage.py check
        ↓
本地桌面端与移动端视觉验证
        ↓
更新 CHANGELOG.md
        ↓
仅暂存本任务文件并提交
        ↓
推送 origin/main
        ↓
按用户授权部署 Cloudflare Pages
        ↓
核对 deployment list 的 commit
        ↓
向用户报告结果、位置、提交号和线上入口
```

## 16. 新 Agent 开始工作前的快速检查清单

- [ ] 已阅读 `AGENTS.md`
- [ ] 已阅读 `PROJECT_HANDOFF.md`
- [ ] 已运行 `git status --short`
- [ ] 已确认任务修改的是源文件而非仅修改 `dist/`
- [ ] 已确认没有覆盖用户未提交文件
- [ ] 已了解是否需要提交、推送和部署
- [ ] 已准备在提交前更新 `CHANGELOG.md`

