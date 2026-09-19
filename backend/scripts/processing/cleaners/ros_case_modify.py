import re
from pathlib import Path

import pandas as pd


def clean_ros(input_file: str | Path) -> Path:

    input_file = Path(input_file)

    output_file = input_file.with_name(
        input_file.stem + "_FINAL.xlsx"
    )

    df = pd.read_excel(input_file)

    # =========================================================
    # SPECIAL MAP
    # =========================================================

    special_map = {
        "26000369CA": "26000306CA"
    }

    # =========================================================
    # LENGTH CHECK
    # =========================================================

    def is_valid_length(case):

        return len(str(case)) <= 15

    # =========================================================
    # FORMAT FUNCTION
    # =========================================================

    def format_case(case):

        if pd.isna(case):
            return case

        raw = str(case).upper().strip()

        # =====================================================
        # REMOVE ALL SPACES
        # =====================================================

        raw = re.sub(
            r'\s+',
            '',
            raw
        )

        # =====================================================
        # SPECIAL MAP
        # =====================================================

        if raw in special_map:

            return special_map[raw]

        # =====================================================
        # CLEAN
        # =====================================================

        cleaned = re.sub(
            r'[^A-Z0-9]',
            '',
            raw
        )

        # =====================================================
        # FIX TYPE
        # C → CA
        # =====================================================

        cleaned = re.sub(
            r'(?<!S)(?<!P)(?<!C)C',
            'CA',
            cleaned
        )

        # =====================================================
        # YEAR
        # =====================================================

        year = None

        m1 = re.search(
            r'20\d{2}',
            cleaned
        )

        if m1:

            year = m1.group()

        elif re.match(
            r'\d{2}',
            cleaned
        ):

            year = "20" + cleaned[:2]

        else:

            m2 = re.search(
                r'(CA|SC|SP|CC)(\d{2})',
                cleaned
            )

            if m2:

                year = "20" + m2.group(2)

        if not year:

            return case

        # =====================================================
        # TYPE
        # =====================================================

        type_match = re.search(
            r'(CA|SC|SP|CC)',
            cleaned
        )

        if not type_match:

            return case

        case_type = type_match.group()

        # =====================================================
        # NUMBER
        # =====================================================

        parts = re.split(
            r'(CA|SC|SP|CC)',
            cleaned,
            maxsplit=1
        )

        if len(parts) < 3:

            return case

        after = parts[2]

        nums = re.findall(
            r'\d+',
            after
        )

        if not nums:

            return case

        case_no = nums[0][:6].zfill(6)

        # =====================================================
        # FINAL
        # =====================================================

        return (
            f"{year}-"
            f"{case_type}-"
            f"{case_no}"
        )

    # =========================================================
    # DETECT CASE COLUMN
    # =========================================================

    df.columns = (
        df.columns
        .str.strip()
        .str.upper()
    )

    case_col = None

    for col in [
        "ID_CASE_NUM",
        "CASE_NUMBER",
        "CASE_NUM"
    ]:

        if col in df.columns:

            case_col = col
            break

    if not case_col:

        raise ValueError(
            "No case column found"
        )

    # =========================================================
    # CLEAN INPUT CASE COLUMN
    # =========================================================

    df[case_col] = (
        df[case_col]
        .astype(str)
        .str.strip()
    )

    df[case_col] = (
        df[case_col]
        .str.replace(
            r'\s+',
            '',
            regex=True
        )
    )

    # =========================================================
    # APPLY FORMATTING
    # =========================================================

    df["MODIFIED_CASE_NUM"] = (
        df[case_col]
        .apply(format_case)
    )

    df["DOWNLOADING_REMARKS"] = ""

    # =========================================================
    # LENGTH COLUMN
    # =========================================================

    df["LENGTH"] = (
        df["MODIFIED_CASE_NUM"]
        .astype(str)
        .apply(len)
    )

    # =========================================================
    # VALIDATION
    # =========================================================

    valid_pattern = (
        r'^20\d{2}-(CA|SC|SP|CC)-\d{6}$'
    )

    length_mask = (
        df["LENGTH"] <= 15
    )

    pattern_mask = (
        df["MODIFIED_CASE_NUM"]
        .astype(str)
        .str.match(valid_pattern)
    )

    valid_mask = (
        length_mask
        & pattern_mask
    )

    # =========================================================
    # INVALID
    # =========================================================

    df.loc[
        ~valid_mask,
        "DOWNLOADING_REMARKS"
    ] = "Invalid case"

    # =========================================================
    # DUPLICATE
    # =========================================================

    dup_mask = (
        df["MODIFIED_CASE_NUM"]
        .duplicated(keep="first")
        & valid_mask
    )

    df.loc[
        dup_mask,
        "DOWNLOADING_REMARKS"
    ] = "Duplicate case"

    # =========================================================
    # COLUMN REORDER
    # =========================================================

    cols = list(df.columns)

    for col in [
        "MODIFIED_CASE_NUM",
        "DOWNLOADING_REMARKS",
        "LENGTH"
    ]:

        if col in cols:

            cols.remove(col)

    id_idx = cols.index(case_col)

    if "DEFENDANT" in cols:

        def_idx = cols.index("DEFENDANT")

        new_cols = (
            cols[:id_idx + 1]
            + [
                "MODIFIED_CASE_NUM",
                "DOWNLOADING_REMARKS",
                "LENGTH"
            ]
            + cols[id_idx + 1:def_idx]
            + cols[def_idx:]
        )

    elif "defendant" in cols:

        def_idx = cols.index("defendant")

        new_cols = (
            cols[:id_idx + 1]
            + [
                "MODIFIED_CASE_NUM",
                "DOWNLOADING_REMARKS",
                "LENGTH"
            ]
            + cols[id_idx + 1:def_idx]
            + cols[def_idx:]
        )

    else:

        new_cols = (
            cols[:id_idx + 1]
            + [
                "MODIFIED_CASE_NUM",
                "DOWNLOADING_REMARKS",
                "LENGTH"
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

    print("ROS CLEANING COMPLETED")
    print(f"Input  : {input_file}")
    print(f"Output : {output_file}")
    print(f"Rows   : {len(df)}")

    return output_file