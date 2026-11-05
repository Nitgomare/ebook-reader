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
  "_rkh_inputs = []",
  "",
  "def _rkh_set_inputs(values):",
  "    global _rkh_inputs",
  "    _rkh_inputs = [str(item) for item in (values or [])]",
  "",
  "def _rkh_input(prompt=''):",
  "    if not _rkh_inputs:",
  "        raise EOFError('这段代码还要一个输入值，但这次运行没有提供。请在运行前把输入填进页面上的输入框。')",
  "    value = _rkh_inputs.pop(0)",
  "    try:",
  "        sys.stdout.write(str(prompt) + value + '\\n')",
  "    except Exception:",
  "        pass",
  "    return value",
  "",
  "builtins.input = _rkh_input",
  "builtins.raw_input = _rkh_input",
  "",
  "def _rkh_setup_font():",
  "    path = '/fonts/NotoSansSC-Regular.otf'",
  "    try:",
  "        if not os.path.exists(path):",
  "            return",
  "        from matplotlib import font_manager",
  "        if path in getattr(font_manager.fontManager, '_rkh_loaded', set()):",
  "            return",
  "        font_manager.fontManager.addfont(path)",
  "        names = [font_manager.FontProperties(fname=path).get_name(), 'DejaVu Sans']",
  "        import matplotlib",
  "        matplotlib.rcParams['font.sans-serif'] = names",
  "        matplotlib.rcParams['font.family'] = 'sans-serif'",
  "        matplotlib.rcParams['axes.unicode_minus'] = False",
  "        if not hasattr(font_manager.fontManager, '_rkh_loaded'):",
  "            font_manager.fontManager._rkh_loaded = set()",
  "        font_manager.fontManager._rkh_loaded.add(path)",
  "    except Exception:",
  "        pass",
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
  "def _rkh_check(source):",
  "    try:",
  "        compile(source, '<cell>', 'exec')",
  "        return {'ok': True, 'error': '', 'line': 0}",
  "    except SyntaxError as exc:",
  "        return {'ok': False, 'error': str(exc.msg or '语法错误'), 'line': int(exc.lineno or 0)}",
  "    except Exception as exc:",
  "        return {'ok': False, 'error': str(exc), 'line': 0}",
  "",
  "def _rkh_run(source, inputs=None):",
  "    global _rkh_out, _rkh_err",
  "    _rkh_set_inputs(inputs)",
  "    _rkh_setup_font()",
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
      await installFont(pyodide, candidate);
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

async function installFont(instance, base) {
  try {
    var response = await fetch(base + "fonts/NotoSansSC-Regular.otf");
    if (!response.ok) return;
    var bytes = new Uint8Array(await response.arrayBuffer());
    instance.FS.mkdirTree("/fonts");
    instance.FS.writeFile("/fonts/NotoSansSC-Regular.otf", bytes);
  } catch (error) {
    // 字体缺失时退回默认字体，中文会显示方框，不影响其它功能
  }
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
  try {
    pyodide.runPython("_rkh_setup_font()");
  } catch (error) {
    // 字体设置失败不影响运行
  }
  post({ type: "status", id: payload.id, message: "运行中…" });
  var runner = pyodide.globals.get("_rkh_run");
  var output;
  try {
    var proxy = runner(payload.code, payload.inputs || []);
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

async function analyze(payload) {
  if (!pyodide) {
    if (!bootPromise) {
      post({ type: "analysis", id: payload.id, results: [], error: "运行时尚未开始加载" });
      return;
    }
    await bootPromise;
    if (!pyodide) {
      post({ type: "analysis", id: payload.id, results: [], error: "运行时加载失败" });
      return;
    }
  }
  var check = pyodide.globals.get("_rkh_check");
  var sources = payload.sources || [];
  var results = [];
  try {
    for (var index = 0; index < sources.length; index += 1) {
      var proxy = check(String(sources[index] == null ? "" : sources[index]));
      var plain = toPlain(proxy);
      if (proxy && proxy.destroy) proxy.destroy();
      results.push({ ok: !!plain.ok, error: String(plain.error || ""), line: Number(plain.line || 0) });
    }
  } finally {
    if (check && check.destroy) check.destroy();
  }
  post({ type: "analysis", id: payload.id, results: results });
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
  if (message.type === "analyze") {
    analyze(message).catch(function (error) {
      post({ type: "analysis", id: message.id, results: [], error: String((error && error.message) || error) });
    });
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
