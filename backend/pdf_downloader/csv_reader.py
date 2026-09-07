import csv
from pathlib import Path

def read_case_numbers(csv_path):
    case_numbers = []

    with open(
        csv_path,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        print("CSV columns:", reader.fieldnames)

        for row in reader:

            print("ROW:", row)

            case_number = row.get(
                "case_number",
                ""
            ).strip()

            remark = row.get(
                "download remarks",
                ""
            ).strip()

            print(
                f"CASE: {case_number} | "
                f"REMARK: '{remark}'"
            )

            if not case_number:
                continue

            if remark:
                print(
                    f"SKIPPING: {case_number} "
                    f"| {remark}"
                )
                continue

            case_numbers.append(case_number)

    print("Cases to process:", case_numbers)

    return case_numbers

def update_download_remark(
    csv_path,
    case_number,
    remark="Downloaded"
):
    csv_path = Path(csv_path)

    temp_path = csv_path.with_suffix(".tmp.csv")

    # Read original CSV
    with open(
        csv_path,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        fieldnames = reader.fieldnames
        rows = list(reader)

    # Add column if it doesn't already exist
    if "download remarks" not in fieldnames:
        fieldnames.append("download remarks")

    # Update matching case
    for row in rows:
        if row["case_number"].strip() == case_number:
            row["download remarks"] = remark
            break

    # Write to temporary file FIRST
    with open(
        temp_path,
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(rows)

    # Only after successful write, replace original
    temp_path.replace(csv_path)