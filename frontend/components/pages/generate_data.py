import streamlit as st
import requests
import os

from ..headers import show_header
from ..footers import show_footer


def app():
    show_header("Data Generator", "Create synthetic datasets for testing and demonstration.")

    BACKEND_URL = st.secrets["BACKEND_URL"]

    # Ensure the user is authenticated
    if "auth_token" not in st.session_state:
        st.warning("You need to log in to generate datasets.")
        return

    with st.form("data_generator_form"):
        col1, col2 = st.columns([1, 2])

        with col1:
            n_rows = st.number_input("Number of Rows", min_value=100, max_value=100000, step=100, value=1000)
            dataset_name = st.text_input("Dataset Name", value="Synthetic Dataset")

        with col2:
            st.write("")  # Empty to align the submit button

        submit = st.form_submit_button("Generate Dataset")

    if submit:
        if not dataset_name:
            st.error("Please provide a dataset name.")
            return

        headers = {
            "Authorization": f"Bearer {st.session_state['auth_token']}"
        }

        with st.spinner("Generating dataset..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/data-generator/generate",
                    json={"n_rows": int(n_rows)},
                    headers=headers
                )
                if response.status_code == 200:
                    dataset = response.json()
                    st.success(f"Dataset '{dataset['name']}' generated successfully!")
                    st.write(f"Download CSV: [Click Here]({BACKEND_URL}/uploads/{dataset['file_name']})")
                elif response.status_code == 401:
                    st.error("Authentication failed. Please log in again.")
                    st.session_state.pop("auth_token", None)
                    st.rerun()
                else:
                    st.error(f"Failed to generate dataset: {response.json().get('detail', 'Unknown error.')}")
            except requests.exceptions.ConnectionError:
                st.error("Unable to connect to the backend. Please try again later.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

    show_footer()