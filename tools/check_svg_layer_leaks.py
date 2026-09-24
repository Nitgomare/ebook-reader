"""批量检测交互图的「渲染泄漏」：把每张图的 HTML 变成自检副本，用无头 Chrome 读回根层残留。

原理：正常实现里，所有动态图形都应落在命名图层（#grid/#axes/#guides/#vectors/#labels）内，
SVG 根层只应有 <defs> 与这些图层；如果 render() 反复触发后根层出现 <g class="fk-grid">
或裸 <line>，说明有元素挂在了根 SVG 上 —— 每次重绘都会累积，形成拖影。

用法：
    ..\\.venv\\Scripts\\python.exe tools\\check_svg_layer_leaks.py            # 扫描两本书全部交互图
    ..\\.venv\\Scripts\\python.exe tools\\check_svg_layer_leaks.py figure-2-6 # 只查一张
输出：tmp/probe/leaks/<figure>.txt（每图的检测报告），并在终端给出汇总。
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BOOKS = ["craig-introduction-to-robotics", "robot-technology-basics"]
PROBE_DIR = REPO / "tmp" / "probe" / "leaks"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PROFILE = REPO / "tmp" / "chrome-leakscan"

INJECT = r"""
<pre id="leak-report" style="position:fixed;left:0;bottom:0;z-index:99;background:#0f172a;color:#e2e8f0;font:11px/1.4 Consolas,monospace;margin:0;padding:6px 8px">probing…</pre>
<script>
(function () {
  var lines = [];
  function log(s) { lines.push(String(s)); var b = document.getElementById("leak-report"); if (b) b.textContent = lines.join("\n"); }
  function snap(tag) {
    var svg = document.getElementById("viewport");
    if (!svg) { log(tag + " | 无 #viewport"); return; }
    // 只统计"由脚本反复绘制、挂在根层"的动态元素：
    // 手写的静态 SVG（如 figure-2-1 的 <line id="vector">）不算泄漏。
    var strayGrid = svg.querySelectorAll(":scope > g.fk-grid").length;
    var strayDynamic = svg.querySelectorAll(":scope > line.fk-vec-line, :scope > line.fk-arc, :scope > line.fk-projection, :scope > polyline, :scope > circle").length;
    log(tag + " | 根层 g.fk-grid=" + strayGrid + " 根层动态图元=" + strayDynamic
      + " 根层子元素=" + svg.childElementCount
      + " 总节点=" + svg.querySelectorAll("*").length);
  }
  function fire(id, times) {
    var el = document.getElementById(id);
    if (!el) return false;
    var lo = Number(el.min), hi = Number(el.max);
    for (var i = 0; i < times; i += 1) {
      if (el.type === "checkbox") { el.checked = !el.checked; el.dispatchEvent(new Event("change", { bubbles: true })); }
      else { el.value = String(lo + (hi - lo) * ((i % 13) / 12)); el.dispatchEvent(new Event("input", { bubbles: true })); }
    }
    return true;
  }
  try {
    snap("1初始");
    var moved = false;
    ["theta", "px", "py", "pz", "dx", "dy", "dz", "t1", "t2", "t3", "l1", "l2", "d", "d2", "psi"].forEach(function (id) {
      if (fire(id, 12)) moved = true;
    });
    ["showMid", "showGuide", "showMatrix", "auto"].forEach(function (id) { fire(id, 4); });
    var tabs = ["tabTrans", "tabRot", "tabEuler", "tabFixed", "tabB", "tabA"];
    tabs.forEach(function (id) { var el = document.getElementById(id); if (el) { el.click(); el.click(); } });
    snap("2高频操作后" + (moved ? "" : "（未找到滑块）"));
    var reset = document.getElementById("reset");
    if (reset) reset.click();
    snap("3重置后");
    var svg = document.getElementById("viewport");
    var stray = svg.querySelectorAll(":scope > g.fk-grid").length
      + svg.querySelectorAll(":scope > line.fk-vec-line, :scope > line.fk-arc, :scope > line.fk-projection, :scope > polyline, :scope > circle").length;
    log(stray === 0 ? "结论：PASS（根层无动态残留）" : "结论：FAIL（根层有 " + stray + " 个动态残留，每次重绘会累积）");
  } catch (error) {
    log("! 异常：" + error.message);
  }
}());
</script>
"""


def figure_files(only: str | None) -> list[tuple[str, Path]]:
    found: list[tuple[str, Path]] = []
    for book in BOOKS:
        folder = REPO / "content" / "books" / book / "docs" / "interactive"
        for path in sorted(folder.glob("figure-*.html")):
            if only and path.stem != only:
                continue
            # 手写静态 SVG（不使用 FK.Scene）的图不参与本检测：
            # 它们的根层元素是初始标记，不会随渲染累积。
            html = path.read_text(encoding="utf-8")
            if "new FK.Scene(" not in html and "new FK.AdaptiveScene(" not in html:
                print(f"SKIP {path.stem:22} 未使用 FK.Scene（手写静态 SVG）")
                continue
            found.append((book, path))
    return found


def main() -> None:
    parser = argparse.ArgumentParser(description="扫描交互图的 SVG 图层泄漏")
    parser.add_argument("figure", nargs="?", help="只检查某一张，如 figure-2-6")
    args = parser.parse_args()

    PROBE_DIR.mkdir(parents=True, exist_ok=True)
    PROFILE.mkdir(parents=True, exist_ok=True)
    results: list[tuple[str, str, int, int]] = []

    for book, path in figure_files(args.figure):
        html = path.read_text(encoding="utf-8")
        injected = html.replace("</body>", INJECT + "\n</body>", 1) if "</body>" in html else html + INJECT
        probe = PROBE_DIR / f"{path.stem}.probe.html"
        probe.write_text(injected, encoding="utf-8")
        url = probe.resolve().as_uri()
        try:
            completed = subprocess.run(
                [CHROME, "--headless", "--disable-gpu", "--no-sandbox", "--no-first-run",
                 f"--user-data-dir={PROFILE}", "--virtual-time-budget=8000", "--dump-dom", url],
                capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=180,
            )
            dom = completed.stdout or ""
        except subprocess.TimeoutExpired:
            dom = ""
        match = re.search(r'<pre id="leak-report"[^>]*>(.*?)</pre>', dom, re.S)
        report = (match.group(1) if match else "未取到报告").strip()
        (PROBE_DIR / f"{path.stem}.txt").write_text(report, encoding="utf-8")
        final = re.search(r"2高频操作后[^\n]*", report)
        numbers = re.search(r"根层 g\.fk-grid=(\d+) 根层动态图元=(\d+)", final.group(0)) if final else None
        stray_grid = int(numbers.group(1)) if numbers else -1
        stray_line = int(numbers.group(2)) if numbers else -1
        status = "PASS" if stray_grid == 0 and stray_line == 0 else ("FAIL" if stray_grid > 0 or stray_line > 0 else "N/A")
        results.append((path.stem, status, stray_grid, stray_line))
        print(f"{status:4} {path.stem:22} 根层残留: g.fk-grid={stray_grid} 动态图元={stray_line}")

    print("\n=== 汇总 ===")
    failed = [item for item in results if item[1] == "FAIL"]
    print(f"共 {len(results)} 张：PASS {len([i for i in results if i[1] == 'PASS'])}、"
          f"FAIL {len(failed)}、未知 {len([i for i in results if i[1] == 'N/A'])}")
    for name, _status, grid, line in failed:
        print(f"  FAIL {name}: 根层 g.fk-grid={grid} 裸line={line}")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
