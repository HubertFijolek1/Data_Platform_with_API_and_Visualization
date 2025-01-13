import time

import requests
import streamlit as st

from ..footers import show_footer
from ..headers import show_header


def app():
    show_header("Login", "Access your account")

    if "auth_token" in st.session_state:
        st.info("You are already logged in.")
        show_footer()
        return

    BACKEND_URL = st.secrets["BACKEND_URL"]

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if submit:
        if not email or not password:
            st.error("Please enter both email and password.")
            return

        data = {
            "email": email,
            "password": password,
        }

        with st.spinner("Logging in..."):
            try:
                response = requests.post(f"{BACKEND_URL}/auth/login", json=data)
                if response.status_code == 200:
                    token_data = response.json()
                    st.session_state["auth_token"] = token_data.get("access_token")
                    st.success("Logged in successfully!")
                    time.sleep(1.3)
                    st.session_state["login_successful"] = True  # Set the flag
                    st.rerun()  # Rerun the app to update the UI
                else:
                    st.error(
                        f"Login failed: {response.json().get('detail', 'Unknown error.')}"
                    )
            except requests.exceptions.ConnectionError:
                st.error("Unable to connect to the backend. Please try again later.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

    show_footer()
