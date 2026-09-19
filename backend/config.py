from pathlib import Path


# LAWSUIT REPORT DATA

# CHANGE ONLY THIS PATH WHEN MOVING TO ANOTHER SYSTEM
LAWSUIT_ROOT = Path(r"C:\Users\Rukmana\Documents")

# CHANGE ONLY THIS PATH WHEN MOVING TO ANOTHER SYSTEM
TURBO_VPN_EXTENSION = Path(
    r"C:\Users\Rukmana\AppData\Local\Google\Chrome\User Data\Default\Extensions\bnlofglpdlboacepdieejiecfbfpmhlb\2.0.4_0"
)

LAWSUIT_DIR = LAWSUIT_ROOT / "Lawsuit"

REPORTS_DIR = LAWSUIT_DIR

INDEX_DIR = LAWSUIT_DIR / "Files"

LAWSUIT_INDEX = INDEX_DIR / "index_lawsuits_20250121.xlsx"

INDEX_DIR.mkdir(parents=True, exist_ok=True)




# TAPESWAR PART

# Project Root
BASE_DIR = Path(__file__).resolve().parent

# Website
BASE_URL = "https://www2.miamidadeclerk.gov/ocs/"

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