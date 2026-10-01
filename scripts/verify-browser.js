async (page) => {
  const results = [];
  for (const [width, height] of [[1440,1000],[360,800],[390,844],[430,932]]) {
    await page.setViewportSize({width,height});
    await page.goto('http://localhost:3013/');
    for (const image of await page.locator('img').all()) {
      await image.scrollIntoViewIfNeeded();
      await image.evaluate(async image => { await image.decode(); });
    }
    await page.locator('#inicio').scrollIntoViewIfNeeded();
    await page.screenshot({path:`output/playwright/preview-${width}.png`,fullPage:true});
    results.push(await page.evaluate(() => ({
      width: innerWidth,
      overflow: document.documentElement.scrollWidth > innerWidth,
      brokenImages: [...document.images].filter(i=>!i.complete || !i.naturalWidth).map(i=>i.src),
      h1: document.querySelectorAll('h1').length,
      contactUrls: [...document.querySelectorAll('a[href*="wa.me"]')].map(a=>a.href),
      missingAnchors: [...document.querySelectorAll('a[href^="#"]')].filter(a=>!document.querySelector(a.getAttribute('href'))).map(a=>a.href),
    })));
  }
  await page.getByRole('button',{name:'Abrir menu'}).click();
  results.push({menuOpened: await page.locator('#mobile-nav').isVisible()});
  await page.keyboard.press('Escape');
  results.push({menuClosed: !(await page.locator('#mobile-nav').isVisible()),focusReturned: await page.getByRole('button',{name:'Abrir menu'}).evaluate(e=>e===document.activeElement)});
  await page.getByRole('button',{name:'Abrir menu'}).click();
  await page.locator('#mobile-nav').getByRole('link',{name:'Serviços'}).click();
  results.push({anchor:page.url(),menuClosedAfterLink:!(await page.locator('#mobile-nav').isVisible())});
  await page.emulateMedia({reducedMotion:'reduce'});
  await page.goto('http://localhost:3013/');
  // movimento reduzido: sem vídeo, pôster do aparelho instalado
  results.push({videoCount:await page.locator('video').count(),poster:await page.locator('.scene-poster img').evaluate(i=>i.currentSrc.split('/').pop())});
  await page.screenshot({path:'output/playwright/hero-mobile-390.png'});
  await page.setViewportSize({width:1440,height:1000});
  await page.screenshot({path:'output/playwright/hero-desktop-1440.png'});
  return results;
}
