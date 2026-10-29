# Apply lodging/service directory - JSON phone cleanup, cards+map HTML, Servicios page, nav.
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIRROR = ROOT / "mirror"

DIR_STAY = """<div class="directorio" data-directorio data-src="/data/alojamientos.json" data-kind="stay">
<p class="directorio__eyebrow">Dónde alojarse</p>
<h2 class="directorio__title">Alojamientos en Epuyén</h2>
<p class="directorio__lead">Elegí un establecimiento, ubicalo en el mapa y escribilé o llamalo desde acá. Cada ficha se puede abrir, ver en el mapa y contratar directo por WhatsApp, teléfono o mail.</p>
<div class="directorio__toolbar">
<div class="directorio__filters" data-filters></div>
<label class="directorio__search"><span class="screen-reader-text">Buscar alojamiento</span><input type="search" data-search placeholder="Buscar por nombre, zona o dirección"></label>
</div>
<div class="directorio__layout">
<div class="directorio__map-wrap">
<div class="directorio__map" data-map></div>
<p class="directorio__map-note">Los pines usan la geolocalización del padrón de Turismo. Si falta el link de Maps, el pin queda en la zona.</p>
</div>
<div class="directorio__list" data-list></div>
</div>
<dialog class="directorio__sheet" data-sheet>
<button type="button" class="directorio__sheet-close" data-sheet-close aria-label="Cerrar">×</button>
<div class="directorio__sheet-photo" data-sheet-photo></div>
<div class="directorio__sheet-body">
<h3 data-sheet-title></h3>
<p data-sheet-meta></p>
<p data-sheet-note></p>
<div class="directorio__sheet-actions" data-sheet-actions></div>
</div>
</dialog>
</div>
"""

DIR_SVC = DIR_STAY.replace("/data/alojamientos.json", "/data/servicios.json")
DIR_SVC = DIR_SVC.replace('data-kind="stay"', 'data-kind="service"')
DIR_SVC = DIR_SVC.replace("Dónde alojarse", "Servicios turísticos")
DIR_SVC = DIR_SVC.replace("Alojamientos en Epuyén", "Servicios en Epuyén")
DIR_SVC = DIR_SVC.replace(
    "Elegí un establecimiento, ubicalo en el mapa y escribilé o llamalo desde acá. Cada ficha se puede abrir, ver en el mapa y contratar directo por WhatsApp, teléfono o mail.",
    "Agencias, excursiones, guías y remises para armar la estadía. Cada servicio se puede ver en el mapa y contactar directo desde la página.",
)
DIR_SVC = DIR_SVC.replace("Buscar alojamiento", "Buscar servicio")
DIR_SVC = DIR_SVC.replace(
    "Los pines usan la geolocalización del padrón de Turismo. Si falta el link de Maps, el pin queda en la zona.",
    "Los pines usan la geolocalización del padrón. Remises y guías sin dirección quedan en el casco de Epuyén.",
)

HEAD = """<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin="">
<link rel="stylesheet" href="/assets/directorio.css">
"""
FOOT = """<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin=""></script>
<script src="/assets/directorio.js"></script>
"""

NAV_ITEM = (
    '<li id="menu-item-servicios" class="menu-item menu-item-type-post_type '
    'menu-item-object-page menu-item-servicios"><a href="https://turismoepuyen.com.ar/servicios/" '
    'class="menu-link">Servicios</a></li>\n'
)
NAV_FOOT = (
    '<li class="menu-item menu-item-type-post_type menu-item-object-page menu-item-servicios">'
    '<a href="https://turismoepuyen.com.ar/servicios/" class="menu-link">Servicios</a></li>\n'
)
CONTACT_DESKTOP = (
    '<li id="menu-item-828" class="menu-item menu-item-type-post_type '
    'menu-item-object-page menu-item-828"><a href="https://turismoepuyen.com.ar/contacto/" '
    'class="menu-link">Contacto</a></li>'
)
CONTACT_FOOT = (
    '<li class="menu-item menu-item-type-post_type menu-item-object-page menu-item-828">'
    '<a href="https://turismoepuyen.com.ar/contacto/" class="menu-link">Contacto</a></li>'
)

