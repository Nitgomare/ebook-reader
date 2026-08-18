#!/usr/bin/env python
"""Build the standalone public knowledge site from chapter-oriented courses."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from urllib.parse import quote, unquote, urlsplit

import markdown
import yaml


ROOT = Path(__file__).resolve().parent
BOOKS_CANDIDATES = (
    ROOT / "content" / "books",
    ROOT.parent / "books",
    ROOT.parent / "knowledge-base" / "books",
)
BOOKS_ROOT = next((path for path in BOOKS_CANDIDATES if path.is_dir()), BOOKS_CANDIDATES[0])
PUBLIC_ROOT = ROOT / "public"
DEFAULT_OUTPUT = ROOT / "dist"
SKIP_DIRS = {".git", ".idea", "__pycache__", "site", "dist", "node_modules"}
CODE_EXTENSIONS = {
    ".py": ("source", "python"),
    ".ipynb": ("notebook", "python"),
    ".sql": ("source", "sql"),
    ".md": ("text", "markdown"),
    ".txt": ("text", "text"),
    ".json": ("dataset", "json"),
    ".csv": ("dataset", "csv"),
    ".html": ("source", "html"),
    ".css": ("source", "css"),
    ".js": ("source", "javascript"),
    ".yaml": ("source", "yaml"),
    ".yml": ("source", "yaml"),
    ".toml": ("source", "toml"),
}
MAX_CODE_PREVIEW_BYTES = 256 * 1024
MARKDOWN_EXTENSIONS = [
    "extra",
    "admonition",
    "toc",
    "pymdownx.superfences",
    "pymdownx.highlight",
    "pymdownx.arithmatex",
]
MARKDOWN_EXTENSION_CONFIGS = {
    "pymdownx.arithmatex": {
        "generic": True,
    },
}
URL_ATTR_RE = re.compile(r"(?P<attr>href|src)=(?P<quote>['\"])(?P<url>.*?)(?P=quote)", re.I)
TABLE_RE = re.compile(r"(<table\b[^>]*>.*?</table>)", re.I | re.S)
ESCAPED_HTML_TAG_RE = re.compile(r"\\<(?P<tag>[^>]+)\\>")
FRONT_MATTER_RE = re.compile(r"\A---\s*\r?\n.*?\r?\n---\s*(?:\r?\n|\Z)", re.S)


class MkDocsConfigLoader(yaml.SafeLoader):
    """Read MkDocs YAML while treating Python-extension tags as plain values."""


def construct_unknown_yaml_tag(
    loader: MkDocsConfigLoader, tag_suffix: str, node: yaml.Node
) -> object:
    if isinstance(node, yaml.ScalarNode):
        return loader.construct_scalar(node)
    if isinstance(node, yaml.SequenceNode):
        return loader.construct_sequence(node)
    if isinstance(node, yaml.MappingNode):
        return loader.construct_mapping(node)
    return tag_suffix


MkDocsConfigLoader.add_multi_constructor(
    "tag:yaml.org,2002:python/", construct_unknown_yaml_tag
)


class HeadingCollector(HTMLParser):
    """Collect rendered h2-h4 headings without adding a parser dependency."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.headings: list[dict[str, object]] = []
        self._current: dict[str, object] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag not in {"h2", "h3", "h4"}:
            return
        attributes = dict(attrs)
        self._current = {"level": int(tag[1]), "id": attributes.get("id", ""), "text": []}

    def handle_data(self, data: str) -> None:
        if self._current is not None:
            self._current["text"].append(data)

    def handle_endtag(self, tag: str) -> None:
        if self._current is None or tag != f"h{self._current['level']}":
            return
        text_value = "".join(self._current["text"]).strip()
        if text_value and self._current["id"]:
            self.headings.append(
                {
                    "level": self._current["level"],
                    "id": self._current["id"],
                    "text": text_value,
                }
            )
        self._current = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="构建公共知识学习站")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="静态产物目录")
    parser.add_argument(
        "--book",
        action="append",
        dest="books",
        help="只构建指定书籍；可重复传入，默认构建 books.json 中的全部书籍",
    )
    return parser.parse_args()


