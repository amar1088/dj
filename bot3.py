from playwright.sync_api import sync_playwright
import json
import time

# Load config
with open("config.json", "r") as f:
    config = json.load(f)

email = config["email"]
password = config["password"]

def login_messenger(page):
    page.goto("https://www.messenger.com/")
    time.sleep(3)

    if "login" in page.url:  # Check if we are on the login page
        print("🔑 Logging in...")

        page.fill("input[name='email']", email)
        page.fill("input[name='pass']", password)
        page.click("button[name='login']")  # Click Login Button
        time.sleep(5)

        # Verify login success
        if "login" in page.url:
            print("❌ Login Failed! Check credentials.")
            return False
        print("✅ Login Successful!")

    return True

with sync_playwright() as p:
    # ✅ Enable headless mode
    browser = p.chromium.launch(headless=True, channel="chrome")  # Set headless=True
    context = browser.new_context()
    page = context.new_page()

    if login_messenger(page):
        print("🎉 Logged in successfully. Proceeding...")
    else:
        print("❌ Exiting script.")

    browser.close()
