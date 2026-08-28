(function () {
  "use strict";

  var CHAPTERS = {
    "3": { title: "第 3 章 · NumPy 数组计算", file: "chapter03_numpy_tutorial.py" },
    "4": { title: "第 4 章 · Pandas 基础", file: "chapter04_pandas_basics_tutorial.py" },
    "5": { title: "第 5 章 · 数据读取与写入", file: "chapter05_pandas_io_tutorial.py" },
    "6": { title: "第 6 章 · 数据处理", file: "chapter06_pandas_processing_tutorial.py" },
    "7": { title: "第 7 章 · 数据清洗", file: "chapter07_pandas_cleaning_tutorial.py" }
  };

  var SPECIAL_LABELS = {
    learning_guide: "学习导航",
    final_self_check: "学习成果自检",
    exercises: "章末练习与自动检查",
    main: "脚本总入口"
  };

  function role(root, name) {
    return root.querySelector('[data-role="' + name + '"]');
  }

  function action(root, name) {
    return root.querySelector('[data-action="' + name + '"]');
  }

  function firstDocstringLine(lines, start, end) {
    for (var index = start + 1; index < Math.min(end, start + 8); index += 1) {
      var text = lines[index].trim();
      var match = text.match(/^(?:"""|''')(.*?)(?:"""|''')?$/);
      if (match && match[1]) return match[1].replace(/(?:"""|''')$/, "").trim();
    }
    return "";
  }

  function parseSections(source) {
    var lines = source.replace(/\r\n?/g, "\n").split("\n");
    var definitions = [];
    var outline = [];

    lines.forEach(function (line, index) {
      var definition = line.match(/^def\s+([A-Za-z_]\w*)\s*\(/);
      var marker = line.match(/^\s*#\s*\[((?:[3-7]\.)\d+(?:\.\d+)?)\]\s+(.+?)\s*$/);
      if (definition) definitions.push({ name: definition[1], start: index });
      if (marker) outline.push({ id: marker[1], title: marker[2], start: index });
    });

    var sections = [{ id: "all", label: "完整脚本", group: "base", start: 0, end: lines.length }];
    if (definitions.length && definitions[0].start > 0) {
      sections.push({
        id: "overview",
        label: "模块说明、学习目标与配置",
        group: "base",
        start: 0,
        end: definitions[0].start
      });
    }

    outline.forEach(function (marker, index) {
      var nextMarker = index + 1 < outline.length ? outline[index + 1].start : lines.length;
      var nextDefinition = definitions.find(function (definition) {
        return definition.start > marker.start;
      });
      sections.push({
        id: marker.id,
        label: marker.id + " · " + marker.title,
        group: "outline",
        start: marker.start,
        end: Math.min(nextMarker, nextDefinition ? nextDefinition.start : lines.length)
      });
    });

    definitions.forEach(function (definition, index) {
      if (outline.length && definition.name.indexOf("section_") === 0) return;
      var end = index + 1 < definitions.length ? definitions[index + 1].start : lines.length;
      var docstring = firstDocstringLine(lines, definition.start, end);
      var friendly = SPECIAL_LABELS[definition.name] || docstring || definition.name;
      sections.push({
        id: definition.name,
        label: friendly + " · " + definition.name + "()",
        group: "utility",
        start: definition.start,
        end: end
      });
    });

    return { lines: lines, sections: sections };
  }

  function appendHighlightedText(target, text, query) {
    if (!query) {
      target.textContent = text;
      return 0;
    }

    var lowerText = text.toLocaleLowerCase();
    var lowerQuery = query.toLocaleLowerCase();
    var cursor = 0;
    var count = 0;
    var position = lowerText.indexOf(lowerQuery, cursor);

    while (position !== -1) {
      target.appendChild(document.createTextNode(text.slice(cursor, position)));
      var mark = document.createElement("mark");
      mark.textContent = text.slice(position, position + query.length);
      target.appendChild(mark);
      cursor = position + query.length;
      count += 1;
      position = lowerText.indexOf(lowerQuery, cursor);
    }

    target.appendChild(document.createTextNode(text.slice(cursor)));
    return count;
  }

  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(text);

    return new Promise(function (resolve, reject) {
      var area = document.createElement("textarea");
      area.value = text;
      area.setAttribute("readonly", "");
      area.style.position = "fixed";
      area.style.opacity = "0";
      document.body.appendChild(area);
      area.select();
      try {
        document.execCommand("copy");
        resolve();
      } catch (error) {
        reject(error);
      } finally {
        area.remove();
      }
    });
  }

  function CodeExplorer(root) {
    this.root = root;
    this.chapterSelect = role(root, "chapter");
    this.sectionSelect = role(root, "section");
    this.searchInput = role(root, "search");
    this.wrapInput = role(root, "wrap");
    this.status = role(root, "status");
    this.range = role(root, "range");
    this.matchCount = role(root, "match-count");
    this.viewport = role(root, "viewport");
    this.linesElement = role(root, "lines");
    this.downloadLink = role(root, "download");
    this.rawLink = role(root, "raw");
    this.previousButton = action(root, "previous-match");
    this.nextButton = action(root, "next-match");
    this.copyButton = action(root, "copy");
    this.source = "";
    this.lines = [];
    this.sections = [];
    this.matchLines = [];
    this.activeMatch = -1;
    this.matchSummary = "未搜索";
    this.loadToken = 0;
    this.restoreStatusTimer = null;
    this.bind();
    this.populateChapters();

    var params = new URLSearchParams(window.location.search);
    var chapter = CHAPTERS[params.get("chapter")] ? params.get("chapter") : "3";
    this.chapterSelect.value = chapter;
    this.loadChapter(chapter, params.get("section"));
  }

  CodeExplorer.prototype.bind = function () {
    var self = this;

    this.chapterSelect.addEventListener("change", function () {
      self.searchInput.value = "";
      self.loadChapter(self.chapterSelect.value, null);
    });
    this.sectionSelect.addEventListener("change", function () {
      self.render();
      self.updateUrl();
    });
    this.searchInput.addEventListener("input", function () {
      self.render();
    });
    this.wrapInput.addEventListener("change", function () {
      self.root.classList.toggle("is-wrapped", self.wrapInput.checked);
      try { localStorage.setItem("python-code-lab:wrap", self.wrapInput.checked ? "1" : "0"); } catch (_) {}
    });
    this.copyButton.addEventListener("click", function () {
      var section = self.currentSection();
      var text = self.lines.slice(section.start, section.end).join("\n");
      copyText(text).then(function () {
        self.flashStatus("已复制当前片段（" + (section.end - section.start) + " 行）");
      }).catch(function () {
        self.flashStatus("复制失败，请使用浏览器的复制命令");
      });
    });
    this.previousButton.addEventListener("click", function () { self.moveMatch(-1); });
    this.nextButton.addEventListener("click", function () { self.moveMatch(1); });
    this.root.addEventListener("keydown", function (event) {
      var typing = /INPUT|SELECT|TEXTAREA/.test(event.target.tagName);
      if (event.key === "/" && !typing) {
        event.preventDefault();
        self.searchInput.focus();
      } else if (event.altKey && event.key === "ArrowDown") {
        event.preventDefault();
        self.moveMatch(1);
      } else if (event.altKey && event.key === "ArrowUp") {
        event.preventDefault();
        self.moveMatch(-1);
      }
    });

    try {
      this.wrapInput.checked = localStorage.getItem("python-code-lab:wrap") === "1";
      this.root.classList.toggle("is-wrapped", this.wrapInput.checked);
    } catch (_) {}
  };

  CodeExplorer.prototype.populateChapters = function () {
    var select = this.chapterSelect;
    Object.keys(CHAPTERS).forEach(function (number) {
      var option = document.createElement("option");
      option.value = number;
      option.textContent = CHAPTERS[number].title;
      select.appendChild(option);
    });
  };

  CodeExplorer.prototype.loadChapter = function (chapter, requestedSection) {
    var self = this;
    var config = CHAPTERS[chapter];
    var token = ++this.loadToken;
    var url = new URL(this.root.dataset.codeBase + config.file, window.location.href);

    this.status.textContent = "正在加载 " + config.title + "……";
    this.root.classList.add("is-loading");
    this.sectionSelect.disabled = true;
    this.copyButton.disabled = true;

    fetch(url, { credentials: "same-origin" }).then(function (response) {
      if (!response.ok) throw new Error("HTTP " + response.status);
      return response.text();
    }).then(function (source) {
      if (token !== self.loadToken) return;
      var parsed = parseSections(source);
      self.source = source;
      self.lines = parsed.lines;
      self.sections = parsed.sections;
      self.populateSections(requestedSection);
      self.downloadLink.href = url.href;
      self.downloadLink.setAttribute("download", config.file);
      self.rawLink.href = url.href;
      self.status.textContent = config.title + " · 已加载 " + self.lines.length + " 行";
      self.sectionSelect.disabled = false;
      self.copyButton.disabled = false;
      self.root.classList.remove("is-loading", "has-error");
      self.render();
      self.updateUrl();
    }).catch(function (error) {
      if (token !== self.loadToken) return;
      self.root.classList.remove("is-loading");
      self.root.classList.add("has-error");
      self.status.textContent = "代码加载失败：" + error.message;
      self.linesElement.replaceChildren();
    });
  };

  CodeExplorer.prototype.populateSections = function (requestedSection) {
    var select = this.sectionSelect;
    var groups = {};
    select.replaceChildren();
    this.sections.forEach(function (section) {
      var option = document.createElement("option");
      option.value = section.id;
      option.textContent = section.label;
      if (section.group === "outline" || section.group === "utility") {
        if (!groups[section.group]) {
          groups[section.group] = document.createElement("optgroup");
          groups[section.group].label = section.group === "outline"
            ? "教材大纲（精确到三级）"
            : "学习与工具函数";
          select.appendChild(groups[section.group]);
        }
        groups[section.group].appendChild(option);
      } else {
        select.insertBefore(option, select.firstChild ? select.firstChild.nextSibling : null);
      }
    });
    select.value = this.sections.some(function (section) {
      return section.id === requestedSection;
    }) ? requestedSection : "all";
  };

  CodeExplorer.prototype.currentSection = function () {
    var selected = this.sectionSelect.value || "all";
    return this.sections.find(function (section) { return section.id === selected; }) || this.sections[0];
  };

  CodeExplorer.prototype.render = function () {
    if (!this.lines.length || !this.sections.length) return;
    var self = this;
    var section = this.currentSection();
    var query = this.searchInput.value.trim();
    var fragment = document.createDocumentFragment();
    var matchedOccurrences = 0;
    this.matchLines = [];
    this.activeMatch = -1;
    this.linesElement.start = section.start + 1;

    for (var index = section.start; index < section.end; index += 1) {
      var item = document.createElement("li");
      var code = document.createElement("code");
      var count = appendHighlightedText(code, this.lines[index], query);
      if (count) {
        item.classList.add("has-match");
        this.matchLines.push(item);
        matchedOccurrences += count;
      }
      item.value = index + 1;
      item.appendChild(code);
      fragment.appendChild(item);
    }

    this.linesElement.replaceChildren(fragment);
    this.range.textContent = "显示第 " + (section.start + 1) + "–" + section.end + " 行";
    this.matchSummary = query
      ? this.matchLines.length + " 行 / " + matchedOccurrences + " 处匹配"
      : "未搜索";
    this.matchCount.textContent = this.matchSummary;
    this.previousButton.disabled = !this.matchLines.length;
    this.nextButton.disabled = !this.matchLines.length;

    if (query && this.matchLines.length) {
      window.requestAnimationFrame(function () { self.activateMatch(0); });
    }
  };

  CodeExplorer.prototype.activateMatch = function (index) {
    if (!this.matchLines.length) return;
    if (this.activeMatch >= 0) this.matchLines[this.activeMatch].classList.remove("is-active-match");
    this.activeMatch = (index + this.matchLines.length) % this.matchLines.length;
    var item = this.matchLines[this.activeMatch];
    item.classList.add("is-active-match");
    item.scrollIntoView({ block: "center", behavior: "smooth" });
    this.matchCount.textContent = this.matchSummary + " · 当前第 " + (this.activeMatch + 1) + " 行";
  };

  CodeExplorer.prototype.moveMatch = function (direction) {
    if (!this.matchLines.length) return;
    this.activateMatch(this.activeMatch + direction);
  };

  CodeExplorer.prototype.updateUrl = function () {
    var url = new URL(window.location.href);
    url.searchParams.set("chapter", this.chapterSelect.value);
    if (this.sectionSelect.value && this.sectionSelect.value !== "all") {
      url.searchParams.set("section", this.sectionSelect.value);
    } else {
      url.searchParams.delete("section");
    }
    window.history.replaceState({}, "", url);
  };

  CodeExplorer.prototype.flashStatus = function (message) {
    var self = this;
    var original = this.status.textContent;
    window.clearTimeout(this.restoreStatusTimer);
    this.status.textContent = message;
    this.restoreStatusTimer = window.setTimeout(function () {
      self.status.textContent = original;
    }, 2200);
  };

  function initCodeExplorer() {
    var root = document.querySelector("[data-code-explorer]");
    if (!root || root.dataset.codeExplorerReady) return;
    root.dataset.codeExplorerReady = "true";
    new CodeExplorer(root);
  }

  if (typeof document$ !== "undefined") document$.subscribe(initCodeExplorer);
  document.addEventListener("DOMContentLoaded", initCodeExplorer);
})();
