(function () {
  "use strict";

  var state = { catalog: null, activeBook: null, activeDoc: null, activeCode: null, activeResource: false };
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

  function sourcePreview(content, language) {
    return '<pre class="source-preview" data-language="' + escapeHtml(language || "text") + '"><code>' +
      escapeHtml(content || "") + '</code></pre>';
  }

  function codeLanguage(pre, code) {
    var raw = pre.dataset.language || "";
    if (!raw) {
      Array.prototype.some.call(code.classList, function (name) {
        if (name.indexOf("language-") !== 0) return false;
        raw = name.slice(9);
        return true;
      });
    }
    var key = normalize(raw);
    var labels = {
      py: "Python", python: "Python", js: "JavaScript", javascript: "JavaScript",
      ts: "TypeScript", typescript: "TypeScript", json: "JSON", csv: "CSV",
      md: "Markdown", markdown: "Markdown", html: "HTML", css: "CSS",
      sh: "Shell", bash: "Shell", shell: "Shell", powershell: "PowerShell",
      ps1: "PowerShell", sql: "SQL", yaml: "YAML", yml: "YAML",
      xml: "XML", text: "代码", plaintext: "代码", txt: "代码"
    };
    return labels[key] || (raw ? raw.toUpperCase() : "代码");
  }

  function enhanceCodeBlocks(root) {
    var blocks = root.querySelectorAll ? root.querySelectorAll("pre > code") : [];
    Array.prototype.forEach.call(blocks, function (code) {
      var pre = code.parentElement;
      if (!pre || pre.parentElement.classList.contains("code-block")) return;
      var wrapper = document.createElement("div");
      wrapper.className = "code-block";
      wrapper.innerHTML = '<div class="code-toolbar"><span class="code-language">' +
        escapeHtml(codeLanguage(pre, code)) +
        '</span><button class="code-copy-button" type="button" aria-label="复制代码">' +
        '<span class="copy-icon" aria-hidden="true">⧉</span><span class="copy-label">复制</span></button></div>';
      pre.parentNode.insertBefore(wrapper, pre);
      wrapper.appendChild(pre);
    });
  }

  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(text);
    return new Promise(function (resolve, reject) {
      var helper = document.createElement("textarea");
      helper.value = text;
      helper.setAttribute("readonly", "");
      helper.style.position = "fixed";
      helper.style.opacity = "0";
      document.body.appendChild(helper);
      helper.select();
      try {
        if (!document.execCommand("copy")) throw new Error("浏览器不支持自动复制");
        resolve();
      } catch (error) {
        reject(error);
      } finally {
        helper.remove();
      }
    });
  }

  function setCopyState(button, label, className) {
    window.clearTimeout(button.copyResetTimer);
    button.querySelector(".copy-label").textContent = label;
    button.classList.remove("is-copied", "is-error");
    if (className) button.classList.add(className);
    button.setAttribute("aria-label", label === "复制" ? "复制代码" : label);
    if (label !== "复制") {
      button.copyResetTimer = window.setTimeout(function () {
        setCopyState(button, "复制", "");
      }, 1800);
    }
  }

  function cacheElements() {
    ["siteTitle", "topMeta", "sidebar", "sidebarTitle", "searchLabel", "searchInput", "catalogStatus", "navTree",
      "libraryHome", "heroTitle", "heroSubtitle", "homeStats", "categorySections",
      "homeCategoryNav",
      "documentView", "breadcrumb", "docTitle", "article", "relatedCode", "relatedCodeList", "previousLink",
      "nextLink", "outline", "outlineNav", "openNav", "closeNav", "scrim", "outlineToggle",
      "codeLibrary", "codeCourseList", "codeView", "codeBreadcrumb", "codeTitle", "codeDownload", "codeMeta",
      "codeContent"].forEach(function (id) { elements[id] = byId(id); });
  }

  function hideViews() {
    document.body.classList.remove("home-view");
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
    if (book) { renderBookSidebar(book, needle); return; }
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
      var resourceActive = isActiveBook && state.activeResource ? " is-active" : "";
      var resourceLink = '<a class="course-resource-link' + resourceActive + '" href="#/resources/' +
        encodeURIComponent(item.slug) + '"><span>↗</span><strong>课程资源</strong></a>';
      var groups = groupDocs(docs).map(function (group) {
        return '<section class="nav-group"><h3>' + escapeHtml(group.title) + '</h3>' + group.docs.map(function (doc) {
          var active = state.activeDoc && state.activeDoc.id === doc.id ? " is-active" : "";
          return '<a class="doc-nav-link' + active + '" href="#/doc/' + doc.id + '"><span>' +
            String(doc.order).padStart(2, "0") + '</span><strong>' + escapeHtml(doc.title) + '</strong></a>';
        }).join("") + "</section>";
      }).join("");
      return '<details class="book-tree"' + open + '><summary><span class="book-tree-marker">›</span><strong>' +
        escapeHtml(item.title) + '</strong><small>' + item.docCount + ' 节</small></summary><div class="book-tree-children">' +
        resourceLink + groups + "</div></details>";
    }).join("");
    elements.sidebarTitle.textContent = "课程目录";
    elements.catalogStatus.textContent = needle ? "找到 " + matchedCount + " 个章节" :
      state.catalog.books.length + " 套内容 · " + state.catalog.docs.length + " 个章节";
    elements.navTree.innerHTML = trees || '<p class="empty-nav">没有匹配的章节。</p>';
  }

  function codeGroupLabel(name) {
    var labels = {
      "shared-data": "共享练习数据",
      bayes: "贝叶斯分类",
      cluster: "聚类",
      compare: "算法对照实验",
      dimension_reduction: "降维",
      discriminant_analysis: "判别分析",
      ensemble: "集成学习",
      factorization_machine: "因子分解机",
      feature_selection: "特征选择",
      linear_model: "线性模型",
      metrices: "评估指标",
      svm: "支持向量机",
      tree: "决策树"
    };
    return labels[name] || name.replace("chapter-", "第 ").replace(/^第 (\d+)$/, "第 $1 章").replace(/_/g, " ");
  }

  function groupCodeFiles(files) {
    return files.reduce(function (groups, file) {
      var parts = file.path.split("/");
      var chapterMatch = file.name.match(/^chapter[-_ ]?0*(\d+)/i);
      var name = parts.length > 1 ? parts[0] : chapterMatch ? "chapter-" + chapterMatch[1] : "其他";
      var group = groups.find(function (item) { return item.name === name; });
      if (!group) { group = { name: name, files: [] }; groups.push(group); }
      group.files.push(file);
      return groups;
    }, []);
  }

  function codeFolders(files, needle, activeFile) {
    return groupCodeFiles(files).map(function (group) {
      var isActiveGroup = activeFile && activeFile.path.split("/")[0] === group.name;
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
  }

  function renderBookSidebar(book, needle) {
    var docs = state.catalog.docs.filter(function (doc) {
      if (doc.bookSlug !== book.slug) return false;
      return !needle || normalize(doc.title + " " + doc.excerpt + " " + doc.relPath).indexOf(needle) !== -1;
    });
    var resourceActive = state.activeResource ? " is-active" : "";
    var resourceLink = '<a class="course-resource-link' + resourceActive + '" href="#/resources/' +
      encodeURIComponent(book.slug) + '"><span>↗</span><strong>课程资源</strong></a>';
    var chapters = groupDocs(docs).map(function (group) {
      var isStandaloneKnowledgeBase = book.slug === "research-skills" && group.title === "正文" &&
        group.docs.length === 1 && group.docs[0].relPath === "03-site-building/index.md";
      var groupLabel = group.title === "正文" ? "章节" : group.title;
      var groupHeading = isStandaloneKnowledgeBase ? "" : '<h3>' + escapeHtml(groupLabel) + '</h3>';
      return '<section class="nav-group">' + groupHeading + group.docs.map(function (doc) {
        var active = state.activeDoc && state.activeDoc.id === doc.id ? " is-active" : "";
        return '<a class="doc-nav-link' + active + '" href="#/doc/' + doc.id + '"><span>' +
          String(doc.order).padStart(2, "0") + '</span><strong>' + escapeHtml(doc.title) + '</strong></a>';
      }).join("") + "</section>";
    }).join("");
    var codeNav = "";
    if (book.codeCount) {
      var files = state.catalog.code.filter(function (file) { return file.bookSlug === book.slug; });
      codeNav = '<section class="nav-group book-code-nav"><h3>代码与数据</h3>' +
        codeFolders(files, needle, state.activeCode) + '</section>';
    }
    var nav = resourceLink + chapters + codeNav;
    elements.sidebarTitle.textContent = book.title;
    elements.catalogStatus.textContent = needle ? "找到 " + docs.length + " 个章节" :
      (book.author ? book.author + " · " : "") + docs.length + " 个章节";
    elements.navTree.innerHTML = nav || '<p class="empty-nav">没有匹配的章节。</p>';
  }

  function renderCodeSidebar(activeFile, query) {
    var needle = normalize(query);
    var matchedCount = 0;
    elements.searchLabel.textContent = "搜索代码与数据";
    elements.searchInput.placeholder = "文件名、路径或类型";
    if (activeFile) {
      var files = state.catalog.code.filter(function (file) {
        if (file.bookSlug !== activeFile.bookSlug) return false;
        return !needle || normalize(file.name + " " + file.path + " " + file.language + " " + codeLabel(file)).indexOf(needle) !== -1;
      });
      var book = bookBySlug(activeFile.bookSlug);
      elements.sidebarTitle.textContent = book ? book.title + " · 代码" : "代码与数据";
      elements.catalogStatus.textContent = needle ? "找到 " + files.length + " 个文件" : files.length + " 个文件";
      elements.navTree.innerHTML = codeFolders(files, needle, activeFile) ||
        '<p class="empty-nav">没有匹配的代码或数据。</p>';
      return;
    }
    var trees = state.catalog.books.map(function (book) {
      var files = state.catalog.code.filter(function (file) {
        if (file.bookSlug !== book.slug) return false;
        return !needle || normalize(file.name + " " + file.path + " " + file.language + " " + codeLabel(file)).indexOf(needle) !== -1;
      });
      matchedCount += files.length;
      if (!files.length) return "";
      var isActiveBook = activeFile && activeFile.bookSlug === book.slug;
      var groups = codeFolders(files, needle, activeFile);
      var openBook = needle || isActiveBook || !activeFile && state.catalog.books.filter(function (item) { return item.codeCount; })[0].slug === book.slug ? " open" : "";
      return '<details class="book-tree code-book-tree"' + openBook + '><summary><span class="book-tree-marker">›</span><strong>' +
        escapeHtml(book.title) + '</strong><small>' + files.length + ' 个</small></summary><div class="book-tree-children">' +
        groups + '</div></details>';
    }).join("");
    elements.sidebarTitle.textContent = "代码与数据";
    elements.catalogStatus.textContent = needle ? "找到 " + matchedCount + " 个文件" : state.catalog.code.length + " 个可在线查看文件";
    elements.navTree.innerHTML = trees || '<p class="empty-nav">没有匹配的代码或数据。</p>';
  }

  function courseMonogram(book) {
    var labels = {
      "research-skills": "研", python: "Py", "data-analysis": "DA",
      "artificial-intelligence": "AI", robotics: "RB", "wind-energy": "WE",
      "engineering-systems": "EN"
    };
    return labels[book.category] || book.title.slice(0, 2);
  }

  function renderResourceCard(book) {
    var target = "#/resources/" + encodeURIComponent(book.slug);
    return '<article class="book-card"><a class="book-main" href="' + target + '">' +
      '<span class="book-icon" aria-hidden="true">' + escapeHtml(courseMonogram(book)) + '</span>' +
      '<span class="book-copy"><span class="book-tags">' + book.tags.map(escapeHtml).join(" · ") + '</span><strong>' +
      escapeHtml(book.title) + '</strong><span class="book-description">' + escapeHtml(book.description) +
      '</span></span></a><footer><span>' + book.docCount + ' 个章节' +
      (book.codeCount ? ' · ' + book.codeCount + ' 个代码/数据' : '') + '</span><a href="#/resources/' +
      encodeURIComponent(book.slug) + '">课程资源 →</a></footer></article>';
  }

  function renderCategory(category, availableBooks) {
    var books = availableBooks.filter(function (book) { return book.category === category.id; });
    if (!books.length) return "";
    return '<section class="shelf-section category-section" aria-labelledby="category-' + escapeHtml(category.id) + '">' +
      '<div class="section-heading"><div><p class="eyebrow">' + escapeHtml(category.eyebrow || category.id) +
      '</p><h2 id="category-' + escapeHtml(category.id) + '">' + escapeHtml(category.title) + '</h2></div><p>' +
      escapeHtml(category.description || "") + '</p></div><div class="book-grid">' +
      books.map(renderResourceCard).join("") + '</div></section>';
  }

  function renderHomeSidebar(categories, books, query) {
    elements.sidebarTitle.textContent = "知识分类";
    elements.searchLabel.textContent = "搜索课程";
    elements.searchInput.placeholder = "课程、教材或关键词";
    elements.catalogStatus.textContent = query ? "找到 " + books.length + " 套内容" :
      categories.length + " 个分类 · " + state.catalog.stats.books + " 套内容";
    var links = '<a class="home-nav-link is-active" href="#/">' +
      '<span class="home-nav-icon">⌂</span><strong>首页</strong></a>';
    links += categories.map(function (category) {
      var count = books.filter(function (book) { return book.category === category.id; }).length;
      if (query && !count) return "";
      return '<a class="home-nav-link home-category-link" href="#category-' + escapeHtml(category.id) +
        '" data-home-category="' + escapeHtml(category.id) + '"><span class="home-nav-icon">' +
        escapeHtml(category.title.slice(0, 1)) + '</span><strong>' + escapeHtml(category.title) +
        '</strong><small>' + count + '</small></a>';
    }).join("");
    elements.navTree.innerHTML = links;
  }

  function renderLibrary(query) {
    if (typeof query === "undefined") {
      query = "";
      elements.searchInput.value = "";
    }
    hideViews();
    state.activeBook = null;
    state.activeDoc = null;
    state.activeCode = null;
    state.activeResource = false;
    elements.libraryHome.hidden = false;
    document.body.classList.add("home-view");
    var categories = state.catalog.site.categories || [];
    var needle = normalize(query);
    var books = state.catalog.books.filter(function (book) {
      return !needle || normalize([
        book.title, book.author, book.description, (book.tags || []).join(" ")
      ].join(" ")).indexOf(needle) !== -1;
    });
    elements.heroTitle.textContent = state.catalog.site.title;
    elements.heroSubtitle.textContent = state.catalog.site.subtitle;
    elements.homeStats.innerHTML = '<span><strong>' + categories.length + '</strong> 个知识领域</span><span><strong>' +
      state.catalog.stats.books + '</strong> 套课程与教材</span><span><strong>' +
      state.catalog.stats.docs + '</strong> 个章节</span><span><strong>' + state.catalog.stats.code + '</strong> 个代码与数据文件</span>';
    elements.homeCategoryNav.innerHTML = categories.map(function (category) {
      var count = books.filter(function (book) { return book.category === category.id; }).length;
      if (needle && !count) return "";
      return '<a class="home-category-link" href="#category-' + escapeHtml(category.id) +
        '" data-home-category="' + escapeHtml(category.id) + '"><span>' + escapeHtml(category.title) +
        '</span><small>' + count + '</small></a>';
    }).join("");
    elements.categorySections.innerHTML = books.length ? categories.map(function (category) {
      return renderCategory(category, books);
    }).join("") : '<div class="empty-home"><strong>没有找到匹配的课程</strong><p>请尝试课程名称、作者或关键词。</p></div>';
    renderHomeSidebar(categories, books, needle);
    document.title = state.catalog.site.title;
  }

  function inlineCodeItem(file) {
    return '<details class="inline-code" data-code-id="' + file.id + '"><summary><span class="code-kind">' +
      escapeHtml(codeLabel(file)) + '</span><strong>' + escapeHtml(file.name) + '</strong><small>' +
      formatBytes(file.size) + '</small><b>展开代码</b></summary><div class="inline-code-content">展开后加载代码</div>' +
      '<footer><a href="#/code/' + file.id + '">独立查看</a><a href="' + file.downloadUrl + '" download>下载</a></footer></details>';
  }

  async function loadInlineCode(details) {
    if (details.dataset.loaded === "true") return;
    details.dataset.loaded = "true";
    var target = details.querySelector(".inline-code-content");
    target.innerHTML = '<p class="loading-copy">正在加载代码…</p>';
    try {
      var response = await fetch("data/code/" + details.dataset.codeId + ".json", { cache: "no-store" });
      if (!response.ok) throw new Error("代码加载失败");
      var file = await response.json();
      target.innerHTML = file.kind === "notebook" ? renderNotebook(file.cells) :
        sourcePreview(file.content, file.language);
      enhanceCodeBlocks(target);
    } catch (error) {
      target.innerHTML = '<p class="error-copy">' + escapeHtml(error.message) + '</p>';
    }
  }

  function resourceAction(href, label, external) {
    return '<a class="resource-action" href="' + href + '"' + (external ? ' target="_blank" rel="noopener"' : '') + '>' +
      escapeHtml(label) + '</a>';
  }

  function matchLessonResource(resources, chapter) {
    var hit = null;
    (resources || []).forEach(function (resource) {
      if (hit) return;
      var name = resource.name;
      var lessonPattern = new RegExp("lesson[-_ ]?0?" + chapter + "(?:[^0-9]|$)", "i");
      var chapterPattern = new RegExp("chapter[-_ ]?0?" + chapter + "(?:[^0-9]|$)", "i");
      var chinesePattern = new RegExp("第\\s*" + chapter + "\\s*章");
      if (lessonPattern.test(name) || chapterPattern.test(name) || chinesePattern.test(name)) hit = resource;
    });
    return hit;
  }

  function resourceRows(book, docByChapter, docs) {
    if (Array.isArray(book.courseRows) && book.courseRows.length) return book.courseRows;
    var chapters = Object.keys(docByChapter).map(Number).sort(function (a, b) { return a - b; })
      .map(function (chapter) { return { chapter: chapter }; });
    var unnumbered = docs.filter(function (doc) { return doc.chapterNumber == null; })
      .sort(function (a, b) { return a.order - b.order; })
      .map(function (doc) { return { doc: doc }; });
    return chapters.concat(unnumbered);
  }

  function renderResourceTable(book) {
    var docs = state.catalog.docs.filter(function (doc) { return doc.bookSlug === book.slug; });
    var docByChapter = {};
    docs.forEach(function (doc) { if (doc.chapterNumber != null) docByChapter[doc.chapterNumber] = doc; });
    var resources = book.resources || [];
    var rows = resourceRows(book, docByChapter, docs);
    var lessonResources = {};
    rows.forEach(function (row) {
      if (row.lesson || !row.chapter) return;
      var match = matchLessonResource(resources, row.chapter);
      if (match) lessonResources[row.chapter] = match;
    });
    var downloads = resources.filter(function (resource) {
      return Object.keys(lessonResources).every(function (chapter) {
        return lessonResources[chapter].name !== resource.name;
      });
    });
    var bodyRows = rows.map(function (row) {
      var doc = row.doc || docByChapter[row.chapter];
      var chapterTitle = doc ? doc.title.replace(/^第\s*\d+\s*章\s*/, "") : "";
      var topicLabel = row.chapter ? "第 " + row.chapter + " 章 · " + chapterTitle : (doc ? doc.title : "");
      var lessonResource = row.lesson ? null : lessonResources[row.chapter];
      var article = doc ? resourceAction("#/doc/" + doc.id, "正文") : '<span class="resource-empty">—</span>';
      var lesson = '<span class="resource-empty">—</span>';
      if (row.lesson) {
        var explicit = resources.find(function (resource) { return resource.name === row.lesson; });
        if (explicit) lesson = '<a class="resource-action" href="' + explicit.downloadUrl + '" download>课件</a>';
      } else if (lessonResource) {
        lesson = '<a class="resource-action" href="' + lessonResource.downloadUrl + '" download>课件</a>';
      }
      var code = '<span class="resource-empty">—</span>';
      if (doc && (doc.codeFiles || []).length) {
        code = resourceAction("#/code/" + doc.codeFiles[0], "代码");
      }
      var videoUrl = row.video || (doc && doc.video);
      var video = videoUrl ? resourceAction(videoUrl, "视频", true) : '<span class="resource-empty">—</span>';
      return '<tr><td class="resource-topic"><b>' + escapeHtml(topicLabel) + '</b>' +
        (row.desc ? '<small>' + escapeHtml(row.desc) + '</small>' : '') + '</td>' +
        '<td>' + article + '</td><td>' + lesson + '</td><td>' + code + '</td><td>' + video + '</td></tr>';
    }).join("");
    var external = (book.resourceLinks || []).map(function (link) {
      return '<a class="resource-file" href="' + escapeHtml(link.url) + '" target="_blank" rel="noopener"><span>' +
        escapeHtml(link.kind || "链接") + '</span><strong>' + escapeHtml(link.label) +
        '</strong><small>外部资源</small><b>打开</b></a>';
    }).join("");
    var downloadList = downloads.map(function (resource) {
      return '<a class="resource-file" href="' + resource.downloadUrl + '" download><span>' +
        escapeHtml(resource.kind) + '</span><strong>' + escapeHtml(resource.name) + '</strong><small>' +
        escapeHtml(resource.path) + ' · ' + formatBytes(resource.size) + '</small><b>下载</b></a>';
    }).join("");
    var tags = (book.tags || []).map(function (tag) { return '<span>' + escapeHtml(tag) + '</span>'; }).join("");
    var resourceTotal = resources.length + (book.resourceLinks || []).length;
    var info = '<section class="resource-book-info"><p class="resource-book-kicker">TEXTBOOK · SLIDES · CODE · VIDEO</p><h2>' +
      escapeHtml(book.title) + '</h2><p class="resource-book-author">' + escapeHtml(book.author || "编者信息待补充") +
      '</p><p>' + escapeHtml(book.description || "正文、课件、代码与视频按章节对应整理。") +
      '</p><div class="resource-book-meta"><strong>' + (book.chapterCount || docs.length) + ' 章正文</strong><strong>' +
      resourceTotal + ' 项配套资源</strong>' + tags + '</div></section>';
    var table = '<section class="resource-group"><h2>章节资源</h2><p>正文、课件、代码与视频按章节对应整理；空白项表示目前没有可靠资源。</p><div class="resource-table-wrap"><table class="resource-table"><thead><tr><th>主题</th><th>正文</th><th>课件</th><th>代码</th><th>视频</th></tr></thead><tbody>' +
      (bodyRows || '<tr><td colspan="5" class="resource-empty">本书暂无分章资源。</td></tr>') +
      '</tbody></table></div></section>';
    var filesSection = (external || downloadList) ? '<section class="resource-group"><h2>教材与课程</h2><div class="resource-file-list">' +
      external + downloadList + '</div></section>' : '';
    var steps = '<section class="resource-group"><h2>推荐使用顺序</h2><ol class="resource-steps"><li>用课件快速建立本章结构，记下三个关键词。</li>' +
      '<li>阅读正文，补齐定义、公式和边界条件。</li><li>打开对应实现，沿着数据形状、目标函数、参数更新和停止条件阅读。</li>' +
      '<li>最后看视频中仍不清楚的分 P，并用自己的话写一段解释。</li></ol></section>';
    return info + table + filesSection + steps;
  }

  function renderResources(book) {
    hideViews();
    state.activeBook = book;
    state.activeDoc = null;
    state.activeCode = null;
    state.activeResource = true;
    elements.documentView.hidden = false;
    elements.outline.hidden = true;
    elements.outlineToggle.hidden = true;
    elements.relatedCode.hidden = true;
    elements.previousLink.hidden = true;
    elements.nextLink.hidden = true;
    elements.breadcrumb.textContent = book.title;
    elements.docTitle.textContent = "课程资源";
    elements.article.innerHTML = renderResourceTable(book);
    renderSidebar(book, elements.searchInput.value);
    document.title = "课程资源 · " + book.title;
    window.scrollTo(0, 0);
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
    elements.relatedCodeList.innerHTML = files.map(inlineCodeItem).join("");
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
    state.activeResource = false;
    elements.documentView.hidden = false;
    elements.outline.hidden = false;
    elements.outlineToggle.hidden = false;
    elements.article.innerHTML = '<p class="loading-copy">正在打开课程…</p>';
    var response = await fetch("data/docs/" + id + ".json", { cache: "no-store" });
    if (!response.ok) throw new Error("课程内容加载失败");
    var doc = await response.json();
    state.activeDoc = doc;
    state.activeCode = null;
    elements.breadcrumb.textContent = book.title + " / " + (doc.sections.join(" / ") || "课程内容");
    elements.docTitle.textContent = doc.title;
    elements.article.innerHTML = doc.html;
    enhanceCodeBlocks(elements.article);
    renderRelatedCode(doc.codeFiles);
    var outlineHeadings = (doc.headings || []).slice();
    if ((doc.codeFiles || []).length) {
      outlineHeadings.push({ level: 2, id: "relatedCode", text: "本章代码" });
    }
    renderOutline(outlineHeadings);
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
    state.activeResource = false;
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
      return '<section class="notebook-cell"><span class="cell-label">In [' + cell.index +
        ']</span><pre data-language="python"><code>' +
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
    state.activeResource = false;
    elements.codeBreadcrumb.textContent = book.title + " / " + codeLabel(file);
    elements.codeTitle.textContent = file.name;
    elements.codeDownload.href = file.downloadUrl;
    elements.codeMeta.innerHTML = '<span>' + escapeHtml(file.path) + '</span><span>' + formatBytes(file.size) +
      '</span><span>' + escapeHtml(file.language) + '</span>' + (file.truncated ? '<strong>网页仅显示前 256 KB</strong>' : '');
    elements.codeContent.innerHTML = file.kind === "notebook" ? renderNotebook(file.cells) :
      sourcePreview(file.content, file.language);
    enhanceCodeBlocks(elements.codeContent);
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
    var resourceMatch = current.path.match(/^\/resources\/(.+)$/);
    var bookMatch = current.path.match(/^\/book\/(.+)$/);
    if (docMatch) { await renderDocument(docMatch[1], current.params.get("anchor") || ""); return; }
    if (codeMatch) { await renderCode(codeMatch[1]); return; }
    if (resourceMatch) {
      var resourceBook = bookBySlug(decodeURIComponent(resourceMatch[1]));
      if (resourceBook) { renderResources(resourceBook); return; }
    }
    if (current.path === "/code") { renderCodeLibrary(); return; }
    if (bookMatch) {
      var book = bookBySlug(decodeURIComponent(bookMatch[1]));
      if (book) {
        location.replace("#/resources/" + encodeURIComponent(book.slug)); return;
      }
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
      if (!elements.libraryHome.hidden) { renderLibrary(this.value); return; }
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
    document.addEventListener("toggle", function (event) {
      var details = event.target.closest && event.target.closest("details.inline-code");
      if (details && details.open) loadInlineCode(details);
    }, true);
    document.addEventListener("click", function (event) {
      var categoryLink = event.target.closest && event.target.closest(".home-category-link");
      if (categoryLink) {
        event.preventDefault();
        var categoryHeading = document.getElementById("category-" + categoryLink.dataset.homeCategory);
        var category = categoryHeading && categoryHeading.closest(".category-section");
        if (category) category.scrollIntoView({ behavior: "smooth", block: "start" });
        closeSidebar();
        return;
      }
      var button = event.target.closest && event.target.closest(".code-copy-button");
      if (!button) return;
      var code = button.closest(".code-block").querySelector("pre > code");
      if (!code) return;
      copyText(code.textContent).then(function () {
        setCopyState(button, "已复制", "is-copied");
      }).catch(function () {
        setCopyState(button, "复制失败", "is-error");
      });
    });
  }

  function showError(error) {
    console.error(error);
    hideViews();
    elements.documentView.hidden = false;
    elements.docTitle.textContent = "页面暂时无法打开";
    elements.article.innerHTML = '<div class="error-card"><p>' + escapeHtml(error.message) + '</p><a href="#/">返回学习中心</a></div>';
  }

  async function loadAuthStatus() {
    try {
      var response = await fetch("/__auth/status", { cache: "no-store", credentials: "same-origin" });
      if (!response.ok) return;
      var account = await response.json();
      var form = byId("logoutForm");
      form.classList.add("is-active");
      form.title = account.email ? "当前账号：" + account.email : "退出当前账号";
    } catch (_error) {
      // Local static previews and the migration fallback do not expose this endpoint.
    }
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
    document.body.classList.remove("is-loading");
    loadAuthStatus();
    await route();
  }

  initialize().catch(showError);
})();
