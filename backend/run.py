from config import CSV_PATH, OUTPUT_PATH
from app.services.case_service import process_cases


if __name__ == "__main__":

    print("=" * 60)
    print("Starting Lawsuit Automation - Test Run")
    print("=" * 60)

    print(f"CSV Path    : {CSV_PATH}")
    print(f"Output Path : {OUTPUT_PATH}")

    try:
        result = process_cases(
            csv_path=CSV_PATH,
            output_path=OUTPUT_PATH
        )

        print("\n" + "=" * 60)
        print("PROCESS COMPLETED")
        print("=" * 60)

        print(f"Total cases     : {result['total']}")
        print(f"Processed cases : {result['processed']}")
        print(f"Failed cases    : {result['failed']}")

        if result["failed_cases"]:
            print("\nFailed cases:")

            for failed in result["failed_cases"]:
                print(
                    f"- {failed['case_number']}: "
                    f"{failed['error']}"
                )

    except Exception as e:
        print("\nAutomation failed:")
        print(e)