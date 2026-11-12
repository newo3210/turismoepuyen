// Actividades cards - sticky story beats for photo then title/copy reveal.
(function () {
  const stories = Array.from(document.querySelectorAll(".actividades-cards [data-page-story]"));
  if (!stories.length) return;

  // Desktop flag - sticky timeline only above the Astra breakpoint.
  const desktopQuery = window.matchMedia("(min-width: 922px)");
  let ticking = false;

  function storyBeats(story) {
    const n = Number(story.getAttribute("data-beats"));
    return Number.isFinite(n) && n > 0 ? Math.floor(n) : 2;
  }

  function storyHold(story) {
    const n = Number(story.getAttribute("data-hold"));
    return Number.isFinite(n) && n >= 0 ? n : 0.35;
  }

  function storyPace(story) {
    const n = Number(story.getAttribute("data-pace"));
    return Number.isFinite(n) && n > 0 ? n : 1.15;
  }

  function clamp01(value) {
    return Math.max(0, Math.min(1, value));
  }

  function softstep(value) {
    const t = clamp01(value);
    return t * t * t * (t * (t * 6 - 15) + 10);
  }

  function layoutTop(el) {
    let top = 0;
    let node = el;
    while (node) {
      top += node.offsetTop;
      node = node.offsetParent;
    }
    return top;
  }

  function sizeStories() {
    stories.forEach((story) => {
      if (!desktopQuery.matches) {
        story.style.removeProperty("height");
        story.style.removeProperty("min-height");
        return;
      }
      const end = Math.max(1, storyBeats(story));
      const travel = (end * storyPace(story) + storyHold(story)) * window.innerHeight;
      story.style.height = `${travel}px`;
      story.style.minHeight = `${travel}px`;
    });
  }

  function updateStories() {
    ticking = false;
    stories.forEach((story) => {
      const layers = story.querySelectorAll("[data-story-beat]");
      const beats = storyBeats(story);
      const hold = storyHold(story);
      const pace = storyPace(story);

      if (!desktopQuery.matches) {
        layers.forEach((layer) => {
          layer.style.setProperty("--beat-in", "1");
          layer.classList.add("is-shown");
        });
        return;
      }

      const top = layoutTop(story);
      const range = Math.max(1, story.offsetHeight - window.innerHeight);
      const progress = clamp01((window.scrollY - top) / range);
      const revealUnits = Math.max(0.001, beats * pace);
      const units = revealUnits + hold;
      const reveal = clamp01((progress * units) / revealUnits);
      const cursor = reveal * beats;

      layers.forEach((layer) => {
        const need = Number(layer.getAttribute("data-story-beat")) || 0;
        const start = need === 0 ? -1 : need - 1;
        const amount = softstep(cursor - start);
        layer.style.setProperty("--beat-in", amount.toFixed(3));
        layer.classList.toggle("is-shown", amount > 0.55);
      });
    });
  }

  function requestFrame() {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(updateStories);
  }

  function relayout() {
    sizeStories();
    requestFrame();
  }

  relayout();
  window.addEventListener("scroll", requestFrame, { passive: true });
  window.addEventListener("resize", relayout);
  window.addEventListener("load", relayout);
  desktopQuery.addEventListener("change", relayout);
})();
