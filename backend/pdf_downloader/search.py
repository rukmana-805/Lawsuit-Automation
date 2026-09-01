# from playwright.sync_api import Page
# from pathlib import Path

# from .selectors import (
#     LOCAL_CASE,
#     CASE_YEAR,
#     CASE_SEQUENCE,
#     CASE_CODE,
#     CASE_LOCATION,
#     SEARCH_BUTTON,
#     DOCKETS_SECTION,
#     DOCKETS_TEXT,
#     STATEMENT_OF_CLAIM_BUTTON,
#     PRINT_BUTTON,
# )


# class CaseSearch:

#     def __init__(self, page: Page):
#         self.page = page

#     def open_local_case_search(self):
#         print("STEP 1: Opening Local Case")

#         self.page.get_by_text(LOCAL_CASE).click()
#         self.page.wait_for_load_state("networkidle")

#         print("STEP 1 DONE")

#     def search_case(self, case: dict):
#         print("STEP 2: Searching Case")

#         self.page.locator(CASE_YEAR).select_option(case["year"])
#         self.page.locator(CASE_SEQUENCE).fill(case["sequence"])
#         self.page.locator(CASE_CODE).select_option(case["code"])
#         self.page.locator(CASE_LOCATION).select_option(case["location"])

#         self.page.locator(SEARCH_BUTTON).click()

#         self.page.wait_for_load_state("networkidle")

#         print("Case Search Completed")
#         print("Current URL:", self.page.url)

#     def open_dockets(self):
#         print("STEP 3: Opening Dockets")

#         dockets = self.page.locator(
#             DOCKETS_SECTION
#         ).filter(
#             has_text=DOCKETS_TEXT
#         )

#         print("Dockets count:", dockets.count())

#         dockets.first.wait_for(
#             state="visible",
#             timeout=15000
#         )

#         dockets.first.click()

#         print("STEP 3 DONE")

#     def open_statement_of_claim(self):
#         print("Opening Statement of Claim...")
#         with self.page.expect_popup() as popup_info:
#             self.page.get_by_role(
#                 "button",
#                 name="View details for Statement of Claim"
#             ).click()

#         pdf_page = popup_info.value

#         pdf_page.wait_for_load_state("domcontentloaded")

#         print("PDF page opened:")
#         print(pdf_page.url)

#         self.page = pdf_page

#         print("Statement of Claim opened")


#     def print_case(self):
#         print("Looking for Print button...")

#         print_button = self.page.locator(PRINT_BUTTON)

#         print("Locator created")

#         print_button.wait_for(
#             state="visible",
#             timeout=1200000
#         )

#         print("Print button is visible")
#         print("Print button count:", print_button.count())

#         print_button.click(
#             force=True,
#             timeout=120000
#         )

#         print("Print button clicked")
import time
import pyautogui
from pathlib import Path

from playwright.sync_api import Page

from .selectors import (
    LOCAL_CASE,
    CASE_YEAR,
    CASE_SEQUENCE,
    CASE_CODE,
    CASE_LOCATION,
    SEARCH_BUTTON,
    DOCKETS_SECTION,
    DOCKETS_TEXT,
    STATEMENT_OF_CLAIM_BUTTON,
    PRINT_BUTTON,
)


class CaseSearch:

    def __init__(self, page: Page):
        self.page = page

    def open_local_case_search(self):
        print("STEP 1: Opening Local Case")

        self.page.get_by_text(LOCAL_CASE).click()
        self.page.wait_for_load_state("networkidle")

        print("STEP 1 DONE")

    def search_case(self, case: dict):
        print("STEP 2: Searching Case")

        self.page.locator(CASE_YEAR).select_option(case["year"])
        self.page.locator(CASE_SEQUENCE).fill(case["sequence"])
        self.page.locator(CASE_CODE).select_option(case["code"])
        self.page.locator(CASE_LOCATION).select_option(case["location"])

        self.page.locator(SEARCH_BUTTON).click()

        self.page.wait_for_load_state("networkidle")

        print("Case Search Completed")
        print("Current URL:", self.page.url)

    def open_dockets(self):
        print("STEP 3: Opening Dockets")

        dockets = self.page.locator(DOCKETS_SECTION).filter(has_text=DOCKETS_TEXT)

        print("Dockets count:", dockets.count())

        dockets.first.wait_for(state="visible", timeout=15000)

        dockets.first.click()

        print("STEP 3 DONE")

    def open_statement_of_claim(self):
        print("Opening Statement of Claim...")

        with self.page.expect_popup() as popup_info:
            self.page.get_by_role("button", name=STATEMENT_OF_CLAIM_BUTTON).click()

        pdf_page = popup_info.value

        pdf_page.wait_for_load_state("domcontentloaded")

        print("Statement of Claim opened")
        print("PDF URL:", pdf_page.url)

        return pdf_page

    def print_case(self, pdf_page):
        print("Looking for Print button...")

        print_button = pdf_page.locator(PRINT_BUTTON)

        print_button.wait_for(
            state="visible",
            timeout=120000
        )

        print("Print button found")

        print_button.click(
            force=True,
            timeout=30000
        )

        print("Print button clicked")
