import { test, expect, chromium, Browser } from '@playwright/test';
import readline from 'readline';

let browser: Browser;

test.beforeAll(async () => {
    browser = await chromium.connectOverCDP('http://localhost:9222');
});

test.afterAll(async () => {
    // Don't automatically close browser after test
    console.log('Test complete. Browser will remain open.');
})

test('Control existing Chrome browser session', async ({}) => {
    const context = browser.contexts()[0];
    const page = await context.newPage();

    console.log('Navigating to Discord...');
    await page.goto('https://discord.com');
    
    const title = await page.title();
    console.log('Page title:', title);
    
    // Interactive control loop
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });
    
    // A simple command handler
    const handleCommand = async (command: string): Promise<boolean> => {
        command = command.trim().toLowerCase();
        
        if (command === 'exit' || command === 'quit') {
            return false;
        } else if (command === 'screenshot') {
            await page.screenshot({ path: `screenshot-${Date.now()}.png` });
            console.log(`Screenshot taken at ${new Date().toLocaleTimeString()}`);
        } else if (command.startsWith('goto ')) {
            const url = command.substring(5);
            console.log(`Navigating to ${url}...`);
            await page.goto(url.startsWith('http') ? url : `https://${url}`);
            console.log(`Current page: ${await page.title()}`);
        } else if (command === 'title') {
            console.log(`Current page title: ${await page.title()}`);
        } else if (command === 'help') {
            console.log(`
Available commands:
- goto [url]: Navigate to the specified URL
- screenshot: Take a screenshot
- title: Show current page title
- help: Show this help message
- exit/quit: End the session
            `);
        } else {
            console.log('Unknown command. Type "help" to see available commands.');
        }
        
        return true;
    };
    
    console.log('\nBrowser control session started. Type "help" for available commands.');
    
    // Command loop
    let continueRunning = true;
    while (continueRunning) {
        const command = await new Promise<string>(resolve => {
            rl.question('> ', (answer) => {
                resolve(answer);
            });
        });
        
        continueRunning = await handleCommand(command);
    }
    
    rl.close();
    console.log('Browser control session ended.');
});