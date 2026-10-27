(function () {
  "use strict";
  var mode = "scroll", active = false, page = 0, count = 1, stride = 1, timer;
  var article, viewport, view, toolbar, controls, previous, next, status, hint, articleObserver;
  var immersive = false, spread = 1, bar, drawer, enter, exit, fullScreenOwned = false;
  var settings = { size: 20, font: "song", theme: "paper", margin: 28 }, menuOpen = false, suppressClickUntil = 0;
  var guide, guideFadeTimer, guideHideTimer;
  var wheelTotal = 0, wheelDirection = 0, wheelLastEvent = 0, wheelLastTurn = 0;
  var fonts = { song: '"Noto Serif SC", "Songti SC", SimSun, serif', hei: '"Microsoft YaHei", "PingFang SC", sans-serif', kai: 'KaiTi, STKaiti, "Kaiti SC", serif' };
  try { if (localStorage.getItem("knowledge-reading-mode") === "pages") mode = "pages"; } catch (_) {}
  try {
    var saved = JSON.parse(localStorage.getItem("knowledge-reader-settings") || "null");
    if (saved) {
      if (Number.isFinite(saved.size)) settings.size = Math.max(14, Math.min(32, saved.size));
      if (Number.isFinite(saved.margin)) settings.margin = Math.max(8, Math.min(60, saved.margin));
      if (fonts[saved.font]) settings.font = saved.font;
      if (["paper", "white", "green", "dark"].indexOf(saved.theme) !== -1) settings.theme = saved.theme;
    }
  } catch (_) {}

  function paged() { return active && mode === "pages"; }
  function visibleNode() {
    var bounds = paged() ? viewport.getBoundingClientRect() : { left: 0, right: innerWidth, top: 80, bottom: innerHeight };
    var nodes = article.querySelectorAll("h1,h2,h3,h4,p,li,pre,figure,table,img");
    for (var i = 0; i < nodes.length; i++) {
      var rects = nodes[i].getClientRects();
      for (var j = 0; j < rects.length; j++) {
        var r = rects[j];
        if (r.bottom > bounds.top && r.top < bounds.bottom && r.right > bounds.left && r.left < bounds.right) return nodes[i];
      }
    }
    return null;
  }
  function showPage(value) {
    page = Math.floor(Math.max(0, Math.min(count - 1, value)) / spread) * spread;
    viewport.scrollLeft = page * stride;
    viewport.scrollTop = 0;
    status.textContent = "第 " + (page + 1) + (spread === 2 && page + 1 < count ? "–" + Math.min(page + spread, count) : "") + " / " + count + " 页";
    previous.disabled = page === 0;
    next.disabled = page + spread >= count;
  }
  function targetPage(target) {
    return Math.floor((target.getBoundingClientRect().left - article.getBoundingClientRect().left + 1) / stride);
  }
  function fitMath() {
    var gap = paged() ? parseFloat(getComputedStyle(article).columnGap) : 0;
    var width = paged() ? (article.clientWidth - gap * (spread - 1)) / spread : article.clientWidth;
    if (width <= 0) return;
    article.querySelectorAll(".arithmatex mjx-container").forEach(function (container) {
      var math = container.querySelector("mjx-math");
      if (!math) return;
      var scale = Number(container.dataset.readerMathScale || 1);
      var naturalWidth = math.getBoundingClientRect().width / scale;
      var parent = container.closest("td,th,li,blockquote");
      var available = parent ? Math.min(width, parent.clientWidth) : width;
      var nextScale = naturalWidth > available ? Math.max(.05, (available - 4) / naturalWidth) : 1;
      if (Math.abs(nextScale - scale) < .005) return;
      if (!container.dataset.readerMathBaseSize) container.dataset.readerMathBaseSize = container.style.fontSize || getComputedStyle(container).fontSize;
      var base = container.dataset.readerMathBaseSize;
      var unit = base.replace(/[\d.\s]/g, "");
      container.style.fontSize = (parseFloat(base) * nextScale) + unit;
      container.dataset.readerMathScale = String(nextScale);
    });
    // Scaling writes inline styles. Do not feed those writes back into scaling.
    if (articleObserver) articleObserver.takeRecords();
  }
  function layout(target) {
    if (!paged()) return;
    // Keep one complete paper page and its controls within a normal screen.
    var paperStyle = getComputedStyle(viewport);
    var paperEdges = parseFloat(paperStyle.paddingTop) + parseFloat(paperStyle.paddingBottom) +
      parseFloat(paperStyle.borderTopWidth) + parseFloat(paperStyle.borderBottomWidth);
    var topbar = document.querySelector(".topbar").offsetHeight;
    var height = immersive ? Math.max(120, view.clientHeight - paperEdges) :
      Math.max(220, innerHeight - topbar - toolbar.offsetHeight - paperEdges - controls.offsetHeight - 64);
    viewport.style.setProperty("--page-height", height + "px");
    spread = immersive ? 2 : 1;
    var gap = parseFloat(getComputedStyle(article).columnGap);
    stride = (article.clientWidth + gap) / spread;
    fitMath();
    count = Math.max(1, Math.ceil((article.scrollWidth + gap) / stride));
    // An odd final page leaves the right-hand leaf empty.
    if (immersive) {
      var end = 0, origin = article.getBoundingClientRect().left;
      Array.prototype.forEach.call(article.children, function (node) {
        var rects = node.getClientRects();
        for (var i = 0; i < rects.length; i++) end = Math.max(end, rects[i].right - origin);
      });
      count = Math.max(1, Math.ceil((end + gap - 1) / stride));
    }
    var endMarker = document.getElementById("readingEnd");
    endMarker.hidden = !immersive;
    if (immersive) endMarker.style.left = (Math.ceil(count / 2) * 2 * stride - gap + parseFloat(paperStyle.paddingLeft) + parseFloat(paperStyle.paddingRight) - 1) + "px";
    showPage(target && article.contains(target) ? targetPage(target) : page);
  }
  function scheduleLayout() {
    if (!paged()) { if (active) fitMath(); return; }
    var target = visibleNode();
    clearTimeout(timer);
    timer = setTimeout(function () { layout(target); }, 80);
  }
  function goTo(target, smooth) {
    if (!target) return;
    if (paged() && article.contains(target)) {
      layout();
      showPage(targetPage(target));
      if (!immersive) toolbar.scrollIntoView({ block: "start", behavior: smooth ? "smooth" : "instant" });
    } else target.scrollIntoView({ block: "start", behavior: smooth ? "smooth" : "instant" });
  }
  function apply(target) {
    view.classList.toggle("is-paged", paged());
    controls.hidden = !paged();
    hint.hidden = !paged();
    toolbar.querySelectorAll("[data-reading-mode]").forEach(function (button) {
      button.setAttribute("aria-pressed", String(button.dataset.readingMode === mode));
    });
    viewport.scrollLeft = 0;
    if (paged()) {
      layout(target);
      if (!immersive) toolbar.scrollIntoView({ block: "start", behavior: "instant" });
    } else {
      viewport.style.removeProperty("--page-height");
      fitMath();
      if (target) goTo(target);
    }
  }
  function closeContents() {
    drawer.hidden = true;
    document.getElementById("immersiveContents").setAttribute("aria-expanded", "false");
  }
  function setMenu(value) {
    if (value) hideGuide();
    menuOpen = immersive && value;
    bar.hidden = !menuOpen;
    view.classList.toggle("reading-menu-open", menuOpen);
    if (menuOpen) document.getElementById("closeReadingMenu").focus({ preventScroll: true });
    else if (immersive) view.focus({ preventScroll: true });
  }
  function resetWheel() {
    wheelTotal = 0; wheelDirection = 0; wheelLastEvent = 0; wheelLastTurn = 0;
  }
  function hideGuide() {
    clearTimeout(guideFadeTimer); clearTimeout(guideHideTimer);
    guide.hidden = true;
    guide.classList.remove("is-fading");
  }
  function showGuide() {
    hideGuide();
    guide.hidden = false;
    guideFadeTimer = setTimeout(function () { guide.classList.add("is-fading"); }, 4000);
    guideHideTimer = setTimeout(hideGuide, 4700);
  }
  function updateSettings(save) {
    var target = visibleNode();
    view.style.setProperty("--reader-font-size", settings.size + "px");
    view.style.setProperty("--reader-font-family", fonts[settings.font]);
    view.style.setProperty("--reader-margin", settings.margin + "px");
    view.dataset.readerTheme = settings.theme;
    document.getElementById("readerFontSize").value = settings.size;
    document.getElementById("readerFontSizeValue").textContent = settings.size + " px";
    document.getElementById("readerFontFamily").value = settings.font;
    document.getElementById("readerPageMargin").value = settings.margin;
    document.getElementById("readerPageMarginValue").textContent = settings.margin + " px";
    bar.querySelectorAll("[data-reader-theme]").forEach(function (button) {
      button.setAttribute("aria-pressed", String(button.dataset.readerTheme === settings.theme));
    });
    if (save) { try { localStorage.setItem("knowledge-reader-settings", JSON.stringify(settings)); } catch (_) {} }
    if (immersive) layout(target);
  }
  function setImmersive(value) {
    var target = visibleNode();
    immersive = value;
    view.classList.toggle("is-immersive", value);
    document.body.classList.toggle("immersive-reading", value);
    setMenu(false);
    closeContents();
    resetWheel();
    hideGuide();
    if (value) {
      mode = "pages";
      document.getElementById("immersiveTitle").textContent = document.getElementById("docTitle").textContent;
      document.getElementById("immersiveOutlineNav").innerHTML = document.getElementById("outlineNav").innerHTML;
      apply(target);
      view.focus({ preventScroll: true });
      showGuide();
    } else {
      apply(target);
      enter.focus({ preventScroll: true });
    }
  }
  function leaveImmersive() {
    if (!immersive) return;
    setImmersive(false);
    if (fullScreenOwned && document.fullscreenElement) document.exitFullscreen().catch(function () {});
    fullScreenOwned = false;
  }
  function init() {
    article = document.getElementById("article");
    viewport = document.getElementById("readingViewport");
    view = document.getElementById("documentView");
    toolbar = document.getElementById("readingToolbar");
    controls = document.getElementById("pageControls");
    previous = document.getElementById("bookPreviousPage");
    next = document.getElementById("bookNextPage");
    status = document.getElementById("bookPageStatus");
    hint = document.getElementById("readingHint");
    bar = document.getElementById("immersiveBar");
    drawer = document.getElementById("immersiveOutline");
    enter = document.getElementById("enterImmersive");
    exit = document.getElementById("exitImmersive");
    guide = document.getElementById("readingGuide");
    view.tabIndex = -1;
    updateSettings(false);
    document.getElementById("closeReadingMenu").addEventListener("click", function () { setMenu(false); });
    document.getElementById("readerFontSize").addEventListener("input", function () { settings.size = Number(this.value); updateSettings(true); });
    document.getElementById("readerFontFamily").addEventListener("change", function () { settings.font = this.value; updateSettings(true); });
    document.getElementById("readerPageMargin").addEventListener("input", function () { settings.margin = Number(this.value); updateSettings(true); });
    bar.addEventListener("click", function (event) {
      var button = event.target.closest("[data-reader-theme]");
      if (button) { settings.theme = button.dataset.readerTheme; updateSettings(true); }
    });
    var pointerStart;
    viewport.addEventListener("pointerdown", function (event) { pointerStart = { x: event.clientX, y: event.clientY }; });
    viewport.addEventListener("wheel", function (event) {
      if (!paged() || event.ctrlKey || event.metaKey || event.shiftKey ||
          (immersive && (menuOpen || !drawer.hidden)) ||
          event.target.closest('.interactive-figure-pane[data-figure-pane="interactive"],iframe,video,input,textarea,select,[contenteditable]')) {
        resetWheel(); return;
      }
      var vertical = Math.abs(event.deltaY) >= Math.abs(event.deltaX);
      var delta = vertical ? event.deltaY : event.deltaX;
      if (!delta) return;
      // Let nested content scroll while it has room in the requested direction.
      for (var node = event.target; node && node !== viewport; node = node.parentElement) {
        var style = getComputedStyle(node);
        var overflow = vertical ? style.overflowY : style.overflowX;
        var position = vertical ? node.scrollTop : node.scrollLeft;
        var limit = vertical ? node.scrollHeight - node.clientHeight : node.scrollWidth - node.clientWidth;
        if (/(auto|scroll)/.test(overflow) && limit > 1 && (delta > 0 ? position < limit - 1 : position > 1)) {
          resetWheel(); return;
        }
      }
      event.preventDefault();
      var direction = delta > 0 ? 1 : -1, now = Date.now();
      if (now - wheelLastEvent > 220 || direction !== wheelDirection) resetWheel();
      wheelLastEvent = now; wheelDirection = direction;
      // A brief cooldown stops accidental rapid flips without locking a long gesture.
      if (wheelLastTurn && now - wheelLastTurn < 320) return;
      wheelTotal += Math.abs(delta) * (event.deltaMode === 1 ? 24 : event.deltaMode === 2 ? viewport.clientHeight : 1);
      if (wheelTotal >= 40) {
        showPage(page + direction * spread);
        wheelLastTurn = now; wheelTotal = 0;
      }
    }, { passive: false });
    viewport.addEventListener("click", function (event) {
      if (!immersive || event.defaultPrevented || Date.now() < suppressClickUntil ||
          event.target.closest("a,button,input,select,textarea,pre,table,iframe,video,.interactive-figure,[contenteditable]") || String(window.getSelection())) return;
      if (pointerStart && Math.hypot(event.clientX - pointerStart.x, event.clientY - pointerStart.y) > 12) return;
      if (menuOpen || !drawer.hidden) { closeContents(); setMenu(false); return; }
      var bounds = viewport.getBoundingClientRect(), x = (event.clientX - bounds.left) / bounds.width;
      if (x < .33) showPage(page - spread);
      else if (x > .67) showPage(page + spread);
      else setMenu(true);
    });
    enter.addEventListener("click", function () {
      setImmersive(true);
      // The overlay also works in browsers that cannot enter native fullscreen.
      if (view.requestFullscreen && !document.fullscreenElement) {
        fullScreenOwned = true;
        view.requestFullscreen().then(scheduleLayout).catch(function () { fullScreenOwned = false; });
      }
    });
    exit.addEventListener("click", leaveImmersive);
    document.addEventListener("fullscreenchange", function () {
      if (fullScreenOwned && !document.fullscreenElement) { fullScreenOwned = false; leaveImmersive(); }
      scheduleLayout();
    });
    document.getElementById("immersiveContents").addEventListener("click", function () {
      setMenu(false);
      drawer.hidden = !drawer.hidden;
      this.setAttribute("aria-expanded", String(!drawer.hidden));
      if (!drawer.hidden) document.getElementById("closeImmersiveContents").focus();
    });
    document.getElementById("closeImmersiveContents").addEventListener("click", function () {
      closeContents(); setMenu(true);
    });
    drawer.addEventListener("click", function (event) {
      var link = event.target.closest("a");
      if (!link) return;
      event.preventDefault();
      var target = document.getElementById(decodeURIComponent(link.hash.slice(1)));
      if (target && !article.contains(target)) { leaveImmersive(); }
      goTo(target); closeContents();
      if (immersive) view.focus({ preventScroll: true });
    });
    toolbar.addEventListener("click", function (event) {
      var button = event.target.closest("[data-reading-mode]");
      if (!button || button.dataset.readingMode === mode) return;
      var target = visibleNode();
      mode = button.dataset.readingMode;
      try { localStorage.setItem("knowledge-reading-mode", mode); } catch (_) {}
      apply(target);
    });
    previous.addEventListener("click", function () { showPage(page - spread); });
    next.addEventListener("click", function () { showPage(page + spread); });
    document.addEventListener("keydown", function (event) {
      if (immersive && menuOpen && event.key === "Tab") {
        var focusable = Array.prototype.slice.call(bar.querySelectorAll("button,input,select")).concat([previous, next]).filter(function (node) { return !node.disabled; });
        var index = focusable.indexOf(event.target);
        event.preventDefault();
        focusable[(index + (event.shiftKey ? -1 : 1) + focusable.length) % focusable.length].focus();
        return;
      }
      if (immersive && !event.ctrlKey && !event.altKey && !event.metaKey && event.key.toLowerCase() === "m" && !event.target.closest("input,select,textarea,[contenteditable]")) {
        event.preventDefault(); closeContents(); setMenu(!menuOpen); return;
      }
      if (event.key === "Escape" && immersive) {
        event.preventDefault();
        if (!drawer.hidden) { closeContents(); setMenu(true); }
        else if (menuOpen) setMenu(false);
        else leaveImmersive();
        return;
      }
      if (!paged() || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey ||
          event.target.closest("input,textarea,select,a,[contenteditable],pre,iframe,[role='slider']") ||
          (event.target.closest("button") && !event.target.closest(".page-controls,.immersive-bar,.reading-toolbar")) ||
          (immersive && !drawer.hidden) ||
          (immersive && menuOpen) ||
          document.body.classList.contains("nav-open") || document.querySelector(".outline.is-open")) return;
      if (event.key === "ArrowRight" || event.key === "ArrowLeft") {
        event.preventDefault(); showPage(page + (event.key === "ArrowRight" ? spread : -spread));
      }
    });
    var touch;
    viewport.addEventListener("touchstart", function (event) {
      touch = null;
      if (!paged() || (immersive && (menuOpen || !drawer.hidden)) || event.touches.length !== 1 || event.target.closest("pre,table,iframe,button,a,input,textarea,select,.interactive-figure")) return;
      touch = { x: event.touches[0].clientX, y: event.touches[0].clientY };
    }, { passive: true });
    viewport.addEventListener("touchend", function (event) {
      if (!touch || !paged() || !event.changedTouches.length) return;
      var dx = event.changedTouches[0].clientX - touch.x, dy = event.changedTouches[0].clientY - touch.y;
      if (Math.abs(dx) > 55 && Math.abs(dx) > Math.abs(dy) * 1.5 && !String(window.getSelection())) {
        showPage(page + (dx < 0 ? spread : -spread)); suppressClickUntil = Date.now() + 500;
      }
      touch = null;
    }, { passive: true });
    viewport.addEventListener("touchcancel", function () { touch = null; }, { passive: true });
    article.addEventListener("load", scheduleLayout, true);
    article.addEventListener("focusin", function (event) { if (paged()) showPage(targetPage(event.target)); });
    article.addEventListener("click", function (event) {
      var link = event.target.closest("a[href^='#']");
      if (!link || link.hash.indexOf("#/") === 0) return;
      var target;
      try { target = document.getElementById(decodeURIComponent(link.hash.slice(1))); } catch (_) { return; }
      if (target) { event.preventDefault(); goTo(target, true); }
    });
    window.addEventListener("resize", scheduleLayout);
    new ResizeObserver(scheduleLayout).observe(viewport);
    articleObserver = new MutationObserver(scheduleLayout);
    articleObserver.observe(article, { childList: true, subtree: true, attributes: true, attributeFilter: ["style", "hidden", "open"] });
    if (document.fonts) document.fonts.ready.then(scheduleLayout);
  }
  window.ReaderMode = {
    init: init,
    reset: function () {
      hideGuide(); resetWheel();
      if (immersive) leaveImmersive();
      active = false; clearTimeout(timer); page = 0;
      view.classList.remove("is-paged"); toolbar.hidden = true; controls.hidden = true;
      document.getElementById("readingEnd").hidden = true;
      viewport.scrollLeft = 0; viewport.style.removeProperty("--page-height");
    },
    activate: function () { active = true; toolbar.hidden = false; apply(); },
    reflow: scheduleLayout,
    goTo: goTo
  };
})();
