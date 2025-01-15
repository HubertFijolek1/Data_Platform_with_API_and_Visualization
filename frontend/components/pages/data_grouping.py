import pandas as pd
import requests
import streamlit as st

from ..footers import show_footer
from ..headers import show_header
from ..recommendations import recommend_visualizations


def app():
    show_header("Data Grouping & Aggregation", "Group your dataset by selected columns")

    if "auth_token" not in st.session_state:
        st.warning("You need to log in to group data.")
        show_footer()
        return

    BACKEND_URL = st.secrets["BACKEND_URL"]
    headers = {"Authorization": f"Bearer {st.session_state.get('auth_token', '')}"}

    # 1) List datasets
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

    ds_names = [d["name"] for d in datasets]
    chosen_ds_name = st.selectbox("Select a Dataset to View/Group", ds_names)
    chosen_ds = next((d for d in datasets if d["name"] == chosen_ds_name), None)

    if not chosen_ds:
        st.warning("Could not find the chosen dataset.")
        show_footer()
        return

    file_url = f"{BACKEND_URL}/uploads/{chosen_ds['file_name']}"

    try:
        df = pd.read_csv(file_url)
        if df.empty:
            st.warning("This dataset is empty.")
            show_footer()
            return

        st.write(f"### Preview of {chosen_ds_name}")
        st.dataframe(df.head())

        # 2) Choose grouping columns
        st.subheader("Select Grouping Columns")
        all_columns = df.columns.tolist()
        group_cols = st.multiselect("Group By", options=all_columns)

        # 3) Choose Aggregation
        st.subheader("Select Aggregation(s)")
        numeric_cols = df.select_dtypes(include=["float", "int"]).columns.tolist()
        if not numeric_cols:
            st.info("No numeric columns found for aggregation.")
            show_footer()
            return

        aggr_funcs = ["sum", "mean", "count", "max", "min"]
        chosen_aggr_funcs = st.multiselect(
            "Aggregation Functions", aggr_funcs, default=["sum"]
        )

        # 4) Perform grouping
        if group_cols and chosen_aggr_funcs:
            # Build the agg dict. Example: { 'col1': ['sum','mean'], 'col2': ['sum'] }
            agg_dict = {col: chosen_aggr_funcs for col in numeric_cols}

            grouped_df = df.groupby(group_cols).agg(agg_dict)
            # Flatten multi-level column index if needed
            grouped_df.columns = ["_".join(col) for col in grouped_df.columns]
            st.write("### Grouped & Aggregated Data")
            st.dataframe(grouped_df.reset_index().head())

            st.download_button(
                label="Download CSV of Aggregated Data",
                data=grouped_df.reset_index().to_csv(index=False),
                file_name="aggregated_data.csv",
                mime="text/csv",
            )

    except Exception as e:
        st.error(f"Failed to load dataset file: {e}")

    show_footer()
