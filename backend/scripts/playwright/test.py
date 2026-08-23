from browser import get_browser

playwright, browser, context, page = get_browser()

page.goto("https://google.com")

print(page.title())

input("Press Enter to close...")

browser.close()
playwright.stop()