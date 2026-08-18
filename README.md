# Python 与数据分析学习中心

这是一个面向长期运营的静态学习网站，把课程 Markdown、逐章 Python 源码、Jupyter Notebook 和练习数据组织在同一条学习路径中。左侧目录仍采用“课程 → 章节”的下拉结构；每章末尾会显示关联代码，代码库页面也可以集中浏览和下载文件。

## 当前核心课程

- Python 系统学习：14 章，配套逐章 `.py` 示例。
- Python 数据分析实战：4 章，配套 NumPy、Pandas、Matplotlib、Seaborn Notebook 与练习数据。

## 架构

```text
ebook-reader/content/books/*/docs/*.md    课程 Markdown 与图片
ebook-reader/content/books/*/code/*       配套源码、Notebook 和数据
                 │
                 ▼
ebook-reader/build.py               渲染正文、生成目录、代码预览并复制下载文件
                 │
                 ▼
ebook-reader/dist/
  ├─ index.html                     原生 JavaScript 单页学习站
  ├─ data/catalog.json              课程、章节与代码总目录
  ├─ data/docs/*.json               预渲染章节
  ├─ data/code/*.json               源码或 Notebook 网页预览
  └─ files/...                      图片、源码和数据下载文件
```

运行时不需要 Python、Node、数据库或后端服务，浏览器只读取静态 HTML、CSS、JavaScript 和 JSON，适合 GitHub Pages、Cloudflare Pages 等静态托管平台。

## 本地运行

首次在工作区根目录创建环境并安装依赖：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r .\ebook-reader\requirements.txt
```

进入 `ebook-reader` 后运行：

```powershell
..\.venv\Scripts\python.exe manage.py preview
```

然后打开 `http://127.0.0.1:8010`。也可以双击 `preview.cmd`。

只构建或检查：

```powershell
..\.venv\Scripts\python.exe manage.py build
..\.venv\Scripts\python.exe manage.py check
```

## 内容维护流程

1. 在课程的 `docs/` 中维护 Markdown 与图片。
2. 在 `mkdocs.yml` 中维护章节顺序。
3. 将可在线查看的源码和数据放进课程 `code/`，按 `chapter-XX/` 与教程章节自动关联。
4. 大型数据文件仍可下载，但网页预览最多读取前 256 KB，避免浏览器卡顿。
5. 发布前运行 `manage.py check`，检查章节路由、图片、代码关联、下载文件和 GitHub 单文件上限。
6. 提交源码配置和 `dist/`；推送到 `main` 后，GitHub Actions 自动部署 Pages。

## 部署

`.github/workflows/pages.yml` 直接上传构建完成的 `dist/`。课程源文件同时保存在 `content/books/`，因此仓库克隆后可以独立重建；线上仍只发布静态产物，不运行任何动态代码。
