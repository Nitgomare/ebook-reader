import assert from "node:assert/strict";
import { createRequire } from "node:module";
import test from "node:test";

const require = createRequire(import.meta.url);
const detect = require("../public/python-detect.js");

test("识别纯 Python 单元", () => {
  const cases = [
    "import numpy as np\nx = np.linspace(0, 6, 100)\nprint(x.mean())",
    "def add(a, b):\n    return a + b",
    "class Point:\n    pass",
    "for i in range(3):\n    print(i)",
    "x = [1, 2, 3]\nsum(x)",
    "print('hello')",
  ];
  for (const source of cases) {
    const result = detect.detectUnit(source, "python");
    assert.equal(result.kind, "python", source);
    assert.equal(detect.isRunnable(result.kind), true);
  }
});

test("识别终端命令与魔术命令", () => {
  const cases = [
    "!pip install numpy",
    "!apt-get update",
    "%matplotlib inline",
    "%%bash\nls -l",
    "sudo apt install ros-humble-desktop",
    "ros2 run turtlesim turtlesim_node\nros2 topic list",
    "$ python3 main.py",
    "pip install -r requirements.txt",
  ];
  for (const source of cases) {
    const result = detect.detectUnit(source, "python");
    assert.equal(result.kind, "shell", source);
    assert.equal(detect.isRunnable(result.kind), false);
  }
});

test("识别 XML / URDF 与 YAML 配置", () => {
  assert.equal(
    detect.detectUnit('<?xml version="1.0"?>\n<robot name="so101">\n</robot>').kind,
    "xml",
  );
  assert.equal(detect.detectUnit('<sdf version="1.7">\n  <model name="box"/>\n</sdf>').kind, "xml");
  assert.equal(
    detect.detectUnit("turtlesim:\n  ros__parameters:\n    background_r: 69").kind,
    "yaml",
  );
});

test("识别 CMake 与纯文本", () => {
  assert.equal(
    detect.detectUnit("cmake_minimum_required(VERSION 3.8)\nproject(demo)").kind,
    "cmake",
  );
  assert.equal(detect.detectUnit("   ").kind, "empty");
});

test("文件级类型按扩展名判定", () => {
  assert.equal(detect.detectFileKind({ name: "01_基础.py" }), "python");
  assert.equal(detect.detectFileKind({ name: "第1章.ipynb", kind: "notebook" }), "notebook");
  assert.equal(detect.detectFileKind({ name: "setup.sh" }), "shell");
  assert.equal(detect.detectFileKind({ name: "robot.urdf" }), "xml");
  assert.equal(detect.detectFileKind({ name: "params.yaml" }), "yaml");
  assert.equal(detect.detectFileKind({ name: "readme.txt" }), "text");
  assert.equal(detect.detectFileKind({ name: "data.csv" }), "text");
  assert.equal(detect.detectFileKind({ name: "notes", language: "python" }), "python");
});

test("低置信度时仍按 Python 尝试，并给出可读标签", () => {
  const result = detect.detectUnit("x", "python");
  assert.equal(result.kind, "python");
  assert.equal(result.confidence, "low");
  assert.equal(detect.kindLabel("shell"), "终端命令");
  assert.equal(detect.kindLabel("python"), "Python");
});
