from playwright.async_api import async_playwright
import asyncio
import threading
import queue
from datetime import datetime
import time

# Shared command queue
command_queue = queue.Queue()

# Flag to signal threads to stop
stop_flag = threading.Event()

# Define command handler functions
async def handle_browser_commands(browser, page):
    while not stop_flag.is_set():
        try:
            # Check if there are commands in the queue
            if not command_queue.empty():
                command = command_queue.get()
                
                # Process commands
                if command == "discord":
                    print("Navigating to Discord...")
                    await page.goto('https://gmail.com')
                    print(f"Current page: {await page.title()}")
                
                elif command == "ss" or command == "screenshot":
                    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                    path = f"screenshot-{timestamp}.png"
                    await page.screenshot(path=path)
                    print(f"Screenshot saved as {path}")
                
                elif command == "exit" or command == "quit":
                    print("Exiting...")
                    stop_flag.set()
                
                elif command.startswith("goto "):
                    url = command[5:]
                    if not url.startswith("http"):
                        url = f"https://{url}"
                    print(f"Navigating to {url}...")
                    await page.goto(url)
                    print(f"Current page: {await page.title()}")
                
                else:
                    print(f"Unknown command: {command}")
            
            # Small delay to prevent CPU overuse
            await asyncio.sleep(0.1)
            
        except Exception as e:
            print(f"Error processing command: {e}")
    
    print("Browser command handler stopped")

# Thread for command input
def command_listener():
    print("Command listener started. Type 'help' for available commands.")
    print("Available commands:")
    print("  discord - Navigate to Discord website")
    print("  ss/screenshot - Take a screenshot")
    print("  goto [url] - Navigate to specified URL")
    print("  exit/quit - Exit the program")
    
    while not stop_flag.is_set():
        try:
            command = input("> ").strip().lower()
            command_queue.put(command)
            
            if command in ["exit", "quit"]:
                break
        except (EOFError, KeyboardInterrupt):
            print("\nDetected keyboard interrupt, exiting...")
            stop_flag.set()
            break
    
    print("Command listener stopped")

# Browser control coroutine
async def browser_control():
    try:
        async with async_playwright() as playwright:
            # Launch headless browser if not connecting to existing one
            # Option 1: Connect to an existing browser in debug mode
            try:
                browser = await playwright.chromium.connect_over_cdp("http://localhost:9222")
                print("Connected to existing Chrome instance")
            except Exception as e:
                print(f"Could not connect to existing browser: {e}")
                print("Launching new headless browser instance...")
                browser = await playwright.chromium.launch(
                    headless=True,
                    args=['--remote-debugging-port=9222']
                )
                print("Launched new headless browser instance")
            
            # Get or create a context
            if len(browser.contexts) > 0:
                context = browser.contexts[0]
            else:
                context = await browser.new_context()
                
            # Create a new page
            page = await context.new_page()
            print("Browser connection established")
            
            # Start command handler
            await handle_browser_commands(browser, page)
            
            # Clean up
            await browser.close()
            print("Browser closed")
            
    except Exception as e:
        print(f"Browser control error: {e}")
        stop_flag.set()

# Main function
async def main():
    # Start command listener thread
    listener_thread = threading.Thread(target=command_listener)
    listener_thread.daemon = True
    listener_thread.start()
    
    # Run the browser control in the main thread
    await browser_control()
    
    # Wait for listener thread to finish
    stop_flag.set()
    if listener_thread.is_alive():
        listener_thread.join(timeout=2)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
        stop_flag.set()
