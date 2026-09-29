#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""机器人课程资源中心 · 页面自检

做两件事：
  1. 检查所有页面里的相对链接（href/src）指向的文件是否真的存在；
  2. 检查页内锚点（#xxx）在目标页面里是否存在；
  3. 顺带检查主要标签是否配平（漏闭合的 div/section 之类）。

用法：
    python check_links.py                 # 检查本目录下的页面
    python check_links.py <目录>          # 检查指定目录（例如发布包）

退出码：0 = 全部通过；1 = 存在缺失链接或标签问题。
"""

import os
import re
import sys
import urllib.parse
from html.parser import HTMLParser

ROOT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
SKIP_SCHEMES = ("http://", "https://", "mailto:", "tel:", "data:", "javascript:")

VOID = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}
# 这些标签允许自闭合写法，也允许不闭合（HTML 里可省略）
OPTIONAL_CLOSE = {"p", "li", "dt", "dd", "thead", "tbody", "tr", "td", "th", "option"}


class Scan(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.links = []      # (tag, attr, value, line)
        self.ids = set()
        self.stack = []
        self.errors = []

    def _attrs(self, tag, attrs):
        d = dict(attrs)
        if d.get("id"):
            self.ids.add(d["id"])
        for key in ("href", "src"):
            if d.get(key):
                self.links.append((tag, key, d[key], self.getpos()[0]))

    def handle_starttag(self, tag, attrs):
        self._attrs(tag, attrs)
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_startendtag(self, tag, attrs):
        self._attrs(tag, attrs)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if tag in OPTIONAL_CLOSE:
            # 允许被隐式闭合：从栈顶往下找最近一个同名标签
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i][0] == tag:
                    del self.stack[i:]
                    return
            return
        if not self.stack:
            self.errors.append("第 %d 行：多余的结束标签 </%s>" % (self.getpos()[0], tag))
            return
        top, line = self.stack.pop()
        if top != tag:
            self.errors.append(
                "第 %d 行：<%s>（第 %d 行开始）被 </%s> 关闭，标签不配平"
                % (self.getpos()[0], top, line, tag)
            )


def load(path):
    with open(path, "rb") as fp:
        return fp.read().decode("utf-8")


def main():
    pages = sorted(f for f in os.listdir(ROOT) if f.endswith(".html"))
    if not pages:
        print("没有找到 HTML 页面")
        return 1

    page_data = {}
    fatal = 0

    # 第一遍：解析所有页面，收集 id 与链接
    for name in pages:
        path = os.path.join(ROOT, name)
        scan = Scan()
        try:
            scan.feed(load(path))
        except Exception as exc:  # noqa: BLE001
            print("[解析失败] %s: %s" % (name, exc))
            fatal += 1
            continue
        for tag, line in scan.stack:
            scan.errors.append("第 %d 行：<%s> 未闭合" % (line, tag))
        page_data[name] = scan

    # 第二遍：校验链接
    total_links = 0
    missing_files = []
    missing_anchors = []

    for name in pages:
        scan = page_data.get(name)
        if scan is None:
            continue
        base = os.path.dirname(os.path.join(ROOT, name))
        for tag, attr, value, line in scan.links:
            low = value.strip()
            if not low or low.startswith(SKIP_SCHEMES) or low.startswith("#"):
                if low.startswith("#") and len(low) > 1:
                    target = low[1:]
                    if target not in scan.ids:
                        missing_anchors.append((name, line, low, name))
                continue
            total_links += 1
            target_file, _, anchor = low.partition("#")
            decoded = urllib.parse.unquote(target_file)
            abs_path = os.path.normpath(os.path.join(base, decoded))
            if not os.path.exists(abs_path):
                missing_files.append((name, line, low, os.path.relpath(abs_path, ROOT)))
                continue
            if anchor and target_file.lower().endswith(".html"):
                key = os.path.basename(decoded)
                other = page_data.get(key)
                if other is not None and anchor not in other.ids:
                    missing_anchors.append((name, line, low, key))

    # 输出
    print("=" * 68)
    print("页面：%d 个 -> %s" % (len(pages), ", ".join(pages)))
    print("相对链接：%d 条" % total_links)
    print("=" * 68)

    for name in pages:
        scan = page_data.get(name)
        if scan and scan.errors:
            print("\n[标签问题] %s" % name)
            for err in scan.errors:
                print("   -", err)
            fatal += len(scan.errors)

    if missing_files:
        print("\n[链接目标不存在] %d 条" % len(missing_files))
        for name, line, value, resolved in missing_files:
            print("   - %s 第 %d 行 -> %s" % (name, line, resolved))
            print("       %s" % value)
        fatal += len(missing_files)

    if missing_anchors:
        print("\n[锚点不存在] %d 条" % len(missing_anchors))
        for name, line, value, target in missing_anchors:
            print("   - %s 第 %d 行 -> %s (%s)" % (name, line, value, target))
        fatal += len(missing_anchors)

    if not fatal:
        print("\n全部通过：链接、锚点与标签配平均正常。")
    else:
        print("\n发现问题：%d 处。" % fatal)
    return 1 if fatal else 0


if __name__ == "__main__":
    sys.exit(main())
