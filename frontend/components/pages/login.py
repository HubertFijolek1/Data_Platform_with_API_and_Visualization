import requests
import streamlit as st

from ..footers import show_footer
from ..forms import create_login_form
from ..headers import show_header


def app():
    show_header("Login", "Access your account")

    BACKEND_URL = st.secrets["BACKEND_URL"]

    email, password, submit = create_login_form()

    if submit:
        if not email or not password:
            st.error("Please enter both email and password.")
            return

        data = {"email": email, "password": password}

        with st.spinner("Logging in..."):
            try:
                response = requests.post(f"{BACKEND_URL}/auth/login", json=data)
                if response.status_code == 200:
                    token_data = response.json()
                    st.success("Logged in successfully!")
                    st.session_state["auth_token"] = token_data.get("access_token")
                    st.rerun()
                elif response.status_code == 401:
                    st.error("Invalid credentials. Please try again.")
                else:
                    error_detail = response.json().get("detail", "Unknown error.")
                    st.error(f"Login failed: {error_detail}")
            except requests.exceptions.ConnectionError:
                st.error("Unable to connect to the backend. Please try again later.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

    show_footer()
