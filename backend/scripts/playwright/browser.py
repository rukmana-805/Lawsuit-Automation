# from playwright.sync_api import sync_playwright


# def get_browser():
#     playwright = sync_playwright().start()

#     browser = playwright.chromium.launch(
#         headless=False,
#         slow_mo=500
#     )

#     context = browser.new_context(
#         accept_downloads=True
#     )

#     page = context.new_page()

#     return playwright, browser, context, page

from pathlib import Path
from playwright.sync_api import sync_playwright


# ==========================================
# Dedicated Playwright browser profile
# ==========================================

PROFILE_DIR = (
    Path(__file__).resolve().parents[2]
    / "browser_profile"
)


# ==========================================
# Turbo VPN extension
# ==========================================

EXTENSION_PATH = Path(
    r"C:\Users\Rukmana\AppData\Local\Google\Chrome\User Data\Default\Extensions\bnlofglpdlboacepdieejiecfbfpmhlb\2.0.4_0"
)


def get_browser():

    playwright = sync_playwright().start()

    context = playwright.chromium.launch_persistent_context(

        user_data_dir=str(PROFILE_DIR),

        headless=False,

        viewport={
            "width": 1280,
            "height": 900
        },

        args=[
            f"--disable-extensions-except={EXTENSION_PATH}",
            f"--load-extension={EXTENSION_PATH}",
        ]
    )

    if context.pages:

        page = context.pages[0]

    else:

        page = context.new_page()

    return playwright, context, page