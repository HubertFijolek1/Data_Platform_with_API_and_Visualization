import pandas as pd
import requests
import streamlit as st

from ..footers import show_footer
from ..headers import show_header


def app():
    """
    A combined wizard-like page that guides the user through:
    1) Selecting a dataset
    2) Choosing a problem type and algorithm
    3) Optionally setting hyperparameters
    4) Training the model
    5) Viewing metrics
    6) Making predictions
    This is intended to be more user-friendly for beginners.
    """
    show_header("Model Wizard", "Step-by-step model creation and prediction")

    if "auth_token" not in st.session_state:
        st.warning("You need to log in first to access the Model Wizard.")
        show_footer()
        return

    # We'll reuse the backend URL from st.secrets
    BACKEND_URL = st.secrets["BACKEND_URL"]
    ML_BACKEND_URL = st.secrets["ML_BACKEND_URL"]
    headers = {"Authorization": f"Bearer {st.session_state['auth_token']}"}

    # Keep track of current step in st.session_state, e.g. step 1..7
    if "wizard_step" not in st.session_state:
        st.session_state["wizard_step"] = 1

    # -------------------------------------------------------------------
    # STEP 1: Select a Dataset
    # -------------------------------------------------------------------
    if st.session_state["wizard_step"] == 1:
        st.subheader("Step 1: Choose a dataset")

        # Fetch datasets from the backend
        try:
            resp = requests.get(
                f"{BACKEND_URL}/data/?page=1&page_size=100", headers=headers
            )
            if resp.status_code == 200:
                datasets = resp.json()
                if not datasets:
                    st.info("No datasets found. Please upload or generate one.")
                    show_footer()
                    return
            else:
                st.error(f"Failed to fetch datasets: {resp.text}")
                show_footer()
                return
        except Exception as e:
            st.error(f"Error fetching datasets: {e}")
            show_footer()
            return

        ds_names = [d["name"] for d in datasets]
        chosen_ds_name = st.selectbox(
            "Pick a dataset to train on",
            options=ds_names,
        )

        # Next button
        if st.button("Next Step"):
            # Store chosen dataset in session_state
            st.session_state["chosen_dataset_name"] = chosen_ds_name
            # Move wizard step forward
            st.session_state["wizard_step"] = 2
            st.rerun()

    # -------------------------------------------------------------------
    # STEP 2: Problem Type
    # -------------------------------------------------------------------
    elif st.session_state["wizard_step"] == 2:
        st.subheader("Step 2: Choose the type of problem")

        # We'll let user pick "Classification", "Regression", or "Clustering"
        problem_type = st.radio(
            "Problem type:",
            ["Classification", "Regression", "Clustering"],
            index=0,
        )

        st.markdown(
            """
        **Hint for beginners**:
        - **Classification** is used when your target is a discrete category (e.g. Yes/No).
        - **Regression** is used when you want to predict a continuous numeric value (e.g. price).
        - **Clustering** is used when you have no explicit label column and want to group data automatically.
        """
        )

        if st.button("Next Step"):
            st.session_state["problem_type"] = problem_type
            st.session_state["wizard_step"] = 3
            st.rerun()

    # -------------------------------------------------------------------
    # STEP 3: Choose Algorithm
    # -------------------------------------------------------------------
    elif st.session_state["wizard_step"] == 3:
        st.subheader("Step 3: Pick an algorithm (or let the system auto-select)")

        problem_type = st.session_state.get("problem_type", "Classification")
        algo_options = []
        if problem_type == "Classification":
            algo_options = ["LogisticRegression", "RandomForestClassifier"]
        elif problem_type == "Regression":
            # For demonstration, let's say we do "LogisticRegression" for regression or add "LinearRegression"
            algo_options = ["LogisticRegression"]  # as a placeholder
        else:
            # Clustering
            algo_options = ["KMeans"]

        chosen_algo = st.selectbox("Select an algorithm", algo_options)
        st.session_state["chosen_algo"] = chosen_algo

        # Let user pick if they want advanced hyperparameters or not
        advanced = st.checkbox("Show advanced hyperparameters?", value=False)

        hyperparams = {}
        if advanced:
            st.write("You can adjust hyperparams here:")
            # Just examples:
            if chosen_algo == "LogisticRegression":
                c_val = st.number_input(
                    "C (regularization)", value=1.0, min_value=0.01, max_value=100000.0
                )
                hyperparams["C"] = c_val
            elif chosen_algo == "RandomForestClassifier":
                n_est = st.number_input(
                    "Number of trees (n_estimators)",
                    value=100,
                    min_value=1,
                    max_value=10000,
                )
                hyperparams["n_estimators"] = int(n_est)
            elif chosen_algo == "KMeans":
                n_clusters = st.number_input(
                    "Number of clusters (n_clusters)",
                    value=2,
                    min_value=1,
                    max_value=100,
                )
                hyperparams["n_clusters"] = int(n_clusters)
        else:
            # Use default hyperparams if advanced is not checked
            hyperparams = {}

        if st.button("Next Step"):
            st.session_state["hyperparams"] = hyperparams
            # If classification/regression, we go to step 4 (choose label)
            # If clustering, skip directly to step 5 (train)
            if problem_type in ["Classification", "Regression"]:
                st.session_state["wizard_step"] = 4
            else:
                st.session_state["wizard_step"] = 5
            st.rerun()

    # -------------------------------------------------------------------
    # STEP 4: Choose Label Column (only for supervised)
    # -------------------------------------------------------------------
    elif st.session_state["wizard_step"] == 4:
        st.subheader("Step 4: Choose your target (label) column")

        # Retrieve dataset info from session
        chosen_ds_name = st.session_state["chosen_dataset_name"]
        problem_type = st.session_state["problem_type"]
        # We need to fetch dataset detail or sample
        try:
            # Might need the actual dataset ID from name:
            ds_resp = requests.get(
                f"{BACKEND_URL}/data/?page=1&page_size=100", headers=headers
            )
            ds_resp.raise_for_status()
            all_datasets = ds_resp.json()
            chosen_ds = next(
                (d for d in all_datasets if d["name"] == chosen_ds_name), None
            )

            if not chosen_ds:
                st.error("Could not find the chosen dataset details.")
                show_footer()
                return

            file_url = f"{BACKEND_URL}/uploads/{chosen_ds['file_name']}"
            df_sample = pd.read_csv(file_url, nrows=50)  # just load partial for display
            columns = df_sample.columns.tolist()
        except Exception as e:
            st.error(f"Error reading dataset: {e}")
            show_footer()
            return

        st.write(f"Dataset: **{chosen_ds_name}** | Columns preview:")
        st.dataframe(df_sample.head())

        label_col = st.selectbox(
            "Which column is your target (label)?", options=columns
        )
        if st.button("Next Step (Train)"):
            st.session_state["label_column"] = label_col
            st.session_state["wizard_step"] = 5
            st.rerun()

    # -------------------------------------------------------------------
    # STEP 5: Train the model
    # -------------------------------------------------------------------
    elif st.session_state["wizard_step"] == 5:
        st.subheader("Step 5: Train the model")

        chosen_ds_name = st.session_state["chosen_dataset_name"]
        problem_type = st.session_state["problem_type"]
        chosen_algo = st.session_state["chosen_algo"]
        hyperparams = st.session_state["hyperparams"]

        # We fetch the dataset ID from name again:
        ds_resp = requests.get(
            f"{BACKEND_URL}/data/?page=1&page_size=100", headers=headers
        )
        ds_resp.raise_for_status()
        all_datasets = ds_resp.json()
        chosen_ds = next((d for d in all_datasets if d["name"] == chosen_ds_name), None)
        if not chosen_ds:
            st.error("Could not find chosen dataset ID.")
            show_footer()
            return

        # If supervised, get label column from state
        label_col = st.session_state.get("label_column", "")

        # We'll call /ml/train2
        if st.button("Start Training"):
            payload = {
                "dataset_path": f"uploads/{chosen_ds['file_name']}",
                "label_column": label_col,
                "algorithm": chosen_algo,
                "hyperparams": hyperparams,
            }
            try:
                train_resp = requests.post(
                    f"{ML_BACKEND_URL}/ml/train2",
                    json=payload,
                    headers=headers,
                )
                if train_resp.status_code == 200:
                    st.success("Model trained successfully!")
                    # Optionally store the name of model_file returned
                    resp_data = train_resp.json()
                    st.session_state["trained_model_file"] = resp_data.get(
                        "model_file", None
                    )
                    # Move to step 6
                    st.session_state["wizard_step"] = 6
                    st.rerun()
                else:
                    st.error(f"Training failed: {train_resp.text}")
            except Exception as e:
                st.error(f"Error calling train endpoint: {e}")

    # -------------------------------------------------------------------
    # STEP 6: View metrics
    # -------------------------------------------------------------------
    elif st.session_state["wizard_step"] == 6:
        st.subheader("Step 6: View performance metrics")

        # We can attempt to retrieve metrics from the backend-ml or from /ml/metrics
        # E.g. if your ML container exposes GET /ml/metrics/<model_name>/<version>
        # or we simply show a minimal output if we haven't integrated robust metrics
        st.markdown(
            "Below are the computed metrics for the newly trained model (if available)."
        )

        # We'll try to see if there's a standard name from st.session_state["trained_model_file"]
        model_file = st.session_state.get("trained_model_file", "")
        if model_file:
            st.write(f"Trained model file: **{model_file}**")

            # We can attempt an endpoint like GET /ml/metrics/model_file/v1
            # or if you store metrics in memory:
            metrics_url = f"{ML_BACKEND_URL}/ml/metrics/{model_file}/v1"
            try:
                metrics_resp = requests.get(metrics_url, headers=headers)
                if metrics_resp.status_code == 200:
                    metrics_json = metrics_resp.json()
                    st.json(metrics_json)
                    # We can also visualize as a bar chart if numeric
                    numeric_entries = {
                        k: v
                        for k, v in metrics_json.items()
                        if isinstance(v, (int, float))
                    }
                    if numeric_entries:
                        st.bar_chart(
                            pd.DataFrame(
                                numeric_entries.values(),
                                index=numeric_entries.keys(),
                                columns=["Value"],
                            )
                        )
                else:
                    st.info(
                        "No specific metrics found or metrics endpoint not implemented."
                    )
            except Exception as e:
                st.info(f"Unable to fetch metrics automatically: {e}")
        else:
            st.info(
                "No model file name found. Possibly training did not return a standard name."
            )

        st.markdown(
            """
        **Basic Metrics Explanation**:
        - **Accuracy**: how many predictions are correct out of all.
        - **Precision**: among predicted positives, how many are truly positive.
        - **Recall**: among actual positives, how many did we capture as positive.
        - **MSE**: Mean Squared Error, relevant for regression.
        """
        )

        # Next Step button
        if st.button("Next Step (Make Predictions)"):
            st.session_state["wizard_step"] = 7
            st.rerun()

    # -------------------------------------------------------------------
    # STEP 7: Make predictions
    # -------------------------------------------------------------------
    elif st.session_state["wizard_step"] == 7:
        st.subheader("Step 7: Make predictions using the trained model")

        st.markdown(
            """
        ### Option A: Single Data Point
        Please enter values for each feature.
        """
        )

        # If we want to show dynamic input fields, we need the columns except the label
        # This is just a simplified approach (hardcoded feature1, feature2).
        # In a real scenario, you'd parse the dataset or store the feature list somewhere.

        feat1 = st.number_input("Feature1", value=0.0)
        feat2 = st.number_input("Feature2", value=0.0)

        if st.button("Predict Single"):
            model_file = st.session_state.get("trained_model_file", None)
            if not model_file:
                st.error(
                    "No model_file found in session. Make sure training is complete."
                )
            else:
                payload = {
                    "model_name": model_file.replace(
                        ".joblib", ""
                    ),  # or exactly model_file if needed
                    "data": [{"feature1": feat1, "feature2": feat2}],
                }
                try:
                    r = requests.post(
                        f"{ML_BACKEND_URL}/predict2",  # or /ml/predict2
                        json=payload,
                        headers=headers,
                    )
                    if r.status_code == 200:
                        out = r.json()
                        preds = out.get("predictions", [])
                        probs = out.get("probabilities", [])
                        st.success(f"Prediction: {preds}, Probability: {probs}")
                    else:
                        st.error(f"Prediction failed: {r.text}")
                except Exception as e:
                    st.error(f"Error: {e}")

        st.markdown("---")
        st.markdown(
            """
        ### Option B: Batch Prediction with CSV
        You can upload a CSV file with the same columns that the model expects.
        """
        )

        file_up = st.file_uploader("Upload CSV", type=["csv"])
        if file_up:
            df_batch = pd.read_csv(file_up)
            st.write("Preview of your uploaded CSV:")
            st.dataframe(df_batch.head())

            if st.button("Make Batch Predictions"):
                model_file = st.session_state.get("trained_model_file", None)
                if not model_file:
                    st.error("No model_file found in session.")
                else:
                    payload = {
                        "model_name": model_file.replace(".joblib", ""),
                        "data": df_batch.to_dict(orient="records"),
                    }
                    try:
                        r = requests.post(
                            f"{BACKEND_URL}/predict2",
                            json=payload,
                            headers=headers,
                        )
                        if r.status_code == 200:
                            out = r.json()
                            preds = out.get("predictions", [])
                            probs = out.get("probabilities", [])
                            df_out = df_batch.copy()
                            df_out["Predicted"] = preds
                            df_out["Probability"] = probs
                            st.success("Batch prediction complete!")
                            st.dataframe(df_out.head())

                            csv_data = df_out.to_csv(index=False)
                            st.download_button(
                                "Download Predictions CSV",
                                data=csv_data,
                                file_name="predictions.csv",
                                mime="text/csv",
                            )
                        else:
                            st.error(f"Batch prediction failed: {r.text}")
                    except Exception as e:
                        st.error(f"Error: {e}")

        st.markdown(
            "**End of Wizard**: You have successfully trained a model, checked metrics, and made predictions!"
        )
        show_footer()
