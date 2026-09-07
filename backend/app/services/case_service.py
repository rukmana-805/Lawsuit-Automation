from pathlib import Path

from config import BASE_URL

from pdf_downloader.browser import Browser
from pdf_downloader.parser import CaseParser
from pdf_downloader.search import CaseSearch
from pdf_downloader.csv_reader import (
    read_case_numbers,
    update_download_remark
)


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

        # Browser opens HERE
        page = browser.start()

        # Website opens HERE
        page.goto(BASE_URL)

        search = CaseSearch(page)

        search.open_local_case_search()

        for case_number in case_numbers:

            pdf_page = None

            try:

                print("=" * 60)
                print(f"Processing: {case_number}")
                print("=" * 60)

                case = CaseParser.parse(case_number)

                search.search_case(case)

                search.open_dockets()

                # pdf_page = search.open_statement_of_claim()
                # search.download_pdf(
                #     pdf_page,
                #     case_number,
                #     output_path
                # )

                # update_download_remark(
                #     csv_path,
                #     case_number,
                #     "Downloaded"
                # )

                pdf_page = search.open_statement_of_claim()

                if pdf_page is None:
                    update_download_remark(
                        csv_path,
                        case_number,
                        "Statement of Claim not found"
                    )

                    print(f"Statement of Claim not found: {case_number}")

                else:
                    search.download_pdf(
                        pdf_page,
                        case_number,
                        output_path
                    )

                update_download_remark(
                    csv_path,
                    case_number,
                    "Downloaded"
                )

                print(f"Downloaded successfully: {case_number}")

                pdf_page.close()

                print(f"Download remark updated: {case_number}")

                # PDF saving will go here
                #
                # search.save_pdf(
                #     pdf_page,
                #     case_number,
                #     output_path
                # )

                pdf_page.close()
                print(f"PDF page closed: {case_number}")
                
                # Go back to Home → Local Case
                search.go_to_home_and_local_case()

                processed_cases.append(case_number)

                print(f"Completed: {case_number}")

            except Exception as e:

                print(
                    f"Failed: {case_number} | {e}"
                )

                failed_cases.append({
                    "case_number": case_number,
                    "error": str(e)
                })

            finally:

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