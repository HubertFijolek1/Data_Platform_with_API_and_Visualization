import streamlit as st
from components.navbar import show_navbar
from components.pages import (
    data_grouping,
    data_visualization,
    generate_data,
    login,
    model_wizard,
    register,
    upload_data,
    user_profile,
)


def main():
    st.set_page_config(page_title="Data Analysis Dashboard", layout="wide")

    if "PAGES" not in st.session_state:
        # Create our page dictionary
        st.session_state["PAGES"] = {
            "Login": login,
            "Register": register,
            "Upload Data": upload_data,
            "Generate Data": generate_data,
            "Data Visualization": data_visualization,
            "Group & Aggregate": data_grouping,
            "Model Wizard": model_wizard,
            "User Profile": user_profile,
        }

    show_navbar()


if __name__ == "__main__":
    main()
