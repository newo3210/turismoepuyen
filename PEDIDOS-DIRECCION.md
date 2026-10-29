# Pedidos de la Dirección de Turismo

Pedido enviado al editor anterior. Recibido 2026-10-27. Fuente: carpeta de Google Drive + resumen por mensaje.

Fuente local: `googledrive/PÁGINA WEB/` (import comprimido a `mirror/media/` y listados a `mirror/data/`).

## Estado

| Pedido | Se puede hacer acá | Falta | Estado |
| --- | --- | --- | --- |
| Encuentro de Artesanos (32°) | Sí | Nada | Hecho en la home (fotos, YouTube, PDF) |
| Mapas (2 imágenes nuevas) | Sí | Nada | Hecho en `/mapas/` |
| Actividades: barra `/` en URLs | Sí, ya | Nada | Hecho (espejo) |
| Alojamientos: sumar Carelhue | Sí | Foto propia del hostel | En `/alojamientos/` con tel, mail, zona y pin del Excel GEO |
| Sección Servicios | Sí | Direcciones de remises y guías | `/servicios/` con rubros del Excel; Puerto Bonito usa el pin del parque |

---

## 1. Encuentro de Artesanos — 32° edición

**Pedido:** actualizar el apartado con el resumen de la 32°, fotos relevantes y el video de YouTube.

**Material citado (en Drive, no en el repo):**

- PDF en la carpeta de la 32° edición
- Fotos con nombre, entre ellas Christian Herrera, Los Súper Rancheros de Pucón y los premios de la Dirección de Cultura
- Video: [https://youtu.be/7KE-2Aw87fc](https://youtu.be/7KE-2Aw87fc)

**Hecho en el espejo:** el bloque de la home muestra la 32° edición (sedes Rawson/Epuyén/Rada Tilly), fotos de Christian Herrera, Los Súper Rancheros de Pucón y el premio a la mejor obra, embed de YouTube, premios de Cultura y el PDF. El mp4 de 374 MB no se publicó: se usa [https://youtu.be/7KE-2Aw87fc](https://youtu.be/7KE-2Aw87fc).

---

## 2. Mapas — reemplazar 2 imágenes viejas

**Pedido:** cambiar las 2 imágenes viejas por las que están usando ahora (subidas al Drive).

**Hoy en `/mapas/`:**

- Imagen principal: `wp-content/uploads/2024/04/Folleto-para-descarga.jpeg`
- PDF de descarga (link también sin `/`): `wp-content/uploads/2024/04/correccion-folleto-turismo-epuyen.pdf`
- Cabezal: `wp-content/uploads/2024/04/maapa-cabezal.jpeg`

**Hecho en el espejo:** `/mapas/` muestra el mapa ilustrado de Epuyén y el folleto de invierno (comprimidos a JPG). El cabezal viejo se dejó.

---

## 3. Actividades — barra `/` faltante

**Pedido:** “Más información” abre `turismoepuyen.com.arsenderismo` y da `DNS_PROBE_FINISHED_NXDOMAIN`. Corregir poniendo la barra.

**Diagnóstico:** es eso. El dominio y el path quedaron pegados (`turismoepuyen.com.arsenderismo` en vez de `turismoepuyen.com.ar/senderismo`). Las páginas locales (`/senderismo/`, `/la-condorera/`, etc.) sí existen.

Enlaces rotos vistos:

- Home: `...arsenderismo/`, `...aractividades#condorera`, `...arcontacto/`, `...arsenderismo#piedrapintada`
- Actividades: senderismo, laguna-las-mercedes, la-condorera, centro-cultural-antuquillen, stupa-de-samantabhadra
- Mapas: el PDF de descarga
- Hay más copias del mismo error en tags, footer y JSON del espejo

**No hace falta Drive.** Se puede corregir ya en la home y en Actividades (y, si se quiere, en todo el espejo).

---

## 4. Alojamientos — sumar Carelhue

**Pedido:** en el Excel agregaron el establecimiento Carelhue al listado.

**Hoy:**

- Hay ficha vieja de WordPress en `/cabanas-carelhue/` (casi vacía: sin teléfono, mail ni fotos útiles).
- **Ya está** en `/alojamientos/` con contacto, mail, dirección y zona del Excel. Falta foto propia del hostel.

**También del Excel:** se sumó Valle de Epuyen; Alen no figura en el padrón habilitado y se sacó del listado.

---

## 5. Servicios — sección tipo Alojamientos / Gastronomía

**Pedido:** quedó pendiente una sección similar a Alojamientos y Gastronómicos, con los prestadores del Excel.

**Hoy:** en `/alojamientos/` ya hay tres pestañas: Alojamientos, Gastronomía y Servicios. La de Servicios tiene 8 filas (Puerto Bonito, Eputur, Trekking Epuyén, remises, etc.), varias sin categoría ni nombre de fantasía. No hay ítem de menú “Servicios” ni página propia.

**Hecho en el espejo:** página `/servicios/` en el menú (después de Gastronomía), con las mismas fichas + mapa + contacto que Alojamientos. Ya no vive solo como pestaña de la tabla.

**Hecho del Excel:** rubros Kayak / Guía / Agencia / Remís. Los pines de servicios sin zona siguen en el casco de Epuyén (la hoja “Otros Servicos” no trae GEO). Puerto Bonito y Puerto Bonito Aventura usan el pin del parque.

---

## 6. Geolocalización — Excel con links de Google Maps

**Pedido:** el padrón `PRESTADORES TURÍSTICOS HABILITADOS con GEO.xlsx` trae una columna GEOLOCALIZACIÓN (links `maps.app.goo.gl`) para actualizar los pines.

**Hecho en el espejo (2026-10-29):**

- Alojamientos: 26 de 30 con pin exacto; La Playita, El Santy, El Morenito y Casa de Tato siguen por zona.
- Gastronomía: misma UI de fichas + mapa; 15 de 19 con pin exacto.
- Servicios: sin columna GEO en esa hoja; remises y guías quedan en el casco.

Quedan fuera de este pedido (archivos muy pesados): drones de la oficina en Ruta 40 y de Puerto Bonito.

---

## Cómo seguir

Pedidos del Drive ya aplicados en el espejo. Pendiente opcional: fotos propias de Carelhue, GEO de remises/guías, y si se quiere una página propia de artesanos además de la home.
