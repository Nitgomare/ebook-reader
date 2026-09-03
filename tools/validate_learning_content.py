#!/usr/bin/env python
"""Validate the minimal textbook, resources and inline-code experience."""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
LANDING_LABELS = {"课程导读", "课程首页", "图书首页", "文档首页", "专题首页", "课程资源"}


def main() -> None:
    catalog = json.loads((DIST / "data" / "catalog.json").read_text(encoding="utf-8"))
    payloads = {
        doc["id"]: json.loads(
            (DIST / "data" / "docs" / f"{doc['id']}.json").read_text(encoding="utf-8")
        )
        for doc in catalog["docs"]
    }
    code_payloads = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in (DIST / "data" / "code").glob("*.json")
    ]
    app_js = (DIST / "app.js").read_text(encoding="utf-8")
    index_html = (DIST / "index.html").read_text(encoding="utf-8")
    styles_css = (DIST / "styles.css").read_text(encoding="utf-8")
    worker_js = (DIST / "_worker.js").read_text(encoding="utf-8")
    all_html = "".join(payload["html"] for payload in payloads.values())
    chapter_docs = [doc for doc in catalog["docs"] if doc.get("chapterNumber")]
    expected_books = {
        "research-skills", "shangguigu-python", "python-beginner-to-master",
        "shangguigu-data-analysis", "python-data-analysis", "deep-learning",
        "zhou-machine-learning", "machine-vision", "robot-textbook", "wind-energy", "风能技术",
        "wind-turbine-theory-and-design", "Utilizing-large-scale-foundation-models-for",
        "wind-scada-data-analysis-modeling",
        "smart-analysis-system-user-manual", "smart-analysis-system-technical-docs",
    }

    badly_numbered_headings: list[str] = []
    for doc in chapter_docs:
        for heading in payloads[doc["id"]]["headings"]:
            if heading["level"] in {2, 3, 4} and not re.match(
                rf"^{doc['chapterNumber']}\.\d+", heading["text"]
            ):
                badly_numbered_headings.append(
                    f"{doc['bookSlug']}:{doc['relPath']}:{heading['text']}"
                )

    resource_downloads = [
        resource for book in catalog["books"] for resource in book.get("resources", [])
    ]
    machine_learning_book = next(
        book for book in catalog["books"] if book["slug"] == "zhou-machine-learning"
    )
    machine_learning_images = list(
        (DIST / "files" / "zhou-machine-learning" / "images").glob("*.jpg")
    )
    scada_book = next(
        book for book in catalog["books"]
        if book["slug"] == "wind-scada-data-analysis-modeling"
    )
    scada_payloads = [
        payloads[doc["id"]] for doc in catalog["docs"]
        if doc["bookSlug"] == "wind-scada-data-analysis-modeling"
    ]
    scada_image_urls = re.findall(
        r'<img\b[^>]*\bsrc=["\']([^"\']+)["\']',
        "".join(payload["html"] for payload in scada_payloads),
        re.I,
    )
    scada_html = "".join(payload["html"] for payload in scada_payloads)
    research_book = next(
        book for book in catalog["books"] if book["slug"] == "research-skills"
    )
    research_computing_doc = next(
        payloads[doc["id"]] for doc in catalog["docs"]
        if doc["bookSlug"] == "research-skills"
        and doc["relPath"] == "04-python-research-computing/index.md"
    )
    ai_translation_doc = next(
        payloads[doc["id"]] for doc in catalog["docs"]
        if doc["bookSlug"] == "research-skills"
        and doc["relPath"] == "05-ai-paper-translation/index.md"
    )
    site_building_docs = [
        doc for doc in catalog["docs"]
        if doc["bookSlug"] == "research-skills"
        and doc["relPath"].startswith("03-site-building/")
    ]
    figure_doc = next(
        payloads[doc["id"]] for doc in catalog["docs"]
        if doc["bookSlug"] == "research-skills"
        and doc["relPath"] == "06-paper-figure-reproduction/index.md"
    )
    figure_video = next(
        resource for resource in research_book["resources"]
        if resource["path"] == "06-paper-figure-reproduction/paper-figure-reproduction.mp4"
    )
    presentation_docs = [
        payloads[doc["id"]] for doc in catalog["docs"]
        if doc["bookSlug"] == "research-skills"
        and doc["relPath"].startswith("07-research-presentation/")
    ]
    presentation_video = next(
        resource for resource in research_book["resources"]
        if resource["path"] == "07-research-presentation/research-presentation.mp4"
    )
    machine_vision_book = next(
        book for book in catalog["books"] if book["slug"] == "machine-vision"
    )
    machine_vision_docs = [
        payloads[doc["id"]] for doc in catalog["docs"]
        if doc["bookSlug"] == "machine-vision"
    ]
    machine_vision_image_urls = re.findall(
        r'<img\b[^>]*\bsrc=["\']([^"\']+)["\']',
        "".join(doc["html"] for doc in machine_vision_docs), re.I,
    )
    report = {
        "stats": catalog["stats"],
        "paper_figure_reproduction": {
            "title": figure_doc["title"],
            "sections": sum(h["level"] == 2 for h in figure_doc["headings"]),
            "video_present": (DIST / figure_video["downloadUrl"]).is_file(),
            "video_size": (DIST / figure_video["downloadUrl"]).stat().st_size,
            "video_linked": figure_doc.get("video") == figure_video["downloadUrl"],
            "video_actions": figure_doc["html"].count(figure_video["downloadUrl"]),
            "download_action": 'download="论文图片复现教学视频.mp4"' in figure_doc["html"],
            "creator_credit": "内容制作：窦丽露" in figure_doc["html"],
        },
        "research_presentation": {
            "documents": len(presentation_docs),
            "images": len(re.findall(
                r'<img\b[^>]*\bsrc=', "".join(doc["html"] for doc in presentation_docs), re.I,
            )),
            "missing_images": sum(
                not (DIST / Path(unquote(url))).is_file()
                for url in re.findall(
                    r'<img\b[^>]*\bsrc=["\']([^"\']+)["\']',
                    "".join(doc["html"] for doc in presentation_docs), re.I,
                )
            ),
            "video_present": (DIST / presentation_video["downloadUrl"]).is_file(),
            "video_size": (DIST / presentation_video["downloadUrl"]).stat().st_size,
            "video_linked": presentation_docs[0].get("video") == presentation_video["downloadUrl"],
            "creator_credit": "内容制作：戴琼" in presentation_docs[0]["html"],
        },
        "machine_vision_book": {
            "documents": machine_vision_book["docCount"],
            "chapters": machine_vision_book["chapterCount"],
            "images": len(machine_vision_image_urls),
            "missing_images": sum(
                not (DIST / Path(unquote(url))).is_file()
                for url in machine_vision_image_urls
            ),
        },
        "categories": [item["id"] for item in catalog["site"]["categories"]],
        "book_slugs": {book["slug"] for book in catalog["books"]},
        "chapter_documents": len(chapter_docs),
        "landing_documents": [
            f"{doc['bookSlug']}:{doc['title']}"
            for doc in catalog["docs"]
            if re.sub(r"\s+", "", doc["title"]) in LANDING_LABELS
        ],
        "embedded_media": len(
            re.findall(r"<(?:iframe|video)\b|chapter-video|chapter-videos", all_html, re.I)
        ),
        "badly_numbered_chapters": [
            doc["title"]
            for doc in chapter_docs
            if not re.match(rf"^第{doc['chapterNumber']}章(?:\s|$)", doc["title"])
        ],
        "badly_numbered_headings": badly_numbered_headings,
        "books_with_resource_model": sum("resources" in book for book in catalog["books"]),
        "resource_downloads": len(resource_downloads),
        "missing_resource_downloads": sum(
            not (DIST / Path(unquote(resource["downloadUrl"]))).is_file()
            for resource in resource_downloads
        ),
        "external_resource_links": sum(
            len(book.get("resourceLinks", [])) for book in catalog["books"]
        ),
        "notebooks": sum(item["kind"] == "notebook" for item in code_payloads),
        "missing_code_downloads": sum(
            not (DIST / Path(unquote(item["downloadUrl"]))).is_file()
            for item in code_payloads
        ),
        "machine_learning_code": sum(
            item["bookSlug"] == "zhou-machine-learning" for item in code_payloads
        ),
        "machine_learning_lab_pages": [
            doc["relPath"] for doc in catalog["docs"]
            if doc["bookSlug"] == "zhou-machine-learning" and "tinyml-lab" in doc["relPath"]
        ],
        "machine_learning_book": {
            "documents": machine_learning_book["docCount"],
            "chapters": machine_learning_book["chapterCount"],
            "images": len(machine_learning_images),
            "cover": machine_learning_book["cover"],
        },
        "resource_book_info": "resource-book-info" in app_js,
        "minimal_navigation": (
            "course-resource-link" in app_js
            and "renderResources" in app_js
            and "renderBookOverview" not in app_js
            and "startReadingLink" not in app_js
            and "课程首页" not in app_js
            and "课程安排" not in app_js
        ),
        "resource_first_entry": (
            'var target = "#/resources/" + encodeURIComponent(book.slug)' in app_js
            and 'location.replace("#/resources/" + encodeURIComponent(book.slug))' in app_js
            and 'book.firstDocId ? "#/doc/"' not in app_js
        ),
        "scada_book": {
            "documents": scada_book["docCount"],
            "chapters": scada_book["chapterCount"],
            "images": len(set(scada_image_urls)),
            "missing_images": sum(
                not (DIST / Path(unquote(url))).is_file() for url in scada_image_urls
            ),
            "legacy_vector_images": sum(
                Path(url).suffix.lower() in {".wmf", ".emf"} for url in scada_image_urls
            ),
            "math_fragments": scada_html.count('class="arithmatex"'),
            "formula_images": len(re.findall(r"formula-(?:inline|display)", scada_html)),
            "raw_dollar_delimiters": scada_html.count("$"),
        },
        "python_research_computing": {
            "title": research_computing_doc["title"],
            "code_blocks": research_computing_doc["html"].count("<pre"),
            "tables": research_computing_doc["html"].count("<table"),
            "slide_download": any(
                resource["name"] == "Python科研计算基础与环境搭建.pptx"
                and (DIST / Path(unquote(resource["downloadUrl"]))).is_file()
                for resource in research_book.get("resources", [])
            ),
            "bilibili_video_link": any(
                link.get("url") == "https://www.bilibili.com/video/BV1pVt363EZy/"
                for link in research_book.get("resourceLinks", [])
            ),
            "creator_credit": (
                "内容制作：李锦瑞" in research_computing_doc["html"]
                and any(
                    "李锦瑞" in link.get("label", "")
                    for link in research_book.get("resourceLinks", [])
                )
            ),
        },
        "removed_research_skill_pages": [
            doc["relPath"] for doc in catalog["docs"]
            if doc["bookSlug"] == "research-skills"
            and (
                doc["relPath"].startswith("programming/")
                or doc["relPath"].startswith("research-tools/")
            )
        ],
        "ai_translation_guide": {
            "title": ai_translation_doc["title"],
            "images": len(re.findall(r'<img\b[^>]*\bsrc=', ai_translation_doc["html"], re.I)),
            "missing_images": sum(
                not (DIST / Path(unquote(url))).is_file()
                for url in re.findall(
                    r'<img\b[^>]*\bsrc=["\']([^"\']+)["\']',
                    ai_translation_doc["html"], re.I,
                )
            ),
            "creator_credit": "内容制作：李东" in ai_translation_doc["html"],
            "bilibili_video_link": (
                "https://www.bilibili.com/video/BV1JmtU6kE9T/"
                in ai_translation_doc["html"]
                and any(
                    link.get("url") == "https://www.bilibili.com/video/BV1JmtU6kE9T/"
                    for link in research_book.get("resourceLinks", [])
                )
            ),
        },
        "site_building_guide": {
            "documents": len(site_building_docs),
            "title": payloads[site_building_docs[0]["id"]]["title"],
            "sections": sum(
                heading["level"] == 2
                for heading in payloads[site_building_docs[0]["id"]]["headings"]
            ),
        },
        "standalone_site_building_nav": all(
            token in app_js
            for token in (
                "isStandaloneKnowledgeBase",
                'group.docs[0].relPath === "03-site-building/index.md"',
                'var groupHeading = isStandaloneKnowledgeBase ? ""',
            )
        ),
        "inline_code": all(
            token in app_js for token in ("inlineCodeItem", "loadInlineCode", "展开代码")
        ),
        "code_copy_controls": (
            all(
                token in app_js
                for token in (
                    "enhanceCodeBlocks", "code-copy-button", "navigator.clipboard",
                    'document.execCommand("copy")', "已复制",
                )
            )
            and all(
                token in styles_css
                for token in (".code-block", ".code-toolbar", ".code-copy-button")
            )
        ),
        "home_card_layout": (
            all(
                token in app_js
                for token in ("renderHomeSidebar", "home-category-link", "courseMonogram", "课程资源 →")
            )
            and all(
                token in styles_css
                for token in ("grid-template-columns: repeat(3", ".book-icon", ".book-card footer", ".home-nav-link")
            )
        ),
        "light_code_style": (
            '"JetBrains Mono"' in styles_css
            and "background: #f7f8fa" in styles_css
            and ".highlight .k" in styles_css
            and ".highlight .s" in styles_css
            and "font-size: .88rem" in styles_css
        ),
        "server_side_syntax_highlighting": (
            '"pymdownx.highlight"' in (ROOT / "build.py").read_text(encoding="utf-8")
            and bool(re.search(r'<span class="(?:k|kn|n|s1|s2)">', all_html))
        ),
        "scrollable_outline": all(
            token in styles_css
            for token in (
                "overflow-y: auto", "overscroll-behavior: contain",
                "scrollbar-gutter: stable", ".outline-inner { position: static; }",
            )
        ),
        "song_font_in_css": bool(re.search("宋体|SimSun", styles_css, re.I)),
        "nonblocking_math_loader": (
            'defer src="app.js?v=' in index_html
            and 'async src="https://cdn.jsdelivr.net/npm/mathjax' in index_html
        ),
        "versioned_static_assets": (
            "__ASSET_VERSION__" not in index_html
            and bool(re.search(r"app\.js\?v=[0-9a-f]{12}", index_html))
            and bool(re.search(r"styles\.css\?v=[0-9a-f]{12}", index_html))
        ),
        "server_side_access_gate": all(
            token in worker_js
            for token in (
                "SITE_ACCESS_USERNAME", "SITE_ACCESS_PASSWORD", "WWW-Authenticate",
                "secureEqual", "env.ASSETS.fetch(request)", '"Cache-Control": "no-store"',
            )
        ),
        "managed_account_auth": all(
            token in worker_js
            for token in (
                "SUPABASE_URL", "SUPABASE_PUBLISHABLE_KEY", "__Host-rkh_access",
                "__Host-rkh_refresh", "/__auth/login", "/__auth/logout",
                "/auth/v1/.well-known/jwks.json", "HttpOnly; Secure; SameSite=Lax",
                "TURNSTILE_SECRET_KEY", "ALLOW_LEGACY_BASIC",
            )
        ),
    }

    assert report["stats"] == {"books": 16, "docs": 213, "code": 221}
    assert report["paper_figure_reproduction"] == {
        "title": "论文图片复现",
        "sections": 17,
        "video_present": True,
        "video_size": 10379955,
        "video_linked": True,
        "video_actions": 2,
        "download_action": True,
        "creator_credit": True,
    }
    assert report["research_presentation"] == {
        "documents": 2,
        "images": 11,
        "missing_images": 0,
        "video_present": True,
        "video_size": 14423915,
        "video_linked": True,
        "creator_credit": True,
    }
    assert report["machine_vision_book"] == {
        "documents": 11,
        "chapters": 10,
        "images": 70,
        "missing_images": 0,
    }
    assert report["categories"] == [
        "research-skills", "python", "data-analysis", "artificial-intelligence",
        "robotics", "wind-energy", "engineering-systems",
    ]
    assert report["book_slugs"] == expected_books
    assert report["chapter_documents"] >= 140
    assert not report["landing_documents"]
    assert report["embedded_media"] == 0
    assert not report["badly_numbered_chapters"]
    assert not report["badly_numbered_headings"]
    assert report["books_with_resource_model"] == 16
    assert report["resource_downloads"] >= 13
    assert report["missing_resource_downloads"] == 0
    assert report["external_resource_links"] >= 6
    assert report["notebooks"] == 7
    assert report["missing_code_downloads"] == 0
    assert report["machine_learning_code"] == 34
    assert not report["machine_learning_lab_pages"]
    assert report["machine_learning_book"] == {
        "documents": 18,
        "chapters": 16,
        "images": 122,
        "cover": "files/zhou-machine-learning/assets/cover.jpeg",
    }
    assert report["resource_book_info"]
    assert report["minimal_navigation"]
    assert report["resource_first_entry"]
    assert report["scada_book"] == {
        "documents": 10,
        "chapters": 9,
        "images": 259,
        "missing_images": 0,
        "legacy_vector_images": 0,
        "math_fragments": 2418,
        "formula_images": 0,
        "raw_dollar_delimiters": 0,
    }
    assert report["python_research_computing"]["title"] == "科研计算基础与环境搭建"
    assert report["python_research_computing"]["code_blocks"] >= 80
    assert report["python_research_computing"]["tables"] >= 6
    assert report["python_research_computing"]["slide_download"]
    assert report["python_research_computing"]["bilibili_video_link"]
    assert report["python_research_computing"]["creator_credit"]
    assert not report["removed_research_skill_pages"]
    assert report["ai_translation_guide"] == {
        "title": "Kimi 论文翻译操作指南",
        "images": 7,
        "missing_images": 0,
        "creator_credit": True,
        "bilibili_video_link": True,
    }
    assert report["site_building_guide"] == {
        "documents": 1,
        "title": "知识库搭建",
        "sections": 12,
    }
    assert report["standalone_site_building_nav"]
    assert report["inline_code"]
    assert report["code_copy_controls"]
    assert report["home_card_layout"]
    assert report["light_code_style"]
    assert report["server_side_syntax_highlighting"]
    assert report["scrollable_outline"]
    assert not report["song_font_in_css"]
    assert report["nonblocking_math_loader"]
    assert report["versioned_static_assets"]
    assert report["server_side_access_gate"]
    assert report["managed_account_auth"]

    report["book_slugs"] = sorted(report["book_slugs"])
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
