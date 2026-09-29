/* 机器人课程资源中心 · 交互
   只做两件事：顶部进度条；目录/页内导航跟随滚动高亮。
   无依赖，离线可用。 */
(function () {
  'use strict';

  var bar = document.getElementById('progress');
  function tick() {
    if (!bar) return;
    var max = document.documentElement.scrollHeight - window.innerHeight;
    bar.style.width = (max > 0 ? (window.scrollY / max) * 100 : 0) + '%';
  }

  var links = Array.prototype.slice.call(document.querySelectorAll('[data-spy]'));
  var targets = links.map(function (a) {
    return document.querySelector(a.getAttribute('href'));
  });

  var queued = false;
  function spy() {
    queued = false;
    if (!links.length) return;
    var active = links[0].getAttribute('href');
    targets.forEach(function (t, i) {
      if (t && t.getBoundingClientRect().top <= 150) active = links[i].getAttribute('href');
    });
    links.forEach(function (a) {
      a.classList.toggle('active', a.getAttribute('href') === active);
    });
  }

  function onScroll() {
    tick();
    if (!queued) {
      queued = true;
      window.requestAnimationFrame(spy);
    }
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', function () { tick(); spy(); });
  tick();
  spy();
}());
