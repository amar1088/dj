from playwright.sync_api import sync_playwright
import json
import time

# Load configuration
with open("config.json", "r") as f:
    config = json.load(f)

# Load session cookies
with open(config["cookie_file"], "r") as f:
    cookies = json.load(f)

receiver_id = config["receiver_id"]
message_file = config["message_file"]
delay_time = config["delay_time"]

def send_messages():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()

        # Load cookies
        context.add_cookies([
            {"name": "c_user", "value": cookies["c_user"], "domain": ".facebook.com", "path": "/"},
            {"name": "xs", "value": cookies["xs"], "domain": ".facebook.com", "path": "/"}
        ])

        page = context.new_page()
        page.goto(f"https://www.messenger.com/t/{receiver_id}")

        # Wait for chat to load
        time.sleep(5)

        # Read messages from file
        with open(message_file, "r") as f:
            messages = f.readlines()

        while True:
            for msg in messages:
                page.fill("div[role='textbox']", msg.strip())
                page.keyboard.press("Enter")
                print(f"📩 Sent: {msg.strip()}")
                time.sleep(delay_time)

send_messages()
