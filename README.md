# Road Safety Hotspots and Severity Drivers (UK STATS19)

## Project overview
Decision-centric analytics to identify collision hotspots and factors associated with collision outcomes in Greater London, 2020–2024.

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

1. Run the full pipeline (data cleaning + modeling)
py -3.11 run.sh

2. Run modeling scripts
py -3.11 src/modeling.py

3. Launch interactive UK heatmap (Streamlit)
py -3.11 -m streamlit run src/heatmap.py

NOTE: i used -3.11 because I have multiple python versions, may not be the same for you guys.

Opens a local web app (http://localhost:8501) showing a UK collision hotspot heatmap.


## Project structure
```
data/
  raw/               
  clean/            
  outputs/            
  README.md

config/
  config.yaml       
  README.md    

src/
  import_collisions.py 
  clean_dataframe.py   
  modeling.py          # machine learning model (Random Forest) for severity and exploratory data analysis (EDA) charts
  heatmap.py           # Streamlit/Plotly UK hotspot heatmap
  requirements.txt     

outputs/
  (outputs of HTML instances)
  
run.sh                
README.md             
proposal_draft.md
```

## Reproduction notes
- Deterministic seeds in config.
- All intermediate datasets are saved (raw → clean → outputs).
- Document any manual download steps in `data/README.md`.

## License
Code: MIT. Data: OGL v3 (DfT STATS19). See dataset page for terms.
