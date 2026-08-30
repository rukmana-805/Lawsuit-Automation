from datetime import date
import calendar
import logging
from pathlib import Path
import time

from scripts.playwright.detail_report import download_report


# LOGGING

LOG_DIR = (
    Path(__file__).resolve().parents[2]
    / "logs"
)

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True
)

LOG_FILE = LOG_DIR / "scheduler.log"


logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)



# DOWNLOAD WITH RETRY

def download_with_retry(
    from_date: str,
    to_date: str,
    max_attempts: int = 3,
    retry_delay: int = 10
):
    """
    Download report with retry.

    Every retry starts the complete download process again.

    Attempt 1
        ↓
    download_report()
        ↓
    FAILED
        ↓
    Browser closes
        ↓
    Wait 10 seconds
        ↓
    Attempt 2
        ↓
    Fresh browser + VPN + website
        ↓
    ...

    Maximum attempts = 3
    """

    for attempt in range(
        1,
        max_attempts + 1
    ):

        print()
        print("================================")
        print(
            f"DOWNLOAD ATTEMPT "
            f"{attempt}/{max_attempts}"
        )
        print("================================")

        logger.info(
            f"Download attempt "
            f"{attempt}/{max_attempts} started"
        )

        try:

            
            # Complete fresh download attempt
            

            file_path = download_report(
                from_date,
                to_date
            )

            
            # SUCCESS
            

            print()
            print("================================")
            print(
                f"DOWNLOAD SUCCESSFUL "
                f"ON ATTEMPT {attempt}"
            )
            print("================================")

            print(
                f"File: {file_path}"
            )

            logger.info(
                f"Download successful on attempt "
                f"{attempt}: {file_path}"
            )

            return file_path

        except Exception as e:

            
            # ATTEMPT FAILED
            

            print()
            print("================================")
            print(
                f"DOWNLOAD ATTEMPT "
                f"{attempt}/{max_attempts} FAILED"
            )
            print("================================")

            print(
                f"Error: {e}"
            )

            logger.exception(
                f"Download attempt "
                f"{attempt}/{max_attempts} failed"
            )

            
            # RETRY
            

            if attempt < max_attempts:

                print()
                print(
                    "Browser will be closed."
                )

                print(
                    f"Retrying in "
                    f"{retry_delay} seconds..."
                )

                logger.info(
                    f"Retrying in "
                    f"{retry_delay} seconds"
                )

                time.sleep(
                    retry_delay
                )

            
            # FINAL ATTEMPT FAILED
            

            else:

                print()
                print("================================")
                print("ALL DOWNLOAD ATTEMPTS FAILED")
                print("================================")

                logger.error(
                    "All download attempts failed"
                )

                # Re-raise the current exception
                raise



# SCHEDULED REPORT

def run_scheduled_report():

    try:

        
        # TODAY
        # FINAL VERSION:
        #
        # today = date.today()
        #
    

        # TESTING ONLY
        today = date(2026, 8, 15)

        # When testing is finished, change to:
        #
        # today = date.today()


        year = today.year
        month = today.month
        day = today.day


        # Get last day of current month
        #
        # Example:
        # August  -> 31
        # September -> 30
        # February -> 28/29

        last_day = calendar.monthrange(
            year,
            month
        )[1]


        
        # SCHEDULER START
        

        print("================================")
        print("Scheduler Started")
        print(f"Today: {today}")
        print("================================")

        logger.info(
            "================================"
        )

        logger.info(
            "Scheduler Started"
        )

        logger.info(
            f"Today: {today}"
        )

        logger.info(
            "================================"
        )


        
        # FIRST HALF: 1 -> 15
        

        if day == 15:

            from_date = date(
                year,
                month,
                1
            )

            to_date = date(
                year,
                month,
                15
            )


            print(
                f"Running first-half report: "
                f"{from_date} -> {to_date}"
            )

            logger.info(
                f"Running first-half report: "
                f"{from_date} -> {to_date}"
            )


            
            # DOWNLOAD WITH RETRY
            

            file_path = download_with_retry(
                from_date.isoformat(),
                to_date.isoformat()
            )


            print()
            print(
                "First-half report downloaded:"
            )

            print(
                file_path
            )


            logger.info(
                f"First-half report downloaded successfully: "
                f"{file_path}"
            )


        
        # SECOND HALF: 16 -> LAST DAY
        

        elif day == last_day:

            from_date = date(
                year,
                month,
                16
            )

            to_date = date(
                year,
                month,
                last_day
            )


            print(
                f"Running second-half report: "
                f"{from_date} -> {to_date}"
            )

            logger.info(
                f"Running second-half report: "
                f"{from_date} -> {to_date}"
            )


            
            # DOWNLOAD WITH RETRY
            

            file_path = download_with_retry(
                from_date.isoformat(),
                to_date.isoformat()
            )


            print()
            print(
                "Second-half report downloaded:"
            )

            print(
                file_path
            )


            logger.info(
                f"Second-half report downloaded successfully: "
                f"{file_path}"
            )


        
        # NOT A REPORT DAY
        

        else:

            print()
            print(
                "Today is not a scheduled report day."
            )

            logger.info(
                "Today is not a scheduled report day."
            )


    
    # SCHEDULER ERROR HANDLING

    except Exception as e:

        print()
        print("================================")
        print("SCHEDULER FAILED")
        print("================================")

        print(
            f"Error: {e}"
        )


        # logger.exception automatically stores
        # the complete traceback.

        logger.exception(
            "Scheduled report failed"
        )


        # Important for Task Scheduler:
        # non-zero exit code when something fails.

        raise


# MAIN

if __name__ == "__main__":

    run_scheduled_report()