def load_reader_config() -> dict[str, object]:
    return json.loads((ROOT / "books.json").read_text(encoding="utf-8"))


def doc_id(book_slug: str, rel_path: str) -> str:
    digest = hashlib.sha1(f"{book_slug}/{rel_path}".encode("utf-8")).hexdigest()[:16]
    return digest


def code_id(book_slug: str, rel_path: str) -> str:
    return hashlib.sha1(f"code/{book_slug}/{rel_path}".encode("utf-8")).hexdigest()[:16]


def flatten_nav(items: object, sections: tuple[str, ...] = ()) -> list[dict[str, object]]:
    flattened: list[dict[str, object]] = []
    if not isinstance(items, list):
        return flattened

    for item in items:
        if isinstance(item, str):
            if item.lower().endswith(".md"):
                flattened.append({"title": "", "path": item, "sections": list(sections)})
            continue
        if not isinstance(item, dict):
            continue
        for title, value in item.items():
            if isinstance(value, str) and value.lower().endswith(".md"):
                flattened.append({"title": str(title), "path": value, "sections": list(sections)})
            elif isinstance(value, list):
                flattened.extend(flatten_nav(value, sections + (str(title),)))
    return flattened


def title_from_markdown(markdown_text: str, fallback: str) -> str:
    match = re.search(r"^\s{0,3}#\s+(.+?)\s*#*\s*$", markdown_text, re.M)
    if not match:
        return fallback
    value = re.sub(r"[`*_~\[\]]", "", match.group(1)).strip()
    return value or fallback


def excerpt_from_markdown(markdown_text: str) -> str:
    in_fence = False
    for raw_line in markdown_text.splitlines():
        line = raw_line.strip()
        if line.startswith(("```", "~~~")):
            in_fence = not in_fence
            continue
        if in_fence or not line or line.startswith(("#", "!", "|", "<", ">", "- ", "* ")):
            continue
        clean = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", line)
        clean = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", clean)
        clean = re.sub(r"[`*_~]", "", clean).strip()
        if len(clean) >= 18:
            return clean[:140]
    return ""


def find_cover(docs_root: Path) -> Path | None:
    candidates: list[Path] = []
    for path in docs_root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp", ".svg"}:
            continue
        lower_name = path.name.lower()
        if "cover" in lower_name or "封面" in lower_name:
            candidates.append(path)
    return sorted(candidates, key=lambda item: (len(item.parts), item.as_posix()))[0] if candidates else None


def copy_public(output: Path) -> None:
    if output.exists():
        shutil.rmtree(output)
    shutil.copytree(PUBLIC_ROOT, output)
    asset_digest = hashlib.sha1(
        (output / "app.js").read_bytes() + (output / "styles.css").read_bytes()
    ).hexdigest()[:12]
    index_path = output / "index.html"
    index_path.write_text(
        index_path.read_text(encoding="utf-8").replace("__ASSET_VERSION__", asset_digest),
        encoding="utf-8",
    )
    (output / "data" / "docs").mkdir(parents=True)
    (output / "data" / "code").mkdir(parents=True)
    (output / "files").mkdir(parents=True)


def decode_text(source: Path, limit: int = MAX_CODE_PREVIEW_BYTES) -> tuple[str, bool]:
    raw = source.read_bytes()
    truncated = len(raw) > limit
    sample = raw[:limit]
    for encoding in ("utf-8-sig", "gb18030", "latin-1"):
        try:
            return sample.decode(encoding), truncated
        except UnicodeDecodeError:
            continue
    return sample.decode("utf-8", errors="replace"), truncated


