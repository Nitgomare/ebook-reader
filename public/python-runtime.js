/**
 * 浏览器内 Python 运行入口（主线程）。
 * 负责：判断文件类型 → 生成运行按钮 → 起 Worker → 把结果写回页面。
 * 真正的计算在 python-worker.js（Pyodide），这里不阻塞渲染。
 */
(function (root) {
  "use strict";

  var DETECT = root.PythonDetect;
  var CONFIG = root.PYTHON_RUNTIME || {};
  var VERSION = CONFIG.version || "314.0.7";
  var MIRRORS = CONFIG.mirrors || [
    "https://gcore.jsdelivr.net/pyodide",
    "https://fastly.jsdelivr.net/pyodide",
    "https://cdn.jsdelivr.net/pyodide",
  ];
  var WORKER_URL = CONFIG.workerUrl || "python-worker.js";

  var session = {
    worker: null,
    state: "idle",          // idle | booting | ready | running | failed
    pythonVersion: "",
    fileId: "",
    pending: new Map(),
    onFatal: null,
  };

  function element(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text != null) node.textContent = text;
    return node;
  }

  function currentFileWidgets() {
    return Array.prototype.slice.call(document.querySelectorAll("[data-py-run]")); 
  }

  function setBusy(scope, busy) {
    scope.querySelectorAll(".py-run-button, .cell-run-button").forEach(function (button) {
      button.disabled = busy;
    });
    scope.querySelectorAll(".py-stop-button").forEach(function (button) {
      button.hidden = !busy;
    });
    scope.querySelectorAll(".py-reset-button").forEach(function (button) {
      button.disabled = busy;
    });
  }

  function describeError(text) {
    if (!text) return "";
    if (/ModuleNotFoundError|ImportError/.test(text)) {
      var name = (text.match(/No module named '([^']+)'/) || [])[1];
      return "浏览器运行时没有 " + (name ? "「" + name + "」" : "这个依赖") +
        "。它需要操作系统、GPU 或真机环境，请在本机 Jupyter 中运行这一段。";
    }
    if (/SyntaxError/.test(text)) return "这一段不是有效的 Python 代码，可能是终端命令、配置文件或其它语言的代码。";
    if (/input\(\)/.test(text)) return "浏览器端不支持 input() 交互输入。";
    return "";
  }

  function workerMessage(event) {
    var message = event.data || {};
    if (message.type === "ready") {
      session.state = "ready";
      session.pythonVersion = message.pythonVersion || "";
      document.querySelectorAll(".py-run-status").forEach(function (status) {
        status.textContent = "Python " + session.pythonVersion + " · 浏览器内运行";
        status.classList.add("is-ready");
      });
      document.querySelectorAll(".py-run-progress").forEach(function (progress) {
        if (progress.classList.contains("is-error")) return;
        progress.textContent = "运行时已就绪";
      });
      return;
    }
    if (message.type === "status") {
      document.querySelectorAll(".py-run-progress").forEach(function (progress) {
        progress.textContent = message.message || "";
      });
      return;
    }
    if (message.type === "fatal") {
      session.state = "failed";
      document.querySelectorAll(".py-run-progress").forEach(function (progress) {
        progress.textContent = message.message || "运行时加载失败";
        progress.classList.add("is-error");
      });
      setBusy(document.body, false);
      return;
    }
    if (message.type === "result") {
      var handler = session.pending.get(message.id);
      if (handler) {
        session.pending.delete(message.id);
        handler(message);
      }
    }
  }

  function terminateWorker() {
    if (session.worker) {
      session.worker.terminate();
      session.worker = null;
    }
    session.state = "idle";
    session.pythonVersion = "";
    session.pending.clear();
  }

  function ensureWorker() {
    if (session.worker && session.state !== "failed") return session.worker;
    terminateWorker();
    var worker = new Worker(WORKER_URL, { type: "module" });
    worker.onmessage = workerMessage;
    worker.onerror = function (event) {
      session.state = "failed";
      document.querySelectorAll(".py-run-progress").forEach(function (progress) {
        progress.textContent = "运行时出错：" + (event.message || "未知错误");
        progress.classList.add("is-error");
      });
      setBusy(document.body, false);
    };
    session.worker = worker;
    session.state = "booting";
    var preferred = "";
    if (CONFIG.indexURL !== false) {
      preferred = new URL(CONFIG.indexURL || "pyodide/", window.location.href).href.replace(/\/+$/, "") + "/";
    }
    worker.postMessage({ type: "init", mirrors: MIRRORS, version: VERSION, preferred: preferred });
    return worker;
  }

  function runCode(code) {
    return new Promise(function (resolve, reject) {
      var worker = ensureWorker();
      var id = "run-" + Date.now() + "-" + Math.random().toString(16).slice(2, 8);
      session.pending.set(id, function (message) {
        session.state = "ready";
        resolve(message);
      });
      var timer = window.setTimeout(function () {
        if (!session.pending.has(id)) return;
        session.pending.delete(id);
        reject(new Error("timeout"));
      }, 10 * 60 * 1000);
      var original = session.pending.get(id);
      session.pending.set(id, function (message) {
        window.clearTimeout(timer);
        original(message);
      });
      session.state = "running";
      worker.postMessage({ type: "run", id: id, code: code });
    });
  }

  function renderResult(target, message) {
    target.textContent = "";
    target.hidden = false;
    var header = element("div", "py-output-header");
    var took = message.durationMs ? " · " + (message.durationMs / 1000).toFixed(2) + " s" : "";
    header.textContent = (message.error ? "运行出错" : "运行结果") + took;
    if (message.error) header.classList.add("is-error");
    target.appendChild(header);
    if (message.warning) {
      var warning = element("p", "py-output-note", message.warning);
      target.appendChild(warning);
    }
    if (message.stdout) {
      var stdout = element("pre", "py-stdout", message.stdout);
      target.appendChild(stdout);
    }
    if (message.stderr) {
      target.appendChild(element("pre", "py-stderr", message.stderr));
    }
    (message.images || []).forEach(function (base64) {
      var figure = new Image();
      figure.className = "py-figure";
      figure.alt = "运行生成的图形";
      figure.src = "data:image/png;base64," + base64;
      target.appendChild(figure);
    });
    if (message.result) {
      target.appendChild(element("pre", "py-expression", message.result));
    }
    if (message.error) {
      var hint = describeError(message.error);
      if (hint) target.appendChild(element("p", "py-output-hint", hint));
      target.appendChild(element("pre", "py-traceback", message.error));
    }
  }

  function mountSourceFile(container, file) {
    var bar = element("div", "py-run-bar");
    bar.setAttribute("data-py-run", "1");
    var run = element("button", "py-run-button", "▶ 在浏览器中运行");
    run.type = "button";
    var stop = element("button", "py-stop-button", "停止");
    stop.type = "button";
    stop.hidden = true;
    var reset = element("button", "py-reset-button", "重启内核");
    reset.type = "button";
    reset.hidden = true;
    var status = element("span", "py-run-status", "首次运行需下载约 12 MB 的 Python 运行时");
    bar.appendChild(run);
    bar.appendChild(stop);
    bar.appendChild(reset);
    bar.appendChild(status);
    container.appendChild(bar);

    var output = element("div", "py-run-output");
    output.hidden = true;
    container.appendChild(output);
    var progress = element("p", "py-run-progress");
    output.appendChild(progress);

    run.addEventListener("click", function () {
      output.textContent = "";
      output.appendChild(progress);
      output.hidden = false;
      progress.classList.remove("is-error");
      progress.textContent = "正在启动 Python 运行时…";
      setBusy(container, true);
      reset.hidden = false;
      runCode(file.content || "").then(function (message) {
        renderResult(output, message);
      }).catch(function (error) {
        progress.textContent = error && error.message === "timeout" ? "运行超过 10 分钟，已放弃" : "运行失败";
        progress.classList.add("is-error");
      }).finally(function () {
        setBusy(container, false);
      });
    });

    stop.addEventListener("click", function () {
      terminateWorker();
      progress.textContent = "已停止，内核已重启（变量已清空）";
      setBusy(container, false);
    });

    reset.addEventListener("click", function () {
      terminateWorker();
      progress.textContent = "内核已重启，变量已清空";
      output.hidden = true;
      status.textContent = "首次运行需下载约 12 MB 的 Python 运行时";
      status.classList.remove("is-ready");
    });
  }

  function mountNotebook(container, file) {
    var cells = file.cells || [];
    var nodes = Array.prototype.slice.call(container.querySelectorAll(".notebook-cell"));
    var pythonCells = [];

    nodes.forEach(function (node, position) {
      var cell = cells[position] || {};
      var source = cell.type === "markdown" ? "" : String(cell.source || "");
      if (cell.type === "markdown") {
        var detected = DETECT.detectUnit(source, "python");
        if (detected.kind === "shell" || detected.kind === "xml" || detected.kind === "yaml") {
          node.setAttribute("data-kind", detected.kind);
        }
        return;
      }
      var target = node.querySelector("pre > code");
      var code = target ? target.textContent : source;
      var kind = DETECT.detectUnit(code, DETECT.detectFileKind(file) === "notebook" ? "notebook" : "python");
      var label = node.querySelector(".cell-label");
      if (label) {
        var badge = element("span", "cell-kind", DETECT.kindLabel(kind.kind));
        badge.setAttribute("data-kind", kind.kind);
        label.appendChild(badge);
      }
      if (!DETECT.isRunnable(kind.kind)) {
        node.classList.add("cell--not-runnable");
        return;
      }
      node.classList.add("cell--runnable");
      var output = element("div", "py-run-output cell-run-output");
      output.hidden = true;
      node.appendChild(output);
      var entry = { node: node, code: code, output: output };
      pythonCells.push(entry);
      if (!label) return;
      var button = element("button", "cell-run-button", "▶ 运行");
      button.type = "button";
      button.addEventListener("click", function () {
        runSingle(entry, button);
      });
      label.appendChild(button);
    });

    if (!pythonCells.length) {
      var note = element("p", "py-run-note", "这个 Notebook 里没有可在浏览器运行的 Python 单元。");
      container.insertBefore(note, container.firstChild);
      return;
    }

    var bar = element("div", "py-run-bar");
    bar.setAttribute("data-py-run", "1");
    var runAll = element("button", "py-run-button", "▶ 运行全部 Python 单元");
    runAll.type = "button";
    var stop = element("button", "py-stop-button", "停止");
    stop.type = "button";
    stop.hidden = true;
    var reset = element("button", "py-reset-button", "重启内核");
    reset.type = "button";
    reset.hidden = true;
    var status = element("span", "py-run-status",
      pythonCells.length + " 个 Python 单元 · 首次运行需下载约 12 MB 运行时");
    bar.appendChild(runAll);
    bar.appendChild(stop);
    bar.appendChild(reset);
    bar.appendChild(status);
    container.insertBefore(bar, container.firstChild);

    var progress = element("p", "py-run-progress");
    container.insertBefore(progress, container.firstChild.nextSibling);

    function runSingle(entry, button) {
      entry.output.textContent = "";
      entry.output.hidden = false;
      var line = element("p", "py-run-progress", "运行中…");
      entry.output.appendChild(line);
      if (button) button.disabled = true;
      return runCode(entry.code).then(function (message) {
        renderResult(entry.output, message);
        return message;
      }).catch(function (error) {
        line.textContent = error && error.message === "timeout" ? "运行超过 10 分钟，已放弃" : "运行失败";
        line.classList.add("is-error");
        return null;
      }).finally(function () {
        if (button) button.disabled = false;
      });
    }

    runAll.addEventListener("click", function () {
      reset.hidden = false;
      setBusy(container, true);
      progress.classList.remove("is-error");
      var index = 0;
      function next() {
        if (index >= pythonCells.length) {
          progress.textContent = "全部 " + pythonCells.length + " 个单元运行完毕";
          setBusy(container, false);
          return;
        }
        var entry = pythonCells[index];
        index += 1;
        progress.textContent = "运行第 " + index + " / " + pythonCells.length + " 个单元…";
        runSingle(entry, entry.node.querySelector(".cell-run-button")).then(next);
      }
      next();
    });

    stop.addEventListener("click", function () {
      terminateWorker();
      progress.textContent = "已停止，内核已重启（变量已清空）";
      setBusy(container, false);
    });

    reset.addEventListener("click", function () {
      terminateWorker();
      progress.textContent = "内核已重启，变量已清空";
      status.textContent = pythonCells.length + " 个 Python 单元 · 首次运行需下载约 12 MB 运行时";
      status.classList.remove("is-ready");
    });
  }

  /**
   * 把运行界面挂到已渲染好的代码内容上。
   * @param {HTMLElement} container 渲染容器
   * @param {object} file 代码文件 JSON（含 kind/name/language/content/cells）
   */
  function mount(container, file) {
    if (!container || !file || !DETECT) return;
    if (container.querySelector("[data-py-mounted]")) return;
    container.setAttribute("data-py-mounted", (file.id || file.name || "") + "");
    var kind = DETECT.detectFileKind(file);
    if (kind === "notebook") {
      mountNotebook(container, file);
      return;
    }
    if (kind === "python") {
      mountSourceFile(container, file);
      return;
    }
    var note = element("p", "py-run-note",
      "此文件是" + DETECT.kindLabel(kind) + "，不能在浏览器里直接执行 Python；可以下载后在本地使用。");
    container.appendChild(note);
  }

  root.PythonPlayground = {
    mount: mount,
    terminate: terminateWorker,
    version: VERSION,
  };
})(typeof globalThis !== "undefined" ? globalThis : this);
