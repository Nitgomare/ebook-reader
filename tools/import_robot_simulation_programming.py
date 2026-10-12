"""Merge the four supplied MinerU exports and import their seven chapters."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "robot-simulation-programming"
TITLES = [
    "机器人学与 MATLAB 机器人工具箱",
    "MATLAB 机器人工具箱的应用",
    "V-REP 在机器人仿真中的应用",
    "Gazebo 在机器人仿真中的应用",
    "OpenRAVE 在机器人仿真中的应用",
    "机器人操作系统的基础",
    "机器人操作系统的应用",
]
PART_TITLES = [
    "第一篇 基于 MATLAB 工具箱的机器人仿真",
    "第二篇 机器人仿真软件的基础与应用",
    "第三篇 机器人操作系统基础与应用",
]
CHAPTER_PATTERNS = [
    r"^# 机器人学与 MATLAB\s*\n\s*## 机器人工具箱\s*$",
    r"^# MATLAB 机器人\s*\n\s*## 工具箱的应用\s*$",
    r"^# V-REP 在机器人仿真中的应用\s*$",
    r"^# Gazebo 在机器人仿真中的应用\s*$",
    r"^## OpenRAVE 在机器人\s*\n\s*## 仿真中的应用\s*$",
    r"^# 机器人操作系统的基础\s*$",
    r"^# 机器人操作系统的应用\s*$",
]
IMAGE_RE = re.compile(r"!\[[^\]]*\]\((images/[^)]+)\)")
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})([^\n]*)$")
URL_RE = re.compile(r"https?://[^\s<>\"'\]\u4e00-\u9fff，。；：]+")


def link_plain_urls(line: str) -> str:
    def replace(match):
        before = line[:match.start()]
        if before.endswith(("](", "<", 'href="', "href='", 'src="', "src='")):
            return match.group(0)
        original = match.group(0)
        url = original.rstrip(".,;:，。；：")
        while url.endswith(")") and url.count(")") > url.count("("):
            url = url[:-1]
        cleaned = url.replace(r"\_", "_")
        return "<" + cleaned + ">" + original[len(url):]
    return URL_RE.sub(replace, line)


def load_parts(mineru: Path):
    parts = []
    image_sources = {}
    inventory = []
    for number in range(1, 5):
        matches = sorted(mineru.glob(f"机器人仿真与编程技术_part{number}_*.pdf-*"))
        if len(matches) != 1:
            raise ValueError(f"part{number}: expected one source, found {len(matches)}")
        source = matches[0]
        original = (source / "full.md").read_text(encoding="utf-8-sig")
        text = original.replace("\r\n", "\n")
        text = re.sub(r"(?<=\()images/", f"images/part{number}/", text)
        text = re.sub(r'(src=["\'])images/', rf"\g<1>images/part{number}/", text)
        files = sorted((source / "images").rglob("*"))
        files = [item for item in files if item.is_file()]
        for item in files:
            rel = f"part{number}/" + item.relative_to(source / "images").as_posix()
            image_sources[rel] = item
        inventory.append({
            "part": number, "source": str(source), "images": len(files),
            "markdown_sha256": hashlib.sha256(original.encode("utf-8")).hexdigest(),
        })
        parts.append(text.strip())
    merged = parts[0]
    joins = []
    for number, part in enumerate(parts[1:], 2):
        if number == 2 and merged.endswith("沿着 z") and part.startswith("方向执行"):
            merged += part
            joins.append("part1→part2: 接续被页边界拆开的 z方向 段落")
        elif number == 4 and merged.endswith("\n```") and part.startswith("```cpp\n"):
            merged = merged[:-4].rstrip() + "\n" + part[len("```cpp\n"):]
            joins.append("part3→part4: 合并同一 Hydra 插件的 C++ 代码围栏")
        else:
            merged += "\n\n" + part
            joins.append(f"part{number-1}→part{number}: 保留正文与图片的连续顺序")
    merged += "\n"
    missing = [p for p in IMAGE_RE.findall(merged) if p.removeprefix("images/") not in image_sources]
    if missing:
        raise ValueError(f"Missing images: {missing[:10]}")
    return merged, image_sources, inventory, joins


def outside_fences(text: str):
    active = None
    for line in text.splitlines():
        match = FENCE_RE.match(line)
        if match:
            marker, language = match.groups()
            if active is None:
                active = marker
            elif marker[0] == active[0] and len(marker) >= len(active) and not language.strip():
                active = None
            yield line, True
        else:
            yield line, active is not None
    if active:
        raise ValueError("Unclosed code fence")


def prepare_document(body: str, title: str, image_prefix: str) -> str:
    lines = []
    section_level = 2
    for line, in_code in outside_fences(body):
        if not in_code:
            line = link_plain_urls(line)
            heading = re.match(r"^#{1,6}\s+(.+)$", line)
            if heading:
                label = heading.group(1)
                decimal = re.match(r"^(\d+(?:\.\d+)+)\s+", label)
                if decimal:
                    section_level = min(4, decimal.group(1).count(".") + 1)
                    line = "#" * section_level + " " + label
                elif re.match(r"\d+\.\s+", label):
                    label = re.sub(r"^\d+\.\s+", "", label)
                    line = "#" * min(4, section_level + 1) + " " + label
                else:
                    line = "## " + label
            if re.match(r"^图\s*\d+\s*[-—.．]\s*\d+", line) and len(line) < 800:
                lines.extend(["", line.strip(), "{: .figure-caption }", ""])
                continue
        lines.append(line.rstrip())
    rendered = "\n".join(lines).strip()
    # MinerU duplicated truncated equation numbers before their complete tags.
    rendered = re.sub(r"\\tag\s*\{1\.10\}\s*(?=\\tag\{1\.105\})", "", rendered)
    rendered = re.sub(r"\\tag\s*\{2\.\}\s*(?=\\tag\{2\.137\})", "", rendered)
    rendered = rendered.replace("(images/", f"({image_prefix}")
    rendered = re.sub(r'(src=["\'])images/', rf"\g<1>{image_prefix}", rendered)
    # Raw HTML table cells bypass Markdown math processing; mark only their math.
    def table_math(match):
        table = match.group(0)
        return re.sub(r"(?<!\$)\$([^$\n]+)\$(?!\$)",
                      lambda m: '<span class="arithmatex">\\(' + m.group(1) + '\\)</span>', table)
    rendered = re.sub(r"<table\b[\s\S]*?</table>", table_math, rendered)
    return f"# {title}\n\n{rendered}\n"


def sections(merged: str):
    chapters = []
    for pattern in CHAPTER_PATTERNS:
        hits = list(re.finditer(pattern, merged, re.M))
        if len(hits) != 1:
            raise ValueError(f"Chapter heading mismatch: {pattern}, {len(hits)}")
        chapters.append(hits[0])
    if [m.start() for m in chapters] != sorted(m.start() for m in chapters):
        raise ValueError("Chapter order mismatch")
    part1 = merged.index("## 第一篇 基于MATLAB工具箱的机器人仿真")
    part2 = merged.index("## 第二篇 机器人仿真软件的基础与应用", chapters[1].end())
    part3 = merged.index("## 第三篇 机器人操作系统 基础与应用", chapters[4].end())
    back = merged.index("《机器人仿真与编程技术》的内容十分丰富", chapters[6].end())
    docs = [("00-front-matter/index.md", "前置内容", merged[:part1], "../images/")]
    for index, (start, first) in enumerate([(part1, 0), (part2, 2), (part3, 5)], 1):
        intro = merged[start:chapters[first].start()]
        intro = intro.split("\n", 1)[1]
        docs.append((f"parts/{index:02d}/index.md", PART_TITLES[index - 1] + " · 导言", intro, "../../images/"))
    ends = [chapters[1].start(), part2, chapters[3].start(), chapters[4].start(), part3, chapters[6].start(), back]
    for index, (chapter, end) in enumerate(zip(chapters, ends), 1):
        docs.append((f"chapters/{index:02d}/index.md", f"第{index}章 {TITLES[index-1]}",
                     merged[chapter.end():end], "../../images/"))
    docs.append(("back-matter/index.md", "封底与出版信息", merged[back:], "../images/"))
    return docs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mineru", type=Path, default=Path("C:/Users/18066/MinerU"))
    parser.add_argument("--merged-output", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    merged, image_sources, inventory, joins = load_parts(args.mineru)
    docs = sections(merged)
    report = {
        "slug": SLUG, "parts": inventory, "images": len(image_sources),
        "image_references": len(IMAGE_RE.findall(merged)), "joins": joins,
        "image_mib": round(sum(item.stat().st_size for item in image_sources.values()) / 1048576, 2),
        "documents": [{"path": path, "title": title, "characters": len(body)}
                      for path, title, body, _ in docs],
        "source_note": "保留 MinerU 提供的公式、表格和代码内容；未将 OCR 代码视为经过运行验证的源码。",
    }
    blocks = re.findall(r"(?ms)^```([^\n]*)\n(.*?)^```\s*$", merged)
    report["code_languages"] = dict(Counter(language.strip() for language, _ in blocks))
    report["math_like_code"] = [
        {"language": language, "sample": body[:180]}
        for language, body in blocks
        if re.search(r"\\(?:frac|sqrt|begin\{|theta|omega|mathbf)", body)
    ]
    prepared = [(path, prepare_document(body, title, prefix)) for path, title, body, prefix in docs]
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if args.dry_run:
        return
    target = ROOT / "content" / "books" / SLUG
    if target.exists() or args.merged_output.exists():
        raise FileExistsError("Target already exists; inspect it before replacing a previous import")
    args.merged_output.mkdir(parents=True)
    (args.merged_output / "full.md").write_text(merged, encoding="utf-8", newline="\n")
    for rel, source in image_sources.items():
        destination = args.merged_output / "images" / rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    (args.merged_output / "merge-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (target / "docs").mkdir(parents=True)
    shutil.copytree(args.merged_output / "images", target / "docs" / "images")
    for rel, text in prepared:
        path = target / "docs" / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
    nav = ['site_name: "机器人仿真与编程技术"', 'docs_dir: docs', 'nav:',
           '  - "前置内容": 00-front-matter/index.md']
    for number, chapter_numbers in enumerate([[1, 2], [3, 4, 5], [6, 7]], 1):
        nav.extend([f'  - "{PART_TITLES[number-1]}":',
                    f'      - "导言": parts/{number:02d}/index.md'])
        for chapter in chapter_numbers:
            nav.append(f'      - "第{chapter}章 {TITLES[chapter-1]}": chapters/{chapter:02d}/index.md')
    nav.append('  - "封底与出版信息": back-matter/index.md')
    (target / "mkdocs.yml").write_text("\n".join(nav) + "\n", encoding="utf-8")
    notes = ROOT / "resource-inventory" / SLUG
    notes.mkdir(parents=True, exist_ok=True)
    (notes / "import-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
