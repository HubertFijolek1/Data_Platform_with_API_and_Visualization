import streamlit as st
import pandas as pd

st.title("Data Analysis Dashboard")

st.write("Upload a CSV file to analyze:")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("Data Preview:")
    st.dataframe(data.head())