def notebook_cells(source: Path) -> list[dict[str, object]]:
    notebook = json.loads(source.read_text(encoding="utf-8-sig"))
    cells: list[dict[str, object]] = []
    for index, cell in enumerate(notebook.get("cells", [])):
        cell_type = str(cell.get("cell_type", "code"))
        cell_source = cell.get("source", "")
        text = "".join(cell_source) if isinstance(cell_source, list) else str(cell_source)
        payload: dict[str, object] = {"index": index + 1, "type": cell_type, "source": text}
        if cell_type == "markdown":
            payload["html"] = markdown.markdown(text, extensions=["extra"])
        elif cell_type == "code":
            outputs: list[str] = []
            for output in cell.get("outputs", []):
                value = output.get("text")
                if value is None:
                    value = output.get("data", {}).get("text/plain")
                if isinstance(value, list):
                    value = "".join(value)
                if value:
                    outputs.append(str(value))
            if outputs:
                payload["output"] = "\n".join(outputs)[:20000]
        cells.append(payload)
    return cells


def build_code_assets(
    book: dict[str, object], output: Path, docs: list[dict[str, object]]
) -> tuple[list[dict[str, object]], dict[str, list[str]]]:
    configured = str(book.get("codeSource", "")).strip()
    if not configured:
        return [], {}
    slug = str(book["slug"])
    book_root = BOOKS_ROOT / slug
    code_root = (book_root / configured).resolve()
    code_root.relative_to(book_root.resolve())
    if not code_root.is_dir():
        raise FileNotFoundError(f"找不到配套代码目录：{code_root}")

    configured_links = book.get("codeLinks", {})
    explicit_links = configured_links if isinstance(configured_links, dict) else {}
    by_doc: dict[str, list[str]] = {str(doc["relPath"]): [] for doc in docs}
    public_files: list[dict[str, object]] = []
    for source in sorted(code_root.rglob("*"), key=lambda path: path.as_posix().casefold()):
        if not source.is_file() or source.suffix.lower() not in CODE_EXTENSIONS:
            continue
        if any(part in SKIP_DIRS for part in source.relative_to(code_root).parts):
            continue
        rel_path = source.relative_to(code_root).as_posix()
        identifier = code_id(slug, rel_path)
        kind, language = CODE_EXTENSIONS[source.suffix.lower()]
        destination = output / "files" / "code" / slug / Path(*PurePosixPath(rel_path).parts)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        encoded = "/".join(quote(part) for part in ("files", "code", slug, *PurePosixPath(rel_path).parts))
        payload: dict[str, object] = {
            "id": identifier,
            "bookSlug": slug,
            "path": rel_path,
            "name": source.name,
            "kind": kind,
            "language": language,
            "size": source.stat().st_size,
            "downloadUrl": encoded,
        }
        if kind == "notebook":
            payload["cells"] = notebook_cells(source)
            payload["truncated"] = False
        else:
            payload["content"], payload["truncated"] = decode_text(source)
        (output / "data" / "code" / f"{identifier}.json").write_text(
            json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8"
        )
        public_files.append({key: value for key, value in payload.items() if key not in {"content", "cells"}})

        group = PurePosixPath(rel_path).parts[0]
        automatic_doc = f"{group}.md"
        if automatic_doc in by_doc:
            by_doc[automatic_doc].append(identifier)
        for doc_path in explicit_links.get(group, []):
            normalized = str(doc_path).replace("\\", "/")
            if normalized in by_doc and identifier not in by_doc[normalized]:
                by_doc[normalized].append(identifier)
    return public_files, by_doc


def safe_target(source_root: Path, current_rel: str, raw_url: str) -> tuple[Path, str, str] | None:
    parsed = urlsplit(html.unescape(raw_url))
    if parsed.scheme or parsed.netloc or raw_url.startswith(("#", "data:", "mailto:", "tel:")):
        return None
    decoded_path = unquote(parsed.path).replace("\\", "/")
    if not decoded_path:
        return None
    rel = PurePosixPath(current_rel).parent.joinpath(decoded_path)
    if rel.is_absolute():
        return None
    full_path = (source_root / Path(*rel.parts)).resolve()
    try:
        normalized_path = full_path.relative_to(source_root.resolve())
    except ValueError:
        return None
    return full_path, normalized_path.as_posix(), parsed.fragment


