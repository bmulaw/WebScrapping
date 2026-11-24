"""Tools for the check.py files that need Chrome. You do not need to change (or even read) this file.

check.py starts a LOCAL COPY of the website: a small web server inside Python, on http://127.0.0.1:<port>.
It serves the real pages saved in samples/ and a fake API that answers like the real one. Chrome runs your code
on this copy: no request ever reaches the real website (and no internet is needed, except the very first time,
when Selenium downloads the right chromedriver).
"""
import base64
import json
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

PNG = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==")
TYPES = {".html": "text/html; charset=utf-8", ".json": "application/json", ".js": "text/javascript",
         ".css": "text/css", ".png": "image/png", ".txt": "text/plain; charset=utf-8"}


class QuietServer(ThreadingHTTPServer):
    daemon_threads = True

    def handle_error(self, request, client_address):
        """Chrome often leaves a page while an answer is still being sent: not an error for us, say nothing."""


class LocalSite:
    """A local copy of a website.

    pages:  {"/path": html_text}                         -> GET /path answers this HTML
    routes: {"POST /api/x": function(body, query)}       -> the function returns (status, json_data)
    Every request is saved in .hits as (method, path). /img/... always answers a tiny PNG.
    """

    def __init__(self, pages=None, routes=None, folder=None):
        self.pages, self.routes, self.folder, self.hits = pages or {}, routes or {}, folder, []
        site = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_GET(self):
                site._handle(self, "GET")

            def do_POST(self):
                site._handle(self, "POST")

            def send(self, status, body, content_type):
                self.send_response(status)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(body)

        self.server = QuietServer(("127.0.0.1", 0), Handler)
        self.port = self.server.server_address[1]
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def url(self, path="/"):
        return f"http://127.0.0.1:{self.port}{path}"

    def _handle(self, handler, method):
        parts = urlsplit(handler.path)
        self.hits.append((method, parts.path))
        body = handler.rfile.read(int(handler.headers.get("Content-Length") or 0)) if method == "POST" else b""
        route = self.routes.get(f"{method} {parts.path}")
        if route:
            try:
                data = json.loads(body or b"{}")
            except json.JSONDecodeError:
                data = None
            status, answer = route(data, parse_qs(parts.query))
            return handler.send(status, json.dumps(answer, ensure_ascii=False).encode("utf-8"), "application/json")
        if parts.path in self.pages:
            return handler.send(200, self.pages[parts.path].encode("utf-8"), TYPES[".html"])
        if parts.path.startswith("/img/"):
            return handler.send(200, PNG, "image/png")
        if self.folder:
            file = Path(self.folder) / parts.path.lstrip("/")
            if file.is_file():
                return handler.send(200, file.read_bytes(), TYPES.get(file.suffix, "application/octet-stream"))
        handler.send(404, b"<h1>Not found (local copy)</h1>", TYPES[".html"])

    def close(self):
        self.server.shutdown()
        self.server.server_close()


def test_driver():
    """A headless Chrome FOR THE CHECKS, independent of your make_driver (so you can do the exercises in any order).
    Network logging is on, like in the lesson."""
    from selenium import webdriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1400,1000")
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    return webdriver.Chrome(options=options)


def wait_until(condition, timeout=10):
    """Wait (in the check, not in your code) until condition() is true. Returns its last value."""
    end = time.time() + timeout
    value = condition()
    while not value and time.time() < end:
        time.sleep(0.1)
        value = condition()
    return value
