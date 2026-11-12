// Section heroes - fixed media covered by mountain waves; pause video when covered.
(function () {
  const hero = document.querySelector(".page-hero");
  if (!hero) return;

  // Cover fill - white matches typical Elementor content sheets.
  const COVER_FILL = "#fff";

  // Wave markup - Elementor mountains rotated; cream paint lives on the panel.
  const waveHtml =
    '<div class="page-cover-wave" aria-hidden="true">' +
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 100" preserveAspectRatio="none">' +
    '<path class="page-cover-wave__fill page-cover-wave__fill--soft" d="M473,67.3c-203.9,88.3-263.1-34-320.3,0C66,119.1,0,59.7,0,59.7V0h1000v59.7 c0,0-62.1,26.1-94.9,29.3c-32.8,3.3-62.8-12.3-75.8-22.1C806,49.6,745.3,8.7,694.9,4.7S492.4,59,473,67.3z"/>' +
    '<path class="page-cover-wave__fill page-cover-wave__fill--mid" d="M734,67.3c-45.5,0-77.2-23.2-129.1-39.1c-28.6-8.7-150.3-10.1-254,39.1 s-91.7-34.4-149.2,0C115.7,118.3,0,39.8,0,39.8V0h1000v36.5c0,0-28.2-18.5-92.1-18.5C810.2,18.1,775.7,67.3,734,67.3z"/>' +
    '<path class="page-cover-wave__fill" d="M766.1,28.9c-200-57.5-266,65.5-395.1,19.5C242,1.8,242,5.4,184.8,20.6C128,35.8,132.3,44.9,89.9,52.5C28.6,63.7,0,0,0,0 h1000c0,0-9.9,40.9-83.6,48.1S829.6,47,766.1,28.9z"/>' +
    "</svg></div>";

  // Frame state - one paint per scroll tick.
  let ticking = false;
  let heroVideo = null;
  let coverPanel = null;

  // Next content block - first Elementor top sibling after the hero.
  function findCoverTarget() {
    let node = hero.nextElementSibling;
    while (node) {
      if (
        node.matches(
          "section.elementor-top-section, section.actividades-cards, .actividades-cards, .e-con-parent, .e-con.e-parent, .elementor-element.e-con"
        ) ||
        (node.classList.contains("elementor-element") && !node.classList.contains("page-hero"))
      ) {
        return node;
      }
      node = node.nextElementSibling;
    }
    return null;
  }

  // Cover sheet - wrap first content block so wave can sit above opaque paint.
  let coverRoot = null;
  let coverWave = null;

  function buildCover() {
    const target = findCoverTarget();
    if (!target) return;
    if (target.classList.contains("page-cover")) {
      coverRoot = target;
      coverPanel = target.querySelector(".page-cover-panel");
      coverWave = target.querySelector(".page-cover-wave");
      return;
    }

    target.classList.add("page-cover");
    // Sticky story pins must stay direct children of the tall section.
    const storyPin = target.querySelector(":scope > [data-page-story-pin], :scope > [data-home-story-pin]");
    if (storyPin) {
      if (!target.querySelector(":scope > .page-cover-wave")) {
        target.insertAdjacentHTML("afterbegin", waveHtml);
      }
      storyPin.classList.add("page-cover-panel");
      storyPin.style.background = COVER_FILL;
      coverRoot = target;
      coverPanel = storyPin;
      coverWave = target.querySelector(".page-cover-wave");
      return;
    }

    const panel = document.createElement("div");
    panel.className = "page-cover-panel";
    while (target.firstChild) {
      panel.appendChild(target.firstChild);
    }
    target.insertAdjacentHTML("afterbegin", waveHtml);
    target.appendChild(panel);
    coverRoot = target;
    coverPanel = panel;
    coverWave = target.querySelector(".page-cover-wave");
    panel.style.background = COVER_FILL;
  }

  // Hero backdrop - copy classic bg / poster into the fixed layer; keep video muted.
  function pinHeroBackdrop(presetBg) {
    const hosted = hero.querySelector(".elementor-background-video-hosted");
    const videoWrap = hero.querySelector(".elementor-background-video-container");
    heroVideo = hosted || null;

    let bg = presetBg || document.documentElement.style.getPropertyValue("--page-hero-bg");
    if (!bg || bg === "none") {
      const computed = window.getComputedStyle(hero).backgroundImage;
      if (computed && computed !== "none") bg = computed;
    }
    if (!bg || bg === "none") {
      const poster = hosted && hosted.getAttribute("poster");
      if (poster) bg = `url("${poster}")`;
    }
    if (bg && bg !== "none") {
      document.documentElement.style.setProperty("--page-hero-bg", bg);
    }

    hero.style.setProperty("background-image", "none", "important");
    hero.style.setProperty("background-color", "transparent", "important");

    if (videoWrap) {
      videoWrap.style.setProperty("display", "block", "important");
    }
    if (hosted) {
      hosted.muted = true;
      hosted.defaultMuted = true;
      hosted.playsInline = true;
    }
  }

  // Curtain edge - leading Y of the wave (falls back to the cream panel).
  function curtainEdge() {
    if (coverWave) return coverWave.getBoundingClientRect().top;
    if (coverPanel) return coverPanel.getBoundingClientRect().top;
    return window.innerHeight - window.scrollY;
  }

  // Hero covered - cream curtain has reached the top of the viewport.
  function isHeroCovered() {
    return curtainEdge() <= 0;
  }

  // Hero video sync - play only while visible; pause to save resources.
  function syncHeroVideo(shouldPlay) {
    if (!heroVideo) return;
    if (shouldPlay) {
      if (heroVideo.paused) {
        const play = heroVideo.play && heroVideo.play();
        if (play && typeof play.catch === "function") play.catch(() => {});
      }
      return;
    }
    if (!heroVideo.paused) heroVideo.pause();
  }

  // Stage flags - floor tracks the rising wave so side gaps never show the header.
  function updateStage() {
    ticking = false;
    const edge = curtainEdge();
    const floorTop = Math.max(0, Math.min(window.innerHeight, edge));
    const showFloor = edge < window.innerHeight;
    const covered = edge <= 0;

    document.body.style.setProperty("--page-hero-floor-top", `${floorTop}px`);
    document.body.classList.toggle("is-page-hero-covered", covered);
    document.body.classList.toggle("is-page-hero-floor", showFloor);
    syncHeroVideo(!covered && !document.hidden);
  }

  // Request frame - coalesce scroll into one paint.
  function requestFrame() {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(updateStage);
  }

  // Boot - capture bg before CSS clears it, then floor + cover + scroll sync.
  const floor = document.createElement("div");
  floor.className = "page-hero-floor";
  floor.setAttribute("aria-hidden", "true");
  document.body.insertBefore(floor, document.body.firstChild);

  const initialBg = window.getComputedStyle(hero).backgroundImage;
  document.body.classList.add("page-hero-parallax-ready");
  pinHeroBackdrop(initialBg);
  buildCover();
  updateStage();

  window.addEventListener("scroll", requestFrame, { passive: true });
  window.addEventListener("resize", requestFrame);
  window.addEventListener("load", () => {
    pinHeroBackdrop();
    requestFrame();
  });
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) syncHeroVideo(false);
    else requestFrame();
  });
})();
