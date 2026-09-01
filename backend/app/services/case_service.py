from pathlib import Path

from config import BASE_URL
from pdf_downloader.browser import Browser
from pdf_downloader.parser import CaseParser
from pdf_downloader.search import CaseSearch
from pdf_downloader.csv_reader import read_case_numbers


def process_cases(csv_path: str, output_path: str):

    csv_path = Path(csv_path)
    output_path = Path(output_path)

    if not csv_path.exists():
        raise FileNotFoundError(
            f"CSV file not found: {csv_path}"
        )

    output_path.mkdir(
        parents=True,
        exist_ok=True
    )

    case_numbers = read_case_numbers(csv_path)

    if not case_numbers:
        raise ValueError(
            "No case numbers found in CSV"
        )

    browser = Browser()

    processed_cases = []
    failed_cases = []

    try:
        # Start browser
        page = browser.start()

        # Open website
        page.goto(BASE_URL)

        # Create search object
        search = CaseSearch(page)

        # Open Local Case Search
        search.open_local_case_search()

        # Process each case
        for case_number in case_numbers:

            pdf_page = None

            try:
                print("=" * 60)
                print(f"Processing: {case_number}")
                print("=" * 60)

                # Parse case number
                case = CaseParser.parse(case_number)

                # Search case
                search.search_case(case)

                # Open dockets
                search.open_dockets()

                # Open Statement of Claim
                pdf_page = search.open_statement_of_claim()

                # PDF saving will be added here
                #
                # search.save_pdf(
                #     pdf_page,
                #     case_number,
                #     output_path
                # )

                processed_cases.append(case_number)

                print(f"Completed: {case_number}")

            except Exception as e:

                print(
                    f"Failed: {case_number} | Error: {e}"
                )

                failed_cases.append({
                    "case_number": case_number,
                    "error": str(e)
                })

            finally:

                # Close the PDF tab only.
                # The Local Case Search page remains open.
                if pdf_page is not None:
                    try:
                        if not pdf_page.is_closed():
                            pdf_page.close()
                    except Exception:
                        pass

        return {
            "total": len(case_numbers),
            "processed": len(processed_cases),
            "failed": len(failed_cases),
            "processed_cases": processed_cases,
            "failed_cases": failed_cases
        }

    finally:
        browser.close()