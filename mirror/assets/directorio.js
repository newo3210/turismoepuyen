// Directory boot - load JSON, then wire filters, cards, map, and booking links.
(function () {
  const roots = document.querySelectorAll("[data-directorio]");
  roots.forEach((root) => bootDirectory(root));
})();

// Page bootstrap - fetch listings for one directory root and render the UI.
function bootDirectory(root) {
  const src = root.getAttribute("data-src");
  if (!src) return;

  fetch(src)
    .then((res) => {
      if (!res.ok) throw new Error("No se pudo cargar el directorio");
      return res.json();
    })
    .then((payload) => renderDirectory(root, payload))
    .catch(() => {
      const list = root.querySelector("[data-list]");
      if (list) {
        list.innerHTML =
          '<p class="directorio__empty">No se pudieron cargar los prestadores. Probá recargar la página.</p>';
      }
    });
}

// HTML escaping - keep names, zones, and popup text safe in templates.
function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (char) => {
    const map = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" };
    return map[char];
  });
}

// WhatsApp digits - Argentine mobiles need 54 9 + area + number for wa.me.
function waDigits(phone) {
  let digits = String(phone || "").replace(/\D/g, "");
  if (!digits) return "";
  if (digits.startsWith("54") && !digits.startsWith("549")) {
    digits = "549" + digits.slice(2);
  } else if (!digits.startsWith("54")) {
    digits = digits.startsWith("9") ? "54" + digits : "549" + digits;
  }
  return digits;
}

// Booking copy - prefill WhatsApp so the guest can ask for dates from the listing.
function waHref(item) {
  const digits = waDigits(item.whatsapp || (item.phones && item.phones[0] && item.phones[0].wa));
  if (!digits) return "";
  const text = encodeURIComponent(
    "Hola, les escribo desde turismoepuyen.com.ar. Quiero consultar disponibilidad en " +
      item.name +
      "."
  );
  return "https://wa.me/" + digits + "?text=" + text;
}

// Maps query - official Excel pin, exact lat/lng, or address search in Epuyén.
function mapsHref(item) {
  if (item.mapsUrl) return item.mapsUrl;
  if (!item.coordsApproximate && typeof item.lat === "number" && typeof item.lng === "number") {
    return (
      "https://www.google.com/maps/search/?api=1&query=" +
      encodeURIComponent(String(item.lat) + "," + String(item.lng))
    );
  }
  const parts = [item.address, item.zone, "Epuyén", "Chubut"].filter(Boolean);
  const query =
    parts.length > 2 ? parts.join(", ") : String(item.lat) + "," + String(item.lng);
  return "https://www.google.com/maps/search/?api=1&query=" + encodeURIComponent(query);
}

// Category chips - unique labels plus an "Todos" filter from the current payload.
function collectCategories(items) {
  const set = new Set();
  items.forEach((item) => (item.categories || []).forEach((cat) => set.add(cat)));
  return ["Todos", ...Array.from(set).sort()];
}

// Visible rows - category chip plus free-text search over name, zone, and address.
function filterItems(items, category, query) {
  const needle = query.trim().toLowerCase();
  return items.filter((item) => {
    const cats = item.categories || [];
    const catOk = category === "Todos" || cats.includes(category);
    if (!catOk) return false;
    if (!needle) return true;
    const hay = [item.name, item.zone, item.address, item.responsable, cats.join(" ")]
      .join(" ")
      .toLowerCase();
    return hay.includes(needle);
  });
}

// Button icons - WhatsApp brand mark, envelope, and map pin as inline SVG.
function btnIcon(kind) {
  if (kind === "wa") {
    return (
      '<svg class="directorio__ico" viewBox="0 0 24 24" aria-hidden="true" focusable="false">' +
      '<path fill="currentColor" d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.435 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413z"/>' +
      "</svg>"
    );
  }
  if (kind === "mail") {
    return (
      '<svg class="directorio__ico" viewBox="0 0 24 24" aria-hidden="true" focusable="false">' +
      '<path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M4 6h16a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1z"/>' +
      '<path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="m3.5 7 8.5 6 8.5-6"/>' +
      "</svg>"
    );
  }
  return (
    '<svg class="directorio__ico" viewBox="0 0 24 24" aria-hidden="true" focusable="false">' +
    '<path fill="currentColor" d="M12 2a7 7 0 0 0-7 7c0 5.25 7 13 7 13s7-7.75 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/>' +
    "</svg>"
  );
}

