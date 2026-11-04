"""浏览器内 Python 运行时的端到端检查（Playwright + 本机 Chrome）。

覆盖四件事：
1. 公式：MathJax 换镜像回退后仍能渲染正文里的 arithmatex 公式。
2. .ipynb：代码视图出现运行工具条，逐个单元的「▶ 运行」能跑出结果。
3. .py：源码视图的「▶ 在浏览器中运行」能跑出 stdout 与末表达式。
4. 运行时同源加载：请求落在 /pyodide/ 下，不走第三方 CDN。

用法：python tools/check_python_runtime.py [--keep]
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
SHOTS = ROOT / "tmp" / "python-runtime-qa"
CHROME = "C:/Program Files/Google/Chrome/Application/chrome.exe"
BOOK = "robot-simulation-programming"
PORT = 8031

sys.path.insert(0, str(ROOT / "tools"))
from dev_server import serve  # noqa: E402


def start_server():
    return serve(DIST, PORT)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--keep", action="store_true", help="保留截图")
    parser.parse_args()

    catalog = json.loads((DIST / "data" / "catalog.json").read_text(encoding="utf-8"))
    notebook = next(
        item for item in catalog["code"]
        if item["bookSlug"] == BOOK and item["kind"] == "notebook" and "chapter-1" in item["path"]
    )
    doc = next(
        item for item in catalog["docs"]
        if item["bookSlug"] == BOOK and item.get("chapterNumber") == 1
    )
    SHOTS.mkdir(parents=True, exist_ok=True)
    server, base = start_server()
    failures: list[str] = []
    console_errors: list[str] = []
    runtime_requests: list[str] = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=CHROME, headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 1000})
        page.on("console", lambda message: console_errors.append(message.text)
                if message.type == "error" and "status of 404" not in message.text else None)
        page.on("pageerror", lambda error: console_errors.append(str(error)))
        page.on("response", lambda response: runtime_requests.append(response.url)
                if "/pyodide/" in response.url else None)
        page.on("response", lambda response: console_errors.append(f"{response.status} {response.url}")
                if response.status >= 400 and not response.url.endswith(("/__auth/status", "/favicon.ico"))
                else None)

        # 1. 公式渲染
        page.goto(f"{base}/#/doc/{doc['id']}", wait_until="load")
        page.wait_for_function("() => document.querySelector('#article')?.textContent.length > 200")
        page.wait_for_timeout(6000)
        formulas = page.evaluate("""() => ({
            arithmatex: document.querySelectorAll('#article .arithmatex').length,
            rendered: document.querySelectorAll('#article mjx-container').length
        })""")
        print(f"公式：arithmatex {formulas['arithmatex']} 处，已渲染 {formulas['rendered']} 处")
        if formulas["arithmatex"] and not formulas["rendered"]:
            failures.append("MathJax 没有渲染出 mjx-container")

        # 2. Notebook：运行一个单元
        page.goto(f"{base}/#/code/{notebook['id']}", wait_until="load")
        page.wait_for_selector(".py-run-bar", timeout=20000)
        info = page.evaluate("""() => ({
            cells: document.querySelectorAll('.notebook-cell').length,
            runnable: document.querySelectorAll('.cell--runnable').length,
            buttons: document.querySelectorAll('.cell-run-button').length,
            badges: [...new Set([...document.querySelectorAll('.cell-kind')].map(n => n.textContent))]
        })""")
        print(f"Notebook：{info['cells']} 个单元，可运行 {info['runnable']} 个，按钮 {info['buttons']} 个，"
              f"识别类型 {info['badges']}")
        if not info["buttons"]:
            failures.append("Notebook 里没有生成单格运行按钮")

        picked = page.evaluate("""() => {
            const cells = [...document.querySelectorAll('.notebook-cell.cell--runnable')];
            const scored = cells.map((cell, i) => {
                const code = cell.querySelector('pre > code')?.textContent || '';
                let score = code.length;
                if (!/import |from /.test(code) && /print\\(|=|\\d/.test(code)) score -= 500;
                return { i, score, code };
            }).sort((a, b) => a.score - b.score);
            return scored.length ? scored[0] : null;
        }""")
        if picked:
            print(f"挑中第 {picked['i']} 个可运行单元：{picked['code'][:60]!r}")
            page.evaluate("""(index) => {
                const cells = [...document.querySelectorAll('.notebook-cell.cell--runnable')];
                cells[index].querySelector('.cell-run-button').click();
            }""", picked["i"])
            page.wait_for_selector(".cell-run-output .py-output-header", timeout=300000)
            page.wait_for_timeout(500)
            result = page.evaluate("""() => {
                const header = document.querySelector('.cell-run-output .py-output-header');
                const out = header?.parentElement;
                return {
                    header: header?.textContent || '',
                    error: Boolean(header?.classList.contains('is-error')),
                    stdout: out?.querySelector('.py-stdout')?.textContent || '',
                    expression: out?.querySelector('.py-expression')?.textContent || '',
                    hint: out?.querySelector('.py-output-hint')?.textContent || '',
                    status: document.querySelector('.py-run-status')?.textContent || ''
                };
            }""")
            print(f"单格运行：{result['header']}")
            if result["stdout"]:
                print(f"  stdout: {result['stdout'][:120]!r}")
            if result["expression"]:
                print(f"  表达式: {result['expression'][:80]!r}")
            if result["error"]:
                print(f"  报错提示: {result['hint'][:120]!r}")
                failures.append("单格运行没有跑通（详见上面的报错）")
            page.screenshot(path=str(SHOTS / "notebook-run.png"), full_page=False)

        # 3. .py：源码视图运行
        page.evaluate("""async () => {
            const host = document.createElement('div');
            host.id = 'py-sandbox';
            document.body.appendChild(host);
            window.PythonPlayground.mount(host, {
                id: 'sandbox',
                kind: 'code',
                language: 'python',
                content: 'import sys\\nprint("hello", sys.version.split()[0])\\nx = 6 * 7\\nx'
            });
        }""")
        page.wait_for_selector("#py-sandbox .py-run-button", timeout=10000)
        page.click("#py-sandbox .py-run-button")
        page.wait_for_selector("#py-sandbox .py-output-header", timeout=300000)
        page.wait_for_timeout(500)
        sandbox = page.evaluate("""() => ({
            out: document.querySelector('#py-sandbox .py-stdout')?.textContent || '',
            expr: document.querySelector('#py-sandbox .py-expression')?.textContent || '',
            error: Boolean(document.querySelector('#py-sandbox .py-output-header.is-error'))
        })""")
        print(f".py 运行：stdout={sandbox['out']!r} 表达式={sandbox['expr']!r}")
        if sandbox["error"] or "hello" not in sandbox["out"] or "42" not in sandbox["expr"]:
            failures.append(".py 文件运行结果不符合预期")
        page.screenshot(path=str(SHOTS / "python-file-run.png"), full_page=False)

        # 4. 同源加载
        same_origin = all(url.startswith(base) for url in runtime_requests)
        print(f"运行时请求 {len(runtime_requests)} 个，全部同源：{same_origin}")
        if runtime_requests and not same_origin:
            failures.append("运行时资源没走同源 /pyodide/")

        browser.close()

    server.shutdown()
    if console_errors:
        unique = sorted(set(console_errors))
        print("控制台错误：")
        for item in unique[:10]:
            print("  " + item[:200])
        failures.append(f"{len(unique)} 条控制台错误")
    print(f"截图：{SHOTS}")
    if failures:
        print("未通过：")
        for item in failures:
            print("  - " + item)
        return 1
    print("全部通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
