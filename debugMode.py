from playwright.async_api import async_playwright
import asyncio
from datetime import datetime

async def main():
    # Connect to existing browser using CDP
    async with async_playwright() as playwright:
        browser = await playwright.chromium.connect_over_cdp("http://localhost:9222")
        
        try:
            # Get the first context or create one if none exists
            if len(browser.contexts) > 0:
                context = browser.contexts[0]
            else:
                context = await browser.new_context()
            
            page = await context.new_page()
            
            print('Navigating to Discord...')
            await page.goto('https://discord.com')
            
            title = await page.title()
            print('Page title:', title)
            
            # Click at coordinates x=1190, y=66 in the viewport
            await page.mouse.click(1190, 66)
            
            input("Click performed at (1190, 66). Press Enter to exit...")
            
            # Close the browser when done
            await browser.close()
            
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
