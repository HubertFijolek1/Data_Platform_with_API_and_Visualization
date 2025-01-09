import pandas as pd
import requests
import streamlit as st

from ..footers import show_footer
from ..headers import show_header


def app():
    show_header(
        "Make Predictions", "Use a trained model to make predictions on your data."
    )

    # Check if user is authenticated
    if "auth_token" not in st.session_state:
        st.warning("You need to log in to make predictions.")
        show_footer()
        return

    BACKEND_URL = st.secrets["BACKEND_URL"]
    headers = {"Authorization": f"Bearer {st.session_state['auth_token']}"}

    # Select Model
    st.subheader("Select Model")
    # Fetch available models (You might need to create an endpoint to list models)
    # For simplicity, assuming a model name is known
    model_name = st.text_input("Model Name", value="my_classification_model")

    # Option 1: Single Data Point
    st.subheader("Input Data for Single Prediction")
    with st.form("single_prediction_form"):
        feature1 = st.number_input("Feature 1", value=0.0)
        feature2 = st.number_input("Feature 2", value=0.0)
        submit_single = st.form_submit_button("Predict Single")

    if submit_single:
        # Prepare payload
        payload = {
            "model_name": model_name,
            "data": [{"feature1": feature1, "feature2": feature2}],
        }

        # Make API call to predict
        with st.spinner("Making prediction..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/predict/", json=payload, headers=headers
                )
                if response.status_code == 200:
                    prediction = response.json()
                    st.success("Prediction successful!")
                    st.write(f"**Predicted Label:** {prediction['predictions'][0]}")
                    st.write(
                        f"**Prediction Probability:**"
                        f" {prediction['probabilities'][0]:.2f}"
                    )
                else:
                    st.error(
                        f"Prediction failed:"
                        f" {response.json().get('detail', 'Unknown error.')}"
                    )
            except requests.exceptions.ConnectionError:
                st.error("Unable to connect to the backend. Please try again later.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

    # Option 2: Batch Predictions via File Upload
    st.subheader("Batch Predictions via File Upload")
    uploaded_file = st.file_uploader(
        "Upload CSV file for batch predictions", type=["csv"]
    )

    if uploaded_file is not None:
        try:
            data_df = pd.read_csv(uploaded_file)
            st.write("Preview of Uploaded Data:")
            st.dataframe(data_df.head())

            if st.button("Make Batch Predictions"):
                # Convert DataFrame to list of dicts
                data_payload = data_df.to_dict(orient="records")

                payload = {"model_name": model_name, "data": data_payload}

                with st.spinner("Making batch predictions..."):
                    response = requests.post(
                        f"{BACKEND_URL}/predict/", json=payload, headers=headers
                    )
                    if response.status_code == 200:
                        prediction = response.json()
                        predictions = prediction["predictions"]
                        probabilities = prediction["probabilities"]
                        results_df = data_df.copy()
                        results_df["Predicted Label"] = predictions
                        results_df["Prediction Probability"] = probabilities
                        st.success("Batch prediction successful!")
                        st.write("Prediction Results:")
                        st.dataframe(results_df)
                        # Optionally, allow users to download the results
                        csv = results_df.to_csv(index=False)
                        st.download_button(
                            label="Download Predictions as CSV",
                            data=csv,
                            file_name="predictions.csv",
                            mime="text/csv",
                        )
                    else:
                        st.error(
                            f"Batch prediction failed:"
                            f" {response.json().get('detail', 'Unknown error.')}"
                        )
        except Exception as e:
            st.error(f"Error processing the uploaded file: {e}")

    show_footer()
