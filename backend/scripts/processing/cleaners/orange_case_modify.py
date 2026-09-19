import re
from pathlib import Path

import pandas as pd


def clean_orange(input_file: str | Path) -> Path:

    input_file = Path(input_file)

    output_file = input_file.with_name(
        input_file.stem + "_ALL.xlsx"
    )

    df = pd.read_excel(input_file)

    # =========================================================
    # ORIGINAL CASE FORMATTING
    # =========================================================

    def format_case_final(case):

        if pd.isna(case):
            return "UNKNOWN"

        txt = str(case).upper().strip()

        # =====================================================
        # ALREADY CORRECT NORMAL FORMAT
        # Example:
        # 25-021960WWA
        # =====================================================

        if re.fullmatch(
            r'\d{2}-\d{6}[A-Z]+',
            txt
        ):

            return txt

        # =====================================================
        # SPECIAL CASE
        # DD-YYYY-CA-######-X
        # =====================================================

        txt_clean = re.sub(
            r'-[A-Z]$',
            '',
            txt
        )

        m = re.match(
            r'\d{1,3}-(\d{4})-(CA|SC|CC)-(\d{6})',
            txt_clean
        )

        if m:

            year = m.group(1)
            case_type = m.group(2)
            case_num = m.group(3)

            return (
                f"{year}-"
                f"{case_type}-"
                f"{case_num}-O"
            )

        # =====================================================
        # SPECIAL CASE
        # YYYYCA###### / YYYYCC######
        # =====================================================

        clean = re.sub(
            r'[^A-Z0-9]',
            '',
            txt
        )

        m2 = re.match(
            r'(\d{4})(CA|SC|CC)(\d{6})',
            clean
        )

        if m2:

            return (
                f"{m2.group(1)}-"
                f"{m2.group(2)}-"
                f"{m2.group(3)}-O"
            )

        # =====================================================
        # FALLBACK
        # =====================================================

        return txt

    # =========================================================
    # CASE COLUMN
    # =========================================================

    id_case_col = "ID_CASE_NUM"

    # =========================================================
    # MODIFIED CASE
    # =========================================================

    df["MODIFIED_CASE_NUM"] = (
        df[id_case_col]
        .apply(format_case_final)
    )

    df["DOWNLOADING_REMARKS"] = ""

    # =========================================================
    # INVALID
    # =========================================================

    df.loc[
        df["MODIFIED_CASE_NUM"].str.len() != 16,
        "DOWNLOADING_REMARKS"
    ] = "Invalid case"

    # =========================================================
    # DUPLICATE
    # =========================================================

    dup_mask = (
        df["MODIFIED_CASE_NUM"]
        .duplicated(keep="first")
        & ~df["MODIFIED_CASE_NUM"].isin(["UNKNOWN"])
        & (
            df["DOWNLOADING_REMARKS"]
            != "Invalid case"
        )
    )

    df.loc[
        dup_mask,
        "DOWNLOADING_REMARKS"
    ] = "Duplicate case"

    # =========================================================
    # UNKNOWN LOG
    # =========================================================

    unknown_cases = df[
        df["MODIFIED_CASE_NUM"] == "UNKNOWN"
    ][id_case_col].tolist()

    if unknown_cases:

        print(
            "⚠ Unknown case formats found:",
            unknown_cases
        )

    # =========================================================
    # COLUMN REORDER
    # =========================================================

    cols = list(df.columns)

    cols.remove("MODIFIED_CASE_NUM")
    cols.remove("DOWNLOADING_REMARKS")

    id_idx = cols.index(id_case_col)

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

    print("ORANGE CLEANING COMPLETED")
    print(f"Input  : {input_file}")
    print(f"Output : {output_file}")
    print(f"Rows   : {len(df)}")

    return output_file