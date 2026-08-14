# 统一电子书阅读器（迁移原型）

这个目录是现有 MkDocs 网站旁边的一套独立电子书前端。它不会修改 `books/` 中的正文，也不会覆盖当前主站。左侧导航采用“书籍 → 章节”折叠菜单：一本书是一个一级下拉项，展开后显示该书的章节。

## 架构

```text
books/*/docs/*.md              原有 Markdown（唯一内容源）
        │
        ├─ books/*/mkdocs.yml  沿用现有章节顺序
        ▼
ebook-reader/build.py          扫描、渲染、改写内部链接、复制正文引用的资源
        ▼
ebook-reader/dist/
  ├─ index.html                原生 JavaScript 单页阅读器
  ├─ data/catalog.json         书籍与章节总目录
  ├─ data/docs/*.json          预渲染文章与页内标题
  └─ files/<book>/...          只复制实际引用的图片和附件
```

运行时没有 Python、Node 或数据库：浏览器只读取静态 HTML、CSS、JavaScript 和 JSON，因此可以部署到 GitHub Pages、Cloudflare Pages、Netlify 或任意静态文件服务器。

## 快速验证

在当前工作区的 `ebook-reader` 目录运行：

```powershell
..\knowledge-base\.venv\Scripts\python.exe manage.py preview --book deep-learning
```

也可以直接双击 `preview.cmd`，或在 PowerShell 中运行：

```powershell
.\preview.cmd
```

然后打开 `http://127.0.0.1:8010`。去掉 `--book deep-learning` 会构建 `books.json` 中配置的全部电子书；大型教材图片较多，首次完整构建会更慢、产物也会更大。

只生成静态文件：

```powershell
..\knowledge-base\.venv\Scripts\python.exe manage.py build
```

构建并检查目录、章节路由和图片附件是否完整：

```powershell
..\knowledge-base\.venv\Scripts\python.exe manage.py check
```

## 日常内容工作流

1. 继续在原来的 `books/<书名>/docs/` 中编写 Markdown。
2. 在对应 `mkdocs.yml` 的 `nav` 中调整章节顺序；未列入 `nav` 的 Markdown 会自动追加到“其他”。
3. 新增一本书时，在 `books.json` 添加书名、作者、简介和标签。
4. 本地运行 `manage.py preview` 检查书架、章节、图片、公式、上一篇/下一篇和移动端目录。
5. 发布前运行 `manage.py build`，将 `dist/` 作为静态站点产物部署。

## 推荐迁移顺序

1. **并行试运行**：保留当前 MkDocs 主站和独立图书站，只发布新的电子书入口供验收。
2. **逐书校验**：检查每本书的内部链接、图片、公式、表格和代码块；有问题只修构建器或原 Markdown，不复制正文。
3. **接入主站**：把当前“课程中心”的卡片链接改到新阅读器的 `#/book/<slug>`。
4. **统一部署**：CI 中先运行 `build.py`，再上传 `dist/`；若仍需主站，可将阅读器产物放在主站的 `ebook/` 子路径。
5. **下线旧产物**：全部图书验证完成后，停止构建 `site/book-sites/*`，保留 `books/*/docs` 作为内容源。

## GitHub Pages 发布

仓库提交预构建的 `dist/`。推送到 `main` 后，`.github/workflows/pages.yml` 会直接上传该目录并部署 GitHub Pages。更新正文时，先在本地重新构建并检查，再提交新的 `dist/`。

## 与参考站的关系

本原型复用了相同的核心思路：Markdown 自动生成目录与文章数据、Hash 路由、左侧章节树、中间正文、右侧页内目录、静态部署。界面和代码为本项目重新实现，并扩展成“一套阅读器管理多本书”，更适合现有知识库。
