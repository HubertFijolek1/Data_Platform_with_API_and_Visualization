import streamlit as st
import pandas as pd
import requests
import io


def app():
    st.title("Data Upload")

    if "auth_token" not in st.session_state:
        st.warning("You must be logged in to upload data.")
        return

    st.write("Upload a CSV or TXT file to the platform:")

    uploaded_file = st.file_uploader("Choose a file", type=["csv", "txt"])
    dataset_name = st.text_input("Dataset Name", value="My Dataset")
    train_model_flag = st.checkbox("Train Model Immediately?")
    label_col = st.text_input("Label Column (if training)")

    if uploaded_file is not None:
        try:
            if uploaded_file.name.lower().endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_csv(uploaded_file, delimiter="\t")

            st.write("Data Preview:")
            st.dataframe(df.head())

            # Optionally, send to backend
            if st.button("Submit to Backend"):
                headers = {"Authorization": f"Bearer {st.session_state['auth_token']}"}

                # Prepare files payload
                files = {
                    "file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")
                }
                form_data = {
                    "name": dataset_name,
                    "train": str(train_model_flag).lower(),  # "true" or "false"
                    "label_column": label_col if label_col else ""
                }

                try:
                    resp = requests.post(
                        "http://localhost:8000/data/upload",
                        headers=headers,
                        files=files,
                        data=form_data
                    )
                    if resp.status_code == 200:
                        st.success("Dataset uploaded successfully!")
                        st.json(resp.json())
                    else:
                        st.error(f"Upload failed: {resp.json().get('detail', resp.text)}")
                except Exception as ex:
                    st.error(f"Error uploading file: {ex}")

        except Exception as e:
            st.error(f"Error reading file locally: {e}")
