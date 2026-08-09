from playwright.sync_api import Page


class CaseSearch:
    def __init__(self, page: Page):
        self.page = page

    def open_local_case_search(self):
        self.page.get_by_text("Local Case").click()
        self.page.wait_for_load_state("networkidle")

    def search_case(self, case: dict):

        # Select Case Year
        self.page.locator("#caseYear").select_option(case["year"])

        # Enter Case Sequence
        self.page.locator("#caseSeq").fill(case["sequence"])

        # Select Case Code
        self.page.locator("#caseCode").select_option(case["code"])

        # Wait until Case Location becomes enabled
        self.page.locator("#caseLocation").wait_for(state="visible")
        self.page.locator("#caseLocation").wait_for(
            state="attached"
        )

        # Select Case Location
        self.page.locator("#caseLocation").select_option(case["location"])

        # Click Search
        self.page.locator("button[type='submit']").click()

        # Wait for results page
        self.page.wait_for_load_state("networkidle")

        print("Case Search Completed")

    def open_dockets(self):
        dockets = self.page.locator(
            "div.mdc-custom__section-header"
        ).filter(has_text="Dockets")

        dockets.locator("div.symbol").click()
        print(" Dockets clicked")