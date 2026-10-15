const menuButton = document.querySelector(".menu-toggle");
const navigation = document.querySelector("#site-links");

if (menuButton && navigation) {
  const setMenu = (open) => {
    navigation.classList.toggle("is-open", open);
    menuButton.setAttribute("aria-expanded", String(open));
    menuButton.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    menuButton.title = open ? "Close menu" : "Open menu";
    menuButton.querySelector("i").className = open
      ? "fas fa-xmark"
      : "fas fa-bars";
  };

  menuButton.addEventListener("click", () => {
    setMenu(menuButton.getAttribute("aria-expanded") !== "true");
  });
  navigation.addEventListener("click", (event) => {
    if (event.target.closest("a")) setMenu(false);
  });
  document.addEventListener("keydown", (event) => {
    if (
      event.key === "Escape" &&
      menuButton.getAttribute("aria-expanded") === "true"
    ) {
      setMenu(false);
      menuButton.focus();
    }
  });
  document.addEventListener("click", (event) => {
    if (!event.target.closest(".site-nav")) setMenu(false);
  });
  window
    .matchMedia("(min-width: 701px)")
    .addEventListener("change", () => setMenu(false));

  const normalizePath = (path) =>
    path.replace(/\.html$/, "").replace(/\/$/, "") || "/index";
  navigation.querySelectorAll("a").forEach((link) => {
    if (
      normalizePath(new URL(link.href).pathname) ===
      normalizePath(location.pathname)
    ) {
      link.setAttribute("aria-current", "page");
    }
  });
  document.documentElement.classList.add("js");
}

const knowledgeSearch = document.querySelector("#knowledge-search");

if (knowledgeSearch) {
  const filterButtons = [...document.querySelectorAll(".knowledge-filter")];
  const notes = [...document.querySelectorAll(".knowledge-note")];
  const groups = document.querySelectorAll(".knowledge-track-group");
  const count = document.querySelector("#knowledge-count");
  const queryLabel = document.querySelector("#knowledge-query-label");
  const emptyState = document.querySelector("#empty-state");
  let activeTrack = "all";

  const updateNotes = () => {
    const query = knowledgeSearch.value.trim().toLowerCase();
    let visibleCount = 0;
    notes.forEach((note) => {
      const text = (
        note.textContent +
        " " +
        (note.dataset.keywords || "")
      ).toLowerCase();
      const visible =
        (!query || text.includes(query)) &&
        (activeTrack === "all" || note.dataset.track === activeTrack);
      note.hidden = !visible;
      if (visible) visibleCount++;
    });
    groups.forEach((group) => {
      group.hidden = !group.querySelector(".knowledge-note:not([hidden])");
    });
    count.textContent =
      visibleCount + (visibleCount === 1 ? " note" : " notes");
    queryLabel.textContent =
      " · " +
      filterButtons.find((button) => button.dataset.track === activeTrack)
        .textContent;
    emptyState.hidden = visibleCount !== 0;
  };

  const selectTrack = (track) => {
    activeTrack = track;
    filterButtons.forEach((button) => {
      const selected = button.dataset.track === track;
      button.classList.toggle("is-active", selected);
      button.setAttribute("aria-pressed", String(selected));
    });
    updateNotes();
  };

  knowledgeSearch.addEventListener("input", updateNotes);
  filterButtons.forEach((button) =>
    button.addEventListener("click", () => selectTrack(button.dataset.track)),
  );
  document.querySelector("#reset-notes").addEventListener("click", () => {
    knowledgeSearch.value = "";
    selectTrack("all");
    knowledgeSearch.focus();
  });
  updateNotes();
}
