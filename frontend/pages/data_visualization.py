import streamlit as st
import pandas as pd
import altair as alt
import requests

def app():
    st.title("Data Visualization")

    # Attempt to retrieve data from the backend's /data/ endpoint
    # (Requires the user to be logged in)
    try:
        response = requests.get("http://localhost:8000/data/?page=1&page_size=20")
        if response.status_code == 200:
            datasets = response.json()  # This is a list of dataset metadata
            # For now, let's show the raw JSON:
            st.write("Fetched Datasets (metadata):")
            st.json(datasets)
        else:
            st.warning("No datasets found or unable to fetch.")
    except Exception as e:
        st.error(f"Error retrieving data from API: {e}")

    st.write("Sample Bar Chart (Altair):")

    sample_data = pd.DataFrame({
        "category": ["A", "B", "C", "D"],
        "value": [10, 23, 7, 18]})
    chart = alt.Chart(sample_data).mark_bar().encode(
          x = 'category',
          y = 'value'
                     )
    st.altair_chart(chart, use_container_width=True)

    st.write("Table View:")
    st.dataframe(sample_data)
