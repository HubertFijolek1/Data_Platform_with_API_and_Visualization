import streamlit as st


def logout_callback():
    """
    Callback function to handle user logout.
    """
    st.session_state.pop("auth_token", None)
    st.session_state["selected_page"] = "Login"
    st.success("Logged out successfully!")
    st.rerun()  # Rerun the app to update the UI immediately


def show_navbar():
    st.sidebar.title("Navigation")

    # Determine available pages based on authentication
    if "auth_token" in st.session_state:
        # Pages for logged-in users
        available_pages = [
            "Upload Data",
            "Generate Data",
            "Data Visualization",
            "Group & Aggregate",
            "Model Wizard",
            "User Profile",
        ]
        default_page = "Upload Data"
    else:
        # Pages for anonymous users
        available_pages = ["Login", "Register"]
        default_page = "Login"

    # Handle login redirection
    if "login_successful" in st.session_state:
        st.session_state["selected_page"] = "Upload Data"
        st.session_state.pop("login_successful")  # Remove the flag after handling

    # Initialize 'selected_page' in session_state if not present
    if "selected_page" not in st.session_state:
        st.session_state["selected_page"] = default_page

    # Radio button selection
    selection = st.sidebar.radio(
        "Go to",
        options=available_pages,
        index=available_pages.index(st.session_state["selected_page"])
        if st.session_state["selected_page"] in available_pages
        else 0,
        key="selected_page",
    )

    # Render the selected page
    page = st.session_state["PAGES"].get(selection)
    if page:
        page.app()

    # Logout button logic
    if "auth_token" in st.session_state:
        st.sidebar.button("Logout", on_click=logout_callback)