DIR_FOOD = DIR_STAY.replace("/data/alojamientos.json", "/data/gastronomia.json")
DIR_FOOD = DIR_FOOD.replace('data-kind="stay"', 'data-kind="food"')
DIR_FOOD = DIR_FOOD.replace("Dónde alojarse", "Dónde comer")
DIR_FOOD = DIR_FOOD.replace("Alojamientos en Epuyén", "Gastronomía en Epuyén")
DIR_FOOD = DIR_FOOD.replace(
    "Elegí un establecimiento, ubicalo en el mapa y escribilé o llamalo desde acá. Cada ficha se puede abrir, ver en el mapa y contratar directo por WhatsApp, teléfono o mail.",
    "Restaurantes, confiterías, rotiserías y fábricas locales. Cada local se puede ver en el mapa y contactar directo desde la página.",
)
DIR_FOOD = DIR_FOOD.replace("Buscar alojamiento", "Buscar gastronomía")


# Argentine phone cleanup - tel for call links, wa digits with the 9 prefix.
def normalize_phone(raw: str) -> dict[str, str] | None:
    raw = (raw or "").strip()
    digits = re.sub(r"\D", "", raw)
    if len(digits) < 8:
        return None
    if digits.startswith("54"):
        rest = digits[2:]
    elif digits.startswith("0"):
        rest = digits.lstrip("0")
    else:
        rest = digits
    if rest.startswith("1115") and len(rest) >= 12:
        national = "911" + rest[4:]
        return {"raw": raw, "tel": "+54" + national, "wa": "54" + national}
    tel_rest = rest[1:] if rest.startswith("9") else rest
    wa_rest = rest if rest.startswith("9") else "9" + rest
    return {"raw": raw, "tel": "+54" + tel_rest, "wa": "54" + wa_rest}


# Listing phone/mail pass - drop junk emails into notes and rebuild WhatsApp digits.
def patch_item(item: dict) -> dict:
    phones = []
    seen: set[str] = set()
    for phone in item.get("phones") or []:
        norm = normalize_phone(phone.get("raw") or phone.get("wa") or "")
        if not norm or norm["wa"] in seen:
            continue
        seen.add(norm["wa"])
        phones.append(norm)
    item["phones"] = phones
    item["whatsapp"] = phones[0]["wa"] if phones else ""
    mail = (item.get("email") or "").strip()
    if mail and "@" not in mail:
        item["notes"] = mail
        item["email"] = ""
    return item


# Service categories - infer Agencia / Excursiones / Guía when the Excel left them blank.
def infer_service_cat(item: dict) -> None:
    cats = item.get("categories") or []
    if cats and cats not in ([], ["Servicio"], [""]):
        return
    blob = (item.get("name", "") + " " + item.get("responsable", "")).lower()
    if "eputur" in blob or "viaje" in blob:
        item["categories"] = ["Agencia"]
    elif "trekking" in blob or "bonito" in blob or "aventura" in blob:
        item["categories"] = ["Excursiones"]
    elif item.get("name") == item.get("responsable") or not item.get("name"):
        item["categories"] = ["Guía"]
        if not item.get("name"):
            item["name"] = item.get("responsable") or "Servicio"
    else:
        item["categories"] = ["Turismo"]


# JSON files - rewrite phones and service labels after the HTML table extract.
def patch_json() -> None:
    for name in ("alojamientos.json", "servicios.json", "gastronomia.json"):
        path = MIRROR / "data" / name
        data = json.loads(path.read_text(encoding="utf-8"))
        for item in data["items"]:
            patch_item(item)
            if name == "servicios.json":
                infer_service_cat(item)
                if "chofer" in item.get("id", ""):
                    item["name"] = "Chofer Pablo"
                    item["notes"] = item.get("notes") or "Auto Toyota Etios blanco"
                    item["categories"] = ["Remís"]
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(name, len(data["items"]))


# Map-note swap - keep already-converted directory pages in sync with the Excel pins.
def patch_map_notes() -> None:
    replacements = {
        MIRROR / "alojamientos" / "index.html": (
            '<p class="directorio__map-note">Los pines marcan la zona del establecimiento. El padrón no trae coordenada de puerta.</p>',
            '<p class="directorio__map-note">Los pines usan la geolocalización del padrón de Turismo. Si falta el link de Maps, el pin queda en la zona.</p>',
        ),
        MIRROR / "servicios" / "index.html": (
            '<p class="directorio__map-note">Si no hay dirección exacta, el pin queda en el casco de Epuyén. El padrón no trae coordenadas de puerta.</p>',
            '<p class="directorio__map-note">Los pines usan la geolocalización del padrón. Remises y guías sin dirección quedan en el casco de Epuyén.</p>',
        ),
    }
    for path, (old, new) in replacements.items():
        html = path.read_text(encoding="utf-8")
        if old in html:
            path.write_text(html.replace(old, new), encoding="utf-8")
            print("note", path.parent.name)


