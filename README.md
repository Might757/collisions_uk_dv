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

```bash
sh run.sh
```

This runs: getting the data → cleaning and reporting → EDA aggregates/figures → model → dashboard prep.

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
