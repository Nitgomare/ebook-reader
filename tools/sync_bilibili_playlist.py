#!/usr/bin/env python
"""Insert the official Bilibili multipart playlist into matching Python chapters."""

from __future__ import annotations

import json
import hashlib
import re
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "content" / "books" / "shangguigu-python" / "docs"
CODE = ROOT / "content" / "books" / "shangguigu-python" / "code"
BVID = "BV1tDsgzxECr"
API_URL = f"https://api.bilibili.com/x/web-interface/view?bvid={BVID}"
VIDEO_URL = f"https://www.bilibili.com/video/{BVID}?p={{page}}"
START = "<!-- bilibili-playlist:start -->"
END = "<!-- bilibili-playlist:end -->"

# The playlist follows the same progression as the 14 tutorial chapters.
CHAPTER_RANGES = {
    "chapter-01.md": (1, 8),
    "chapter-02.md": (9, 14),
    "chapter-03.md": (15, 30),
    "chapter-04.md": (31, 43),
    "chapter-05.md": (44, 59),
    "chapter-06.md": (60, 88),
    "chapter-07.md": (89, 110),
    "chapter-08.md": (111, 123),
    "chapter-09.md": (124, 126),
    "chapter-10.md": (127, 131),
    "chapter-11.md": (132, 135),
    "chapter-12.md": (136, 141),
    "chapter-13.md": (142, 165),
    "chapter-14.md": (166, 172),
}

CHAPTER_TITLES = {
    "chapter-01.md": "必备基础知识",
    "chapter-02.md": "初识 Python",
    "chapter-03.md": "Python 核心基础",
    "chapter-04.md": "流程控制语句",
    "chapter-05.md": "函数入门",
    "chapter-06.md": "数据容器",
    "chapter-07.md": "面向对象",
    "chapter-08.md": "函数进阶",
    "chapter-09.md": "错误与异常",
    "chapter-10.md": "模块与包",
    "chapter-11.md": "迭代器与生成器",
    "chapter-12.md": "文件操作",
    "chapter-13.md": "进程与线程",
    "chapter-14.md": "协程",
}

CODE_EXTENSIONS = {".py", ".ipynb", ".sql", ".md", ".txt", ".json", ".csv", ".html", ".css", ".js", ".yaml", ".yml", ".toml"}


def load_pages() -> list[dict[str, object]]:
    request = urllib.request.Request(
        API_URL,
        headers={"User-Agent": "Mozilla/5.0 course-content-sync"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
    if payload.get("code") != 0:
        raise RuntimeError(f"Bilibili API error: {payload.get('message', payload.get('code'))}")
    pages = payload["data"]["pages"]
    if len(pages) != 172 or [item["page"] for item in pages] != list(range(1, 173)):
        raise RuntimeError("The playlist no longer matches the reviewed 172-part sequence")
    return pages


def video_block(pages: list[dict[str, object]], start: int, end: int) -> str:
    links = []
    for item in pages[start - 1 : end]:
        page = int(item["page"])
        title = str(item["part"]).strip()
        links.append(f"- [P{page:03d} · {title}]({VIDEO_URL.format(page=page)})")
    return "\n".join(
        [
            START,
            '<details class="chapter-videos" markdown="1">',
            f"<summary><strong>本章配套视频 · P{start:03d}–P{end:03d}（{end - start + 1} 集）</strong></summary>",
            "",
            "视频来自尚硅谷 Python 零基础教程；点击分 P 标题可直接播放对应内容。",
            "",
            *links,
            "",
            "</details>",
            END,
        ]
    )


def compact_video_links(pages: list[dict[str, object]], start: int, end: int) -> str:
    return "<br>".join(
        f"[P{int(item['page']):03d}]({VIDEO_URL.format(page=int(item['page']))})"
        for item in pages[start - 1 : end]
    )


def chapter_code_link(chapter: str) -> str:
    folder = CODE / chapter.removesuffix(".md")
    if not folder.is_dir():
        return ""
    files = sorted(
        path for path in folder.rglob("*")
        if path.is_file()
        and path.suffix.lower() in CODE_EXTENSIONS
        and "__pycache__" not in path.parts
    )
    if not files:
        return ""
    rel_path = files[0].relative_to(CODE).as_posix()
    identifier = hashlib.sha1(f"code/shangguigu-python/{rel_path}".encode("utf-8")).hexdigest()[:16]
    return f"[本章源码（{len(files)}）](#/code/{identifier})"


def build_guide(pages: list[dict[str, object]]) -> str:
    rows = []
    learning_path = []
    for number, (chapter, (start, end)) in enumerate(CHAPTER_RANGES.items(), start=1):
        title = CHAPTER_TITLES[chapter]
        rows.append(
            f"| {number:02d} · {title} | [第 {number} 章]({chapter}) |  | "
            f"{chapter_code_link(chapter)} | {compact_video_links(pages, start, end)} |"
        )
        learning_path.append(f"{number}. [{title}]({chapter})")
    return "\n".join([
        "# Python 基础课程",
        "",
        "从开发环境、核心语法和数据容器逐步学习到面向对象、文件操作、并发与协程，将课本、逐章源码和 172 节配套视频集中在同一条学习路径中。",
        "",
        '<div class="course-guide-note" markdown="1">',
        "",
        "**使用方法**：按课程安排顺序阅读课本，打开对应源码边学边运行，再用分 P 视频补充讲解。空白单元格表示当前资源中没有对应课件或代码。",
        "",
        "</div>",
        "",
        "## 课程安排",
        "",
        '<div class="course-schedule" markdown="1">',
        "",
        "| 主题 | 课本位置 | 课件 | 代码 | 视频 |",
        "| --- | --- | --- | --- | --- |",
        *rows,
        "",
        "</div>",
        "",
        "## 学习路径",
        "",
        *learning_path,
        "",
        "> 所有示例源码均可在网页端预览，也可下载后在本地运行。",
    ])


def update_chapter(path: Path, block: str) -> None:
    raw = path.read_bytes()
    newline = "\r\n" if b"\r\n" in raw else "\n"
    text = raw.decode("utf-8-sig").replace("\r\n", "\n")
    marker = re.compile(rf"{re.escape(START)}.*?{re.escape(END)}", re.S)
    if marker.search(text):
        updated = marker.sub(block, text, count=1)
        updated = re.sub(rf"{re.escape(END)}\n+", END + "\n\n", updated, count=1)
    else:
        heading = re.search(r"^#\s+.+$", text, re.M)
        if not heading:
            raise RuntimeError(f"Missing H1 heading: {path}")
        updated = text[: heading.end()] + "\n\n" + block + "\n\n" + text[heading.end() :].lstrip("\n")
    path.write_text(updated.replace("\n", newline), encoding="utf-8", newline="")


def main() -> None:
    pages = load_pages()
    for filename, (start, end) in CHAPTER_RANGES.items():
        update_chapter(DOCS / filename, video_block(pages, start, end))
        print(f"Updated {filename}: P{start:03d}-P{end:03d}")
    (DOCS / "index.md").write_text(build_guide(pages) + "\n", encoding="utf-8")
    print("Updated index.md course schedule")


if __name__ == "__main__":
    main()
