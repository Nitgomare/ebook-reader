# Python科研计算基础与环境搭建

> **配套资源**
>
> - [播放课程视频（哔哩哔哩）](https://www.bilibili.com/video/BV1pVt363EZy/)
> - [下载课程课件（PPTX）](./Python科研计算基础与环境搭建.pptx)
>
> **内容制作：李锦瑞**

本专题面向需要使用 Python 完成科研数据处理、可视化与建模的学习者。建议先结合课件和视频了解工具链，再按正文步骤完成环境配置与示例实践。

## 第一章 数据分析概述与环境搭建

### 1.1 适用场景

本课程所教授的数据分析技能适用于以下典型场景：

- **科研数据处理**：实验数据清洗、转换、统计检验、结果可视化。
- **工业监控分析**：设备传感器数据（如SCADA）的异常检测、性能趋势分析。
- **商业智能**：销售、用户行为数据的聚合统计与可视化报表。
- **教学演示**：Jupyter Notebook 可即时展示代码、图表和解释，适合教学与报告。
- **快速原型开发**：在投入大型项目前，用 Python 快速验证算法和模型。

### 1.2 数据分析的完整流程

一个典型的数据分析项目通常包含以下环节：

```text
数据采集
    ↓
数据清洗（缺失值、异常值处理）
    ↓
数据探索与统计分析
    ↓
数据可视化
    ↓
建模与评估
    ↓
结果输出与报告
```

本课程将围绕这一流程，从环境搭建开始，逐步掌握每个环节所需的核心工具。

### 1.3 数据分析工具链

本课程使用的核心工具链包括：

| 工具                 | 作用                              |
| -------------------- | --------------------------------- |
| **Anaconda**         | Python 发行版 + 包管理 + 环境管理 |
| **Jupyter Notebook** | 交互式编程环境，适合探索性分析    |
| **PyCharm**          | 集成开发环境，适合项目级代码编写  |
| **NumPy**            | 数值计算基础库                    |
| **pandas**           | 数据处理与分析核心库              |
| **Matplotlib**       | 科研数据可视化库                  |
| **scikit-learn**     | 机器学习建模库                    |

本课程第一章重点完成 **Anaconda + Jupyter Notebook + PyCharm** 的安装与配置，并完成 **NumPy、pandas、Matplotlib** 的导入验证。

---

## 第二章 工具简介

### 2.1 Anaconda：一站式科研环境

Anaconda 是一个面向数据科学的 Python 发行版，它把 Python 解释器、Conda 环境管理工具以及大量数据科学库整合到一起。

#### Anaconda 解决什么问题？

科研工作中经常需要同时使用多个 Python 库：

```text
Python
├── NumPy
├── pandas
├── Matplotlib
├── SciPy
├── scikit-learn
├── Jupyter
└── 其他科研库
```

真正容易出问题的往往不是 Python 语法本身，而是：

```text
Python 版本不一致
+
第三方库版本冲突
+
库之间的依赖关系不兼容
+
不同项目需要使用不同环境
```

Anaconda 通过 Conda 虚拟环境解决了这些问题，让每个科研项目拥有独立、可记录、可恢复的 Python 环境。

> **核心理念：一个科研项目 = 一个相对独立、可记录、可恢复的 Python 环境。**

#### Anaconda 的构成

| 组件                   | 说明                                            |
| ---------------------- | ----------------------------------------------- |
| **Python 解释器**      | 运行 Python 代码的基础                          |
| **Conda**              | 包管理与环境管理工具                            |
| **预置库**             | NumPy、pandas、Matplotlib、SciPy 等 180+ 常用库 |
| **Anaconda Navigator** | 图形化管理界面                                  |
| **Jupyter Notebook**   | 交互式编程环境                                  |

### 2.2 Jupyter Notebook：交互式数据分析

Jupyter Notebook 是一个开源的交互式计算环境，广泛应用于数据科学、机器学习、科学研究等领域。其主要组件包括：

- **Jupyter Notebook**：经典的交互式编程界面，代码、文本、公式、图表混排
- **JupyterLab**：Notebook 的继承者，提供更现代化和功能丰富的界面

#### 为什么适合科研数据分析？

科研数据分析的工作模式通常是：

```text
读取数据 → 查看数据 → 修改代码 → 重新运行 → 画图 → 检查异常 → 修改参数 → 再运行
```

Jupyter Notebook 完美契合这一流程：

| 特性              | 说明                                           |
| ----------------- | ---------------------------------------------- |
| **代码分块运行**  | 每次只执行一个或几个代码块，即时查看结果       |
| **可视化集成**    | 图表直接显示在代码下方                         |
| **Markdown 支持** | 在代码间插入说明文字、标题、列表               |
| **LaTeX 支持**    | 直接编写数学公式                               |
| **结果持久化**    | 所有输出保存在 `.ipynb` 文件中，便于存档和分享 |

#### 适用场景

```text
数据清洗
数据探索
绘图分析
统计分析
模型试验
教学演示
论文前期数据探索
```

### 2.3 PyCharm：科研项目开发环境

PyCharm 是 JetBrains 公司出品的专业 Python IDE。

#### 适用场景

- 批量数据处理脚本编写
- 复杂算法实现
- 完整科研项目的代码组织与管理

#### 核心优势

| 特性                      | 说明                               |
| ------------------------- | ---------------------------------- |
| **Conda 原生集成**        | 一键切换不同虚拟环境作为项目解释器 |
| **Jupyter Notebook 支持** | 在 IDE 内直接编辑、运行 Notebook   |
| **调试器**                | 逐行执行、断点调试、变量监控       |
| **代码补全**              | 智能提示函数名、参数，提升编码效率 |
| **项目文件管理**          | 清晰组织代码、数据、图表等不同模块 |



## 第三章 详细安装与配置步骤


### 3.1 Anaconda 安装与环境配置


#### 3.1.1 下载 Anaconda

**第一步：进入官方网站**

打开浏览器，进入 Anaconda 官方网站：

https://www.anaconda.com/

**第二步：进入下载页面**

点击页面的“Free Download”按钮，进入下载页面。

**第三步：确认系统类型**

Windows 用户通常选择：

```text
64-Bit Graphical Installer
```

如果不确定系统是 32 位还是 64 位：

```text
设置 → 系统 → 系统信息 → 系统类型
```

**第四步：下载**

下载完成后得到一个 `.exe` 安装文件：

```text
Anaconda3-xxxx.x-Windows-x86_64.exe
```

> **复现检查点 01**
>
> 此时不要急着安装多个 Python 版本。
>
> 建议先只建立一套明确的 Anaconda 主环境，减少初学阶段的解释器混乱。


#### 3.1.2 安装 Anaconda（Windows 版）

双击下载的安装程序，按以下步骤操作：

**步骤 1：Welcome**

点击 **Next**

**步骤 2：License Agreement**

阅读许可协议后，点击 **I Agree**

**步骤 3：Installation Type**

选择安装方式：

```text
Just Me（推荐：仅当前用户使用）
```

或

```text
All Users（需要管理员权限，所有用户共享）
```

**步骤 4：安装路径**

建议使用简洁的路径，例如：

```text
D:\Anaconda
```

或

```text
C:\Users\你的用户名\anaconda3
```

> ⚠️ **不建议**在初学阶段使用包含中文字符或特殊符号的路径。

**步骤 5：安装选项**

如果安装程序出现以下选项：

```text
Add Anaconda to my PATH environment variable
```

初学阶段推荐 **不勾选** 此项。更稳妥的方法是使用 Anaconda Prompt 或手动配置环境变量。

**步骤 6：完成安装**

点击 **Install**，等待安装完成（约 5-10 分钟），点击 **Next → Next → Finish**。


#### 3.1.3 验证安装

**使用 Anaconda Prompt**

在 Windows 开始菜单中搜索：

```text
Anaconda Prompt
```

打开后依次执行以下命令：

```bash
conda --version
```

正常输出类似：

```text
conda 25.x.x
```

继续验证 Python：

```bash
python --version
```

正常输出类似：

```text
Python 3.x.x
```

检查当前 Python 位置：

```bash
where python
```

> **重要原则**
>
> 不要把不同 Python 发行版、多个 Conda 环境、多个虚拟环境的路径全部堆入 PATH。
>
> 路径越混乱，越容易出现：
>
> ```text
> python 能运行
> 但 pip 安装到了另一个 Python
> ```
>
> 或：
>
> ```text
> Jupyter 使用的 Python
> 与
> PyCharm 使用的 Python
> 不一致
> ```

### 3.2 Jupyter Notebook 的使用


#### 3.2.1 启动 Jupyter Notebook

**使用本地 Jupyter**

在 Anaconda Prompt 中输入：

```bash
jupyter notebook
```

正常情况下，浏览器会自动打开 Jupyter Notebook 界面，地址通常是：

```text
http://localhost:8888/
```

如果浏览器没有自动打开，可以手动复制终端中显示的本地地址到浏览器。

**如果提示找不到 jupyter**

说明当前环境中尚未安装 Jupyter：

```bash
conda install notebook
```

安装完成后再次启动：

```bash
jupyter notebook
```

#### 3.2.2 Jupyter Notebook 界面介绍

启动后主要关注以下区域：

| 区域                   | 说明                                  |
| ---------------------- | ------------------------------------- |
| **文件列表**           | 显示当前目录下的所有文件和文件夹      |
| **新建按钮（New）**    | 创建新的 Notebook、文本文件、文件夹等 |
| **上传按钮（Upload）** | 上传已有的 `.ipynb` 文件              |
| **运行状态**           | Kernel 连接状态，右上角显示           |

> **重要概念**
>
> Notebook 本身是 `.ipynb` 文件，而 **Kernel（内核）** 才是实际运行 Python 代码的环境。
>
> 因此必须学会确认：
>
> ```text
> 当前 Notebook
> ↓
> 使用哪个 Kernel
> ↓
> 这个 Kernel 对应哪个 Conda 环境
> ```


#### 3.2.3 Notebook 基本操作

**新建 Notebook**

点击 **New** → **Python 3**，创建一个新的 Notebook。

**重命名**

点击顶部的 **Untitled**，修改为有意义的名称，例如：

```text
01_environment_test.ipynb
```

**Jupyter 快捷键**

| 快捷键          | 功能                           |
| --------------- | ------------------------------ |
| `Shift + Enter` | 运行当前单元格并进入下一个     |
| `Ctrl + Enter`  | 运行当前单元格但停留在当前单元 |
| `Esc + A`       | 在当前单元格上方插入新单元格   |
| `Esc + B`       | 在当前单元格下方插入新单元格   |
| `Esc + M`       | 将当前单元格切换为 Markdown    |
| `Esc + Y`       | 将当前单元格切换为 Code        |
| `Esc + D + D`   | 删除当前单元格                 |

**Code 单元格**

在 Code 单元格中输入 Python 代码，例如：

```python
print("Hello Python")
```

按 `Shift + Enter` 运行，预期输出：

```text
Hello Python
```

**Markdown 单元格**

将单元格切换为 Markdown（`Esc + M`），输入：

```markdown
# 我的第一个科研 Notebook

## 环境测试

这是我的第一个 Jupyter Notebook，用于验证数据分析环境是否配置成功。
```

按 `Shift + Enter` 渲染后即可看到格式化文本。

> **复现检查点 03**
>
> 完成一个 Notebook，并确保其中至少包含：
>
> ```text
> 一个 Markdown 单元格
> 一个 Code 单元格
> 一个正确运行的输出
> ```


#### 3.2.4 在指定虚拟环境中使用 Jupyter

这是整个配置过程中**非常关键的一步**。

**第一步：创建科研环境**

在 Anaconda Prompt 中执行：

```bash
conda create -n research python=3.12
```

创建成功后激活环境：

```bash
conda activate research
```

确认当前环境：

```bash
conda env list
```

正常显示：

```text
base
research     *
```

其中 `*` 表示当前激活的是 `research` 环境。

**第二步：安装基础科研库**

在 `research` 环境中执行：

```bash
conda install numpy pandas matplotlib notebook
```

**第三步：启动 Jupyter**

确保仍在 `research` 环境中：

```bash
jupyter notebook
```



**第四步：验证 Python 解释器路径**

在 Notebook 的 Code 单元格中执行：

```python
import sys

print(sys.executable)
print(sys.version)
```

重点确认 `sys.executable` 输出指向：

```text
...\envs\research\python.exe
```

```text
...\anaconda3\python.exe
```

> **复现检查点 04**
>
> Notebook 中必须能够证明：
>
> ```text
> 当前 Notebook
> ↓
> 使用的是 research 环境
> ↓
> research 环境中的 Python
> ```


### 3.3 PyCharm 中使用 Jupyter 与 Conda 虚拟环境

#### 3.3.1 下载与安装 PyCharm

进入 JetBrains 官方 PyCharm 下载页面：

https://www.jetbrains.com/pycharm/download/

- 当前版本采用统一版 PyCharm，免费版本已包含 Jupyter Notebook 支持
- Windows 用户下载对应操作系统的安装程序
- 按默认流程完成安装即可

#### 3.3.2 在 PyCharm 中配置 Conda 虚拟环境

在实际科研项目中，推荐直接在 PyCharm 中为项目配置独立的 Conda 虚拟环境。这样可以确保 **项目、Python 解释器、第三方库和 Jupyter Kernel** 使用一致的环境。

**第一步：创建项目**

打开 PyCharm → **New Project**

项目名称示例：

```text
wind_power_research
```

在项目创建界面中，找到 **Interpreter type / Python Interpreter** 等解释器设置区域，选择使用 Conda 环境。

推荐设置为：

```text
Environment：Conda
Python version：3.12
Environment location：
<项目路径>\.conda
```

将环境放在项目目录下的 `.conda` 文件夹中，便于区分不同科研项目各自使用的环境。

如果已经安装好 Anaconda 或 Miniconda，PyCharm 通常可以自动识别 Conda；如果没有自动识别，可以在解释器设置中手动指定 Conda 可执行文件，例如：

```text
C:\Users\用户名\anaconda3\Scripts\conda.exe
```

或：

```text
D:\Anaconda\Scripts\conda.exe
```

**第二步：选择已有 Conda 环境**

如果之前已经通过 Anaconda 创建过环境，例如：

```bash
conda create -n research python=3.12
```

则不需要重新创建。

在 PyCharm 的解释器设置中选择：

```text
Conda Environment
→ Existing environment
```

然后选择已有环境中的 Python 解释器，例如：

```text
C:\Users\用户名\anaconda3\envs\research\python.exe
```

配置完成后，PyCharm 的项目解释器就会指向 `research` 环境。

**第三步：确认项目解释器**

进入：

```text
File → Settings → Project → Python Interpreter
```

检查当前解释器是否指向目标 Conda 环境。

例如：

```text
Python Interpreter:
...\anaconda3\envs\research\python.exe
```

或者项目独立环境：

```text
...\wind_power_research\.conda\python.exe
```

> **重要原则**
>
> PyCharm 中最重要的不是“安装了多少个 Python”，而是确认：
>
> ```text
> 当前项目
>     ↓
> 使用哪个 Python Interpreter
>     ↓
> 这个 Interpreter 属于哪个 Conda 环境
>     ↓
> Jupyter Notebook 是否也使用同一个环境
> ```
>
> 如果出现“代码可以运行，但某个库无法导入”的情况，首先检查 **Python Interpreter**，不要立即重复安装软件。

**第四步：在 PyCharm 中安装科研计算库**

确认已经选择正确的 Conda 环境后，可以在 PyCharm 的 Terminal 中执行：

```bash
conda install numpy pandas matplotlib notebook
```

如果需要机器学习功能，再安装：

```bash
conda install scikit-learn
```

也可以在：

```text
File → Settings → Project → Python Interpreter
```

中通过图形界面搜索并安装所需软件包。

安装完成后，可在 PyCharm 的 Python Console 或 Notebook 中验证：

```python
import numpy as np
import pandas as pd
import matplotlib
import sklearn

print("NumPy:", np.__version__)
print("pandas:", pd.__version__)
print("Matplotlib:", matplotlib.__version__)
print("scikit-learn:", sklearn.__version__)
```

**第五步：查看当前 Conda 环境**

在 PyCharm Terminal 中可以使用：

```bash
conda env list
```

查看所有 Conda 环境。

也可以使用：

```bash
python --version
```

和：

```bash
where python
```

检查当前终端使用的 Python 版本和路径。

> **复现检查点 05**
>
> 完成项目创建后，至少确认：
>
> ```text
> 项目已经创建
> ↓
> 项目 Interpreter 指向正确的 Conda 环境
> ↓
> NumPy、pandas、Matplotlib 可以正常导入
> ↓
> Python 路径与预期环境一致
> ```
>
> 到这里，PyCharm 的 Conda 虚拟环境基本配置完成。

#### 3.3.3 PyCharm 中新建 Jupyter Notebook 并运行

**第一步：创建项目目录**

推荐项目目录结构：

```text
wind_power_research/
│
├── notebooks/          # Jupyter Notebook 文件
├── data/               # 数据文件
├── figures/            # 图表输出
├── scripts/             # Python 脚本
├── results/            # 结果输出
├── .conda/              # 项目专用 Conda 环境（如采用项目内环境）
└── README.md            # 项目说明
```

如果使用已经创建好的 Conda 环境，则不一定需要在项目中出现 `.conda` 目录。

**第二步：新建 Notebook**

在项目中：

```text
New → Jupyter Notebook
```

例如：

```text
notebooks/01_environment_test.ipynb
```

**第三步：运行 Notebook**

输入测试代码：

```python
print("PyCharm Jupyter test")
```

点击运行按钮或按 `Shift+Enter`。

**第四步：验证 Notebook 使用的 Python 环境**

在 Notebook 中执行：

```python
import sys

print("Python路径：")
print(sys.executable)

print("\nPython版本：")
print(sys.version)
```

重点检查输出路径是否与前面配置的 Conda 环境一致，例如：

```text
...\anaconda3\envs\research\python.exe
```

或者：

```text
...\wind_power_research\.conda\python.exe
```

这样可以确认：

```text
PyCharm 项目
    ↓
Python Interpreter
    ↓
Conda 环境
    ↓
Jupyter Notebook Kernel
```

使用的是同一个 Python 环境。

#### 3.3.4 PyCharm 基本设置

**主题**

根据个人偏好选择：

```text
File → Settings → Appearance & Behavior → Appearance → Theme
```

推荐科研场景使用深色主题（Darcula），减少长时间编码的眼部疲劳。

**编辑器字体**

```text
File → Settings → Editor → Font
```

建议使用等宽字体，如 Consolas、JetBrains Mono 等。

**解释器检查**

遇到以下问题时：

```text
代码能写
但库导入失败
```

第一反应不是重新安装软件，而是检查：

```text
Python Interpreter
→ 当前项目使用的是哪个 Conda 环境？
```

快速验证代码：

```python
import sys

print("Python路径：")
print(sys.executable)

print("\nPython版本：")
print(sys.version)
```

如果这里显示的 Python 路径与项目所配置的 Conda 环境一致，通常说明解释器配置正确。


## 第四章 完整实例：风电SCADA数据分析

本章以一个真实的**风电SCADA数据集**为例，完整演示从数据加载、探索性分析、可视化到多元回归建模的全流程。通过该实例，你将掌握如何将前面学到的工具链应用于实际科研问题。

### 4.1 数据准备与加载

首先，我们使用 pandas 读取 Excel 数据文件，并查看数据概况。

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

# 设置中文字体（Windows）
plt.rcParams['font.family'] = ['Microsoft YaHei']

# 读取数据
df = pd.read_excel('data/风电scada练习数据.xlsx')
print("数据集形状：", df.shape)
print("前5行数据：")
print(df.head())
print("\n数据统计描述：")
print(df.describe())
```

**输出示例：**
```
数据集形状： (5000, 6)
前5行数据：
   风速  风向  功率  桨距角  发电机转速  风速区间
0  5.2  45.0  120.5  2.3  1450.0   NaN
...
数据统计描述：
             风速         风向          功率       桨距角     发电机转速
count  5000.000000  5000.000000  5000.000000  5000.000000  5000.000000
mean      7.235000   180.500000  1520.340000     8.120000  1620.450000
...
```

### 4.2 探索性可视化分析

#### 4.2.1 时序折线图

绘制风速、功率、发电机转速随样本序号变化的折线图，直观观察变量的变化趋势。

```python
n = len(df)
x = np.arange(n)

plt.figure(figsize=(12, 6))
plt.plot(x, df['风速'], label='风速', linewidth=1)
plt.plot(x, df['功率'], label='功率', linewidth=1)
plt.plot(x, df['发电机转速'], label='发电机转速', linewidth=1.5)
plt.xlabel("记录序号")
plt.ylabel("数值")
plt.title("图1：风速、功率、发电机转速随样本序号变化（折线图）")
plt.legend()
plt.grid(alpha=0.2)
plt.tight_layout()
plt.show()
```

**分析**：从图中可看出功率和发电机转速与风速有相似的变化趋势，初步表明风速是影响功率的关键因素。

#### 4.2.2 散点图：风速与功率关系

```python
plt.figure(figsize=(10, 6))
plt.scatter(df['风速'], df['功率'], s=20, alpha=0.2, color='blue')
plt.xlabel("风速 / (m/s)")
plt.ylabel("功率 / (kW)")
plt.title("风速与功率关系（散点图）")
plt.grid(alpha=0.2)
plt.tight_layout()
plt.show()
```

散点图显示功率随风速增大而上升，且存在明显的正相关关系，但高风速区间功率趋于饱和。

#### 4.2.3 分组平均曲线（风速-功率曲线）

将风速按0.5 m/s 间隔分组，计算每个区间的平均功率，绘制更平滑的功率曲线。

```python
bins = np.arange(1, 19.5, 0.5)
df['风速区间'] = pd.cut(df['风速'], bins=bins)
group = df.groupby('风速区间', observed=True).mean(numeric_only=True)

plt.figure(figsize=(10, 6))
plt.plot(group['风速'], group['功率'], color='red', marker='o', markersize=4, linewidth=1.5, label='平均功率')
plt.xlabel("风速 / (m/s)")
plt.ylabel("平均功率 / (kW)")
plt.title("风速-功率关系（折线图）")
plt.legend()
plt.grid(alpha=0.2)
plt.tight_layout()
plt.show()
```

该曲线清晰展示了风速与功率的典型关系：在切入风速后功率迅速上升，额定风速后趋于稳定。

#### 4.2.4 其他变量关系图

类似地，可绘制风速与桨距角、发电机转速的关系图，了解变量间的关联。

```python
# 风速-桨距角曲线
plt.figure(figsize=(10, 6))
plt.plot(group['风速'], group['桨距角'], marker='o', markersize=4, linewidth=1.5, label='平均桨距角')
plt.xlabel("风速 / (m/s)")
plt.ylabel("桨距角 / (°)")
plt.title("风速-桨距角关系（折线图）")
plt.legend()
plt.grid(alpha=0.2)
plt.tight_layout()
plt.show()

# 风速-发电机转速曲线
plt.figure(figsize=(10, 6))
plt.plot(group['风速'], group['发电机转速'], marker='o', markersize=4, linewidth=1.5, label='平均发电机转速')
plt.xlabel("风速 / (m/s)")
plt.ylabel("发电机转速 / (rpm)")
plt.title("风速-发电机转速关系（折线图）")
plt.legend()
plt.grid(alpha=0.2)
plt.tight_layout()
plt.show()
```

### 4.3 相关性分析

计算各数值变量之间的皮尔逊相关系数，并通过热图直观展示。

```python
data = df[['风速', '风向', '功率', '桨距角', '发电机转速']]
corr = data.corr()
print("相关系数矩阵：")
print(corr)

# 热图绘制
plt.figure(figsize=(8, 8))
plt.imshow(corr, cmap='Blues', vmin=-1, vmax=1)
labels = corr.columns
plt.xticks(np.arange(len(labels)), labels, ha='right', fontsize=10)
plt.yticks(np.arange(len(labels)), labels, fontsize=10)

# 显示数值
for i in range(len(labels)):
    for j in range(len(labels)):
        value = corr.iloc[i, j]
        if abs(value) < 0.005:
            value = 0
        plt.text(j, i, f'{value:.2f}', ha='center', va='center', fontsize=11)

# 网格线
plt.gca().set_xticks(np.arange(-0.5, len(labels), 1), minor=True)
plt.gca().set_yticks(np.arange(-0.5, len(labels), 1), minor=True)
plt.grid(which='minor', color='white', linewidth=1.5)
plt.tick_params(which='minor', bottom=False, left=False)
plt.tick_params(which='major', length=0)

plt.colorbar(label='Pearson相关系数')
plt.title("风电SCADA数据库各变量相关系数矩阵", fontsize=13)
plt.tight_layout()
plt.show()
```

**结果分析**：
- 风速与功率（0.921）、发电机转速（0.866）呈强正相关。
- 桨距角与风速（0.887）也呈强正相关，因为高风速下需要增大桨距角限制功率。
- 风向与其他变量相关性极弱，对功率影响不大。

### 4.4 多元回归建模

我们以**风速**和**桨距角**为特征，**功率**为目标变量，构建多项式回归模型（最高次数为3），用于预测功率。

#### 4.4.1 构造多项式特征

```python
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split

# 原始特征
X_orig = df[['风速', '桨距角']].values
y = df['功率'].values

# 构造3次多项式特征（含交互项）
poly = PolynomialFeatures(degree=3, include_bias=False)
X = poly.fit_transform(X_orig)

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 添加常数项（用于线性回归）
X_train_model = np.column_stack((np.ones(len(X_train)), X_train))
X_test_model = np.column_stack((np.ones(len(X_test)), X_test))
```

#### 4.4.2 模型训练与参数输出

使用最小二乘法求解回归系数。

```python
# 求解系数
coef = np.linalg.lstsq(X_train_model, y_train, rcond=None)[0]

print("模型参数：")
print("截距 =", coef[0])
print("风速系数 =", coef[1])
print("桨距角系数 =", coef[2])
# 还可输出更高次项系数，这里省略
```

**输出示例**：
```
模型参数：
截距 = 1358.0055008829506
风速系数 = -879.3501053333913
桨距角系数 = 1708.0759770896311
```

#### 4.4.3 模型评估

计算测试集上的 MAE、RMSE 和 R²。

```python
y_train_pred = X_train_model @ coef
y_test_pred = X_test_model @ coef

MAE = np.mean(np.abs(y_test - y_test_pred))
RMSE = np.sqrt(np.mean((y_test - y_test_pred) ** 2))
SS_res = np.sum((y_test - y_test_pred) ** 2)
SS_tot = np.sum((y_test - np.mean(y_test)) ** 2)
R2 = 1 - SS_res / SS_tot

print("\n模型评价指标：")
print("MAE =", MAE, "kW")
print("RMSE =", RMSE, "kW")
print("R² =", R2)
```

**输出**：
```
MAE = 107.76552322130024 kW
RMSE = 159.36302534317863 kW
R² = 0.9729513705500539
```

R² 达到 0.973，说明模型解释了97%以上的功率变化，拟合效果良好。

#### 4.4.4 预测结果可视化

绘制测试集上的预测功率与实际功率对比图及散点图。

**对比图**：
```python
test_x = np.arange(len(y_test))
plt.figure(figsize=(20, 6))
plt.plot(test_x, y_test, color='#1f77b4', linestyle='-', linewidth=2.5, label='实际功率', zorder=3)
plt.plot(test_x, y_test_pred, color='#ff7f0e', linestyle='--', linewidth=1.5, alpha=0.7, label='预测功率', zorder=2)
plt.xlabel("测试集样本序号")
plt.ylabel("功率 / kW")
plt.title("预测功率与实际功率对比图")
plt.legend()
plt.grid(alpha=0.2)
plt.tight_layout()
plt.show()
```

**散点图**（理想预测线）：
```python
plt.figure(figsize=(8, 7))
plt.scatter(y_test, y_test_pred, s=8, alpha=0.25, label='预测样本')
min_val = min(y_test.min(), y_test_pred.min())
max_val = max(y_test.max(), y_test_pred.max())
plt.plot([min_val, max_val], [min_val, max_val], linestyle='--', linewidth=1.5, label='理想预测线', color='red')
plt.xlim(0, 3000)
plt.ylim(0, 3000)
plt.xlabel("实际功率 / kW")
plt.ylabel("预测功率 / kW")
plt.title("预测功率与实际功率关系")
plt.legend()
plt.grid(alpha=0.2)
plt.tight_layout()
plt.show()
```

从图形可以看出，预测值紧密围绕理想线分布，误差较小，模型具备较高的预测精度。

---

## 第五章 常见问题与总结

### 5.1 常见问题

**Q1：Jupyter Notebook 启动后找不到内核（Kernel）？**  
A：通常是因为没有在正确的 Conda 环境中安装 Jupyter。请确保先激活目标环境（如 `conda activate research`），再执行 `jupyter notebook`。若仍无效，可在该环境中重新安装：`conda install notebook`。

**Q2：导入 matplotlib 时出现中文乱码？**  
A：需要设置中文字体，如 `plt.rcParams['font.family'] = ['Microsoft YaHei']`（Windows）或 `['SimHei']`。Linux/macOS 需安装相应字体并设置正确路径。

**Q3：pandas 读取 Excel 文件报错？**  
A：需要安装 `openpyxl` 或 `xlrd` 库。可用 `conda install openpyxl` 或 `pip install openpyxl` 解决。

**Q4：模型预测结果 R² 很高但实际应用效果差？**  
A：可能过拟合。建议使用交叉验证、正则化或增加更多样本。本例中数据量较大且特征选择合理，过拟合风险较低。

**Q5：Conda 环境管理混乱，如何清理？**  
A：使用 `conda env list` 查看所有环境，用 `conda remove -n env_name --all` 删除无用环境。定期整理可避免冲突。

**Q6：PyCharm 中无法识别已安装的库？**  
A：检查项目解释器是否指向正确的 Conda 环境（File → Settings → Project → Python Interpreter）。若未显示，手动添加 Conda 环境。

### 5.2 总结

通过本课程的学习，你已经掌握了：

- 数据分析的完整流程和常用工具链。
- Anaconda、Jupyter Notebook 和 PyCharm 的安装与配置方法。
- 使用 pandas 进行数据加载、清洗和探索性分析。
- 利用 Matplotlib 绘制科研级可视化图表。
- 基于 scikit-learn 和 NumPy 构建多项式回归模型，并评估模型性能。本实例以风电SCADA数据为背景，完整再现了从数据理解、可视化、相关性分析到建模预测的全过程。这些技能可迁移至其他科研领域，如环境监测、金融分析、生物信息等。建议你在自己的数据集上重复上述步骤，并尝试调整模型参数、引入更多特征或使用其他算法（如随机森林、XGBoost）进一步提升预测效果。
