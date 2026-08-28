---
title: 从这里开始
---

# 从这里开始：把电脑变成科研工具

这不是一份“把 Python 语法背一遍”的清单。你的第一个目标是：**在一个独立环境中运行脚本，读取一组数据，生成一张图，并且知道出错后去哪里找原因。**

## 15 分钟能力诊断

逐项判断自己能否独立完成。遇到第一个“不能”，就从对应位置开始。

| 我能独立完成 | 否：从哪里开始 | 是：下一步 |
|---|---|---|
| 在终端看到 `python --version` | 本页“建立环境” | 创建虚拟环境 |
| 解释 `.venv` 为什么不能提交到 Git | 本页“建立环境” | 运行第一个脚本 |
| 看懂 `(1000, 3)` 代表什么 | [Python 基础与数据处理](python-basics.md) | 处理一组数组数据 |
| 区分训练集、验证集和测试集 | [从零读懂机器学习](ml-from-scratch.md) | 做完整项目 |
| 知道同一对象的数据不能随机散落两边 | [第一个机器学习完整项目](first-project.md) | 整理一次完整实验 |
| 别人按 README 能复现自己的结果 | [实验复现与项目整理](reproducible-research.md) | 可以进入真实课题 |

## 建立第一个独立环境

在 Windows Terminal 或 VS Code 终端中执行：

```powershell
mkdir python-lab
cd python-lab
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install numpy pandas matplotlib scipy scikit-learn jupyterlab
```

macOS / Linux 只需把激活命令换成：

```bash
source .venv/bin/activate
```

!!! question "PowerShell 提示禁止运行脚本怎么办？"
    先执行 `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`，关闭并重新打开终端，再激活环境。只修改当前用户范围，不要为了省事关闭系统安全策略。

用下面三条命令做验收：

```powershell
where.exe python
python --version
python -c "import numpy, sklearn; print(numpy.__version__, sklearn.__version__)"
```

第一条输出应指向项目中的 `.venv`。如果仍指向系统 Python，说明环境没有激活。

## 第一个可检查的程序

新建 `check_signal.py`：

```python
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(42)
fs = 1_000  # Hz
t = np.arange(0, 1, 1 / fs)
acceleration = 0.8 * np.sin(2 * np.pi * 30 * t) + 0.08 * rng.normal(size=t.size)

output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)

fig, ax = plt.subplots(figsize=(8, 3))
ax.plot(t[:250], acceleration[:250], linewidth=1)
ax.set(xlabel="Time [s]", ylabel="Acceleration [m/s²]", title="Synthetic vibration")
fig.tight_layout()
fig.savefig(output_dir / "signal.png", dpi=180)

print(f"shape={acceleration.shape}, rms={np.sqrt(np.mean(acceleration**2)):.3f} m/s²")
```

运行：

```powershell
python check_signal.py
```

验收标准：终端打印 `shape=(1000,)`，并且 `outputs/signal.png` 能打开。现在你已经完成了科研编程最小闭环：**输入假设 → 数值计算 → 可视化 → 保存结果**。

## 看懂报错，而不是复制报错

Python 的 Traceback 要从最后一行开始读：

1. 最后一行：错误类型和直接原因，例如 `FileNotFoundError`。
2. 向上找到第一个属于你项目的文件，而不是第三方库文件。
3. 打印关键变量的 `type()`、`shape`、范围和单位。
4. 把问题缩成十行以内的最小示例，再搜索完整错误信息。

常见问题可以先按下面判断：

| 症状 | 最可能原因 | 先检查 |
|---|---|---|
| `ModuleNotFoundError` | 装到了另一个 Python | `where.exe python` 与 `python -m pip --version` |
| `FileNotFoundError` | 当前工作目录与想象不同 | `Path.cwd()` 与 `Path(__file__).parent` |
| `ValueError: shapes ...` | 样本轴、特征轴混了 | 每一步都打印 `array.shape` |
| 图上有中文方框 | Matplotlib 字体缺失 | 先用英文坐标，之后统一配置字体 |
| 模型测试分数异常高 | 数据泄漏或重复样本 | 按设备/试验批次分组划分 |

## 30 天最短路线

| 周次 | 只学这些 | 必须留下的产物 |
|---|---|---|
| 第 1 周 | 环境、变量、函数、路径、异常 | 一个能读取文件并保存图片的脚本 |
| 第 2 周 | NumPy 数组、广播、索引、FFT | 一张时域图和一张频谱图 |
| 第 3 周 | Pandas、缺失值、分组统计、可视化 | 一份清洗后的 CSV 与数据字典 |
| 第 4 周 | 划分、基线模型、指标、交叉验证 | 一张比较表和一段结论 |

不要等“语法全部学完”才开始处理数据。每学一个概念，马上在一小组真实或模拟数据上使用；语法会在重复使用中自然固定下来。

## 本页完成标准

- [ ] 项目目录里存在 `.venv`，且 `where.exe python` 指向它。
- [ ] `check_signal.py` 能从空目录一次运行成功。
- [ ] `outputs/signal.png` 不是手工拖进来的，而是脚本生成的。
- [ ] 你能解释 `fs`、`t`、`acceleration.shape` 的含义与单位。
- [ ] 你知道下一步该进入 [Python 基础与数据处理](python-basics.md)。
