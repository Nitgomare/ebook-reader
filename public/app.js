(function () {
  "use strict";

  var state = { catalog: null, activeBook: null, activeDoc: null, activeCode: null };
  var elements = {};

  function byId(id) { return document.getElementById(id); }
  function escapeHtml(value) {
    return String(value == null ? "" : value).replace(/[&<>"']/g, function (char) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[char];
    });
  }
  function normalize(value) { return String(value || "").trim().toLocaleLowerCase(); }
  function bookBySlug(slug) { return state.catalog.books.find(function (book) { return book.slug === slug; }); }
  function docById(id) { return state.catalog.docs.find(function (doc) { return doc.id === id; }); }
  function codeById(id) { return state.catalog.code.find(function (file) { return file.id === id; }); }
  function formatBytes(bytes) {
    var value = Number(bytes || 0);
    if (value < 1024) return value + " B";
    if (value < 1024 * 1024) return (value / 1024).toFixed(1) + " KB";
    return (value / 1024 / 1024).toFixed(1) + " MB";
  }
  function codeLabel(file) {
    return { notebook: "Notebook", dataset: "数据", source: "源码", text: "文本" }[file.kind] || "文件";
  }

  function cacheElements() {
    ["siteTitle", "topMeta", "sidebar", "sidebarTitle", "searchLabel", "searchInput", "catalogStatus", "navTree",
      "libraryHome", "heroTitle", "heroSubtitle", "homeStats", "categorySections",
      "documentView", "breadcrumb", "docTitle", "article", "relatedCode", "relatedCodeList", "previousLink",
      "nextLink", "outline", "outlineNav", "openNav", "closeNav", "scrim", "outlineToggle", "startReadingLink",
      "codeLibrary", "codeCourseList", "codeView", "codeBreadcrumb", "codeTitle", "codeDownload", "codeMeta",
      "codeContent"].forEach(function (id) { elements[id] = byId(id); });
  }

  function hideViews() {
    [elements.libraryHome, elements.documentView, elements.codeLibrary, elements.codeView].forEach(function (view) {
      view.hidden = true;
    });
    elements.outline.hidden = true;
  }

  function groupDocs(docs) {
    return docs.reduce(function (groups, doc) {
      var label = doc.sections && doc.sections.length ? doc.sections[0] : "课程内容";
      var existing = groups.find(function (group) { return group.title === label; });
      if (!existing) { existing = { title: label, docs: [] }; groups.push(existing); }
      existing.docs.push(doc);
      return groups;
    }, []);
  }

  function renderSidebar(book, query) {
    state.activeBook = book || state.activeBook;
    elements.searchLabel.textContent = "搜索章节";
    elements.searchInput.placeholder = "标题、章节或关键词";
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
          return '<a class="doc-nav-link' + active + '" href="#/doc/' + doc.id + '"><span>' +
            String(doc.order).padStart(2, "0") + '</span><strong>' + escapeHtml(doc.title) + '</strong></a>';
        }).join("") + "</section>";
      }).join("");
      return '<details class="book-tree"' + open + '><summary><span class="book-tree-marker">›</span><strong>' +
        escapeHtml(item.title) + '</strong><small>' + item.docCount + ' 节</small></summary><div class="book-tree-children">' +
        groups + "</div></details>";
    }).join("");
    elements.sidebarTitle.textContent = "课程目录";
    elements.catalogStatus.textContent = needle ? "找到 " + matchedCount + " 个章节" :
      state.catalog.books.length + " 套内容 · " + state.catalog.docs.length + " 个章节";
    elements.navTree.innerHTML = trees || '<p class="empty-nav">没有匹配的章节。</p>';
  }

  function codeGroupLabel(name) {
    return name === "shared-data" ? "共享练习数据" :
      name.replace("chapter-", "第 ").replace(/^第 (\d+)$/, "第 $1 章");
  }

  function groupCodeFiles(files) {
    return files.reduce(function (groups, file) {
      var name = file.path.split("/")[0] || "其他";
      var group = groups.find(function (item) { return item.name === name; });
      if (!group) { group = { name: name, files: [] }; groups.push(group); }
      group.files.push(file);
      return groups;
    }, []);
  }

  function renderCodeSidebar(activeFile, query) {
    var needle = normalize(query);
    var matchedCount = 0;
    elements.searchLabel.textContent = "搜索代码与数据";
    elements.searchInput.placeholder = "文件名、路径或类型";
    var trees = state.catalog.books.map(function (book) {
      var files = state.catalog.code.filter(function (file) {
        if (file.bookSlug !== book.slug) return false;
        return !needle || normalize(file.name + " " + file.path + " " + file.language + " " + codeLabel(file)).indexOf(needle) !== -1;
      });
      matchedCount += files.length;
      if (!files.length) return "";
      var isActiveBook = activeFile && activeFile.bookSlug === book.slug;
      var groups = groupCodeFiles(files).map(function (group) {
        var isActiveGroup = isActiveBook && activeFile.path.split("/")[0] === group.name;
        var open = needle || isActiveGroup ? " open" : "";
        var links = group.files.map(function (file) {
          var active = activeFile && activeFile.id === file.id ? " is-active" : "";
          var label = file.path.split("/").slice(1).join("/") || file.name;
          return '<a class="code-nav-link' + active + '" href="#/code/' + file.id + '" title="' +
            escapeHtml(file.path) + '"><span>' + escapeHtml(codeLabel(file)) + '</span><strong>' +
            escapeHtml(label) + '</strong></a>';
        }).join("");
        return '<details class="code-folder"' + open + '><summary><span class="book-tree-marker">›</span><strong>' +
          escapeHtml(codeGroupLabel(group.name)) + '</strong><small>' + group.files.length + '</small></summary><div>' +
          links + '</div></details>';
      }).join("");
      var openBook = needle || isActiveBook || !activeFile && state.catalog.books.filter(function (item) { return item.codeCount; })[0].slug === book.slug ? " open" : "";
      return '<details class="book-tree code-book-tree"' + openBook + '><summary><span class="book-tree-marker">›</span><strong>' +
        escapeHtml(book.title) + '</strong><small>' + files.length + ' 个</small></summary><div class="book-tree-children">' +
        groups + '</div></details>';
    }).join("");
    elements.sidebarTitle.textContent = "代码与数据";
    elements.catalogStatus.textContent = needle ? "找到 " + matchedCount + " 个文件" : state.catalog.code.length + " 个可在线查看文件";
    elements.navTree.innerHTML = trees || '<p class="empty-nav">没有匹配的代码或数据。</p>';
  }

  function renderCourseCard(book, index) {
    return '<a class="course-card" href="#/book/' + encodeURIComponent(book.slug) + '">' +
      '<div class="course-index">0' + (index + 1) + '</div><div class="course-copy"><p class="book-tags">' +
      book.tags.map(escapeHtml).join(" · ") + '</p><h3>' + escapeHtml(book.title) + '</h3><p>' +
      escapeHtml(book.description) + '</p><div class="course-facts"><span>' + book.docCount + ' 节教程</span><span>' +
      book.codeCount + ' 个代码/数据文件</span></div><strong>进入学习路径 →</strong></div></a>';
  }

  function renderResourceCard(book) {
    var cover = book.cover ? '<img src="' + book.cover + '" alt="' + escapeHtml(book.title) + '封面" loading="lazy">' :
      '<div class="cover-fallback"><span>' + escapeHtml(book.title.slice(0, 2)) + '</span></div>';
    return '<a class="book-card" href="#/book/' + encodeURIComponent(book.slug) + '"><div class="book-cover">' + cover +
      '</div><div class="book-copy"><p class="book-tags">' + book.tags.map(escapeHtml).join(" · ") + '</p><h3>' +
      escapeHtml(book.title) + '</h3><p class="book-author">' + escapeHtml(book.author) + '</p><p>' +
      escapeHtml(book.description) + '</p><div class="book-facts"><span>' + book.docCount + ' 个章节</span>' +
      (book.codeCount ? '<span>' + book.codeCount + ' 个代码/数据文件</span>' : '') +
      '</div><span class="book-open">进入学习 <b>→</b></span></div></a>';
  }

  function renderCategory(category) {
    var books = state.catalog.books.filter(function (book) { return book.category === category.id; });
    if (!books.length) return "";
    return '<section class="shelf-section category-section" aria-labelledby="category-' + escapeHtml(category.id) + '">' +
      '<div class="section-heading"><div><p class="eyebrow">' + escapeHtml(category.eyebrow || category.id) +
      '</p><h2 id="category-' + escapeHtml(category.id) + '">' + escapeHtml(category.title) + '</h2></div><p>' +
      escapeHtml(category.description || "") + '</p></div><div class="book-grid">' +
      books.map(renderResourceCard).join("") + '</div></section>';
  }

  function renderLibrary() {
    hideViews();
    state.activeBook = null;
    state.activeDoc = null;
    state.activeCode = null;
    elements.libraryHome.hidden = false;
    var categories = state.catalog.site.categories || [];
    elements.heroTitle.textContent = state.catalog.site.title;
    elements.heroSubtitle.textContent = state.catalog.site.subtitle;
    elements.homeStats.innerHTML = '<span><strong>' + categories.length + '</strong> 个知识领域</span><span><strong>' +
      state.catalog.stats.books + '</strong> 套课程与教材</span><span><strong>' +
      state.catalog.stats.docs + '</strong> 个章节</span><span><strong>' + state.catalog.stats.code + '</strong> 个代码与数据文件</span>';
    elements.categorySections.innerHTML = categories.map(renderCategory).join("");
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
    elements.previousLink.innerHTML = previous ? '<small>上一节</small><strong>← ' + escapeHtml(previous.title) + '</strong>' : "";
    elements.previousLink.href = previous ? "#/doc/" + previous.id : "#";
    elements.previousLink.hidden = !previous;
    elements.nextLink.innerHTML = next ? '<small>下一节</small><strong>' + escapeHtml(next.title) + ' →</strong>' : "";
    elements.nextLink.href = next ? "#/doc/" + next.id : "#";
    elements.nextLink.hidden = !next;
  }

  function renderRelatedCode(ids) {
    var files = (ids || []).map(codeById).filter(Boolean);
    elements.relatedCode.hidden = !files.length;
    elements.relatedCodeList.innerHTML = files.map(function (file) {
      return '<a class="code-file-card" href="#/code/' + file.id + '"><span class="code-kind">' + codeLabel(file) +
        '</span><strong>' + escapeHtml(file.name) + '</strong><small>' + escapeHtml(file.path) + ' · ' +
        formatBytes(file.size) + '</small></a>';
    }).join("");
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
    hideViews();
    var book = bookBySlug(summary.bookSlug);
    state.activeBook = book;
    elements.documentView.hidden = false;
    elements.outline.hidden = false;
    elements.article.innerHTML = '<p class="loading-copy">正在打开课程…</p>';
    var response = await fetch("data/docs/" + id + ".json", { cache: "no-store" });
    if (!response.ok) throw new Error("课程内容加载失败");
    var doc = await response.json();
    state.activeDoc = doc;
    state.activeCode = null;
    elements.breadcrumb.textContent = book.title + " / " + (doc.sections.join(" / ") || "课程内容");
    elements.docTitle.textContent = doc.title;
    elements.article.innerHTML = doc.html;
    renderRelatedCode(doc.codeFiles);
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

  function renderCodeLibrary() {
    hideViews();
    state.activeBook = null;
    state.activeDoc = null;
    state.activeCode = null;
    elements.codeLibrary.hidden = false;
    var books = state.catalog.books.filter(function (book) { return book.codeCount; });
    elements.codeCourseList.innerHTML = books.map(function (book) {
      var files = state.catalog.code.filter(function (file) { return file.bookSlug === book.slug; });
      var groups = groupCodeFiles(files);
      return '<section class="code-course"><div class="section-heading"><div><p class="eyebrow">' +
        escapeHtml(book.author) + '</p><h2>' + escapeHtml(book.title) + '</h2></div><p>' + files.length +
        ' 个文件</p></div>' + groups.map(function (group) {
          return '<details class="code-group" open><summary>' + escapeHtml(codeGroupLabel(group.name)) + '<small>' +
            group.files.length + '</small></summary><div>' + group.files.map(function (file) {
              return '<a href="#/code/' + file.id + '"><span>' + codeLabel(file) + '</span><strong>' +
                escapeHtml(file.name) + '</strong><small>' + formatBytes(file.size) + '</small></a>';
            }).join("") + '</div></details>';
        }).join("") + '</section>';
    }).join("");
    renderCodeSidebar(null, elements.searchInput.value);
    document.title = "代码与数据 · " + state.catalog.site.title;
    window.scrollTo(0, 0);
  }

  function renderNotebook(cells) {
    return (cells || []).map(function (cell) {
      if (cell.type === "markdown") {
        return '<section class="notebook-cell markdown-cell"><span class="cell-label">Markdown ' + cell.index +
          '</span><div class="notebook-markdown">' + (cell.html || "") + '</div></section>';
      }
      var output = cell.output ? '<div class="cell-output"><span>输出</span><pre>' + escapeHtml(cell.output) + '</pre></div>' : "";
      return '<section class="notebook-cell"><span class="cell-label">In [' + cell.index + ']</span><pre><code>' +
        escapeHtml(cell.source) + '</code></pre>' + output + '</section>';
    }).join("");
  }

  async function renderCode(id) {
    var summary = codeById(id);
    if (!summary) { renderCodeLibrary(); return; }
    hideViews();
    elements.codeView.hidden = false;
    elements.codeContent.innerHTML = '<p class="loading-copy">正在加载文件…</p>';
    var response = await fetch("data/code/" + id + ".json", { cache: "no-store" });
    if (!response.ok) throw new Error("代码文件加载失败");
    var file = await response.json();
    var book = bookBySlug(file.bookSlug);
    state.activeBook = book;
    state.activeDoc = null;
    state.activeCode = file;
    elements.codeBreadcrumb.textContent = book.title + " / " + codeLabel(file);
    elements.codeTitle.textContent = file.name;
    elements.codeDownload.href = file.downloadUrl;
    elements.codeMeta.innerHTML = '<span>' + escapeHtml(file.path) + '</span><span>' + formatBytes(file.size) +
      '</span><span>' + escapeHtml(file.language) + '</span>' + (file.truncated ? '<strong>网页仅显示前 256 KB</strong>' : '');
    elements.codeContent.innerHTML = file.kind === "notebook" ? renderNotebook(file.cells) :
      '<pre class="source-preview"><code>' + escapeHtml(file.content || "") + '</code></pre>';
    renderCodeSidebar(file, elements.searchInput.value);
    document.title = file.name + " · " + state.catalog.site.title;
    window.scrollTo(0, 0);
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
    var codeMatch = current.path.match(/^\/code\/([^/]+)$/);
    var bookMatch = current.path.match(/^\/book\/(.+)$/);
    if (docMatch) { await renderDocument(docMatch[1], current.params.get("anchor") || ""); return; }
    if (codeMatch) { await renderCode(codeMatch[1]); return; }
    if (current.path === "/code") { renderCodeLibrary(); return; }
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
    window.addEventListener("load", function () { if (state.activeDoc) typesetMath(); });
    elements.openNav.addEventListener("click", openSidebar);
    elements.closeNav.addEventListener("click", closeSidebar);
    elements.scrim.addEventListener("click", closeSidebar);
    elements.searchInput.addEventListener("input", function () {
      var codeMode = !elements.codeLibrary.hidden || !elements.codeView.hidden;
      if (codeMode) renderCodeSidebar(state.activeCode, this.value);
      else renderSidebar(state.activeBook, this.value);
    });
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
    hideViews();
    elements.documentView.hidden = false;
    elements.docTitle.textContent = "页面暂时无法打开";
    elements.article.innerHTML = '<div class="error-card"><p>' + escapeHtml(error.message) + '</p><a href="#/">返回学习中心</a></div>';
  }

  async function initialize() {
    cacheElements();
    bindEvents();
    var response = await fetch("data/catalog.json", { cache: "no-store" });
    if (!response.ok) throw new Error("课程目录加载失败，请先运行构建命令");
    state.catalog = await response.json();
    state.catalog.code = state.catalog.code || [];
    elements.siteTitle.textContent = state.catalog.site.title;
    elements.topMeta.textContent = state.catalog.stats.docs + " 个章节 · " + state.catalog.stats.code + " 个代码/数据文件";
    var firstCourse = state.catalog.books.find(function (book) { return book.firstDocId; });
    if (firstCourse) elements.startReadingLink.href = "#/doc/" + firstCourse.firstDocId;
    document.body.classList.remove("is-loading");
    await route();
  }

  initialize().catch(showError);
})();
