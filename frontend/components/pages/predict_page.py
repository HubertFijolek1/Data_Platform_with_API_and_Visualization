import pandas as pd
import requests
import streamlit as st

from ..footers import show_footer
from ..headers import show_header


def app():
    show_header(
        "Make Predictions", "Use a trained model (PyTorch, scikit-learn, TF, etc.)"
    )

    if "auth_token" not in st.session_state:
        st.warning("You need to log in to make predictions.")
        show_footer()
        return

    BACKEND_URL = st.secrets["BACKEND_URL"]
    headers = {"Authorization": f"Bearer {st.session_state['auth_token']}"}

    # --------------------------------------------------------------------
    # ADDED EXPLANATIONS: Provide basic instructions on how to use the page
    # --------------------------------------------------------------------
    st.markdown(
        """
    ### How to Use This Page

    **1. Select a trained model** (e.g., logistic regression, random forest, etc.) from the dropdown below.
    - If no models appear, you may need to go to **Train & Select Model** first or ensure a saved model is present.

    **2. Make a single prediction** by manually entering a couple of numeric features (like feature1, feature2).
    - Depending on how the model was trained, these inputs should match the model's expected features.

    **3. (Optional) Upload a CSV for batch predictions** if you have multiple rows of data.
    - The CSV should include columns named exactly as the model expects (e.g., feature1, feature2).
    - The platform will apply the model to every row in that CSV.

    **4. View the resulting predictions** and download them if you like (CSV).
    - For classification models, you may also see **probabilities** (model confidence).
    - For clustering or other unsupervised tasks, probabilities may be zero.

    **Important**: The features you input here must match the features used during training. For example, if you trained a model with columns `[feature1, feature2, ..., featureN]`, you need to supply the same set of features.
    """
    )

    st.subheader("Select Model")
    try:
        # Get list of trained models
        resp = requests.get(f"{BACKEND_URL}/ml/models", headers=headers)
        if resp.status_code != 200:
            st.error("Failed to fetch models list.")
            show_footer()
            return
        model_list = resp.json()  # e.g. ["LR_dataset1.joblib", "tf_dataset5.h5", ...]
        if not model_list:
            st.info("No trained models found yet. Train a model first.")
            show_footer()
            return
    except Exception as e:
        st.error(f"Error fetching model list: {e}")
        show_footer()
        return

    chosen_model = st.selectbox("Choose a Model Name", model_list)

    # Option 1: Single Data Point
    st.subheader("Single Data Point Prediction")
    with st.form("single_prediction_form"):
        # Hardcoded for demonstration
        feat1 = st.number_input("Feature 1", value=0.0)
        feat2 = st.number_input("Feature 2", value=0.0)
        submit_single = st.form_submit_button("Predict Single")

    if submit_single:
        payload = {
            "model_name": chosen_model,
            "data": [{"feature1": feat1, "feature2": feat2}],
        }
        with st.spinner("Predicting..."):
            try:
                # Hitting /predict2
                r = requests.post(
                    f"{BACKEND_URL}/predict2",
                    json=payload,
                    headers=headers,
                )
                if r.status_code == 200:
                    out = r.json()
                    st.success("Prediction successful!")
                    preds = out.get("predictions", [])
                    probs = out.get("probabilities", [])
                    st.write("**Predictions:**", preds)
                    st.write("**Probabilities:**", probs)
                else:
                    st.error(f"Prediction failed: {r.text}")
            except Exception as e:
                st.error(f"Error: {e}")

    # Option 2: Batch
    st.subheader("Batch Prediction via CSV")
    file_up = st.file_uploader("Upload CSV for batch predictions", type=["csv"])
    if file_up:
        try:
            batch_df = pd.read_csv(file_up)
            st.write("Preview of uploaded data:")
            st.dataframe(batch_df.head())

            if st.button("Make Batch Predictions"):
                payload = {
                    "model_name": chosen_model,
                    "data": batch_df.to_dict(orient="records"),
                }
                with st.spinner("Predicting in batch..."):
                    r = requests.post(
                        f"{BACKEND_URL}/predict2",
                        json=payload,
                        headers=headers,
                    )
                    if r.status_code == 200:
                        out = r.json()
                        preds = out.get("predictions", [])
                        probs = out.get("probabilities", [])
                        res_df = batch_df.copy()
                        res_df["Predicted"] = preds
                        res_df["Prob"] = probs
                        st.success("Batch prediction done!")
                        st.dataframe(res_df.head())

                        # Download option
                        csv_data = res_df.to_csv(index=False)
                        st.download_button(
                            "Download CSV predictions",
                            data=csv_data,
                            file_name="predictions.csv",
                            mime="text/csv",
                        )
                    else:
                        st.error(f"Prediction failed: {r.text}")
        except Exception as e:
            st.error(f"Error reading file: {e}")

    show_footer()
