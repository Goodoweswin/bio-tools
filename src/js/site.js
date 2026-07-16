const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

if (!prefersReducedMotion) {
  const revealTargets = [
    ".feature-panel",
    ".route-cell",
    ".loop-card",
    ".research-brief",
    ".tool-card",
    ".tool-instrument",
    ".signal-row",
    ".news-item",
    ".project-brief",
    ".brief-cell",
    ".tool-entry",
    ".article-entry",
    ".output-entry",
    ".roadmap-panel",
    ".roadmap-list",
    ".research-module",
    ".research-module-rail a",
    ".module-board section",
    ".module-route",
    ".validation-card",
  ];

  const elements = document.querySelectorAll(revealTargets.join(","));

  if (elements.length) {
    document.documentElement.classList.add("has-scroll-reveal");

    elements.forEach((element, index) => {
      element.classList.add("reveal-on-scroll");
      element.style.setProperty("--reveal-delay", `${Math.min(index % 6, 5) * 45}ms`);
    });

    if ("IntersectionObserver" in window) {
      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              entry.target.classList.add("is-visible");
              observer.unobserve(entry.target);
            }
          });
        },
        { rootMargin: "0px 0px -8% 0px", threshold: 0.12 },
      );

      elements.forEach((element) => observer.observe(element));
    } else {
      elements.forEach((element) => element.classList.add("is-visible"));
    }
  }
}
