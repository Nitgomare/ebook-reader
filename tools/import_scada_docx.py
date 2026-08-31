#!/usr/bin/env python
"""Convert the two reviewed SCADA DOCX volumes into one web textbook."""

from __future__ import annotations

import argparse
import html
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
BOOK_ROOT = ROOT / "content" / "books" / "wind-scada-data-analysis-modeling"
VECTOR_EXTENSIONS = {".wmf", ".emf"}
CHAPTER_RE = re.compile(r"^(?:<span[^>]*></span>)?第([1-9])章\s*(.+?)\s*$")
SECTION_RE = re.compile(r"^(\d+(?:\.\d+){1,3})\s+(.+?)\s*$")
MARKDOWN_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HTML_IMAGE_RE = re.compile(r"<img\s+([^>]*?)src=\"([^\"]+)\"([^>]*)>", re.I)
ANCHOR_RE = re.compile(r"<span\s+id=\"[^\"]+\"\s+class=\"anchor\"></span>")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("part_1", type=Path)
    parser.add_argument("part_2", type=Path)
    parser.add_argument("--pandoc", type=Path, default=Path("pandoc"))
    return parser.parse_args()


def run_pandoc(source: Path, part: int, work: Path, pandoc: Path) -> tuple[str, Path]:
    markdown = work / f"part-{part}.md"
    media_dir = work / f"part-{part}-media"
    subprocess.run(
        [
            str(pandoc), str(source), "--from=docx", "--to=gfm+tex_math_dollars",
            "--wrap=none", "--markdown-headings=atx", f"--extract-media={media_dir}",
            f"--output={markdown}",
        ],
        check=True,
    )
    return markdown.read_text(encoding="utf-8"), media_dir


def find_chapters(text: str, allowed: set[int]) -> dict[int, list[str]]:
    lines = text.splitlines()
    starts: list[tuple[int, int, str]] = []
    for index, line in enumerate(lines):
        match = CHAPTER_RE.match(line.strip())
        if match and int(match.group(1)) in allowed:
            starts.append((index, int(match.group(1)), match.group(2).strip()))
    result: dict[int, list[str]] = {}
    for position, (start, number, title) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        result[number] = [f"# 第{number}章 {title}", *lines[start + 1 : end]]
    missing = allowed - result.keys()
    if missing:
        raise ValueError(f"未找到章节：{sorted(missing)}")
    return result


def front_matter(text: str) -> list[str]:
    lines = text.splitlines()
    chapter_start = next(index for index, line in enumerate(lines) if CHAPTER_RE.match(line.strip()))
    toc_start = next((index for index, line in enumerate(lines[:chapter_start]) if re.fullmatch(r"\*\*目\s*录\*\*", line.strip())), chapter_start)
    body = lines[:toc_start]
    while body and not body[-1].strip():
        body.pop()
    # Title, English title and author are shown on the course resource page.
    body = body[3:] if len(body) >= 3 else body
    converted = ["# 前置内容"]
    for line in body:
        stripped = line.strip()
        heading = re.fullmatch(r"\*\*\s*(内容简介|序|前\s*言|符号表)\s*\*\*", stripped)
        converted.append(f"## {re.sub(r'\s+', '', heading.group(1))}" if heading else line)
    return converted


