#!/usr/bin/env python
"""Validate generated catalog, document payloads, links, and copied assets."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
URL_RE = re.compile(r"(?:href|src)=['\"]([^'\"]+)['\"]", re.I)
DOC_ROUTE_RE = re.compile(r"^#/doc/([^?]+)")


def main() -> int:
    catalog_path = DIST / "data" / "catalog.json"
    if not catalog_path.is_file():
        print("缺少 dist/data/catalog.json；请先运行构建。", file=sys.stderr)
        return 1

    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    docs = catalog.get("docs", [])
    ids = {str(doc["id"]) for doc in docs}
    errors: list[str] = []
    if len(ids) != len(docs):
        errors.append("目录中存在重复文档 ID")

    referenced_assets: set[Path] = set()
    for summary in docs:
        payload_path = DIST / "data" / "docs" / f"{summary['id']}.json"
        if not payload_path.is_file():
            errors.append(f"缺少文章数据：{payload_path.relative_to(DIST)}")
            continue
        payload = json.loads(payload_path.read_text(encoding="utf-8"))
        if payload.get("title") != summary.get("title"):
            errors.append(f"标题不一致：{summary['id']}")
        for raw_url in URL_RE.findall(str(payload.get("html", ""))):
            doc_match = DOC_ROUTE_RE.match(raw_url)
            if doc_match and doc_match.group(1) not in ids:
                errors.append(f"文章 {summary['id']} 指向不存在的章节：{raw_url}")
                continue
            parsed = urlsplit(raw_url)
            if parsed.path.startswith("files/"):
                asset = DIST / Path(*unquote(parsed.path).split("/"))
                referenced_assets.add(asset)
                if not asset.is_file():
                    errors.append(f"文章 {summary['id']} 缺少资源：{parsed.path}")

    for book in catalog.get("books", []):
        first_id = str(book.get("firstDocId", ""))
        if first_id and first_id not in ids:
            errors.append(f"书籍 {book.get('slug')} 的首篇文章不存在：{first_id}")
        cover = str(book.get("cover", ""))
        if cover and not (DIST / Path(*unquote(cover).split("/"))).is_file():
            errors.append(f"书籍 {book.get('slug')} 的封面不存在：{cover}")

    if errors:
        print("电子书产物检查失败：", file=sys.stderr)
        for error in errors[:50]:
            print(f"- {error}", file=sys.stderr)
        if len(errors) > 50:
            print(f"- 另有 {len(errors) - 50} 个错误", file=sys.stderr)
        return 1

    print(
        "检查通过："
        f"{catalog['stats']['books']} 本书，{len(docs)} 篇文章，"
        f"{len(referenced_assets)} 个正文引用资源。"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

