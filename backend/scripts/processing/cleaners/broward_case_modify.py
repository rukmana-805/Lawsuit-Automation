import re
from pathlib import Path

import pandas as pd


def clean_broward(input_file: str | Path) -> Path:

    input_file = Path(input_file)

    output_file = input_file.with_name(
        input_file.stem + "_ALL.xlsx"
    )

    df = pd.read_excel(input_file)

    # ---------------------------------------------------------
    # ORIGINAL BROWARD LOGIC
    # ---------------------------------------------------------

    def make_modified_case(case):

        if pd.isna(case):
            return ""

        original_txt = str(case).upper().strip()

        txt = re.sub(r'\(.*?\)', '', original_txt)
        txt = re.sub(r'DIVISION[:\s]*\d+', '', txt)
        txt = re.sub(r'[*.,\-\/]', ' ', txt)
        txt = re.sub(r'\s+', ' ', txt).strip()

        prefixes = [
            "CACE",
            "COCE",
            "COSO",
            "COWE",
            "CONO",
            "COINX",
            "CA"
        ]

        prefix = next(
            (p for p in prefixes if p in txt),
            None
        )

        if prefix == "CA":
            prefix = "CACE"

        year_match = re.search(
            r'\b(\d{2})\b',
            txt
        )

        year = (
            year_match.group(1)
            if year_match
            else ""
        )

        # -----------------------------------------------------
        # COINX LOGIC
        # -----------------------------------------------------

        if prefix == "COINX":

            nums = re.findall(
                r'\d+',
                txt
            )

            if len(nums) >= 2:

                year = nums[0]
                case_num = nums[1]

            elif len(nums) == 1:

                case_num = nums[0]

            else:

                return original_txt

            return f"{prefix}{year}{case_num.zfill(6)}"

        # -----------------------------------------------------
        # NORMAL PREFIX LOGIC
        # -----------------------------------------------------

        if not prefix or not year:
            return original_txt

        nums = re.findall(
            r'\d+',
            txt
        )

        nums = [
            n for n in nums
            if n != year
        ]

        case_num = (
            max(nums, key=len)
            if nums
            else ""
        )

        if not case_num:
            return original_txt

        return f"{prefix}{year}{case_num.zfill(6)}"

    # ---------------------------------------------------------
    # CREATE MODIFIED CASE NUMBER
    # ---------------------------------------------------------

    df["MODIFIED_CASE_NUM"] = (
        df["ID_CASE_NUM"].apply(make_modified_case)
    )

    # ---------------------------------------------------------
    # DOWNLOADING REMARKS
    # ---------------------------------------------------------

    df["DOWNLOADING_REMARKS"] = ""

    valid_length_mask = (
        df["MODIFIED_CASE_NUM"]
        .str.len()
        .isin([12, 13])
    )

    df.loc[
        ~valid_length_mask,
        "DOWNLOADING_REMARKS"
    ] = "invalid case"

    # ---------------------------------------------------------
    # DUPLICATE CASE LOGIC
    # ---------------------------------------------------------

    dup_mask = (
        df["MODIFIED_CASE_NUM"].duplicated(
            keep="first"
        )
        & valid_length_mask
    )

    df.loc[
        dup_mask,
        "DOWNLOADING_REMARKS"
    ] = "Duplicate case"

    # ---------------------------------------------------------
    # COLUMN ORDER
    # ---------------------------------------------------------
    #
    # Original requirement:
    # MODIFIED_CASE_NUM
    # DOWNLOADING_REMARKS
    #
    # should be after ID_CASE_NUM
    # and before DEFENDANT.
    #
    # Your actual generated Excel has:
    # ID_CASE_NUM
    # defendant
    #
    # so we use the actual column name "defendant".
    # ---------------------------------------------------------

    modified_case = df.pop(
        "MODIFIED_CASE_NUM"
    )

    downloading_remarks = df.pop(
        "DOWNLOADING_REMARKS"
    )

    defendant_index = df.columns.get_loc(
        "defendant"
    )

    df.insert(
        defendant_index,
        "MODIFIED_CASE_NUM",
        modified_case
    )

    df.insert(
        defendant_index + 1,
        "DOWNLOADING_REMARKS",
        downloading_remarks
    )

    # ---------------------------------------------------------
    # SAVE OUTPUT
    # ---------------------------------------------------------

    df.to_excel(
        output_file,
        index=False,
        engine="openpyxl"
    )

    print("BROWARD CLEANING COMPLETED")
    print(f"Input  : {input_file}")
    print(f"Output : {output_file}")
    print(f"Rows   : {len(df)}")

    return output_file