const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');

(async () => {
  const browser = await chromium.launch({
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
    headless: true,
  });
  const output = path.resolve('tmp/robot-hub-acceptance');
  fs.mkdirSync(output, { recursive: true });
  const errors = [];
  const pages = ['index.html', 'ros-mobile.html', 'go2.html', 'vision-sorting.html', 'abb-baxter.html'];
  for (const width of [1440, 390]) {
    const context = await browser.newContext({ viewport: { width, height: 900 } });
    const page = await context.newPage();
    page.on('pageerror', error => errors.push(error.message));
    for (const file of pages) {
      await page.goto(`http://127.0.0.1:8015/robot-hub/${file}`, { waitUntil: 'networkidle' });
      const state = await page.evaluate(() => ({
        overflow: document.documentElement.scrollWidth > innerWidth + 2,
        heading: document.querySelector('h1')?.textContent.trim(),
        backLink: !!document.querySelector('a[href="../#/"]'),
        media: document.querySelectorAll('video, audio, iframe').length,
        maintenancePanels: document.querySelectorAll('#overview, #notes, .fact-grid').length,
        releaseBanner: document.body.textContent.includes('线上发布版说明'),
      }));
      if (state.overflow || !state.heading || !state.backLink || state.media || state.maintenancePanels || state.releaseBanner) {
        errors.push(`${width}/${file}: ${JSON.stringify(state)}`);
      }
      if (file === 'index.html' && await page.locator('.track-card').count() !== 4) errors.push('Expected four course cards');
      if (file === 'vision-sorting.html') {
        const text = await page.locator('main').innerText();
        for (const keyword of ['加密狗', 'SOFTWARE', '高度']) {
          if (!text.includes(keyword)) errors.push(`Missing reader constraint: ${keyword}`);
        }
      }
      if (file === 'go2.html' && !await page.getByRole('link', { name: '《智能机器人综合应用》实训大纲' }).count()) errors.push('Missing Go2 outline');
      await page.screenshot({ path: path.join(output, `${width}-${file}.png`) });
      const anchor = page.locator('[data-spy]').first();
      if (await anchor.count()) {
        const id = await anchor.getAttribute('href');
        await anchor.click();
        await page.waitForTimeout(600);
        const top = await page.locator(id).evaluate(el => el.getBoundingClientRect().top);
        const header = await page.locator('.topbar').evaluate(el => el.getBoundingClientRect().bottom);
        if (top + 2 < header) errors.push(`${width}/${file}: heading hidden by header (${top}/${header})`);
      }
      console.log(`${width}/${file}: ${JSON.stringify(state)}`);
    }
    await page.goto('http://127.0.0.1:8015/', { waitUntil: 'networkidle' });
    const card = page.locator('#category-robotics').locator('..').locator('..').locator('..').locator('a[href="robot-hub/"]');
    if (!await card.count()) errors.push(`${width}: missing robotics card`);
    if (!await page.locator('.top-links a[href="robot-hub/"]').count()) errors.push(`${width}: missing top navigation`);
    await page.screenshot({ path: path.join(output, `${width}-learning-center.png`) });
    await context.close();
  }
  await browser.close();
  if (errors.length) throw new Error(errors.join('\n'));
  console.log('PASS: desktop/mobile pages, navigation, anchors, overflow, and JavaScript.');
})().catch(error => { console.error(error); process.exitCode = 1; });
