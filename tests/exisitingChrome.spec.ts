import { test, expect, chromium, Browser } from '@playwright/test';

let browser: Browser;

test.beforeAll(async () => {
    browser = await chromium.connectOverCDP('http://localhost:9222');
});

test.afterAll(async () => {
    if (browser) {
        await browser.close();
    }
})

test('Open Gmail with existing Chrome profile', async ({}) => {
    const context = browser.contexts()[0];
    const page = await context.newPage();

    const title = await page.title();
    console.log('Page title:', title);

    await page.goto('https://gmail.com');

})