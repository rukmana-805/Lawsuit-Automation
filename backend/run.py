from config import BASE_URL
from pdf_downloader.browser import Browser
from pdf_downloader.parser import CaseParser
from pdf_downloader.search import CaseSearch

browser = Browser()

try:
    page = browser.start()

    page.goto(BASE_URL)

    search = CaseSearch(page)

    search.open_local_case_search()

    # Temporary hardcoded case number
    case_number = "2026-058549-SP-25"

    case = CaseParser.parse(case_number)

    search.search_case(case)

    input("Press Enter to close...")

finally:
    browser.close()