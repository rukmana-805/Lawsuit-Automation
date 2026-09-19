import re
from pathlib import Path

import pandas as pd


def clean_dade(input_file: str | Path) -> Path:

    input_file = Path(input_file)

    output_file = input_file.with_name(
        input_file.stem + "_output.xlsx"
    )

    df = pd.read_excel(input_file)

    # =========================================================
    # ORIGINAL CASE FORMATTING FUNCTION
    # =========================================================

    def make_modified_case(case):

        if pd.isna(case):
            return case

        raw = str(case).upper().strip()

        # remove brackets
        raw = re.sub(
            r'\(.*?\)',
            '',
            raw
        )

        # remove spaces
        raw = re.sub(
            r'\s+',
            '',
            raw
        )

        # =====================================================
        # YEAR
        # =====================================================

        year_match = re.match(
            r'(19\d{2}|20\d{2}|\d{2})',
            raw
        )

        if not year_match:
            return case

        yr = year_match.group()

        year = (
            "20" + yr
            if len(yr) == 2
            else yr
        )

        # =====================================================
        # CASE TYPE
        # =====================================================

        if "CA" in raw:

            case_type = "CA"

        elif "SP" in raw:

            case_type = "SP"

        elif "CC" in raw:

            case_type = "CC"

        else:

            return case

        # =====================================================
        # CASE NUMBER
        # =====================================================

        pattern = rf'{yr}(\d{{6}}){case_type}'

        match = re.search(
            pattern,
            raw
        )

        if match:

            case_no = match.group(1).zfill(6)

        else:

            nums = re.findall(
                r'\d+',
                raw
            )

            if len(nums) >= 2:

                case_no = nums[1].zfill(6)

            elif len(nums) == 1:

                case_no = nums[0].zfill(6)

            else:

                return case

        # =====================================================
        # SECTION
        # =====================================================

        if case_type == "CA":

            # CA section forced to 01
            section = "01"

        else:

            # SP/CC section from original ID_CASE_NUM

            sec_match = re.search(
                rf'{case_type}-?(\d+)',
                raw
            )

            if sec_match:

                section = sec_match.group(1).zfill(2)

            else:

                section = "01"

        # =====================================================
        # FINAL
        # =====================================================

        final = (
            f"{year}-"
            f"{case_no}-"
            f"{case_type}-"
            f"{section}"
        )

        return final

    # =========================================================
    # APPLY FORMATTING
    # =========================================================

    df["MODIFIED_CASE_NUM"] = (
        df["ID_CASE_NUM"]
        .apply(make_modified_case)
    )

    df["DOWNLOADING_REMARKS"] = ""

    # =========================================================
    # INVALID
    # =========================================================

    invalid_mask = (
        df["MODIFIED_CASE_NUM"].str.len() != 17
    )

    df.loc[
        invalid_mask,
        "DOWNLOADING_REMARKS"
    ] = "Invalid case"

    # =========================================================
    # DUPLICATE
    # =========================================================

    dup_mask = (
        df["MODIFIED_CASE_NUM"]
        .duplicated(keep="first")
        & (
            df["MODIFIED_CASE_NUM"].str.len()
            == 17
        )
    )

    df.loc[
        dup_mask,
        "DOWNLOADING_REMARKS"
    ] = "Duplicate case"

    # =========================================================
    # FALLBACK LOG
    # =========================================================

    fallback_cases = df[
        df["MODIFIED_CASE_NUM"]
        == df["ID_CASE_NUM"]
    ]["ID_CASE_NUM"].tolist()

    if fallback_cases:

        print(
            "⚠ Cases fallback to ID_CASE_NUM "
            f"(could not parse): {fallback_cases}"
        )

    # =========================================================
    # COLUMN REORDER
    # =========================================================

    cols = list(df.columns)

    cols.remove("MODIFIED_CASE_NUM")
    cols.remove("DOWNLOADING_REMARKS")

    id_idx = cols.index("ID_CASE_NUM")

    if "defendant" in cols:

        def_idx = cols.index("defendant")

        new_cols = (
            cols[:id_idx + 1]
            + [
                "MODIFIED_CASE_NUM",
                "DOWNLOADING_REMARKS"
            ]
            + cols[id_idx + 1:def_idx]
            + cols[def_idx:]
        )

    else:

        new_cols = (
            cols[:id_idx + 1]
            + [
                "MODIFIED_CASE_NUM",
                "DOWNLOADING_REMARKS"
            ]
            + cols[id_idx + 1:]
        )

    df = df[new_cols]

    # =========================================================
    # EXPORT
    # =========================================================

    df.to_excel(
        output_file,
        index=False,
        engine="openpyxl"
    )

    print("DADE CLEANING COMPLETED")
    print(f"Input  : {input_file}")
    print(f"Output : {output_file}")
    print(f"Rows   : {len(df)}")

    return output_file