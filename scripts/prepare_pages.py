"""Build a GitHub Pages copy of the static mirror with rewritten URLs."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

# Paths - repo root, live mirror, and default Pages output folder.
ROOT = Path(__file__).resolve().parents[1]
MIRROR = ROOT / "mirror"
DEFAULT_OUT = ROOT / "_site"
DEFAULT_BASE = "/turismoepuyen"
TEXT_SUFFIXES = {".html", ".htm", ".css", ".js", ".json", ".svg", ".xml", ".txt"}

# Origin rewrite - strip the live domain so paths become root-relative.
ORIGIN_PATTERNS = (
    re.compile(r"https?:\\/\\/turismoepuyen\.com\.ar", re.IGNORECASE),
    re.compile(r"https?://turismoepuyen\.com\.ar", re.IGNORECASE),
    re.compile(r"https?%3A%2F%2Fturismoepuyen\.com\.ar", re.IGNORECASE),
    re.compile(r"//turismoepuyen\.com\.ar", re.IGNORECASE),
)


# CLI flags - output folder and GitHub Pages base path.
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare mirror/ for GitHub Pages")
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="Output directory")
    parser.add_argument("--base", default=DEFAULT_BASE, help="Pages base path, e.g. /turismoepuyen")
    return parser.parse_args()


# Origin strip - turn https://turismoepuyen.com.ar/foo into /foo.
def strip_origin(text: str) -> str:
    for pattern in ORIGIN_PATTERNS:
        text = pattern.sub("", text)
    return text


# Base prefix - /assets/foo becomes /turismoepuyen/assets/foo on project Pages.
def prefix_base(text: str, base: str) -> str:
    base = base.rstrip("/")
    if not base:
        return text

    slug = re.escape(base.lstrip("/"))
    quoted = re.compile(
        rf'(?P<pre>["\']|url\(\s*["\']?)'
        rf'(?P<path>/(?!/)(?!{slug}/)[^"\'\)\s]*)',
        re.IGNORECASE,
    )
    text = quoted.sub(lambda m: f"{m.group('pre')}{base}{m.group('path')}", text)

    escaped_root = re.compile(rf'(["\'])\\/(?!\\/)(?!{slug}\\/)')
    text = escaped_root.sub(rf'\1\\/{base.lstrip("/")}\\/', text)
    return text


# File rewrite - apply origin + base transforms to one text file.
def rewrite_file(path: Path, base: str) -> None:
    raw = path.read_text(encoding="utf-8", errors="replace")
    path.write_text(prefix_base(strip_origin(raw), base), encoding="utf-8")


# Site copy - duplicate mirror/, rewrite text, and disable Jekyll.
def build_site(out_dir: Path, base: str) -> None:
    if not MIRROR.is_dir():
        raise SystemExit(f"No se encontro la carpeta del espejo: {MIRROR}")

    if out_dir.exists():
        shutil.rmtree(out_dir)
    shutil.copytree(MIRROR, out_dir, ignore=shutil.ignore_patterns("__pycache__"))
    (out_dir / ".nojekyll").write_text("", encoding="utf-8")

    for path in out_dir.rglob("*"):
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
            rewrite_file(path, base)


# Entry point - build _site for the GitHub Pages workflow.
def main() -> None:
    args = parse_args()
    out_dir = Path(args.out).resolve()
    build_site(out_dir, args.base)
    print(f"Preview listo en {out_dir} (base {args.base or '/'})", flush=True)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
