const root = document.querySelector("[data-hero-carousel]");

if (root) {
  const viewport = root.querySelector("[data-carousel-viewport]");
  const slides = [...root.querySelectorAll("[data-carousel-slide]")];
  const dots = [...root.querySelectorAll("[data-carousel-dot]")];
  const pause = root.querySelector("[data-carousel-pause]");
  const status = root.querySelector("[data-carousel-status]");
  const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)");
  let current = 0;
  let playing = !reducedMotion.matches;
  let hovered = false;
  let focused = false;
  let visible = false;
  let timer;
  let scrollTimer;

  const schedule = () => {
    clearTimeout(timer);
    if (playing && visible && !hovered && !focused && !document.hidden) {
      timer = setTimeout(() => select((current + 1) % slides.length), 8000);
    }
  };

  const setCurrent = (index) => {
    current = index;
    if (index === 0) root.querySelectorAll("details[open]").forEach((details) => { details.open = false; });
    root.dataset.slide = String(index);
    slides.forEach((slide, i) => {
      slide.inert = i !== index;
      slide.setAttribute("aria-hidden", String(i !== index));
    });
    dots.forEach((dot, i) => dot.setAttribute("aria-current", String(i === index)));
    status.textContent = slides[index].getAttribute("aria-label");
    schedule();
  };

  const select = (index, instant = false) => {
    setCurrent((index + slides.length) % slides.length);
    viewport.scrollTo({ left: current * viewport.clientWidth, behavior: instant || reducedMotion.matches ? "instant" : "smooth" });
  };

  const updatePlayback = () => {
    pause.setAttribute("aria-pressed", String(!playing));
    pause.setAttribute("aria-label", playing ? "暂停自动轮播" : "播放自动轮播");
    pause.querySelector("[data-pause-icon]").toggleAttribute("hidden", !playing);
    pause.querySelector("[data-play-icon]").toggleAttribute("hidden", playing);
    status.setAttribute("aria-live", playing ? "off" : "polite");
    schedule();
  };

  root.querySelector("[data-carousel-prev]").addEventListener("click", () => select(current - 1));
  root.querySelector("[data-carousel-next]").addEventListener("click", () => select(current + 1));
  dots.forEach((dot, i) => dot.addEventListener("click", () => select(i)));
  pause.addEventListener("click", () => { playing = !playing; updatePlayback(); });
  root.addEventListener("pointerenter", (event) => {
    if (event.pointerType !== "touch") { hovered = true; schedule(); }
  });
  root.addEventListener("pointerleave", () => { hovered = false; schedule(); });
  root.addEventListener("focusin", () => { focused = true; schedule(); });
  root.addEventListener("focusout", (event) => { focused = root.contains(event.relatedTarget); schedule(); });
  document.addEventListener("visibilitychange", schedule);
  viewport.addEventListener("scroll", () => {
    clearTimeout(timer);
    clearTimeout(scrollTimer);
    scrollTimer = setTimeout(() => setCurrent(Math.max(0, Math.min(slides.length - 1, Math.round(viewport.scrollLeft / viewport.clientWidth)))), 120);
  }, { passive: true });
  new ResizeObserver(() => select(current, true)).observe(viewport);
  new IntersectionObserver(([entry]) => { visible = entry.isIntersecting; schedule(); }).observe(root);
  reducedMotion.addEventListener("change", () => {
    if (reducedMotion.matches) { playing = false; updatePlayback(); }
  });
  window.addEventListener("hashchange", () => {
    if (location.hash === "#time") select(1, true);
  });
  updatePlayback();
  select(location.hash === "#time" ? 1 : 0, true);
}
