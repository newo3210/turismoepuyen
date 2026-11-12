# Patch section pages - wire section-hero parallax CSS/JS on page-hero pages.
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1] / "mirror"
css_href = "/assets/section-hero.css?v=4"
js_src = "/assets/section-hero.js?v=4"
css_tag = f'<link rel="stylesheet" href="{css_href}">'
js_tag = f'<script src="{js_src}" defer></script>'

skip = {
    "r",
    "tag",
    "feed",
    "wp-json",
    "category",
    "author",
    "2024",
    "elementor-hf",
    "turismo-epuyen",
}

css_re = re.compile(r'<link[^>]+section-hero\.css[^>]*>\s*', re.I)
js_re = re.compile(r'<script[^>]+section-hero\.js[^>]*>\s*</script>\s*', re.I)

changed = []
for path in sorted(root.rglob("index.html")):
    rel = path.relative_to(root)
    if any(part in skip for part in rel.parts[:-1]):
        continue
    original = path.read_text(encoding="utf-8", errors="ignore")
    if "page-hero" not in original:
        continue

    text = css_re.sub("", original)
    text = js_re.sub("", text)
    if "</head>" not in text or "</body>" not in text:
        continue
    text = text.replace("</head>", f"{css_tag}\n</head>", 1)
    text = text.replace("</body>", f"{js_tag}\n</body>", 1)

    if text != original:
        path.write_text(text, encoding="utf-8")
        changed.append(str(rel).replace("\\", "/"))

print("Patched", len(changed), "pages:")
for item in changed:
    print(" -", item)
