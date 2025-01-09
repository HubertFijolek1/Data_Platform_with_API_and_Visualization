import streamlit as st


def show_header(title: str, subtitle: str = ""):
    st.markdown(
        f"""
        <div style="text-align: center; padding: 10px;">
            <h1 style="color: #4CAF50;">{title}</h1>
            <p style="font-size: 18px; color: #555;">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
