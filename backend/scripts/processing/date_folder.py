from datetime import date
from pathlib import Path


# Main Lawsuit Reports folder
# BASE_DIR = Path(
#     r"C:\Users\Rukmana\Documents\Lawsuit Reports"
# )

from config import REPORTS_DIR


def get_report_folder(report_date: date) -> Path:
    """
    Returns the correct folder for the given report date.

    1st - 15th = 1ST
    16th - month end = 2ND
    """

    year = report_date.year

    month = report_date.strftime("%B").upper()

    if report_date.day <= 15:
        half = "1ST"
    else:
        half = "2ND"

    folder = REPORTS_DIR / str(year) / month / half

    folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    return folder