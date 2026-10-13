import os, random, time
from playwright.sync_api import sync_playwright

if not os.environ.get("TEST_MODE"):
    time.sleep(random.randint(0, 300))

with sync_playwright() as p:
    browser = p.chromium.launch(headless=not os.environ.get("TEST_MODE"))
    ctx = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36",
        viewport={"width": 1366, "height": 900},
    )
    page = ctx.new_page()
    try:
        page.goto("https://www.naukri.com/nlogin/login")
        page.screenshot(path="1_login_page.png")
        page.fill("#usernameField", os.environ["NAUKRI_USER"])
        page.fill("#passwordField", os.environ["NAUKRI_PASS"])
        page.click("button[type=submit]")
        page.wait_for_url("**/mnjuser/**", timeout=30000)
        page.screenshot(path="2_after_login.png")

        page.goto("https://www.naukri.com/mnjuser/profile")
        page.wait_for_load_state("networkidle")
        page.screenshot(path="3_profile.png")

        # Edit icon next to Resume headline (selector is a guess; check screenshots if it fails)
        section = page.get_by_text("Resume headline", exact=False).first
        section.scroll_into_view_if_needed()
        section.locator("xpath=ancestor::div[1]").locator("[class*=edit]").first.click()
        page.screenshot(path="4_edit_open.png")

        page.get_by_role("button", name="Save").click()
        page.wait_for_timeout(3000)
        page.screenshot(path="5_saved.png")
        print("Profile saved")
    except Exception:
        page.screenshot(path="error.png")
        print(page.url)
        raise
    finally:
        browser.close()