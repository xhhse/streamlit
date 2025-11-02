import os
import pandas as pd
import requests
import streamlit as st
import plotly.express as px
from tinyhtml5.constants import special_elements

# File name and GitHub raw URL
filename = "trees.csv"
url = "https://raw.githubusercontent.com/tylerjrichards/Streamlit-for-Data-Science/main/trees_app/trees.csv"

# Check if the file already exists in the current directory
if not os.path.exists(filename):
    print(f"{filename} not found. Downloading...")
    response = requests.get(url)
    response.raise_for_status()  # Ensure the download was successful
    with open(filename, "wb") as f:
        f.write(response.content)
    st.write(f"{filename} downloaded successfully.")
else:
    st.write(f"{filename} already exists. Reading directly...")

# Read the CSV file
df = pd.read_csv(filename)
st.title("🌳 Tree Data Explorer")

st.write("Here’s a quick look at the data:")
st.dataframe(df.head())
species_list = sorted(df["species"].dropna().unique())[1:]
selected_species = st.multiselect(
    "Select one or more species:",
    options=species_list,
    default=species_list[:1]  # pre-select first species
)

# Filter data
if selected_species:
    filtered_df = df[df["species"].isin(selected_species)]
else:
    filtered_df = df.copy()  # show all if none selected

st.write(f"Showing {len(filtered_df)} trees for selected species.")
# --- Plotly Map ---
st.subheader("🗺️ Tree Locations on Map")
fig = px.scatter_mapbox(
    filtered_df,
    lat="latitude",
    lon = "longitude",
    hover_name="tree_id",
    color="species",
    zoom=11,
    height=600
)

fig.update_layout(
    mapbox_style="open-street-map",
    showlegend=False
)
# Make all markers larger
fig.update_traces(marker=dict(size=15))
st.plotly_chart(fig, use_container_width=True)