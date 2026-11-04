# 第一篇 Jupyter Notebook 工具 · 导言

## Jupyter Notebook 的简介

Jupyter Notebook（旧称 IPython Notebook）是 Project Jupyter 推出的基于浏览器的交互式编程环境，支持在同一个文档中编写并运行代码、即时查看输出、书写文字说明、插入图片与数学公式。它把代码、结果与叙述组织为"可执行文档"，非常适合数据分析、科学计算、机器学习和教学演示，如今已成为数据科学与科研领域使用最广泛的交互式工具之一。

本书主要基于 Project Jupyter 生态中的 Jupyter Notebook（及其升级版 JupyterLab），使用 Python 语言在浏览器中进行交互式编程与仿真。Jupyter 通过"内核"（Kernel）机制支持 40 多种编程语言，本书以 Python 内核为主，重点介绍 Jupyter Notebook 在数据处理、数据分析、机器学习、科学计算与图像处理等领域的应用。

Jupyter Notebook 的文档由一个个"单元格"（Cell）组成，分为代码单元格与 Markdown 单元格两类。代码单元格可以独立运行并即时显示运行结果；Markdown 单元格支持标题、列表、表格、图片与 LaTeX 数学公式，使代码与叙述在同一文档中并列呈现。配合 numpy、pandas、matplotlib、scikit-learn 等科学计算库，用户可以在文档中直接完成数据加载、计算、绘图与结果分析，无需在多个软件之间来回切换，这大大降低了机器人、控制与算法研究中"写代码、看结果、写说明"的切换成本，也使得实验过程可以被完整地记录与复现。

Jupyter Notebook 的优点包括：

（1）交互性强，易于上手。单元格可以独立运行，代码、输出与说明并列展示，适合边写边调、即时反馈，也非常适合教学演示与算法调试。

（2）生态完善，扩展丰富。Jupyter 支持多种语言内核与丰富的扩展机制（如魔法命令、Widget 交互控件、nbconvert 文档导出等），可与 numpy、pandas、matplotlib、scikit-learn 等科学计算与机器学习库无缝配合。

（3）开放共享，可复现。Notebook 文件（.ipynb）以 JSON 格式保存，便于版本管理与分享；支持导出为 HTML、PDF、Markdown 等格式，也可通过 Binder、nbviewer 等平台在线发布，方便协作交流与研究成果复现。

本书第 1 章介绍 Jupyter Notebook 的下载安装、界面操作、Markdown 与数学公式、Python 代码与魔法命令、数据可视化与数据处理基础；第 2 章通过销售数据分析、机器学习分类、方程求根与微分方程求解、图像处理与协作发布等案例，展示 Jupyter Notebook 的典型应用。

***
