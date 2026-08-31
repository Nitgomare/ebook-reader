#!/usr/bin/env python
"""Build the SCADA textbook from two Markdown exports with TeX equations."""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path
from urllib.parse import parse_qs, urlsplit


ROOT = Path(__file__).resolve().parents[1]
BOOK_ROOT = ROOT / "content" / "books" / "wind-scada-data-analysis-modeling"
CHAPTER_RE = re.compile(r"^##\s+第\s*([1-9])\s*章\s*(.+?)\s*$", re.M)
SECTION_RE = re.compile(r"^#{2,4}\s+(\d+(?:\.\d+){1,3})\s*\.?\s*(.+?)\s*$")
LOCAL_HEADING_RE = re.compile(r"^#{2,4}\s+(\d+)\s*[.)、]\s*(.+?)\s*$")
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\((images/[^)\s]+)(?:\s+\"[^\"]*\")?\)")
HTML_TABLE_RE = re.compile(r"<table\b.*?</table>", re.I | re.S)
INLINE_MATH_RE = re.compile(r"(?<!\\)\$(?!\$)(.+?)(?<!\\)\$(?!\$)", re.S)
REMOTE_CROP_RE = re.compile(
    r'<img\s+src="(https://cdn\.noedgeai\.com/[^"?]+\?[^"#]+)"\s*/?>', re.I
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("part_1", type=Path)
    parser.add_argument("part_2", type=Path)
    return parser.parse_args()


def clean_title(title: str) -> str:
    title = re.sub(r"\s+", " ", title).strip()
    return title.replace("绪 论", "绪论")


def split_source(text: str, allowed: set[int]) -> tuple[str, dict[int, str]]:
    matches = [match for match in CHAPTER_RE.finditer(text) if int(match.group(1)) in allowed]
    found = {int(match.group(1)) for match in matches}
    if found != allowed:
        raise ValueError(f"章节不完整：期望 {sorted(allowed)}，找到 {sorted(found)}")
    chapters: dict[int, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        number = int(match.group(1))
        title = clean_title(match.group(2))
        chapters[number] = f"# 第{number}章 {title}\n\n{text[match.end():end].strip()}\n"
    return text[: matches[0].start()].strip(), chapters


def clean_front_matter(text: str) -> str:
    text = re.sub(r"^#\s+.*?\n", "", text, count=1)
    text = re.sub(r"^戴巨川\s+赵前程\s+刘德顺\s+著\s*$", "", text, count=1, flags=re.M)
    text = re.split(r"^##\s+目\s*录\s*$", text, maxsplit=1, flags=re.M)[0]
    text = re.sub(r"^序\s*$", "## 序", text, count=1, flags=re.M)
    return f"# 前置内容\n\n{text.strip()}\n"


def normalize_chapter_headings(text: str, chapter: int) -> str:
    lines = text.splitlines()
    top_sections: list[int] = []
    for line in lines:
        match = SECTION_RE.match(line.strip())
        if match and match.group(1).count(".") == 1 and int(match.group(1).split(".")[0]) == chapter:
            top_sections.append(int(match.group(1).split(".")[1]))
    reference_number = max(top_sections, default=0) + 1
    current_subsection = ""
    output: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped == "## 参考文献":
            output.append(f"## {chapter}.{reference_number} 参考文献")
            continue
        section = SECTION_RE.match(stripped)
        if section and int(section.group(1).split(".")[0]) == chapter:
            number, title = section.groups()
            level = min(6, number.count(".") + 1)
            output.append(f"{'#' * level} {number} {clean_title(title)}")
            if number.count(".") >= 2:
                current_subsection = number
            continue
        local = LOCAL_HEADING_RE.match(stripped)
        if local and current_subsection:
            output.append(
                f"#### {current_subsection}.{local.group(1)} {clean_title(local.group(2))}"
            )
            continue
        output.append(line.rstrip())
    return compact_blank_lines("\n".join(output))


def rewrite_and_copy_images(
    text: str,
    *,
    source_root: Path,
    destination: Path,
    prefix: str,
    url_prefix: str,
) -> tuple[str, set[str]]:
    copied: set[str] = set()

    def replace(match: re.Match[str]) -> str:
        alt, raw_path = match.groups()
        source = source_root / Path(*Path(raw_path).parts)
        if not source.is_file():
            raise FileNotFoundError(source)
        filename = f"{prefix}-{source.name}"
        target = destination / filename
        if filename not in copied:
            shutil.copy2(source, target)
            copied.add(filename)
        return f"![{alt or source.stem}]({url_prefix}/{filename})"

    def replace_remote_crop(match: re.Match[str]) -> str:
        parsed = urlsplit(match.group(1))
        query = parse_qs(parsed.query)
        page_match = re.search(r"_(\d+)\.jpg$", Path(parsed.path).name, re.I)
        if not page_match:
            raise ValueError(f"无法识别远程裁剪图：{match.group(1)}")
        values = [query.get(key, [""])[0] for key in ("x", "y", "w", "h", "r")]
        if not all(value.isdigit() for value in values):
            raise ValueError(f"远程裁剪图参数不完整：{match.group(1)}")
        source_name = f"{page_match.group(1)}_{'_'.join(values)}.jpg"
        source = source_root / "images" / source_name
        if not source.is_file():
            raise FileNotFoundError(source)
        filename = f"{prefix}-{source_name}"
        target = destination / filename
        if filename not in copied:
            shutil.copy2(source, target)
            copied.add(filename)
        return f'<img src="{url_prefix}/{filename}" alt="图表">'

    text = REMOTE_CROP_RE.sub(replace_remote_crop, text)
    return IMAGE_RE.sub(replace, text), copied


def compact_blank_lines(text: str) -> str:
    return re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"


def normalize_html_table_math(text: str) -> str:
    """Use MathJax-native delimiters inside raw HTML, which Markdown leaves untouched."""
    return HTML_TABLE_RE.sub(
        lambda table: INLINE_MATH_RE.sub(
            lambda formula: (
                '<span class="arithmatex">\\('
                f"{formula.group(1)}"
                '\\)</span>'
            ),
            table.group(0),
        ),
        text,
    )


def write_book(part_1_path: Path, part_2_path: Path) -> None:
    if BOOK_ROOT.exists():
        raise FileExistsError(f"目标目录已存在，请先人工确认：{BOOK_ROOT}")
    part_1 = part_1_path.read_text(encoding="utf-8-sig")
    part_2 = part_2_path.read_text(encoding="utf-8-sig")
    front, chapters_1 = split_source(part_1, {1, 2, 3, 4})
    extra_front, chapters_2 = split_source(part_2, {5, 6, 7, 8, 9})
    if extra_front.strip():
        raise ValueError("第二部分在第 5 章前包含意外正文")

    docs = BOOK_ROOT / "docs"
    images = docs / "images"
    chapters_root = docs / "chapters"
    images.mkdir(parents=True)
    chapters_root.mkdir()

    front_text, front_images = rewrite_and_copy_images(
        clean_front_matter(front),
        source_root=part_1_path.parent,
        destination=images,
        prefix="p1",
        url_prefix="images",
    )
    (docs / "00-front-matter.md").write_text(
        compact_blank_lines(normalize_html_table_math(front_text)), encoding="utf-8"
    )

    titles: dict[int, str] = {}
    copied = set(front_images)
    all_chapters = {**chapters_1, **chapters_2}
    for number, chapter_text in sorted(all_chapters.items()):
        title_match = re.match(rf"^# 第{number}章\s+(.+)$", chapter_text.splitlines()[0])
        if not title_match:
            raise ValueError(f"第 {number} 章标题无效")
        titles[number] = title_match.group(1).strip()
        normalized = normalize_chapter_headings(chapter_text, number)
        rewritten, chapter_images = rewrite_and_copy_images(
            normalized,
            source_root=part_1_path.parent if number <= 4 else part_2_path.parent,
            destination=images,
            prefix="p1" if number <= 4 else "p2",
            url_prefix="../../images",
        )
        copied.update(chapter_images)
        chapter_dir = chapters_root / f"{number:02d}"
        chapter_dir.mkdir()
        (chapter_dir / "index.md").write_text(
            compact_blank_lines(normalize_html_table_math(rewritten)), encoding="utf-8"
        )

    nav = [
        "site_name: 风电SCADA数据分析与智能建模",
        "",
        "docs_dir: docs",
        "",
        "nav:",
        '  - "前置内容": 00-front-matter.md',
    ]
    nav.extend(
        f'  - "第{number}章 {titles[number]}": chapters/{number:02d}/index.md'
        for number in sorted(titles)
    )
    nav.extend([
        "", "markdown_extensions:", "  - tables", "  - attr_list", "  - md_in_html",
        "  - pymdownx.arithmatex:", "      generic: true", "  - toc:",
        '      toc_depth: "2-4"', "",
    ])
    (BOOK_ROOT / "mkdocs.yml").write_text("\n".join(nav), encoding="utf-8")
    total = sum(path.stat().st_size for path in images.iterdir())
    print(f"Converted 9 chapters and front matter; {len(copied)} figures, {total / 1024 / 1024:.1f} MB")


def main() -> None:
    args = parse_args()
    for source in (args.part_1, args.part_2):
        if not source.is_file():
            raise FileNotFoundError(source)
    write_book(args.part_1, args.part_2)


if __name__ == "__main__":
    main()
