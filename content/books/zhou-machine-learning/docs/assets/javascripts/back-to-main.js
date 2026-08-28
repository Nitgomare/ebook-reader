(() => {
  const addBackButton = () => {
    const header = document.querySelector(".md-header__inner");
    if (!header || header.querySelector(".back-to-main")) return;
    const logo = header.querySelector("a.md-logo");
    if (logo) {
      logo.removeAttribute("href");
      logo.removeAttribute("target");
      logo.setAttribute("aria-hidden", "true");
      logo.tabIndex = -1;
    }
    const link = document.createElement("a");
    link.className = "back-to-main";
    link.href = "/";
    link.target = "_top";
    link.setAttribute("aria-label", "返回主站首页");
    link.title = "返回主站首页";
    link.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"></path></svg>';
    const searchToggle = header.querySelector('label[for="__search"]');
    if (searchToggle) header.insertBefore(link, searchToggle);
    else header.append(link);
  };
  if (typeof document$ !== "undefined") document$.subscribe(addBackButton);
  else document.addEventListener("DOMContentLoaded", addBackButton);
})();