# Gastronomía page - swap the old table for the same cards+map directory.
def patch_gastronomia() -> None:
    path = MIRROR / "gastronomia" / "index.html"
    html = path.read_text(encoding="utf-8")
    if 'data-src="/data/gastronomia.json"' in html:
        print("gastronomia already patched")
        return
    start = html.find("<style>\n\n.gastro-wrapper {")
    if start < 0:
        start = html.find("<style>\n.gastro-wrapper {")
    end = html.find('<div class="elementor-element elementor-element-0cb3e70')
    if start < 0 or end < 0:
        raise SystemExit(f"gastronomia markers missing start={start} end={end}")
    html = html[:start] + DIR_FOOD + "\n\t\t\t\t</div>\n\t\t\t\t</div>\n\t\t\t\t</div>\n\t\t" + html[end:]
    if "/assets/directorio.css" not in html:
        html = html.replace("</head>", HEAD + "</head>", 1)
    if "/assets/directorio.js" not in html:
        html = html.replace("</body>", FOOT + "</body>", 1)
    path.write_text(html, encoding="utf-8")
    print("gastronomia patched")


# Alojamientos page - swap the Excel table for the directory module.
def patch_alojamientos() -> str:
    path = MIRROR / "alojamientos" / "index.html"
    html = path.read_text(encoding="utf-8")
    start = html.find("<style>\n.prestadores-wrapper {")
    end = html.find(
        '<section class="elementor-section elementor-top-section elementor-element elementor-element-f03ded5'
    )
    if start < 0 or end < 0:
        raise SystemExit(f"prestadores markers missing start={start} end={end}")
    html = html[:start] + DIR_STAY + html[end:]
    if "/assets/directorio.css" not in html:
        html = html.replace("</head>", HEAD + "</head>", 1)
    if "/assets/directorio.js" not in html:
        html = html.replace("</body>", FOOT + "</body>", 1)
    path.write_text(html, encoding="utf-8")
    print("alojamientos patched")
    return html


# Servicios page - clone Alojamientos with its own JSON, title, and current menu item.
def write_servicios(aloj_html: str) -> None:
    html = aloj_html
    html = html.replace("Alojamientos &#8211; Turismo Epuyén", "Servicios &#8211; Turismo Epuyén")
    html = html.replace(
        'rel="canonical" href="https://turismoepuyen.com.ar/alojamientos/"',
        'rel="canonical" href="https://turismoepuyen.com.ar/servicios/"',
    )
    html = html.replace(
        "https%3A%2F%2Fturismoepuyen.com.ar%2Falojamientos%2F",
        "https%3A%2F%2Fturismoepuyen.com.ar%2Fservicios%2F",
    )
    html = html.replace(
        "current-menu-item page_item page-item-672 current_page_item menu-item-678",
        "menu-item-678",
    )
    html = html.replace(
        'aria-current="page" class="menu-link">Alojamientos',
        'class="menu-link">Alojamientos',
    )
    html = html.replace(DIR_STAY, DIR_SVC)
    out = MIRROR / "servicios"
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(html, encoding="utf-8")
    print("servicios written")


# Site nav - insert Servicios before Contacto on visitor-facing HTML pages.
def insert_nav() -> None:
    changed = 0
    for path in MIRROR.rglob("*.html"):
        rel = path.relative_to(MIRROR).as_posix()
        if rel.startswith("wp-json/") or "/feed/" in rel:
            continue
        text = path.read_text(encoding="utf-8")
        orig = text
        if "menu-item-servicios" not in text:
            text = text.replace(CONTACT_DESKTOP, NAV_ITEM + CONTACT_DESKTOP)
            text = text.replace(CONTACT_FOOT, NAV_FOOT + CONTACT_FOOT)
        if path == MIRROR / "servicios" / "index.html":
            text = text.replace(
                'menu-item-servicios"><a href="https://turismoepuyen.com.ar/servicios/" class="menu-link">Servicios</a>',
                'menu-item-servicios current-menu-item"><a href="https://turismoepuyen.com.ar/servicios/" aria-current="page" class="menu-link">Servicios</a>',
            )
        if text != orig:
            path.write_text(text, encoding="utf-8")
            changed += 1
    print("nav files", changed)


def main() -> None:
    patch_json()
    patch_map_notes()
    patch_gastronomia()
    stay_path = MIRROR / "alojamientos" / "index.html"
    if "<style>\n.prestadores-wrapper {" in stay_path.read_text(encoding="utf-8"):
        aloj_html = patch_alojamientos()
        write_servicios(aloj_html)
        insert_nav()


if __name__ == "__main__":
    main()
