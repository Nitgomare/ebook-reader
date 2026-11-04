"""本地预览 dist 的小服务器。

Python 自带的 `http.server` 不支持 Range 请求：浏览器下载大文件（例如 9.6 MB 的
`pyodide.asm.wasm`、2.5 MB 的 `python_stdlib.zip`）中断后会带 `Range` 续传，而
`SimpleHTTPRequestHandler` 会忽略 `Range` 从头再发一遍，浏览器判定内容不符，最终
表现为「HTTP 204 + 0 字节」。Pyodide 因此报 `Failed to import encodings module`。
这里补上 `Accept-Ranges`/`206 Partial Content`，让本地预览与线上（Cloudflare）一致。
"""

from __future__ import annotations

import re
from http.server import SimpleHTTPRequestHandler
from shutil import copyfileobj

_RANGE = re.compile(r"bytes=(\d*)-(\d*)")


class _Limited:
    """只读取前 limit 个字节的只读文件包装，供 copyfileobj 使用。"""

    def __init__(self, handle, limit: int):
        self.handle = handle
        self.remaining = limit

    def read(self, size: int = -1) -> bytes:
        if self.remaining <= 0:
            return b""
        if size is None or size < 0 or size > self.remaining:
            size = self.remaining
        chunk = self.handle.read(size)
        self.remaining -= len(chunk)
        return chunk


class RangeRequestHandler(SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *args):  # 预览时不需要逐条访问日志
        pass

    def end_headers(self):
        self.send_header("Accept-Ranges", "bytes")
        super().end_headers()

    def send_head(self):
        if not self.headers.get("Range"):
            return super().send_head()

        path = self.translate_path(self.path)
        try:
            handle = open(path, "rb")
        except OSError:
            self.send_error(404, "File not found")
            return None

        import os

        size = os.fstat(handle.fileno()).st_size
        start, end = self._parse_range(self.headers["Range"], size)
        if start is None:
            handle.close()
            self.send_response(416)
            self.send_header("Content-Range", f"bytes */{size}")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return None

        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(path))
        self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.send_header("Content-Length", str(end - start + 1))
        self.end_headers()
        handle.seek(start)
        return _Limited(handle, end - start + 1)

    @staticmethod
    def _parse_range(header: str, size: int):
        match = _RANGE.search(header)
        if not match:
            return None, None
        first, last = match.group(1), match.group(2)
        if first:
            start = int(first)
            end = int(last) if last else size - 1
        else:  # bytes=-500 取末尾 500 字节
            if not last:
                return None, None
            start = max(0, size - int(last))
            end = size - 1
        if start >= size or start > end:
            return None, None
        return start, min(end, size - 1)


def serve(directory, port: int = 8030, quiet: bool = True):
    """在后台线程里起一个支持 Range 的静态服务器，返回 (server, base_url)。"""

    import functools
    import threading
    from http.server import ThreadingHTTPServer

    handler = functools.partial(RangeRequestHandler, directory=str(directory))
    server = ThreadingHTTPServer(("127.0.0.1", port), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{port}"


__all__ = ["RangeRequestHandler", "serve", "copyfileobj"]
