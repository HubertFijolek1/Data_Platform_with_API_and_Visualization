import streamlit as st
import requests
import os

def app():
    st.title("Login")

    BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Log In")

    if submit:
        data = {
            "email": email,
            "password": password
        }
        try:
            response = requests.post(f"{BACKEND_URL}/auth/login", json=data)
            if response.status_code == 200:
                token_data = response.json()
                st.success("Logged in successfully!")
                st.session_state["auth_token"] = token_data.get("access_token")
                st.rerun()
            else:
                error_detail = response.json().get("detail", "Unknown error.")
                st.error(f"Login failed: {error_detail}")
        except Exception as e:
            st.error(f"Error connecting to server: {e}")