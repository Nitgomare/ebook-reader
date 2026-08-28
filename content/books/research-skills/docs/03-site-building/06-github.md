# 6. 上传到 GitHub

GitHub 保存的是网站源文件。Cloudflare Pages 连接仓库后，每次收到新的提交都会自动构建并部署。

## 1. 上传前本地检查

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

## 2. 在 GitHub 创建空仓库

1. 登录 GitHub，点击右上角 **New repository**；
2. 填写仓库名，例如 `research-knowledge-base`；
3. 公开站可选 Public，内部协作可选 Private；Cloudflare Pages 支持连接公开和私有仓库；
4. 如果本地已有项目，不要勾选自动创建 README、`.gitignore` 或 License；
5. 点击 **Create repository**。

## 3. 第一次上传

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

## 4. 日常更新

```powershell
git status
git add docs books mkdocs.yml build_all.py requirements.txt
git commit -m "新增网站制作教程"
git push
```

比起总用 `git add .`，明确列出要提交的路径更容易避免误传。

## 5. 用分支预览后再上线

重要改版建议使用分支：

```powershell
git switch -c update/site-tutorial
git add docs mkdocs.yml
git commit -m "新增建站教程"
git push -u origin update/site-tutorial
```

在 GitHub 创建 Pull Request 后，Cloudflare Pages 会为它生成独立预览地址。检查无误再合并到 `main`，生产网站才会更新。

## 6. 常见推送错误

| 错误 | 处理 |
| --- | --- |
| `remote origin already exists` | 先运行 `git remote -v`；需要改地址时用 `git remote set-url origin 新地址` |
| `rejected ... fetch first` | 远端已有提交，先 `git pull --rebase origin main`，解决冲突后再推送 |
| 文件超过 100 MiB | 不要反复 push；先从即将提交的内容和历史中正确移除，再压缩、拆分或使用对象存储 |
| 大小写改名线上不生效 | 用 `git mv old.md temp.md` 后再 `git mv temp.md New.md` |
| Cloudflare 没有触发 | 确认推送到了它设置的生产分支，并检查 Pages 的 Git 集成权限 |

GitHub 官方说明：[从命令行添加本地代码](https://docs.github.com/en/repositories/creating-and-managing-repositories/adding-locally-hosted-code-to-github)、[大文件限制](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)。

下一步：[用 Cloudflare Pages 部署 →](07-cloudflare-pages.md)
