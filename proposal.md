# Project Proposal
## Team Name: Insight Squad
## Project Title: Assignment 2 — Team Data Analytics & Visualization Project

### Stakeholder & Decision Context
We will visualize automobile crashes across the UK using an interactive heatmap, complemented by breakdowns of causation factors and casualty counts. The primary audience includes road safety organizations (e.g., Road Safety Authority) and policy makers who need to understand crash “hot spots,” causal drivers, and severity patterns to prioritize preventive action and allocate resources effectively.

### Primary Question & Success Metrics

#### Primary Questions
- Where are the high volumes of crashes across the UK?
- How can visualization help prioritize preventive action across locations, time periods, and conditions?

#### Success Metrics
- An interactive heatmap that clearly showcases crash intensity for years 2020–2025.
- Descriptive analytics indicating how, where, and when crashes occur (e.g., by region, road type, day of week, weather).
- Visualizations and narratives that inform safety planning, including actionable insights (e.g., top hotspot clusters, peak times, high-risk conditions).
- Usability: filters for year, conditions, and casualty severity with responsive performance (target <2s interaction latency on typical hardware).

### Datasets

- Source: STATS19 Collision data (Department for Transport, UK)
- License: Open Government Licence
- Approx. Size: ~500,000 rows (subset depending on years used)
- Key Fields: `longitude`, `latitude`, `date`, `day_of_week`, `casualties`, `severity`, `weather_conditions`, `road_type`, `speed_limit`, `light_conditions`
- Refresh Frequency: Static (for the scope of this assignment; can be extended to periodic refresh if new releases are available)

### Methods

1. Data Ingestion & Cleaning
   - Load STATS19 datasets for 2020–2025.
   - Handle missing values, normalize categorical fields (e.g., conditions), validate geospatial coordinates.
   - Deduplicate records and align schema across years.

2. Exploratory Data Analysis (EDA)
   - Summary statistics and distributions (casualties, severity, temporal patterns).
   - Spatial EDA (regional clustering, urban vs rural patterns).
   - Correlation analysis between conditions (weather, light, speed limit) and crash counts/severity.

3. Data Visualization Pipeline
   - Preprocessing for geospatial rendering (project coordinates, tile providers).
   - Generate aggregated grids or density estimates for heatmaps (e.g., KDE or hexbin).
   - Implement year and condition filters; optionally add severity and time-of-day facets.

4. Interactive Heatmap
   - Build an interactive map showing collision density across the UK.
   - Provide tooltips for hotspot regions (e.g., counts, severity mix).
   - Controls for filtering by year, condition, and severity; optional time slider for month/quarter.

5. Reporting & Web Page
   - Create a webpage that explains methodology, data sources, and interpretation guidance.
   - Include key visuals: heatmap, trend charts, bar charts by conditions, and casualty severity breakdowns.
   - Document limitations and assumptions; provide recommendations for safety planning.

### Technical Stack (Proposed)
- Data: CSV/Parquet STATS19 files
- Processing: Python (pandas, geopandas), optional Spark for scalability
- Visualization: Folium/Leaflet or kepler.gl/Deck.gl, Plotly for charts
- Web: Static site (e.g., Markdown + static generator) or lightweight Flask/Streamlit app
- Mapping: OpenStreetMap tiles; optional Mapbox/Carto if needed

### Risks / Assumptions

- Data Quality
  - Missing or inconsistent entries; geospatial inaccuracies; variant categorical codes across years.
- Schema Alignment
  - Some fields may not align perfectly between years, requiring mapping and normalization.
- Performance & UX
  - Rendering large datasets may cause latency; may require aggregation, tiling, or server-side precomputation.
- Stakeholder Access
  - Assumes stakeholders can access visualization tools via a modern browser and have basic familiarity with interactive dashboards.
- Ethical & Privacy
  - Data is aggregated and publicly licensed; ensure no inadvertent identification of individuals or sensitive locations.

### Deliverables

- Cleaned, documented dataset (or preprocessing scripts).
- Interactive heatmap with filters (year, conditions, severity).
- EDA report with key findings and visuals.
- Webpage that explains the approach and provides decision support insights.
- README with instructions to run the visualization locally.

### Timeline (Indicative)

- Week 1: Data acquisition, cleaning plan, schema alignment.
- Week 2: EDA and preliminary visuals; finalize visualization stack.
- Week 3: Build interactive heatmap and filters; performance tuning.
- Week 4: Webpage integration, documentation, and final polish.

### Evaluation

- Accuracy: Consistent geospatial mapping and correct aggregation.
- Clarity: Intuitive visuals with clear legends and guidance.
- Actionability: Insights that can inform safety interventions (e.g., targeted enforcement, infrastructure changes).
- Performance: Smooth interaction under typical stakeholder usage.
