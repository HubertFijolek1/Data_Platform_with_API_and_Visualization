import streamlit as st


def show_navbar():
    st.sidebar.title("Navigation")

    # Check if 'selected_page' is pre-set (e.g., from registration)
    default_selection = st.session_state.get("selected_page", "Login")
    selection = st.sidebar.radio(
        "Go to",
        list(st.session_state.get("PAGES", {}).keys()),
        index=list(st.session_state["PAGES"].keys()).index(default_selection),
    )

    # Update "selected_page" for seamless interaction
    st.session_state["selected_page"] = selection

    # Load the selected page
    page = st.session_state["PAGES"][selection]
    page.app()

    # Logout button logic
    if "auth_token" in st.session_state:
        if st.sidebar.button("Logout"):
            st.session_state.pop("auth_token")
            st.success("Logged out successfully!")
            st.rerun()
