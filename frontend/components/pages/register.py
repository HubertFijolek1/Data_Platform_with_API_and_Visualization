import streamlit as st
import requests
from requests.exceptions import RequestException
import os
import time


def app():
    st.title("Register")

    st.write("Create a new account to access the Data Analysis Platform.")

    with st.form("registration_form"):
        username = st.text_input("Username", max_chars=50)
        email = st.text_input("Email", max_chars=100)
        password = st.text_input("Password", type="password", max_chars=100)
        confirm_password = st.text_input(
            "Confirm Password", type="password", max_chars=100
        )
        submit = st.form_submit_button("Register")

    if submit:
        # Input Validation
        if not username or not email or not password or not confirm_password:
            st.error("Please fill out all fields.")
            return

        if password != confirm_password:
            st.error("Passwords do not match.")
            return

        if len(password) < 6:
            st.error("Password must be at least 6 characters long.")
            return

        # Backend API URL
        BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")
        register_endpoint = f"{BACKEND_URL}/auth/register"

        # Prepare payload
        payload = {"username": username, "email": email, "password": password}

        try:
            response = requests.post(register_endpoint, json=payload)
            if response.status_code == 200:
                st.success("Registration successful! You can now log in.")
                st.info("Redirecting to the login page...")
                # Add a small delay before redirecting
                time.sleep(2)
                st.rerun()  # Refresh the app
            else:
                # Extract error message from response
                try:
                    error_detail = response.json().get("detail", "Unknown error.")
                except ValueError:
                    error_detail = response.text or "Unknown error."
                st.error(f"Registration failed: {error_detail}")
        except RequestException as e:
            st.error(f"Error connecting to the backend: {e}")
