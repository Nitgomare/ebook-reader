/**
 * 代码类型识别：判断一个文件或一个代码单元是 Python、Notebook、Shell、XML、YAML 还是纯文本。
 * 只做浏览器内可判定的规则匹配，不猜：判定不确定时返回 low 置信度（仍按 Python 尝试，最终以内核编译结果为准）。
 * 同一份实现在 node 里也能直接 require，便于单元测试。
 */
(function (root) {
  "use strict";

  var SHELL_COMMAND = /^(?:sudo|apt|apt-get|dpkg|pip|pip3|python|python3|conda|mamba|uv|colcon|ros2|rosrun|roslaunch|rosnode|rostopic|rosservice|rosparam|rospack|roscd|rosls|catkin|catkin_make|catkin_create_pkg|make|cmake|git|wget|curl|tar|unzip|zip|cd|ls|ll|cp|mv|rm|mkdir|rmdir|chmod|chown|export|source|echo|cat|nano|vim|gedit|bash|sh|zsh|shutdown|reboot|systemctl|journalctl|ssh|scp|nvidia-smi|tree|less|more|head|tail|grep|find|which|whereis|whoami|pwd|kill|ps|top|htop|mount|umount|lsusb|lspci|pkg-config|ldconfig|gedit|xacro)\b/;
  var PYTHON_STRONG_LINE = /^(?:import\s+[\w.]|from\s+[\w.]+\s+import\b|def\s+\w+\s*\(|class\s+\w+\s*[(:]|async\s+def\b|print\s*\(|elif\b|else\s*:\s*$|try\s*:\s*$|except\b|finally\s*:\s*$|with\s+.*\bas\b.*:\s*$|for\s+.*\bin\b.*:\s*$|while\s+.*:\s*$|if\s+.*:\s*$|@\w+)/;
  var PYTHON_STRONG_INLINE = /(?:\bself\.|__\w+__\b|\bNone\b|\bTrue\b|\bFalse\b|\bnot\s|\bassert\s|\braise\s|\blambda\b|\brange\(|\blen\(|\.append\(|\bf"[^"]*\{|\bf'[^']*\{|\bimport\s+[\w.]+)/;
  var PYTHON_WEAK = /(?:^[\w.\[\]]+\s*=\s*[^\s=]|\w+\(|\#[^#]|[[\]{}])/m;
  var C_FAMILY = /^\s*#\s*(?:include|define|ifdef|ifndef|endif|pragma|if\s+defined)\b/;
  var PROMPT_START = /^(?:\$\s|>>>\s|In\s*\[\d*\]:)/;
  var YAML_LINE = /^[\w.$\/-][\w.$\/\-\s]*:\s*(?:$|[^\s:])/;
  var XML_START = /^\s*(?:<\?xml|<[a-zA-Z][\w:-]*(?:\s|>|\/))/;
  var PROSE_PUNCT = /[，。；：、（）《》“”‘’！？]/;
  var CJK = /[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]/g;
  var TABLE_ROW = /^\s*\S+(?:\s{2,}\S+)+\s*$/;
  var SHELL_PROMPT = /(?:^|\s)(?:\$|#)\s*$/;

  function trimSource(source) {
    return String(source == null ? "" : source).replace(/\r\n?/g, "\n").trim();
  }

  function linesOf(source) {
    return trimSource(source).split("\n");
  }

  function substantialLines(source) {
    return linesOf(source).filter(function (line) { return line.trim(); });
  }

  function cjkRatio(source) {
    var stripped = trimSource(source).replace(/\s+/g, "");
    if (!stripped) return 0;
    var matches = stripped.match(CJK);
    return (matches ? matches.length : 0) / stripped.length;
  }

  function hasStrongPythonSignal(source) {
    var lines = linesOf(source);
    for (var i = 0; i < lines.length; i += 1) {
      if (PYTHON_STRONG_LINE.test(lines[i].trim())) return true;
    }
    return PYTHON_STRONG_INLINE.test(source);
  }

  function looksLikeShell(source) {
    var lines = substantialLines(source);
    if (!lines.length) return false;
    var commandLines = lines.filter(function (line) {
      var text = line.trim();
      return text.charAt(0) === "!" || SHELL_PROMPT.test(text) || SHELL_COMMAND.test(text);
    });
    return commandLines.length >= Math.max(1, Math.ceil(lines.length * 0.6));
  }

  function looksLikeYaml(source) {
    var lines = linesOf(source).filter(function (line) {
      var text = line.trim();
      return text && text.charAt(0) !== "#";
    });
    if (lines.length < 2) return false;
    if (hasStrongPythonSignal(source)) return false;
    var yamlLines = lines.filter(function (line) {
      var text = line.trim();
      return YAML_LINE.test(text) || /^-\s+\S/.test(text) || /^\s+-\s+\S/.test(line);
    });
    return yamlLines.length >= Math.ceil(lines.length * 0.7);
  }

  /**
   * 判定这段文本更像“人写的说明 / 程序输出”，而不是代码：
   * 中文占比高、带中文标点、成列的表格行、行尾有 shell 提示符。
   */
  function looksLikeProse(source) {
    var lines = substantialLines(source);
    if (!lines.length) return false;
    if (hasStrongPythonSignal(source)) return false;
    var ratio = cjkRatio(source);
    if (ratio >= 0.15) return true;
    if (PROSE_PUNCT.test(source)) return true;
    var tableLines = lines.filter(function (line) { return TABLE_ROW.test(line); });
    if (tableLines.length >= 2 && tableLines.length >= Math.ceil(lines.length * 0.6)) return true;
    var promptLines = lines.filter(function (line) { return SHELL_PROMPT.test(line.trim()); });
    if (promptLines.length >= Math.ceil(lines.length * 0.5)) return true;
    var proseLines = lines.filter(function (line) {
      var text = line.trim();
      return /[，。、；：！？]/.test(text) || (text.length > 12 && !/[=()\[\]{}<>#:'"@]/.test(text));
    });
    if (proseLines.length >= Math.ceil(lines.length * 0.7) && !/[=()\[\]{}]/.test(source)) return true;
    return false;
  }

  /**
   * 判定单个代码单元。
   * @param {string} source 原始代码文本
   * @param {string} [hint] 上级已知类型（文件扩展名推断），python 之外的类型直接沿用
   * @returns {{kind: string, confidence: string, reason: string}}
   */
  function detectUnit(source, hint) {
    var text = trimSource(source);
    if (!text) return { kind: "empty", confidence: "high", reason: "空单元" };
    if (text.charAt(0) === "!" || /^%(?!%)\w+/.test(text)) {
      return { kind: "shell", confidence: "high", reason: "以 ! 或 % 开头，是终端命令或魔术命令" };
    }
    if (/^%%(?:bash|sh|script\s+bash)/i.test(text)) {
      return { kind: "shell", confidence: "high", reason: "%%bash 单元" };
    }
    if (hint && hint !== "python" && hint !== "notebook" && hint !== "unknown") {
      return { kind: hint, confidence: "high", reason: "按文件类型判定" };
    }
    if (PROMPT_START.test(text)) {
      return { kind: "shell", confidence: "high", reason: "以终端提示符开头，是命令行记录" };
    }
    if (C_FAMILY.test(text)) {
      return { kind: "text", confidence: "high", reason: "C / C++ 头文件或宏，不是 Python" };
    }
    if (XML_START.test(text)) {
      return { kind: "xml", confidence: "high", reason: "以 XML 标签开头" };
    }
    if (/^\s*(?:cmake_minimum_required|project\s*\(|find_package\s*\(|add_executable\s*\(|ament_\w+\s*\()/m.test(text)) {
      return { kind: "cmake", confidence: "high", reason: "CMake 指令" };
    }
    if (looksLikeShell(text)) {
      return { kind: "shell", confidence: "medium", reason: "多数行以终端命令开头" };
    }
    if (looksLikeYaml(text)) {
      return { kind: "yaml", confidence: "medium", reason: "键值对结构，无 Python 语法特征" };
    }
    if (looksLikeProse(text)) {
      return { kind: "text", confidence: "medium", reason: "中文说明或程序输出，不是代码" };
    }
    if (hasStrongPythonSignal(text)) {
      return { kind: "python", confidence: "high", reason: "含 Python 语法特征" };
    }
    return { kind: "python", confidence: "low", reason: "无明确特征，按 Python 尝试执行" };
  }

  var EXTENSION_KINDS = {
    ".py": "python", ".pyw": "python", ".ipynb": "notebook",
    ".sh": "shell", ".bash": "shell", ".zsh": "shell", ".ps1": "shell", ".bat": "shell", ".cmd": "shell",
    ".xml": "xml", ".urdf": "xml", ".sdf": "xml", ".xacro": "xml", ".launch": "xml", ".world": "xml", ".html": "xml",
    ".yml": "yaml", ".yaml": "yaml",
    ".cmake": "cmake", ".txt": "text", ".md": "text", ".csv": "text", ".json": "text",
  };

  function detectFileKind(file) {
    var payload = file || {};
    if (payload.kind === "notebook") return "notebook";
    var name = String(payload.name || payload.path || "").toLowerCase();
    var extension = name.slice(name.lastIndexOf("."));
    if (EXTENSION_KINDS[extension]) return EXTENSION_KINDS[extension];
    var language = String(payload.language || "").toLowerCase();
    if (language === "python" || language === "py") return "python";
    if (language === "notebook" || language === "jupyter") return "notebook";
    if (language === "shell" || language === "bash" || language === "console") return "shell";
    if (language === "xml") return "xml";
    if (language === "yaml" || language === "yml") return "yaml";
    return "unknown";
  }

  function isRunnable(kind) {
    return kind === "python";
  }

  var KIND_LABELS = {
    python: "Python",
    notebook: "Jupyter Notebook",
    shell: "终端命令",
    xml: "XML / URDF",
    yaml: "YAML",
    cmake: "CMake",
    text: "文本 / 输出",
    empty: "空单元",
    unknown: "未知类型",
  };

  function kindLabel(kind) {
    return KIND_LABELS[kind] || kind;
  }

  var api = {
    detectUnit: detectUnit,
    detectFileKind: detectFileKind,
    isRunnable: isRunnable,
    kindLabel: kindLabel,
  };

  if (typeof module !== "undefined" && module.exports) module.exports = api;
  root.PythonDetect = api;
})(typeof globalThis !== "undefined" ? globalThis : this);
