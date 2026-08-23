from pathlib import Path
from datetime import datetime

from scripts.playwright.browser import get_browser
from scripts.playwright.selectors import *


URL = "https://apps.fldfs.com/LSOPReports/Reports/Report.aspx"


# Temporary folder
OUTPUT_DIR = Path(__file__).resolve().parents[2] / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DOWNLOAD_ROOT = Path(
    r"C:\Users\Rukmana\Documents\Lawsuit Reports"
)


def get_download_directory(from_date: str) -> Path:

    report_date = datetime.strptime(
        from_date,
        "%Y-%m-%d"
    )

    year = report_date.year

    month = report_date.strftime("%B")

    download_directory = (
        DOWNLOAD_ROOT
        / str(year)
        / month
    )

    download_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    return download_directory


def format_date(date_str: str) -> str:
    """
    React se:
        YYYY-MM-DD

    Website ke liye:
        MM/DD/YYYY
    """

    return datetime.strptime(
        date_str,
        "%Y-%m-%d"
    ).strftime("%m/%d/%Y")


def download_report(from_date: str, to_date: str):

    # Find year/month folder
    download_directory = get_download_directory(
        from_date
    )

    from_date = format_date(from_date)
    to_date = format_date(to_date)

    playwright, browser, context, page = get_browser()

    try:

        
        # Open website

        print("Opening website...")

        page.goto(
            URL,
            wait_until="networkidle",
            timeout=60000
        )

        print("Website opened successfully.")


        
        # From Date
        
        page.locator(
            REPORT_FROM_DATE_INPUT
        ).fill(from_date)

        print(f"From Date : {from_date}")


        
        # To Date
        
        page.locator(
            REPORT_TO_DATE_INPUT
        ).fill(to_date)

        print(f"To Date : {to_date}")


        
        # Submit
        
        print("Submitting Form...")

        with context.expect_page() as new_page_info:

            page.locator(
                REPORT_SUBMIT_BUTTON
            ).click()

        report_page = new_page_info.value

        report_page.wait_for_load_state(
            "networkidle"
        )

        print(
            "Report Page Opened Successfully."
        )


        
        # Open Export Menu
        
        report_page.locator(
            REPORT_EXPORT_BUTTON
        ).click()

        report_page.locator(
            REPORT_EXPORT_CSV
        ).wait_for(
            state="visible"
        )

        print("Export Menu Opened.")


        
        # Download CSV
        
        with report_page.expect_download() as download_info:

            report_page.locator(
                REPORT_EXPORT_CSV
            ).click()

        download = download_info.value


        
        # Save temporary CSV
        
        file_path = (
            download_directory /
            download.suggested_filename
        )

        download.save_as(
            file_path
        )

        print(
            f"CSV Downloaded Successfully: {file_path}"
        )

        # Return path to FastAPI
        
        return str(file_path)


    except Exception as e:

        print(
            f"CSV download failed: {e}"
        )

        raise


    finally:

        browser.close()

        playwright.stop()