import streamlit as st
import plotly.express as px
import pandas as pd

st.markdown("""
<style>

/* GLOBAL STYLES */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Gradient Title */
.section-title {
    font-size: 1.6rem;
    font-weight: 800;
    background: linear-gradient(90deg, #4a90e2, #6f42c1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-top: 10px;
    margin-bottom: 20px;
}

/* Gradient Cards with Hover */
.card {
    padding: 25px;
    border-radius: 18px;
    background: linear-gradient(145deg, #ffffff 0%, #f3f7ff 100%);
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    transition: all 0.3s ease;
    margin-bottom: 25px;
}

/* Hover hover hover ✨ */
.card:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 26px rgba(0,0,0,0.12);
}

/* Insight Box Gradient + Hover Glow */
.insight-box {
    background: linear-gradient(135deg, #eef2ff, #f8f9ff);
    padding: 16px;
    border-radius: 10px;
    border-left: 5px solid #4a90e2;
    font-size: 0.95rem;
    transition: all 0.3s ease;
    color: black;
}

.insight-box:hover {
    border-left-color: #6f42c1;
    box-shadow: 0 4px 18px rgba(110, 70, 193, 0.18);
    transform: translateX(4px);
}

/* Chart Image Hover Effect */
img {
    border-radius: 10px;
    transition: 0.3s ease;
}

img:hover {
    transform: scale(1.01);
    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
}

/* Subheader */
.chart-title {
    font-size: 1.25rem;
    font-weight: 700;
    margin-bottom: 8px;
}

</style>
""", unsafe_allow_html=True)

st.title("UK Road Collisions Heatmap")


st.markdown('<div class="section-title">Interactive Heatmap</div>', unsafe_allow_html=True)

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



# Display Saved Matplotlib Charts
# ======================

st.markdown('<div class="section-title">📊 Collisions Overview</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])




st.subheader("Collisions per Year & Accident Severity")

col1, col2 = st.columns([2, 1])

with col1:
    st.image("./src/images/overview_plots.png")

with col2:
    st.markdown('<div class="chart-title">Collisions per Year & Accident Severity</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
    • Displays total collisions per year  
    • Shows accident severity distribution  
    • Noticeable increase in crashes after 2020  
    • Majority of crashes are slight  
    • Fatalities remain under 5,000 per year  
    </div>
    """, unsafe_allow_html=True)


    



st.markdown('<div class="section-title">📅 Weekend vs Weekday Crashes</div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.image("./src/images/weekend_vs_weekday.png")

with col2:
    st.markdown('<div class="chart-title">Key Insights</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
    • Weekdays show a significantly higher crash rate  
    • Likely caused by commuter traffic volume  
    • Clear behavioural differences between days  
    • Helps identify high-risk time periods  
    </div>
    """, unsafe_allow_html=True)






st.markdown('<div class="section-title">🤖 Model Confusion Matrix</div>', unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])

with col1:
    st.image("./src/images/confusion_matrix.png")

with col2:
    st.markdown('<div class="chart-title">How to Read This</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
    • Rows = actual severity levels  
    • Columns = predicted severity  
    • Diagonal cells = correct predictions  
    • Off-diagonal = misclassifications  
    • Useful for assessing model reliability  
    </div>
    """, unsafe_allow_html=True)


