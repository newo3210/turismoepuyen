"""Fetch the latest Instagram posts via Graph API and refresh the homepage cards."""

from __future__ import annotations

import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# Paths - repo root, homepage, JSON feed, and downloaded post images.
ROOT = Path(__file__).resolve().parents[1]
MIRROR = ROOT / "mirror"
FEED_JSON = MIRROR / "data" / "instagram-posts.json"
IMAGE_DIR = MIRROR / "media" / "instagram"
HOME = MIRROR / "index.html"
ENV_FILES = (ROOT / ".env", ROOT / "instagram.env")
PROFILE_URL = "https://www.instagram.com/turismoepuyen/"
GRAPH_VERSION = "v21.0"
POST_LIMIT = 2
FEED_START = "<!-- instagram-feed:start -->"
FEED_END = "<!-- instagram-feed:end -->"


# Env loading - read KEY=VALUE from local env files without extra dependencies.
def load_env() -> None:
    for path in ENV_FILES:
        if not path.is_file():
            continue
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip("'").strip('"')
            os.environ.setdefault(key, value)


def graph_get(url: str) -> dict:
    context = ssl.create_default_context()
    request = urllib.request.Request(url, headers={"User-Agent": "turismoepuyen-static/1.0"})
    try:
        with urllib.request.urlopen(request, context=context, timeout=30) as response:
            payload = response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Instagram Graph API {error.code}: {detail}") from error
    return json.loads(payload)


def download_image(url: str, dest: Path) -> str:
    dest.parent.mkdir(parents=True, exist_ok=True)
    context = ssl.create_default_context()
    request = urllib.request.Request(url, headers={"User-Agent": "turismoepuyen-static/1.0"})
    with urllib.request.urlopen(request, context=context, timeout=60) as response:
        dest.write_bytes(response.read())
    return f"/media/instagram/{dest.name}"


def split_caption(caption: str) -> tuple[str, str]:
    text = (caption or "").strip()
    if not text:
        return "Novedades de Epuyén", "Mirá la publicación original en Instagram."
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    title = lines[0][:90]
    rest = text[len(lines[0]) :].strip() if lines else ""
    body = (rest or text).replace("\n", " ")
    if len(body) > 220:
        body = body[:217].rstrip() + "…"
    return title, body


def html_escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def card_html(post: dict, index: int) -> str:
    tone = "teal" if index == 0 else "green"
    title, body = split_caption(post.get("caption") or "")
    href = post.get("permalink") or PROFILE_URL
    image = post.get("local_image") or post.get("media_url") or ""
    photo = (
        f'<img src="{html_escape(image)}" alt="{html_escape(title)}" loading="lazy" decoding="async">'
        if image
        else '<div class="ig-feed__photo-empty">@turismoepuyen</div>'
    )
    return f"""
    <article class="ig-feed__card ig-feed__card--{tone}">
      <div class="ig-feed__photo">{photo}</div>
      <div class="ig-feed__body">
        <h3 class="ig-feed__title">{html_escape(title)}</h3>
        <p class="ig-feed__excerpt">{html_escape(body)}</p>
        <a class="ig-feed__more" href="{html_escape(href)}" target="_blank" rel="noopener noreferrer">Conocer más</a>
      </div>
    </article>
    """


def fallback_posts() -> list[dict]:
    return [
        {
            "id": "demo-lago",
            "caption": "Lago Epuyén\nPaisajes de la cordillera, directo desde @turismoepuyen.",
            "permalink": PROFILE_URL,
            "local_image": "/media/instagram/demo-lago.jpg",
        },
        {
            "id": "demo-playas",
            "caption": "Las playas del lago\nAgua cristalina y montaña, para planear la próxima visita.",
            "permalink": PROFILE_URL,
            "local_image": "/media/instagram/demo-playas.jpg",
        },
    ]


def feed_section_html(posts: list[dict]) -> str:
    cards = "".join(card_html(post, index) for index, post in enumerate(posts[:POST_LIMIT] or fallback_posts()))
    return f"""{FEED_START}
<section class="ig-feed" id="novedades-instagram" aria-label="Novedades de Instagram">
  <div class="ig-feed__inner">
    <span class="ig-feed__eyebrow">Instagram</span>
    <h2 class="ig-feed__heading">Novedades</h2>
    <div class="ig-feed__grid" data-ig-feed-grid>
      {cards}
    </div>
  </div>
</section>
{FEED_END}
"""


