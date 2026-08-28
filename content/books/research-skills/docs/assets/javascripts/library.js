(function () {
  "use strict";

  function normalize(value) {
    return (value || "").trim().toLocaleLowerCase();
  }

  function initializeLibrary(root) {
    if (!root || root.dataset.libraryReady === "true") return;

    var cards = Array.prototype.slice.call(
      root.querySelectorAll("[data-library-card]")
    );
    var search = root.querySelector("[data-library-search]");
    var filters = root.querySelector("[data-library-filters]");
    var resultCount = root.querySelector("[data-library-result-count]");
    var totalCount = root.querySelector("[data-library-total]");
    var categoryTotal = root.querySelector("[data-library-category-total]");
    var empty = root.querySelector("[data-library-empty]");
    var activeCategory = "全部";

    if (!cards.length || !search || !filters) return;

    var categories = cards.reduce(function (result, card) {
      var tags = (card.dataset.tags || "").split(",").map(function (tag) { return tag.trim(); });
      tags.forEach(function (tag) {
        if (tag && result.indexOf(tag) === -1) result.push(tag);
      });
      return result;
    }, []);

    categories.forEach(function (category) {
      var button = document.createElement("button");
      button.type = "button";
      button.dataset.libraryFilter = category;
      button.textContent = category;
      filters.appendChild(button);
    });

    if (totalCount) totalCount.textContent = String(cards.length);
    if (categoryTotal) categoryTotal.textContent = String(categories.length);

    function updateResults() {
      var query = normalize(search.value);
      var visibleCount = 0;

      cards.forEach(function (card) {
        var cardTags = (card.dataset.tags || "").split(",");
        var matchesCategory = activeCategory === "全部" || cardTags.indexOf(activeCategory) !== -1;
        var searchable = normalize((card.dataset.search || "") + " " + (card.dataset.tags || ""));
        var matchesQuery = !query || searchable.indexOf(query) !== -1;
        var visible = matchesCategory && matchesQuery;

        card.hidden = !visible;
        if (visible) visibleCount += 1;
      });

      if (resultCount) resultCount.textContent = String(visibleCount);
      if (empty) empty.hidden = visibleCount !== 0;
    }

    filters.addEventListener("click", function (event) {
      var button = event.target.closest("[data-library-filter]");
      if (!button) return;

      activeCategory = button.dataset.libraryFilter;
      filters.querySelectorAll("[data-library-filter]").forEach(function (item) {
        item.classList.toggle("is-active", item === button);
      });
      updateResults();
    });

    search.addEventListener("input", updateResults);
    root.dataset.libraryReady = "true";
    updateResults();
  }

  function initializeAllLibraries() {
    document.querySelectorAll("[data-library]").forEach(initializeLibrary);
  }

  if (typeof document$ !== "undefined") {
    document$.subscribe(initializeAllLibraries);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initializeAllLibraries);
  } else {
    initializeAllLibraries();
  }
})();
