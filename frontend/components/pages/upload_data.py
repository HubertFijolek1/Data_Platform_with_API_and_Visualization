import requests
import streamlit as st

from ..footers import show_footer
from ..headers import show_header


def app():
    show_header("Upload Data", "Add your datasets to the platform")

    if "auth_token" not in st.session_state:
        st.warning("You need to log in before uploading data.")
        show_footer()
        return

    BACKEND_URL = st.secrets["BACKEND_URL"]

    with st.form("upload_form"):
        col1, col2 = st.columns([1, 2])

        with col1:
            name = st.text_input("Dataset Name (optional)")

        with col2:
            file = st.file_uploader("Upload CSV", type=["csv"])

        submit = st.form_submit_button("Upload")

    if submit:
        if not file:
            st.error("Please upload a CSV file.")
            return

        # If dataset name is empty, it will be handled by the backend to use the original file name
        data = {}
        files = {"file": (file.name, file.getvalue(), file.type)}
        if name:
            data["name"] = name

        headers = {"Authorization": f"Bearer {st.session_state.get('auth_token', '')}"}

        with st.spinner("Uploading dataset..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/data/upload",
                    data=data,
                    files=files,
                    headers=headers,
                )
                if response.status_code == 200:
                    dataset = response.json()
                    st.success(f"Dataset '{dataset['name']}' uploaded successfully!")
                    st.write(f"File Name: {dataset['file_name']}")
                else:
                    st.error(
                        f"Failed to upload dataset: {response.json().get('detail', 'Unknown error.')}"
                    )
            except requests.exceptions.ConnectionError:
                st.error("Unable to connect to the backend. Please try again later.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

    show_footer()
