from pathlib import Path
from datetime import datetime
import time
import logging

from scripts.playwright.browser import get_browser
from scripts.playwright.selectors import *



# FLDFS REPORT URL

URL = (
    "https://apps.fldfs.com/"
    "LSOPReports/Reports/Report.aspx"
)



# VPN CONFIGURATION

EXTENSION_ID = (
    "bnlofglpdlboacepdieejiecfbfpmhlb"
)

VPN_POPUP_URL = (
    f"chrome-extension://{EXTENSION_ID}"
    "/dist/popup/index.html"
)

# Maximum VPN clicks inside the SAME browser
VPN_MAX_ATTEMPTS = 3

# Maximum seconds to wait for VPN connection
# after each click
VPN_CONNECT_TIMEOUT = 30

# Wait between VPN click attempts
VPN_RETRY_DELAY = 5



# VPN SELECTORS

# Disconnected state:
#
# <div class="mt-5 w-16 h-16 cursor-pointer">
#     <img src="/assets/radish@3x.png">
# </div>

VPN_CONNECT_SELECTOR = (
    'div.mt-5.w-16.h-16.cursor-pointer'
    ':has(img[src="/assets/radish@3x.png"])'
)


# Connected state:
#
# <div class="mt-5 w-16 h-16 cursor-pointer">
#     <img src="/assets/stop@3x.png">
# </div>

VPN_CONNECTED_SELECTOR = (
    'div.mt-5.w-16.h-16.cursor-pointer'
    ':has(img[src="/assets/stop@3x.png"])'
)



# DOWNLOAD LOCATION

DOWNLOAD_ROOT = Path(
    r"C:\Users\Rukmana\Documents\Lawsuit Reports"
)



# LOGGING

LOG_DIR = (
    Path(__file__).resolve().parents[2]
    / "logs"
)

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True
)

LOG_FILE = (
    LOG_DIR / "scheduler.log"
)

logger = logging.getLogger(__name__)



# GET YEAR / MONTH FOLDER

def get_download_directory(
    from_date: str
) -> Path:

    report_date = datetime.strptime(
        from_date,
        "%Y-%m-%d"
    )

    year = report_date.year

    month = report_date.strftime(
        "%B"
    )

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



# FORMAT DATE

def format_date(
    date_str: str
) -> str:

    """
    Input:
        YYYY-MM-DD

    Output:
        MM/DD/YYYY
    """

    return datetime.strptime(
        date_str,
        "%Y-%m-%d"
    ).strftime(
        "%m/%d/%Y"
    )



# CONNECT TURBO VPN


