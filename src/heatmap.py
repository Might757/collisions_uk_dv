import streamlit as st
import plotly.express as px
import pandas as pd

st.title("UK Road Collisions Heatmap")

df = pd.read_csv("data/clean/collisions_clean.csv")
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

year_filter = st.slider("Select Year", int(df['year'].min()), int(df['year'].max()), int(df['year'].min()))
df = df[df['year'] == year_filter]

fig = px.density_mapbox(
    df,
    lat='latitude',
    lon='longitude',
    z='number_of_casualties',
    radius=10,
    center=dict(lat=54.5, lon=-2),
    zoom=5,
    mapbox_style="carto-positron",
)

st.plotly_chart(fig)
fig.write_html("outputs/uk_collisions_heatmap.html")
