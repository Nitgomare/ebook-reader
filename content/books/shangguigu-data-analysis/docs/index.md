# Python 数据分析课程

围绕 NumPy、Pandas、Matplotlib 与 Seaborn，将课本、代码和 69 节配套视频组织在同一条学习路径中。建议按表格顺序学习；每章正文末尾仍可查看关联源码和数据文件。

<div class="course-guide-note" markdown="1">

**使用方法**：先读课本定位知识点，再在线打开 Notebook 对照运行，最后用视频补充讲解。课件栏为空表示当前资源中没有对应课件。

</div>

## 课程安排

<div class="course-schedule" markdown="1">

| 主题 | 课本位置 | 课件 | 代码 | 视频 |
| --- | --- | --- | --- | --- |
| 课程介绍与学习路线 | [第 1 章](chapter-01.md) |  |  | [P001](https://www.bilibili.com/video/BV1D9GLzyEL6?p=1) |
| Anaconda、Jupyter 与 PyCharm | [第 1 章](chapter-01.md) |  |  | [P002](https://www.bilibili.com/video/BV1D9GLzyEL6?p=2)<br>[P003](https://www.bilibili.com/video/BV1D9GLzyEL6?p=3)<br>[P004](https://www.bilibili.com/video/BV1D9GLzyEL6?p=4)<br>[P005](https://www.bilibili.com/video/BV1D9GLzyEL6?p=5) |
| NumPy 与 ndarray 基础 | [第 2 章](chapter-02.md) |  | [NumPy Notebook](#/code/2e13022a9c828d0b) | [P006](https://www.bilibili.com/video/BV1D9GLzyEL6?p=6)<br>[P007](https://www.bilibili.com/video/BV1D9GLzyEL6?p=7)<br>[P008](https://www.bilibili.com/video/BV1D9GLzyEL6?p=8) |
| ndarray 创建与数据类型 | [第 2 章](chapter-02.md) |  | [NumPy Notebook](#/code/2e13022a9c828d0b) | [P009](https://www.bilibili.com/video/BV1D9GLzyEL6?p=9)<br>[P010](https://www.bilibili.com/video/BV1D9GLzyEL6?p=10)<br>[P011](https://www.bilibili.com/video/BV1D9GLzyEL6?p=11)<br>[P012](https://www.bilibili.com/video/BV1D9GLzyEL6?p=12) |
| 索引、运算与常用函数 | [第 2 章](chapter-02.md) |  | [NumPy Notebook](#/code/2e13022a9c828d0b) | [P013](https://www.bilibili.com/video/BV1D9GLzyEL6?p=13)<br>[P014](https://www.bilibili.com/video/BV1D9GLzyEL6?p=14)<br>[P015](https://www.bilibili.com/video/BV1D9GLzyEL6?p=15)<br>[P016](https://www.bilibili.com/video/BV1D9GLzyEL6?p=16)<br>[P017](https://www.bilibili.com/video/BV1D9GLzyEL6?p=17)<br>[P018](https://www.bilibili.com/video/BV1D9GLzyEL6?p=18) |
| NumPy 小结与练习 | [第 2 章](chapter-02.md) |  | [NumPy Notebook](#/code/2e13022a9c828d0b) | [P019](https://www.bilibili.com/video/BV1D9GLzyEL6?p=19)<br>[P020](https://www.bilibili.com/video/BV1D9GLzyEL6?p=20)<br>[P021](https://www.bilibili.com/video/BV1D9GLzyEL6?p=21) |
| Pandas 与 Series 基础 | [第 3 章](chapter-03.md) |  | [Series Notebook](#/code/12d66456459b48d3) | [P022](https://www.bilibili.com/video/BV1D9GLzyEL6?p=22)<br>[P023](https://www.bilibili.com/video/BV1D9GLzyEL6?p=23)<br>[P024](https://www.bilibili.com/video/BV1D9GLzyEL6?p=24)<br>[P025](https://www.bilibili.com/video/BV1D9GLzyEL6?p=25)<br>[P026](https://www.bilibili.com/video/BV1D9GLzyEL6?p=26)<br>[P027](https://www.bilibili.com/video/BV1D9GLzyEL6?p=27) |
| Series 数据分析案例 | [第 3 章](chapter-03.md) |  | [Series Notebook](#/code/12d66456459b48d3) | [P028](https://www.bilibili.com/video/BV1D9GLzyEL6?p=28)<br>[P029](https://www.bilibili.com/video/BV1D9GLzyEL6?p=29)<br>[P030](https://www.bilibili.com/video/BV1D9GLzyEL6?p=30)<br>[P031](https://www.bilibili.com/video/BV1D9GLzyEL6?p=31)<br>[P032](https://www.bilibili.com/video/BV1D9GLzyEL6?p=32)<br>[P033](https://www.bilibili.com/video/BV1D9GLzyEL6?p=33) |
| DataFrame 基础与常用方法 | [第 3 章](chapter-03.md) |  | [DataFrame Notebook](#/code/6c1ffe660171cb77) | [P034](https://www.bilibili.com/video/BV1D9GLzyEL6?p=34)<br>[P035](https://www.bilibili.com/video/BV1D9GLzyEL6?p=35)<br>[P036](https://www.bilibili.com/video/BV1D9GLzyEL6?p=36)<br>[P037](https://www.bilibili.com/video/BV1D9GLzyEL6?p=37)<br>[P038](https://www.bilibili.com/video/BV1D9GLzyEL6?p=38) |
| DataFrame 案例与小结 | [第 3 章](chapter-03.md) |  | [DataFrame Notebook](#/code/6c1ffe660171cb77) | [P039](https://www.bilibili.com/video/BV1D9GLzyEL6?p=39)<br>[P040](https://www.bilibili.com/video/BV1D9GLzyEL6?p=40)<br>[P041](https://www.bilibili.com/video/BV1D9GLzyEL6?p=41) |
| 数据分析流程与数据导入导出 | [第 3 章](chapter-03.md) |  | [数据分析 Notebook](#/code/760170eac73f6f5c) | [P042](https://www.bilibili.com/video/BV1D9GLzyEL6?p=42)<br>[P043](https://www.bilibili.com/video/BV1D9GLzyEL6?p=43) |
| 清洗、变形、分箱与时间数据 | [第 3 章](chapter-03.md) |  | [数据分析 Notebook](#/code/760170eac73f6f5c) | [P044](https://www.bilibili.com/video/BV1D9GLzyEL6?p=44)<br>[P045](https://www.bilibili.com/video/BV1D9GLzyEL6?p=45)<br>[P046](https://www.bilibili.com/video/BV1D9GLzyEL6?p=46)<br>[P047](https://www.bilibili.com/video/BV1D9GLzyEL6?p=47)<br>[P048](https://www.bilibili.com/video/BV1D9GLzyEL6?p=48) |
| 分组聚合与综合案例 | [第 3 章](chapter-03.md) |  | [数据分析 Notebook](#/code/760170eac73f6f5c) | [P049](https://www.bilibili.com/video/BV1D9GLzyEL6?p=49)<br>[P050](https://www.bilibili.com/video/BV1D9GLzyEL6?p=50)<br>[P051](https://www.bilibili.com/video/BV1D9GLzyEL6?p=51)<br>[P052](https://www.bilibili.com/video/BV1D9GLzyEL6?p=52) |
| 数据可视化与 Matplotlib | [第 4 章](chapter-04.md) |  | [Matplotlib Notebook](#/code/aab09632493e7a4b) | [P053](https://www.bilibili.com/video/BV1D9GLzyEL6?p=53)<br>[P054](https://www.bilibili.com/video/BV1D9GLzyEL6?p=54)<br>[P055](https://www.bilibili.com/video/BV1D9GLzyEL6?p=55)<br>[P056](https://www.bilibili.com/video/BV1D9GLzyEL6?p=56)<br>[P057](https://www.bilibili.com/video/BV1D9GLzyEL6?p=57)<br>[P058](https://www.bilibili.com/video/BV1D9GLzyEL6?p=58)<br>[P059](https://www.bilibili.com/video/BV1D9GLzyEL6?p=59)<br>[P060](https://www.bilibili.com/video/BV1D9GLzyEL6?p=60) |
| Seaborn 可视化 | [第 4 章](chapter-04.md) |  | [Seaborn Notebook](#/code/699e2e2adb7101e2) | [P061](https://www.bilibili.com/video/BV1D9GLzyEL6?p=61) |
| 房地产市场分析项目 | [第 4 章](chapter-04.md) |  | [项目 Notebook](#/code/a72d82e453f4f082) | [P062](https://www.bilibili.com/video/BV1D9GLzyEL6?p=62)<br>[P063](https://www.bilibili.com/video/BV1D9GLzyEL6?p=63)<br>[P064](https://www.bilibili.com/video/BV1D9GLzyEL6?p=64)<br>[P065](https://www.bilibili.com/video/BV1D9GLzyEL6?p=65)<br>[P066](https://www.bilibili.com/video/BV1D9GLzyEL6?p=66)<br>[P067](https://www.bilibili.com/video/BV1D9GLzyEL6?p=67)<br>[P068](https://www.bilibili.com/video/BV1D9GLzyEL6?p=68)<br>[P069](https://www.bilibili.com/video/BV1D9GLzyEL6?p=69) |

</div>

## 学习路径

1. [数据分析概述与环境搭建](chapter-01.md)
2. [NumPy 科学计算](chapter-02.md)
3. [Pandas 数据分析](chapter-03.md)
4. [数据可视化与项目实战](chapter-04.md)

> 所有 Notebook、示例源码和数据集均可在网页端预览，也可下载后在本地运行。
