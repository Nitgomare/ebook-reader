"""Import the supplied fourth-edition Mechanical Principles Markdown and images."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SLUG = "mechanism-principles-4e"
TITLE = "机械原理（第四版）"

HEADING_RE = re.compile(r"^(#{1,6})\s+(\S.*?)\s*$")
DECIMAL_RE = re.compile(r"^(\d+(?:\.\d+)+)\s+\S")
ENUM_RE = re.compile(r"^(\d+)\.\s+\S")
PAREN_RE = re.compile(r"^[（(]\s*\d+\s*[)）]\s*\S")
CAPTION_RE = re.compile(r"^(?:题)?图\s*\d+\s*[-－—.．]\s*\d+")
IMAGE_RE = re.compile(r"^!\[[^\]]*\]\(")
CJK_RE = re.compile(r"[\u3400-\u9fff\u3000-\u303f\uff00-\uffef]")
TEX_RE = re.compile(r"\\(?:[a-zA-Z]{2,}|[{}%&#_])|\\\\|[_^]\s*\{")
MATH_MARKER = "$$"


def is_tex_fragment(text: str) -> bool:
    """A paragraph that is bare TeX: real commands, no inline math, no HTML."""
    stripped = text.strip()
    if not stripped or "$" in stripped or "<" in stripped or not TEX_RE.search(stripped):
        return False
    if not CJK_RE.search(stripped):
        return True
    outside_text = re.sub(r"\\(?:text|textrm|mathrm|mbox)\s*\{[^{}]*\}", "", stripped)
    return not CJK_RE.search(outside_text) and "。" not in stripped and "，" not in stripped


def looks_like_math(line: str) -> bool:
    """Guess whether a line is equation content rather than prose or a caption."""
    stripped = line.strip()
    if not stripped or stripped.startswith(("#", "![")) or CAPTION_RE.match(stripped):
        return False
    if stripped.startswith(("\\", "$", "{", "[")):
        return True
    if CJK_RE.search(stripped):
        return False
    return bool(re.search(r"[_^=<>]", stripped)) and not stripped.endswith("。")


def resync_math_markers(lines: list[str]) -> list[str]:
    """Re-pair `$$` markers the OCR spread across two adjacent equations."""
    out: list[str] = []
    inside = False
    for position, line in enumerate(lines):
        if line.strip() != MATH_MARKER:
            out.append(line)
            continue
        following = lines[position + 1].strip() if position + 1 < len(lines) else ""
        if not inside:
            if looks_like_math(following):
                inside = True
                out.append(MATH_MARKER)
            continue
        if looks_like_math(following):
            out.extend([MATH_MARKER, "", MATH_MARKER])
            continue
        out.extend([MATH_MARKER, ""])
        inside = False
    return out


def repair_math(paragraphs: list[str]) -> list[str]:
    """Re-seal display-math blocks whose `$$` markers the OCR scrambled."""
    repaired: list[str] = []
    for paragraph in paragraphs:
        stripped = paragraph.strip()
        if stripped == MATH_MARKER:
            continue
        if stripped.endswith("\n" + MATH_MARKER) and not stripped.startswith(MATH_MARKER):
            body = stripped[: -len(MATH_MARKER)].strip()
            repaired.append(f"$$\n{body}\n$$" if is_tex_fragment(body) else body)
            continue
        if is_tex_fragment(stripped):
            repaired.append(f"$$\n{stripped}\n$$")
            continue
        repaired.append(paragraph)
    return repaired


def normalize_heading(line: str, section_level: int) -> tuple[str, int]:
    """Demote OCR-promoted outline noise to the level the printed book implies.

    Returns the rewritten line plus the section level that later items nest under.
    """
    match = HEADING_RE.match(line)
    if not match:
        return line, section_level
    text = match[2]
    text = re.sub(r"^(\d+(?:[.．]\d+)*)\s*\\\\", r"\1 ", text)
    text = re.sub(r"^(\d+)\s*[:：]\s*(?=\d)", r"\1.", text)
    text = re.sub(r"^(\d+(?:[.．]\d+)+)[.．]\s+", r"\1 ", text)
    if ENUM_RE.match(text):
        level = min(4, section_level + 1)
        return "#" * level + " " + text, section_level
    decimal = re.match(r"^(\d+(?:[.．]\d+)+)\s+\S", text)
    if decimal:
        level = min(4, len(re.findall(r"[.．]", decimal[1])) + 1)
        return "#" * level + " " + text, level
    if PAREN_RE.match(text):
        return text, section_level
    if re.fullmatch(r"【[^】]{1,12}】", text.strip()):
        return f"**{text.strip()}**", section_level
    return line, len(match.group(1))


def explode_figure_block(raw_lines: list[str], start: int) -> tuple[list[str], int]:
    """Split `image + part legend + caption` runs into separate paragraphs."""
    out = [raw_lines[start].rstrip(), ""]
    legends: list[str] = []
    caption: str | None = None
    tail: list[str] = []
    index = start + 1
    while index < len(raw_lines) and raw_lines[index].strip():
        text = raw_lines[index].strip()
        if caption is None:
            if CAPTION_RE.match(text) and len(text) < 240:
                caption = text
            else:
                legends.append(text)
        else:
            tail.append(text)
        index += 1
    if caption:
        out.extend([caption, "{: .figure-caption }", ""])
    for text in legends:
        out.extend([text, ""])
    for text in tail:
        out.extend([text, ""])
    return out, index


def prepare(body: str, prefix: str) -> str:
    raw: list[str] = []
    section_level = 1
    for line in body.splitlines():
        line, section_level = normalize_heading(line, section_level)
        raw.append(line)
    lines: list[str] = []
    index = 0
    while index < len(raw):
        line = raw[index]
        if IMAGE_RE.match(line.strip()):
            block, index = explode_figure_block(raw, index)
            lines.extend(block)
            continue
        lines.append(line.rstrip())
        index += 1
    lines = resync_math_markers(lines)
    text = "\n".join(lines).strip()
    paragraphs = text.split("\n\n")
    previous_image = -10
    for position, paragraph in enumerate(paragraphs):
        stripped = paragraph.strip()
        if IMAGE_RE.match(stripped):
            previous_image = position
        elif (CAPTION_RE.match(stripped) and "\n" not in stripped and len(stripped) < 240
              and (position - previous_image <= 3
                   or (len(stripped) < 60 and "。" not in stripped))):
            paragraphs[position] = stripped + "\n{: .figure-caption }"
    paragraphs = repair_math(paragraphs)
    for position in range(1, len(paragraphs)):
        if (paragraphs[position].endswith("{: .figure-caption }")
                and paragraphs[position - 1].lstrip().startswith("#")
                and any(IMAGE_RE.match(p.strip())
                        for p in paragraphs[max(0, position - 4):position - 1])):
            paragraphs[position - 1], paragraphs[position] = (
                paragraphs[position], paragraphs[position - 1])
    text = "\n\n".join(paragraphs)
    text = re.sub(r"(?<=\()images/", prefix, text)
    text = re.sub(r'(src=["\'])images/', lambda m: m[1] + prefix, text)

    def table_math(match):
        return re.sub(r"(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)",
                      lambda m: '<span class="arithmatex">\\(' + html.escape(m[1]) + '\\)</span>',
                      match[0], flags=re.S)
    text = re.sub(r"<table\b.*?</table>", table_math, text, flags=re.S)
    text = re.sub(r"\n\$\$\n(.*?)\n\$\$", r"\n\n$$\n\1\n$$\n", text, flags=re.S)
    return re.sub(r"\n{3,}", "\n\n", text) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    source = args.source.resolve()
    text = source.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    chapters = list(re.finditer(r"^#\s+第\s*(\d+)\s*章\s*(.+)$", text, re.M))
    if [int(m[1]) for m in chapters] != list(range(1, 16)):
        raise ValueError("Expected chapters 1–15 in order")
    markers = [re.search(pattern, text, re.M) for pattern in (
        r"^## 附录\s*$", r"^## 附录 2[：:].*$", r"^## 参考文献\s*$", r"^## 作者简介\s*$")]
    if not all(markers) or sorted(m.start() for m in markers) != [m.start() for m in markers]:
        raise ValueError("Appendix/reference boundaries could not be identified")
    images = re.findall(r"!\[[^\]]*\]\((images/[^)]+)\)", text)
    images += re.findall(r'<img\b[^>]*src=["\'](images/[^"\']+)', text)
    missing = [name for name in set(images) if not (source.parent / name).is_file()]
    if missing:
        raise FileNotFoundError(str(missing[:10]))
    front = text[:chapters[0].start()]
    front = re.sub(r"^# ", "## ", front, flags=re.M)
    docs = [("00-front-matter/index.md", "前置内容", "# " + TITLE +
             "\n\n主编：潘存云、赵又红　｜　内容提供：熊忠帅\n\n" + front, "../images/")]
    for index, chapter in enumerate(chapters, 1):
        end = chapters[index].start() if index < len(chapters) else markers[0].start()
        title = f"第{index}章 {chapter[2].strip()}"
        docs.append((f"chapters/{index:02d}/index.md", title,
                     "# " + title + "\n\n" + text[chapter.end():end], "../../images/"))
    for index, (path, title) in enumerate([
        ("appendices/01/index.md", "附录1 世界机械发展史年鉴"),
        ("appendices/02/index.md", "附录2 重要名词术语中英文对照"),
        ("references/index.md", "参考文献"),
        ("author/index.md", "作者简介"),
    ]):
        end = markers[index + 1].start() if index + 1 < len(markers) else len(text)
        prefix = "../../images/" if path.startswith("appendices/") else "../images/"
        docs.append((path, title, "# " + title + "\n\n" + text[markers[index].end():end], prefix))
    report = {
        "title": TITLE, "slug": SLUG, "author": "潘存云、赵又红 主编", "contentProvider": "熊忠帅",
        "source": str(source), "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "images_in_source": len(list((source.parent / "images").glob("*"))),
        "referenced_images": len(set(images)), "missing_images": missing,
        "documents": [{"path": p, "title": t, "characters": len(b)} for p, t, b, _ in docs],
        "note": "原始 Markdown 和图片保持只读；署名区分原书主编与内容提供者；保留原文公式，不将 OCR 当作数学结论修订依据。",
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if args.dry_run:
        return
    target = ROOT / "content/books" / SLUG
    if target.exists():
        raise FileExistsError("Book exists; inspect changes rather than replacing it")
    captions = 0
    for path, title, body, prefix in docs:
        dest = target / "docs" / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        prepared = prepare(body, prefix)
        captions += prepared.count("{: .figure-caption }")
        dest.write_text(prepared, encoding="utf-8", newline="\n")
    for name in sorted(set(images)):
        src = (source.parent / name).resolve()
        src.relative_to((source.parent / "images").resolve())
        dest = target / "docs" / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
    nav = [{title: path} for path, title, _, _ in docs]
    (target / "mkdocs.yml").write_text(yaml.safe_dump(
        {"site_name": TITLE, "docs_dir": "docs", "nav": nav},
        allow_unicode=True, sort_keys=False), encoding="utf-8")
    inventory = ROOT / "resource-inventory" / SLUG
    inventory.mkdir(parents=True, exist_ok=True)
    report["figure_captions"] = captions
    (inventory / "import-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
