import streamlit as st


def show_navbar():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio(
        "Go to", list(st.session_state.get("PAGES", {}).keys())
    )
    page = st.session_state["PAGES"][selection]
    page.app()

    if "auth_token" in st.session_state:
        if st.sidebar.button("Logout"):
            st.session_state.pop("auth_token")
            st.success("Logged out successfully!")
            st.rerun()
