---
hide:
  - toc
---

<div class="study-hero" markdown>

<span class="study-hero__eyebrow">READ · SEARCH · COPY · DOWNLOAD</span>

# 交互式代码学习器

在线切换第 3～7 章脚本，并按教材三级大纲查看代码片段；也可搜索关键写法、复制当前片段。在线内容与下载入口读取同一份 `.py` 文件；需要运行、修改或保存结果时，请下载后在本地 Python 环境中练习。

[返回课程资源](course-resources.md){ .md-button }
[返回课程首页](index.md){ .md-button }

</div>

<div class="code-explorer" data-code-explorer data-code-base="../assets/code/">
  <div class="code-explorer__controls">
    <label class="code-explorer__field">
      <span>学习章节</span>
      <select data-role="chapter" aria-label="选择学习章节"></select>
    </label>
    <label class="code-explorer__field code-explorer__field--wide">
      <span>教材大纲 / 学习工具</span>
      <select data-role="section" aria-label="选择代码小节"></select>
    </label>
    <div class="code-explorer__primary-actions">
      <button type="button" data-action="copy">复制当前片段</button>
      <a data-role="download" class="code-explorer__download" download>下载完整脚本</a>
    </div>
  </div>

  <div class="code-explorer__searchbar">
    <label class="code-explorer__search">
      <span class="code-explorer__sr-only">搜索当前代码</span>
      <input type="search" data-role="search" placeholder="搜索函数、变量或注释，按 / 可快速定位" autocomplete="off" />
    </label>
    <span class="code-explorer__match-count" data-role="match-count">未搜索</span>
    <button type="button" data-action="previous-match" aria-label="上一个匹配">↑</button>
    <button type="button" data-action="next-match" aria-label="下一个匹配">↓</button>
    <label class="code-explorer__wrap"><input type="checkbox" data-role="wrap" /> 自动换行</label>
  </div>

  <div class="code-explorer__meta" aria-live="polite">
    <span data-role="status">正在准备代码学习器……</span>
    <span data-role="range"></span>
  </div>

  <div class="code-explorer__viewport" data-role="viewport" tabindex="0" aria-label="Python 源代码">
    <ol class="code-explorer__lines" data-role="lines"></ol>
  </div>

  <div class="code-explorer__footer">
    <span>快捷键：<kbd>/</kbd> 搜索，<kbd>Alt</kbd> + <kbd>↑</kbd>/<kbd>↓</kbd> 切换匹配行</span>
    <a data-role="raw" target="_blank" rel="noopener">打开原始文件</a>
  </div>

  <noscript>需要启用 JavaScript 才能使用分节、搜索和复制功能；仍可从课程资源页直接下载脚本。</noscript>
</div>

!!! tip "推荐使用方式"
    先选择一个教材大纲条目，读注释并预测输出；用搜索定位 `loc`、`axis`、`dtype` 等概念；复制片段到本地修改数据；最后下载完整脚本运行自动检查。
