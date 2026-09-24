"""按图片文件名在正文里定位 Markdown 图片行，生成容器替换方案。

用法：
    ..\\.venv\\Scripts\\python.exe tools\\locate_figure_images.py 29_576_780_494_442_0.jpg 41_399_1291_876_432_0.jpg
输出每张图片所在的书籍、Markdown 文件、行号与原始行内容。
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BOOKS_ROOT = REPO / "content" / "books"


def main() -> None:
    names = sys.argv[1:]
    if not names:
        raise SystemExit("请给出至少一个图片文件名")
    for book in sorted(BOOKS_ROOT.iterdir()):
        docs = book / "docs"
        if not docs.is_dir():
            continue
        for path in sorted(docs.rglob("*.md")):
            lines = path.read_text(encoding="utf-8").splitlines()
            for index, line in enumerate(lines, 1):
                for name in names:
                    if name in line and "![" in line:
                        rel = path.relative_to(REPO)
                        print(f"{name}\t{rel.as_posix()}\t{index}\t{line.strip()}")


if __name__ == "__main__":
    main()
