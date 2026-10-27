const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');

(async () => {
  const catalog = JSON.parse(fs.readFileSync('dist/data/catalog.json', 'utf8'));
  const slug = 'solidworks-robot-modeling';
  const book = catalog.books.find(b => b.slug === slug);
  const docs = catalog.docs.filter(d => d.bookSlug === slug);
  if (!book || book.category !== 'robotics' || docs.length !== 9) throw new Error('Course registration mismatch');
  const home = docs.find(d => d.relPath === book.homePage);
  if (!home || docs[0].id !== home.id) throw new Error('Authored homepage missing or misplaced');
  const chapters = docs.filter(d => d.chapterNumber);
  if (JSON.stringify(chapters.map(d => d.chapterNumber)) !== '[1,2,3,4,5,6,7,8]') throw new Error('Chapter order mismatch');
  const out = path.resolve('tmp/solidworks-qa');
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: true });
  const reports = [], errors = [];
  try {
    for (const width of [1440, 390]) {
      const page = await browser.newPage({ viewport: { width, height: 1000 } });
      page.on('pageerror', e => errors.push(e.message));
      await page.goto(`http://127.0.0.1:8023/#/resources/${slug}`, { waitUntil: 'networkidle' });
      const primary = page.locator('.resource-book-info a');
      if (await primary.getAttribute('href') !== '#/doc/' + home.id) throw new Error('Homepage shortcut mismatch');
      if (await page.locator('.resource-table tbody tr').first().locator('a').getAttribute('href') !== '#/doc/' + home.id) throw new Error('Homepage is not the first resource');
      await primary.click();
      await page.waitForFunction(() => document.querySelector('#article')?.textContent.includes('几何建模'));
      for (const doc of docs) {
        await page.goto(`http://127.0.0.1:8023/?qa=${width}-${doc.id}#/doc/${doc.id}`, { waitUntil: 'networkidle' });
        await page.waitForFunction(() => document.querySelector('#article')?.textContent.length > 100);
        await page.waitForTimeout(250);
        const state = await page.evaluate(() => ({
          overflow: document.documentElement.scrollWidth > innerWidth + 2,
          brokenImages: [...document.querySelectorAll('#article img')].filter(i => !i.complete || !i.naturalWidth).map(i => i.src),
          imageCount: document.querySelectorAll('#article img').length,
          documentLinks: [...document.querySelectorAll('#article a[href^="#/doc/"]')].map(a => a.getAttribute('href')),
          videos: [...document.querySelectorAll('#article a[href*="bilibili.com/video/"]')].map(a => a.href),
          badLinks: [...document.querySelectorAll('#article a')].filter(a => /\.md(?:$|#)/.test(a.getAttribute('href') || '')).map(a => a.href),
        }));
        reports.push({ width, chapter: doc.relPath, ...state });
        if (state.overflow || state.brokenImages.length || state.badLinks.length) errors.push(`${width}/${doc.relPath}: layout or links failed`);
        if (doc.id === home.id && !chapters.every(c => state.documentLinks.includes('#/doc/' + c.id))) errors.push('Homepage chapter links missing');
        if (doc.chapterNumber === 7 && (state.videos.length !== 14 || new Set(state.videos).size !== 14)) errors.push('Video chapters missing');
        if (!doc.chapterNumber || [2, 7, 8].includes(doc.chapterNumber)) await page.screenshot({ path: path.join(out, `${doc.chapterNumber || 'home'}-${width}.png`) });
        console.log(JSON.stringify(reports.at(-1)));
      }
      await page.close();
    }
  } finally { await browser.close(); }
  fs.writeFileSync(path.join(out, 'report.json'), JSON.stringify({ reports, errors }, null, 2));
  if (errors.length) throw new Error(errors.join('\n'));
  console.log('PASS: homepage, eight chapter links, images, 14 video links, and desktop/mobile layouts.');
})().catch(e => { console.error(e); process.exitCode = 1; });
