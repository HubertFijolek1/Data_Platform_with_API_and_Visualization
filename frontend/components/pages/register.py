import time

import requests
import streamlit as st

from ..footers import show_footer
from ..headers import show_header


def app():
    show_header("Register", "Create a new account")

    if "auth_token" in st.session_state:
        st.info("You are already logged in.")
        show_footer()
        return

    BACKEND_URL = st.secrets["BACKEND_URL"]

    with st.form("register_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input(
            "Confirm Password", type="password"
        )  # Confirm Password Field
        submit = st.form_submit_button("Register")

    if submit:
        # Check if all fields are filled
        if not username or not email or not password or not confirm_password:
            st.error("Please fill in all fields.")
            return

        # Check if passwords match
        if password != confirm_password:
            st.error("Passwords do not match. Please try again.")
            return

        # Optional: Validate email format, password strength, etc.

        data = {
            "username": username,
            "email": email,
            "password": password,
        }

        with st.spinner("Registering..."):
            try:
                response = requests.post(f"{BACKEND_URL}/auth/register", json=data)
                if response.status_code == 200:
                    st.success("Registration successful! 🎉")
                    st.success(
                        "You can now navigate to the Login page to access your account."
                    )
                else:
                    # Display detailed error message if available
                    error_detail = response.json().get("detail", "Unknown error.")
                    st.error(f"Registration failed: {error_detail}")
            except requests.exceptions.ConnectionError:
                st.error("Unable to connect to the backend. Please try again later.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

    show_footer()
