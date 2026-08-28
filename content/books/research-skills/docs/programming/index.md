---
title: 编程与人工智能学习中心
hide:
  - toc
---

<div class="learning-hub" markdown>

<header class="learning-hub__hero">
  <p class="learning-hub__eyebrow">PYTHON · MACHINE LEARNING · DEEP LEARNING</p>
  <h1>编程与人工智能学习中心</h1>
  <p>以三套课程与教材为主线：先学 Python 数据分析，再建立机器学习理论，最后进入深度学习。遇到环境、代码或实验问题时，再打开学习帮助。</p>
  <div class="learning-hub__meta"><span>3 套课程教材</span><span>由基础到进阶</span><span>配套学习帮助</span></div>
</header>

## 按课程开始学习

<div class="learning-paths">
  <a class="learning-path learning-path--python" href="../book-sites/python-data-analysis/" target="_top">
    <span class="learning-path__number">FOUNDATION · 系统教材</span>
    <h2>Python 数据分析</h2>
    <p>以《Python 数据分析从入门到精通（第 2 版）》为主教材，覆盖 NumPy、Pandas、Matplotlib、Seaborn 与数据分析流程。</p>
    <span class="learning-path__fit">适合：需要补齐科研数据处理基础</span>
    <strong>进入图书站 →</strong>
  </a>
  <a class="learning-path learning-path--ml" href="../book-sites/zhou-machine-learning/" target="_top">
    <span class="learning-path__number">THEORY · 原理教材</span>
    <h2>周志华《机器学习》</h2>
    <p>“西瓜书”16 章完整在线正文，并配合本站的 NumPy 源码实验，理解公式如何变成训练过程。</p>
    <span class="learning-path__fit">适合：系统建立机器学习理论框架</span>
    <strong>进入在线图书 →</strong>
  </a>
  <a class="learning-path learning-path--dl" href="../book-sites/deep-learning/" target="_top">
    <span class="learning-path__number">PRACTICE · 进阶课程</span>
    <h2>动手学深度学习</h2>
    <p>以第二版在线教材为主，李沐中文课程为辅，按基础、卷积网络、序列模型、注意力与科研复现组织学习。</p>
    <span class="learning-path__fit">适合：具备 Python 与机器学习基础后进阶</span>
    <strong>进入课程图书站 →</strong>
  </a>
</div>

<div class="tinyml-bridge" markdown>

<span class="tinyml-bridge__label">新增算法模块</span>

## tiny_ml：把西瓜书公式对应到 NumPy 源码

完整整理上游 README 中 25 个算法实现、两份公式推导和四类 sklearn 对照实验；同时按教材章节对齐正文、周志华课件与视频，不再只是文末的一条 GitHub 链接。

[进入 tiny_ml 算法实验室](../book-sites/zhou-machine-learning/tinyml-lab/){ .md-button .md-button--primary }
[查看课程资源矩阵](../book-sites/zhou-machine-learning/course-resources/){ .md-button }

</div>

<details class="learning-support" markdown>
<summary><strong>学习遇到问题？展开学习帮助</strong><small>环境配置 · Python 基础 · 源码理解 · 项目练习 · 实验复现</small></summary>

<div class="skill-matrix" markdown>

-   **环境配置与第一个程序**

    Python 安装、虚拟环境、终端检查、路径与常见报错。

    [打开帮助](start-here.md)

-   **Python 基础与数据处理**

    数组形状、NumPy、CSV、统计量和可视化的可运行示例。

    [打开帮助](python-basics.md)

-   **算法理解与源码阅读**

    借助 `tiny_ml` 理解线性回归、K-Means、PCA、树与验证流程。

    [打开帮助](ml-from-scratch.md)

-   **完整项目练习**

    从数据、特征、划分和模型比较走完一次机器学习实验。

    [开始练习](first-project.md)

-   **实验复现与项目整理**

    项目结构、配置、测试、实验记录和数据泄漏检查。

    [打开帮助](reproducible-research.md)

</div>

!!! info "源码学习材料说明"
    本站借鉴 `fengyang95/tiny_ml` 用 NumPy 实现经典算法并与 scikit-learn 对照的思路。上游仓库未提供许可证，因此本站不整份复制源码，而是重新编写教学代码、解释兼容性问题，并在对应算法处保留来源。

</details>

## 推荐学习顺序

<div class="learning-sequence">
  <div><b>1</b><span><strong>Python 数据分析</strong><small>语法 → NumPy → Pandas → 可视化</small></span></div>
  <i>→</i>
  <div><b>2</b><span><strong>经典机器学习</strong><small>评估 → 模型 → 算法边界</small></span></div>
  <i>→</i>
  <div><b>3</b><span><strong>深度学习实践</strong><small>训练 → 调参 → 复现 → 报告</small></span></div>
</div>

!!! tip "研究生的学习标准"
    每个单元至少留下一个可检查的产物：一页结构化笔记、一份可运行代码、一个结果图，或一段对实验结论的解释。只看完视频不算完成。

</div>
