"""交互图生成器：把公共底座 figure-kit.js 与各图专属代码合成单文件 HTML。

设计要点：
1. 每张交互图输出为**单文件 HTML**：内联 CSS 与 JavaScript，不依赖任何网络资源。
   公共底座 content/books/<slug>/docs/interactive/figure-kit.js 会在生成时内联进 <script>，
   因此交付物满足《PROJECT_HANDOFF.md》7.3 的“单文件 HTML + 内联 CSS/JS”约束。
2. 每个交互图由“规格文件”描述：content/books/<slug>/docs/interactive/specs/<id>.py
   规格文件必须定义 FIGURE 字典（见本文件 build_html 的字段说明）。
3. 生成结果默认写入 tmp/generated/interactive/，再由调用者（或 --install）搬运到
   content/books/<slug>/docs/interactive/figure-<章号>-<图序号>.html。
   之所以分两步：本工作区的模式化沙箱只允许脚本在 tmp/ 下写文件，
   content/ 与 public/ 的写入由 Agent 的文件工具完成。

用法：
    ..\\.venv\\Scripts\\python.exe tools/build_interactive_figures.py              # 生成到 tmp/generated/interactive
    ..\\.venv\\Scripts\\python.exe tools/build_interactive_figures.py figure-2-6   # 只生成指定图
    ..\\.venv\\Scripts\\python.exe tools/build_interactive_figures.py --check      # 只校验不写盘
    ..\\.venv\\Scripts\\python.exe tools/build_interactive_figures.py --stdout figure-2-6  # 打印到标准输出
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BOOKS_ROOT = REPO_ROOT / "content" / "books"
OUTPUT_ROOT = REPO_ROOT / "tmp" / "generated" / "interactive"

BOOKS = {
    "craig-introduction-to-robotics": "《机器人学导论（第3版）》",
    "robot-technology-basics": "《机器人技术基础（第三版）》",
}

SHELL = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
{css}
</style>
</head>
<body>
<main class="app">
{body}
</main>
<script>
{kit}
</script>
<script>
{script}
</script>
</body>
</html>
"""


def read_kit(book_root: Path) -> str:
    kit = book_root / "docs" / "interactive" / "figure-kit.js"
    if not kit.is_file():
        raise SystemExit(f"找不到 {kit}")
    return kit.read_text(encoding="utf-8")


def load_spec(path: Path) -> dict:
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    figure = getattr(module, "FIGURE", None)
    if not isinstance(figure, dict):
        raise SystemExit(f"{path} 未定义 FIGURE 字典")
    for key in ("id", "title", "css", "body", "script"):
        if key not in figure:
            raise SystemExit(f"{path} 的 FIGURE 缺少字段：{key}")
    return figure


def build_html(figure: dict, kit: str) -> str:
    css = figure["css"].strip()
    script = figure["script"].strip()
    return SHELL.format(
        title=figure["title"],
        css=css,
        body=figure["body"].strip(),
        kit=kit.strip(),
        script=script,
    )


def collect_specs(only: str | None) -> list[tuple[str, Path]]:
    found: list[tuple[str, Path]] = []
    for slug in BOOKS:
        specs_dir = BOOKS_ROOT / slug / "docs" / "interactive" / "specs"
        if not specs_dir.is_dir():
            continue
        for path in sorted(specs_dir.glob("*.py")):
            if path.name.startswith("_"):
                continue
            if only and path.stem != only:
                continue
            found.append((slug, path))
    return found


def main() -> None:
    parser = argparse.ArgumentParser(description="生成交互图单文件 HTML")
    parser.add_argument("figure", nargs="?", help="只生成指定交互图 id（不带 .py）")
    parser.add_argument("--check", action="store_true", help="只检查，不写盘")
    parser.add_argument("--stdout", action="store_true", help="把结果打印到标准输出（配合 --check）")
    parser.add_argument("--install", action="store_true",
                        help="生成后直接搬运到 content/books/<slug>/docs/interactive/")
    args = parser.parse_args()

    specs = collect_specs(args.figure)
    if not specs:
        raise SystemExit("没有找到任何规格文件")

    written = 0
    installed = 0
    for slug, spec_path in specs:
        book_root = BOOKS_ROOT / slug
        figure = load_spec(spec_path)
        kit = read_kit(book_root)
        html = build_html(figure, kit)
        target = OUTPUT_ROOT / slug / f"{figure['id']}.html"
        if args.stdout:
            sys.stdout.write(html)
            continue
        if args.check:
            print(f"[check] {target.relative_to(REPO_ROOT)} 将生成 {len(html)} 字节")
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html, encoding="utf-8")
        written += 1
        print(f"[write] {target.relative_to(REPO_ROOT)} ({len(html)} 字节)")
        install_target = book_root / "docs" / "interactive" / f"{figure['id']}.html"
        if args.install:
            install_target.write_text(html, encoding="utf-8")
            installed += 1
            print(f"[install] {install_target.relative_to(REPO_ROOT)}")
    if not args.check and not args.stdout:
        print(f"完成：生成 {written} 个交互图"
              + (f"，已搬运 {installed} 个到 content/" if args.install else "，待搬运到 content/books/<slug>/docs/interactive/"))


if __name__ == "__main__":
    main()
