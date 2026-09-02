# 知识库搭建

这套教程带你完整复刻一个与本站结构相同的科研知识库：用 Markdown 写内容，用 MkDocs Material 生成静态网页，把代码上传到 GitHub，最后交给 Cloudflare Pages 自动构建和发布。

不要求你会前端开发。完成后，你将拥有一个可以搜索、切换深浅色、按课程折叠导航、在线阅读大型书籍，并且每次推送代码都会自动更新的网站。

## 最终工作流

```text
Markdown 内容 + 图片 + mkdocs.yml
                │
                ▼
          MkDocs 本地构建
                │
                ▼
          GitHub 保存源文件
                │  push
                ▼
   Cloudflare Pages 自动构建并发布
```

## 先理解三个目录

| 目录 | 放什么 | 是否手工修改 |
| --- | --- | --- |
| `docs/` | 主站 Markdown、图片、CSS、JavaScript 等源内容 | 是 |
| `books/` | 每本大型图书的独立 MkDocs 源项目 | 需要增加或更新图书时修改 |
| `site/` | 主站与独立图书统一构建出的 HTML 成品 | 否 |

!!! warning "不要把 `site/` 当源文件编辑"
    下一次运行 `mkdocs build` 时，`site/` 会重新生成，直接改里面的 HTML 会丢失。页面文字应改 `docs/` 里的 Markdown，样式应改 `docs/assets/stylesheets/` 里的 CSS。

## 两条路线

=== "第一次学习"

    先做一个只有首页和两篇文章的最小网站，完成本地预览和部署后，再加入书库。这样最容易定位问题。

=== "直接复刻本站"

    下载本站共享的 `mkdocs.yml`，复制目录结构，再逐项替换站名、导航和页面内容。

## 你需要准备的内容

- 网站名称和一句简介；
- 计划设置的一级栏目；
- 每个栏目下的 Markdown 页面；
- 合法且有权公开的图片、论文或书籍内容；
- GitHub 和 Cloudflare 账号。

!!! danger "公开前检查版权和隐私"
    Cloudflare Pages 的生产站点默认可被任何人访问。不要上传未获授权的书籍、个人信息、账号密码、API 密钥或内部资料。大型资料的“技术上能发布”不等于“法律上可以公开”。

---

## 1. 准备环境与工具

### 需要安装什么

| 工具 | 用途 | 检查命令 |
| --- | --- | --- |
| Python 3.11 或更高版本 | 运行 MkDocs 和图书拆分脚本 | `python --version` |
| Git | 保存版本并上传 GitHub | `git --version` |
| VS Code（推荐） | 编辑 Markdown、YML 和 CSS | 无 |
| GitHub Desktop（可选） | 不熟悉命令行时提交和推送 | 无 |

Windows 安装 Python 时勾选 **Add Python to PATH**。安装后重新打开 PowerShell，再运行检查命令。

### 创建项目和虚拟环境

以下命令里的 `research-site` 是项目文件夹名，可以替换：

```powershell
mkdir research-site
cd research-site
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

成功激活后，命令行开头通常会出现 `(.venv)`。

!!! question "PowerShell 不允许执行 Activate.ps1"
    可以直接跳过激活，在后续命令中使用 `.\.venv\Scripts\python.exe`；也可以只对当前窗口运行：

    ```powershell
    Set-ExecutionPolicy -Scope Process Bypass
    .\.venv\Scripts\Activate.ps1
    ```

### 安装 MkDocs Material

```powershell
python -m pip install --upgrade pip
python -m pip install mkdocs-material==9.7.6
```

确认安装成功：

```powershell
python -m mkdocs --version
```

在项目根目录创建 `requirements.txt`：

```text
mkdocs-material==9.7.6
```

这个文件既能让别人复现相同环境，也会用于 Cloudflare Pages 安装依赖。

### 最小化试运行

```powershell
python -m mkdocs new .
python -m mkdocs serve
```

浏览器访问 `http://127.0.0.1:8000/`。终端保持运行时，保存 Markdown 后浏览器会自动刷新。按 ++ctrl+c++ 停止预览。

!!! tip "本站项目已经存在时"
    不要再运行 `mkdocs new .`，直接进入包含 `mkdocs.yml` 的目录，安装依赖后运行 `python -m mkdocs serve`。

### 建议的编辑器设置

