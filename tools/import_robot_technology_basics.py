from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path


BOOKS_ROOT = Path(__file__).resolve().parents[1] / "content" / "books"
SLUG = "robot-technology-basics"


def rewrite_image_paths(text: str, prefix: str) -> str:
    text = re.sub(r"\((?:\./)?images[\\/]", f"({prefix}", text)
    return re.sub(r'(?P<attr>src=["\'])(?:\./)?images[\\/]', rf'\g<attr>{prefix}', text)


def normalize_chapter_heading(text: str, number: int, title: str) -> str:
    lines = text.strip().splitlines()
    if lines and re.match(r"^#\s+第\s*\d+\s*章", lines[0]):
        lines = lines[1:]
    body = "\n".join(lines).strip()
    return f"# 第{number}章 {title}\n\n{body}\n"


def import_book(source_root: Path) -> None:
    source_markdown = source_root / "大纲及内容修正版.md"
    source_images = source_root / "images"
    if not source_markdown.is_file():
        raise FileNotFoundError(source_markdown)
    if not source_images.is_dir():
        raise FileNotFoundError(source_images)

    text = source_markdown.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    chapter_matches = list(
        re.finditer(r"^#\s+第\s*(\d+)\s*章\s+(.+?)\s*$", text, flags=re.M)
    )
    chapter_numbers = [int(match.group(1)) for match in chapter_matches]
    if chapter_numbers != list(range(1, 11)):
        raise ValueError(f"章节识别异常：{chapter_numbers}")

    appendix_match = re.search(r"^#\s+附录\s+机器人课程实验示例\s*$", text, flags=re.M)
    references_match = re.search(r"^#\s+参考文献\s*$", text, flags=re.M)
    if appendix_match is None or references_match is None:
        raise ValueError("未找到附录或参考文献边界")

    target = BOOKS_ROOT / SLUG
    docs = target / "docs"
    if target.exists():
        shutil.rmtree(target)
    (docs / "00-front-matter").mkdir(parents=True)
    (docs / "chapters").mkdir()
    (docs / "appendices").mkdir()
    shutil.copytree(source_images, docs / "images")

    front = rewrite_image_paths(text[: chapter_matches[0].start()].strip(), "../images/")
    (docs / "00-front-matter" / "index.md").write_text(
        front + "\n", encoding="utf-8", newline="\n"
    )

    nav = [
        'site_name: "机器人技术基础（第三版）"',
        "docs_dir: docs",
        "nav:",
        '  - "前置内容": 00-front-matter/index.md',
    ]
    for index, match in enumerate(chapter_matches):
        number = int(match.group(1))
        title = match.group(2).strip()
        end = (
            chapter_matches[index + 1].start()
            if index + 1 < len(chapter_matches)
            else appendix_match.start()
        )
        chapter = normalize_chapter_heading(text[match.start() : end], number, title)
        chapter = rewrite_image_paths(chapter, "../../images/")
        chapter_dir = docs / "chapters" / f"{number:02d}"
        chapter_dir.mkdir()
        (chapter_dir / "index.md").write_text(
            chapter, encoding="utf-8", newline="\n"
        )
        nav.append(f'  - "第{number}章 {title}": chapters/{number:02d}/index.md')

    appendix = rewrite_image_paths(
        text[appendix_match.start() : references_match.start()].strip(), "../images/"
    )
    references = rewrite_image_paths(text[references_match.start() :].strip(), "../images/")
    appendix_text = f"{appendix}\n\n{references}\n"
    (docs / "appendices" / "index.md").write_text(
        appendix_text, encoding="utf-8", newline="\n"
    )
    nav.append('  - "附录与参考资料": appendices/index.md')
    (target / "mkdocs.yml").write_text(
        "\n".join(nav) + "\n", encoding="utf-8", newline="\n"
    )

    print(f"已导入：{target}")
    print(f"章节：{len(chapter_matches)}；图片：{len(list((docs / 'images').iterdir()))}")


def main() -> None:
    parser = argparse.ArgumentParser(description="导入《机器人技术基础（第三版）》")
    parser.add_argument("source_root", type=Path)
    args = parser.parse_args()
    import_book(args.source_root.resolve())


if __name__ == "__main__":
    main()
