import streamlit as st
from pages import login, register, upload_data, data_visualization, user_profile, generate_data
from components.navbar import show_navbar
from components.footers import show_footer

def main():
    # Must be the first Streamlit command
    st.set_page_config(page_title="Data Analysis Dashboard", layout="wide")

    # Initialize PAGES in session state if not present
    if "PAGES" not in st.session_state:
        st.session_state["PAGES"] = {
            "Login": login,
            "Register": register,
            "Upload Data": upload_data,
            "Generate Data": generate_data,  # New Page
            "Data Visualization": data_visualization,
            "User Profile": user_profile,
        }

    # Show the navbar
    show_navbar()

    # Optionally show a footer on all pages
    show_footer()

if __name__ == "__main__":
    main()