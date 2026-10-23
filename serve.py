"""Local preview server for the static turismoepuyen.com.ar backup."""

from __future__ import annotations

import os
import re
import sys
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

# Preview config - bind address, port, and which files get origin rewrites.
HOST = "127.0.0.1"
PORT = 8080
REWRITE_EXTENSIONS = {".html", ".htm", ".css", ".js", ".json", ".svg", ".xml"}
ORIGIN_PATTERNS = (
    re.compile(r"https?:\\/\\/turismoepuyen\.com\.ar", re.IGNORECASE),
    re.compile(r"https?://turismoepuyen\.com\.ar", re.IGNORECASE),
    re.compile(r"https?%3A%2F%2Fturismoepuyen\.com\.ar", re.IGNORECASE),
    re.compile(r"//turismoepuyen\.com\.ar", re.IGNORECASE),
)

# Backup root - HTML/CSS/JS/images downloaded into mirror/.
ROOT = Path(__file__).resolve().parent / "mirror"


# Origin rewrite - turn live-site URLs into localhost-relative paths.
def rewrite_origin(text: str) -> str:
    for pattern in ORIGIN_PATTERNS:
        text = pattern.sub("", text)
    return text


# Local preview handler - serves mirror files and rewrites HTML/CSS/JS origins.
class BackupHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, format: str, *args) -> None:
        sys.stderr.write("%s - %s\n" % (self.address_string(), format % args))

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        local_path = Path(self.translate_path(unquote(parsed.path)))

        if local_path.is_dir():
            for name in ("index.html", "index.htm"):
                candidate = local_path / name
                if candidate.is_file():
                    local_path = candidate
                    break

        if local_path.suffix.lower() in REWRITE_EXTENSIONS and local_path.is_file():
            raw = local_path.read_text(encoding="utf-8", errors="replace")
            data = rewrite_origin(raw).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", self.guess_type(str(local_path)))
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(data)
            return

        super().do_GET()


# Server bootstrap - listen on localhost and open the browser.
def main() -> None:
    if not ROOT.is_dir():
        raise SystemExit(f"No se encontro la carpeta del backup: {ROOT}")

    os.chdir(ROOT)
    httpd = ThreadingHTTPServer((HOST, PORT), BackupHandler)
    url = f"http://{HOST}:{PORT}/"
    print(f"Backup local en {url}", flush=True)
    print("Ctrl+C para detener.", flush=True)
    webbrowser.open(url)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
        httpd.server_close()


if __name__ == "__main__":
    main()
