import streamlit as st
import pandas as pd
import altair as alt

def app():
    st.title("Data Visualization")

    # For now, let's assume we have some data or an API call:
    # data = ...
    # Here, I'll just make a sample DataFrame:
    data = pd.DataFrame({
        "category": ["A", "B", "C", "D"],
        "value": [10, 23, 7, 18]
    })

    st.write("Sample Bar Chart (Altair):")
    chart = alt.Chart(data).mark_bar().encode(
        x="category",
        y="value"
    )
    st.altair_chart(chart, use_container_width=True)

    st.write("Table View:")
    st.dataframe(data)
