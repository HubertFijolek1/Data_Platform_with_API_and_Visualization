import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import time

def app():
    st.title("Data Visualization")

    # Example: local sample data to demonstrate searching
    sample_data = pd.DataFrame({
           "category": ["A", "B", "C", "D", "E", "F"],
           "value": [10, 23, 7, 18, 23, 5]
                          })

    search_text = st.text_input("Search Category:")
    if search_text:
        filtered_data = sample_data[sample_data["category"].str.contains(search_text, case=False)]
    else:
        filtered_data = sample_data
        st.write("Filtered Data:")
        st.dataframe(filtered_data)

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

    st.write("Plotly Bar Chart:")
    fig_bar = px.bar(data, x="category", y="value", title="Plotly Bar Chart")
    st.plotly_chart(fig_bar, use_container_width=True)

    # Example line chart
    st.write("Plotly Line Chart:")
    data_line = pd.DataFrame({
            "x": list(range(1, 6)),
            "metric": [3, 8, 4, 9, 11]
                           })
    fig_line = px.line(data_line, x="x", y="metric", title="Sample Line Chart")
    st.plotly_chart(fig_line, use_container_width=True)

    st.write("Table View:")
    st.dataframe(sample_data)
