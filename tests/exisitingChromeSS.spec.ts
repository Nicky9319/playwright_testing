import { test, expect, chromium, Browser } from '@playwright/test';
import readline from 'readline';

let browser: Browser;

test.beforeAll(async () => {
    browser = await chromium.connectOverCDP('http://localhost:9222');
});

test.afterAll(async () => {
    if (browser) {
        await browser.close();
    }
})

test('Open Discord with existing Chrome profile and take screenshot', async ({}) => {
    const context = browser.contexts()[0];
    const page = await context.newPage();

    console.log('Navigating to Discord...');
    await page.goto('https://discord.com');
    
    const title = await page.title();
    console.log('Page title:', title);
    
    // Take a screenshot and save it
    console.log('Taking screenshot...');
    await page.screenshot({ path: 'discord-screenshot.png' });
    console.log('Screenshot saved as discord-screenshot.png');
    
    // Create readline interface for terminal input
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });
    
    // Wait for user input before continuing
    await new Promise<void>(resolve => {
        rl.question('Press Enter to continue and close the browser...', () => {
            rl.close();
            resolve();
        });
    });
    
    console.log('Continuing after user input');
});