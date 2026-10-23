# Turismo Epuyén

Copia estática de [turismoepuyen.com.ar](https://turismoepuyen.com.ar) (snapshot 2026-10-20).

## Contenido

- `mirror/` — HTML, CSS, JS e imágenes
- `serve.py` — servidor local que reescribe URLs al localhost
- `urls.txt` / `failed-urls.txt` — sitemap y descargas fallidas

## Vista local

```powershell
python serve.py
```

Abrir http://127.0.0.1:8080/

Es un espejo estático: formularios, búsquedas y el panel de WordPress no funcionan offline.

## Log de cambios

- mariano: 2026-10-23 — Agregamos este log de cambios (autor `mariano:` + fecha) para ir registrando el trabajo.
- mariano: 2026-10-23 — Primera versión en GitHub: snapshot estático de turismoepuyen.com.ar y servidor local (`serve.py`).
