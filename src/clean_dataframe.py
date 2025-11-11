import pandas as pd
import numpy as np
from pathlib import Path
import yaml
# To preview dataframe in IDE
from tabulate import tabulate

from import_collisions import load_cfg


def load_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def load_raw_collisions(raw_dir, years):
    """
    Load and concatenate raw collision CSV files
    :param raw_dir: directory of raw collision files
    :param years: year of collision file
    :return: Concatenated collision dataframe
    """
    dfs = []
    for year in years:
        p = Path(raw_dir) / f"collisions_{year}.csv"
        if not p.exists():
            print(f"Warning: {p} not found, skipping year {year}")
            continue
        df = pd.read_csv(p, low_memory = False)
        dfs.append(df)
    return pd.concat(dfs, ignore_index = True)

def standardize_col(df):
    """
    Standardize the column names by removing whitespaces and replacing them with underscores.
    :param df: dataframe being changed
    :return: dataframe with standardized columns
    """
    df.columns = [c.strip().replace(" ", "_") for c in df.columns]
    return df

def parse_datetime(df):
    """
    Parse the date and the time into datetime;
    Handle missing Time.
    :param df: Dataframe being changed
    :return: Dataframe with datetime columns corrected
    """
    date_col = "date" if "date" in df.columns else "Date"
    time_col = "time" if "time" in df.columns else "Time"

    # Replace missing or invalid time with "00:00"
    df[time_col] = df[time_col].fillna("00:00").replace(["-1", "-"], "00:00")

    dt = pd.to_datetime(
        df[date_col].astype(str) + " " + df[time_col].astype(str),
        errors = "coerce",
        dayfirst = True
    )

    df["datetime"] = dt
    df["year"] = dt.dt.year
    df["month"] = dt.dt.month
    df["day_of_week"] = dt.dt.dayofweek
    df["hour"] = dt.dt.hour
    return df

def clean_coordinates(df):
    """
    Filter out rows with missing or invalid coordinates.
    :param df: Dataframe being changed
    :return: Dataframe with coordinates columns corrected
    """
    lat_col = "latitude" if "latitude" in df.columns else "Latitude"
    lon_col = "longitude" if "longitude" in df.columns else "Longitude"

    before = len(df)

    df = df[df[lat_col].notna() & df[lon_col].notna()]
    df = df[(df[lat_col] > 49) & (df[lat_col] < 61)]
    df = df[(df[lon_col] > -8) & (df[lon_col] < 2)]
    after = len(df)
    print(f"Coordinate cleaning: {before - after:,} rows removed (missing or out-of-bounds)")
    return df

def filter_region(df, local_authorities):
    """
    Filter to specified local authorities"
    :param df: dataframe being changed
    :param local_authorities: local authorities
    :return: dataframe with filtered columns
    """
    if not local_authorities:
        return df

    # Find local authority column
    la_cols = [c for c in df.columns if "local_authority" in c.lower()]
    if not la_cols:
        print(" Warning: No local authority column found")
        return df

    before = len(df)
    mask = False
    for la in local_authorities:
        for col in la_cols:
            mask = mask | df[col].astype(str).str.contains(la, case=False, na=False)
    df = df[mask].copy()
    after = len(df)
    print(f"  Region filter: kept {after:,} / {before:,} rows")
    return df


def main():
    cfg = load_cfg()
    raw_dir = cfg["paths"]["raw_dir"]
    clean_dir = Path(cfg["paths"]["clean_dir"])
    outputs_dir = Path(cfg["paths"]["outputs_dir"])
    clean_dir.mkdir(parents=True, exist_ok=True)
    outputs_dir.mkdir(parents=True, exist_ok=True)

    print("Loading raw collision data...")
    df_raw = load_raw_collisions(raw_dir, cfg["years"])
    print(f"Loaded {len(df_raw):,} raw records")

    print("\nCleaning pipeline:")
    df = standardize_col(df_raw.copy())
    df = parse_datetime(df)
    # df = clean_coordinates(df)
    # df = filter_region(df, cfg["project"]["local_authorities"])
    # df = validate_severity(df)
    # df = clean_categorical(df)
    # df = clean_numeric(df)
    # df = select_final_columns(df)
    print(df.head(5))
    print(f"\nFinal clean dataset: {len(df):,} records, {len(df.columns)} columns")

    # Save clean data as CSV
    clean_path = clean_dir / "collisions_clean.csv"
    df.to_csv(clean_path, index=False)
    print(f"Clean data saved: {clean_path}")

    # Generate reports
    # generate_data_quality_report(df_raw, df, outputs_dir / "data_quality_report.txt")
    # generate_data_dictionary(df, outputs_dir / "data_dictionary.csv")

    print("\nData cleaning complete")


if __name__ == "__main__":
    main()