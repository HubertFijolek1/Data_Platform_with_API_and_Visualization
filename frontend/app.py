import streamlit as st
from pages import login, register, upload_data, data_visualization, user_profile
from components.navbar import show_navbar

def main():
    # Must be the first Streamlit command
    st.set_page_config(page_title="Data Analysis Dashboard", layout="wide")

    # Initialize PAGES in session state if not present
    if "PAGES" not in st.session_state:
        st.session_state["PAGES"] = {
            "Login": login,
            "Register": register,
            "Upload Data": upload_data,
            "Data Visualization": data_visualization,
            "User Profile": user_profile,
        }

    # Show the navbar
    show_navbar()

if __name__ == "__main__":
    main()