def rewrite_document_urls(
    rendered_html: str,
    *,
    output: Path,
    book_slug: str,
    docs_root: Path,
    current_rel: str,
    id_map: dict[str, str],
) -> str:
    def replace(match: re.Match[str]) -> str:
        raw_url = match.group("url")
        target = safe_target(docs_root, current_rel, raw_url)
        if target is None:
            return match.group(0)
        full_path, rel_path, fragment = target
        quote_char = match.group("quote")
        attr = match.group("attr")

        if rel_path.lower().endswith(".md"):
            target_id = id_map.get(rel_path)
            if not target_id:
                return f'{attr}={quote_char}#{quote_char}'
            suffix = f"?anchor={quote(fragment)}" if fragment else ""
            return f'{attr}={quote_char}#/doc/{target_id}{suffix}{quote_char}'

        if not full_path.is_file():
            return match.group(0)
        destination = output / "files" / book_slug / Path(*PurePosixPath(rel_path).parts)
        destination.parent.mkdir(parents=True, exist_ok=True)
        if not destination.exists() or destination.stat().st_mtime_ns != full_path.stat().st_mtime_ns:
            shutil.copy2(full_path, destination)
        encoded = "/".join(quote(part) for part in ("files", book_slug, *PurePosixPath(rel_path).parts))
        suffix = f"#{quote(fragment)}" if fragment else ""
        return f'{attr}={quote_char}{encoded}{suffix}{quote_char}'

    return URL_ATTR_RE.sub(replace, rendered_html)


def collect_book_documents(book: dict[str, object]) -> tuple[Path, list[dict[str, object]], dict[str, object]]:
    slug = str(book["slug"])
    book_root = BOOKS_ROOT / slug
    mkdocs_path = book_root / "mkdocs.yml"
    if not mkdocs_path.is_file():
        raise FileNotFoundError(f"找不到 {mkdocs_path}")
    mkdocs_config = yaml.load(
        mkdocs_path.read_text(encoding="utf-8"), Loader=MkDocsConfigLoader
    ) or {}
    docs_root = book_root / str(mkdocs_config.get("docs_dir", "docs"))
    nav_docs = flatten_nav(mkdocs_config.get("nav", []))

    listed = {str(item["path"]).replace("\\", "/") for item in nav_docs}
    for path in sorted(docs_root.rglob("*.md"), key=lambda item: item.as_posix().casefold()):
        rel = path.relative_to(docs_root).as_posix()
        if rel in listed or any(part in SKIP_DIRS for part in path.parts):
            continue
        nav_docs.append({"title": "", "path": rel, "sections": ["其他"]})

    docs: list[dict[str, object]] = []
    for item in nav_docs:
        rel_path = str(item["path"]).replace("\\", "/")
        source_path = docs_root / Path(*PurePosixPath(rel_path).parts)
        if not source_path.is_file():
            continue
        markdown_text = FRONT_MATTER_RE.sub("", source_path.read_text(encoding="utf-8-sig"), count=1)
        fallback = source_path.stem.replace("-", " ").replace("_", " ")
        docs.append(
            {
                "id": doc_id(slug, rel_path),
                "bookSlug": slug,
                "relPath": rel_path,
                "title": str(item.get("title") or title_from_markdown(markdown_text, fallback)),
                "sections": item.get("sections") or ["正文"],
                "excerpt": excerpt_from_markdown(markdown_text),
                "source": source_path,
                "markdown": markdown_text,
            }
        )

    for index, doc in enumerate(docs):
        doc["order"] = index + 1
        doc["previousId"] = docs[index - 1]["id"] if index else ""
        doc["nextId"] = docs[index + 1]["id"] if index + 1 < len(docs) else ""
    return docs_root, docs, mkdocs_config


