"""下载浏览器内 Python 运行时（Pyodide）到 vendor/pyodide/，供构建时复制进 dist。

设计要点：
- 只下载真正会用到的核心文件与科学计算包的闭包，避免 300 MB 的完整发行版。
- 每个文件按 pyodide-lock.json 的 sha256 校验，已存在且校验通过就跳过。
- vendor/pyodide/ 不进版本库（.gitignore），换机器后跑一次本脚本即可。
- 下载失败时构建仍然成功，前端会回退到公共 CDN 镜像。

用法：
    python tools/fetch_pyodide.py                      # 默认科学计算包
    python tools/fetch_pyodide.py --packages numpy     # 只下 numpy
    python tools/fetch_pyodide.py --mirror https://fastly.jsdelivr.net/pyodide
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VENDOR = ROOT / "vendor" / "pyodide"
VERSION = "314.0.7"
MIRRORS = [
    "https://gcore.jsdelivr.net/pyodide",
    "https://fastly.jsdelivr.net/pyodide",
    "https://cdn.jsdelivr.net/pyodide",
]
CORE_FILES = [
    "pyodide.mjs",
    "pyodide.asm.mjs",
    "pyodide.asm.wasm",
    "python_stdlib.zip",
    "pyodide-lock.json",
]
DEFAULT_PACKAGES = ["numpy", "pandas", "matplotlib", "scipy", "sympy", "scikit-learn"]


def download(url: str, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    partial = target.with_suffix(target.suffix + ".part")
    request = urllib.request.Request(url, headers={"User-Agent": "ebook-reader-fetch-pyodide"})
    with urllib.request.urlopen(request, timeout=120) as response, partial.open("wb") as handle:
        while True:
            chunk = response.read(256 * 1024)
            if not chunk:
                break
            handle.write(chunk)
    partial.replace(target)


def fetch_mirror(base: str, name: str) -> str:
    return f"{base}/v{VERSION}/full/{name}"


def ensure_file(base: str, name: str, expected_sha256: str | None = None) -> bool:
    target = VENDOR / name
    if target.exists():
        if expected_sha256:
            digest = hashlib.sha256(target.read_bytes()).hexdigest()
            if digest == expected_sha256:
                print(f"  已存在  {name}")
                return True
        else:
            print(f"  已存在  {name}")
            return True
        print(f"  校验不符，重新下载  {name}")
    print(f"  下载    {name}")
    download(fetch_mirror(base, name), target)
    if expected_sha256:
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        if digest != expected_sha256:
            target.unlink(missing_ok=True)
            raise SystemExit(f"sha256 校验失败：{name}")
    return True


def dependency_closure(packages: dict[str, dict], seeds: list[str]) -> list[str]:
    seen: set[str] = set()
    stack = [name for name in seeds if name in packages]
    missing = [name for name in seeds if name not in packages]
    if missing:
        print(f"  跳过未知包：{', '.join(missing)}")
    while stack:
        name = stack.pop()
        if name in seen:
            continue
        seen.add(name)
        stack.extend(packages[name].get("depends", []))
    return sorted(seen)


def main() -> int:
    parser = argparse.ArgumentParser(description="下载 Pyodide 运行时到 vendor/pyodide/")
    parser.add_argument("--packages", default=",".join(DEFAULT_PACKAGES),
                        help="逗号分隔的包名，默认下载科学计算常用包")
    parser.add_argument("--mirror", default="", help="指定镜像前缀，默认按顺序尝试")
    parser.add_argument("--force", action="store_true", help="忽略已有文件强制重新下载")
    args = parser.parse_args()

    seeds = [item.strip() for item in args.packages.split(",") if item.strip()]
    bases = [args.mirror] if args.mirror else MIRRORS
    if args.force:
        VENDOR.mkdir(parents=True, exist_ok=True)

    base = ""
    for candidate in bases:
        try:
            probe = urllib.request.Request(fetch_mirror(candidate, "pyodide-lock.json"),
                                           headers={"User-Agent": "ebook-reader-fetch-pyodide"})
            urllib.request.urlopen(probe, timeout=45).read()
            base = candidate
            break
        except Exception as error:  # noqa: BLE001 - 换下一个镜像
            print(f"  镜像不可用：{candidate}（{error}）")
    if not base:
        print("所有镜像都不可用，构建时前端会自行回退到 CDN。")
        return 1

    print(f"使用镜像：{base}")
    print("核心文件：")
    for name in CORE_FILES:
        ensure_file(base, name)

    lock = json.loads((VENDOR / "pyodide-lock.json").read_text(encoding="utf-8"))
    packages = lock["packages"]
    closure = dependency_closure(packages, seeds)
    print(f"依赖闭包：{len(closure)} 个包（{', '.join(closure)}）")
    for name in closure:
        entry = packages[name]
        ensure_file(base, entry["file_name"], entry["sha256"])

    total = sum(path.stat().st_size for path in VENDOR.rglob("*") if path.is_file())
    print(f"完成：{len(list(VENDOR.rglob('*')))} 个文件，共 {total / 1e6:.1f} MB，目录 {VENDOR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