- 文件统一使用 UTF-8 编码；
- 缩进使用空格，不使用 Tab；
- YML 建议每层缩进 2 个空格；
- 打开“保存时删除行尾空格”；
- 安装 Markdown 和 YAML 语法检查扩展。

---

## 2. 建立目录并使用共享 YML

### 推荐目录

本站精简后的目录如下。文件夹和文件名建议使用小写英文、数字和连字符，页面显示的中文标题写在 `mkdocs.yml` 中。

```text
research-site/
├─ mkdocs.yml
├─ requirements.txt
├─ .gitignore
├─ build_all.py
├─ split_book_to_mkdocs_stable_version.py
├─ docs/
│  ├─ index.md
│  ├─ 01-literature/
│  ├─ 02-format-trans/
│  ├─ 03-site-building/
│  ├─ assets/
│  │  ├─ stylesheets/
│  │  │  ├─ navigation.css
│  │  │  └─ homepage.css
│  │  └─ javascripts/
│  │     └─ mathjax.js
│  └─ library/
│     └─ index.md
├─ books/
│  ├─ wind-energy/
│  └─ 风能技术/            # 每本书都是一个独立 MkDocs 源项目
└─ site/                 # 自动生成，不提交
   └─ book-sites/        # build_all.py 自动生成
```

几个容易混淆的规则：

- `mkdocs.yml` 必须位于项目根目录；
- 首页必须是 `docs/index.md`；
- `nav` 中的路径以 `docs/` 为起点，所以写 `01-literature/search.md`，不要写 `docs/01-literature/search.md`；
- CSS、图片和 JavaScript 也要放在 `docs/` 里面，MkDocs 才会复制；
- `books/` 保存可维护的图书源文件，图书 HTML 不放回 `docs/`；
- `site/` 是构建结果，应写进 `.gitignore`。

### 共享 YML

<div class="config-download" markdown>

**不需要从头手写。** 下载后把文件放到项目根目录并命名为 `mkdocs.yml`：

[下载可直接修改的 mkdocs.yml](downloads/mkdocs.yml){ .md-button .md-button--primary download="mkdocs.yml" }

</div>

这份配置已经包含本站使用的 Material 主题、中文搜索、深浅色切换、代码复制、提示框、公式、首页卡片和可折叠一级导航。

拿到文件后通常只需要改四处：

1. `site_name`：浏览器标题和左上角站名；
2. `site_description` 与 `site_author`；
3. `theme.palette`：主色和强调色；
4. `nav`：页面名称、层级和 Markdown 路径。

### YML 最重要的缩进规则

YAML 通过缩进表达层级。只用空格，并保持同一级缩进一致：

```yaml
nav:
  - "课程首页": index.md

  - "1. 一级下拉栏目":
      - "1.1 第一页": 01-course/01-first.md
      - "1.2 第二页": 01-course/02-second.md
```

第一层 `-` 是一级菜单，里面再缩进的 `-` 是下拉项。一级栏目下面有子项时，Material 会在左侧显示展开箭头。

错误示例：

```yaml
nav:
 - "一级栏目":
   - "第一页": docs/01-course/01-first.md  # 缩进混乱，而且多写了 docs/
```

### `.gitignore`

在项目根目录创建：

```gitignore
site/
.venv/
__pycache__/
*.pyc
.DS_Store
```

不要忽略 `docs/`、`books/`、`mkdocs.yml`、`build_all.py`、`requirements.txt`。它们正是 Cloudflare 构建网站所需的源文件。

### 用检查命令发现路径错误

```powershell
python -m mkdocs build --strict
```

`--strict` 会把警告当成错误，特别适合发现 `nav` 指向不存在文件、Markdown 链接失效等问题。第一次整理旧项目时可以先不加 `--strict`，逐步修完警告后再启用。

---

## 3. 编写页面与设置导航

### 新建一篇页面

例如创建 `docs/01-literature/01-search-tools.md`：

```markdown
# 文献检索工具

这节课介绍如何选择数据库并设计检索式。

## 学习目标

- 认识常用数据库；
- 能写出关键词组合；
- 能导出检索结果。

## 操作步骤

1. 明确研究问题；
2. 提取中英文关键词；
3. 组合检索式；
4. 保存检索记录。
```

建议一页只有一个一级标题 `#`，正文从二级标题 `##` 开始。本站右侧页内目录显示二至四级标题。

