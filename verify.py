#!/usr/bin/env python
"""Validate generated courses, code viewers, links, and copied assets."""

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
    code_files = catalog.get("code", [])
    ids = {str(doc["id"]) for doc in docs}
    code_ids = {str(item["id"]) for item in code_files}
    errors: list[str] = []
    if len(ids) != len(docs):
        errors.append("目录中存在重复文档 ID")
    if len(code_ids) != len(code_files):
        errors.append("代码目录中存在重复文件 ID")

    referenced_assets: set[Path] = set()
    for summary in docs:
        payload_path = DIST / "data" / "docs" / f"{summary['id']}.json"
        if not payload_path.is_file():
            errors.append(f"缺少文章数据：{payload_path.relative_to(DIST)}")
            continue
        payload = json.loads(payload_path.read_text(encoding="utf-8"))
        if payload.get("title") != summary.get("title"):
            errors.append(f"标题不一致：{summary['id']}")
        for identifier in payload.get("codeFiles", []):
            if identifier not in code_ids:
                errors.append(f"章节 {summary['id']} 指向不存在的代码：{identifier}")
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
            errors.append(f"课程 {book.get('slug')} 的首篇内容不存在：{first_id}")
        cover = str(book.get("cover", ""))
        if cover and not (DIST / Path(*unquote(cover).split("/"))).is_file():
            errors.append(f"课程 {book.get('slug')} 的封面不存在：{cover}")

    for summary in code_files:
        payload_path = DIST / "data" / "code" / f"{summary['id']}.json"
        if not payload_path.is_file():
            errors.append(f"缺少代码预览：{payload_path.relative_to(DIST)}")
            continue
        payload = json.loads(payload_path.read_text(encoding="utf-8"))
        if payload.get("path") != summary.get("path"):
            errors.append(f"代码路径不一致：{summary['id']}")
        download = str(payload.get("downloadUrl", ""))
        target = DIST / Path(*unquote(download).split("/"))
        if not target.is_file():
            errors.append(f"代码下载文件不存在：{download}")

    for static_name in ("index.html", "app.js"):
        static_text = (DIST / static_name).read_text(encoding="utf-8")
        if "电子书阅读器" in static_text:
            errors.append(f"{static_name} 仍包含旧站定位“电子书阅读器”")

    oversized = [path for path in DIST.rglob("*") if path.is_file() and path.stat().st_size >= 100 * 1024 * 1024]
    for path in oversized:
        errors.append(f"文件超过 GitHub 单文件限制：{path.relative_to(DIST)}")

    if errors:
        print("学习站产物检查失败：", file=sys.stderr)
        for error in errors[:50]:
            print(f"- {error}", file=sys.stderr)
        if len(errors) > 50:
            print(f"- 另有 {len(errors) - 50} 个错误", file=sys.stderr)
        return 1

    print(
        "检查通过："
        f"{catalog['stats']['books']} 套内容，{len(docs)} 个章节，"
        f"{len(code_files)} 个代码/数据文件，{len(referenced_assets)} 个正文引用资源。"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
