from pathlib import Path

from scripts.processing.cleaners.broward_case_modify import clean_broward
from scripts.processing.cleaners.miami_dade_case_modify import clean_dade
from scripts.processing.cleaners.hillsborough_case_modify import clean_hillsborough
from scripts.processing.cleaners.orange_case_modify import clean_orange
from scripts.processing.cleaners.ros_case_modify import clean_ros


def run_cleaning_pipeline(processed_files: dict[str, Path]) -> dict[str, Path]:

    print("\n" + "=" * 60)
    print("STARTING COUNTY CLEANING")
    print("=" * 60)

    cleaned_files = {}

    # Broward
    if "Broward" in processed_files:
        cleaned_files["Broward"] = clean_broward(
            processed_files["Broward"]
        )

    # Dade
    if "Dade" in processed_files:
        cleaned_files["Dade"] = clean_dade(
            processed_files["Dade"]
        )

    # Hillsborough
    if "Hillsborough" in processed_files:
        cleaned_files["Hillsborough"] = clean_hillsborough(
            processed_files["Hillsborough"]
        )

    # Orange
    if "Orange" in processed_files:
        cleaned_files["Orange"] = clean_orange(
            processed_files["Orange"]
        )

    # ROS
    if "ROS" in processed_files:
        cleaned_files["ROS"] = clean_ros(
            processed_files["ROS"]
        )

    print("\n" + "=" * 60)
    print("ALL CLEANING COMPLETED")
    print("=" * 60)

    for county, file_path in cleaned_files.items():
        print(f"{county}: {file_path}")

    return cleaned_files