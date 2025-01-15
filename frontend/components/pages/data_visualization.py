import pandas as pd
import plotly.express as px
import requests
import streamlit as st

from ..footers import show_footer
from ..headers import show_header
from ..recommendations import recommend_visualizations


def app():
    show_header("Data Visualization", "Explore and visualize your datasets")

    if "auth_token" not in st.session_state:
        st.warning("You need to log in to see datasets.")
        show_footer()
        return

    BACKEND_URL = st.secrets["BACKEND_URL"]
    headers = {"Authorization": f"Bearer {st.session_state.get('auth_token', '')}"}

    # Fetch the user's datasets (including both uploaded and generated)
    try:
        response = requests.get(
            f"{BACKEND_URL}/data/?page=1&page_size=100", headers=headers
        )
        if response.status_code == 200:
            datasets = response.json()
            if not datasets:
                st.info("No datasets available.")
                show_footer()
                return
        else:
            st.error(
                f"Failed to fetch datasets: {response.json().get('detail', 'Unknown error.')}"
            )
            show_footer()
            return
    except Exception as e:
        st.error(f"Error fetching datasets: {e}")
        show_footer()
        return

    # Let user choose a dataset by name
    dataset_names = [ds["name"] for ds in datasets]
    selected_dataset = st.selectbox("Select a Dataset", dataset_names)
    selected = next((ds for ds in datasets if ds["name"] == selected_dataset), None)
    if not selected:
        st.warning("Dataset not found.")
        show_footer()
        return

    # Load the CSV
    file_url = f"{BACKEND_URL}/uploads/{selected['file_name']}"
    try:
        data = pd.read_csv(file_url)
        if data.empty:
            st.warning("Selected dataset is empty.")
            show_footer()
            return

        st.write(f"### Preview of {selected_dataset}")
        # Show entire DataFrame in a scrollable table:
        st.dataframe(data, use_container_width=True)

        # ----------------------------------------------------------------------
        # Generate and show recommended visualizations
        # ----------------------------------------------------------------------
        recs = recommend_visualizations(data)

        if not recs:
            st.write("No specific chart recommendations found for this dataset.")
        else:
            st.write("### Recommended Visualizations")
            for i, rec in enumerate(recs):
                st.markdown(f"**{i+1}. {rec['chart_type']}** - {rec['description']}")

            # Optionally allow the user to pick one recommendation to display
            st.write("---")
            chosen_index = st.selectbox(
                "View one of the recommended charts:",
                range(len(recs)),
                format_func=lambda x: recs[x]["chart_type"],
            )
            chosen_rec = recs[chosen_index]

            if chosen_rec["chart_type"] == "Bar Chart":
                fig = px.bar(data, x=chosen_rec["x_col"], y=chosen_rec["y_col"])
                st.plotly_chart(fig)

            elif chosen_rec["chart_type"] == "Scatter Plot":
                fig = px.scatter(data, x=chosen_rec["x_col"], y=chosen_rec["y_col"])
                st.plotly_chart(fig)

            elif chosen_rec["chart_type"] == "Histogram":
                col = chosen_rec["col"]
                fig = px.histogram(data, x=col, nbins=30)
                st.plotly_chart(fig)

            elif chosen_rec["chart_type"] == "Correlation Heatmap":
                corr = data.corr(numeric_only=True)
                fig = px.imshow(corr, text_auto=True, aspect="auto")
                fig.update_layout(title="Correlation Heatmap")
                st.plotly_chart(fig)

    except Exception as e:
        st.error(f"Failed to load dataset file: {e}")

    show_footer()
