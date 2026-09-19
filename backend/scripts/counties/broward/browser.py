from pathlib import Path

from playwright.sync_api import BrowserContext, Playwright


BASE_DIR = Path(__file__).resolve().parents[3]

BROWARD_PROFILE_DIR = BASE_DIR / "browser_profile_broward"

BROWARD_PROFILE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


def get_broward_browser(playwright: Playwright) -> BrowserContext:
    context = playwright.chromium.launch_persistent_context(
        user_data_dir=str(BROWARD_PROFILE_DIR),
        headless=False,
        viewport={
            "width": 1400,
            "height": 900,
        },
        args=[
            "--start-maximized",
        ],
    )

    return context