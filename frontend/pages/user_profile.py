import streamlit as st
import requests

def app():
    st.title("User Profile Management")

    if "auth_token" not in st.session_state:
        st.warning("You must be logged in to manage your profile.")
        return

    st.write("Update Profile Information")

    with st.form("profile_form"):
        new_email = st.text_input("New Email", value="")
        new_password = st.text_input("New Password", type="password")
        submit = st.form_submit_button("Update Profile")

    if submit:
        headers = {"Authorization": f"Bearer {st.session_state['auth_token']}"}
        params = {}
        if new_email:
            params["email"] = new_email
        if new_password:
            params["password"] = new_password

        try:
            response = requests.put(
                "http://localhost:8000/auth/update_profile",
                params=params,
                headers=headers
            )
            if response.status_code == 200:
                st.success("Profile updated successfully.")
            else:
                st.error(f"Update failed: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"Error: {e}")
