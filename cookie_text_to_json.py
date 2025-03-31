import json
import re

# Read raw cookie from file
with open("cookie.txt", "r") as f:
    raw_cookie = f.read().strip()

# Extract c_user and xs values
match_c_user = re.search(r'c_user=([^;]+)', raw_cookie)
match_xs = re.search(r'xs=([^;]+)', raw_cookie)

if match_c_user and match_xs:
    cookies = {
        "c_user": match_c_user.group(1),
        "xs": match_xs.group(1)
    }

    # Save as JSON
    with open("cookies.json", "w") as f:
        json.dump(cookies, f, indent=4)

    print("✅ Cookie converted successfully! Saved to cookies.json")
else:
    print("❌ Error: Could not find c_user or xs in cookie.txt")