### 把页面加入导航

只把文件放进 `docs/` 还不够；要在侧栏显示它，需要修改根目录 `mkdocs.yml`：

```yaml
nav:
  - "课程首页": index.md

  - "1. 文献检索与管理":
      - "1.1 文献检索工具": 01-literature/01-search-tools.md
      - "1.2 文献筛选方法": 01-literature/02-literature-screening.md

  - "3. 网站制作与部署":
      - "教程总览": 03-site-building/index.md
      - "3.1 准备环境": 03-site-building/01-environment.md
```

`1. 文献检索与管理` 和 `2. 网站制作与部署` 是一级下拉栏目。不要启用 `navigation.expand`，否则所有栏目默认同时展开。

### Markdown 常用写法

#### 链接

同一网站优先使用相对路径：

```markdown
[下一节](02-literature-screening.md)
[返回首页](../index.md)
[打开外部网站](https://example.com)
```

路径和文件名大小写要完全一致。Windows 本地不敏感，但 Cloudflare 的 Linux 构建和线上 URL 会区分大小写。

#### 图片

推荐把页面图片放在同级 `images/`：

```text
docs/01-literature/
├─ 01-search-tools.md
└─ images/
   └─ database-search.png
```

Markdown：

```markdown
![数据库检索界面](images/database-search.png)
```

图片文件名不要使用空格。照片优先用 WebP/JPEG，界面截图和线图优先用 WebP/PNG；上传前压缩，避免页面加载过慢。

#### 提示框

```markdown
!!! tip "操作提示"
    提示框正文缩进 4 个空格。

!!! warning "注意"
    修改 YML 后要重新启动本地预览。

??? example "点击展开示例"
    这里可以放较长的补充内容。
```

#### 代码、表格和公式

````markdown
```powershell
python -m mkdocs serve
```

| 项目 | 值 |
| --- | --- |
| 构建目录 | `site` |

行内公式：\(E=mc^2\)

独立公式：

\[
P = \frac{1}{2}\rho A v^3
\]
````

### 首页卡片

Material 的卡片语法适合把课程入口集中到首页：

```markdown
<div class="grid cards" markdown>

-   :material-web:{ .lg .middle } **网站制作教程**

    ---

    从目录配置到自动部署，逐步搭建知识库。

    [开始学习](03-site-building/index.md)

</div>
```

保存后在本地逐个点击导航、卡片、图片和上一页/下一页，确认没有 404。

---

## 4. 调整主题与自定义样式

先用 `mkdocs.yml` 提供的主题选项完成大部分外观设置，只有主题选项无法实现的效果才写 CSS。这样升级 Material 时更稳定。

### 修改主色和强调色

```yaml
theme:
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: blue
      accent: green
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: blue
      accent: green
```

- `primary` 控制顶部栏、主要按钮和部分标题；
- `accent` 控制悬停、高亮等强调状态；
- 两个 `palette` 分别是浅色和深色；
- 常用颜色名有 `indigo`、`blue`、`teal`、`green`、`orange`、`red`、`purple`。

### 修改左上角图标

```yaml
theme:
  icon:
    logo: material/school
```

可以替换为 `material/book-open-page-variant`、`material/flask`、`material/wind-turbine` 等 Material 图标。

### 引入自己的 CSS

创建 `docs/assets/stylesheets/navigation.css`：

```css
/* 一级下拉标题 */
.md-sidebar--primary
.md-nav--primary
> .md-nav__list
> .md-nav__item--nested
> .md-nav__link {
  margin-top: 0.35rem;
  padding-top: 0.45rem;
  padding-bottom: 0.45rem;
  font-size: 0.78rem;
  font-weight: 700;
  color: var(--md-primary-fg-color);
  border-bottom: 1px solid var(--md-default-fg-color--lightest);
}

/* 下拉内容轻微缩进 */
.md-sidebar--primary
.md-nav--primary
> .md-nav__list
> .md-nav__item--nested
> .md-nav
> .md-nav__list {
  padding-left: 0.35rem;
}
```

再在 `mkdocs.yml` 引入：

```yaml
extra_css:
  - assets/stylesheets/navigation.css
  - assets/stylesheets/homepage.css
```

路径仍然以 `docs/` 为起点。

### 制作首页重点入口

`docs/assets/stylesheets/homepage.css`：