class MediaConverter:
    def __init__(self, destination: Path, sources: dict[int, Path]) -> None:
        self.destination = destination
        self.destination.mkdir(parents=True, exist_ok=True)
        self.sources = sources
        self.cache: dict[tuple[int, str], tuple[str, int, int, bool]] = {}

    def convert(self, part: int, raw_path: str) -> tuple[str, int, int, bool]:
        key = (part, raw_path)
        if key in self.cache:
            return self.cache[key]
        relative = raw_path.replace("\\", "/")
        marker = f"part-{part}-media/"
        if marker in relative:
            relative = relative.split(marker, 1)[1]
        source = self.sources[part] / Path(*Path(relative).parts)
        if not source.is_file():
            raise FileNotFoundError(f"找不到媒体文件：{source}")
        extension = source.suffix.lower()
        stem = re.sub(r"[^a-zA-Z0-9_-]+", "-", source.stem)
        vector = extension in VECTOR_EXTENSIONS
        output_extension = ".png" if vector else extension
        filename = f"p{part}-{stem}{output_extension}"
        target = self.destination / filename
        width = height = 0
        if vector:
            with Image.open(source) as image:
                width, height = image.size
                dpi = max(96, min(192, int(96 * 2200 / max(width, height, 1))))
                image.load(dpi=dpi)
                if max(image.size) > 2400:
                    image.thumbnail((2400, 2400), Image.Resampling.LANCZOS)
                if image.mode not in {"RGB", "RGBA"}:
                    image = image.convert("RGBA")
                image.save(target, "PNG", optimize=True, compress_level=9)
        elif extension == ".png":
            with Image.open(source) as image:
                width, height = image.size
                if max(image.size) > 2400:
                    image.thumbnail((2400, 2400), Image.Resampling.LANCZOS)
                image.save(target, "PNG", optimize=True, compress_level=9)
        else:
            shutil.copy2(source, target)
            try:
                with Image.open(source) as image:
                    width, height = image.size
            except Exception:
                pass
        result = (f"images/{filename}", width, height, vector)
        self.cache[key] = result
        return result


def image_class(width: int, height: int, standalone: bool) -> str:
    if width <= 420 and height <= 100:
        return "formula-display" if standalone else "formula-inline"
    return "content-image"


def rewrite_images(
    lines: list[str],
    part: int,
    converter: MediaConverter,
    *,
    url_prefix: str = "images",
) -> list[str]:
    output: list[str] = []
    for line in lines:
        original = line.strip()
        matches = list(MARKDOWN_IMAGE_RE.finditer(line))
        standalone = bool(matches) and re.fullmatch(
            rf"(?:{MARKDOWN_IMAGE_RE.pattern})(?:\s+(?:\([0-9.]+\)|（[0-9.]+）))?",
            original,
        ) is not None
        large_images = 0

        def markdown_replacement(match: re.Match[str]) -> str:
            nonlocal large_images
            alt, raw_path = match.group(1), match.group(2)
            new_path, width, height, vector = converter.convert(part, raw_path)
            new_path = f"{url_prefix}/{Path(new_path).name}"
            if not vector:
                return f"![{alt}]({new_path})"
            css_class = image_class(width, height, standalone)
            if css_class == "content-image":
                large_images += 1
            return (
                f'<img class="{css_class}" src="{new_path}" '
                f'style="width:{max(width, 1)}px" alt="{html.escape(alt, quote=True)}">'
            )

        def html_replacement(match: re.Match[str]) -> str:
            before, raw_path, after = match.groups()
            new_path, width, height, vector = converter.convert(part, raw_path)
            new_path = f"{url_prefix}/{Path(new_path).name}"
            attrs = f"{before}{after}".strip()
            if vector and "class=" not in attrs:
                attrs = f'class="{image_class(width, height, False)}" {attrs}'.strip()
            if vector and "style=" not in attrs:
                attrs = f'{attrs} style="width:{max(width, 1)}px"'.strip()
            return f'<img {attrs} src="{new_path}">'

        line = HTML_IMAGE_RE.sub(html_replacement, line)
        line = MARKDOWN_IMAGE_RE.sub(markdown_replacement, line)
        if large_images > 1 and original.count("![](") > 1:
            line = f'<div class="image-row">{line}</div>'
        output.append(line)
    return output


