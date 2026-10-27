(function () {
  'use strict';
  const base = 'slides/research-skills/';
  let decks = [], category = '全部', query = '', currentPage = 1, observer;
  const $ = id => document.getElementById(id);
  const escape = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const size = bytes => (bytes / 1024 / 1024).toFixed(1) + ' MB';
  const image = (deck, page) => base + deck.id + '/' + String(page).padStart(4, '0') + '.webp';
  function download(deck, cls, label) {
    return '<a class="' + cls + '" href="' + escape(deck.downloadUrl) + '" download="' + escape(deck.sources[0]) + '">' + label + '</a>';
  }
  function renderCards() {
    const selected = decks.filter(d => (category === '全部' || d.category === category) && (d.title + ' ' + d.category).toLocaleLowerCase().includes(query));
    $('resultCount').textContent = selected.length + ' 份';
    $('grid').innerHTML = selected.map(d => '<article class="ppt-card"><a class="cover-link" href="#' + d.id + '" aria-label="预览：' + escape(d.title) + '"><img src="' + image(d, 1) + '" alt="' + escape(d.title) + '封面" loading="lazy"><span class="cover-hover">打开完整预览 →</span></a><div class="card-info"><span class="card-category">' + escape(d.category) + '</span><h3><a href="#' + d.id + '">' + escape(d.title) + '</a></h3><div class="card-meta"><span class="file-type">PPTX</span><span>' + d.pageCount + ' 页</span><span>·</span><span>' + size(d.size) + '</span></div><div class="card-actions"><a class="preview-link" href="#' + d.id + '">在线预览 ↗</a>' + download(d, 'download-link', '↓ 下载原文件') + '</div></div></article>').join('') || '<p class="empty">没有找到匹配的 PPT，试试其他关键词或分类。</p>';
  }
  function selectPage(n, scroll) {
    const deck = decks.find(d => d.id === location.hash.slice(1));
    if (!deck) return;
    currentPage = Math.max(1, Math.min(deck.pageCount, Math.trunc(Number(n)) || 1));
    $('pageNumber').value = currentPage;
    $('prevPage').disabled = currentPage === 1;
    $('nextPage').disabled = currentPage === deck.pageCount;
    document.querySelectorAll('.thumb-list a').forEach((a, i) => a.setAttribute('aria-current', String(i + 1 === currentPage)));
    const thumb = document.querySelector('.thumb-list a[aria-current=true]');
    if (thumb) {
      const rail = thumb.parentElement;
      if (thumb.offsetTop < rail.scrollTop || thumb.offsetTop + thumb.offsetHeight > rail.scrollTop + rail.clientHeight) rail.scrollTop = thumb.offsetTop - rail.clientHeight / 2;
    }
    if (scroll) $('ppt-page-' + currentPage).scrollIntoView({block:'start'});
  }
  function route() {
    if (observer) observer.disconnect();
    const id = location.hash.slice(1);
    const deck = decks.find(d => d.id === id);
    $('library').hidden = !!deck;
    $('detail').hidden = !deck;
    document.title = (deck ? deck.title : 'PPT 资源库') + ' · 科研知识学习中心';
    if (!deck) {
      $('detail').replaceChildren();
      renderCards();
      if (id) {
        const p = document.createElement('p');
        p.className = 'empty'; p.setAttribute('role', 'status'); p.textContent = '该 PPT 不存在，请从下方资源中重新选择。';
        $('grid').prepend(p);
      }
      return;
    }
    $('detail').innerHTML = '<div class="detail-head"><div><a class="back-link" href="ppt-library.html">← 返回 PPT 资源库</a><h1>' + escape(deck.title) + '</h1><div class="detail-meta">' + escape(deck.category) + '　·　' + deck.pageCount + ' 页　·　PPTX　·　' + size(deck.size) + '</div></div>' + download(deck, 'primary-download', '↓ 下载 PPTX') + '</div><div class="preview-layout"><aside class="thumb-panel" aria-label="页面缩略图"><h2>页面目录 · ' + deck.pageCount + ' 页</h2><div class="thumb-list">' + Array.from({length:deck.pageCount}, (_, i) => '<a href="#' + deck.id + '" data-page="' + (i+1) + '" aria-label="查看第 ' + (i+1) + ' 页"><img src="' + image(deck, i+1) + '" loading="lazy" alt=""><span>' + (i+1) + '</span></a>').join('') + '</div></aside><section class="preview-body" id="previewBody" aria-label="PPT 完整预览"><div class="preview-toolbar"><button id="prevPage">← 上一页</button><label class="page-input">第 <input id="pageNumber" type="number" min="1" max="' + deck.pageCount + '" value="1" aria-label="跳转页码"> / ' + deck.pageCount + ' 页</label><button id="nextPage">下一页 →</button><button id="fullscreen">全屏查看</button></div>' + Array.from({length:deck.pageCount}, (_, i) => '<figure class="slide-page" id="ppt-page-' + (i+1) + '" data-page="' + (i+1) + '"><img src="' + image(deck, i+1) + '" width="' + deck.width + '" height="' + deck.height + '" loading="' + (i ? 'lazy' : 'eager') + '" alt="' + escape(deck.title) + ' · 第 ' + (i+1) + ' 页"><figcaption>' + (i+1) + ' / ' + deck.pageCount + '</figcaption></figure>').join('') + '<div class="preview-end">已展示全部 ' + deck.pageCount + ' 页' + download(deck, '', '下载 PPTX，编辑与使用完整内容 →') + '</div></section><aside class="info-panel"><p class="eyebrow">ABOUT THIS PRESENTATION</p><h2>' + escape(deck.title) + '</h2><dl><div><dt>资源分类</dt><dd>' + escape(deck.category) + '</dd></div><div><dt>文件格式</dt><dd>PowerPoint · PPTX</dd></div><div><dt>页面数量</dt><dd>' + deck.pageCount + ' 页</dd></div><div><dt>文件大小</dt><dd>' + size(deck.size) + '</dd></div></dl>' + download(deck, 'primary-download', '↓ 下载 PPT 原文件') + '<p>滚动查看完整内容，或点击左侧缩略图跳转。支持 ← → 方向键翻页。<br><br>在线预览为静态页面，动画、音视频请下载后查看。' + (deck.title === 'PPT 复刻案例' ? '<br><br>此下载版压缩了内嵌图片，幻灯片数量、文字和版式保持不变。' : '') + '</p></aside></div>';
    document.querySelectorAll('[data-page]').forEach(el => {
      if (el.tagName === 'A') el.onclick = e => { e.preventDefault(); selectPage(el.dataset.page, true); };
    });
    $('prevPage').onclick = () => selectPage(currentPage - 1, true);
    $('nextPage').onclick = () => selectPage(currentPage + 1, true);
    $('pageNumber').onchange = e => selectPage(e.target.value, true);
    $('fullscreen').onclick = async () => {
      try {
        if (document.fullscreenElement) await document.exitFullscreen();
        else await $('previewBody').requestFullscreen();
      } catch (_) { $('fullscreen').textContent = '浏览器不支持全屏'; }
    };
    document.querySelectorAll('.slide-page img').forEach(img => img.addEventListener('error', () => {
      const caption = img.parentElement.querySelector('figcaption');
      caption.textContent = '本页加载失败，请刷新重试。'; caption.setAttribute('role', 'status');
    }));
    selectPage(1, false);
    window.scrollTo(0, 0);
    observer = new IntersectionObserver(entries => {
      const visible = [...document.querySelectorAll('.slide-page')].map(el => {
        const rect = el.getBoundingClientRect();
        return {el, visible: Math.max(0, Math.min(rect.bottom, innerHeight) - Math.max(rect.top, 75))};
      }).sort((a,b) => b.visible - a.visible);
      if (visible.length && visible[0].visible > 0) selectPage(visible[0].el.dataset.page, false);
    }, {rootMargin:'-75px 0px 0px 0px', threshold:[0, .1, .25, .5, .75, 1]});
    document.querySelectorAll('.slide-page').forEach(el => observer.observe(el));
  }
  $('search').oninput = e => { query = e.target.value.trim().toLocaleLowerCase(); renderCards(); };
  window.addEventListener('hashchange', route);
  document.addEventListener('fullscreenchange', () => {
    const body = $('previewBody');
    if (body) body.classList.toggle('reader-fullscreen', document.fullscreenElement === body);
    if ($('fullscreen')) $('fullscreen').textContent = document.fullscreenElement ? '退出全屏' : '全屏查看';
  });
  document.addEventListener('keydown', e => {
    if ($('detail').hidden || /INPUT|TEXTAREA|SELECT|BUTTON|A/.test(e.target.tagName) || e.altKey || e.ctrlKey || e.metaKey) return;
    if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { e.preventDefault(); selectPage(currentPage + (e.key === 'ArrowRight' ? 1 : -1), true); }
  });
  fetch(base + 'manifest.json').then(r => { if (!r.ok) throw new Error('目录加载失败'); return r.json(); }).then(data => {
    decks = data.decks;
    $('deckCount').textContent = decks.length;
    ['全部', ...new Set(decks.map(d => d.category))].forEach(label => {
      const button = document.createElement('button'); button.textContent = label; button.setAttribute('aria-pressed', String(label === category));
      button.onclick = () => { category = label; $('filters').querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', String(b === button))); renderCards(); };
      $('filters').append(button);
    });
    route();
  }).catch(() => { $('grid').innerHTML = '<p class="empty" role="alert">PPT 资源加载失败，请刷新页面重试。</p>'; });
}());
