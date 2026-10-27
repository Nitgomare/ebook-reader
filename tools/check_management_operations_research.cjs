const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');

(async () => {
  const root = path.resolve(process.argv[2] || 'dist');
  const catalog = JSON.parse(fs.readFileSync(path.join(root, 'data/catalog.json'), 'utf8'));
  const slug = 'management-operations-research';
  const book = catalog.books.find(item => item.slug === slug);
  const docs = catalog.docs.filter(item => item.bookSlug === slug);
  if (!book || book.category !== 'management-science' || book.contentProvider !== '周芸丽' || docs.length !== 20) throw new Error('Book registration mismatch');
  const numbers = docs.filter(item => item.chapterNumber != null).map(item => item.chapterNumber);
  if (JSON.stringify(numbers) !== '[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]') throw new Error('Chapter order mismatch');
  const browser = await chromium.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: true });
  const reports = [], errors = [];
  const shots = path.resolve('tmp/management-or-qa');
  fs.mkdirSync(shots, { recursive: true });
  try {
    for (const width of [1440, 390]) {
      const page = await browser.newPage({ viewport: { width, height: 1000 } });
      page.on('pageerror', error => errors.push(error.message));
      await page.goto(`http://127.0.0.1:8022/#/resources/${slug}`, { waitUntil: 'networkidle' });
      await page.waitForFunction(() => document.querySelector('.resource-table'));
      const resource = await page.evaluate(() => ({
        title: document.querySelector('.resource-book-info')?.textContent,
        links: document.querySelectorAll('.resource-table a[href^="#/doc/"]').length,
        overflow: document.documentElement.scrollWidth > innerWidth + 2,
      }));
      if (resource.links !== 20 || resource.overflow) errors.push(`${width} resource page: ${JSON.stringify(resource)}`);
      await page.screenshot({ path: path.join(shots, `resources-${width}.png`) });
      const targets = width === 1440 ? docs : docs.filter(item => item.chapterNumber === 1 || item.chapterNumber === 17 || item.chapterNumber === 2 || item.relPath.includes("appendices"));
      for (const doc of targets) {
        await page.goto(`http://127.0.0.1:8022/?qa=${doc.id}-${width}#/doc/${doc.id}`, { waitUntil: 'networkidle' });
        await page.waitForFunction(() => document.querySelector('#article')?.textContent.length > 100);
        await page.evaluate(async () => { if (window.MathJax?.startup?.promise) await window.MathJax.startup.promise; });
        await page.waitForTimeout(700);
        const state = await page.evaluate(() => ({
          overflow: document.documentElement.scrollWidth > innerWidth + 2,
          brokenImages: [...document.querySelectorAll('#article img')].filter(img => img.complete && !img.naturalWidth).length,
          formulaCount: document.querySelectorAll('#article .arithmatex').length,
          renderedMath: document.querySelectorAll('#article mjx-container').length,
          mathErrors: [...document.querySelectorAll('#article mjx-merror')].map(el => ({ error: el.getAttribute('data-mjx-error'), text: el.closest('.arithmatex')?.textContent.slice(0, 260) })),
          rawTableMath: [...document.querySelectorAll('#article td')].filter(el => /\$[^$]+\$/.test(el.textContent)).length,
          captions: document.querySelectorAll('#article .figure-caption').length,
          centered: [...document.querySelectorAll('#article .figure-caption')].every(el => getComputedStyle(el).textAlign === 'center'),
        }));
        reports.push({ width, chapter: doc.relPath, ...state });
        if (state.overflow || state.brokenImages || !state.centered || state.mathErrors.length || state.rawTableMath || (state.formulaCount && !state.renderedMath)) errors.push(`${width}/${doc.relPath}: layout or render failed`);
        console.log(JSON.stringify(reports.at(-1)));
        if ([2, 17].includes(doc.chapterNumber)) {
          await page.screenshot({ path: path.join(shots, `chapter-${doc.chapterNumber}-${width}.png`) });
        }
        if (doc.chapterNumber === 2) {
          const math = page.locator('#article .arithmatex').first();
          if (await math.count()) {
            await math.scrollIntoViewIfNeeded();
            await page.screenshot({ path: path.join(shots, `math-${width}.png`) });
          }
        }
      }
      await page.close();
    }
  } finally { await browser.close(); }
  fs.writeFileSync(path.join(shots, 'report.json'), JSON.stringify({ reports, errors }, null, 2));
  if (errors.length) throw new Error(errors.join('\n'));
  console.log('PASS: book registration, chapter order, resource links, images, captions, and desktop/mobile layout.');
})().catch(error => { console.error(error); process.exitCode = 1; });
