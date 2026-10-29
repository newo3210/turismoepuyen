# Turismo Epuyén

Copia estática de [turismoepuyen.com.ar](https://turismoepuyen.com.ar) (snapshot 2026-10-20).

## Vista previa para Turismo

GitHub muestra el HTML como código. Para ver el sitio (y mandárselo a la Dirección) usá:

**https://newo3210.github.io/turismoepuyen/**

El repo es público: con ese link alcanza, no hace falta cuenta de GitHub. Se actualiza solo con cada push a main.

La primera vez hay que activar Pages: *Settings → Pages → Build and deployment → Source: GitHub Actions*.

## Contenido

- `mirror/` — HTML, CSS, JS e imágenes
- `serve.py` — servidor local que reescribe URLs al localhost
- `scripts/fetch_instagram.py` — trae los 2 últimos posts de @turismoepuyen
- `urls.txt` / `failed-urls.txt` — sitemap y descargas fallidas
- `PEDIDOS-DIRECCION.md` — pedidos de la Dirección de Turismo (Drive, mapas, artesanos, prestadores)

## Vista local

```powershell
python serve.py
```

Abrir http://127.0.0.1:8080/

Es un espejo estático: formularios, búsquedas y el panel de WordPress no funcionan offline.

## Novedades de Instagram

Instagram no permite scrapear el feed público. Los dos módulos de la home (antes “letras corpóreas” y “Semana Santa 2025”) se arman con la [Graph API](https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media/) de una cuenta profesional.

Hace falta:

1. Que @turismoepuyen sea cuenta profesional (Business o Creator).
2. Una app en [Meta for Developers](https://developers.facebook.com/) con permiso `instagram_business_basic`.
3. Un token de acceso (y, si usás Facebook Login, el `IG_USER_ID`).

Copiá `instagram.env.example` a `.env` y completá `IG_ACCESS_TOKEN`. Después:

```powershell
python scripts/fetch_instagram.py
```

Eso baja las fotos a `mirror/media/instagram/`, escribe `mirror/data/instagram-posts.json` y actualiza las tarjetas. **Conocer más** abre el post original en Instagram.

En GitHub, cargá el secret `IG_ACCESS_TOKEN` (y opcional `IG_USER_ID`). El workflow `Actualizar Instagram` corre todos los días a las 08:00 ART, o a mano desde Actions.

Mientras no haya token, las tarjetas usan fotos demo locales y mandan a [instagram.com/turismoepuyen](https://www.instagram.com/turismoepuyen/).

## Log de cambios

- mariano: 2026-10-29 — Preview público en GitHub Pages para que Turismo vea los avances sin abrir el HTML crudo.
- mariano: 2026-10-29 — Comprimimos cultura y header2; cultura reemplaza la tira de fotos bajo Donde Alojarse, y header2 va de fondo en Alojamientos y Servicios.
- mariano: 2026-10-29 — El MP4 web del header queda como `epuyen-header_opti_1.mp4` para reemplazo directo por FTP; el original pesado pasa a `-src`.
- mariano: 2026-10-29 — Comprimimos el video del header a `epuyen-header_opti_1-web.mp4` (720p, sin audio, ~1,5 MB) y un poster para carga rápida.
- mariano: 2026-10-29 — Sacamos el bloque de stats (opiniones y redes) que estaba debajo del header en Alojamientos, Gastronomía y Servicios.
- mariano: 2026-10-29 — En las fichas, WhatsApp lleva el ícono oficial, sacamos Llamar, Escribir pasa a Email y Cómo llegar lleva un pin.
- mariano: 2026-10-29 — Actualizamos los pines del mapa con la geolocalización del Excel (Alojamientos y Gastronomía); Gastronomía pasa a fichas + mapa como Alojamientos.
- mariano: 2026-10-27 — En Artesanos dejamos más espacio entre la foto grande de la izquierda y las tres de abajo.
- mariano: 2026-10-27 — En Artesanos las tres fotos van debajo de la imagen de la izquierda y el video de YouTube queda justo después del texto.
- mariano: 2026-10-27 — Piedra Pintada pasa al mismo formato grande con texto superpuesto; la foto vertical de Artesanos queda alineada arriba.
- mariano: 2026-10-27 — En Explora Epuyén sacamos el bloque de Senderismo y dejamos solo la foto al lado del texto.
- mariano: 2026-10-27 — En la home el carrusel de fotos queda debajo de Donde Alojarse, Piedra Pintada pasa después de Explora Epuyén, y La Condorera usa el mismo formato grande con texto superpuesto.
- mariano: 2026-10-27 — Bajamos el video del header (`epuyen-original-opti.mp4`) al espejo local para poder cortarlo y reutilizarlo.
- mariano: 2026-10-27 — Incorporamos el Drive de la Dirección: Encuentro de Artesanos 32° (fotos, YouTube y PDF), mapas nuevos, Excel de prestadores (Carelhue, Valle de Epuyen y rubros de Servicios) y texto/foto correctos de la Estupa Samantabhadra.
- mariano: 2026-10-27 — Alojamientos pasa de tabla Excel a fichas con mapa y contacto (WhatsApp/tel/mail); Servicios queda como sección propia en el menú; URLs sin barra corregidas para cuando esté online.
- mariano: 2026-10-27 — Documentamos el pedido de la Dirección de Turismo (artesanos 32°, mapas, URLs rotas, Carelhue y Servicios) en `PEDIDOS-DIRECCION.md`.
- mariano: 2026-10-27 — El demo de Instagram muestra fotos locales; el mapa pasa a 16:9 en escritorio y Dónde Alojarse queda como módulo con foto.
- mariano: 2026-10-23 — Reemplazamos las noticias tipo blog de la home por los 2 últimos posts de Instagram (@turismoepuyen), con “Conocer más” al post original.
- mariano: 2026-10-23 — El Instagram de Turismo pasa de @muniepuyen a @turismoepuyen.
- mariano: 2026-10-23 — Sacamos los módulos “Que Opina Los Turistas” y el formulario de suscripción del footer.
- mariano: 2026-10-23 — Sacamos el widget “El tiempo en Epuyén” (tutiempo.net), que no funcionaba.
- mariano: 2026-10-23 — Agregamos este log de cambios (autor `mariano:` + fecha) para ir registrando el trabajo.
- mariano: 2026-10-23 — Primera versión en GitHub: snapshot estático de turismoepuyen.com.ar y servidor local (`serve.py`).
