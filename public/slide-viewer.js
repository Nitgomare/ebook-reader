(function () {
  'use strict';
  var params = new URLSearchParams(location.search);
  var book = params.get('book') || 'robot-technology-basics';
  if (!/^[a-z0-9-]+$/.test(book)) book = 'robot-technology-basics';
  var base = 'slides/' + book + '/', decks = [], active, page = 1;
  var byId = function (id) { return document.getElementById(id); };
  function imageUrl(n) { return base + active.id + '/' + String(n).padStart(4, '0') + '.webp'; }
  function show(n) {
    if (!active) return;
    page = Math.max(1, Math.min(active.pageCount, Math.trunc(Number(n)) || 1));
    byId('slide').src = imageUrl(page);
    byId('slide').alt = active.title + ' · 第' + page + '页';
    byId('page').value = page;
    byId('prev').disabled = page === 1;
    byId('next').disabled = page === active.pageCount;
    byId('status').textContent = '第 ' + page + ' / ' + active.pageCount + ' 页';
    document.querySelectorAll('#thumbs button').forEach(function (b, i) { b.setAttribute('aria-current', String(i + 1 === page)); });
    var url = new URL(location.href); url.searchParams.set('deck', active.id); url.searchParams.set('page', page); history.replaceState(null, '', url);
  }
  function select(id, n) {
    active = decks.find(function (d) { return d.id === id; });
    if (!active) throw new Error('找不到该课件版本，请从课程目录重新打开。');
    byId('deck').value = active.id;
    byId('topic').textContent = active.topic + ' · ' + active.variant + ' · ' + active.sources[0];
    byId('total').textContent = active.pageCount; byId('page').max = active.pageCount;
    document.title = active.title + ' · 在线课件';
    byId('thumbs').replaceChildren();
    for (var i = 1; i <= active.pageCount; i++) {
      var button = document.createElement('button'), img = document.createElement('img');
      img.loading = 'lazy'; img.src = imageUrl(i); img.alt = '第' + i + '页';
      button.append(img, document.createTextNode(String(i))); button.dataset.page = i;
      button.addEventListener('click', function (event) { show(event.currentTarget.dataset.page); });
      byId('thumbs').append(button);
    }
    show(n);
  }
  byId('prev').onclick = function () { show(page - 1); };
  byId('next').onclick = function () { show(page + 1); };
  byId('page').onchange = function () { show(this.value); };
  byId('deck').onchange = function () { select(this.value, 1); };
  byId('full').onclick = async function () { try { if (document.fullscreenElement) await document.exitFullscreen(); else await byId('stage').requestFullscreen(); } catch (_) { byId('status').textContent = '当前浏览器不支持全屏，可使用浏览器缩放查看。'; } };
  byId('slide').onerror = function () { byId('status').textContent = '本页加载失败，请刷新后重试。'; };
  document.addEventListener('keydown', function (event) {
    if (!active || /INPUT|SELECT|TEXTAREA/.test(event.target.tagName)) return;
    var target = {ArrowLeft:page-1,ArrowRight:page+1,Home:1,End:active.pageCount}[event.key];
    if (target !== undefined) { event.preventDefault(); show(target); }
  });
  fetch(base + 'manifest.json').then(function (r) { if (!r.ok) throw new Error('课件目录加载失败'); return r.json(); }).then(function (manifest) {
    decks = manifest.decks;
    document.querySelector('header a').href = 'index.html#/resources/' + book;
    document.querySelector('header h1').textContent = manifest.title;
    byId('notice').textContent = '使用左右方向键翻页，Home / End 跳至首页 / 末页。静态幻灯片保留原版式；动画和嵌入音视频不播放。';
    decks.forEach(function (d) { var option = document.createElement('option'); option.value = d.id; option.textContent = d.title + ' · ' + d.variant + ' · ' + d.pageCount + '页'; byId('deck').append(option); });
    var params = new URLSearchParams(location.search); select(params.get('deck') || decks[0].id, params.get('page'));
  }).catch(function (error) { byId('status').textContent = error.message; });
}());
