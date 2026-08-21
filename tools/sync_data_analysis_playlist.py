#!/usr/bin/env python
"""Build the data-analysis course guide and chapter playlists from Bilibili."""

from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "content" / "books" / "shangguigu-data-analysis" / "docs"
BVID = "BV1D9GLzyEL6"
API_URL = f"https://api.bilibili.com/x/web-interface/view?bvid={BVID}"
VIDEO_URL = f"https://www.bilibili.com/video/{BVID}?p={{page}}"
START = "<!-- bilibili-data-playlist:start -->"
END = "<!-- bilibili-data-playlist:end -->"

CHAPTER_RANGES = {
    "chapter-01.md": (1, 5),
    "chapter-02.md": (6, 21),
    "chapter-03.md": (22, 52),
    "chapter-04.md": (53, 69),
}

# topic, textbook label/path, code label/id, first video, last video
SCHEDULE = [
    ("课程介绍与学习路线", "第 1 章", "chapter-01.md", "", "", 1, 1),
    ("Anaconda、Jupyter 与 PyCharm", "第 1 章", "chapter-01.md", "", "", 2, 5),
    ("NumPy 与 ndarray 基础", "第 2 章", "chapter-02.md", "NumPy Notebook", "2e13022a9c828d0b", 6, 8),
    ("ndarray 创建与数据类型", "第 2 章", "chapter-02.md", "NumPy Notebook", "2e13022a9c828d0b", 9, 12),
    ("索引、运算与常用函数", "第 2 章", "chapter-02.md", "NumPy Notebook", "2e13022a9c828d0b", 13, 18),
    ("NumPy 小结与练习", "第 2 章", "chapter-02.md", "NumPy Notebook", "2e13022a9c828d0b", 19, 21),
    ("Pandas 与 Series 基础", "第 3 章", "chapter-03.md", "Series Notebook", "12d66456459b48d3", 22, 27),
    ("Series 数据分析案例", "第 3 章", "chapter-03.md", "Series Notebook", "12d66456459b48d3", 28, 33),
    ("DataFrame 基础与常用方法", "第 3 章", "chapter-03.md", "DataFrame Notebook", "6c1ffe660171cb77", 34, 38),
    ("DataFrame 案例与小结", "第 3 章", "chapter-03.md", "DataFrame Notebook", "6c1ffe660171cb77", 39, 41),
    ("数据分析流程与数据导入导出", "第 3 章", "chapter-03.md", "数据分析 Notebook", "760170eac73f6f5c", 42, 43),
    ("清洗、变形、分箱与时间数据", "第 3 章", "chapter-03.md", "数据分析 Notebook", "760170eac73f6f5c", 44, 48),
    ("分组聚合与综合案例", "第 3 章", "chapter-03.md", "数据分析 Notebook", "760170eac73f6f5c", 49, 52),
    ("数据可视化与 Matplotlib", "第 4 章", "chapter-04.md", "Matplotlib Notebook", "aab09632493e7a4b", 53, 60),
    ("Seaborn 可视化", "第 4 章", "chapter-04.md", "Seaborn Notebook", "699e2e2adb7101e2", 61, 61),
    ("房地产市场分析项目", "第 4 章", "chapter-04.md", "项目 Notebook", "a72d82e453f4f082", 62, 69),
]


def load_pages() -> list[dict[str, object]]:
    request = urllib.request.Request(API_URL, headers={"User-Agent": "Mozilla/5.0 course-content-sync"})
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
    if payload.get("code") != 0:
        raise RuntimeError(f"Bilibili API error: {payload.get('message', payload.get('code'))}")
    pages = payload["data"]["pages"]
    if len(pages) != 69 or [item["page"] for item in pages] != list(range(1, 70)):
        raise RuntimeError("The playlist no longer matches the reviewed 69-part sequence")
    return pages


def video_links(pages: list[dict[str, object]], start: int, end: int, detailed: bool) -> str:
    links = []
    for item in pages[start - 1 : end]:
        page = int(item["page"])
        label = f"P{page:03d} · {str(item['part']).strip()}" if detailed else f"P{page:03d}"
        links.append(f"[{label}]({VIDEO_URL.format(page=page)})")
    return "<br>".join(links) if not detailed else "\n".join(f"- {link}" for link in links)


def video_block(pages: list[dict[str, object]], start: int, end: int) -> str:
    return "\n".join([
        START,
        '<details class="chapter-videos" markdown="1">',
        f"<summary><strong>本章配套视频 · P{start:03d}–P{end:03d}（{end - start + 1} 集）</strong></summary>",
        "",
        "点击分 P 标题可直接播放对应内容。",
        "",
        video_links(pages, start, end, detailed=True),
        "",
        "</details>",
        END,
    ])


def update_chapter(path: Path, block: str) -> None:
    raw = path.read_bytes()
    newline = "\r\n" if b"\r\n" in raw else "\n"
    text = raw.decode("utf-8-sig").replace("\r\n", "\n")
    marker = re.compile(rf"{re.escape(START)}.*?{re.escape(END)}", re.S)
    if marker.search(text):
        updated = marker.sub(block, text, count=1)
    else:
        heading = re.search(r"^#\s+.+$", text, re.M)
        if not heading:
            raise RuntimeError(f"Missing H1 heading: {path}")
        updated = text[: heading.end()] + "\n\n" + block + "\n\n" + text[heading.end() :].lstrip("\n")
    path.write_text(updated.replace("\n", newline), encoding="utf-8", newline="")


def build_guide(pages: list[dict[str, object]]) -> str:
    rows = []
    for topic, book_label, book_path, code_label, code_id, start, end in SCHEDULE:
        code = f"[{code_label}](#/code/{code_id})" if code_id else ""
        rows.append(
            f"| {topic} | [{book_label}]({book_path}) |  | {code} | "
            f"{video_links(pages, start, end, detailed=False)} |"
        )
    return "\n".join([
        "# Python 数据分析课程",
        "",
        "围绕 NumPy、Pandas、Matplotlib 与 Seaborn，将课本、代码和 69 节配套视频组织在同一条学习路径中。建议按表格顺序学习；每章正文末尾仍可查看关联源码和数据文件。",
        "",
        '<div class="course-guide-note" markdown="1">',
        "",
        "**使用方法**：先读课本定位知识点，再在线打开 Notebook 对照运行，最后用视频补充讲解。课件栏为空表示当前资源中没有对应课件。",
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
        "1. [数据分析概述与环境搭建](chapter-01.md)",
        "2. [NumPy 科学计算](chapter-02.md)",
        "3. [Pandas 数据分析](chapter-03.md)",
        "4. [数据可视化与项目实战](chapter-04.md)",
        "",
        "> 所有 Notebook、示例源码和数据集均可在网页端预览，也可下载后在本地运行。",
    ])


def main() -> None:
    pages = load_pages()
    for filename, (start, end) in CHAPTER_RANGES.items():
        update_chapter(DOCS / filename, video_block(pages, start, end))
        print(f"Updated {filename}: P{start:03d}-P{end:03d}")
    (DOCS / "index.md").write_text(build_guide(pages) + "\n", encoding="utf-8")
    print("Updated index.md course schedule")


if __name__ == "__main__":
    main()
