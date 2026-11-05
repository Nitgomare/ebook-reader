import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const projectRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const packageRoot = process.env.PYODIDE_NODE_DIR
  || path.join(projectRoot, "tmp", "pyodide-node", "node_modules", "pyodide");
const { loadPyodide } = require(path.join(packageRoot, "pyodide.js"));

const workerSource = readFileSync(new URL("../public/python-worker.js", import.meta.url), "utf8");
const start = workerSource.indexOf("var SETUP = [");
const end = workerSource.indexOf('].join("\\n");', start);
if (start < 0 || end < 0) throw new Error("无法从 python-worker.js 提取 SETUP");
const arrayLiteral = workerSource.slice(start + "var SETUP = ".length, end + 1);
const SETUP = eval(arrayLiteral).join("\n");

const pyodide = await loadPyodide({
  indexURL: packageRoot,
});
await pyodide.runPythonAsync(SETUP);
console.log("python", pyodide.runPython("_rkh_python_version"));

const runner = pyodide.globals.get("_rkh_run");
function run(code, inputs) {
  const proxy = runner(code, inputs || []);
  const plain = proxy.toJs({ dict_converter: Object.fromEntries });
  proxy.destroy();
  return plain;
}

const checks = [];
function check(name, condition, detail) {
  checks.push({ name, ok: Boolean(condition), detail });
  console.log((condition ? "PASS " : "FAIL ") + name + (detail ? " → " + detail : ""));
}

// 1. 打印与表达式回显
let out = run("print('hello 世界')\n6 * 7");
check("stdout 捕获", out.stdout === "hello 世界\n", JSON.stringify(out.stdout));
check("末表达式回显", out.result === "42", out.result);
check("无错误", !out.error, out.error);

// 2. 变量跨单元保留
out = run("total = 6 * 7");
out = run("print(total + 1)");
check("跨单元共享变量", out.stdout === "43\n", JSON.stringify(out.stdout));

// 3. 语法定价与报错格式
out = run("def f(:\n    pass");
check("语法错误被捕获", /SyntaxError/.test(out.error), out.error.split("\n").slice(-1)[0]);
check("报错不含内部帧", !/_rkh_run/.test(out.error));

// 4. 运行期异常
out = run("1 / 0");
check("异常被捕获", /ZeroDivisionError/.test(out.error), out.error.split("\n").slice(-1)[0]);

// 5. input()：没给值时给出可读提示，给了值时回显到 stdout
out = run("input('名字')");
check("input 缺值提示", /没有提供/.test(out.error), out.error.split("\n").slice(-1)[0]);
out = run("name = input('名字：')\nprint('你好', name)", ["肥鱼"]);
check("input 取值", out.stdout === "名字：肥鱼\n你好 肥鱼\n", JSON.stringify(out.stdout));
check("input 结束不报错", !out.error, out.error);
out = run("print(input())", ["多余的值"]);
check("空提示也回显", out.stdout === "多余的值\n多余的值\n", JSON.stringify(out.stdout));

// 6. stderr 分离
out = run("import sys\nprint('e', file=sys.stderr)");
check("stderr 捕获", out.stderr === "e\n", JSON.stringify(out.stderr));
check("stdout 未混入 stderr", out.stdout === "", JSON.stringify(out.stdout));

// 7. repr 不重复字符串
out = run("'done'");
check("字符串结果不回显", out.result === "", JSON.stringify(out.result));

// 8. 空图列表（未装 matplotlib 时不应崩溃）
out = run("x = [1, 2, 3]\nsum(x)");
check("无图形时 images 为空", Array.isArray(out.images) && out.images.length === 0, JSON.stringify(out.images));

// 9. 多行末表达式 + 中间语句
out = run("a = 2\nb = 3\na ** b");
check("中间语句不影响末表达式", out.result === "8", out.result);

// 10. 中文与 Unicode
out = run("print('中文 ♥ 测试')");
check("Unicode 输出", out.stdout === "中文 ♥ 测试\n", JSON.stringify(out.stdout));

// 11. 图形捕获：用假的 matplotlib.pyplot 验证「保存为 base64 → images」这条路径
const stub = [
  "import sys, types, io",
  "class _Figure:",
  "    def savefig(self, buffer, **kwargs):",
  "        buffer.write(b'\\x89PNG\\r\\n\\x1a\\n' + bytes([token]))",
  "class _Pyplot(types.ModuleType):",
  "    def __init__(self):",
  "        super().__init__('matplotlib.pyplot')",
  "        self.closed = []",
  "    def get_fignums(self):",
  "        return [1, 2]",
  "    def figure(self, number):",
  "        global token",
  "        token = number",
  "        return _Figure()",
  "    def close(self, number):",
  "        self.closed.append(number)",
  "    def show(self, *args, **kwargs):",
  "        raise AssertionError('show() 应该被替换掉')",
  "sys.modules['matplotlib'] = types.ModuleType('matplotlib')",
  "sys.modules['matplotlib.pyplot'] = _Pyplot()",
].join("\n");
out = run(stub);
check("假 pyplot 注入无错误", !out.error, out.error);
out = run("print('绘制完成')");
check("图形被捕获为两张", out.images.length === 2, JSON.stringify(out.images.length));
check("图形是 base64 PNG", out.images.every((item) => Buffer.from(item, "base64").subarray(1, 4).toString() === "PNG"));
out = run("import matplotlib.pyplot as plt\nprint(plt.show())");
check("show() 已被替换为空操作", out.stdout === "None\n", JSON.stringify(out.stdout));

runner.destroy();
const failed = checks.filter((item) => !item.ok);
console.log(`\n${checks.length - failed.length}/${checks.length} 通过`);
if (failed.length) process.exitCode = 1;
