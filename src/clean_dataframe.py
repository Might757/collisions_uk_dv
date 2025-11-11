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

def validate_severity(df):
    """
    Standardize collision_severity and create binary serious_or_fatal flag.
    :param df: dataframe being changed
    :return: dataframe with binary serious_or_fatal flag
    """
    sev_col = "collision_severity" if "collision_severity" in df.columns else "Collision_Severity"
    # Map to standard labels (handle both text and numeric codes)
    severity_map = {
        "1": "Fatal",
        "2": "Serious",
        "3": "Slight",
        "Fatal": "Fatal",
        "Serious": "Serious",
        "Slight": "Slight"
    }
    df[sev_col] = df[sev_col].astype(str).map(severity_map)

    # Drop any rows with no severity
    before = len(df)
    df = df[df[sev_col].notna()]
    after = len(df)
    if before > after:
        print(f"  Severity validation: {before - after} rows removed (invalid severity)")

    # Create binary target
    df["serious_or_fatal"] = df[sev_col].isin(["Fatal", "Serious"]).astype(int)
    return df


def clean_categorical(df):
    """Clean and validate key categorical columns.
    :param df: dataframe being changed
    :return: dataframe with categorical columns
    """
    cat_cols = [
        "weather_conditions", "Weather_Conditions",
        "light_conditions", "Light_Conditions",
        "road_surface_conditions", "Road_Surface_Conditions",
        "road_type", "Road_Type",
        "urban_or_rural_area", "Urban_or_Rural_Area"
    ]

    for col in cat_cols:
        if col in df.columns:
            # Replace -1 or "Data missing" with NaN
            df[col] = df[col].replace([-1, "-1", "Data missing or out of range"], pd.NA)
            # Convert to category dtype
            df[col] = df[col].astype("category")

    return df


def clean_numeric(df):
    """Validate numeric columns.
    :param df: dataframe being changed
    :return: dataframe with numeric columns
    """
    num_cols = {
        "speed_limit": (0, 80),
        "Speed_limit": (0, 80),
        "number_of_vehicles": (1, 100),
        "Number_of_Vehicles": (1, 100),
        "number_of_casualties": (1, 100),
        "Number_of_Casualties": (1, 100)
    }

    for col, (min_val, max_val) in num_cols.items():
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            # Flag outliers as NaN
            df.loc[(df[col] < min_val) | (df[col] > max_val), col] = pd.NA

    return df


def select_final_columns(df):
    """
    Keep only relevant columns for downstream analysis.
    :param df: dataframe being changed
    :return: dataframe with final columns
    """
    # Map to standardized names
    col_map = {
        "Latitude": "latitude",
        "Longitude": "longitude",
        "collision_severity": "accident_severity",  # Changed this line
        "Speed_limit": "speed_limit",
        "speed_limit": "speed_limit",  # Added lowercase version
        "Weather_Conditions": "weather_conditions",
        "weather_conditions": "weather_conditions",
        "Light_Conditions": "light_conditions",
        "light_conditions": "light_conditions",
        "Road_Surface_Conditions": "road_surface_conditions",
        "road_surface_conditions": "road_surface_conditions",
        "Road_Type": "road_type",
        "road_type": "road_type",
        "Urban_or_Rural_Area": "urban_or_rural_area",
        "urban_or_rural_area": "urban_or_rural_area",
        "Number_of_Vehicles": "number_of_vehicles",
        "number_of_vehicles": "number_of_vehicles",
        "Number_of_Casualties": "number_of_casualties",
        "number_of_casualties": "number_of_casualties",
        "Junction_Detail": "junction_detail",
        "junction_detail": "junction_detail",
        "Junction_Control": "junction_control",
        "junction_control": "junction_control",
        "1st_Road_Class": "road_class_1",
        "first_road_class": "road_class_1",
        "1st_Road_Number": "road_number_1",
        "first_road_number": "road_number_1"
    }

    df = df.rename(columns=col_map)

    keep = [
        "latitude", "longitude", "datetime", "year", "month", "day_of_week", "hour",
        "accident_severity", "serious_or_fatal",
        "number_of_vehicles", "number_of_casualties",
        "speed_limit", "weather_conditions", "light_conditions", "road_surface_conditions",
        "road_type", "urban_or_rural_area", "junction_detail", "junction_control",
        "road_class_1", "road_number_1"
    ]

    # Keep only columns that exist
    keep = [c for c in keep if c in df.columns]
    return df[keep].copy()


def generate_data_quality_report(df_raw, df_clean, output_path):
    """Generate a text report of data quality issues."""
    report = []
    report.append("=" * 60)
    report.append("DATA QUALITY REPORT")
    report.append("=" * 60)
    report.append(f"Raw records loaded: {len(df_raw):,}")
    report.append(f"Clean records output: {len(df_clean):,}")
    report.append(f"Records removed: {len(df_raw) - len(df_clean):,} ({100 * (1 - len(df_clean) / len(df_raw)):.1f}%)")
    report.append("")
    report.append("Missing values in clean dataset:")
    missing = df_clean.isnull().sum()
    missing = missing[missing > 0].sort_values(ascending=False)
    for col, count in missing.items():
        report.append(f"  {col}: {count:,} ({100 * count / len(df_clean):.1f}%)")
    report.append("")
    report.append("Severity distribution:")
    if "accident_severity" in df_clean.columns:
        for sev, count in df_clean["accident_severity"].value_counts().items():
            report.append(f"  {sev}: {count:,}")
    report.append("")
    report.append("Year distribution:")
    for yr, count in df_clean["year"].value_counts().sort_index().items():
        report.append(f"  {yr}: {count:,}")
    report.append("=" * 60)

    with open(output_path, "w") as f:
        f.write("\n".join(report))
    print(f"Data quality report saved: {output_path}")


def generate_data_dictionary(df, output_path):
    """Generate CSV data dictionary."""
    dict_data = {
        "column": df.columns,
        "dtype": [str(df[c].dtype) for c in df.columns],
        "non_null_count": [df[c].notna().sum() for c in df.columns],
        "null_count": [df[c].isna().sum() for c in df.columns],
        "example_values": [df[c].dropna().head(3).tolist() if len(df[c].dropna()) > 0 else [] for c in df.columns]
    }
    dict_df = pd.DataFrame(dict_data)
    dict_df.to_csv(output_path, index=False)
    print(f"Data dictionary saved: {output_path}")


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
    df = clean_coordinates(df)
    df = filter_region(df, cfg["project"]["local_authorities"])
    df = validate_severity(df)
    df = clean_categorical(df)
    df = clean_numeric(df)
    df = select_final_columns(df)
    print(df.head(5))
    print(f"\nFinal clean dataset: {len(df):,} records, {len(df.columns)} columns")

    # Save clean data as CSV
    clean_path = clean_dir / "collisions_clean.csv"
    df.to_csv(clean_path, index=False)
    print(f"Clean data saved: {clean_path}")

    # Generate reports
    generate_data_quality_report(df_raw, df, outputs_dir / "data_quality_report.txt")
    generate_data_dictionary(df, outputs_dir / "data_dictionary.csv")

    print("\nData cleaning complete")


if __name__ == "__main__":
    main()