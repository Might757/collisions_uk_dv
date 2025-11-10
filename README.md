# Road Safety Hotspots and Severity Drivers (UK STATS19)

## Project overview
Decision-centric analytics to identify collision hotspots and factors associated with collision outcomes in Greater London, 2000–2024.

## Data sources & licensing
- UK STATS19 (DfT) accidents/vehicles/casualties: https://www.data.gov.uk/dataset/cb7ae6f0-4be6-4935-9277-47e5ce24a11f/road-safety-data
- License: Open Government Licence v3. Include citation in report.
- We do NOT commit large raw data. See `data/README.md` to obtain.

## Environment / setup
- Python 3.10+
- Create environment:
  ```bash
  python -m venv .venv && source .venv/bin/activate
  pip install -r requirements.txt
  ```

## Config


## How to run (one command)


This runs: ingest → clean/feature → EDA aggregates/figures → model → dashboard prep.


## Project structure
```
data/
  raw/            # downloaded CSV/Parquet (gitignored)
  clean/          # cleaned tables (Parquet)
  outputs/        # aggregates, figures, model artifacts
  README.md
config/
  config.yaml
src/
  ingest_stats19.py
  clean_feature_engineer.py
  analysis_eda.py
  model_severity.py
  dashboard_streamlit.py
run.sh
requirements.txt
environment.yml (optional)
proposal_draft.md
```

## Reproduction notes
- Deterministic seeds in config.
- All intermediate datasets are saved (raw → clean → outputs).
- Document any manual download steps in `data/README.md`.

## License
Code: MIT. Data: OGL v3 (DfT STATS19). See dataset page for terms.
