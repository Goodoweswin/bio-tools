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
    ".tools-module-rail a",
    ".tool-station",
    ".analysis-step-grid article",
    ".next-module-card",
    ".knowledge-route",
    ".knowledge-track-group",
    ".publication-principle-grid article",
    ".publication-record-group",
    ".publication-module-rail a",
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

const knowledgeSearch = document.querySelector("#knowledge-search");

if (knowledgeSearch) {
  const filterButtons = document.querySelectorAll(".knowledge-filter");
  const notes = document.querySelectorAll(".knowledge-note");
  const groups = document.querySelectorAll(".knowledge-track-group");
  const count = document.querySelector("#knowledge-count");
  const queryLabel = document.querySelector("#knowledge-query-label");
  const emptyState = document.querySelector("#empty-state");
  let activeTrack = "all";

  const updateKnowledgeIndex = () => {
    const query = knowledgeSearch.value.trim().toLowerCase();
    let visibleCount = 0;

    notes.forEach((note) => {
      const text = `${note.textContent} ${note.dataset.keywords}`.toLowerCase();
      const matchesQuery = !query || text.includes(query);
      const matchesTrack = activeTrack === "all" || note.dataset.track === activeTrack;
      const visible = matchesQuery && matchesTrack;

      note.hidden = !visible;
      if (visible) visibleCount += 1;
    });

    groups.forEach((group) => {
      group.hidden = !group.querySelector(".knowledge-note:not([hidden])");
    });

    const activeButton = document.querySelector(".knowledge-filter.is-active");
    count.textContent = `${visibleCount} / ${notes.length}`;
    queryLabel.textContent = activeButton ? activeButton.textContent : "All tracks";
    emptyState.classList.toggle("is-visible", visibleCount === 0);
  };

  knowledgeSearch.addEventListener("input", updateKnowledgeIndex);

  filterButtons.forEach((button) => {
    button.addEventListener("click", () => {
      activeTrack = button.dataset.track;
      filterButtons.forEach((item) => {
        const selected = item === button;
        item.classList.toggle("is-active", selected);
        item.setAttribute("aria-pressed", String(selected));
      });
      updateKnowledgeIndex();
    });
  });
}
