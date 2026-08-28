# 4. 调整主题与自定义样式

先用 `mkdocs.yml` 提供的主题选项完成大部分外观设置，只有主题选项无法实现的效果才写 CSS。这样升级 Material 时更稳定。

## 修改主色和强调色

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

## 修改左上角图标

```yaml
theme:
  icon:
    logo: material/school
```

可以替换为 `material/book-open-page-variant`、`material/flask`、`material/wind-turbine` 等 Material 图标。

## 引入自己的 CSS

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

## 制作首页重点入口

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

## 样式调试顺序

1. 保持 `python -m mkdocs serve` 运行；
2. 只改一个 CSS 属性并保存；
3. 浏览器按 ++ctrl+f5++ 强制刷新；
4. 同时检查浅色、深色、桌面和手机宽度；
5. 使用浏览器开发者工具确认选择器命中了目标元素。

!!! warning "避免直接复制主题内部 CSS"
    Material 更新后，内部类名和结构可能变化。自定义选择器尽量短，颜色尽量使用 `--md-*` 变量，以便自动适配深浅色。

## 常见问题

| 现象 | 检查 |
| --- | --- |
| CSS 完全不生效 | 文件是否位于 `docs/`；`extra_css` 路径是否正确；是否重新构建 |
| 本地生效、线上不生效 | 文件名大小写；是否已经提交并推送；Cloudflare 是否部署了最新提交 |
| 深色模式看不清 | 是否写死白色/黑色；改用 Material CSS 变量 |
| 手机侧栏错位 | 选择器是否只限定 `.md-sidebar--primary`；是否设置了固定宽度 |

下一步：[拆分书本等大型文件 →](05-split-large-books.md)
