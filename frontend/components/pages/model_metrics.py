import streamlit as st
import requests
from ..headers import show_header
from ..footers import show_footer


def app():
    show_header("Model Performance Metrics", "View metrics of my trained models.")

    # Check if user is authenticated
    if "auth_token" not in st.session_state:
        st.warning("You need to log in to view model metrics.")
        show_footer()
        return

    BACKEND_URL = st.secrets["BACKEND_URL"]
    headers = {"Authorization": f"Bearer {st.session_state['auth_token']}"}

    # Select Model
    st.subheader("Select Model and Version")
    try:
        response_models = requests.get(f"{BACKEND_URL}/ml/models", headers=headers)
        if response_models.status_code == 200:
            models_list = response_models.json()
            if models_list:
                model_name = st.selectbox("Choose a Model", options=models_list)
                version = st.text_input("Model Version", value="v1")
            else:
                st.warning("No models available. Please train a model first.")
                st.stop()
        else:
            st.error("Failed to fetch models list.")
            st.stop()
    except requests.exceptions.ConnectionError:
        st.error("Unable to connect to the backend. Please try again later.")
        st.stop()
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        st.stop()

    if st.button("Fetch Metrics"):
        payload = {"model_name": model_name, "version": version}
        with st.spinner("Fetching metrics..."):
            try:
                response_metrics = requests.get(
                    f"{BACKEND_URL}/ml/metrics/{model_name}/{version}", headers=headers
                )
                if response_metrics.status_code == 200:
                    metrics = response_metrics.json()
                    st.success("Metrics fetched successfully!")
                    st.write("### Performance Metrics:")
                    st.json(metrics)
                    # Optionally, visualize metrics
                    if "accuracy" in metrics:
                        st.write(f"**Accuracy:** {metrics['accuracy']:.2f}")
                    if "precision" in metrics:
                        st.write(f"**Precision:** {metrics['precision']:.2f}")
                    if "recall" in metrics:
                        st.write(f"**Recall:** {metrics['recall']:.2f}")
                    if "mse" in metrics:
                        st.write(f"**Mean Squared Error (MSE):** {metrics['mse']:.2f}")
                else:
                    st.error(
                        f"Failed to fetch metrics: {response_metrics.json().get('detail', 'Unknown error.')}"
                    )
            except requests.exceptions.ConnectionError:
                st.error("Unable to connect to the backend. Please try again later.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

    show_footer()
