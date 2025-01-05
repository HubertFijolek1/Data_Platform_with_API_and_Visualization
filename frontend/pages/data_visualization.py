import streamlit as st
import pandas as pd
import plotly.express as px
import requests

def app():
    st.title("Data Visualization")

    # Example local sample data to demonstrate searching
    data = pd.DataFrame({
        "category": ["A", "B", "C", "D", "E", "F"],
        "value": [10, 23, 7, 18, 23, 5]
    })

    search_text = st.text_input("Search Category:")
    if search_text:
        filtered_data = data[data["category"].str.contains(search_text, case=False)]
    else:
        filtered_data = data

    st.write("Filtered Data:")
    st.dataframe(filtered_data)

    # Attempt to retrieve data from the backend's /data/ endpoint (Requires auth token)
    headers = {}
    if "auth_token" in st.session_state:
        headers = {"Authorization": f"Bearer {st.session_state['auth_token']}"}

    try:
        response = requests.get("http://localhost:8000/data/?page=1&page_size=20", headers=headers)
        if response.status_code == 200:
            datasets = response.json()
            st.write("Fetched Datasets (metadata):")
            st.json(datasets)
        else:
            st.warning(f"No datasets found or unable to fetch. Status: {response.status_code}")
    except Exception as e:
        st.error(f"Error retrieving data from API: {e}")

    st.write("Plotly Bar Chart:")
    fig_bar = px.bar(data, x="category", y="value", title="Plotly Bar Chart")
    st.plotly_chart(fig_bar, use_container_width=True)

    st.write("Plotly Line Chart:")
    data_line = pd.DataFrame({
        "x": list(range(1, 6)),
        "metric": [3, 8, 4, 9, 11]
    })
    fig_line = px.line(data_line, x="x", y="metric", title="Sample Line Chart")
    st.plotly_chart(fig_line, use_container_width=True)

    # Implement data export as CSV
    csv_data = data.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Export Data as CSV",
        data=csv_data,
        file_name="sample_data.csv",
        mime="text/csv"
    )

    st.write("Table View:")
    st.dataframe(data)
