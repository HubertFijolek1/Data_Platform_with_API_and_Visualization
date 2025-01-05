import streamlit as st
import pandas as pd
from pages import data_visualization

from pages import upload_data, login, register

PAGES = {
    "Login": login,
    "Register": register,
    "Upload Data": upload_data,
    "Data Visualization": data_visualization,

}

def main():
    st.set_page_config(page_title="Data Analysis Dashboard", layout="wide")
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    page_module = PAGES[selection]
    page_module.app()  # call the app() function of the selected module

if __name__ == "__main__":
    main()
