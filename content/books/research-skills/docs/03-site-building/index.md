# 从零制作与部署本站

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

## 学习路线

<ol class="tutorial-steps">
  <li><a href="01-environment/">准备环境与工具</a>：安装 Python、Git 和编辑器，建立虚拟环境。</li>
  <li><a href="02-structure-and-yml/">建立目录并使用共享 YML</a>：照着模板创建项目，不必从头手写配置。</li>
  <li><a href="03-writing-and-nav/">编写页面与设置导航</a>：写 Markdown，把课程做成左侧一级下拉菜单。</li>
  <li><a href="04-styling/">调整主题与自定义样式</a>：修改颜色、字体、卡片和导航样式。</li>
  <li><a href="05-split-large-books/">拆分书本等大型文件</a>：把一本超长 Markdown 按章拆成独立图书站。</li>
  <li><a href="06-github/">上传到 GitHub</a>：创建仓库、首次上传和日常更新。</li>
  <li><a href="07-cloudflare-pages/">用 Cloudflare Pages 部署</a>：连接仓库、填写构建参数、配置域名。</li>
  <li><a href="08-maintenance/">更新、排错与检查</a>：定位构建失败、链接失效和大文件问题。</li>
</ol>

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

    下载本站共享的 [`mkdocs.yml`](02-structure-and-yml.md#yml)，复制目录结构，再逐项替换站名、导航和页面内容。

## 你需要准备的内容

- 网站名称和一句简介；
- 计划设置的一级栏目；
- 每个栏目下的 Markdown 页面；
- 合法且有权公开的图片、论文或书籍内容；
- GitHub 和 Cloudflare 账号。

!!! danger "公开前检查版权和隐私"
    Cloudflare Pages 的生产站点默认可被任何人访问。不要上传未获授权的书籍、个人信息、账号密码、API 密钥或内部资料。大型资料的“技术上能发布”不等于“法律上可以公开”。

下一步：[准备环境与工具 →](01-environment.md)
