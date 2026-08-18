#!/usr/bin/env python
"""Insert the official Bilibili multipart playlist into matching Python chapters."""

from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "content" / "books" / "shangguigu-python" / "docs"
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


def update_chapter(path: Path, block: str) -> None:
    raw = path.read_bytes()
    newline = "\r\n" if b"\r\n" in raw else "\n"
    text = raw.decode("utf-8-sig").replace("\r\n", "\n")
    marker = re.compile(rf"{re.escape(START)}.*?{re.escape(END)}", re.S)
    if marker.search(text):
        updated = marker.sub(block + "\n\n", text, count=1)
        updated = updated.replace(END + "\n\n\n", END + "\n\n", 1)
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


if __name__ == "__main__":
    main()
