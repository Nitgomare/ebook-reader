# 8. 更新、排错与检查清单

## 一次标准更新

```powershell
git pull --rebase
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m mkdocs serve
```

完成编辑并在浏览器检查后：

```powershell
python build_all.py
git status
git add docs books mkdocs.yml build_all.py requirements.txt
git commit -m "说明本次修改"
git push
```

随后到 Cloudflare Pages 确认最新提交部署成功。

## Cloudflare 构建失败怎么查

不要只看最后一行 `Failed`，从日志中找到最早出现的具体错误。

| 日志或现象 | 常见原因 | 处理 |
| --- | --- | --- |
| `No module named mkdocs` | 没安装依赖 | 构建命令先运行 `pip install -r requirements.txt` |
| `requirements.txt` 不存在 | Root directory 填错或文件没提交 | 修正根目录，确认文件在 GitHub |
| YAML `mapping values are not allowed` | 缩进、冒号或引号错误 | 检查报错行附近；中文标题统一加引号 |
| `A nav item ... is not found` | `nav` 路径错误 | 路径从 `docs/` 起算，检查大小写和扩展名 |
| 部署成功但首页 404 | 输出目录不对或没有生成 `index.html` | 输出填 `site`，确认 `docs/index.md` 存在 |
| 页面有内容但无样式 | 部署了 `docs` 而非 `site`，或资源路径错误 | 改输出目录并重新部署 |
| 图片本地有、线上 404 | 大小写不一致、图片未提交 | 对比 GitHub 文件名与 Markdown 路径 |
| 构建超过 20 分钟 | 图片/文件过多或依赖重复下载 | 压缩资源、减少生成文件、检查构建流程 |
| `File size limit exceeded` | 某个部署资源超过 25 MiB | 压缩、拆分，或改用对象存储 |

## 首页下拉菜单不出现

检查 `nav` 是否真正形成两层：

```yaml
nav:
  - "从零制作与部署本站":
      - "教程总览": 03-site-building/index.md
      - "1. 准备环境": 03-site-building/01-environment.md
```

如果写成两个同级页面，它们就不会组成下拉菜单。还要确认 `theme.features` 中没有 `navigation.expand`；它会让菜单默认全部展开，而不是按需下拉。

## 独立图书站更新

如果修改的是 `books/<书名>/docs/` 中已经拆好的章节，直接重新构建：

```powershell
python build_all.py
```

只有从一份新的超长 Markdown 重新生成图书项目时，才先运行拆分脚本：

```powershell
python split_book_to_mkdocs_stable_version.py
python build_all.py
```

然后检查：

1. `site/book-sites/demo-book/index.html` 已生成；
2. Library 的入口路径仍然正确；
3. 图书中上一章/下一章、公式和图片正常；
4. `git status` 中只包含预期变更；
5. 构建后的最大文件小于 25 MiB。

## 发布前检查清单

- [ ] `python build_all.py` 成功；
- [ ] 首页、一级下拉菜单和搜索正常；
- [ ] 所有新页面已加入 `nav`；
- [ ] 新图片和 CSS 已提交；
- [ ] 文件名大小写与链接完全一致；
- [ ] 桌面和手机、浅色和深色均已检查；
- [ ] 没有密码、令牌、隐私数据或未授权内容；
- [ ] 没有把 `.venv/` 和 `site/` 提交；
- [ ] 单文件不超过 25 MiB，站点文件数未超 Pages 限制；
- [ ] GitHub 最新提交与 Cloudflare 生产部署显示同一个提交；
- [ ] 自定义域名和 `pages.dev` 均可访问。

## 备份与回退

每次只做一个主题明确的提交，例如“新增建站教程”或“更新风能技术第 3 章”。部署出问题时，可以在 Cloudflare 查看此前成功的部署，也可以在 Git 中找到上一个提交进行对比。

不要在不理解影响时使用 `git reset --hard` 或强制推送。更安全的回退方式是为有问题的提交创建一个反向提交：

```powershell
git log --oneline
git revert 提交编号
git push
```

## 教别人时的推荐顺序

1. 先让对方用共享 YML 跑出最小站；
2. 让对方独立新增一个一级下拉栏目和两篇页面；
3. 再练习 CSS 小改动；
4. 用一本短书测试拆分脚本；
5. 上传到测试仓库；
6. 在 Cloudflare 先看 `pages.dev`；
7. 最后才处理大书和正式域名。

回到[教程总览](index.md)，或直接打开[共享 YML](02-structure-and-yml.md#yml)。
