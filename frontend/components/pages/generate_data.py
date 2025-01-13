import pandas as pd
import requests
import streamlit as st

from ..footers import show_footer
from ..headers import show_header


def app():
    show_header(
        "Data Generator", "Easily generate synthetic datasets tailored for AI models."
    )

    BACKEND_URL = st.secrets["BACKEND_URL"]

    # Ensure the user is authenticated
    if "auth_token" not in st.session_state:
        st.warning("You need to log in to generate datasets.")
        show_footer()
        return

    headers = {"Authorization": f"Bearer {st.session_state['auth_token']}"}

    st.markdown("### Existing Files")

    try:
        # Grabbing a large page_size up to 100 as per backend limit
        response = requests.get(
            f"{BACKEND_URL}/data/?page=1&page_size=100", headers=headers
        )
        if response.status_code == 200:
            existing_datasets = (
                response.json()
            )  # list of dicts: {id, name, file_name, uploaded_at, ...}
            if existing_datasets:
                for ds in existing_datasets:
                    file_name = ds["file_name"]
                    dataset_name = ds["name"]
                    file_url = f"{BACKEND_URL}/uploads/{file_name}"

                    # Attempt to read CSV to get shape
                    try:
                        df = pd.read_csv(file_url)
                        rows, cols = df.shape
                        st.write(
                            f"**{dataset_name}**  \n"
                            f"File: `{file_name}`  \n"
                            f"Rows: **{rows}**, Columns: **{cols}**"
                        )
                    except Exception as e:
                        st.warning(f"Could not read '{file_name}': {e}")
            else:
                st.info("No datasets found.")
        else:
            st.error(
                f"Failed to fetch existing datasets: "
                f"{response.json().get('detail', 'Unknown error.')}"
            )
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching existing datasets: {e}")

    st.markdown("---")

    dataset_types = {
        "User_Profiles": [
            "user_id",
            "name",
            "email",
            "age",
            "gender",
            "country",
            "sign_up_date",
            "subscription_plan",
            "status",
            "last_login",
        ],
        "E-Commerce_Transactions": [
            "transaction_id",
            "user_id",
            "product_id",
            "category",
            "amount",
            "currency",
            "timestamp",
            "quantity",
            "payment_method",
            "delivery_status",
        ],
        "Healthcare_Patients": [
            "patient_id",
            "name",
            "age",
            "gender",
            "diagnosis",
            "treatment",
            "admission_date",
            "discharge_date",
            "doctor_id",
            "insurance_status",
        ],
        "Banking_Operations": [
            "account_number",
            "customer_name",
            "balance",
            "transaction_id",
            "transaction_type",
            "amount",
            "branch",
            "ifsc_code",
            "timestamp",
            "is_fraud",
        ],
        "Education_Performance": [
            "student_id",
            "name",
            "age",
            "gender",
            "grade",
            "class",
            "subject",
            "attendance_rate",
            "exam_score",
            "extra_curricular",
        ],
        "Product_Reviews": [
            "review_id",
            "product_id",
            "user_id",
            "rating",
            "review_text",
            "timestamp",
            "helpful_votes",
            "verified_purchase",
            "category",
            "brand",
        ],
        "IoT_Sensor_Data": [
            "sensor_id",
            "device_name",
            "timestamp",
            "temperature",
            "humidity",
            "pressure",
            "light_intensity",
            "motion_detected",
            "battery_level",
            "status",
        ],
        "Customer_Support_Tickets": [
            "ticket_id",
            "user_id",
            "issue_type",
            "priority",
            "status",
            "creation_date",
            "resolution_date",
            "assigned_agent",
            "channel",
            "satisfaction_rating",
        ],
        "Financial_Market_Data": [
            "ticker",
            "company_name",
            "price_open",
            "price_close",
            "high",
            "low",
            "volume",
            "market_cap",
            "pe_ratio",
            "dividend_yield",
        ],
        "Social_Media_Metrics": [
            "post_id",
            "user_id",
            "timestamp",
            "platform",
            "content_type",
            "likes",
            "shares",
            "comments",
            "engagement_rate",
            "hashtags",
        ],
    }

    # Let the user select a dataset type
    dataset_type = st.selectbox(
        "Select Dataset Type", options=list(dataset_types.keys())
    )

    # Let the user select columns based on the chosen dataset type
    available_columns = dataset_types.get(dataset_type, [])
    selected_columns = st.multiselect(
        "Select Columns to Include",
        options=available_columns,
        default=available_columns,
    )

    # Generate dataset form
    with st.form("data_generator_form"):
        col1, col2 = st.columns([1, 2])

        with col1:
            # Restrict the user to values between 100 and 100,000
            n_rows = st.number_input(
                "Number of Rows", min_value=100, max_value=100000, step=100, value=1000
            )

            # By default, combine the selected dataset_type + "_Dataset"
            default_dataset_name = f"{dataset_type}_Dataset"
            dataset_name = st.text_input("Dataset Name", value=default_dataset_name)

            filename = st.text_input(
                "File Name (Optional - if left blank, the dataset name will be used as the file name.)",
                value="",
                help="If left blank, the dataset name will be used as the file name.",
            )
            overwrite = st.checkbox(
                "Overwrite if file already exists?",
                value=False,
                help="If checked, existing files with the same name will be overwritten.",
            )

        with col2:
            st.write("")  # for spacing, or any extra fields as needed

        submit = st.form_submit_button("Generate Dataset")

    # When user clicks 'Generate Dataset'
    if submit:
        if not selected_columns:
            st.error("Please select at least one column.")
            st.stop()

        # Double-check in front-end as well
        if not (100 <= n_rows <= 100000):
            st.error("Number of rows must be between 100 and 100000.")
            st.stop()

        payload = {
            "n_rows": int(n_rows),
            "columns": selected_columns,
            "dataset_name": dataset_name.strip(),
            "filename": filename.strip() if filename else None,
            "overwrite": overwrite,
        }

        with st.spinner("Generating dataset..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/data-generator/generate",
                    json=payload,
                    headers=headers,
                )
                if response.status_code == 200:
                    dataset = response.json()
                    st.success(f"Dataset '{dataset['name']}' generated successfully!")
                    # Optionally, provide a download button if the backend returns the file content
                    # Here, assuming the backend does not return the file content, just metadata
                    # To download, the user can use the Existing Files section
                    st.rerun()

                elif response.status_code == 401:
                    st.error("Authentication failed. Please log in again.")
                    st.session_state.pop("auth_token", None)
                    st.rerun()

                elif response.status_code == 409:
                    st.error(response.json().get("detail", "File already exists."))

                else:
                    st.error(
                        f"Failed to generate dataset: "
                        f"{response.json().get('detail', 'Unknown error.')}"
                    )
            except requests.exceptions.ConnectionError:
                st.error("Unable to connect to the backend. Please try again later.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

    show_footer()
