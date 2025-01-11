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
        return

    # Define dataset types with relevant columns
    dataset_types = {
        "User Profiles": [
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
        "E-Commerce Transactions": [
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
        "Healthcare Patients": [
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
        "Banking Operations": [
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
        "Education Performance": [
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
        "Product Reviews": [
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
        "IoT Sensor Data": [
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
        "Customer Support Tickets": [
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
        "Financial Market Data": [
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
        "Social Media Metrics": [
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
            n_rows = st.number_input(
                "Number of Rows", min_value=100, max_value=10000, step=100, value=1000
            )
            dataset_name = st.text_input(
                "Dataset Name", value=f"{dataset_type} Dataset"
            )

        with col2:
            st.write("")  # Empty for alignment

        submit = st.form_submit_button("Generate Dataset")

    # Handle form submission
    if submit:
        if not dataset_name:
            st.error("Please provide a dataset name.")
            return

        if not selected_columns:
            st.error("Please select at least one column.")
            return

        headers = {"Authorization": f"Bearer {st.session_state['auth_token']}"}
        payload = {"n_rows": int(n_rows), "columns": selected_columns}

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
                    st.write(
                        f"Download CSV: [Click Here]({BACKEND_URL}/uploads/{dataset['file_name']})"
                    )
                elif response.status_code == 401:
                    st.error("Authentication failed. Please log in again.")
                    st.session_state.pop("auth_token", None)
                    st.rerun()
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
