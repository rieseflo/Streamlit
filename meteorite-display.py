# starten mit terminal command: streamlit run meteorite-display.py

import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from requests.exceptions import RequestException
import time
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="NASA Meteorite Landings Data")

# Function to fetch data from the API with retries
@st.cache_data
def fetch_data(url, retries=3, backoff_factor=0.3):
    for i in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            st.error(f"Attempt {i+1} of {retries} failed with error: {e}")
            time.sleep(backoff_factor * (2 ** i))  # Exponential backoff
    st.error("Failed to fetch data after several attempts.")
    return []

# Fetch the data
url = "https://data.nasa.gov/resource/gh4g-9sfh.json"
data = fetch_data(url)

# Convert the data into a pandas DataFrame
df = pd.DataFrame(data)

# Ensure the dataframe contains the necessary columns and process the data
if not df.empty:
    df = df[['name', 'id', 'nametype', 'recclass', 'mass', 'fall', 'year', 'reclat', 'reclong']]
    df['mass'] = pd.to_numeric(df['mass'], errors='coerce')
    df['year'] = pd.to_datetime(df['year'], errors='coerce')
    df['reclat'] = pd.to_numeric(df['reclat'], errors='coerce')
    df['reclong'] = pd.to_numeric(df['reclong'], errors='coerce')
    df = df.dropna(subset=['reclat', 'reclong'])
    df = df.rename(columns={'reclat': 'lat', 'reclong': 'lon'})

# Sidebar filters
st.sidebar.header("Filter data")
if not df.empty:
    min_year = int(df['year'].min().year)
    max_year = int(df['year'].max().year)
    selected_years = st.sidebar.slider("Select Year Range", min_year, max_year, (min_year, max_year))

    classes = ['All'] + df['recclass'].unique().tolist()
    selected_class = st.sidebar.selectbox("Select Meteorite Class", classes)

# Apply filters
if selected_class != 'All':
    filtered_df = df[
        (df['year'].dt.year >= selected_years[0]) &
        (df['year'].dt.year <= selected_years[1]) &
        (df['recclass'] == selected_class)
    ]
else:
    filtered_df = df[
        (df['year'].dt.year >= selected_years[0]) &
        (df['year'].dt.year <= selected_years[1])
    ]

# Main page content
st.header("NASA Meteorite Landings Data")

# Display a map with the meteorite landing locations
st.write("Map of Meteorite Landings:")
st.map(filtered_df[['lat', 'lon']])

# Display the data table
st.write("Here's a table of all displayed meteorite landings fetched from the NASA API:")
st.write(filtered_df) 

# Create a bar chart for the number of landings over time
if not filtered_df.empty:
    st.write("Bar Chart of Number of Meteorite Landings Over Time:")
    landings_per_year = filtered_df['year'].dt.year.value_counts().sort_index()
    st.bar_chart(landings_per_year)

# https://share.streamlit.io/ Deployment direkt über GitHub Repo

# create docker image (local)
# docker build -t meteorite-landings-app .

# upload to dockerhub


# deploy over azure