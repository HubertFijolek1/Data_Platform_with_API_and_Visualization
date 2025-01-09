import streamlit as st
from components.pages import (
    login,
    register,
    upload_data,
    data_visualization,
    user_profile,
    generate_data,
    predict_page,
    model_metrics,
)
from components.navbar import show_navbar


def main():
    st.set_page_config(page_title="Data Analysis Dashboard", layout="wide")

    if "PAGES" not in st.session_state:
        st.session_state["PAGES"] = {
            "Login": login,
            "Register": register,
            "Upload Data": upload_data,
            "Generate Data": generate_data,
            "Data Visualization": data_visualization,
            "User Profile": user_profile,
            "Make Predictions": predict_page,
            "Model Metrics": model_metrics,
        }

    # Show the navbar
    show_navbar()


if __name__ == "__main__":
    main()