// Action buttons - WhatsApp, email, maps pin, and optional WordPress sheet.
function actionButtons(item, extraClass) {
  const cls = extraClass ? "directorio__btn " + extraClass : "directorio__btn";
  const bits = [];
  const wa = waHref(item);
  if (wa) {
    bits.push(
      '<a class="' +
        cls +
        ' directorio__btn--wa" href="' +
        wa +
        '" target="_blank" rel="noopener" data-stop>' +
        btnIcon("wa") +
        "WhatsApp</a>"
    );
  }
  if (item.email && item.email.includes("@")) {
    bits.push(
      '<a class="' +
        cls +
        '" href="mailto:' +
        escapeHtml(item.email) +
        '" data-stop>' +
        btnIcon("mail") +
        "Email</a>"
    );
  }
  bits.push(
    '<a class="' +
      cls +
      '" href="' +
      mapsHref(item) +
      '" target="_blank" rel="noopener" data-stop>' +
      btnIcon("pin") +
      "Cómo llegar</a>"
  );
  if (item.page) {
    bits.push('<a class="' + cls + '" href="' + escapeHtml(item.page) + '">Ver ficha</a>');
  }
  return bits.join("");
}

// Card markup - photo, category tags, zone, and booking actions.
function cardHtml(item) {
  const cats = (item.categories || [])
    .map((cat) => '<span class="directorio__tag">' + escapeHtml(cat) + "</span>")
    .join("");
  const meta = [item.zone, item.address].filter(Boolean).join(" · ");
  const photo = item.image
    ? " style=\"background-image:url('" + escapeHtml(item.image) + "')\""
    : "";
  return (
    '<article class="directorio__card" data-id="' +
    escapeHtml(item.id) +
    '">' +
    '<div class="directorio__card-photo"' +
    photo +
    "></div>" +
    '<div class="directorio__card-body">' +
    '<div class="directorio__card-cats">' +
    cats +
    "</div>" +
    ' <h3 class="directorio__card-title">' +
    escapeHtml(item.name) +
    "</h3>" +
    (meta ? '<p class="directorio__card-meta">' + escapeHtml(meta) + "</p>" : "") +
    '<div class="directorio__card-actions">' +
    actionButtons(item) +
    "</div>" +
    "</div></article>"
  );
}

// Detail sheet - larger booking panel opened when a card or map pin is chosen.
function fillSheet(root, item) {
  const sheet = root.querySelector("[data-sheet]");
  if (!sheet || !item) return;
  const photo = sheet.querySelector("[data-sheet-photo]");
  const title = sheet.querySelector("[data-sheet-title]");
  const meta = sheet.querySelector("[data-sheet-meta]");
  const note = sheet.querySelector("[data-sheet-note]");
  const actions = sheet.querySelector("[data-sheet-actions]");
  if (photo) {
    photo.style.backgroundImage = item.image ? "url('" + item.image + "')" : "";
  }
  if (title) title.textContent = item.name;
  if (meta) {
    meta.textContent = [item.categories && item.categories.join(" · "), item.zone, item.address]
      .filter(Boolean)
      .join(" · ");
  }
  if (note) {
    const bits = [];
    if (item.responsable) bits.push("Responsable: " + item.responsable);
    if (item.email && item.email.includes("@")) bits.push(item.email);
    if (item.notes) bits.push(item.notes);
    if (item.coordsApproximate) {
      bits.push("El pin del mapa marca la zona, no la puerta exacta.");
    }
    if (item.pendingDetails) {
      bits.push("Faltan teléfono y mail; los vamos a completar con el Excel de Turismo.");
    }
    note.textContent = bits.join(" · ");
  }
  if (actions) actions.innerHTML = actionButtons(item);
  if (typeof sheet.showModal === "function" && !sheet.open) sheet.showModal();
}

