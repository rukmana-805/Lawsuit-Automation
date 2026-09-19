from playwright.sync_api import BrowserContext, Page

from scripts.counties.broward.selectors import (
    BROWARD_URL,
    CASE_NUMBER_TAB,
    CASE_NUMBER_INPUT,
    SEARCH_BUTTON,
)


class BrowardDownloader:
    def __init__(self, context: BrowserContext):
        self.context = context
        self.page: Page | None = None

    def open(self) -> Page:
        self.page = self.context.new_page()

        print("Opening Broward Clerk website...")

        self.page.goto(
            BROWARD_URL,
            wait_until="domcontentloaded",
            timeout=60_000,
        )

        print("Broward website opened.")

        return self.page

    def search_case(self, case_number: str) -> None:
        if self.page is None:
            raise RuntimeError("Broward page has not been opened.")

        print(f"Searching case: {case_number}")

        if CASE_NUMBER_TAB:
            self.page.locator(CASE_NUMBER_TAB).click()

        self.page.locator(CASE_NUMBER_INPUT).fill(case_number)

        self.page.locator(SEARCH_BUTTON).click()

        print(f"Search submitted for: {case_number}")