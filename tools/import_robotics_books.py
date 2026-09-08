from __future__ import annotations

import argparse
import re
import shutil
import zipfile
from pathlib import Path


BOOKS_ROOT = Path(__file__).resolve().parents[1] / "content" / "books"

ROS_TITLES = [
    "机器人软件平台",
    "机器人操作系统 ROS",
    "搭建 ROS 开发环境",
    "ROS 的重要概念",
    "ROS 命令",
    "ROS 工具",
    "ROS 编程基础",
    "机器人、传感器和电机",
    "嵌入式系统",
    "移动机器人",
    "SLAM 和导航",
    "服务机器人",
    "机械手臂",
]

CRAIG_TITLES = [
    "绪论",
    "空间描述和变换",
    "操作臂运动学",
    "操作臂逆运动学",
    "速度和静力",
    "操作臂动力学",
    "轨迹的生成",
    "操作臂的机械设计",
    "操作臂的线性控制",
    "操作臂的非线性控制",
    "操作臂的力控制",
    "机器人编程语言及编程系统",
    "离线编程系统",
]


def read_archive(archive: Path) -> tuple[str, dict[str, bytes]]:
    with zipfile.ZipFile(archive) as bundle:
        markdown_names = [name for name in bundle.namelist() if name.lower().endswith(".md")]
        if len(markdown_names) != 1:
            raise ValueError(f"{archive.name} 应包含且仅包含一个 Markdown 文件")
        markdown_text = bundle.read(markdown_names[0]).decode("utf-8-sig")
        images = {
            Path(name).name: bundle.read(name)
            for name in bundle.namelist()
            if not name.endswith("/") and "/images/" in f"/{name.replace(chr(92), '/')}"
        }
    return markdown_text.replace("\r\n", "\n"), images


CDN_CROP_RE = re.compile(
    r"https://cdn\.noedgeai\.com/[^\s\"')]+_(?P<page>\d+)\.jpg"
    r"\?x=(?P<x>\d+)&y=(?P<y>\d+)&w=(?P<w>\d+)&h=(?P<h>\d+)&r=(?P<r>\d+)"
)


def rewrite_image_paths(text: str, prefix: str) -> str:
    text = re.sub(r"\((?:\./)?images[\\/]", f"({prefix}", text)
    return CDN_CROP_RE.sub(
        lambda match: (
            f"{prefix}{match.group('page')}_{match.group('x')}_{match.group('y')}_"
            f"{match.group('w')}_{match.group('h')}_{match.group('r')}.jpg"
        ),
        text,
    )


def normalize_front(text: str, title: str) -> str:
    body = re.sub(r"^#\s+", "## ", text.strip(), flags=re.M)
    return rewrite_image_paths(f"# {title}\n\n{body}\n", "../images/")


def normalize_chapter(text: str, chapter: int, title: str) -> str:
    lines = text.strip().splitlines()
    if lines and re.match(r"^##\s*第\s*\d+\s*章", lines[0]):
        lines = lines[1:]
    normalized: list[str] = [f"# 第{chapter}章 {title}", ""]
    numbered = re.compile(rf"^{chapter}\.(\d+)(?:\.(\d+))?(?:\.(\d+))?")
    for line in lines:
        heading = re.match(r"^#{2,6}\s+(.+?)\s*$", line)
        if not heading:
            normalized.append(line)
            continue
        heading_text = heading.group(1).strip()
        match = numbered.match(heading_text)
        if match:
            depth = 2 + sum(group is not None for group in match.groups()[1:])
            normalized.append(f"{'#' * min(depth, 4)} {heading_text}")
        else:
            normalized.append(f"**{heading_text}**")
    return rewrite_image_paths("\n".join(normalized).rstrip() + "\n", "../../images/")


def chapter_positions(text: str, count: int) -> list[int]:
    positions: list[int] = []
    cursor = 0
    for chapter in range(1, count + 1):
        match = re.search(
            rf"^##\s*第\s*{chapter}\s*章(?:\s|$).*?$",
            text[cursor:],
            flags=re.M,
        )
        if match is None:
            raise ValueError(f"未找到第 {chapter} 章")
        positions.append(cursor + match.start())
        cursor += match.end()
    return positions


def write_book(
    archive: Path,
    slug: str,
    site_name: str,
    front_title: str,
    chapter_titles: list[str],
    include_appendices: bool = False,
) -> None:
    text, images = read_archive(archive)
    target = BOOKS_ROOT / slug
    docs = target / "docs"
    (docs / "00-front-matter").mkdir(parents=True, exist_ok=True)
    (docs / "chapters").mkdir(exist_ok=True)
    (docs / "images").mkdir(exist_ok=True)

    positions = chapter_positions(text, len(chapter_titles))
    appendix_position = len(text)
    if include_appendices:
        appendix_match = re.search(r"^##\s*附录A(?:\s|$)", text[positions[-1]:], flags=re.M)
        if appendix_match is None:
            raise ValueError("未找到附录 A")
        appendix_position = positions[-1] + appendix_match.start()

    (docs / "00-front-matter" / "index.md").write_text(
        normalize_front(text[:positions[0]], front_title), encoding="utf-8", newline="\n"
    )
    nav_lines = [f'site_name: "{site_name}"', "docs_dir: docs", "nav:", f'  - "前置内容": 00-front-matter/index.md']
    for index, title in enumerate(chapter_titles, start=1):
        end = positions[index] if index < len(positions) else appendix_position
        chapter_dir = docs / "chapters" / f"{index:02d}"
        chapter_dir.mkdir(exist_ok=True)
        chapter_label = f"第{index}章 {title}"
        (chapter_dir / "index.md").write_text(
            normalize_chapter(text[positions[index - 1]:end], index, title),
            encoding="utf-8",
            newline="\n",
        )
        nav_lines.append(f'  - "{chapter_label}": chapters/{index:02d}/index.md')

    if include_appendices:
        appendix_dir = docs / "appendices"
        appendix_dir.mkdir(exist_ok=True)
        appendix_body = rewrite_image_paths(text[appendix_position:].strip(), "../images/")
        appendix_body = re.sub(r"^##\s+", "## ", appendix_body, flags=re.M)
        (appendix_dir / "index.md").write_text(
            f"# 附录、习题答案与索引\n\n{appendix_body}\n",
            encoding="utf-8",
            newline="\n",
        )
        nav_lines.append('  - "附录、习题答案与索引": appendices/index.md')

    (target / "mkdocs.yml").write_text("\n".join(nav_lines) + "\n", encoding="utf-8", newline="\n")
    for name, payload in images.items():
        (docs / "images" / name).write_bytes(payload)


def main() -> None:
    parser = argparse.ArgumentParser(description="导入并按章节拆分两本机器人教材")
    parser.add_argument("ros_archive", type=Path)
    parser.add_argument("craig_archive", type=Path)
    args = parser.parse_args()
    write_book(
        args.ros_archive,
        "ros-robot-programming",
        "ROS 机器人编程",
        "前置内容",
        ROS_TITLES,
    )
    write_book(
        args.craig_archive,
        "craig-introduction-to-robotics",
        "机器人学导论（第3版）",
        "前置内容",
        CRAIG_TITLES,
        include_appendices=True,
    )


if __name__ == "__main__":
    main()
