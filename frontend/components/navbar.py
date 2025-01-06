import streamlit as st

def show_navbar():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(st.session_state.get("PAGES", {}).keys()))
    page = st.session_state["PAGES"][selection]
    page.app()