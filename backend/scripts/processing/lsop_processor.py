from datetime import datetime
from pathlib import Path

import pandas as pd
from config import LAWSUIT_INDEX

# LAWSUIT_INDEX = Path(
#     r"C:\Users\Rukmana\Documents\Lawsuit Reports\Files\index_lawsuits_20250121.xlsx"
# )

TARGET_COUNTIES = [
    "ORANGE",
    "DADE",
    "HILLSBOROUGH",
    "BROWARD",
]


def process_lsop_csv(
    lsop_file: str | Path,
    date_from: str,
    date_to: str,
) -> dict[str, Path]:

    lsop_path = Path(lsop_file)

    # Rename downloaded CSV according to report date
    date_from_obj = datetime.strptime(
        date_from,
        "%m/%d/%Y"
    ).date()

    date_to_obj = datetime.strptime(
        date_to,
        "%m/%d/%Y"
    ).date()

    new_csv_name = (
        f"LSOPReport_"
        f"{date_from_obj.strftime('%Y%m%d')}_"
        f"{date_to_obj.strftime('%Y%m%d')}.csv"
    )

    new_csv_path = lsop_path.parent / new_csv_name

    # Rename only if the name is different
    if lsop_path != new_csv_path:
        lsop_path.rename(new_csv_path)
        lsop_path = new_csv_path

    print("\n" + "=" * 70)
    print("STARTING LSOP PROCESSING")
    print("=" * 70)

    if not lsop_path.exists():
        raise FileNotFoundError(
            f"LSOP CSV not found: {lsop_path}"
        )

    if not LAWSUIT_INDEX.exists():
        raise FileNotFoundError(
            f"Lawsuit index not found: {LAWSUIT_INDEX}"
        )

    date_range = (
        datetime.strptime(date_from, "%m/%d/%Y").strftime("%Y%m%d")
        + "_"
        + datetime.strptime(date_to, "%m/%d/%Y").strftime("%Y%m%d")
    )

    print("LSOP file:", lsop_path)
    print("Date range:", date_range)

    # Read LSOP CSV
    lsop_file_df = pd.read_csv(
        lsop_path,
        skiprows=3,
    )

    print("LSOP rows:", lsop_file_df.shape[0])

    # Read lawsuit index
    lawsuit_index = pd.read_excel(
        LAWSUIT_INDEX,
        sheet_name=None,
    )

    # County mapping
    county_mapping_df = lawsuit_index["mapping"].copy()

    county_mapping_df["NAME_COUNTY"] = (
        county_mapping_df["NAME_COUNTY"]
        .astype(str)
        .str.upper()
        .str.strip()
    )

    # Defendant mapping
    company_mapping_df = lawsuit_index["defendent"].copy()

    company_mapping_df["defendent"] = (
        company_mapping_df["defendent"]
        .astype(str)
        .str.strip()
    )

    lsop_file_df["defendant"] = (
        lsop_file_df["defendant"]
        .astype(str)
        .str.strip()
    )

    # Merge defendant
    result_df = pd.merge(
        lsop_file_df,
        company_mapping_df,
        left_on="defendant",
        right_on="defendent",
        how="inner",
    )

    print(
        "Rows after defendant merge:",
        result_df.shape[0],
    )

    # Merge county
    result_df_1 = result_df.merge(
        county_mapping_df,
        on="NAME_COUNTY",
        how="inner",
    )

    print(
        "Rows after county merge:",
        result_df_1.shape[0],
    )

    # Categorize
    result_df_1["Category"] = (
        result_df_1["NAME_COUNTY_MAPPING"]
        .astype(str)
        .str.upper()
        .str.strip()
        .apply(
            lambda value:
            value if value in TARGET_COUNTIES else "ROS"
        )
    )

    # Remove duplicates
    result_df_1 = result_df_1.drop_duplicates()

    # Split
    df_orange = result_df_1[
        result_df_1["Category"] == "ORANGE"
    ]

    df_dade = result_df_1[
        result_df_1["Category"] == "DADE"
    ]

    df_hillsborough = result_df_1[
        result_df_1["Category"] == "HILLSBOROUGH"
    ]

    df_broward = result_df_1[
        result_df_1["Category"] == "BROWARD"
    ]

    df_other = result_df_1[
        result_df_1["Category"] == "ROS"
    ]

    # Save beside the downloaded CSV
    output_dir = lsop_path.parent

    output_files = {
        "Orange": output_dir / f"Orange_{date_range}.xlsx",
        "Dade": output_dir / f"Dade_{date_range}.xlsx",
        "Hillsborough": (
            output_dir / f"Hillsborough_{date_range}.xlsx"
        ),
        "Broward": output_dir / f"Broward_{date_range}.xlsx",
        "ROS": output_dir / f"ROS_{date_range}.xlsx",
    }

    df_orange.to_excel(
        output_files["Orange"],
        index=False,
    )

    df_dade.to_excel(
        output_files["Dade"],
        index=False,
    )

    df_hillsborough.to_excel(
        output_files["Hillsborough"],
        index=False,
    )

    df_broward.to_excel(
        output_files["Broward"],
        index=False,
    )

    df_other.to_excel(
        output_files["ROS"],
        index=False,
    )

    print("\nProcessing completed.")
    print("Orange:", len(df_orange))
    print("Dade:", len(df_dade))
    print("Hillsborough:", len(df_hillsborough))
    print("Broward:", len(df_broward))
    print("ROS:", len(df_other))

    return output_files


# if __name__ == "__main__":
#     process_lsop_csv(
#         r"C:\Users\Rukmana\Documents\Lawsuit Reports\2026\SEPTEMBER\1ST\LSOP_Detail_Served_Report.csv",
#         "09/01/2026",
#         "09/15/2026",
#     )
