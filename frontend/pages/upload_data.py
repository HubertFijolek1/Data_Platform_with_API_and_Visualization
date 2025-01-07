import streamlit as st
import requests
import os


def app():
    st.title("Upload Data")

    BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

    with st.form("upload_form"):
        name = st.text_input("Dataset Name")
        file = st.file_uploader("Upload CSV or TXT", type=["csv", "txt"])
        train = st.checkbox("Train Model After Upload")
        label_column = st.text_input("Label Column (if training)")
        submit = st.form_submit_button("Upload")

    if submit:
        if not name or not file:
            st.error("Please provide a dataset name and upload a file.")
            return

        files = {
            "file": (file.name, file.getvalue(), file.type)
        }
        data = {
            "name": name,
            "train": train,
            "label_column": label_column if train else None
        }

        headers = {"Authorization": f"Bearer {st.session_state.get('auth_token', '')}"}

        try:
            response = requests.post(f"{BACKEND_URL}/data/upload", data=data, files=files, headers=headers)
            if response.status_code == 200:
                dataset = response.json()
                st.success(f"Dataset '{dataset['name']}' uploaded successfully!")
                st.write(f"File Name: {dataset['file_name']}")
            else:
                st.error(f"Failed to upload dataset: {response.json().get('detail', 'Unknown error.')}")
        except requests.exceptions.ConnectionError:
            st.error("Unable to connect to the backend. Please try again later.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")