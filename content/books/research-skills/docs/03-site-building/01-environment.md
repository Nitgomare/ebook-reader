# 1. 准备环境与工具

## 需要安装什么

| 工具 | 用途 | 检查命令 |
| --- | --- | --- |
| Python 3.11 或更高版本 | 运行 MkDocs 和图书拆分脚本 | `python --version` |
| Git | 保存版本并上传 GitHub | `git --version` |
| VS Code（推荐） | 编辑 Markdown、YML 和 CSS | 无 |
| GitHub Desktop（可选） | 不熟悉命令行时提交和推送 | 无 |

Windows 安装 Python 时勾选 **Add Python to PATH**。安装后重新打开 PowerShell，再运行检查命令。

## 创建项目和虚拟环境

以下命令里的 `research-site` 是项目文件夹名，可以替换：

```powershell
mkdir research-site
cd research-site
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

成功激活后，命令行开头通常会出现 `(.venv)`。

!!! question "PowerShell 不允许执行 Activate.ps1"
    可以直接跳过激活，在后续命令中使用 `.\.venv\Scripts\python.exe`；也可以只对当前窗口运行：

    ```powershell
    Set-ExecutionPolicy -Scope Process Bypass
    .\.venv\Scripts\Activate.ps1
    ```

## 安装 MkDocs Material

```powershell
python -m pip install --upgrade pip
python -m pip install mkdocs-material==9.7.6
```

确认安装成功：

```powershell
python -m mkdocs --version
```

在项目根目录创建 `requirements.txt`：

```text
mkdocs-material==9.7.6
```

这个文件既能让别人复现相同环境，也会用于 Cloudflare Pages 安装依赖。

## 最小化试运行

```powershell
python -m mkdocs new .
python -m mkdocs serve
```

浏览器访问 `http://127.0.0.1:8000/`。终端保持运行时，保存 Markdown 后浏览器会自动刷新。按 ++ctrl+c++ 停止预览。

!!! tip "本站项目已经存在时"
    不要再运行 `mkdocs new .`，直接进入包含 `mkdocs.yml` 的目录，安装依赖后运行 `python -m mkdocs serve`。

## 建议的编辑器设置

- 文件统一使用 UTF-8 编码；
- 缩进使用空格，不使用 Tab；
- YML 建议每层缩进 2 个空格；
- 打开“保存时删除行尾空格”；
- 安装 Markdown 和 YAML 语法检查扩展。

下一步：[建立目录并使用共享 YML →](02-structure-and-yml.md)
