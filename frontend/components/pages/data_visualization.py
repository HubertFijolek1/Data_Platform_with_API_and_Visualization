import streamlit as st
import requests
import pandas as pd
import os

from ..headers import show_header
from ..footers import show_footer


def app():
    show_header("Data Visualization", "Explore and visualize your datasets")

    if "auth_token" not in st.session_state:
        st.warning("You need to log in to see datasets.")
        show_footer()
        return
    BACKEND_URL = st.secrets["BACKEND_URL"]

    # Fetch datasets from backend
    try:
        headers = {"Authorization": f"Bearer {st.session_state.get('auth_token', '')}"}
        response = requests.get(f"{BACKEND_URL}/data/", headers=headers)
        if response.status_code == 200:
            datasets = response.json()
            dataset_names = [dataset["name"] for dataset in datasets]
            selected_dataset = st.selectbox("Select Dataset", dataset_names)

            # Find selected dataset details
            selected = next(
                (d for d in datasets if d["name"] == selected_dataset), None
            )

            if selected:
                # Fetch the dataset file
                file_url = f"{BACKEND_URL}/uploads/{selected['file_name']}"
                data = pd.read_csv(file_url)

                st.write(f"### Preview of {selected_dataset}")
                st.dataframe(data.head())

                # Example Visualization
                st.write("### Data Visualization")
                if not data.empty:
                    chart_type = st.selectbox(
                        "Select Chart Type", ["Line", "Bar", "Scatter", "Histogram"]
                    )
                    columns = data.columns.tolist()
                    if len(columns) >= 2:
                        x_axis = st.selectbox("Select X-axis", columns)
                        y_axis = st.selectbox("Select Y-axis", columns)

                        col1, col2 = st.columns(2)

                        with col1:
                            st.markdown(f"**{chart_type} Chart**")
                            if chart_type == "Line":
                                st.line_chart(data.set_index(x_axis)[y_axis])
                            elif chart_type == "Bar":
                                st.bar_chart(data.set_index(x_axis)[y_axis])
                            elif chart_type == "Scatter":
                                st.scatter_chart(data[[x_axis, y_axis]])
                            # elif chart_type == "Histogram":
                            #     st.hist_chart(data[y_axis])

                        with col2:
                            st.markdown("**Data Summary**")
                            st.write(data.describe())
                    else:
                        st.warning("Not enough columns to create a chart.")
                else:
                    st.warning("Selected dataset is empty.")
        else:
            st.error(
                f"Failed to fetch datasets: {response.json().get('detail', 'Unknown error.')}"
            )
    except requests.exceptions.ConnectionError:
        st.error("Unable to connect to the backend. Please try again later.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

    show_footer()
