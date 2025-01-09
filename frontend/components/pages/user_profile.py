import streamlit as st
import requests
import os


def app():
    st.title("User Profile")

    BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

    token = st.session_state.get("auth_token", None)
    if not token:
        st.warning("You are not logged in.")
        return

    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(f"{BACKEND_URL}/auth/me", headers=headers)
        if response.status_code == 200:
            user = response.json()
            st.write(f"### Username: {user['username']}")
            st.write(f"### Email: {user['email']}")
        else:
            st.error(
                f"Failed to fetch user profile: {response.json().get('detail', 'Unknown error.')}"
            )
    except requests.exceptions.ConnectionError:
        st.error("Unable to connect to the backend. Please try again later.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

    st.markdown("---")

    st.subheader("Update Profile")
    with st.form("update_profile_form"):
        new_email = st.text_input("New Email")
        new_password = st.text_input("New Password", type="password")
        submit = st.form_submit_button("Update")

    if submit:
        update_data = {}
        if new_email:
            update_data["email"] = new_email
        if new_password:
            update_data["password"] = new_password

        if not update_data:
            st.error("No changes provided.")
            return

        try:
            response = requests.put(
                f"{BACKEND_URL}/auth/update_profile", json=update_data, headers=headers
            )
            if response.status_code == 200:
                st.success("Profile updated successfully.")
                if "email" in update_data:
                    st.session_state["user_email"] = new_email
                if "password" in update_data:
                    st.session_state["user_password"] = new_password
            else:
                st.error(
                    f"Failed to update profile: {response.json().get('detail', 'Unknown error.')}"
                )
        except requests.exceptions.ConnectionError:
            st.error("Unable to connect to the backend. Please try again later.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
