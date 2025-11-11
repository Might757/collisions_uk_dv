# Collision Data Access

Source: STATS19 Collision data (DfT), UK Road Safety Data

Official dataset page: https://www.data.gov.uk/dataset/cb7ae6f0-4be6-4935-9277-47e5ce24a11f/road-safety-data

License: Open Government Licence v3 (OGL)

## How to download

Run:
```bash
python src/download_collisions.py
```

This fetches collision CSV files for configured years from data.dft.gov.uk and saves them as:
- `data/raw/collisions_{YEAR}.csv`
- `data/raw/collisions_{YEAR}.parquet` (for faster loading)

## Notes
- URLs are hardcoded in `src/download_collisions.py` for 2019–2023.
- Large files (~50–150MB per year) are gitignored; don't commit them.

## Citation
Department for Transport (DfT). Road Safety Data - Collisions. Licensed under the Open Government Licence v3.