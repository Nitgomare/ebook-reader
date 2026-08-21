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
    robot_docs = [doc for doc in catalog["docs"] if doc["bookSlug"] == "robot-textbook"]
    robot_html = "".join(
        json.loads((DIST / "data" / "docs" / f"{doc['id']}.json").read_text(encoding="utf-8"))["html"]
        for doc in robot_docs
    )
    data_html = "".join(
        json.loads((DIST / "data" / "docs" / f"{doc['id']}.json").read_text(encoding="utf-8"))["html"]
        for doc in data_docs
    )
    python_docs = [doc for doc in catalog["docs"] if doc["bookSlug"] == "shangguigu-python"]
    python_html = "".join(
        json.loads((DIST / "data" / "docs" / f"{doc['id']}.json").read_text(encoding="utf-8"))["html"]
        for doc in python_docs
    )
    code_payloads = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in (DIST / "data" / "code").glob("*.json")
    ]
    app_js = (DIST / "app.js").read_text(encoding="utf-8")
    index_html = (DIST / "index.html").read_text(encoding="utf-8")
    report = {
        "stats": catalog["stats"],
        "data_titles": [doc["title"] for doc in data_docs],
        "wind_documents": len(wind_docs),
        "robot_documents": len(robot_docs),
        "robot_videos": len(re.findall(r"<video\b", robot_html)),
        "robot_images": len(re.findall(r"<img\b", robot_html)),
        "robot_tables": len(re.findall(r"<table\b", robot_html)),
        "robot_formulas": len(re.findall(r'class="arithmatex"', robot_html)),
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
        "python_video_chapters": python_html.count('class="chapter-videos"'),
        "python_video_links": len(
            set(re.findall(r"https://www\.bilibili\.com/video/BV1tDsgzxECr\?p=\d+", python_html))
        ),
        "data_video_chapters": data_html.count('class="chapter-videos"'),
        "data_video_links": len(
            set(re.findall(r"https://www\.bilibili\.com/video/BV1D9GLzyEL6\?p=\d+", data_html))
        ),
        "data_course_schedule": (
            "课程安排" in data_html
            and all(label in data_html for label in ("课本位置", "课件", "代码", "视频"))
            and all(f"#/code/{identifier}" in data_html for identifier in (
                "2e13022a9c828d0b", "12d66456459b48d3", "6c1ffe660171cb77",
                "760170eac73f6f5c", "aab09632493e7a4b", "699e2e2adb7101e2",
                "a72d82e453f4f082",
            ))
        ),
        "nonblocking_math_loader": (
            'defer src="app.js?v=' in index_html
            and 'async src="https://cdn.jsdelivr.net/npm/mathjax' in index_html
            and index_html.index('defer src="app.js?v=')
            < index_html.index('async src="https://cdn.jsdelivr.net/npm/mathjax')
        ),
        "versioned_static_assets": (
            "__ASSET_VERSION__" not in index_html
            and bool(re.search(r"app\.js\?v=[0-9a-f]{12}", index_html))
            and bool(re.search(r"styles\.css\?v=[0-9a-f]{12}", index_html))
        ),
        "fresh_data_fetches": app_js.count('cache: "no-store"'),
    }
    assert report["stats"] == {"books": 6, "docs": 89, "code": 182}
    assert report["wind_documents"] == 51
    assert report["robot_documents"] == 18
    assert report["robot_videos"] == 3
    assert report["robot_images"] == 7
    assert report["robot_tables"] == 64
    assert report["robot_formulas"] == 172
    assert report["categories"] == ["python", "data-analysis", "robotics", "wind-energy"]
    assert report["data_tables"] == 50
    assert report["data_code_blocks"] >= 250
    assert report["data_images"] == 68
    assert report["notebooks"] == 7
    assert report["truncated_previews"] == 1
    assert report["missing_downloads"] == 0
    assert not report["old_positioning_in_ui"]
    assert not report["song_font_in_css"]
    assert report["code_sidebar_navigation"]
    assert report["python_video_chapters"] == 14
    assert report["python_video_links"] == 172
    assert report["data_video_chapters"] == 4
    assert report["data_video_links"] == 69
    assert report["data_course_schedule"]
    assert report["nonblocking_math_loader"]
    assert report["versioned_static_assets"]
    assert report["fresh_data_fetches"] == 3
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
