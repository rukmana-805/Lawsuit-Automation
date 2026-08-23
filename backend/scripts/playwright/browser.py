from playwright.sync_api import sync_playwright


def get_browser():
    playwright = sync_playwright().start()

    browser = playwright.chromium.launch(
        headless=False,
        slow_mo=500
    )

    context = browser.new_context(
        accept_downloads=True
    )

    page = context.new_page()

    return playwright, browser, context, page