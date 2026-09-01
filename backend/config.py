from pathlib import Path

# Project Root
BASE_DIR = Path(__file__).resolve().parent

# Website
BASE_URL = "https://www2.miamidadeclerk.gov/ocs/"

CSV_PATH = r"C:\Users\tapes\OneDrive\Desktop\CSV Automation\Lawsuit-Automation\backend\input\cases.csv"

OUTPUT_PATH = r"C:\Users\tapes\OneDrive\Desktop\CSV Automation\Lawsuit-Automation\backend\downloads"


# Browser
HEADLESS = False

# Timeout (milliseconds)
TIMEOUT = 30000

# Directories
DOWNLOAD_DIR = BASE_DIR / "downloads" / "pdf"
SCREENSHOT_DIR = BASE_DIR / "screenshots"
LOG_DIR = BASE_DIR / "logs"

DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
SCREENSHOT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)