def normalize_headings(lines: list[str], chapter: int | None) -> list[str]:
    output: list[str] = []
    section_numbers: list[int] = []
    for source_line in lines:
        clean_line = ANCHOR_RE.sub("", source_line).strip()
        match = SECTION_RE.match(clean_line)
        if (
            match and chapter is not None and match.group(1).count(".") == 1
            and int(match.group(1).split(".")[0]) == chapter
        ):
            section_numbers.append(int(match.group(1).split(".")[1]))
    reference_number = max(section_numbers, default=0) + 1
    for line in lines:
        line = ANCHOR_RE.sub("", line).strip() if "class=\"anchor\"" in line else line.rstrip()
        stripped = line.strip()
        if stripped == "参考文献":
            output.append(f"## {chapter}.{reference_number} 参考文献" if chapter else "## 参考文献")
            continue
        match = SECTION_RE.match(stripped)
        if match and chapter is not None and int(match.group(1).split(".")[0]) == chapter and len(stripped) < 180:
            level = min(6, match.group(1).count(".") + 1)
            output.append(f"{'#' * level} {match.group(1)} {match.group(2)}")
            continue
        output.append(line)
    return output


def compact_blank_lines(lines: list[str]) -> str:
    output: list[str] = []
    blank = False
    for line in lines:
        is_blank = not line.strip()
        if is_blank and blank:
            continue
        output.append(line)
        blank = is_blank
    return "\n".join(output).strip() + "\n"


def write_book(part_1: str, media_1: Path, part_2: str, media_2: Path) -> None:
    if BOOK_ROOT.exists():
        raise FileExistsError(f"目标目录已存在，请先人工确认：{BOOK_ROOT}")
    docs = BOOK_ROOT / "docs"
    images = docs / "images"
    chapters = docs / "chapters"
    chapters.mkdir(parents=True)
    converter = MediaConverter(images, {1: media_1, 2: media_2})

    front = normalize_headings(front_matter(part_1), None)
    (docs / "00-front-matter.md").write_text(
        compact_blank_lines(rewrite_images(front, 1, converter)), encoding="utf-8"
    )

    all_chapters = {**find_chapters(part_1, {1, 2, 3, 4}), **find_chapters(part_2, {5, 6, 7, 8, 9})}
    titles: dict[int, str] = {}
    for number, lines in sorted(all_chapters.items()):
        titles[number] = lines[0].removeprefix(f"# 第{number}章 ").strip()
        normalized = normalize_headings(lines, number)
        rewritten = rewrite_images(
            normalized,
            1 if number <= 4 else 2,
            converter,
            url_prefix="../../images",
        )
        chapter_dir = chapters / f"{number:02d}"
        chapter_dir.mkdir()
        (chapter_dir / "index.md").write_text(compact_blank_lines(rewritten), encoding="utf-8")

    nav = ["site_name: 风电SCADA数据分析与智能建模", "", "docs_dir: docs", "", "nav:", '  - "前置内容": 00-front-matter.md']
    nav.extend(f'  - "第{number}章 {titles[number]}": chapters/{number:02d}/index.md' for number in sorted(titles))
    nav.extend([
        "", "markdown_extensions:", "  - tables", "  - attr_list", "  - md_in_html",
        "  - pymdownx.arithmatex:", "      generic: true", "  - toc:", "      toc_depth: \"2-4\"", "",
    ])
    (BOOK_ROOT / "mkdocs.yml").write_text("\n".join(nav), encoding="utf-8")
    total = sum(path.stat().st_size for path in images.iterdir())
    print(f"Converted 9 chapters and front matter; {len(converter.cache)} media files, {total / 1024 / 1024:.1f} MB")


def main() -> None:
    args = parse_args()
    for source in (args.part_1, args.part_2):
        if not source.is_file():
            raise FileNotFoundError(source)
    with tempfile.TemporaryDirectory(prefix="scada-docx-") as temporary:
        work = Path(temporary)
        part_1, media_1 = run_pandoc(args.part_1, 1, work, args.pandoc)
        part_2, media_2 = run_pandoc(args.part_2, 2, work, args.pandoc)
        write_book(part_1, media_1, part_2, media_2)


if __name__ == "__main__":
    main()
