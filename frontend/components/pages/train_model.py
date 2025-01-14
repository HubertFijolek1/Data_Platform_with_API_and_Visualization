import pandas as pd
import requests
import streamlit as st

from ..footers import show_footer
from ..headers import show_header


def app():
    show_header(
        "Train Model", "Train or retrain a model using scikit-learn or TensorFlow"
    )

    # Check authentication
    if "auth_token" not in st.session_state:
        st.warning("You need to log in before training a model.")
        show_footer()
        return

    BACKEND_URL = st.secrets["BACKEND_URL"]
    headers = {"Authorization": f"Bearer {st.session_state['auth_token']}"}

    # 1) Fetch user’s datasets
    try:
        resp = requests.get(
            f"{BACKEND_URL}/data/?page=1&page_size=100", headers=headers
        )
        if resp.status_code != 200:
            st.error(f"Failed to fetch datasets: {resp.text}")
            show_footer()
            return
        datasets = resp.json()
        if not datasets:
            st.info("No datasets available. Please upload or generate a dataset first.")
            show_footer()
            return
    except Exception as exc:
        st.error(f"Error fetching datasets: {exc}")
        show_footer()
        return

    # 2) Choose dataset
    ds_names = [d["name"] for d in datasets]
    if not ds_names:
        st.warning("No datasets found.")
        show_footer()
        return

    chosen_ds_name = st.selectbox("Select a Dataset to Train On", ds_names)
    chosen_ds = next((d for d in datasets if d["name"] == chosen_ds_name), None)
    if not chosen_ds:
        st.warning("Could not find the chosen dataset.")
        show_footer()
        return

    # Display a small preview
    file_url = f"{BACKEND_URL}/uploads/{chosen_ds['file_name']}"
    try:
        df = pd.read_csv(file_url)
        if df.empty:
            st.warning("This dataset is empty.")
            show_footer()
            return
        st.write(f"Preview of {chosen_ds_name}")
        st.dataframe(df.head())
        columns = df.columns.tolist()

        # Let user pick label column (only relevant for supervised)
        label_col = st.selectbox(
            "Label Column (for supervised training)", options=columns
        )
    except Exception as e:
        st.error(f"Failed to read dataset: {e}")
        show_footer()
        return

    # 3) Choose an algorithm
    algo_options = [
        "LogisticRegression",
        "RandomForestClassifier",
        "KMeans",
        "TensorFlow_Classifier",
    ]
    st.markdown("### Choose an Algorithm")
    algo = st.selectbox("Algorithm", algo_options)

    # 4) Hyperparameters
    st.markdown("### Hyperparameters")
    hyperparams = {}
    if algo == "LogisticRegression":
        c_val = st.number_input(
            "C (Regularization)", value=1.0, min_value=0.01, max_value=1e5
        )
        hyperparams["C"] = c_val
    elif algo == "RandomForestClassifier":
        n_estimators = st.number_input(
            "n_estimators", value=100, min_value=1, max_value=10000
        )
        hyperparams["n_estimators"] = int(n_estimators)
    elif algo == "KMeans":
        n_clusters = st.number_input("n_clusters", value=2, min_value=1, max_value=100)
        hyperparams["n_clusters"] = int(n_clusters)
    elif algo == "TensorFlow_Classifier":
        epochs = st.number_input("Epochs", value=5, min_value=1, max_value=100)
        hyperparams["epochs"] = int(epochs)

    # 5) Train
    if st.button("Train Model"):
        payload = {
            "dataset_id": chosen_ds["id"],
            "label_column": label_col,
            "algorithm": algo,
            "hyperparams": hyperparams,
        }
        with st.spinner("Training..."):
            try:
                train_resp = requests.post(
                    f"{BACKEND_URL}/ml/train2", json=payload, headers=headers
                )
                if train_resp.status_code == 200:
                    resp_data = train_resp.json()
                    st.success("Model trained successfully!")
                    st.json(resp_data)
                else:
                    st.error(f"Training failed: {train_resp.text}")
            except requests.exceptions.ConnectionError:
                st.error("Unable to connect to the backend. Please try again later.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

    show_footer()
