"""交互图审查辅助工具。

用途：
1. 扫描指定书籍的 Markdown 正文，逐条抽取全部图片引用（Markdown 语法与 HTML <img>）。
2. 为每条图片收集上下文：所属章节/小节标题、图片前后的正文段落、图题、图号、
   以及图片是否已经被包裹在 interactive-figure 容器中。
3. 输出结构化 JSON 与 Markdown 片段，供人工/AI Agent 判断“是否适合交互化”。

用法：
    python tools/audit_interactive_figures.py --book craig-introduction-to-robotics --json out.json
    python tools/audit_interactive_figures.py --all --markdown out.md
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BOOKS_ROOT = REPO_ROOT / "content" / "books"

DEFAULT_BOOKS = ["craig-introduction-to-robotics", "robot-technology-basics"]

MD_IMAGE_RE = re.compile(r"!\[(?P<alt>[^\]]*)\]\((?P<src>[^)\s]+)(?:\s+\"[^\"]*\")?\)")
HTML_IMG_RE = re.compile(r"<img\b(?P<attrs>[^>]*)>", re.I)
HTML_SRC_RE = re.compile(r"""src\s*=\s*(?P<q>['"])(?P<src>.*?)(?P=q)""", re.I)
HTML_ALT_RE = re.compile(r"""alt\s*=\s*(?P<q>['"])(?P<alt>.*?)(?P=q)""", re.I)
HTML_INTERACTIVE_SRC_RE = re.compile(
    r"""data-interactive-src\s*=\s*(?P<q>['"])(?P<src>.*?)(?P=q)""", re.I
)
HEADING_RE = re.compile(r"^(?P<hashes>#{1,6})\s+(?P<title>.+?)\s*$")
CAPTION_RE = re.compile(r"^\s*图\s*(?P<num>[0-9]+[.\-][0-9]+)\s*(?P<title>.*)$")
FIGURE_CAPTION_HTML_RE = re.compile(
    r"<p\s+class=\"figure-caption\"[^>]*>(?P<body>.*?)</p>", re.I | re.S
)


@dataclass
class FigureRecord:
    book: str
    doc_path: str
    line: int
    alt: str
    image_path: str
    heading_path: list[str] = field(default_factory=list)
    section: str = ""
    caption: str = ""
    figure_number: str = ""
    before_text: str = ""
    after_text: str = ""
    already_interactive: bool = False
    interactive_src: str = ""
    image_bytes: int = 0
    image_exists: bool = False


def strip_markup(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\$[^$]*\$", "", text)
    text = re.sub(r"[#*_`>]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def collect_captions(lines: list[str]) -> dict[int, tuple[str, str]]:
    """返回行号 -> (图号, 图题) 的映射，覆盖 Markdown 图题与 figure-caption 段落。"""
    captions: dict[int, tuple[str, str]] = {}
    for index, raw in enumerate(lines):
        match = CAPTION_RE.match(raw)
        if match:
            captions[index] = (f"图{match.group('num')}", strip_markup(match.group("title")))
    buffer = "\n".join(lines)
    for match in FIGURE_CAPTION_HTML_RE.finditer(buffer):
        body = strip_markup(match.group("body"))
        number = re.match(r"图\s*([0-9]+[.\-][0-9]+)", body)
        if number:
            line_index = buffer.count("\n", 0, match.start())
            captions[line_index] = (f"图{number.group(1)}", body)
    return captions


def nearest_caption(
    captions: dict[int, tuple[str, str]], line: int, window: int = 8
) -> tuple[str, str]:
    best: tuple[int, str, str] | None = None
    for index, (number, title) in captions.items():
        distance = abs(index - line)
        if distance > window:
            continue
        if best is None or distance < best[0]:
            best = (distance, number, title)
    if best is None:
        return "", ""
    return best[1], best[2]


def context_paragraph(
    lines: list[str], line: int, direction: int, limit: int = 6
) -> str:
    """向指定方向收集正文段落，跳过空行、图片行和图题行。"""
    chunks: list[str] = []
    index = line + direction
    steps = 0
    while 0 <= index < len(lines) and steps < limit:
        raw = lines[index].strip()
        index += direction
        if not raw:
            if chunks:
                break
            continue
        if MD_IMAGE_RE.search(raw) or HTML_IMG_RE.search(raw) or CAPTION_RE.match(raw):
            if chunks:
                break
            continue
        if raw.startswith("<") and not raw.startswith("<p") and not raw.startswith("<div"):
            continue
        chunks.append(raw)
        steps += 1
    if direction < 0:
        chunks.reverse()
    return strip_markup(" ".join(chunks))[:400]


def scan_document(book: str, docs_root: Path, path: Path) -> list[FigureRecord]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    rel = path.relative_to(docs_root).as_posix()
    captions = collect_captions(lines)

    heading_path: list[str] = []
    records: list[FigureRecord] = []
    current_h2 = ""
    active_interactive_src = ""
    interactive_depth = 0

    for index, raw in enumerate(lines):
        heading = HEADING_RE.match(raw)
        if heading:
            level = len(heading.group("hashes"))
            title = strip_markup(heading.group("title"))
            heading_path = heading_path[: level - 1] + [title]
            if level == 2:
                current_h2 = title
            continue

        interactive_src = HTML_INTERACTIVE_SRC_RE.search(raw)
        if interactive_src:
            active_interactive_src = interactive_src.group("src")
            interactive_depth = raw.count("<div") - raw.count("</div>")
        elif active_interactive_src:
            interactive_depth += raw.count("<div") - raw.count("</div>")
            if interactive_depth <= 0:
                active_interactive_src = ""

        matches: list[tuple[str, str]] = []
        for match in MD_IMAGE_RE.finditer(raw):
            matches.append((match.group("alt"), match.group("src")))
        for match in HTML_IMG_RE.finditer(raw):
            src = HTML_SRC_RE.search(match.group("attrs"))
            alt = HTML_ALT_RE.search(match.group("attrs"))
            if src:
                matches.append((alt.group("alt") if alt else "", src.group("src")))

        for alt, src in matches:
            image_path = src.split("?")[0].split("#")[0]
            resolved = (path.parent / image_path).resolve()
            try:
                resolved.relative_to(docs_root.resolve())
            except ValueError:
                continue
            number, caption_title = nearest_caption(captions, index)
            record = FigureRecord(
                book=book,
                doc_path=rel,
                line=index + 1,
                alt=strip_markup(alt),
                image_path=image_path,
                heading_path=list(heading_path),
                section=current_h2,
                caption=caption_title,
                figure_number=number,
                before_text=context_paragraph(lines, index, -1),
                after_text=context_paragraph(lines, index, 1),
                already_interactive=bool(active_interactive_src),
                interactive_src=active_interactive_src,
                image_bytes=resolved.stat().st_size if resolved.is_file() else 0,
                image_exists=resolved.is_file(),
            )
            records.append(record)
    return records


def scan_book(book: str) -> list[FigureRecord]:
    book_root = BOOKS_ROOT / book
    docs_root = book_root / "docs"
    if not docs_root.is_dir():
        raise SystemExit(f"找不到书籍目录：{docs_root}")
    records: list[FigureRecord] = []
    for path in sorted(docs_root.rglob("*.md"), key=lambda item: item.as_posix()):
        records.extend(scan_document(book, docs_root, path))
    return records


def to_markdown(records: list[FigureRecord]) -> str:
    lines = [
        "| # | 书籍 | 章节文档 | 小节 | 图号 | 图题 | 图片路径 | 行号 | alt | 已交互 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for position, record in enumerate(records, 1):
        lines.append(
            "| {pos} | {book} | {doc} | {section} | {number} | {caption} | {image} | {line} | {alt} | {flag} |".format(
                pos=position,
                book=record.book,
                doc=record.doc_path,
                section=record.section,
                number=record.figure_number,
                caption=record.caption.replace("|", "/"),
                image=record.image_path,
                line=record.line,
                alt=record.alt.replace("|", "/")[:60],
                flag="是" if record.already_interactive else "",
            )
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="交互图审查扫描工具")
    parser.add_argument("--book", action="append", default=[], help="书籍 slug，可重复")
    parser.add_argument("--all", action="store_true", help="扫描默认两本机器人教材")
    parser.add_argument("--json", type=Path, help="输出 JSON 路径")
    parser.add_argument("--markdown", type=Path, help="输出 Markdown 表格路径")
    parser.add_argument("--limit", type=int, default=0, help="仅输出前 N 条")
    args = parser.parse_args()

    books = args.book or (DEFAULT_BOOKS if args.all else DEFAULT_BOOKS)
    records: list[FigureRecord] = []
    for book in books:
        records.extend(scan_book(book))
    if args.limit:
        records = records[: args.limit]

    payload = [asdict(record) for record in records]
    if args.json:
        args.json.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"JSON 已写入 {args.json}")
    if args.markdown:
        args.markdown.write_text(to_markdown(records), encoding="utf-8")
        print(f"Markdown 已写入 {args.markdown}")

    print(f"共扫描图片 {len(records)} 条")
    for book in books:
        subset = [record for record in records if record.book == book]
        interactive = sum(1 for record in subset if record.already_interactive)
        missing = sum(1 for record in subset if not record.image_exists)
        print(f"  - {book}: {len(subset)} 条，已交互 {interactive}，图片缺失 {missing}")


if __name__ == "__main__":
    main()
