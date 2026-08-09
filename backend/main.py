from pdf_downloader.browser import Browser
from pdf_downloader.search import CaseSearch
from config import BASE_URL


browser = Browser()

page = browser.start()

page.goto(BASE_URL)

search = CaseSearch(page)
search.open_local_case_search()

input("Press Enter to close...")

browser.close()