def connect_turbo_vpn(
    context
):
    """
    Connect Turbo VPN.

    VPN retry happens inside the SAME browser.

    Attempt 1
        ↓
    click connect
        ↓
    wait for stop@3x.png
        ↓
    connected → return

    If not connected:

    Attempt 2
        ↓
    click again
        ↓
    wait

    Attempt 3
        ↓
    click again
        ↓
    wait

    If all attempts fail:
        raise Exception

    The outer scheduler will then start
    a completely fresh browser.
    """

    print()
    print("================================")
    print("Connecting Turbo VPN")
    print("================================")

    logger.info(
        "Starting Turbo VPN connection"
    )

    popup_page = context.new_page()

    try:

        
        # OPEN VPN POPUP
        

        popup_page.goto(
            VPN_POPUP_URL,
            wait_until="domcontentloaded",
            timeout=30000
        )

        popup_page.wait_for_timeout(
            2000
        )

        print(
            "Turbo VPN popup opened."
        )

        logger.info(
            "Turbo VPN popup opened"
        )


        
        # VPN ATTEMPTS
        

        for attempt in range(
            1,
            VPN_MAX_ATTEMPTS + 1
        ):

            print()
            print(
                "================================"
            )

            print(
                f"VPN ATTEMPT "
                f"{attempt}/{VPN_MAX_ATTEMPTS}"
            )

            print(
                "================================"
            )

            logger.info(
                f"VPN attempt "
                f"{attempt}/{VPN_MAX_ATTEMPTS}"
            )


            
            # CHECK IF ALREADY CONNECTED

            connected_button = popup_page.locator(
                VPN_CONNECTED_SELECTOR
            )

            if connected_button.count() > 0:

                print(
                    "Turbo VPN is already connected."
                )

                logger.info(
                    "Turbo VPN already connected"
                )

                return


           
            # FIND CONNECT BUTTON

            connect_button = popup_page.locator(
                VPN_CONNECT_SELECTOR
            ).first

            connect_count = connect_button.count()

            print(
                f"VPN Connect button count: "
                f"{connect_count}"
            )

            logger.info(
                f"VPN Connect button count: "
                f"{connect_count}"
            )


            
            # CONNECT BUTTON NOT FOUND

            if connect_count == 0:

                print(
                    "VPN Connect button not found."
                )

                logger.warning(
                    "VPN Connect button not found"
                )

            else:

                
                # CLICK VPN

                print(
                    "Clicking Turbo VPN Connect..."
                )

                logger.info(
                    "Clicking Turbo VPN Connect"
                )

                connect_button.click(
                    timeout=10000
                )

                print(
                    "Turbo VPN Connect clicked."
                )

                logger.info(
                    "Turbo VPN Connect clicked"
                )


            
            # WAIT FOR ACTUAL CONNECTION

            print(
                "Waiting for VPN connection..."
            )

            connected = False

            for second in range(
                1,
                VPN_CONNECT_TIMEOUT + 1
            ):

                popup_page.wait_for_timeout(
                    1000
                )


                
                # CHECK STOP IMAGE

                connected_button = (
                    popup_page.locator(
                        VPN_CONNECTED_SELECTOR
                    )
                )

                if connected_button.count() > 0:

                    connected = True

                    print()
                    print(
                        "================================"
                    )

                    print(
                        "VPN CONNECTED SUCCESSFULLY"
                    )

                    print(
                        f"Connection established "
                        f"after {second} seconds."
                    )

                    print(
                        "================================"
                    )

                    logger.info(
                        "VPN connected successfully "
                        f"after {second} seconds"
                    )

                    break


            
            # SUCCESS

            if connected:

                return


            # CURRENT ATTEMPT FAILED

            print()
            print(
                f"VPN attempt {attempt} "
                f"did not connect."
            )

            logger.warning(
                f"VPN attempt {attempt} "
                f"did not connect"
            )


            # RETRY SAME BROWSER

            if attempt < VPN_MAX_ATTEMPTS:

                print(
                    f"Waiting {VPN_RETRY_DELAY} "
                    f"seconds before VPN retry..."
                )

                logger.info(
                    f"Waiting {VPN_RETRY_DELAY} "
                    f"seconds before VPN retry"
                )

                popup_page.wait_for_timeout(
                    VPN_RETRY_DELAY * 1000
                )


            
            # ALL VPN ATTEMPTS FAILED

            else:

                print()
                print(
                    "================================"
                )

                print(
                    "VPN CONNECTION FAILED"
                )

                print(
                    f"VPN failed after "
                    f"{VPN_MAX_ATTEMPTS} attempts."
                )

                print(
                    "================================"
                )

                logger.error(
                    "Turbo VPN failed after "
                    f"{VPN_MAX_ATTEMPTS} attempts"
                )

                raise Exception(
                    "Turbo VPN could not connect "
                    f"after {VPN_MAX_ATTEMPTS} attempts."
                )


    finally:

        # Only close VPN popup.
        #
        # Do NOT close browser/context here.
        #
        # download_report() owns the browser.

        try:

            popup_page.close()

        except Exception:

            pass



# DOWNLOAD REPORT

