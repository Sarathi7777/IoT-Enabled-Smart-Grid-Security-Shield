import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Geospatial Threat Map", page_icon="🌍", layout="wide")

st.title("🌍 Global Threat Map")
st.markdown("---")

st.info("Visualizing real-time attack origins based on IP geolocation (Simulated).")

# Simulate data if not present
if "map_data" not in st.session_state:
    # Generate random coordinates
    n_points = 50
    lats = np.random.uniform(-50, 70, n_points)
    lons = np.random.uniform(-120, 140, n_points)
    statuses = np.random.choice(['Normal', 'Attack'], n_points, p=[0.7, 0.3])
    
    st.session_state.map_data = pd.DataFrame({
        'lat': lats,
        'lon': lons,
        'status': statuses
    })

# Refresh button
if st.button("Refresh Threat Data"):
    # Generate new random coordinates on refresh
    n_points = 50
    lats = np.random.uniform(-50, 70, n_points)
    lons = np.random.uniform(-120, 140, n_points)
    statuses = np.random.choice(['Normal', 'Attack'], n_points, p=[0.7, 0.3])
    st.session_state.map_data = pd.DataFrame({
        'lat': lats,
        'lon': lons,
        'status': statuses
    })
    st.rerun()

df = st.session_state.map_data

# Metrics
col1, col2, col3 = st.columns(3)
total_ips = len(df)
active_threats = len(df[df['status'] == 'Attack'])
safe_nodes = total_ips - active_threats

col1.metric("Monitored Nodes", total_ips)
col2.metric("Active Threats", active_threats, delta_color="inverse")
col3.metric("Safe Nodes", safe_nodes)

# Create Map
m = folium.Map(location=[20, 0], zoom_start=2)

for _, row in df.iterrows():
    color = 'red' if row['status'] == 'Attack' else 'green'
    tooltip = f"Status: {row['status']}"
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=5,
        color=color,
        fill=True,
        fill_color=color,
        tooltip=tooltip
    ).add_to(m)

# Display Map
st_folium(m, width=1200, height=600)

st.markdown("### Threat Details")
st.dataframe(df[df['status'] == 'Attack'], use_container_width=True)
