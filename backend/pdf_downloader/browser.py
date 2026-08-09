from playwright.sync_api import sync_playwright

from config import HEADLESS


class Browser:

    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def start(self):

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=HEADLESS
        )

        self.context = self.browser.new_context(
            accept_downloads=True
        )

        self.page = self.context.new_page()

        return self.page

    def close(self):

        self.context.close()
        self.browser.close()
        self.playwright.stop()