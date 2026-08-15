#!/usr/bin/env python
"""Convert the supplied legacy EPUB into this reader's Markdown book layout."""

from __future__ import annotations

import argparse
import html
import json
import posixpath
import re
import shutil
import textwrap
import zipfile
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

import yaml


BOOK_TITLE = "Python从入门到精通"
BOOK_SLUG = "python-beginner-to-master"
SOURCE_FILES = [
    ("OEBPS/text00001.html", "版权信息", "copyright.md", "导读"),
    ("OEBPS/text00002.html", "内容简介", "introduction.md", "导读"),
    ("OEBPS/text00003.html", "前言", "preface.md", "导读"),
    *[
        (f"OEBPS/text{index + 5:05d}.html", f"第{index}章", f"chapter-{index:02d}.md", "第1篇 基础知识")
        for index in range(1, 8)
    ],
    *[
        (f"OEBPS/text{index + 6:05d}.html", f"第{index}章", f"chapter-{index:02d}.md", "第2篇 进阶提高")
        for index in range(8, 15)
    ],
    *[
        (f"OEBPS/text{index + 7:05d}.html", f"第{index}章", f"chapter-{index:02d}.md", "第3篇 高级应用")
        for index in range(15, 22)
    ],
    ("OEBPS/text00030.html", "第22章", "chapter-22.md", "第4篇 项目实战"),
    ("OEBPS/text00031.html", "附录CD", "appendix.md", "附录"),
]
FILE_MAP = {PurePosixPath(source).name: target for source, _, target, _ in SOURCE_FILES}
BLOCK_TAGS = {"div", "p", "section", "article", "blockquote"}
SKIP_TAGS = {"head", "style", "script"}


