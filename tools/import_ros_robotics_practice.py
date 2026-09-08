from __future__ import annotations

import argparse
import re
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOKS_ROOT = ROOT / "content" / "books"
SLUG = "ros-robotics-practice"

CHAPTER_TITLES = [
    "绪论",
    "空间描述和变换",
    "操作臂运动学",
    "操作臂逆运动学",
    "雅可比：速度和静力",
    "操作臂动力学",
    "轨迹生成",
    "操作臂的控制",
    "ROS 概述与环境搭建",
    "ROS 核心概念与通信机制",
    "ROS 命令与工具",
    "ROS 编程基础",
    "机器人传感器与执行器",
    "移动机器人与仿真",
    "SLAM 与导航",
    "综合项目实战：自主巡逻机器人",
]


def read_archive(archive: Path) -> tuple[str, dict[str, bytes]]:
    with zipfile.ZipFile(archive) as bundle:
        markdown_names = [name for name in bundle.namelist() if name.lower().endswith(".md")]
        if len(markdown_names) != 1:
            raise ValueError("压缩包应包含且仅包含一个 Markdown 文件")
        markdown_text = bundle.read(markdown_names[0]).decode("utf-8-sig").replace("\r\n", "\n")
        images = {
            Path(name).name: bundle.read(name)
            for name in bundle.namelist()
            if not name.endswith("/") and "/images/" in f"/{name.replace(chr(92), '/')}"
        }
    references = re.findall(r"!\[[^]]*\]\(images[\\/]([^)]+)\)", markdown_text)
    missing = sorted(set(references) - set(images))
    if missing:
        raise ValueError(f"压缩包缺少 {len(missing)} 张引用图片")
    return markdown_text, images


def repair_fences(text: str) -> str:
    lines: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
            lines.append(line)
            continue
        if in_fence and line.strip() == "---":
            lines.extend(["```", "", "---"])
            in_fence = False
            continue
        lines.append(line)
    if in_fence:
        lines.append("```")
    return "\n".join(lines) + "\n"


def rewrite_images(text: str, prefix: str) -> str:
    return re.sub(r"\((?:\./)?images[\\/]", f"({prefix}", text)


def chapter_positions(text: str) -> list[int]:
    positions: list[int] = []
    cursor = 0
    for chapter in range(1, len(CHAPTER_TITLES) + 1):
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


def normalize_front(text: str) -> str:
    text = re.sub(r"^##\s*ROS机器人编程与机器人学导论实战\s*$", "", text, count=1, flags=re.M)
    text = re.sub(r"^##\s*第[一二三]篇.*$", "", text, flags=re.M)
    return rewrite_images(
        "# ROS 机器人编程与机器人学导论实战\n\n" + text.strip() + "\n",
        "../images/",
    )


def normalize_chapter(text: str, chapter: int, title: str) -> str:
    lines = text.strip().splitlines()
    if lines and re.match(r"^##\s*第\s*\d+\s*章", lines[0]):
        lines = lines[1:]
    output = [f"# 第{chapter}章 {title}", ""]
    numbered = re.compile(rf"^{chapter}\.(\d+)(?:\.(\d+))?(?:\.(\d+))?")
    in_fence = False
    for line in lines:
        if line.startswith("```"):
            in_fence = not in_fence
            output.append(line)
            continue
        if in_fence:
            output.append(line)
            continue
        if re.match(r"^##\s*第[一二三]篇", line):
            continue
        heading = re.match(r"^#{2,6}\s+(.+?)\s*$", line)
        if not heading:
            output.append(line)
            continue
        heading_text = heading.group(1).strip()
        match = numbered.match(heading_text)
        if match:
            depth = 2 + sum(group is not None for group in match.groups()[1:])
            output.append(f"{'#' * min(depth, 4)} {heading_text}")
        else:
            output.append(f"**{heading_text}**")
    return rewrite_images("\n".join(output).rstrip() + "\n", "../../images/")


def normalize_appendices(text: str) -> str:
    text = re.sub(r"^##\s*附录\s*$", "", text, count=1, flags=re.M)
    text = re.sub(r"^##\s+", "## ", text, flags=re.M)
    return rewrite_images("# 附录与资源索引\n\n" + text.strip() + "\n", "../images/")


def main() -> None:
    parser = argparse.ArgumentParser(description="导入 ROS 与机器人学融合实践教程")
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()
    text, images = read_archive(args.archive)
    start = re.search(r"^##\s*ROS机器人编程与机器人学导论实战\s*$", text, flags=re.M)
    if start is None:
        raise ValueError("未找到正文起始标题")
    text = repair_fences(text[start.start():])
    positions = chapter_positions(text)
    appendix_match = re.search(r"^##\s*附录\s*$", text[positions[-1]:], flags=re.M)
    if appendix_match is None:
        raise ValueError("未找到附录")
    appendix_position = positions[-1] + appendix_match.start()

    target = BOOKS_ROOT / SLUG
    docs = target / "docs"
    (docs / "00-front-matter").mkdir(parents=True, exist_ok=True)
    (docs / "chapters").mkdir(exist_ok=True)
    (docs / "appendices").mkdir(exist_ok=True)
    (docs / "images").mkdir(exist_ok=True)
    (docs / "00-front-matter" / "index.md").write_text(
        normalize_front(text[:positions[0]]), encoding="utf-8", newline="\n"
    )

    nav = [
        'site_name: "ROS 机器人编程与机器人学导论实战"',
        "docs_dir: docs",
        "nav:",
        '  - "前置内容": 00-front-matter/index.md',
        '  - "第一篇 机器人学基础理论":',
    ]
    for index, title in enumerate(CHAPTER_TITLES, start=1):
        end = positions[index] if index < len(positions) else appendix_position
        chapter_dir = docs / "chapters" / f"{index:02d}"
        chapter_dir.mkdir(exist_ok=True)
        (chapter_dir / "index.md").write_text(
            normalize_chapter(text[positions[index - 1]:end], index, title),
            encoding="utf-8",
            newline="\n",
        )
        if index == 9:
            nav.append('  - "第二篇 ROS 机器人编程实战":')
        if index == 16:
            nav.append('  - "第三篇 综合实战":')
        nav.append(f'      - "第{index}章 {title}": chapters/{index:02d}/index.md')

    (docs / "appendices" / "index.md").write_text(
        normalize_appendices(text[appendix_position:]), encoding="utf-8", newline="\n"
    )
    nav.append('  - "附录与资源索引": appendices/index.md')
    (target / "mkdocs.yml").write_text("\n".join(nav) + "\n", encoding="utf-8", newline="\n")
    for name, payload in images.items():
        (docs / "images" / name).write_bytes(payload)


if __name__ == "__main__":
    main()
