(function () {
  "use strict";

  var state = { catalog: null, activeBook: null, activeDoc: null };
  var elements = {};

  function byId(id) { return document.getElementById(id); }
  function escapeHtml(value) {
    return String(value || "").replace(/[&<>"']/g, function (char) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[char];
    });
  }
  function normalize(value) { return String(value || "").trim().toLocaleLowerCase(); }
  function bookBySlug(slug) { return state.catalog.books.find(function (book) { return book.slug === slug; }); }
  function docById(id) { return state.catalog.docs.find(function (doc) { return doc.id === id; }); }

  function cacheElements() {
    ["siteTitle", "topMeta", "sidebar", "sidebarTitle", "searchInput", "catalogStatus", "navTree",
      "libraryHome", "heroTitle", "heroSubtitle", "heroAction", "shelfStats", "bookGrid", "documentView",
      "breadcrumb", "docTitle", "article", "previousLink", "nextLink", "outline", "outlineNav", "openNav",
      "closeNav", "scrim", "outlineToggle", "startReadingLink"].forEach(function (id) { elements[id] = byId(id); });
  }

  function groupDocs(docs) {
    return docs.reduce(function (groups, doc) {
      var label = doc.sections && doc.sections.length ? doc.sections[0] : "正文";
      var existing = groups.find(function (group) { return group.title === label; });
      if (!existing) { existing = { title: label, docs: [] }; groups.push(existing); }
      existing.docs.push(doc);
      return groups;
    }, []);
  }

  function renderSidebar(book, query) {
    state.activeBook = book || state.activeBook;
    var needle = normalize(query);
    var matchedCount = 0;
    var trees = state.catalog.books.map(function (item) {
      var docs = state.catalog.docs.filter(function (doc) {
        if (doc.bookSlug !== item.slug) return false;
        return !needle || normalize(doc.title + " " + doc.excerpt + " " + doc.relPath + " " + item.title).indexOf(needle) !== -1;
      });
      matchedCount += docs.length;
      if (needle && !docs.length) return "";

      var isActiveBook = state.activeBook && state.activeBook.slug === item.slug;
      var open = isActiveBook || Boolean(needle) ? " open" : "";
      var groups = groupDocs(docs).map(function (group) {
        return '<section class="nav-group"><h3>' + escapeHtml(group.title) + '</h3>' + group.docs.map(function (doc) {
          var active = state.activeDoc && state.activeDoc.id === doc.id ? " is-active" : "";
          return '<a class="doc-nav-link' + active + '" data-doc-id="' + doc.id + '" href="#/doc/' + doc.id + '">' +
            '<span>' + String(doc.order).padStart(2, "0") + '</span><strong>' + escapeHtml(doc.title) + '</strong></a>';
        }).join("") + "</section>";
      }).join("");

      return '<details class="book-tree" data-book-slug="' + escapeHtml(item.slug) + '"' + open + '>' +
        '<summary><span class="book-tree-marker" aria-hidden="true">›</span><strong>' + escapeHtml(item.title) +
        '</strong><small>' + item.docCount + ' 章</small></summary><div class="book-tree-children">' + groups + '</div></details>';
    }).join("");

    elements.sidebarTitle.textContent = "电子书目录";
    elements.catalogStatus.textContent = needle
      ? "找到 " + matchedCount + " 个章节"
      : state.catalog.books.length + " 本书 · " + state.catalog.docs.length + " 个章节";
    elements.navTree.innerHTML = trees || '<p class="empty-nav">没有匹配的章节。</p>';
  }

  function renderLibrary() {
    state.activeBook = null;
    state.activeDoc = null;
    elements.libraryHome.hidden = false;
    elements.documentView.hidden = true;
    elements.outline.hidden = true;
    elements.heroTitle.textContent = "把知识放进一条连续的阅读路径。";
    elements.heroSubtitle.textContent = state.catalog.site.subtitle;
    elements.heroAction.href = state.catalog.books.length ? "#/book/" + encodeURIComponent(state.catalog.books[0].slug) : "#/";
    elements.shelfStats.textContent = state.catalog.stats.books + " 本书 · " + state.catalog.stats.docs + " 篇内容";
    elements.bookGrid.innerHTML = state.catalog.books.map(function (book, index) {
      var cover = book.cover ? '<img src="' + book.cover + '" alt="' + escapeHtml(book.title) + '封面" loading="lazy">' :
        '<div class="cover-fallback"><span>' + escapeHtml(book.title.slice(0, 2)) + '</span></div>';
      return '<a class="book-card" href="#/book/' + encodeURIComponent(book.slug) + '">' +
        '<div class="book-cover">' + cover + '<span class="book-number">' + String(index + 1).padStart(2, "0") + '</span></div>' +
        '<div class="book-copy"><p class="book-tags">' + book.tags.map(escapeHtml).join(" · ") + '</p><h3>' + escapeHtml(book.title) +
        '</h3><p class="book-author">' + escapeHtml(book.author) + '</p><p>' + escapeHtml(book.description) +
        '</p><span class="book-open">开始阅读 <b>→</b></span></div></a>';
    }).join("");
    renderSidebar(null, elements.searchInput.value);
    document.title = state.catalog.site.title;
  }

  function renderOutline(headings) {
    elements.outlineNav.innerHTML = headings.map(function (heading) {
      return '<a class="outline-level-' + heading.level + '" href="#' + encodeURIComponent(heading.id) + '">' +
        escapeHtml(heading.text) + '</a>';
    }).join("") || '<span class="outline-empty">本页没有小标题</span>';
  }

  function renderPager(doc) {
    var previous = doc.previousId ? docById(doc.previousId) : null;
    var next = doc.nextId ? docById(doc.nextId) : null;
    elements.previousLink.innerHTML = previous ? '<small>上一篇</small><strong>← ' + escapeHtml(previous.title) + '</strong>' : "";
    elements.previousLink.href = previous ? "#/doc/" + previous.id : "#";
    elements.previousLink.hidden = !previous;
    elements.nextLink.innerHTML = next ? '<small>下一篇</small><strong>' + escapeHtml(next.title) + ' →</strong>' : "";
    elements.nextLink.href = next ? "#/doc/" + next.id : "#";
    elements.nextLink.hidden = !next;
  }

  function typesetMath() {
    if (!window.MathJax || !window.MathJax.startup || !window.MathJax.startup.promise) return;
    window.MathJax.startup.promise.then(function () {
      if (window.MathJax.typesetClear) window.MathJax.typesetClear([elements.article]);
      return window.MathJax.typesetPromise([elements.article]);
    }).catch(function () {});
  }

  async function renderDocument(id, anchor) {
    var summary = docById(id);
    if (!summary) { renderLibrary(); return; }
    var book = bookBySlug(summary.bookSlug);
    state.activeBook = book;
    elements.libraryHome.hidden = true;
    elements.documentView.hidden = false;
    elements.outline.hidden = false;
    elements.article.innerHTML = '<p class="loading-copy">正在打开章节…</p>';
    var response = await fetch("data/docs/" + id + ".json");
    if (!response.ok) throw new Error("章节数据加载失败");
    var doc = await response.json();
    state.activeDoc = doc;
    elements.breadcrumb.textContent = book.title + " / " + (doc.sections.join(" / ") || "正文");
    elements.docTitle.textContent = doc.title;
    elements.article.innerHTML = doc.html;
    renderOutline(doc.headings || []);
    renderPager(doc);
    renderSidebar(book, elements.searchInput.value);
    document.title = doc.title + " · " + state.catalog.site.title;
    typesetMath();
    requestAnimationFrame(function () {
      var target = anchor && document.getElementById(anchor);
      if (target) target.scrollIntoView({ block: "start" }); else window.scrollTo(0, 0);
    });
  }

  function parseRoute() {
    var raw = location.hash.slice(1) || "/";
    var parts = raw.split("?");
    return { path: parts[0], params: new URLSearchParams(parts[1] || "") };
  }

  async function route() {
    closeSidebar();
    var current = parseRoute();
    var docMatch = current.path.match(/^\/doc\/([^/]+)$/);
    var bookMatch = current.path.match(/^\/book\/(.+)$/);
    if (docMatch) {
      await renderDocument(docMatch[1], current.params.get("anchor") || "");
      return;
    }
    if (bookMatch) {
      var book = bookBySlug(decodeURIComponent(bookMatch[1]));
      if (book && book.firstDocId) { location.replace("#/doc/" + book.firstDocId); return; }
    }
    renderLibrary();
  }

  function openSidebar() { document.body.classList.add("nav-open"); }
  function closeSidebar() { document.body.classList.remove("nav-open"); }

  function bindEvents() {
    window.addEventListener("hashchange", function () { route().catch(showError); });
    elements.openNav.addEventListener("click", openSidebar);
    elements.closeNav.addEventListener("click", closeSidebar);
    elements.scrim.addEventListener("click", closeSidebar);
    elements.searchInput.addEventListener("input", function () { renderSidebar(state.activeBook, this.value); });
    elements.outlineToggle.addEventListener("click", function () { elements.outline.classList.toggle("is-open"); });
    elements.outlineNav.addEventListener("click", function (event) {
      var link = event.target.closest("a");
      if (!link) return;
      event.preventDefault();
      var target = document.getElementById(decodeURIComponent(link.hash.slice(1)));
      if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
      elements.outline.classList.remove("is-open");
    });
  }

  function showError(error) {
    console.error(error);
    elements.libraryHome.hidden = true;
    elements.documentView.hidden = false;
    elements.docTitle.textContent = "页面暂时无法打开";
    elements.article.innerHTML = '<div class="error-card"><p>' + escapeHtml(error.message) + '</p><a href="#/">返回书架</a></div>';
  }

  async function initialize() {
    cacheElements();
    bindEvents();
    var response = await fetch("data/catalog.json");
    if (!response.ok) throw new Error("目录数据加载失败，请先运行构建命令");
    state.catalog = await response.json();
    elements.siteTitle.textContent = state.catalog.site.title.replace(/\s*·\s*电子书$/, "");
    elements.topMeta.textContent = state.catalog.stats.books + " 本书 · " + state.catalog.stats.docs + " 篇内容";
    if (state.catalog.books.length && state.catalog.books[0].firstDocId) {
      elements.startReadingLink.href = "#/doc/" + state.catalog.books[0].firstDocId;
    }
    document.body.classList.remove("is-loading");
    await route();
  }

  initialize().catch(showError);
})();
