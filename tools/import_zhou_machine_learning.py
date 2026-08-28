#!/usr/bin/env python
"""Import the single-file Zhou Zhihua textbook export into the site structure."""

from __future__ import annotations

import argparse
import re
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK_ROOT = ROOT / "content" / "books" / "zhou-machine-learning"
DOCS_ROOT = BOOK_ROOT / "docs"
CONTENT_TARGETS = (
    DOCS_ROOT / "00-front-matter",
    DOCS_ROOT / "chapters",
    DOCS_ROOT / "99-back-matter",
    DOCS_ROOT / "images",
)
CHAPTER_PATHS = {
    1: "01-introduction",
    2: "02-model-evaluation-and-selection",
    3: "03-linear-models",
    4: "04-decision-trees",
    5: "05-neural-networks",
    6: "06-support-vector-machines",
    7: "07-bayesian-classifiers",
    8: "08-ensemble-learning",
    9: "09-clustering",
    10: "10-dimensionality-reduction-and-metric-learning",
    11: "11-feature-selection-and-sparse-learning",
    12: "12-computational-learning-theory",
    13: "13-semi-supervised-learning",
    14: "14-probabilistic-graphical-models",
    15: "15-rule-learning",
    16: "16-reinforcement-learning",
}
CHAPTER_RE = re.compile(r"^##\s+第\s*(\d+)\s*章\s*(.+?)\s*$", re.M)


def safe_remove_tree(path: Path) -> None:
    resolved = path.resolve()
    resolved.relative_to(DOCS_ROOT.resolve())
    if resolved == DOCS_ROOT.resolve():
        raise ValueError("拒绝删除整个 docs 目录")
    if path.exists():
        shutil.rmtree(path)


def tidy_title(number: int, raw_title: str) -> str:
    title = re.sub(r"\s+", "", raw_title) if raw_title in {"决 策 树", "聚 类"} else re.sub(r"\s+", " ", raw_title).strip()
    return f"第{number}章 {title}"


def rewrite_images(markdown_text: str, prefix: str) -> str:
    return markdown_text.replace("images/", f"{prefix}images/")


def normalize_chapter(markdown_text: str, number: int, raw_title: str) -> str:
    lines = markdown_text.strip().splitlines()
    lines[0] = f"# {tidy_title(number, raw_title)}"
    normalized: list[str] = []
    for index, line in enumerate(lines):
        if index:
            if line.startswith("#### "):
                line = "### " + line[5:]
            elif line.startswith("### "):
                line = "## " + line[4:]
            if re.match(rf"^##\s+{number}\.\d+\.\d+", line):
                line = "#" + line
        normalized.append(line.rstrip())
    result = "\n".join(normalized).strip() + "\n"
    return rewrite_images(result, "../../")


def import_book(archive_path: Path) -> dict[str, int]:
    with zipfile.ZipFile(archive_path) as archive:
        markdown_names = [name for name in archive.namelist() if name.lower().endswith(".md")]
        if len(markdown_names) != 1:
            raise ValueError(f"预期 1 个 Markdown，实际找到 {len(markdown_names)} 个")
        source = archive.read(markdown_names[0]).decode("utf-8-sig")
        chapter_matches = list(CHAPTER_RE.finditer(source))
        chapter_numbers = [int(match.group(1)) for match in chapter_matches]
        if chapter_numbers != list(range(1, 17)):
            raise ValueError(f"章节序列不完整：{chapter_numbers}")

        front_match = re.search(r"^#\s+机器学习\s*$", source, re.M)
        if front_match is None or front_match.start() < chapter_matches[-1].start():
            raise ValueError("找不到位于正文后的前置内容")
        back_match = re.search(r"^##\s+附录\s*$", source[chapter_matches[-1].start():front_match.start()], re.M)
        if back_match is None:
            raise ValueError("找不到附录起点")
        back_start = chapter_matches[-1].start() + back_match.start()

        chapters: dict[int, str] = {}
        for index, match in enumerate(chapter_matches):
            number = int(match.group(1))
            if number < 16:
                end = chapter_matches[index + 1].start()
            else:
                end = back_start
            chapters[number] = normalize_chapter(source[match.start():end], number, match.group(2))

        front = source[front_match.end():].strip() + "\n"
        back = source[back_start:front_match.start()].strip() + "\n"
        front = rewrite_images(front, "../")
        back = rewrite_images(back, "../")

        for target in CONTENT_TARGETS:
            safe_remove_tree(target)
        (DOCS_ROOT / "00-front-matter").mkdir(parents=True)
        (DOCS_ROOT / "99-back-matter").mkdir(parents=True)
        (DOCS_ROOT / "chapters").mkdir(parents=True)
        images_root = DOCS_ROOT / "images"
        images_root.mkdir(parents=True)

        (DOCS_ROOT / "00-front-matter" / "index.md").write_text(front, encoding="utf-8")
        (DOCS_ROOT / "99-back-matter" / "index.md").write_text(back, encoding="utf-8")
        for number, markdown_text in chapters.items():
            chapter_root = DOCS_ROOT / "chapters" / CHAPTER_PATHS[number]
            chapter_root.mkdir(parents=True)
            (chapter_root / "index.md").write_text(markdown_text, encoding="utf-8")

        image_entries = [
            entry for entry in archive.infolist()
            if not entry.is_dir() and entry.filename.startswith("images/")
        ]
        for entry in image_entries:
            relative = Path(entry.filename).relative_to("images")
            target = (images_root / relative).resolve()
            target.relative_to(images_root.resolve())
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.read(entry))

    referenced = set(re.findall(r"(?:\.\./)+images/([^\s)\"']+)", "\n".join([front, back, *chapters.values()])))
    extracted = {path.relative_to(images_root).as_posix() for path in images_root.rglob("*") if path.is_file()}
    missing = referenced - extracted
    if missing:
        raise ValueError(f"正文引用了未解包图片：{sorted(missing)[:5]}")
    return {
        "chapters": len(chapters),
        "markdown_files": 2 + len(chapters),
        "images": len(extracted),
        "referenced_images": len(referenced),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="导入周志华《机器学习》Markdown 导出包")
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()
    if not args.archive.is_file():
        raise FileNotFoundError(args.archive)
    result = import_book(args.archive.resolve())
    print("导入完成：" + "，".join(f"{key}={value}" for key, value in result.items()))


if __name__ == "__main__":
    main()
