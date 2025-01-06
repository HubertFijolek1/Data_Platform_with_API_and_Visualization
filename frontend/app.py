import streamlit as st
from pages import login, register, upload_data, data_visualization, user_profile

def main():
    # Must be the first Streamlit command
    st.set_page_config(page_title="Data Analysis Dashboard", layout="wide")

    if "auth_token" not in st.session_state:
        # If not logged in, only show "Login" or "Register"
        available_pages = {"Login": login, "Register": register}
        st.sidebar.title("Navigation")
        selection = st.sidebar.radio("Go to", list(available_pages.keys()))
        page_module = available_pages[selection]
        page_module.app()
        return

    # If logged in, show all pages
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    page_module = PAGES[selection]
    page_module.app()

PAGES = {
    "Login": login,
    "Register": register,
    "Upload Data": upload_data,
    "Data Visualization": data_visualization,
    "User Profile": user_profile,
}

if __name__ == "__main__":
    main()