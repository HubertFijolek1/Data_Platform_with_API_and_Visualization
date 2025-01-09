import streamlit as st


def show_footer():
    st.markdown(
        """
        <hr>
        <div style="text-align: center; color: #888;">
            <p>© 2025 Data Analysis Platform. All rights reserved.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
