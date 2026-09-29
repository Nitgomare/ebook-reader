#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""生成「机器人课程资源中心」的可部署发布包。

发布包结构（落到 ebook-reader/public/robot-hub/，构建后即出现在 dist/robot-hub/）：

    robot-hub/
      index.html  ros-mobile.html  go2.html  vision-sorting.html  abb-baxter.html
      assets/hub.css  assets/hub.js
      机器人相关课程from文丽/<保留下来的原始资料>
      RELEASE.md

处理规则：
  1. 视频一律不上传（.mp4 .avi .mov .mkv .wmv .m4v .mpg .flv）；
  2. 单文件超过 --max-mb（默认 25，Cloudflare Pages 免费版单文件上限）不上传；
  3. 临时文件（~$ 开头）与缓存（__pycache__、*.pyc）不上传；
  4. 页面中指向“未上传文件”的链接改写成文字标注，避免线上死链；
  5. 页面里的 ../机器人相关课程from文丽/ 前缀改写为 机器人相关课程from文丽/。

用法：
    python build_release.py                # 输出到 ../ebook-reader/public/robot-hub
    python build_release.py --out <目录>
    python build_release.py --dry-run      # 只报告，不写任何文件
"""

import argparse
import json
import os
import re
import shutil
import sys
import urllib.parse
import zipfile

SITE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(SITE))
RES_SRC = os.path.join(os.path.dirname(REPO), "机器人相关课程from文丽")
DEFAULT_OUT = os.path.join(REPO, "public", "robot-hub")

PREFIX_OLD = "../机器人相关课程from文丽/"
PREFIX_NEW = "机器人相关课程from文丽/"

VIDEO_EXT = {".mp4", ".avi", ".mov", ".mkv", ".wmv", ".m4v", ".mpg", ".flv", ".webm"}
SKIP_DIRS = {"__pycache__"}


def contains_video(path):
    """排除 Office 或 ZIP 中的内嵌视频，避免仅按外部扩展名筛选。"""
    if os.path.splitext(path)[1].lower() not in {".pptx", ".docx", ".xlsx", ".zip"}:
        return False
    with zipfile.ZipFile(path) as archive:
        return any(os.path.splitext(name)[1].lower() in VIDEO_EXT for name in archive.namelist())

ANCHOR_RE = re.compile(r'<a\s+href="([^"]+)"([^>]*)>(.*?)</a>', re.S)


def excluded_reason(name, size, max_bytes):
    """返回排除原因；None 表示可以发布。"""
    if name.startswith("~$"):
        return "Office 临时文件"
    if os.path.splitext(name)[1].lower() in VIDEO_EXT:
        return "视频（不上传）"
    if size > max_bytes:
        return "单文件超过 %.0f MB 上限" % (max_bytes / 1048576)
    return None


def scan_resources(max_bytes):
    """遍历原始资料，返回 (可发布集合, 被排除清单)。"""
    included = {}
    excluded = []
    for dirpath, dirnames, filenames in os.walk(RES_SRC):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in sorted(filenames):
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, RES_SRC).replace("\\", "/")
            size = os.path.getsize(full)
            reason = excluded_reason(name, size, max_bytes)
            if name.endswith(".pyc"):
                reason = "Python 缓存"
            if not reason and contains_video(full):
                reason = "包含内嵌视频（不上传）"
            if reason:
                excluded.append({"path": rel, "size": size, "reason": reason})
            else:
                included[rel] = size
    return included, excluded


def rewrite_page(text, included):
    """改写单页：未发布资源的链接降级为文字，资源前缀去掉 ../。返回 (新文本, 未上线条目数)。"""
    missed = []

    def repl(match):
        href, attrs, label = match.group(1), match.group(2), match.group(3)
        if PREFIX_OLD not in href:
            return match.group(0)
        rel = urllib.parse.unquote(href.split(PREFIX_OLD, 1)[1])
        if rel in included:
            return match.group(0)
        missed.append(rel)
        plain = re.sub(r"<[^>]+>", "", label).strip()
        return '<span class="txt">%s</span><span class="meta">暂未上线</span>' % plain

    text = ANCHOR_RE.sub(repl, text)
    text = text.replace(PREFIX_OLD, PREFIX_NEW)
    document_count = sum(os.path.splitext(rel)[1].lower() in {".pdf", ".docx", ".pptx"} for rel in included)
    text = text.replace(
        '<strong>64</strong><span>静态课件与指导书</span>',
        '<strong>%d</strong><span>已上线课件与指导书</span>' % document_count
    )
    text = text.replace(
        '<nav class="coursenav" aria-label="课程导航">',
        '<nav class="coursenav" aria-label="课程导航"><a href="../#/">学习中心</a>'
    )
    # 展示稿的发布规划不作为线上课程内容，避免与实际筛选结果矛盾。
    text = re.sub(r'<section class="section" id="policy">.*?</section>', '', text, flags=re.S)
    text = text.replace('状态：页面已建，课件减重与视频接入待做', '视频链接待补')
    text = text.replace('内容依据：机器人课程资源中心-展示稿', '课程资料按平台与教学任务编排')
    text = text.replace(
        '本页为课程导航页，不含视频与原始课程文件；原始资料位于 <code>机器人相关课程from文丽/</code>，保持只读。',
        '资料提供：文丽 · 讲义、课件与源码按教学任务整理 · 视频链接待补。'
    )

    return text, missed


def human(size):
    if size >= 1048576:
        return "%.1f MB" % (size / 1048576)
    if size >= 1024:
        return "%.0f KB" % (size / 1024)
    return "%d B" % size


def main():
    parser = argparse.ArgumentParser(description="生成机器人课程资源中心的发布包")
    parser.add_argument("--out", default=DEFAULT_OUT, help="输出目录（默认为 ebook-reader/public/robot-hub）")
    parser.add_argument("--max-mb", type=float, default=25.0, help="单文件体积上限（MB），默认 25")
    parser.add_argument("--dry-run", action="store_true", help="只报告，不写文件")
    args = parser.parse_args()

    if not os.path.isdir(RES_SRC):
        print("找不到原始资料目录：%s" % RES_SRC)
        return 1

    max_bytes = int(args.max_mb * 1024 * 1024)
    included, excluded = scan_resources(max_bytes)
    total = sum(included.values())

    pages = sorted(f for f in os.listdir(SITE) if f.endswith(".html"))
    out = os.path.abspath(args.out)

    print("=" * 72)
    print("源站点    : %s" % SITE)
    print("原始资料  : %s" % RES_SRC)
    print("输出目录  : %s%s" % (out, "（dry-run，不写入）" if args.dry_run else ""))
    print("单文件上限: %.0f MB" % args.max_mb)
    print("=" * 72)
    print("可发布资源：%d 个 / %s" % (len(included), human(total)))
    print("排除资源  ：%d 个 / %s" % (len(excluded), human(sum(e["size"] for e in excluded))))

    by_reason = {}
    for item in excluded:
        key = item["reason"].split("，")[0]
        by_reason.setdefault(key, []).append(item)
    for reason, items in sorted(by_reason.items(), key=lambda kv: -len(kv[1])):
        print("   - %-28s %d 个 / %s" % (reason, len(items), human(sum(i["size"] for i in items))))

    rewritten = {}
    for name in pages:
        text = open(os.path.join(SITE, name), encoding="utf-8").read()
        new_text, missed = rewrite_page(text, included)
        rewritten[name] = (new_text, missed)
        if missed:
            print("   ! %s：%d 个入口降级为“未上线”标注" % (name, len(missed)))

    if args.dry_run:
        print("\ndry-run 结束，未写入任何文件。")
        return 0

    if os.path.normcase(out) != os.path.normcase(os.path.abspath(DEFAULT_OUT)):
        raise ValueError("发布输出必须是项目 public/robot-hub，避免覆盖其他目录")
    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(out)

    for name in pages:
        with open(os.path.join(out, name), "w", encoding="utf-8") as fp:
            fp.write(rewritten[name][0])

    shutil.copytree(os.path.join(SITE, "assets"), os.path.join(out, "assets"))

    copied = 0
    for rel in sorted(included):
        src = os.path.join(RES_SRC, rel.replace("/", os.sep))
        dst = os.path.join(out, "机器人相关课程from文丽", rel.replace("/", os.sep))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        copied += 1

    notes = [
        "# 发布包说明（自动生成）",
        "",
        "本目录由 `tools/robot-hub/build_release.py` 生成，对应线上路径 `/robot-hub/`。",
        "不要直接改这里的文件：改源站点或原始资料后重新运行该脚本即可。",
        "",
        "## 内容",
        "",
        "- 页面：%s" % "、".join(pages),
        "- 资源：`机器人相关课程from文丽/` 下 %d 个文件，合计 %s" % (copied, human(total)),
        "- 排除：%d 个文件，合计 %s" % (len(excluded), human(sum(e["size"] for e in excluded))),
        "",
        "## 排除规则",
        "",
        "1. 视频一律不上传；",
        "   Office 课件与 ZIP 包内嵌的视频同样排除。",
        "2. 单文件超过 %.0f MB（Cloudflare Pages 免费版单文件上限）不上传；" % args.max_mb,
        "3. Office 临时文件（`~$` 开头）与 Python 缓存（`__pycache__`、`*.pyc`）不上传。",
        "",
        "## 未上线的文件",
        "",
        "| 文件 | 体积 | 原因 |",
        "| --- | --- | --- |",
    ]
    for item in sorted(excluded, key=lambda i: -i["size"]):
        notes.append("| `%s` | %s | %s |" % (item["path"], human(item["size"]), item["reason"]))
    notes += [
        "",
        "## 重新生成",
        "",
        "```powershell",
        "# 在 ebook-reader 仓库根目录执行",
        "..\\.venv\\Scripts\\python.exe tools/robot-hub/build_release.py",
        "..\\.venv\\Scripts\\python.exe tools/robot-hub/check_links.py public/robot-hub",
        "```",
        "",
    ]
    with open(os.path.join(out, "RELEASE.md"), "w", encoding="utf-8") as fp:
        fp.write("\n".join(notes))

    with open(os.path.join(out, "release-manifest.json"), "w", encoding="utf-8") as fp:
        json.dump(
            {
                "pages": pages,
                "included_count": copied,
                "included_bytes": total,
                "excluded_count": len(excluded),
                "excluded_bytes": sum(e["size"] for e in excluded),
                "excluded": excluded,
            },
            fp,
            ensure_ascii=False,
            indent=2,
        )

    print("\n已写出：%s" % out)
    print("  - 页面 %d 个 + assets/" % len(pages))
    print("  - 资源 %d 个 / %s" % (copied, human(total)))
    print("  - RELEASE.md 与 release-manifest.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