def download_report(
    from_date: str,
    to_date: str
):

    
    # FIND DOWNLOAD DIRECTORY
    
    download_directory = (
        get_download_directory(
            from_date
        )
    )

    print()
    print(
        f"Download directory: "
        f"{download_directory}"
    )


    
    # FORMAT DATES

    website_from_date = (
        format_date(
            from_date
        )
    )

    website_to_date = (
        format_date(
            to_date
        )
    )

    print(
        f"From Date : "
        f"{website_from_date}"
    )

    print(
        f"To Date   : "
        f"{website_to_date}"
    )


    
    # START PLAYWRIGHT

    playwright, context, page = (
        get_browser()
    )


    try:

        
        # STEP 1 — CONNECT VPN

        connect_turbo_vpn(
            context
        )

        print(
            "VPN step completed."
        )

        logger.info(
            "VPN step completed"
        )


        
        # STEP 2 — OPEN FLDFS WEBSITE
        
        print()
        print(
            "Opening FLDFS website..."
        )

        logger.info(
            "Opening FLDFS website"
        )

        page.goto(
            URL,
            wait_until="networkidle",
            timeout=60000
        )

        print(
            "FLDFS website opened successfully."
        )

        logger.info(
            "FLDFS website opened successfully"
        )


        
        # STEP 3 — FROM DATE
        
        page.locator(
            REPORT_FROM_DATE_INPUT
        ).fill(
            website_from_date
        )

        print(
            f"From Date filled: "
            f"{website_from_date}"
        )

        logger.info(
            f"From Date filled: "
            f"{website_from_date}"
        )


        
        # STEP 4 — TO DATE

        page.locator(
            REPORT_TO_DATE_INPUT
        ).fill(
            website_to_date
        )

        print(
            f"To Date filled: "
            f"{website_to_date}"
        )

        logger.info(
            f"To Date filled: "
            f"{website_to_date}"
        )


        
        # STEP 5 — SUBMIT

        print()
        print(
            "Submitting report..."
        )

        logger.info(
            "Submitting report"
        )

        with context.expect_page() as (
            new_page_info
        ):

            page.locator(
                REPORT_SUBMIT_BUTTON
            ).click()

        report_page = (
            new_page_info.value
        )

        report_page.wait_for_load_state(
            "networkidle"
        )

        print(
            "Report Page Opened Successfully."
        )

        logger.info(
            "Report page opened successfully"
        )


        
        # STEP 6 — OPEN EXPORT MENU

        print(
            "Opening Export Menu..."
        )

        logger.info(
            "Opening export menu"
        )

        report_page.locator(
            REPORT_EXPORT_BUTTON
        ).click()


        # Wait for CSV option

        report_page.locator(
            REPORT_EXPORT_CSV
        ).wait_for(
            state="visible"
        )

        print(
            "Export Menu Opened."
        )

        logger.info(
            "Export menu opened"
        )


        
        # STEP 7 — DOWNLOAD CSV
        
        print(
            "Downloading CSV..."
        )

        logger.info(
            "Downloading CSV"
        )

        with report_page.expect_download() as (
            download_info
        ):

            report_page.locator(
                REPORT_EXPORT_CSV
            ).click()

        download = (
            download_info.value
        )

        print(
            "CSV download completed."
        )

        logger.info(
            "CSV download completed"
        )


        
        # STEP 8 — SAVE CSV

        file_path = (
            download_directory
            / download.suggested_filename
        )

        download.save_as(
            file_path
        )

        print()
        print(
            "================================"
        )

        print(
            "CSV Downloaded Successfully!"
        )

        print(
            f"File: {file_path}"
        )

        print(
            "================================"
        )

        logger.info(
            f"CSV downloaded successfully: "
            f"{file_path}"
        )


        
        # RETURN FILE PATH

        return str(
            file_path
        )



    # ERROR HANDLING

    except Exception as e:

        print()
        print(
            "================================"
        )

        print(
            "CSV DOWNLOAD FAILED"
        )

        print(
            "================================"
        )

        print(
            e
        )

        logger.exception(
            "CSV download failed"
        )

        raise


    # CLEANUP

    finally:

        print()
        print(
            "Closing browser..."
        )

        logger.info(
            "Closing browser"
        )

        context.close()

        playwright.stop()

        logger.info(
            "Browser closed"
        )



# TEST


if __name__ == "__main__":

    download_report(
        "2026-08-01",
        "2026-08-15"
    )