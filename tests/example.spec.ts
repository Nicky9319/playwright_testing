import { test, expect, chromium} from '@playwright/test';

// const userDataDir: string = 
// "/home/donna/.config/google-chrome/";


const userDataDir: string =
"/opt/google/chrome/google-chrome";

test("Launch chrom wirh ue fproile " , async ({}) => {
  try{
    const browserContext = await chromium.launchPersistentContext(userDataDir, {
      viewport: { width: 800, height: 600 },
      headless: false,
      channel: 'chrome',
      executablePath: '/opt/google/chrome/google-chrome',
    });
    console.log("Using User Data Directory: ", userDataDir);
    const page = await browserContext.newPage();
    await page.goto('https://gmail.com');
    await page.pause();
  }
  catch (error) {
    console.error("Error launching browser with user profile:", error);
  } finally {
    // Cleanup if necessary
    // await browserContext.close();
  }
})
