# 机器人课程资源中心

本目录保存课程页面、样式与发布生成脚本，线上路径为 `/robot-hub/`。
原始资料来自仓库上一级 `机器人相关课程from文丽/`，不修改原始文件。

页面信息取舍与资料核对、缺件、发布待办见 [维护说明](MAINTENANCE.md)。读者必要的使用限制保留在对应资源旁，维护事项不展示在课程页面。

## 更新方式

1. 修改本目录 HTML 或 `assets/`。
2. 运行 `..\.venv\Scripts\python.exe tools/robot-hub/build_release.py`，生成 `public/robot-hub/`。
3. 运行 `..\.venv\Scripts\python.exe tools/robot-hub/check_links.py public/robot-hub`。
4. 更新 `CHANGELOG.md`，运行完整 `manage.py check`，再提交和部署。

命令在仓库根目录执行。完整发布包已保存在仓库 `public/robot-hub/`，不需要原始资料也可构建和部署现有版本；重新筛选资源时需要原始目录。

发布规则：不发布独立视频、Office 或 ZIP 内嵌视频、超过 25 MiB 的单文件、Office 临时文件及 Python 缓存。未发布的链接改为文字说明。明细见生成后的 `RELEASE.md` 和 `release-manifest.json`。

课程资源中心使用现有 Worker 登录保护。学习中心顶部及智能机器人分类均有入口，课程页面导航提供返回学习中心链接。
