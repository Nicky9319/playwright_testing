import asyncio
import time
from playwright.async_api import async_playwright

# USER_DATA_DIR = "/home/paarth/.config/google-chrome/"
USER_DATA_DIR = "/home/paarth/chrome-debug-profile/"

print("working...")


async def main():
    async with async_playwright() as p:
        browser = None
        current_url = None
        
        try:
            print("Phase 1: Launching headless browser...")
            
            # Phase 1: Headless mode - go to YouTube and do search
            browser = await p.chromium.launch_persistent_context(
                user_data_dir=USER_DATA_DIR,
                headless=True,  # Headless mode
                executable_path='/opt/google/chrome/google-chrome',
            )
            
            print(f"Using User Data Directory: {USER_DATA_DIR}")
            page = await browser.new_page()
            
            print("Going to YouTube in headless mode...")
            await page.goto("https://youtube.com")
            await page.wait_for_load_state('networkidle')
            print("YouTube page loaded successfully in headless mode")
            
            # Do a search in headless mode to demonstrate state preservation
            print("Performing search in headless mode...")
            await page.fill('input[name="search_query"]', "python tutorial")
            await page.press('input[name="search_query"]', 'Enter')
            await page.wait_for_load_state('networkidle')
            
            # Save the current URL (this preserves the search results page)
            current_url = page.url
            print(f"Current URL after search: {current_url}")
            
            # Close the headless browser (all state is preserved in user_data_dir)
            await browser.close()
            print("Headless browser closed - URL and state preserved")
            
            print("\nPhase 2: Launching headful browser with preserved page state...")
            
            # Phase 2: Headful mode - navigate to exact same URL
            browser = await p.chromium.launch_persistent_context(
                user_data_dir=USER_DATA_DIR,  # Same directory = complete state preservation
                headless=False,  # Headful mode
                executable_path='/opt/google/chrome/google-chrome',
            )
            
            print("Browser opened in headful mode with preserved context")
            page = await browser.new_page()
            
            # Navigate to the exact same URL (search results page)
            print(f"Navigating to preserved URL: {current_url}")
            await page.goto(current_url)
            await page.wait_for_load_state('networkidle')
            
            print("YouTube search results loaded in headful mode!")
            print("You have 30 secs to interact with the search results page.")
            print("The browser will automatically close after 30 secs.")
            print("Notice: You're on the same search results page, not the homepage!")
            
            # Wait for 30 seconds for user interaction
            await asyncio.sleep(30)
            
            # Get the final URL after user interaction
            final_url = page.url
            print(f"Final URL after user interaction: {final_url}")
            
            # Close the headful browser (state automatically saved to user_data_dir)
            await browser.close()
            print("Headful browser closed - all interactions saved to user data directory")
            
            print("\nPhase 3: Taking screenshot in headless mode with preserved page state...")
            
            # Phase 3: Headless mode - navigate to final URL
            browser = await p.chromium.launch_persistent_context(
                user_data_dir=USER_DATA_DIR,  # Same directory = all changes preserved
                headless=True,  # Back to headless mode
                executable_path='/opt/google/chrome/google-chrome',
            )
            
            print("Browser opened in headless mode with all previous interactions preserved")
            page = await browser.new_page()
            
            # Navigate to the final URL (preserving any navigation user did)
            print(f"Navigating to final URL: {final_url}")
            await page.goto(final_url)
            await page.wait_for_load_state('networkidle')
            
            # Take screenshot showing the preserved page state
            await page.screenshot(path="context_check.png")
            print("Screenshot saved as context_check.png")
            print("The screenshot should show the exact page you were on after your interactions!")
            
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if browser is not None:
                await browser.close()
            print("Browser closed.")


if __name__ == "__main__":
    asyncio.run(main())
