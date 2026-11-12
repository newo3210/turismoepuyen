# Replace Actividades Elementor list with paired sticky tarjetones (no buttons).
from pathlib import Path
import re

path = Path(__file__).resolve().parents[1] / "mirror" / "actividades" / "index.html"
text = path.read_text(encoding="utf-8")

cards = """
<!-- actividades-cards:start -->
<section class="actividades-cards" id="actividades-listado" aria-label="Actividades en Epuyén">
  <section class="actividades-cards__pair" data-page-story data-beats="2" data-hold="0.35" data-pace="1.15">
    <div class="actividades-cards__stage" data-page-story-pin>
      <div class="actividades-cards__inner">
        <div class="actividades-cards__grid">
          <article class="actividades-cards__card actividades-cards__card--teal">
            <div class="actividades-cards__photo" data-story-beat="0">
              <img src="https://turismoepuyen.com.ar/wp-content/uploads/2024/04/conocenos.webp" alt="Senderismo en Epuyén" loading="lazy" decoding="async">
            </div>
            <div class="actividades-cards__body">
              <p class="actividades-cards__num" data-story-beat="1">01</p>
              <h3 class="actividades-cards__title" data-story-beat="1">Senderismo</h3>
              <p class="actividades-cards__excerpt" data-story-beat="1">Parque Municipal con miradores, área de recreación y senderos turísticos entre bosques y aguas puras.</p>
            </div>
          </article>
          <article class="actividades-cards__card actividades-cards__card--green">
            <div class="actividades-cards__photo" data-story-beat="0">
              <img src="https://turismoepuyen.com.ar/wp-content/uploads/elementor/thumbs/maxresdefault-qnhm3tcdh6dzr09cuf8fc6uqx0doo52ta3vl6ladyk.jpg" alt="Laguna Las Mercedes" loading="lazy" decoding="async">
            </div>
            <div class="actividades-cards__body">
              <p class="actividades-cards__num" data-story-beat="1">02</p>
              <h3 class="actividades-cards__title" data-story-beat="1">Laguna Las Mercedes</h3>
              <p class="actividades-cards__excerpt" data-story-beat="1">En la reserva El Coihue, a 12 km del casco urbano por ruta 70 hacia El Maitén, con acceso de ripio.</p>
            </div>
          </article>
        </div>
      </div>
    </div>
  </section>
  <section class="actividades-cards__pair" data-page-story data-beats="2" data-hold="0.35" data-pace="1.15">
    <div class="actividades-cards__stage" data-page-story-pin>
      <div class="actividades-cards__inner">
        <div class="actividades-cards__grid">
          <article class="actividades-cards__card actividades-cards__card--teal">
            <div class="actividades-cards__photo" data-story-beat="0">
              <img src="https://turismoepuyen.com.ar/wp-content/uploads/2024/05/CoeRNgpHTNRzmvo-800x450-noPad-1.jpg" alt="Centro Cultural Antú Quillén" loading="lazy" decoding="async">
            </div>
            <div class="actividades-cards__body">
              <p class="actividades-cards__num" data-story-beat="1">03</p>
              <h3 class="actividades-cards__title" data-story-beat="1">Centro Cultural Antú Quillén</h3>
              <p class="actividades-cards__excerpt" data-story-beat="1">Más de 20 años de arte y cultura en Puerto Bonito, en un entorno natural único.</p>
            </div>
          </article>
          <article class="actividades-cards__card actividades-cards__card--green">
            <div class="actividades-cards__photo" data-story-beat="0">
              <img src="/media/stupa/stupa.jpg" alt="Stupa de Samantabhadra" loading="lazy" decoding="async">
            </div>
            <div class="actividades-cards__body">
              <p class="actividades-cards__num" data-story-beat="1">04</p>
              <h3 class="actividades-cards__title" data-story-beat="1">Stupa de Samantabhadra</h3>
              <p class="actividades-cards__excerpt" data-story-beat="1">Monumento budista de 12 metros, abierto de día todo el año, con banderas de oración y ruedas.</p>
            </div>
          </article>
        </div>
      </div>
    </div>
  </section>
  <section class="actividades-cards__pair" data-page-story data-beats="2" data-hold="0.35" data-pace="1.15">
    <div class="actividades-cards__stage" data-page-story-pin>
      <div class="actividades-cards__inner">
        <div class="actividades-cards__grid">
          <article class="actividades-cards__card actividades-cards__card--teal">
            <div class="actividades-cards__photo" data-story-beat="0">
              <img src="https://turismoepuyen.com.ar/wp-content/uploads/2024/05/molino.jpg" alt="Molino Harinero" loading="lazy" decoding="async">
            </div>
            <div class="actividades-cards__body">
              <p class="actividades-cards__num" data-story-beat="1">05</p>
              <h3 class="actividades-cards__title" data-story-beat="1">Molino Harinero</h3>
              <p class="actividades-cards__excerpt" data-story-beat="1">A orillas del río Minas: molienda artesanal desde 1914, con harinas de la zona y visita al público.</p>
            </div>
          </article>
        </div>
      </div>
    </div>
  </section>
</section>
<!-- actividades-cards:end -->
"""

# Replace previous cards block or legacy Elementor list.
if "actividades-cards:start" in text:
    pattern = re.compile(
        r"<!-- actividades-cards:start -->[\s\S]*?<!-- actividades-cards:end -->\s*",
        re.M,
    )
    new_text, n = pattern.subn(cards.strip() + "\n", text, count=1)
else:
    pattern = re.compile(
        r'<section class="elementor-section elementor-top-section elementor-element elementor-element-0016efd[\s\S]*?</section>\s*(?=<section class="elementor-section elementor-top-section elementor-element elementor-element-ad9b2ac)',
        re.M,
    )
    new_text, n = pattern.subn(cards + "\n\t\t\t\t", text, count=1)

if n != 1:
    raise SystemExit(f"replace failed: {n}")

new_text = new_text.replace("actividades-cards.css?v=1", "actividades-cards.css?v=3")
new_text = new_text.replace("actividades-cards.css?v=2", "actividades-cards.css?v=3")
new_text = new_text.replace("actividades-cards.js?v=1", "actividades-cards.js?v=3")
new_text = new_text.replace("actividades-cards.js?v=2", "actividades-cards.js?v=3")

if "actividades-cards.css" not in new_text:
    new_text = new_text.replace(
        'href="/assets/section-hero.css?v=7">',
        'href="/assets/section-hero.css?v=7">\n<link rel="stylesheet" href="/assets/actividades-cards.css?v=3">',
        1,
    )
if "actividades-cards.js" not in new_text:
    new_text = new_text.replace(
        'src="/assets/section-hero.js?v=7" defer></script>',
        'src="/assets/section-hero.js?v=7" defer></script>\n<script src="/assets/actividades-cards.js?v=3" defer></script>',
        1,
    )

path.write_text(new_text, encoding="utf-8")
print("patched", path)
