// Home stage - native scroll, module fade, sticky stories, and hold spacers.
(function () {
  if (!document.body.classList.contains("home")) return;

  // Module list - top-level home blocks that take focus as a whole.
  const modules = Array.from(document.querySelectorAll(".home-module"));
  if (!modules.length) return;

  // Desktop flag - scroll-linked fade/stories only above the Astra breakpoint.
  const desktopQuery = window.matchMedia("(min-width: 922px)");
  const hero = document.querySelector(".home-module--hero");
  const stay = document.getElementById("donde-alojarse");
  const cultura = document.querySelector(".home-cultura");
  const homeMap = document.getElementById("mapa-epuyen");
  const footer = document.getElementById("colophon");
  const stories = Array.from(document.querySelectorAll("[data-home-story]"));
  const holds = Array.from(document.querySelectorAll("[data-home-hold]:not([data-home-story])"));

  // Frame state - one paint per scroll tick.
  let ticking = false;

  // Story timing defaults - hold after the last beat; pace stretches each beat.
  const STORY_HOLD = 0.45;

  // Stage veil - whites out the pinned video as later modules sit on top of it.
  const veil = document.createElement("div");
  veil.className = "home-stage-veil";
  veil.setAttribute("aria-hidden", "true");
  document.body.insertBefore(veil, document.body.firstChild);

  // Layout top - document position, ignoring sticky visual offsets.
  function layoutTop(el) {
    let top = 0;
    let node = el;
    while (node) {
      top += node.offsetTop;
      node = node.offsetParent;
    }
    return top;
  }

  // Video slide - hero and cultura occupy the full viewport with no overlay card.
  function isVideoModule(mod) {
    return Boolean(mod && (mod.classList.contains("home-module--hero") || mod.classList.contains("home-module--video")));
  }

  // Clamp - keep a 0..1 visibility value in range.
  function clamp01(value) {
    return Math.max(0, Math.min(1, value));
  }

  // Softstep - smoother ease so later logos/layers fade in gently.
  function softstep(value) {
    const t = clamp01(value);
    return t * t * t * (t * (t * 6 - 15) + 10);
  }

  // Story beats - how many reveal stops a sticky module needs.
  function storyBeats(story) {
    const n = Number(story.getAttribute("data-beats"));
    return Number.isFinite(n) && n > 0 ? Math.floor(n) : 2;
  }

  // Story hold - extra viewport travel after the last layer settles.
  function storyHold(story) {
    const n = Number(story.getAttribute("data-hold"));
    return Number.isFinite(n) && n >= 0 ? n : STORY_HOLD;
  }

  // Story pace - >1 stretches each beat for a slower transition.
  function storyPace(story) {
    const n = Number(story.getAttribute("data-pace"));
    return Number.isFinite(n) && n > 0 ? n : 1;
  }

  // Hold spacer - modules that only linger (e.g. cultura video) without layer beats.
  function sizeHolds() {
    holds.forEach((mod) => {
      const hold = Number(mod.getAttribute("data-home-hold"));
      const units = Number.isFinite(hold) && hold > 0 ? 1 + hold : 2;
      if (!desktopQuery.matches) {
        mod.style.removeProperty("height");
        mod.style.removeProperty("min-height");
        return;
      }
      const travel = units * window.innerHeight;
      mod.style.height = `${travel}px`;
      mod.style.minHeight = `${travel}px`;
    });
  }

  // Story height - paced travel per beat, then the module's hold.
  function sizeStories() {
    stories.forEach((story) => {
      const beats = storyBeats(story);
      const hold = storyHold(story);
      const pace = storyPace(story);
      story.style.setProperty("--story-beats", String(beats));
      if (!desktopQuery.matches) {
        story.style.removeProperty("height");
        story.style.removeProperty("min-height");
        return;
      }
      const travel = (beats * pace + hold) * window.innerHeight;
      story.style.height = `${travel}px`;
      story.style.minHeight = `${travel}px`;
    });
  }

  // Slide vs tall - photo/text slides fill the viewport; long blocks keep their height.
  function markModules() {
    modules.forEach((mod) => {
      if (mod.hasAttribute("data-home-story") || mod.hasAttribute("data-home-hold")) {
        mod.classList.remove("home-module--tall");
        return;
      }
      const alwaysSlide = mod.matches(
        ".home-module--hero, .home-module--video, .ig-feed, .home-stay, .elementor-element-b46e728, .elementor-element-47c4bbc"
      );
      mod.classList.toggle("home-module--tall", !alwaysSlide && mod.scrollHeight > window.innerHeight * 1.12);
    });
  }

  // Module center - document Y of a block's midpoint.
  function moduleCenter(mod) {
    return layoutTop(mod) + mod.offsetHeight / 2;
  }

  // Stage dim - header video whites out until stay; cultura sticky takes over for its hold.
  function updateStage(focusY, best) {
    const heroCenter = hero ? moduleCenter(hero) : 0;
    const stayCenter = stay ? moduleCenter(stay) : heroCenter;
    const culturaTop = cultura ? layoutTop(cultura) : Number.POSITIVE_INFINITY;
    const culturaBottom = cultura ? culturaTop + cultura.offsetHeight : culturaTop;
    const last = modules[modules.length - 1];
    const lastCenter = last ? moduleCenter(last) : culturaTop;

    let dim = 0;
    let culturaIn = 0;

    if (!cultura) {
      dim = stay && stay !== hero ? clamp01((focusY - heroCenter) / Math.max(1, stayCenter - heroCenter)) : 0;
    } else if (window.scrollY + window.innerHeight > culturaTop + 24 && window.scrollY < culturaBottom - 24) {
      // Inside the cultura story - keep the second video fully on while it holds.
      culturaIn = 1;
      dim = 0;
    } else if (focusY <= stayCenter) {
      dim = stay && stay !== hero ? clamp01((focusY - heroCenter) / Math.max(1, stayCenter - heroCenter)) : 0;
      culturaIn = 0;
    } else if (focusY < culturaTop + window.innerHeight * 0.5) {
      const t = clamp01((focusY - stayCenter) / Math.max(1, culturaTop + window.innerHeight * 0.5 - stayCenter));
      dim = 1 - t;
      culturaIn = t;
    } else {
      culturaIn = clamp01(1 - (window.scrollY - culturaBottom + window.innerHeight) / Math.max(1, window.innerHeight * 0.6));
      dim = Math.min(0.88, clamp01((focusY - culturaBottom) / Math.max(1, lastCenter - culturaBottom)) * 0.88);
    }

    document.body.classList.toggle("is-stage-cultura", culturaIn > 0.45);
    document.body.classList.toggle("is-past-hero", Boolean(best && best !== hero));
    document.body.style.setProperty("--home-stage-dim", dim.toFixed(3));
    document.body.style.setProperty("--home-cultura-in", culturaIn.toFixed(3));
  }

  // Map distances - stagger chips once the points beat is on.
  function updateMapDistanceItems(amount) {
    if (!homeMap) return;
    homeMap.style.setProperty("--map-pins", amount.toFixed(3));
    homeMap.querySelectorAll(".home-distances__item").forEach((item, index) => {
      const vis = softstep(amount * 3.4 - index * 0.55);
      item.style.setProperty("--item-in", vis.toFixed(3));
    });
  }

  // Story layers - soft scroll-linked reveal, then hold on the finished frame.
  function updateStories() {
    stories.forEach((story) => {
      const layers = story.querySelectorAll("[data-story-beat]");
      const beats = storyBeats(story);
      const hold = storyHold(story);
      const pace = storyPace(story);

      if (!desktopQuery.matches) {
        story.dataset.beat = String(beats - 1);
        story.style.setProperty("--story-progress", "1");
        layers.forEach((layer) => {
          layer.style.setProperty("--beat-in", "1");
          layer.classList.add("is-shown");
        });
        if (story === homeMap) updateMapDistanceItems(1);
        return;
      }

      const top = layoutTop(story);
      const range = Math.max(1, story.offsetHeight - window.innerHeight);
      const progress = clamp01((window.scrollY - top) / range);
      const revealUnits = Math.max(0.001, beats * pace);
      const units = revealUnits + hold;
      const reveal = clamp01((progress * units) / revealUnits);
      const local = reveal * beats;
      const beat = Math.min(beats - 1, Math.floor(local + 0.001));

      story.dataset.beat = String(beat);
      story.style.setProperty("--story-progress", progress.toFixed(3));

      let mapPoints = 0;
      layers.forEach((layer) => {
        const need = Number(layer.getAttribute("data-story-beat")) || 0;
        // Beat 0 is already on when the pin lands; later beats ease in over the next unit.
        const amount = softstep(local - need + 1);
        layer.style.setProperty("--beat-in", amount.toFixed(3));
        layer.classList.toggle("is-shown", amount > 0.55);
        if (layer.classList.contains("home-distances")) mapPoints = amount;
      });

      if (story === homeMap) updateMapDistanceItems(mapPoints);
    });
  }

  // Visibility - how centered a module is; drives fade and the float from below.
  function visibilityFor(mod, focusY) {
    if (isVideoModule(mod)) return 1;
    const top = layoutTop(mod);
    const height = Math.max(1, mod.offsetHeight);
    const y = window.scrollY;
    if (mod === homeMap || mod.hasAttribute("data-home-story") || mod.hasAttribute("data-home-hold")) {
      const bottom = top + height;
      if (y + window.innerHeight > top + 48 && y < bottom - 48) return 1;
    }
    const center = top + height / 2;
    const range = Math.max(window.innerHeight * 0.62, height * 0.45);
    const dist = Math.abs(center - focusY);
    let vis = clamp01(1 - dist / range);
    vis = vis * vis * (3 - 2 * vis);
    if (footer && y + window.innerHeight >= layoutTop(footer) + 48 && mod === modules[modules.length - 1]) {
      vis *= 0.35;
    }
    return vis;
  }

  // Active module - fade each block with the scroll, keep the closest one interactive.
  function updateFocus() {
    ticking = false;
    if (!desktopQuery.matches) {
      modules.forEach((mod) => {
        mod.style.removeProperty("--home-in");
        mod.classList.remove("is-active", "is-leaving");
      });
      updateStories();
      return;
    }

    const focusY = window.scrollY + window.innerHeight / 2;
    let best = null;
    let bestVis = -1;

    modules.forEach((mod) => {
      const vis = visibilityFor(mod, focusY);
      mod.style.setProperty("--home-in", vis.toFixed(3));
      if (!isVideoModule(mod) && vis > bestVis) {
        bestVis = vis;
        best = mod;
      }
    });

    if (bestVis < 0.12) best = null;

    const videoFocus = cultura && focusY >= layoutTop(cultura) - 8 && focusY < layoutTop(cultura) + cultura.offsetHeight
      ? cultura
      : hero && focusY < (stay ? layoutTop(stay) : layoutTop(modules[1] || hero));
    if (!best && videoFocus) best = videoFocus === true ? hero : videoFocus;

    modules.forEach((mod) => {
      mod.classList.toggle("is-active", mod === best);
      mod.classList.remove("is-leaving");
    });

    updateStories();
    updateStage(focusY, best);
  }

  // Request frame - coalesce scroll and resize into one paint.
  function requestFrame() {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(updateFocus);
  }

  // Layout pass - measure story/hold travel and refresh focus.
  function relayout() {
    sizeStories();
    sizeHolds();
    markModules();
    requestFrame();
  }

  // Boot - pin the stage and let native scroll drive fade + story beats.
  document.documentElement.setAttribute("data-home-focus", "on");
  document.body.classList.add("home-parallax-ready");
  if (hero) hero.classList.add("is-active");
  relayout();

  window.addEventListener("scroll", requestFrame, { passive: true });
  window.addEventListener("resize", relayout);
  window.addEventListener("load", relayout);
  desktopQuery.addEventListener("change", relayout);
})();
