# 3. 编写页面与设置导航

## 新建一篇页面

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

## 把页面加入导航

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

## Markdown 常用写法

### 链接

同一网站优先使用相对路径：

```markdown
[下一节](02-literature-screening.md)
[返回首页](../index.md)
[打开外部网站](https://example.com)
```

路径和文件名大小写要完全一致。Windows 本地不敏感，但 Cloudflare 的 Linux 构建和线上 URL 会区分大小写。

### 图片

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

### 提示框

```markdown
!!! tip "操作提示"
    提示框正文缩进 4 个空格。

!!! warning "注意"
    修改 YML 后要重新启动本地预览。

??? example "点击展开示例"
    这里可以放较长的补充内容。
```

### 代码、表格和公式

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

## 首页卡片

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

下一步：[调整主题与自定义样式 →](04-styling.md)
