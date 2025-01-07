import streamlit as st

def show_header(title: str, subtitle: str = ""):
    st.markdown(f"""
        <div style="text-align: center;">
            <h1>{title}</h1>
            <p style="font-size: 18px;">{subtitle}</p>
        </div>
        """, unsafe_allow_html=True)