/**
 * 浏览器内 Python 运行时（Web Worker + Pyodide）。
 * 主线程只负责界面；这个文件里没有 DOM，全部计算在独立线程，长循环不会卡住阅读页。
 * 协议：
 *   主线程 → worker  { type: "init", mirrors: string[], version: string, preferred?: string }
 *                    { type: "run", id: string, code: string }
 *    worker → 主线程  { type: "ready", baseUrl, pythonVersion }
 *                    { type: "status", id, message }
 *                    { type: "result", id, stdout, stderr, result, images, error, warning, durationMs }
 *                    { type: "fatal", message }
 */
"use strict";

var pyodide = null;
var baseUrl = "";
var pythonVersion = "";
var bootPromise = null;

var SETUP = [
  "import sys, io, os, ast, base64, traceback, builtins",
  "os.environ.setdefault('MPLBACKEND', 'Agg')",
  "_rkh_globals = globals()",
  "_rkh_internal = set(_rkh_globals.keys())",
  "_rkh_out = io.StringIO()",
  "_rkh_err = io.StringIO()",
  "sys.stdout = _rkh_out",
  "sys.stderr = _rkh_err",
  "",
  "def _rkh_input(*args, **kwargs):",
  "    raise RuntimeError('浏览器环境不支持 input() 交互输入，请把输入改成固定值，或在本机 Jupyter 中运行')",
  "",
  "builtins.input = _rkh_input",
  "builtins.raw_input = _rkh_input",
  "",
  "def _rkh_patch_matplotlib():",
  "    pyplot = sys.modules.get('matplotlib.pyplot')",
  "    if pyplot is None:",
  "        return",
  "    try:",
  "        pyplot.show = lambda *a, **k: None",
  "    except Exception:",
  "        pass",
  "",
  "def _rkh_collect_images(limit=8):",
  "    pyplot = sys.modules.get('matplotlib.pyplot')",
  "    if pyplot is None:",
  "        return []",
  "    images = []",
  "    try:",
  "        numbers = pyplot.get_fignums()",
  "    except Exception:",
  "        numbers = []",
  "    for number in numbers[-limit:]:",
  "        try:",
  "            figure = pyplot.figure(number)",
  "            buffer = io.BytesIO()",
  "            figure.savefig(buffer, format='png', dpi=144, bbox_inches='tight', facecolor='white')",
  "            images.append(base64.b64encode(buffer.getvalue()).decode('ascii'))",
  "        except Exception:",
  "            pass",
  "        finally:",
  "            try:",
  "                pyplot.close(number)",
  "            except Exception:",
  "                pass",
  "    return images",
  "",
  "def _rkh_run(source):",
  "    global _rkh_out, _rkh_err",
  "    _rkh_out = io.StringIO()",
  "    _rkh_err = io.StringIO()",
  "    sys.stdout = _rkh_out",
  "    sys.stderr = _rkh_err",
  "    result = None",
  "    error = ''",
  "    try:",
  "        tree = ast.parse(source, '<cell>', 'exec')",
  "        if tree.body and isinstance(tree.body[-1], ast.Expr):",
  "            head = ast.Module(body=tree.body[:-1], type_ignores=[])",
  "            if head.body:",
  "                exec(compile(head, '<cell>', 'exec'), _rkh_globals)",
  "            result = eval(compile(ast.Expression(tree.body[-1].value), '<cell>', 'eval'), _rkh_globals)",
  "        else:",
  "            exec(compile(tree, '<cell>', 'exec'), _rkh_globals)",
  "    except Exception:",
  "        lines = [line for line in traceback.format_exc().splitlines() if '_rkh_run' not in line]",
  "        error = '\\n'.join(lines[-25:])",
  "    _rkh_patch_matplotlib()",
  "    images = _rkh_collect_images()",
  "    output = _rkh_out.getvalue()",
  "    errors = _rkh_err.getvalue()",
  "    display = ''",
  "    if result is not None and not isinstance(result, str):",
  "        try:",
  "            display = repr(result)",
  "        except Exception:",
  "            display = ''",
  "    return {'stdout': output, 'stderr': errors, 'result': display, 'images': images, 'error': error}",
  "",
  "import platform",
  "_rkh_python_version = platform.python_version()",
].join("\n");

function post(payload) {
  self.postMessage(payload);
}