```css
.library-hero {
  margin: 1.5rem 0 2.5rem;
  padding: 1.8rem 2rem 2rem;
  border: 1px solid var(--md-primary-fg-color--light);
  border-radius: 0.35rem;
  background: linear-gradient(
    120deg,
    var(--md-primary-fg-color--transparent),
    var(--md-primary-fg-color--lightest)
  );
}

.library-hero h2 {
  margin-top: 0;
  color: var(--md-primary-fg-color);
}
```

首页 Markdown：

```markdown
<div class="library-hero" markdown>

## :material-library-shelves: Library

**从这里浏览专业资料。**

[进入 Library](library/){ .md-button .md-button--primary }

</div>
```

`md_in_html` 让 `<div>` 内部继续解析 Markdown，`attr_list` 让按钮的 `{ .md-button }` 生效；共享 YML 已启用两者。

### 样式调试顺序

1. 保持 `python -m mkdocs serve` 运行；
2. 只改一个 CSS 属性并保存；
3. 浏览器按 ++ctrl+f5++ 强制刷新；
4. 同时检查浅色、深色、桌面和手机宽度；
5. 使用浏览器开发者工具确认选择器命中了目标元素。

!!! warning "避免直接复制主题内部 CSS"
    Material 更新后，内部类名和结构可能变化。自定义选择器尽量短，颜色尽量使用 `--md-*` 变量，以便自动适配深浅色。

### 常见问题

| 现象 | 检查 |
| --- | --- |
| CSS 完全不生效 | 文件是否位于 `docs/`；`extra_css` 路径是否正确；是否重新构建 |
| 本地生效、线上不生效 | 文件名大小写；是否已经提交并推送；Cloudflare 是否部署了最新提交 |
| 深色模式看不清 | 是否写死白色/黑色；改用 Material CSS 变量 |
| 手机侧栏错位 | 选择器是否只限定 `.md-sidebar--primary`；是否设置了固定宽度 |

---

## 5. 拆分书本等大型文件

把几十万字放在一个 Markdown 页面里会导致加载、搜索和编辑都很慢。本站采用“主知识库 + 独立图书站”：每本书按章拆分成自己的 MkDocs 项目，统一构建时再把静态网页放入 `site/book-sites/`。仓库只保存 `books/` 中的图书源文件，不保存重复的图书 HTML。

### 为什么按章拆分

- 浏览器一次只加载当前章；
- 左侧显示章目录，右侧显示本章小节；
- 每章图片独立存放，链接更容易维护；
- 修改一章时不必打开超长文件；
- 搜索索引和构建错误更容易定位。

### 1. 整理源文件

建议先准备：

```text
book-source/
├─ book.md
└─ images/
   ├─ figure-001.webp
   ├─ figure-002.webp
   └─ ...
```

源 Markdown 的主章节使用二级标题：

```markdown
# 书名

封面、作者和前言等前置内容。

## 第1章 绪论

### 1.1 研究背景

### 1.2 基本概念

## 第2章 方法

### 2.1 方法一

## 参考文献
```

本站拆分脚本能识别 `## 第1章 标题`、`## 1. 标题`、`## 1 标题`、`## Chapter 1 Title`，也会处理无编号的前置/后置内容。拆分前应先统一标题层级；如果正文用加粗文本模拟标题，脚本无法可靠判断章节。

图片使用相对路径：

```markdown
![风机结构](images/figure-001.webp)
```

### 2. 使用本站拆分脚本

脚本位于仓库根目录：

