window.MathJax = {
  tex: {
    inlineMath: [
      ["\\(", "\\)"]
    ],
    displayMath: [
      ["\\[", "\\]"]
    ],
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex"
  }
};

function renderMath() {
  if (
    window.MathJax &&
    typeof window.MathJax.typesetPromise === "function"
  ) {
    MathJax.typesetClear();
    MathJax.texReset();
    MathJax.typesetPromise();
  }
}

/* Material for MkDocs */
if (typeof document$ !== "undefined") {
  document$.subscribe(function () {
    renderMath();
  });
}

/* 普通 MkDocs 主题 */
document.addEventListener("DOMContentLoaded", function () {
  renderMath();
});