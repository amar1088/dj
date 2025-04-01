from playwright.sync_api import sync_playwright
import json
import time

# Load configuration
with open("config.json", "r") as f:
    config = json.load(f)

email = config["email"]
password = config["password"]
receiver_id = config["receiver_id"]
message_file = config["message_file"]
delay_time = config["delay_time"]

def send_messages():
    with sync_playwright() as p:
        # Launch Google Chrome with a persistent session
        browser = p.chromium.launch_persistent_context(
            user_data_dir="chrome_data",  # Saves session for next use
            channel="chrome",  # Uses Google Chrome
            headless=True  # Run Chrome in headless mode (no GUI)
        )

        page = browser.new_page()

        # Go to Messenger login page
        page.goto("https://www.messenger.com/")

        # Log in
        page.fill("input[name='email']", email)
        page.fill("input[name='pass']", password)
        
        # Click login button (Ensure correct selector)
        page.click("button[type='submit']")
        time.sleep(10)  # Wait for login to complete

        # Go to receiver's chat
        page.goto(f"https://www.messenger.com/t/{receiver_id}")
        time.sleep(5)

        # Handle "End-to-End Encrypted Chat" prompt
        try:
            if page.is_visible("text=Continue"):
                page.click("text=Continue")
                time.sleep(3)
                print("✅ Clicked on 'Continue'")
        except:
            print("✅ No 'Continue' button found, proceeding...")

        # Read messages from file
        with open(message_file, "r") as f:
            messages = f.readlines()

        # Send messages in a loop
        while True:
            for msg in messages:
                page.fill("div[role='textbox']", msg.strip())
                page.keyboard.press("Enter")
                print(f"📩 Sent: {msg.strip()}")
                time.sleep(delay_time)

send_messages()