[`split_book_to_mkdocs_stable_version.py`](https://github.com/Nitgomare/sskb/blob/main/split_book_to_mkdocs_stable_version.py)

最简单的方法是交互运行：

```powershell
python split_book_to_mkdocs_stable_version.py
```

按提示依次填写源 Markdown、图片文件夹、目标图书项目、书名等路径。

也可以一次写完整命令：

```powershell
python split_book_to_mkdocs_stable_version.py `
  --markdown "D:/books/source/book.md" `
  --images-dir "D:/books/source/images" `
  --project-dir "books/demo-book" `
  --site-name "示例图书" `
  --site-dir "../../site/book-sites/demo-book" `
  --homepage "/" `
  --icon "material/book-open-page-variant" `
  --clean
```

参数说明：

| 参数 | 含义 |
| --- | --- |
| `--markdown` | 未拆分的源 Markdown |
| `--images-dir` | 原始图片文件夹；没有图片可省略 |
| `--project-dir` | 独立图书项目，推荐 `books/英文短名` |
| `--site-name` | 图书网页显示名称 |
| `--site-dir` | 单独构建该书时的输出位置，推荐主站 `site/book-sites/英文短名` |
| `--homepage` | 点击图书 Logo 返回的主站地址 |
| `--icon` | 图书站左上角 Material 图标 |
| `--clean` | 先清空目标项目的 `docs/`；确认目标路径无误后再用 |

!!! danger "`--clean` 会清空目标图书项目的 docs"
    它不会删除源 Markdown 和源图片，但会重建 `--project-dir` 下的 `docs/`。第一次先用测试目录；后续若在拆分结果中手工改过内容，请先备份。

### 3. 检查拆分结果

输出大致如下：

```text
books/demo-book/
├─ mkdocs.yml
└─ docs/
   ├─ index.md
   ├─ split-report.txt
   ├─ 00-front-matter/
   │  └─ index.md
   ├─ chapters/
   │  ├─ 01-introduction/
   │  │  ├─ index.md
   │  │  └─ images/
   │  └─ 02-method/
   │     ├─ index.md
   │     └─ images/
   └─ 99-back-matter/
      └─ index.md
```

重点打开 `split-report.txt`，检查：

- 识别了多少章；
- 每章标题是否正确；
- 是否有找不到的图片；
- 参考文献是否进入后置内容；
- 生成目录名是否过长或重复。

### 4. 用统一脚本构建主站和全部图书

本站根目录的 `build_all.py` 会先清理并构建主站，再扫描 `books/*/mkdocs.yml`，把每本书构建到对应的 `site/book-sites/<书名>/`：

```powershell
python build_all.py
```

构建结果：

```text
site/
├─ index.html
├─ assets/
├─ library/
└─ book-sites/
   └─ demo-book/
      ├─ index.html
      ├─ assets/
      └─ chapters/
```

最终访问路径是：

```text
/book-sites/demo-book/
```

在 `docs/library/index.md` 加入口：

```markdown
-   :material-book-open-page-variant:{ .lg .middle } **示例图书**

    ---

    一句话介绍这本书。

    [进入独立图书站](../book-sites/demo-book/){ .md-button .md-button--primary target=_top }
```

!!! tip "为什么不把生成的 HTML 放进 docs"
    `books/` 已经包含 Markdown 和图片源文件，再提交一份 `docs/book-sites/` 会使仓库重复膨胀。统一构建脚本让本地和 Cloudflare 都从同一份源文件生成结果，更容易维护。

### 5. 大文件限制与优化

这里必须同时考虑 GitHub 和 Cloudflare Pages：

- GitHub 网页上传单文件最多 25 MiB，普通 Git 推送会警告超过 50 MiB，并阻止超过 100 MiB 的单个 Git 对象；
- Cloudflare Pages 单个站点资源最大 25 MiB；
- Cloudflare Pages Free 方案每个站点最多 20,000 个文件；
- GitHub 建议仓库尽量小，并避免提交 `site/`、图书 HTML 等可重复生成的文件。

因此，网站中的每一张图片、PDF 或下载文件都应小于 25 MiB。超大原始 PDF 不要直接放进 Pages；可以只发布按章转换后的 Markdown 和压缩图片，原文件放在有权限控制的对象存储中。

图片优化建议：

1. 批量缩放到实际需要的分辨率；
2. 照片转 WebP/JPEG，示意图转 WebP/PNG；
3. 删除重复图片；
4. 避免同时提交原图和压缩图；
5. 构建后统计文件数和最大单文件。

PowerShell 检查：

```powershell
$files = Get-ChildItem site -Recurse -File
$files.Count
$files |
  Sort-Object Length -Descending |
  Select-Object -First 20 FullName, Length
```

!!! note "Git LFS 不是 Pages 大资源的万能解法"
    Git LFS 能解决 GitHub 的大文件存储方式，但 Cloudflare Pages 最终部署的单个静态资源仍受 25 MiB 限制。对于要直接提供下载的大文件，更适合使用 Cloudflare R2 等对象存储，再从页面链接过去。

官方限制说明：[GitHub 大文件](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)、[Cloudflare Pages 限制](https://developers.cloudflare.com/pages/platform/limits/)。

---

## 6. 上传到 GitHub

GitHub 保存的是网站源文件。Cloudflare Pages 连接仓库后，每次收到新的提交都会自动构建并部署。

### 1. 上传前本地检查

在项目根目录运行：

```powershell
python build_all.py
python -m mkdocs serve
```

`build_all.py` 检查主站和全部独立图书能否构建；`mkdocs serve` 用于边编辑边预览主站页面。确认 `.gitignore` 已排除：

```gitignore
site/
.venv/
__pycache__/
*.pyc
```

!!! danger "绝不要提交密钥"
    提交前搜索 `.env`、令牌、密码、Cookie、私人邮箱和内部数据。仅仅删除工作区中的文件并不能清除 Git 历史；若密钥已提交，应立刻撤销密钥并清理历史。

### 2. 在 GitHub 创建空仓库

1. 登录 GitHub，点击右上角 **New repository**；
2. 填写仓库名，例如 `research-knowledge-base`；
3. 公开站可选 Public，内部协作可选 Private；Cloudflare Pages 支持连接公开和私有仓库；
4. 如果本地已有项目，不要勾选自动创建 README、`.gitignore` 或 License；
5. 点击 **Create repository**。

### 3. 第一次上传

把下面地址替换为自己的仓库：

```powershell
git init
git branch -M main
git add .
git status
git commit -m "创建科研知识库"
git remote add origin https://github.com/你的用户名/你的仓库名.git
git push -u origin main
```

`git status` 是提交前最重要的一步。确认没有 `.venv/`、`site/`、超大原始 PDF 和私密文件，再执行 `git commit`。

如果 GitHub 要求登录，推荐使用浏览器授权、Git Credential Manager 或 GitHub Desktop，不要把个人访问令牌写入文件。

### 4. 日常更新

```powershell
git status
git add docs books mkdocs.yml build_all.py requirements.txt
git commit -m "新增网站制作教程"
git push
```

比起总用 `git add .`，明确列出要提交的路径更容易避免误传。

### 5. 用分支预览后再上线

重要改版建议使用分支：

```powershell
git switch -c update/site-tutorial
git add docs mkdocs.yml
git commit -m "新增建站教程"
git push -u origin update/site-tutorial
```

在 GitHub 创建 Pull Request 后，Cloudflare Pages 会为它生成独立预览地址。检查无误再合并到 `main`，生产网站才会更新。

### 6. 常见推送错误

| 错误 | 处理 |
| --- | --- |
| `remote origin already exists` | 先运行 `git remote -v`；需要改地址时用 `git remote set-url origin 新地址` |
| `rejected ... fetch first` | 远端已有提交，先 `git pull --rebase origin main`，解决冲突后再推送 |
| 文件超过 100 MiB | 不要反复 push；先从即将提交的内容和历史中正确移除，再压缩、拆分或使用对象存储 |
| 大小写改名线上不生效 | 用 `git mv old.md temp.md` 后再 `git mv temp.md New.md` |
| Cloudflare 没有触发 | 确认推送到了它设置的生产分支，并检查 Pages 的 Git 集成权限 |

GitHub 官方说明：[从命令行添加本地代码](https://docs.github.com/en/repositories/creating-and-managing-repositories/adding-locally-hosted-code-to-github)、[大文件限制](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)。

---

## 7. 用 Cloudflare Pages 部署

Cloudflare Pages 会克隆 GitHub 仓库、安装 `requirements.txt` 中的 Python 包、运行 MkDocs，再把 `site/` 发布到全球网络。以后每次推送到生产分支都会自动重复这套流程。

### 1. 连接 GitHub 仓库

1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com/)；
2. 进入 **Workers & Pages**；
3. 选择 **Create application** → **Pages** → **Connect to Git**（界面文字可能随版本调整）；
4. 选择 GitHub 并安装/授权 **Cloudflare Workers and Pages**；
5. 只授权目标仓库更安全；仓库不出现时，回 GitHub 的应用安装设置补充访问权限；
6. 选中知识库仓库，进入构建设置。

Cloudflare Pages 支持公开和私有 GitHub 仓库。

### 2. 填写构建参数

本站这种根目录就是 MkDocs 项目的仓库，推荐填写：

| 设置 | 值 |
| --- | --- |
| Project name | 自定义，例如 `research-kb` |
| Production branch | `main` |
| Framework preset | `None` / 不使用预设 |
| Build command | `pip install -r requirements.txt && python build_all.py` |
| Build output directory | `site` |
| Root directory | 留空 |

如果 MkDocs 项目位于仓库子目录，例如 `website/`，则把 **Root directory** 填为 `website`。构建命令和输出目录都从这个根目录开始计算。

!!! tip "为什么不能把输出目录写成 docs"
    `docs/` 是源内容，`site/` 才是 `mkdocs build` 生成的 HTML。输出目录填错通常会得到没有样式的文件列表或首页 404。

### 3. Python 版本

Cloudflare Pages 的新构建镜像自带 Python。一般无需设置版本；若希望环境完全可复现，可以在项目设置的环境变量中添加：

```text
PYTHON_VERSION = 3.12
```

也可以在仓库根目录使用 `.python-version`。`requirements.txt` 中固定 MkDocs Material 版本，可以避免主题自动升级导致构建结果突然改变。

### 4. 首次部署

点击 **Save and Deploy** 后依次观察日志：

1. 克隆仓库；
2. 安装 `requirements.txt`；
3. 执行 `python build_all.py`，生成主站和全部独立图书；
4. 上传 `site/`；
5. 显示 Success 和 `项目名.pages.dev` 地址。

先打开 `pages.dev` 地址，逐项检查：

- 首页样式；
- 左侧一级下拉菜单；
- 搜索；
- 深浅色切换；
- 中文路径和图片；
- Library 中的独立图书站；
- 手机端菜单。

### 5. 自动更新与预览

- 推送到 `main`：更新生产站；
- 推送到其他分支：默认生成预览部署；
- 创建 Pull Request：GitHub 页面可显示 Pages 检查和预览链接；
- 每次部署都对应一个提交，可在 Pages 的部署列表查看日志和历史版本。

预览地址默认公开，但 Cloudflare 会给预览部署添加 `X-Robots-Tag: noindex`。敏感项目仍应配置 Cloudflare Access，不能只依赖“不被搜索引擎收录”。

### 6. 绑定自定义域名（可选）

在 Pages 项目中进入 **Custom domains** → **Set up a domain**。

=== "根域名"

    例如 `example.com`。该域名需要作为 Cloudflare Zone，并把域名服务器指向 Cloudflare。

=== "子域名"

    例如 `kb.example.com`。如果 DNS 不托管在 Cloudflare，可在原 DNS 服务商添加 CNAME：

    ```text
    类型：CNAME
    名称：kb
    目标：你的项目.pages.dev
    ```

必须先在 Pages 项目中添加自定义域名，再配置 CNAME；只手工添加 DNS 而没有在 Pages 关联域名，可能出现解析错误。

HTTPS 证书通常由 Cloudflare 自动签发。若长时间停留在验证状态，检查 CNAME、CAA 记录和域名是否已在其他 Pages 项目中使用。

### 7. 当前需要注意的限制

以 Cloudflare 官方页面的实时说明为准。Free 方案目前主要包括：

| 项目 | 限制 |
| --- | --- |
| 构建次数 | 每月 500 次 |
| 同时构建 | 1 个 |
| 单次构建超时 | 20 分钟 |
| 站点文件数 | 20,000 |
| 单个静态资源 | 25 MiB |

大型书库最容易碰到“文件数”和“单文件 25 MiB”限制。发布前压缩图片并统计 `site/`；大下载文件放到 R2 等对象存储。

### 8. 构建命令为什么使用 build_all.py

只运行 `mkdocs build` 只能生成主知识库，不能把根目录 `books/` 中的独立图书放入最终站点。本站的生产构建命令必须是：

```text
pip install -r requirements.txt && python build_all.py
```

如果以后希望把所有警告也作为失败处理，可以在 `build_all.py` 的每次 MkDocs 调用中加入 `--strict`。先在本地修完旧警告，否则一个未修复的链接警告就会阻止整站上线。

官方文档：[MkDocs 部署指南](https://developers.cloudflare.com/pages/framework-guides/deploy-an-mkdocs-site/)、[Git 集成](https://developers.cloudflare.com/pages/get-started/git-integration/)、[自定义域名](https://developers.cloudflare.com/pages/configuration/custom-domains/)、[Pages 限制](https://developers.cloudflare.com/pages/platform/limits/)。

---

## 8. 更新、排错与检查清单

### 一次标准更新

```powershell
git pull --rebase
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m mkdocs serve
```

完成编辑并在浏览器检查后：

```powershell
python build_all.py
git status
git add docs books mkdocs.yml build_all.py requirements.txt
git commit -m "说明本次修改"
git push
```

随后到 Cloudflare Pages 确认最新提交部署成功。

### Cloudflare 构建失败怎么查

不要只看最后一行 `Failed`，从日志中找到最早出现的具体错误。

| 日志或现象 | 常见原因 | 处理 |
| --- | --- | --- |
| `No module named mkdocs` | 没安装依赖 | 构建命令先运行 `pip install -r requirements.txt` |
| `requirements.txt` 不存在 | Root directory 填错或文件没提交 | 修正根目录，确认文件在 GitHub |
| YAML `mapping values are not allowed` | 缩进、冒号或引号错误 | 检查报错行附近；中文标题统一加引号 |
| `A nav item ... is not found` | `nav` 路径错误 | 路径从 `docs/` 起算，检查大小写和扩展名 |
| 部署成功但首页 404 | 输出目录不对或没有生成 `index.html` | 输出填 `site`，确认 `docs/index.md` 存在 |
| 页面有内容但无样式 | 部署了 `docs` 而非 `site`，或资源路径错误 | 改输出目录并重新部署 |
| 图片本地有、线上 404 | 大小写不一致、图片未提交 | 对比 GitHub 文件名与 Markdown 路径 |
| 构建超过 20 分钟 | 图片/文件过多或依赖重复下载 | 压缩资源、减少生成文件、检查构建流程 |
| `File size limit exceeded` | 某个部署资源超过 25 MiB | 压缩、拆分，或改用对象存储 |

### 首页下拉菜单不出现

检查 `nav` 是否真正形成两层：

```yaml
nav:
  - "从零制作与部署本站":
      - "教程总览": 03-site-building/index.md
      - "1. 准备环境": 03-site-building/01-environment.md
```

如果写成两个同级页面，它们就不会组成下拉菜单。还要确认 `theme.features` 中没有 `navigation.expand`；它会让菜单默认全部展开，而不是按需下拉。

### 独立图书站更新

如果修改的是 `books/<书名>/docs/` 中已经拆好的章节，直接重新构建：

```powershell
python build_all.py
```

只有从一份新的超长 Markdown 重新生成图书项目时，才先运行拆分脚本：

```powershell
python split_book_to_mkdocs_stable_version.py
python build_all.py
```

然后检查：

1. `site/book-sites/demo-book/index.html` 已生成；
2. Library 的入口路径仍然正确；
3. 图书中上一章/下一章、公式和图片正常；
4. `git status` 中只包含预期变更；
5. 构建后的最大文件小于 25 MiB。

### 发布前检查清单

- [ ] `python build_all.py` 成功；
- [ ] 首页、一级下拉菜单和搜索正常；
- [ ] 所有新页面已加入 `nav`；
- [ ] 新图片和 CSS 已提交；
- [ ] 文件名大小写与链接完全一致；
- [ ] 桌面和手机、浅色和深色均已检查；
- [ ] 没有密码、令牌、隐私数据或未授权内容；
- [ ] 没有把 `.venv/` 和 `site/` 提交；
- [ ] 单文件不超过 25 MiB，站点文件数未超 Pages 限制；
- [ ] GitHub 最新提交与 Cloudflare 生产部署显示同一个提交；
- [ ] 自定义域名和 `pages.dev` 均可访问。

### 备份与回退

每次只做一个主题明确的提交，例如“新增建站教程”或“更新风能技术第 3 章”。部署出问题时，可以在 Cloudflare 查看此前成功的部署，也可以在 Git 中找到上一个提交进行对比。

不要在不理解影响时使用 `git reset --hard` 或强制推送。更安全的回退方式是为有问题的提交创建一个反向提交：

```powershell
git log --oneline
git revert 提交编号
git push
```

### 教别人时的推荐顺序

1. 先让对方用共享 YML 跑出最小站；
2. 让对方独立新增一个一级下拉栏目和两篇页面；
3. 再练习 CSS 小改动；
4. 用一本短书测试拆分脚本；
5. 上传到测试仓库；
6. 在 Cloudflare 先看 `pages.dev`；
7. 最后才处理大书和正式域名。
