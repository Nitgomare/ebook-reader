# 5. 拆分书本等大型文件

把几十万字放在一个 Markdown 页面里会导致加载、搜索和编辑都很慢。本站采用“主知识库 + 独立图书站”：每本书按章拆分成自己的 MkDocs 项目，统一构建时再把静态网页放入 `site/book-sites/`。仓库只保存 `books/` 中的图书源文件，不保存重复的图书 HTML。

## 为什么按章拆分

- 浏览器一次只加载当前章；
- 左侧显示章目录，右侧显示本章小节；
- 每章图片独立存放，链接更容易维护；
- 修改一章时不必打开超长文件；
- 搜索索引和构建错误更容易定位。

## 1. 整理源文件

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

## 2. 使用本站拆分脚本

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

## 3. 检查拆分结果

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

## 4. 用统一脚本构建主站和全部图书

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

## 5. 大文件限制与优化

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

下一步：[上传到 GitHub →](06-github.md)
