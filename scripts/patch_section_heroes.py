# Patch section heroes - hide overlay titles and add mountain waves like home.
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1] / "mirror"
css_href = "/assets/section-hero.css?v=2"
css_tag = f'<link rel="stylesheet" href="{css_href}">'

shape_html = """						<div class="elementor-shape elementor-shape-bottom" aria-hidden="true" data-negative="false">
			<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 100" preserveAspectRatio="none">
	<path class="elementor-shape-fill" opacity="0.33" d="M473,67.3c-203.9,88.3-263.1-34-320.3,0C66,119.1,0,59.7,0,59.7V0h1000v59.7 c0,0-62.1,26.1-94.9,29.3c-32.8,3.3-62.8-12.3-75.8-22.1C806,49.6,745.3,8.7,694.9,4.7S492.4,59,473,67.3z"/>
	<path class="elementor-shape-fill" opacity="0.66" d="M734,67.3c-45.5,0-77.2-23.2-129.1-39.1c-28.6-8.7-150.3-10.1-254,39.1 s-91.7-34.4-149.2,0C115.7,118.3,0,39.8,0,39.8V0h1000v36.5c0,0-28.2-18.5-92.1-18.5C810.2,18.1,775.7,67.3,734,67.3z"/>
	<path class="elementor-shape-fill" d="M766.1,28.9c-200-57.5-266,65.5-395.1,19.5C242,1.8,242,5.4,184.8,20.6C128,35.8,132.3,44.9,89.9,52.5C28.6,63.7,0,0,0,0 h1000c0,0-9.9,40.9-83.6,48.1S829.6,47,766.1,28.9z"/>
</svg>		</div>
"""

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

# Broken attribute from first patch pass: class="...middle" page-hero data-id
broken_re = re.compile(
    r'(class="elementor-section elementor-top-section[^"]*elementor-section-height-min-height[^"]*)"\s+page-hero(\s+data-id=)'
)
section_re = re.compile(
    r'(<section class=")(elementor-section elementor-top-section[^"]*elementor-section-height-min-height[^"]*)(")([^>]*>)([\s\S]{0,3500}?)(</section>)'
)
h1_re = re.compile(r'<h1 class="elementor-heading-title[^"]*">[^<]*</h1>')
css_anywhere_re = re.compile(r'<link[^>]+section-hero\.css[^>]*>\s*', re.I)


def ensure_css_in_head(text: str) -> str:
    text = css_anywhere_re.sub("", text)
    return text.replace("</head>", f"{css_tag}\n</head>", 1)


def patch_section(match: re.Match) -> str:
    prefix, classes, quote, attrs, body, close = match.groups()
    if not h1_re.search(body):
        return match.group(0)
    if "page-hero" not in classes:
        classes = f"{classes} page-hero"
    if "data-settings=" in attrs:
        if "shape_divider_bottom" not in attrs:
            attrs = attrs.replace(
                'data-settings="{',
                'data-settings="{&quot;shape_divider_bottom&quot;:&quot;mountains&quot;,',
                1,
            )
    else:
        attrs = (
            ' data-settings="{&quot;shape_divider_bottom&quot;:&quot;mountains&quot;}"'
            + attrs
        )
    if "elementor-shape-bottom" not in body:
        insert_at = body.find('<div class="elementor-container')
        if insert_at == -1:
            body = body + shape_html
        else:
            body = body[:insert_at] + shape_html + body[insert_at:]
    return f"{prefix}{classes}{quote}{attrs}{body}{close}"


changed = []
for path in sorted(root.rglob("index.html")):
    rel = path.relative_to(root)
    if any(part in skip for part in rel.parts[:-1]):
        continue
    original = path.read_text(encoding="utf-8", errors="ignore")
    text = broken_re.sub(r'\1 page-hero"\2', original)
    match = section_re.search(text)
    if not match or not h1_re.search(match.group(0)):
        continue
    text, n = section_re.subn(patch_section, text, count=1)
    if n == 0:
        continue
    text = ensure_css_in_head(text)
    if text != original:
        path.write_text(text, encoding="utf-8")
        changed.append(str(rel).replace("\\", "/"))

print("Patched", len(changed), "pages:")
for item in changed:
    print(" -", item)
