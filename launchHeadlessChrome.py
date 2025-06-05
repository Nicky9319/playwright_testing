import subprocess
import sys
import time
import signal
import os

def main():
    print("Launching headless Chrome with remote debugging enabled...")
    
    # Create the directory if it doesn't exist
    os.makedirs('/tmp/chrome-debug-profile', exist_ok=True)
    
    # Command to launch Chrome in headless mode with remote debugging
    chrome_cmd = [
        '/opt/google/chrome/google-chrome',  # Adjust path as needed
        '--headless',                        # Run in headless mode
        '--remote-debugging-port=9222',      # Enable remote debugging on port 9222
        '--user-data-dir=/tmp/chrome-debug-profile',  # User profile directory
        '--disable-gpu',                     # Disable GPU acceleration (often needed for headless)
        '--no-sandbox',                      # Run without sandbox (may be needed in some environments)
        '--disable-dev-shm-usage'            # Overcome limited /dev/shm in certain environments
    ]
    
    try:
        # Start Chrome process
        chrome_process = subprocess.Popen(chrome_cmd)
        print("Headless Chrome launched with debugging port 9222")
        print("You can now connect to this browser with your scripts")
        print("Press Ctrl+C to stop the browser")
        
        # Keep the script running until interrupted
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nShutting down browser...")
    finally:
        # Make sure to properly terminate Chrome
        if 'chrome_process' in locals():
            chrome_process.terminate()
            try:
                chrome_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                chrome_process.kill()
        print("Browser closed")

if __name__ == "__main__":
    main()
