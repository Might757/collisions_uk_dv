import sys
from pathlib import Path
import pandas as pd
import yaml
import requests
from io import BytesIO
import zipfile


def load_cfg():
    with open("config/config.yaml", "r") as f:
        return yaml.safe_load(f)


def ensure_dir(p):
    Path(p).mkdir(parents=True, exist_ok=True)


def download_file(url, desc=""):
    print(f"Downloading {desc}... {url}")
    resp = requests.get(url, timeout=180)
    resp.raise_for_status()
    return BytesIO(resp.content)


def extract_csv_from_zip(zip_bytes, target_path):
    with zipfile.ZipFile(zip_bytes) as z:

        # This finds the accidents/collisions CSV
        candidates = [n for n in z.namelist() if n.lower().endswith(".csv") and "collision" in n.lower()]
        if not candidates:
            candidates = [n for n in z.namelist() if n.lower().endswith(".csv")]
        if not candidates:
            raise RuntimeError("No CSV found in ZIP archive.")
        csv_name = candidates[0]
        with z.open(csv_name) as src, open(target_path, "wb") as dst:
            dst.write(src.read())
        print(f"  Extracted {csv_name} → {target_path.name}")


def main():
    cfg = load_cfg()
    years = cfg["years"]
    raw_dir = Path(cfg["paths"]["raw_dir"])
    ensure_dir(raw_dir)

    # Official STATS19 collision data URLs (data.gov.uk)
    # These are the direct links to the latest published files as of Nov 2024
    # Format: {year: URL}
    urls = {
        2020: "https://data.dft.gov.uk/road-accidents-safety-data/dft-road-casualty-statistics-collision-2020.csv",
        2021: "https://data.dft.gov.uk/road-accidents-safety-data/dft-road-casualty-statistics-collision-2021.csv",
        2022: "https://data.dft.gov.uk/road-accidents-safety-data/dft-road-casualty-statistics-collision-2022.csv",
        2023: "https://data.dft.gov.uk/road-accidents-safety-data/dft-road-casualty-statistics-collision-2023.csv",
        2024: "https://data.dft.gov.uk/road-accidents-safety-data/dft-road-casualty-statistics-collision-2024.csv",
    }

    for y in years:
        csv_path = raw_dir / f"collisions_{y}.csv"
        pq_path = csv_path.with_suffix(".parquet")

        if csv_path.exists():
            print(f"Already exists: {csv_path.name} (skipping download)")
        else:
            if y not in urls:
                print(f"No URL configured for {y}; skipping.")
                continue
            url = urls[y]
            blob = download_file(url, desc=f"collisions {y}")

            # Check if it's a ZIP (some years are zipped)
            if url.lower().endswith(".zip"):
                extract_csv_from_zip(blob, csv_path)
            else:
                with open(csv_path, "wb") as f:
                    f.write(blob.getvalue())
                print(f"  Saved {csv_path.name}")

        # Convert to Parquet for faster loading
        if not pq_path.exists():
            df = pd.read_csv(csv_path, low_memory=False)
            df.to_parquet(pq_path)
            print(f"  Wrote {pq_path.name} ({len(df):,} rows)")

    print("Done. Collisions data ready in data/raw/")


if __name__ == "__main__":
    main()