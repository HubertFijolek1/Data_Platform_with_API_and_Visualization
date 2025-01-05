import streamlit as st
from pages import login, register, upload_data, data_visualization, user_profile

def main():
    # A simple global-level error catch in Streamlit might be limited,
    # but i want to demonstrate the concept:
    try:
        st.set_page_config(page_title="Data Analysis Dashboard", layout="wide")
        st.sidebar.title("Navigation")
        selection = st.sidebar.radio("Go to", list(PAGES.keys()))
        page_module = PAGES[selection]
        page_module.app()
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

PAGES = {
    "Login": login,
    "Register": register,
    "Upload Data": upload_data,
    "Data Visualization": data_visualization,
    "User Profile": user_profile,
}

if __name__ == "__main__":
    main()
