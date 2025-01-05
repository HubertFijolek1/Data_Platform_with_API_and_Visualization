import streamlit as st
import pandas as pd

def app():
    st.title("Data Upload")

    st.write("Upload a CSV or TXT file to the platform:")

    uploaded_file = st.file_uploader("Choose a file", type=["csv", "txt"])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.lower().endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_csv(uploaded_file, delimiter="\t")
            st.write("Data Preview:")
            st.dataframe(df.head())
        except Exception as e:
            st.error(f"Error reading file: {e}")
