from scripts.playwright.browser import get_browser
from scripts.playwright.selectors import VPN_CONNECT_BUTTON


EXTENSION_ID = "bnlofglpdlboacepdieejiecfbfpmhlb"

POPUP_URL = (
    f"chrome-extension://{EXTENSION_ID}"
    "/dist/popup/index.html"
)


playwright, context, page = get_browser()

try:

    print("Browser started")

    popup_page = context.new_page()

    popup_page.goto(
        POPUP_URL,
        wait_until="domcontentloaded"
    )

    popup_page.wait_for_timeout(3000)

    print("Turbo VPN popup opened!")

    # ==========================================
    # Actual Connect Image Container
    # ==========================================

    connect_button = popup_page.locator(
        VPN_CONNECT_BUTTON
    )

    print(
        "Connect button count:",
        connect_button.count()
    )

    print(
        "Clicking actual Connect button..."
    )

    connect_button.click()

    print(
        "Connect button clicked!"
    )

    # Give VPN time to react
    popup_page.wait_for_timeout(10000)

    print(
        "\n========== AFTER CLICK =========="
    )

    print(
        popup_page.locator("body").inner_text()
    )

    print(
        "================================="
    )

    input(
        "\nBrowser observe karo. "
        "Press Enter to close..."
    )

finally:

    context.close()
    playwright.stop()