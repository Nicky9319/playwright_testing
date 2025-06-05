import asyncio
from playwright.async_api import async_playwright

USER_DATA_DIR = "/home/paarth/.config/google-chrome/"
USER_DATA_DIR = "/tmp/chrome-debug-profile/"

print("working...")


async def main():
    async with async_playwright() as p:
        browser = None
        try:
            print("Launching browser...")

            browser = await p.chromium.launch_persistent_context(
                user_data_dir=USER_DATA_DIR,
                headless=False,
                executable_path='/opt/google/chrome/google-chrome',
            )
            # context = await browser.new_context()
            # page = await context.new_page()
            print(f"Using User Data Directory: {USER_DATA_DIR}")
            page = await browser.new_page()
            await page.goto("https://gmail.com")
            await page.screenshot(path="gmail_screenshot.png")
            print("Screenshot saved as gmail_screenshot.png")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            input("Press Enter to close the browser...")
            if browser is not None:
                browser.close()
            print("Browser closed.")




if __name__ == "__main__":
    asyncio.run(main())