def decode_legacy_text(raw: bytes) -> str:
    for encoding in ("utf-8", "gb18030"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("gb18030", errors="replace")


def clean_title(value: str) -> str:
    value = re.sub(r"<[^>]+>", "", value)
    value = html.unescape(value)
    return re.sub(r"\s+", " ", value).strip()


def title_from_html(source: str, fallback: str) -> str:
    match = re.search(r"<h1\b[^>]*>(.*?)</h1>", source, re.I | re.S)
    return clean_title(match.group(1)) if match else fallback


def escape_markdown_text(value: str) -> str:
    value = value.replace("\\", "\\\\")
    value = value.replace("<", "&lt;").replace(">", "&gt;")
    return re.sub(r"([*_\[\]|])", r"\\\1", value)


class MarkdownConverter(HTMLParser):
    """Convert the small, known XHTML vocabulary used by this EPUB."""

    def __init__(self, source_name: str, archive_names: set[str]) -> None:
        super().__init__(convert_charrefs=True)
        self.source_name = source_name
        self.archive_names = archive_names
        self.parts: list[str] = []
        self.used_assets: set[str] = set()
        self.skip_depth = 0
        self.in_pre = False
        self.pre_parts: list[str] = []
        self.heading_depth = 0
        self.link_stack: list[str | None] = []
        self.caption_stack: list[bool] = []

    def append(self, value: str) -> None:
        if value:
            self.parts.append(value)

    def newline(self) -> None:
        self.append("\n\n")

    def resolve_asset(self, raw_url: str) -> tuple[str, str] | None:
        parsed = urlsplit(html.unescape(raw_url))
        if parsed.scheme or parsed.netloc or not parsed.path:
            return None
        source_dir = posixpath.dirname(self.source_name)
        archive_path = posixpath.normpath(posixpath.join(source_dir, unquote(parsed.path)))
        if archive_path.startswith("../") or archive_path not in self.archive_names:
            raise FileNotFoundError(f"图片资源不存在或路径越界：{raw_url}（{self.source_name}）")
        filename = PurePosixPath(archive_path).name
        self.used_assets.add(archive_path)
        return archive_path, f"assets/images/{filename}"

    def rewrite_link(self, raw_url: str) -> str | None:
        parsed = urlsplit(html.unescape(raw_url))
        if parsed.scheme or parsed.netloc:
            return raw_url
        if not parsed.path:
            return f"#{parsed.fragment}" if parsed.fragment else None
        target = FILE_MAP.get(PurePosixPath(unquote(parsed.path)).name)
        if not target:
            return None
        return f"{target}#{parsed.fragment}" if parsed.fragment else target

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        attributes = {key.lower(): value or "" for key, value in attrs}
        if tag in SKIP_TAGS:
            self.skip_depth += 1
            return
        if self.skip_depth:
            return
        if tag == "pre":
            self.newline()
            self.in_pre = True
            self.pre_parts = []
            return
        if self.in_pre:
            if tag == "br":
                self.pre_parts.append("\n")
            return
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            source_level = int(tag[1])
            markdown_level = {1: 1, 2: 2, 3: 2, 4: 3, 5: 4, 6: 5}[source_level]
            self.newline()
            anchor = attributes.get("id")
            if anchor:
                self.append(f'<a id="{html.escape(anchor, quote=True)}"></a>\n\n')
            self.append("#" * markdown_level + " ")
            self.heading_depth += 1
        elif tag == "p":
            self.newline()
            classes = set(attributes.get("class", "").split())
            is_caption = bool(classes & {"tuti", "book-caption", "caption"})
            self.caption_stack.append(is_caption)
            if is_caption:
                self.append("*")
        elif tag == "div":
            self.newline()
        elif tag in {"b", "strong"}:
            self.append("**")
        elif tag in {"i", "em"}:
            self.append("*")
        elif tag == "sup":
            self.append("<sup>")
        elif tag == "sub":
            self.append("<sub>")
        elif tag == "br":
            self.append(" " if self.heading_depth else "  \n")
        elif tag == "hr":
            self.append("\n\n---\n\n")
        elif tag == "img":
            resolved = self.resolve_asset(attributes.get("src", ""))
            if resolved:
                _, markdown_path = resolved
                alt = clean_title(attributes.get("alt", "")) or "插图"
                self.append(f"\n\n![{escape_markdown_text(alt)}]({markdown_path})\n\n")
        elif tag == "a":
            anchor = attributes.get("id") or attributes.get("name")
            if anchor:
                self.append(f'<a id="{html.escape(anchor, quote=True)}"></a>')
            target = self.rewrite_link(attributes.get("href", "")) if attributes.get("href") else None
            self.link_stack.append(target)
            if target:
                self.append("[")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in SKIP_TAGS:
            if self.skip_depth:
                self.skip_depth -= 1
            return
        if self.skip_depth:
            return
        if tag == "pre" and self.in_pre:
            code = textwrap.dedent("".join(self.pre_parts)).strip("\r\n")
            self.append(f"```python\n{code}\n```\n\n")
            self.in_pre = False
            self.pre_parts = []
            return
        if self.in_pre:
            return
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.heading_depth = max(0, self.heading_depth - 1)
            self.newline()
        elif tag == "p":
            is_caption = self.caption_stack.pop() if self.caption_stack else False
            if is_caption:
                self.append("*")
            self.newline()
        elif tag in BLOCK_TAGS:
            self.newline()
        elif tag in {"b", "strong"}:
            self.append("**")
        elif tag in {"i", "em"}:
            self.append("*")
        elif tag == "sup":
            self.append("</sup>")
        elif tag == "sub":
            self.append("</sub>")
        elif tag == "a":
            target = self.link_stack.pop() if self.link_stack else None
            if target:
                self.append(f"]({target})")

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        if self.in_pre:
            self.pre_parts.append(data)
            return
        normalized = re.sub(r"\s+", " ", data)
        if normalized.strip():
            self.append(escape_markdown_text(normalized))

    def markdown(self) -> str:
        value = "".join(self.parts)
        lines = [line.rstrip() for line in value.splitlines()]
        value = "\n".join(lines)
        value = re.sub(r"[ \t]+\n", "\n", value)
        value = re.sub(r"\n{3,}", "\n\n", value)
        return value.strip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="将指定 EPUB 转换为电子书阅读器的 Markdown 源文件")
    parser.add_argument("epub", type=Path)
    parser.add_argument("target", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    epub_path = args.epub.resolve()
    target = args.target.resolve()
    if target.exists():
        raise FileExistsError(f"目标目录已存在，为避免覆盖已停止：{target}")

    staging = target.with_name(f"{target.name}.importing")
    if staging.exists():
        raise FileExistsError(f"临时目录已存在，请先检查：{staging}")
    docs_root = staging / "docs"
    image_root = docs_root / "assets" / "images"
    image_root.mkdir(parents=True)

    report: dict[str, object] = {
        "source": epub_path.name,
        "documents": 0,
        "images": 0,
        "codeBlocks": 0,
        "mathMlElements": 0,
        "brokenLinks": [],
    }

    try:
        with zipfile.ZipFile(epub_path) as archive:
            archive_names = set(archive.namelist())
            unsafe = [name for name in archive_names if PurePosixPath(name).is_absolute() or ".." in PurePosixPath(name).parts]
            if unsafe:
                raise ValueError(f"EPUB 包含不安全路径：{unsafe[:3]}")

            nav_groups: dict[str, list[dict[str, str]]] = {}
            used_assets: set[str] = set()
            for source_name, fallback_title, output_name, group in SOURCE_FILES:
                if source_name not in archive_names:
                    raise FileNotFoundError(f"EPUB 缺少章节：{source_name}")
                source = decode_legacy_text(archive.read(source_name))
                body_match = re.search(r"<body\b[^>]*>(.*?)</body>", source, re.I | re.S)
                body = body_match.group(1) if body_match else source
                converter = MarkdownConverter(source_name, archive_names)
                converter.feed(body)
                converter.close()
                markdown = converter.markdown()
                title = title_from_html(source, fallback_title)
                (docs_root / output_name).write_text(markdown, encoding="utf-8", newline="\n")
                used_assets.update(converter.used_assets)
                nav_groups.setdefault(group, []).append({title: output_name})
                report["documents"] = int(report["documents"]) + 1
                report["codeBlocks"] = int(report["codeBlocks"]) + markdown.count("```python")
                report["mathMlElements"] = int(report["mathMlElements"]) + len(
                    re.findall(r"<(?:\w+:)?math\b", source, re.I)
                )

            cover_source = "OEBPS/Image00000.jpg"
            if cover_source not in archive_names:
                raise FileNotFoundError("EPUB 缺少封面 Image00000.jpg")
            used_assets.add(cover_source)

            for archive_path in sorted(used_assets):
                filename = PurePosixPath(archive_path).name
                destination = image_root / filename
                if destination.exists() and destination.read_bytes() != archive.read(archive_path):
                    raise ValueError(f"图片文件名冲突：{filename}")
                destination.write_bytes(archive.read(archive_path))

            report["images"] = len(used_assets)
            mkdocs = {
                "site_name": BOOK_TITLE,
                "docs_dir": "docs",
                "nav": [{group: items} for group, items in nav_groups.items()],
            }
            (staging / "mkdocs.yml").write_text(
                yaml.safe_dump(mkdocs, allow_unicode=True, sort_keys=False, width=120),
                encoding="utf-8",
                newline="\n",
            )
            (staging / "import-report.json").write_text(
                json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
                newline="\n",
            )

        target.parent.mkdir(parents=True, exist_ok=True)
        staging.replace(target)
    except Exception:
        if staging.exists():
            shutil.rmtree(staging)
        raise

    print(json.dumps(report, ensure_ascii=False))
    print(f"Created: {target}")


if __name__ == "__main__":
    main()
