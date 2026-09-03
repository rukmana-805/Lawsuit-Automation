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
        print("Case details:", case)

        self.page.locator(CASE_YEAR).select_option(
            case["year"]
        )

        self.page.locator(CASE_SEQUENCE).fill(
            case["sequence"]
        )

        self.page.locator(CASE_CODE).select_option(
            case["code"]
        )

        self.page.locator(CASE_LOCATION).select_option(
            case["location"]
        )

        print("Case details entered")

        self.page.locator(SEARCH_BUTTON).click()

        self.page.wait_for_load_state("networkidle")

        print("Case Search Completed")
        print("Current URL:", self.page.url)

    def open_dockets(self):
        print("STEP 3: Opening Dockets")

        dockets = self.page.locator(
            DOCKETS_SECTION
        ).filter(
            has_text=DOCKETS_TEXT
        )

        print("Dockets count:", dockets.count())

        dockets.first.wait_for(
            state="visible",
            timeout=15000
        )

        dockets.first.click()

        print("STEP 3 DONE")

    def open_statement_of_claim(self):
        print("STEP 4: Opening Statement of Claim...")

        with self.page.expect_popup() as popup_info:

            self.page.get_by_role(
                "button",
                name=STATEMENT_OF_CLAIM_BUTTON
            ).click()

        pdf_page = popup_info.value

        pdf_page.wait_for_load_state(
            "domcontentloaded"
        )

        print("PDF page opened:")
        print(pdf_page.url)

        # IMPORTANT:
        # Do NOT do self.page = pdf_page

        return pdf_page

    def download_pdf(
        self,
        pdf_page: Page,
        case_number: str,
        output_path: str
    ):
        print(f"Downloading PDF: {case_number}")

        output_path = Path(output_path)
        output_path.mkdir(
            parents=True,
            exist_ok=True
        )

        file_path = (
            output_path / f"{case_number}.pdf"
        )

        download_button = pdf_page.get_by_role(
            "button",
            name="Download"
        )

        download_button.wait_for(
            state="visible",
            timeout=120000
        )

        print("Download button found")

        with pdf_page.expect_download() as download_info:
            download_button.click()

        download = download_info.value

        download.save_as(
            str(file_path)
        )

        print(f"PDF saved: {file_path}")


        return file_path

# def go_to_home_and_local_case(self):
#     print("STEP 5: Returning to OCS Home...")

#     # Click OCS Home from breadcrumb
#     self.page.locator("#breadcrumb").get_by_text(
#         "OCS Home",
#         exact=True
#     ).click()

#     self.page.wait_for_load_state("networkidle")

#     print("OCS Home opened")

#     # Open Local Case again
#     self.page.get_by_text(
#         LOCAL_CASE,
#         exact=True
#     ).click()

#     self.page.locator(CASE_YEAR).wait_for(
#         state="visible",
#         timeout=30000
#     )

#     print("Local Case Search opened")

    def go_to_home_and_local_case(self):
        print("STEP 5: Going back to OCS Home...")

        home = self.page.locator(
            "#breadcrumb li"
        ).filter(
            has_text="OCS Home"
        )

        home.wait_for(
            state="visible",
            timeout=30000
        )

        print("OCS Home link found")

        home.click()

        self.page.wait_for_load_state(
            "networkidle"
        )

        print("OCS Home opened")
        print("Current URL:", self.page.url)

        local_case = self.page.get_by_text(
            LOCAL_CASE,
            exact=True
        )

        local_case.wait_for(
            state="visible",
            timeout=30000
        )

        local_case.click()

        self.page.locator(
            CASE_YEAR
        ).wait_for(
            state="visible",
            timeout=30000
        )

        print("Local Case Search opened")