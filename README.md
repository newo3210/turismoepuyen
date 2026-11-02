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

## Destacados de la home

Las dos tarjetas del lago/playas son contenido estático (ya no se scrapea Instagram). El script `scripts/fetch_instagram.py` y el workflow quedan por si más adelante se vuelve a conectar un feed.

## Log de cambios

- mariano: 2026-11-02 — Alojamientos queda sticky con hold largo; fade más suave en los 01–04 de Por qué elegir.
- mariano: 2026-11-02 — El video de cultura pasa a sticky con hold largo para que el delay se sienta antes de Conocé más.
- mariano: 2026-11-02 — Mapa en 3 beats (mapa → distancias/pines → guardar ruta) con hold; delay en video, Conocé más y Artesanos.
- mariano: 2026-11-02 — Suavizamos el reveal de stories, hold al final de cada módulo y restauramos las dos columnas de Conocé más.
- mariano: 2026-11-02 — Parallax por etapas en destacados, alojamientos, conoce, piedra y por qué elegir; sin scrap de Instagram en la home.
- mariano: 2026-11-02 — Sacamos el scroll con tensión del index; vuelve el scroll normal con fade de módulos.
- mariano: 2026-10-30 — Cada módulo se centra y frena; el scroll suave vuelve con tensión y solo uno fuerte o insistente pasa al siguiente.
- mariano: 2026-10-30 — Cada distancia bajo el mapa abre en Google Maps la ruta en auto desde Epuyén hasta ese destino.
- mariano: 2026-10-30 — Debajo del mapa fijo, el siguiente scroll trae las distancias a El Bolsón, Bariloche, Esquel y Los Alerces en fade.
- mariano: 2026-10-30 — El video del header se blanquea con el scroll hasta Donde alojarse; después entra el de cultura y se opaca igual hacia el blanco.
- mariano: 2026-10-30 — El index vuelve al scroll continuo: el fade y el flotado de cada módulo siguen el gesto, sin bloquear la rueda.
- mariano: 2026-10-30 — Al cargar el index, el primer scroll hacia abajo ya no se come módulos: se frenan alturas, inercia y el salto nativo hasta que cada slide se presenta.
- mariano: 2026-10-30 — Todos los módulos del index esperan a presentarse (~1,4 s) antes de que el siguiente scroll pueda pasar al próximo.
- mariano: 2026-10-30 — El video de cultura entra como slide a pantalla completa y se queda hasta el siguiente scroll; los módulos vuelven a fade suave y flotan desde abajo.
- mariano: 2026-10-30 — En el index: sin Nuestras redes ni Condorera ni Punto Web; mapa de alojamientos a pantalla completa; fades más cortos con pausa entre módulos; el video se blanquea hasta Donde alojarse y después sigue el de cultura.
- mariano: 2026-10-29 — El video del header arranca sin filtro y se oscurece a medida que los módulos se enciman para usarlo de fondo.
- mariano: 2026-10-29 — El fondo del index queda fijo (video del header) y los módulos se cruzan más lento, como diapositivas sobre el paisaje.
- mariano: 2026-10-29 — El index pasa a un módulo en foco por vez (pantalla completa); sacamos el parallax de fotos que corría el video del header.
- mariano: 2026-10-29 — El parallax del index queda siempre activo (Windows lo apagaba) y el fade al entrar/salir se nota más.
- mariano: 2026-10-29 — En el index, cada módulo se centra al scrollear con transiciones suaves, fade y parallax.
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
