import re
from pathlib import Path

import pandas as pd


def clean_hillsborough(input_file: str | Path) -> Path:

    input_file = Path(input_file)

    output_file = input_file.with_name(
        input_file.stem + "_output.xlsx"
    )

    df = pd.read_excel(input_file)

    # =========================================================
    # ORIGINAL FORMAT FUNCTION
    # =========================================================

    def format_case_unified(case):

        if pd.isna(case):
            return case

        raw = (
            str(case)
            .upper()
            .replace(' ', '')
            .replace('–', '-')
            .replace('--', '-')
        )

        # -------- CA CASES --------

        m_ca = re.match(
            r'(20)?(\d{2})-?CA-?(\d+)',
            raw
        )

        if m_ca:

            year = m_ca.group(2)
            case_no = m_ca.group(3).zfill(6)

            return f"{year}-CA-{case_no}"

        # -------- SP/CC CASES --------

        m_spcc = re.match(
            r'(20)?(\d{2})-?(SP|CC)-?(\d+)-?(\d+)?',
            raw
        )

        if m_spcc:

            year = m_spcc.group(2)
            case_type = m_spcc.group(3)
            case_no = m_spcc.group(4).zfill(6)
            section = m_spcc.group(5)

            section_str = (
                f"-{section.zfill(2)}"
                if section
                else ""
            )

            return (
                f"{year}-{case_type}-"
                f"{case_no}{section_str}"
            )

        # -------- FALLBACK --------

        return case

    # =========================================================
    # APPLY FORMATTING
    # =========================================================

    df["MODIFIED_CASE_NUM"] = (
        df["ID_CASE_NUM"]
        .apply(format_case_unified)
    )

    df["DOWNLOADING_REMARKS"] = ""

    # =========================================================
    # INVALID CASE
    # =========================================================

    invalid_mask = ~df["MODIFIED_CASE_NUM"].str.match(
        r'\d{2}-(CA|SP|CC)-\d{6}(-\d{2})?$'
    )

    df.loc[
        invalid_mask,
        "DOWNLOADING_REMARKS"
    ] = "Invalid case"

    # =========================================================
    # DUPLICATE CASE
    # =========================================================

    dup_mask = (
        df["MODIFIED_CASE_NUM"].duplicated(
            keep="first"
        )
        & ~invalid_mask
    )

    df.loc[
        dup_mask,
        "DOWNLOADING_REMARKS"
    ] = "Duplicate case"

    # =========================================================
    # FALLBACK LOG
    # =========================================================

    fallback_cases = df[
        df["MODIFIED_CASE_NUM"] == df["ID_CASE_NUM"]
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

    # Actual generated LSOP files use lowercase "defendant"
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

    print("HILLSBOROUGH CLEANING COMPLETED")
    print(f"Input  : {input_file}")
    print(f"Output : {output_file}")
    print(f"Rows   : {len(df)}")

    return output_file