def build_book(
    book: dict[str, object], output: Path
) -> tuple[dict[str, object], list[dict[str, object]], list[dict[str, object]]]:
    docs_root, docs, mkdocs_config = collect_book_documents(book)
    slug = str(book["slug"])
    id_map = {str(doc["relPath"]): str(doc["id"]) for doc in docs}
    public_code, code_by_doc = build_code_assets(book, output, docs)

    public_docs: list[dict[str, object]] = []
    for doc in docs:
        renderer = markdown.Markdown(
            extensions=MARKDOWN_EXTENSIONS,
            extension_configs=MARKDOWN_EXTENSION_CONFIGS,
            output_format="html5",
        )
        rendered = renderer.convert(str(doc.pop("markdown")))
        rendered = ESCAPED_HTML_TAG_RE.sub(
            lambda match: f"&lt;{html.escape(match.group('tag'))}&gt;",
            rendered,
        )
        rendered = TABLE_RE.sub(r'<div class="table-wrapper">\1</div>', rendered)
        rendered = rewrite_document_urls(
            rendered,
            output=output,
            book_slug=slug,
            docs_root=docs_root,
            current_rel=str(doc["relPath"]),
            id_map=id_map,
        )
        collector = HeadingCollector()
        collector.feed(rendered)
        payload = {key: value for key, value in doc.items() if key != "source"}
        payload["html"] = rendered
        payload["headings"] = collector.headings
        payload["codeFiles"] = code_by_doc.get(str(doc["relPath"]), [])
        (output / "data" / "docs" / f"{doc['id']}.json").write_text(
            json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8",
        )
        public_docs.append({key: value for key, value in payload.items() if key not in {"html", "headings"}})

    cover_url = ""
    configured_cover = str(book.get("coverSource", "")).strip()
    cover = docs_root / Path(*PurePosixPath(configured_cover).parts) if configured_cover else None
    if cover is not None:
        try:
            cover.resolve().relative_to(docs_root.resolve())
        except ValueError:
            raise ValueError(f"封面路径越界：{configured_cover}")
        if not cover.is_file():
            raise FileNotFoundError(f"找不到封面：{cover}")
    else:
        cover = find_cover(docs_root)
    if cover:
        rel_cover = cover.relative_to(docs_root).as_posix()
        destination = output / "files" / slug / Path(*PurePosixPath(rel_cover).parts)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(cover, destination)
        cover_url = "/".join(quote(part) for part in ("files", slug, *PurePosixPath(rel_cover).parts))

    public_book = {
        **book,
        "sourceSiteName": mkdocs_config.get("site_name", book["title"]),
        "cover": cover_url,
        "docCount": len(public_docs),
        "firstDocId": public_docs[0]["id"] if public_docs else "",
        "codeCount": len(public_code),
    }
    return public_book, public_docs, public_code


def main() -> None:
    args = parse_args()
    output = args.output.resolve()
    config = load_reader_config()
    configured_books = list(config.get("books", []))
    if args.books:
        requested = set(args.books)
        configured_books = [book for book in configured_books if book.get("slug") in requested]
        missing = requested - {str(book.get("slug")) for book in configured_books}
        if missing:
            raise SystemExit(f"books.json 中没有这些书：{', '.join(sorted(missing))}")

    copy_public(output)
    catalog_books: list[dict[str, object]] = []
    catalog_docs: list[dict[str, object]] = []
    catalog_code: list[dict[str, object]] = []
    for book in configured_books:
        print(f"Building {book['slug']} ...", flush=True)
        public_book, public_docs, public_code = build_book(book, output)
        catalog_books.append(public_book)
        catalog_docs.extend(public_docs)
        catalog_code.extend(public_code)

    catalog = {
        "site": config.get("site", {}),
        "stats": {"books": len(catalog_books), "docs": len(catalog_docs), "code": len(catalog_code)},
        "books": catalog_books,
        "docs": catalog_docs,
        "code": catalog_code,
    }
    (output / "data" / "catalog.json").write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    shutil.copy2(output / "index.html", output / "404.html")
    (output / ".nojekyll").write_text("", encoding="utf-8")
    print(
        f"Complete: {output} ({len(catalog_books)} courses, "
        f"{len(catalog_docs)} documents, {len(catalog_code)} code files)"
    )


if __name__ == "__main__":
    main()
