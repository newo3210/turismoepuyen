// Feed config - JSON path, Instagram profile, and how many posts to show.
const IG_FEED_URL = "/data/instagram-posts.json";
const IG_PROFILE_URL = "https://www.instagram.com/turismoepuyen/";
const IG_POST_LIMIT = 2;

// Caption helpers - first line as title, remaining text as short excerpt.
function firstLine(caption) {
  const lines = String(caption || "")
    .split(/\n+/)
    .map((line) => line.trim())
    .filter(Boolean);
  return lines[0] || "Novedades de Epuyén";
}

function excerpt(caption, title) {
  const full = String(caption || "").trim();
  if (!full) {
    return "Mirá la publicación original en Instagram.";
  }
  const rest = full.startsWith(title) ? full.slice(title.length).trim() : full;
  const text = (rest || full).replace(/\s+/g, " ");
  return text.length > 220 ? `${text.slice(0, 217).trim()}…` : text;
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (char) => {
    const map = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" };
    return map[char];
  });
}

// Card rendering - photo, title, caption excerpt, and "Conocer más" permalink.
function renderCard(post, index) {
  const tone = index === 0 ? "teal" : "green";
  const title = firstLine(post.caption);
  const body = excerpt(post.caption, title);
  const href = post.permalink || IG_PROFILE_URL;
  const alt = title;
  const image = post.local_image || post.media_url || "";
  const photo = image
    ? `<img src="${escapeHtml(image)}" alt="${escapeHtml(alt)}" loading="lazy" decoding="async">`
    : `<div class="ig-feed__photo-empty">@turismoepuyen</div>`;

  return `
    <article class="ig-feed__card ig-feed__card--${tone}">
      <div class="ig-feed__photo">${photo}</div>
      <div class="ig-feed__body">
        <h3 class="ig-feed__title">${escapeHtml(title)}</h3>
        <p class="ig-feed__excerpt">${escapeHtml(body)}</p>
        <a class="ig-feed__more" href="${escapeHtml(href)}" target="_blank" rel="noopener noreferrer">Conocer más</a>
      </div>
    </article>
  `;
}

function renderFallback() {
  return [
    {
      caption: "Lago Epuyén\nPaisajes de la cordillera, directo desde @turismoepuyen.",
      permalink: IG_PROFILE_URL,
      local_image: "/media/instagram/demo-lago.jpg",
    },
    {
      caption: "Las playas del lago\nAgua cristalina y montaña, para planear la próxima visita.",
      permalink: IG_PROFILE_URL,
      local_image: "/media/instagram/demo-playas.jpg",
    },
  ]
    .map(renderCard)
    .join("");
}

// Feed bootstrap - load JSON and paint the two homepage cards.
async function paintInstagramFeed() {
  const grid = document.querySelector("[data-ig-feed-grid]");
  if (!grid) {
    return;
  }

  try {
    const response = await fetch(IG_FEED_URL, { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const data = await response.json();
    const posts = Array.isArray(data.posts) ? data.posts.slice(0, IG_POST_LIMIT) : [];
    grid.innerHTML = posts.length ? posts.map(renderCard).join("") : renderFallback();
  } catch (error) {
    grid.innerHTML = renderFallback();
  }
}

paintInstagramFeed();
