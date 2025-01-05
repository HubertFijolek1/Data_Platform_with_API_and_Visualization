import streamlit as st
import requests

def app():
    st.title("Login")

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Log In")

    if submit:
        # Example API call to backend /auth/login
        # later I will handle tokens, sessions, etc.
        data = {
            "username": "",  # if needed
            "email": email,
            "password": password
        }
        try:
            response = requests.post("http://localhost:8000/auth/login", json=data)
            if response.status_code == 200:
                token_data = response.json()
                st.success(f"Logged in! Token: {token_data.get('access_token')}")
                st.session_state["auth_token"] = token_data.get("access_token")
            else:
                st.error(f"Login failed: {response.json().get('detail')}")
        except Exception as e:
            st.error(f"Error connecting to server: {e}")
