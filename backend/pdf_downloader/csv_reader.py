import csv


def read_case_numbers(csv_path):
    case_numbers = []

    with open(csv_path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            case_number = row["case_number"].strip()

            if case_number:
                case_numbers.append(case_number)

    return case_numbers

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

        for row in reader:
            case_number = row["case_number"].strip()

            if case_number:
                case_numbers.append(case_number)

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