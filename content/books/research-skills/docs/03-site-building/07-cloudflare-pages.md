# 7. 用 Cloudflare Pages 部署

Cloudflare Pages 会克隆 GitHub 仓库、安装 `requirements.txt` 中的 Python 包、运行 MkDocs，再把 `site/` 发布到全球网络。以后每次推送到生产分支都会自动重复这套流程。

## 1. 连接 GitHub 仓库

1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com/)；
2. 进入 **Workers & Pages**；
3. 选择 **Create application** → **Pages** → **Connect to Git**（界面文字可能随版本调整）；
4. 选择 GitHub 并安装/授权 **Cloudflare Workers and Pages**；
5. 只授权目标仓库更安全；仓库不出现时，回 GitHub 的应用安装设置补充访问权限；
6. 选中知识库仓库，进入构建设置。

Cloudflare Pages 支持公开和私有 GitHub 仓库。

## 2. 填写构建参数

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

## 3. Python 版本

Cloudflare Pages 的新构建镜像自带 Python。一般无需设置版本；若希望环境完全可复现，可以在项目设置的环境变量中添加：

```text
PYTHON_VERSION = 3.12
```

也可以在仓库根目录使用 `.python-version`。`requirements.txt` 中固定 MkDocs Material 版本，可以避免主题自动升级导致构建结果突然改变。

## 4. 首次部署

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

## 5. 自动更新与预览

- 推送到 `main`：更新生产站；
- 推送到其他分支：默认生成预览部署；
- 创建 Pull Request：GitHub 页面可显示 Pages 检查和预览链接；
- 每次部署都对应一个提交，可在 Pages 的部署列表查看日志和历史版本。

预览地址默认公开，但 Cloudflare 会给预览部署添加 `X-Robots-Tag: noindex`。敏感项目仍应配置 Cloudflare Access，不能只依赖“不被搜索引擎收录”。

## 6. 绑定自定义域名（可选）

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

## 7. 当前需要注意的限制

以 Cloudflare 官方页面的实时说明为准。Free 方案目前主要包括：

| 项目 | 限制 |
| --- | --- |
| 构建次数 | 每月 500 次 |
| 同时构建 | 1 个 |
| 单次构建超时 | 20 分钟 |
| 站点文件数 | 20,000 |
| 单个静态资源 | 25 MiB |

大型书库最容易碰到“文件数”和“单文件 25 MiB”限制。发布前压缩图片并统计 `site/`；大下载文件放到 R2 等对象存储。

## 8. 构建命令为什么使用 build_all.py

只运行 `mkdocs build` 只能生成主知识库，不能把根目录 `books/` 中的独立图书放入最终站点。本站的生产构建命令必须是：

```text
pip install -r requirements.txt && python build_all.py
```

如果以后希望把所有警告也作为失败处理，可以在 `build_all.py` 的每次 MkDocs 调用中加入 `--strict`。先在本地修完旧警告，否则一个未修复的链接警告就会阻止整站上线。

官方文档：[MkDocs 部署指南](https://developers.cloudflare.com/pages/framework-guides/deploy-an-mkdocs-site/)、[Git 集成](https://developers.cloudflare.com/pages/get-started/git-integration/)、[自定义域名](https://developers.cloudflare.com/pages/configuration/custom-domains/)、[Pages 限制](https://developers.cloudflare.com/pages/platform/limits/)。

下一步：[更新、排错与检查清单 →](08-maintenance.md)