// Directory render - chips, list, Leaflet map, and selection between cards and pins.
function renderDirectory(root, payload) {
  const items = payload.items || [];
  const listEl = root.querySelector("[data-list]");
  const filtersEl = root.querySelector("[data-filters]");
  const searchEl = root.querySelector("[data-search]");
  const mapEl = root.querySelector("[data-map]");
  const sheet = root.querySelector("[data-sheet]");
  const closeBtn = root.querySelector("[data-sheet-close]");
  const state = { category: "Todos", query: "", selected: null };
  const markersById = {};
  let map;
  let markerLayer;

  if (filtersEl) {
    filtersEl.innerHTML = collectCategories(items)
      .map((cat) => {
        const active = cat === "Todos" ? " is-active" : "";
        return (
          '<button type="button" class="directorio__chip' +
          active +
          '" data-cat="' +
          escapeHtml(cat) +
          '">' +
          escapeHtml(cat) +
          "</button>"
        );
      })
      .join("");
  }

  function paintList(visible) {
    if (!listEl) return;
    if (!visible.length) {
      listEl.innerHTML =
        '<p class="directorio__empty">No hay resultados con ese filtro. Probá otra categoría o borrá la búsqueda.</p>';
      return;
    }
    listEl.innerHTML = visible.map(cardHtml).join("");
    listEl.querySelectorAll(".directorio__card").forEach((card) => {
      card.classList.toggle("is-active", card.getAttribute("data-id") === state.selected);
    });
  }

  function paintMap(visible) {
    if (!map || !window.L) return;
    if (markerLayer) markerLayer.clearLayers();
    markerLayer = window.L.layerGroup().addTo(map);
    Object.keys(markersById).forEach((key) => delete markersById[key]);
    const bounds = [];
    visible.forEach((item) => {
      if (typeof item.lat !== "number" || typeof item.lng !== "number") return;
      const marker = window.L.circleMarker([item.lat, item.lng], {
        radius: 8,
        color: "#1688a3",
        weight: 2,
        fillColor: "#2bbede",
        fillOpacity: 0.9,
      }).addTo(markerLayer);
      marker.bindPopup(
        "<strong>" +
          escapeHtml(item.name) +
          "</strong><br>" +
          escapeHtml((item.categories || []).join(" · ")) +
          (item.zone ? "<br>" + escapeHtml(item.zone) : "")
      );
      marker.on("click", () => selectItem(item.id, false));
      markersById[item.id] = marker;
      bounds.push([item.lat, item.lng]);
    });
    if (bounds.length) {
      map.fitBounds(bounds, { padding: [28, 28], maxZoom: 14 });
    }
  }

  function refresh() {
    const visible = filterItems(items, state.category, state.query);
    paintList(visible);
    paintMap(visible);
  }

  function selectItem(id, openSheet) {
    const item = items.find((row) => row.id === id);
    if (!item) return;
    state.selected = id;
    root.querySelectorAll(".directorio__card").forEach((card) => {
      card.classList.toggle("is-active", card.getAttribute("data-id") === id);
    });
    const marker = markersById[id];
    if (marker && map) {
      map.setView([item.lat, item.lng], Math.max(map.getZoom(), 14), { animate: true });
      marker.openPopup();
    }
    if (openSheet !== false) fillSheet(root, item);
    history.replaceState(null, "", "#" + encodeURIComponent(id));
  }

  if (filtersEl) {
    filtersEl.addEventListener("click", (event) => {
      const chip = event.target.closest("[data-cat]");
      if (!chip) return;
      state.category = chip.getAttribute("data-cat");
      filtersEl.querySelectorAll(".directorio__chip").forEach((btn) => {
        btn.classList.toggle("is-active", btn === chip);
      });
      refresh();
    });
  }

  if (searchEl) {
    searchEl.addEventListener("input", () => {
      state.query = searchEl.value || "";
      refresh();
    });
  }

  if (listEl) {
    listEl.addEventListener("click", (event) => {
      if (event.target.closest("[data-stop]")) return;
      const card = event.target.closest("[data-id]");
      if (!card) return;
      selectItem(card.getAttribute("data-id"), true);
    });
  }

  if (closeBtn && sheet) {
    closeBtn.addEventListener("click", () => sheet.close());
  }

    if (mapEl && window.L) {
    map = window.L.map(mapEl, { scrollWheelZoom: false });
    window.L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 18,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    }).addTo(map);
    map.setView([-42.23, -71.365], 12);
    window.setTimeout(() => map.invalidateSize(), 200);
  }

  refresh();

  const hashId = decodeURIComponent((location.hash || "").replace(/^#/, ""));
  if (hashId) {
    window.setTimeout(() => selectItem(hashId, true), 300);
  }
}
