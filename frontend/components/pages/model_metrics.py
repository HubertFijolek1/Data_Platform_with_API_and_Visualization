import pandas as pd  # ADDED to help create a quick chart
import requests
import streamlit as st

from ..footers import show_footer
from ..headers import show_header


def app():
    show_header("Model Performance Metrics", "View metrics of my trained models.")

    # Check if user is authenticated
    if "auth_token" not in st.session_state:
        st.warning("You need to log in to view model metrics.")
        show_footer()
        return

    BACKEND_URL = st.secrets["BACKEND_URL"]
    headers = {"Authorization": f"Bearer {st.session_state['auth_token']}"}

    # --------------------------------------------------------------------
    # ADDED EXPLANATIONS: Provide basic instructions on how to use this page
    # --------------------------------------------------------------------
    st.markdown(
        """
    ### How to Use This Page

    **1. Select a trained model** from the dropdown (the same list used in predictions).
    - These models come from files in `saved_models/` (e.g., `.joblib` or `.h5`).

    **2. Enter a model version** if your training process supports versioning (default: "v1").

    **3. Click "Fetch Metrics"** to retrieve performance stats such as Accuracy, Precision, Recall, or MSE.
    - The exact metrics depend on whether it’s a classification or regression model.
    - If no metrics are found, either the model might not have been evaluated, or the backend doesn’t store them.

    **Example Usage**:
    - If you trained a Logistic Regression for classification, you may see `accuracy`, `precision`, and `recall`.
    - If you trained a regression model, you might see `mse` (Mean Squared Error).

    **4. (Optional) Visualize or interpret the displayed metrics**:
    - Higher accuracy/precision/recall is typically better for classification tasks.
    - Lower MSE is better for regression tasks.
    - You can use these metrics to compare models and pick the best one for predictions.
    """
    )

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
        with st.spinner("Fetching metrics..."):
            try:
                # The route is /ml/metrics/{model_name}/{version}
                response_metrics = requests.get(
                    f"{BACKEND_URL}/ml/metrics/{model_name}/{version}",
                    headers=headers,
                )
                if response_metrics.status_code == 200:
                    metrics = response_metrics.json()
                    st.success("Metrics fetched successfully!")
                    st.write("### Performance Metrics:")
                    st.json(metrics)

                    # OPTIONAL CHART: If the metrics are numeric, we can show a bar chart
                    numeric_entries = {
                        k: v
                        for k, v in metrics.items()
                        if isinstance(v, (int, float))  # ignore complex or lists
                    }
                    if numeric_entries:
                        chart_df = pd.DataFrame(
                            list(numeric_entries.values()),
                            index=numeric_entries.keys(),
                            columns=["Metric Value"],
                        )
                        st.bar_chart(chart_df)
                    else:
                        st.info("No numeric metrics to display as a chart.")
                else:
                    st.error(
                        f"Failed to fetch metrics: "
                        f"{response_metrics.json().get('detail', 'Unknown error.')}"
                    )
            except requests.exceptions.ConnectionError:
                st.error("Unable to connect to the backend. Please try again later.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

    show_footer()
