#!/usr/bin/env python
"""Report the course-specific conversion and code-viewer invariants."""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"


def main() -> None:
    catalog = json.loads((DIST / "data" / "catalog.json").read_text(encoding="utf-8"))
    data_docs = [
        doc for doc in catalog["docs"] if doc["bookSlug"] == "shangguigu-data-analysis"
    ]
    wind_docs = [
        doc
        for doc in catalog["docs"]
        if doc["bookSlug"]
        in {"wind-energy", "风能技术", "wind-turbine-theory-and-design"}
    ]
    data_html = "".join(
        json.loads((DIST / "data" / "docs" / f"{doc['id']}.json").read_text(encoding="utf-8"))["html"]
        for doc in data_docs
    )
    code_payloads = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in (DIST / "data" / "code").glob("*.json")
    ]
    app_js = (DIST / "app.js").read_text(encoding="utf-8")
    report = {
        "stats": catalog["stats"],
        "data_titles": [doc["title"] for doc in data_docs],
        "wind_documents": len(wind_docs),
        "categories": [item["id"] for item in catalog["site"]["categories"]],
        "data_tables": len(re.findall(r"<table\b", data_html)),
        "data_code_blocks": len(re.findall(r"<pre\b", data_html)),
        "data_images": len(re.findall(r"<img\b", data_html)),
        "notebooks": sum(item["kind"] == "notebook" for item in code_payloads),
        "truncated_previews": sum(bool(item.get("truncated")) for item in code_payloads),
        "missing_downloads": sum(
            not (DIST / Path(unquote(item["downloadUrl"]))).is_file()
            for item in code_payloads
        ),
        "old_positioning_in_ui": any(
            "电子书阅读器" in path.read_text(encoding="utf-8")
            for path in (DIST / "index.html", DIST / "app.js")
        ),
        "song_font_in_css": bool(
            re.search("宋体|SimSun", (DIST / "styles.css").read_text(encoding="utf-8"), re.I)
        ),
        "code_sidebar_navigation": all(
            token in app_js
            for token in ("renderCodeSidebar", "code-nav-link", "搜索代码与数据")
        ),
    }
    assert report["stats"] == {"books": 5, "docs": 71, "code": 182}
    assert report["wind_documents"] == 51
    assert report["categories"] == ["python", "data-analysis", "wind-energy"]
    assert report["data_tables"] == 49
    assert report["data_code_blocks"] >= 250
    assert report["data_images"] == 68
    assert report["notebooks"] == 7
    assert report["truncated_previews"] == 1
    assert report["missing_downloads"] == 0
    assert not report["old_positioning_in_ui"]
    assert not report["song_font_in_css"]
    assert report["code_sidebar_navigation"]
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