function isProbeOk(url) {
  return fetch(url, { method: "GET", cache: "force-cache" })
    .then(function (response) { return response.ok; })
    .catch(function () { return false; });
}

function candidateUrls(message) {
  var bases = [];
  var version = String(message.version || "");
  if (message.preferred) bases.push(String(message.preferred));
  (message.mirrors || []).forEach(function (mirror) {
    bases.push(String(mirror).replace(/\/+$/, "") + "/v" + version + "/full/");
  });
  return bases.filter(function (base, index) { return base && bases.indexOf(base) === index; });
}

async function boot(message) {
  var bases = candidateUrls(message);
  var failures = [];
  for (var index = 0; index < bases.length; index += 1) {
    var candidate = bases[index];
    post({ type: "status", message: "正在连接 Python 运行时（" + (index + 1) + "/" + bases.length + "）…" });
    var reachable = await isProbeOk(candidate + "pyodide-lock.json");
    if (!reachable) {
      failures.push(candidate + " 无法访问");
      continue;
    }
    try {
      // Pyodide 0.28 起只支持模块（module）worker，用动态 import 拿 pyodide.mjs
      var module = await import(candidate + "pyodide.mjs");
      pyodide = await module.loadPyodide({ indexURL: candidate });
      baseUrl = candidate;
      await pyodide.runPythonAsync(SETUP);
      pythonVersion = String(pyodide.runPython("_rkh_python_version"));
      post({ type: "ready", baseUrl: baseUrl, pythonVersion: pythonVersion });
      return;
    } catch (error) {
      failures.push(candidate + "：" + String((error && error.message) || error));
      pyodide = null;
    }
  }
  post({ type: "fatal", message: "无法加载 Python 运行时。" + failures.join("；") });
}

async function ensurePackages(code) {
  if (!pyodide) return "";
  try {
    await pyodide.loadPackagesFromImports(code);
    return "";
  } catch (error) {
    var text = String((error && error.message) || error).split("\n")[0];
    return text;
  }
}

function toPlain(pyResult) {
  var plain = pyResult.toJs({ dict_converter: Object.fromEntries });
  pyResult.destroy();
  return plain;
}

async function run(payload) {
  if (!pyodide) {
    // 首次点「运行」时内核可能还在下载：等它就绪，而不是直接报错。
    if (!bootPromise) {
      post({ type: "result", id: payload.id, stdout: "", stderr: "", result: "", images: [],
        error: "Python 运行时尚未开始加载，请再点一次运行。", warning: "", durationMs: 0 });
      return;
    }
    await bootPromise;
    if (!pyodide) {
      post({ type: "result", id: payload.id, stdout: "", stderr: "", result: "", images: [],
        error: "Python 运行时加载失败，请检查网络后刷新页面重试。", warning: "", durationMs: 0 });
      return;
    }
  }
  var started = Date.now();
  post({ type: "status", id: payload.id, message: "准备依赖…" });
  var warning = await ensurePackages(payload.code);
  post({ type: "status", id: payload.id, message: "运行中…" });
  var runner = pyodide.globals.get("_rkh_run");
  var output;
  try {
    var proxy = runner(payload.code);
    output = toPlain(proxy);
  } finally {
    if (runner && runner.destroy) runner.destroy();
  }
  var stdout = String(output.stdout || "");
  var stderr = String(output.stderr || "");
  var limit = 200000;
  if (stdout.length > limit) stdout = stdout.slice(0, limit) + "\n…（输出超过 200 KB，后面省略）";
  if (stderr.length > limit) stderr = stderr.slice(0, limit) + "\n…（输出超过 200 KB，后面省略）";
  post({
    type: "result",
    id: payload.id,
    stdout: stdout,
    stderr: stderr,
    result: String(output.result || ""),
    images: Array.from(output.images || []),
    error: String(output.error || ""),
    warning: warning || "",
    durationMs: Date.now() - started,
  });
}

self.onmessage = function (event) {
  var message = event.data || {};
  if (message.type === "init") {
    if (!bootPromise) {
      bootPromise = boot(message).catch(function (error) {
        post({ type: "fatal", message: String((error && error.message) || error) });
      });
    }
    return;
  }
  if (message.type === "run") {
    run(message).catch(function (error) {
      post({
        type: "result",
        id: message.id,
        stdout: "",
        stderr: "",
        result: "",
        images: [],
        error: String((error && error.message) || error),
        warning: "",
        durationMs: 0,
      });
    });
  }
};
