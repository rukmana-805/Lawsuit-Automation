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