# 公共知识学习中心

这是一个面向长期运营的静态知识网站，把课程 Markdown、教材图片、逐章 Python 源码、Jupyter Notebook 和练习数据组织在同一个站点中。首页按知识领域分类，左侧目录采用“课程 → 章节”的下拉结构；具备配套代码的章节会显示关联文件，代码库页面也可以集中浏览和下载。

## 当前知识领域

- Python 编程：系统教程，配套逐章 `.py` 示例。
- Python 数据分析：配套 NumPy、Pandas、Matplotlib、Seaborn Notebook 与练习数据。
- 智能机器人：湖南科技大学微专业《轮腿式智能安保巡逻机器人项目实战》，包含跨学科项目教程和演示资源。
- 风电技术：《Wind Energy Handbook》《风能技术（第二版）》和《风力发电机组理论与设计》。

## 架构

```text
ebook-reader/content/books/*/docs/*.md    课程、教材 Markdown 与图片
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

正文仍是静态 HTML、CSS、JavaScript 和 JSON；线上由 Cloudflare Worker 在返回任何文件前执行访问控制。共享密码与 Supabase 独立账号两种模式可以安全切换，账号配置见 [AUTHENTICATION.md](AUTHENTICATION.md)。

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

1. 在课程或教材的 `docs/` 中维护 Markdown 与图片。
2. 在 `mkdocs.yml` 中维护章节顺序。
3. 将可在线查看的源码和数据放进课程 `code/`，按 `chapter-XX/` 与教程章节自动关联。
4. 大型数据文件仍可下载，但网页预览最多读取前 256 KB，避免浏览器卡顿。
5. Python 视频分 P 目录可用 `..\.venv\Scripts\python.exe tools\sync_bilibili_playlist.py` 从 Bilibili 官方接口同步，并按既定章节范围更新。
6. 在 `books.json` 中设置课程所属 `category`；首页会按 `site.categories` 的顺序自动分区。
7. 发布前运行 `manage.py check`，检查章节路由、图片、代码关联、下载文件和 GitHub 单文件上限。
8. 提交源码配置和 `dist/`，再部署到受访问控制保护的 Cloudflare Pages。

## 部署

Cloudflare Pages 发布构建完成的 `dist/`，其中 `_worker.js` 负责登录和内容访问保护。课程源文件同时保存在 `content/books/`，因此仓库克隆后可以独立重建；GitHub 仓库保持私密且不启用 GitHub Pages。
