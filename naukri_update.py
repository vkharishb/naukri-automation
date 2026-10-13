import os, random, time
from playwright.sync_api import sync_playwright

time.sleep(random.randint(0, 300))  # random delay

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36")
    page = ctx.new_page()
    try:
        page.goto("https://www.naukri.com/nlogin/login")
        page.fill("#usernameField", os.environ["NAUKRI_USER"])
        page.fill("#passwordField", os.environ["NAUKRI_PASS"])
        page.click("button[type=submit]")
        page.wait_for_url("**/mnjuser/**", timeout=30000)

        page.goto("https://www.naukri.com/mnjuser/profile")
        page.wait_for_load_state("networkidle")

        # SELECTOR PLACEHOLDER: replace using playwright codegen (Step 7)
        page.locator("text=Resume headline").locator("xpath=..").locator("[class*=edit]").first.click()
        page.get_by_role("button", name="Save").click()
        page.wait_for_timeout(3000)

        print("Profile saved")
    except Exception:
        page.screenshot(path="error.png")
        raise
    finally:
        browser.close()