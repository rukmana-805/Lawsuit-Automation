from playwright.sync_api import sync_playwright

from scripts.counties.broward.browser import get_broward_browser
from scripts.counties.broward.broward import BrowardDownloader


def main():
    with sync_playwright() as playwright:
        context = get_broward_browser(playwright)

        try:
            broward = BrowardDownloader(context)

            broward.open()

            print("Broward test completed.")

            input("Press Enter to close browser...")

        finally:
            context.close()


if __name__ == "__main__":
    main()