def patch_homepage(posts: list[dict]) -> None:
    html = HOME.read_text(encoding="utf-8")
    start = html.find(FEED_START)
    end = html.find(FEED_END)
    if start == -1 or end == -1:
        raise SystemExit("No se encontraron los marcadores instagram-feed en index.html")
    end += len(FEED_END)
    HOME.write_text(html[:start] + feed_section_html(posts).rstrip() + html[end:], encoding="utf-8")


def media_url_for(item: dict, token: str, host: str) -> str:
    media_type = (item.get("media_type") or "").upper()
    if media_type == "VIDEO":
        return item.get("thumbnail_url") or item.get("media_url") or ""
    if media_type == "CAROUSEL_ALBUM":
        children = item.get("children", {}).get("data") or []
        if children:
            child_id = children[0]["id"]
            child_url = (
                f"https://{host}/{GRAPH_VERSION}/{urllib.parse.quote(child_id)}"
                f"?fields=media_type,media_url,thumbnail_url"
                f"&access_token={urllib.parse.quote(token)}"
            )
            child = graph_get(child_url)
            if (child.get("media_type") or "").upper() == "VIDEO":
                return child.get("thumbnail_url") or child.get("media_url") or ""
            return child.get("media_url") or ""
    return item.get("media_url") or item.get("thumbnail_url") or ""


def fetch_posts(token: str, user_id: str, host: str) -> list[dict]:
    user = user_id or "me"
    fields = "id,caption,media_type,media_url,permalink,timestamp,thumbnail_url,children{id,media_type,media_url,thumbnail_url}"
    url = (
        f"https://{host}/{GRAPH_VERSION}/{urllib.parse.quote(user)}/media"
        f"?fields={urllib.parse.quote(fields, safe=',{}')}"
        f"&limit=8&access_token={urllib.parse.quote(token)}"
    )
    data = graph_get(url)
    items = data.get("data") or []
    posts: list[dict] = []
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    for item in items:
        if len(posts) >= POST_LIMIT:
            break
        image_url = media_url_for(item, token, host)
        local_image = ""
        post_id = re.sub(r"[^A-Za-z0-9_-]", "", str(item.get("id") or "")) or f"post-{len(posts)}"
        if image_url:
            ext = ".jpg"
            parsed = urllib.parse.urlparse(image_url)
            suffix = Path(parsed.path).suffix.lower()
            if suffix in {".jpg", ".jpeg", ".png", ".webp"}:
                ext = suffix
            local_image = download_image(image_url, IMAGE_DIR / f"{post_id}{ext}")
        posts.append(
            {
                "id": item.get("id"),
                "caption": item.get("caption") or "",
                "permalink": item.get("permalink") or PROFILE_URL,
                "timestamp": item.get("timestamp"),
                "media_type": item.get("media_type"),
                "local_image": local_image,
            }
        )

    keep = {Path(post["local_image"]).name for post in posts if post.get("local_image")}
    for leftover in IMAGE_DIR.glob("*"):
        if not leftover.is_file():
            continue
        if leftover.name in keep or leftover.name == ".gitkeep" or leftover.name.startswith("demo-"):
            continue
        leftover.unlink()
    return posts


def main() -> None:
    load_env()
    token = os.environ.get("IG_ACCESS_TOKEN", "").strip()
    user_id = os.environ.get("IG_USER_ID", "").strip()
    host = os.environ.get("IG_GRAPH_HOST", "graph.instagram.com").strip() or "graph.instagram.com"

    if not token:
        print(
            "Falta IG_ACCESS_TOKEN. Instagram no deja scrapear el feed público.\n"
            "Creá un token de la Graph API (cuenta profesional) y guardalo en .env o en un secret de GitHub.\n"
            "Mientras tanto la home muestra el acceso a https://www.instagram.com/turismoepuyen/",
            file=sys.stderr,
        )
        demo_posts = fallback_posts()
        patch_homepage(demo_posts)
        FEED_JSON.parent.mkdir(parents=True, exist_ok=True)
        FEED_JSON.write_text(
            json.dumps(
                {
                    "account": "turismoepuyen",
                    "profile_url": PROFILE_URL,
                    "updated_at": None,
                    "demo": True,
                    "posts": demo_posts,
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        raise SystemExit(2)

    posts = fetch_posts(token, user_id, host)
    payload = {
        "account": "turismoepuyen",
        "profile_url": PROFILE_URL,
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "posts": posts,
    }
    FEED_JSON.parent.mkdir(parents=True, exist_ok=True)
    FEED_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    patch_homepage(posts)
    print(f"Actualizados {len(posts)} posts de Instagram en la home.")


if __name__ == "__main__":
    main()
