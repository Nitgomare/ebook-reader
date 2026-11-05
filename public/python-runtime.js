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
    if (message.type === "result" || message.type === "analysis") {
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

  function runCode(code, inputs) {
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
      worker.postMessage({ type: "run", id: id, code: code, inputs: inputs || [] });
    });
  }

  var INPUT_CALL = /(^|[^.\w$])input\s*\(/g;

  /** 找出代码里需要输入的位置，以及 input() 里写死的提示语。 */
  function inputPlan(code) {
    var text = String(code || "");
    var prompts = [];
    var match;
    INPUT_CALL.lastIndex = 0;
    while ((match = INPUT_CALL.exec(text))) {
      var rest = text.slice(match.index + match[0].length);
      var literal = /^\s*(['"])((?:\\.|(?!\1).){0,160})\1/.exec(rest);
      prompts.push(literal ? literal[2] : "");
    }
    return { count: prompts.length, prompts: prompts };
  }

  /** 运行前收集输入值：浏览器的 Promise 里没有终端，只能先填好。 */
  function collectInputs(target, plan, title) {
    return new Promise(function (resolve) {
      var panel = element("div", "py-input-panel");
      panel.appendChild(element("div", "py-input-title", title + "（" + plan.count + " 个值）"));
      panel.appendChild(element("p", "py-input-note",
        "浏览器里没有终端可以当场读入，先在下面填好，再点运行。留空表示输入空字符串。"));
      var fields = [];
      for (var index = 0; index < plan.count; index += 1) {
        var row = element("label", "py-input-row");
        row.appendChild(element("span", "py-input-label", plan.prompts[index] || ("输入 " + (index + 1))));
        var box = element("input", "py-input-field");
        box.type = "text";
        row.appendChild(box);
        panel.appendChild(row);
        fields.push(box);
      }
      var submit = element("button", "py-run-button py-input-submit", "▶ 填入并运行");
      submit.type = "button";
      submit.addEventListener("click", function () {
        var values = fields.map(function (box) { return box.value; });
        panel.remove();
        resolve(values);
      });
      panel.appendChild(submit);
      target.appendChild(panel);
      panel.scrollIntoView({ block: "nearest" });
      if (fields[0]) fields[0].focus();
    });
  }

  function analyzeSources(sources) {
    return new Promise(function (resolve, reject) {
      var worker = ensureWorker();
      var id = "check-" + Date.now() + "-" + Math.random().toString(16).slice(2, 8);
      session.pending.set(id, function (message) {
        session.state = "ready";
        if (message.error) {
          reject(new Error(message.error));
          return;
        }
        resolve(message.results || []);
      });
      worker.postMessage({ type: "analyze", id: id, sources: sources });
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
    var status = element("span", "py-run-status", "首次运行需下载约 14 MB 的 Python 运行时");
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
      var source = file.content || "";
      var plan = inputPlan(source);
      var prepared = plan.count ? collectInputs(output, plan, "这段代码需要输入") : Promise.resolve([]);
      prepared.then(function (values) {
        progress.textContent = "正在启动 Python 运行时…";
        return runCode(source, values);
      }).then(function (message) {
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
      status.textContent = "首次运行需下载约 14 MB 的 Python 运行时";
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
      var badge = null;
      if (label) {
        badge = element("span", "cell-kind", DETECT.kindLabel(kind.kind));
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
      var entry = {
        node: node, code: code, output: output, badge: badge, kind: kind.kind, verdict: null, button: null,
      };
      pythonCells.push(entry);
      if (!label) return;
      var button = element("button", "cell-run-button", "▶ 运行");
      button.type = "button";
      entry.button = button;
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
      pythonCells.length + " 个 Python 单元 · 首次运行需下载约 14 MB 运行时");
    bar.appendChild(runAll);
    bar.appendChild(stop);
    bar.appendChild(reset);
    bar.appendChild(status);
    container.insertBefore(bar, container.firstChild);

    var progress = element("p", "py-run-progress");
    container.insertBefore(progress, container.firstChild.nextSibling);

    function markNotRunnable(entry, verdict) {
      entry.verdict = verdict || { ok: false, error: "" };
      entry.node.classList.remove("cell--runnable");
      entry.node.classList.add("cell--not-runnable");
      if (entry.button) {
        entry.button.remove();
        entry.button = null;
      }
      if (entry.badge) {
        entry.badge.textContent = entry.kind === "python" ? "非 Python 代码" : DETECT.kindLabel(entry.kind);
        entry.badge.setAttribute("data-kind", "text");
      }
    }

    function ensureVerdict(entry) {
      if (entry.verdict) return Promise.resolve(entry.verdict);
      return analyzeSources([entry.code]).then(function (results) {
        var verdict = (results && results[0]) || { ok: false, error: "无法判定", line: 0 };
        if (!verdict.ok) markNotRunnable(entry, verdict);
        else entry.verdict = verdict;
        return verdict;
      });
    }

    function renderSkipped(target, entry, verdict) {
      target.textContent = "";
      target.hidden = false;
      target.appendChild(element("div", "py-output-header", "不是 Python 代码 · 未执行"));
      var reason = "";
      if (verdict && verdict.error) {
        reason = "编译器报错：" + verdict.error + (verdict.line ? "（第 " + verdict.line + " 行）" : "") + "。";
      }
      target.appendChild(element("p", "py-output-note",
        "这一段的内容是终端命令、程序输出或其它语言的代码，浏览器里只执行 Python，已跳过。" + reason));
    }

    function runSingle(entry, button, values) {
      if (entry.verdict && !entry.verdict.ok) {
        renderSkipped(entry.output, entry, entry.verdict);
        return Promise.resolve(null);
      }
      entry.output.textContent = "";
      entry.output.hidden = false;
      var line = element("p", "py-run-progress", "检查代码…");
      entry.output.appendChild(line);
      if (button) button.disabled = true;
      return ensureVerdict(entry).then(function (verdict) {
        if (!verdict.ok) {
          renderSkipped(entry.output, entry, verdict);
          return null;
        }
        var plan = inputPlan(entry.code);
        if (plan.count && !values) {
          line.remove();
          if (button) button.disabled = false;
          return collectInputs(entry.output, plan, "这个单元需要输入").then(function (collected) {
            if (button) button.disabled = true;
            return runSingle(entry, button, collected);
          });
        }
        line.textContent = "运行中…";
        return runCode(entry.code, values).then(function (message) {
          renderResult(entry.output, message);
          return message;
        });
      }).catch(function (error) {
        line.textContent = error && error.message === "timeout" ? "运行超过 10 分钟，已放弃" : "运行时不可用，请刷新页面重试";
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
      progress.textContent = "正在检查 " + pythonCells.length + " 个单元…";
      analyzeSources(pythonCells.map(function (entry) { return entry.code; })).then(function (results) {
        var runnable = [];
        var skipped = 0;
        pythonCells.forEach(function (entry, index) {
          var verdict = (results && results[index]) || { ok: false, error: "无法判定", line: 0 };
          entry.verdict = verdict;
          if (verdict.ok) {
            runnable.push(entry);
            return;
          }
          skipped += 1;
          markNotRunnable(entry, verdict);
          renderSkipped(entry.output, entry, verdict);
        });
        if (!runnable.length) {
          progress.textContent = "没有可直接运行的 Python 单元（" + skipped + " 个单元是终端命令、输出或其它语言）";
          setBusy(container, false);
          return;
        }
        var index = 0;
        var plans = runnable.map(function (entry) { return inputPlan(entry.code); });
        var total = plans.reduce(function (sum, plan) { return sum + plan.count; }, 0);
        var begin = Promise.resolve([]);
        if (total) {
          var prompts = [];
          plans.forEach(function (plan, position) {
            plan.prompts.forEach(function (prompt) {
              prompts.push(prompt || ("第 " + (position + 1) + " 个可运行单元"));
            });
          });
          progress.textContent = "运行前需要填写 " + total + " 个输入值";
          var holder = element("div", "py-run-output");
          container.insertBefore(holder, progress.nextSibling);
          begin = collectInputs(holder, { count: total, prompts: prompts }, "这次运行需要输入");
        }
        begin.then(function (values) {
          var cursor = 0;
          var slices = plans.map(function (plan) {
            var slice = values.slice(cursor, cursor + plan.count);
            cursor += plan.count;
            return slice;
          });
          progress.textContent = "开始运行 " + runnable.length + " 个单元…";
        function next() {
          if (index >= runnable.length) {
            progress.textContent = "全部 " + runnable.length + " 个单元运行完毕" +
              (skipped ? "，跳过 " + skipped + " 个非 Python 单元" : "");
            setBusy(container, false);
            return;
          }
          var entry = runnable[index];
          var cellInputs = slices[index];
          index += 1;
          progress.textContent = "运行第 " + index + " / " + runnable.length + " 个单元…";
          runSingle(entry, entry.button, cellInputs).then(next);
        }
        next();
        });
      }).catch(function () {
        progress.textContent = "运行时不可用，请刷新页面重试";
        progress.classList.add("is-error");
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
      status.textContent = pythonCells.length + " 个 Python 单元 · 首次运行需下载约 14 MB 运行时";
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
