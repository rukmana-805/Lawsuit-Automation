from datetime import date
import calendar

from scripts.playwright.detail_report import download_report


def run_scheduled_report():

    today = date.today()

    # today = date(2026, 8, 15)

    year = today.year
    month = today.month
    day = today.day

    last_day = calendar.monthrange(
        year,
        month
    )[1]

    print("================================")
    print("Scheduler Started")
    print(f"Today: {today}")
    print("================================")


    
    # First half: 1 -> 15
    
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

        download_report(
            from_date.isoformat(),
            to_date.isoformat()
        )


    
    # Second half: 16 -> Last Day

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

        download_report(
            from_date.isoformat(),
            to_date.isoformat()
        )


    else:

        print(
            "Today is not a scheduled report day."
        )


if __name__ == "__main__":

    run_scheduled_report()