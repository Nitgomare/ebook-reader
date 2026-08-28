# 2. 建立目录并使用共享 YML

## 推荐目录

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

## 共享 YML

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

## YML 最重要的缩进规则

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

## `.gitignore`

在项目根目录创建：

```gitignore
site/
.venv/
__pycache__/
*.pyc
.DS_Store
```

不要忽略 `docs/`、`books/`、`mkdocs.yml`、`build_all.py`、`requirements.txt`。它们正是 Cloudflare 构建网站所需的源文件。

## 用检查命令发现路径错误

```powershell
python -m mkdocs build --strict
```

`--strict` 会把警告当成错误，特别适合发现 `nav` 指向不存在文件、Markdown 链接失效等问题。第一次整理旧项目时可以先不加 `--strict`，逐步修完警告后再启用。

下一步：[编写页面与设置导航 →](03-writing-and-nav.md)
