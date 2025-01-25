import os

import pandas as pd
import requests
import streamlit as st


def app():
    st.title("User Profile")

    BACKEND_URL = os.getenv("BACKEND_URL", "http://backend-api:8000")

    token = st.session_state.get("auth_token", None)
    if not token:
        st.warning("You are not logged in.")
        return

    headers = {"Authorization": f"Bearer {token}"}

    # ----------------------------------------------------------------
    # ADDED: Provide helpful instructions for new or non-technical users
    # ----------------------------------------------------------------
    st.markdown(
        """
        ## How to Use This Page

        **1. View your basic account info** (username, email) below.

        **2. See the list of your uploaded/created datasets**.
        - If you want to delete one, just hit the 'Delete' button.

        **3. Update your profile** (change email or password) at the bottom.
        - If your chosen new email is already used by another user, the update fails.
        - After updating your password, remember to use the new password at next login.

        You can always log out using the *Logout* button on the sidebar.
        """
    )

    # -------------------------------------------
    # 1) Fetch & display user info
    # -------------------------------------------
    try:
        response = requests.get(f"{BACKEND_URL}/auth/me", headers=headers)
        if response.status_code == 200:
            user = response.json()
            st.write(f"### Username: {user['username']}")
            st.write(f"### Email: {user['email']}")
        else:
            st.error(
                f"Failed to fetch user profile:"
                f" {response.json().get('detail', 'Unknown error.')}"
            )
    except requests.exceptions.ConnectionError:
        st.error("Unable to connect to the backend. Please try again later.")
        return
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return

    st.markdown("---")

    # -------------------------------------------
    # 2) Show user's own datasets
    # -------------------------------------------
    st.subheader("Your Datasets")

    try:
        # This GET /data/?page=1&page_size=999 will list only the user's own data
        # (since the backend filters by user_id unless you're admin).
        ds_resp = requests.get(
            f"{BACKEND_URL}/data/?page=1&page_size=9999",
            headers=headers,
        )
        if ds_resp.status_code == 200:
            user_datasets = ds_resp.json()
            if user_datasets:
                df = pd.DataFrame(user_datasets)
                st.dataframe(df[["id", "name", "file_name", "uploaded_at"]])

                # Let them delete a selected dataset
                st.write("Select a dataset ID to delete:")
                ds_id_to_delete = st.selectbox(
                    "Dataset ID", [d["id"] for d in user_datasets]
                )
                if st.button("Delete Selected Dataset"):
                    del_resp = requests.delete(
                        f"{BACKEND_URL}/data/{ds_id_to_delete}", headers=headers
                    )
                    if del_resp.status_code == 204:
                        st.success(f"Dataset {ds_id_to_delete} deleted.")
                        st.experimental_rerun()
                    else:
                        st.error(f"Error deleting dataset: {del_resp.text}")
            else:
                st.info("No datasets found for your account.")
        else:
            st.error(
                f"Failed to fetch datasets: {ds_resp.json().get('detail', 'Unknown error.')}"
            )
    except Exception as e:
        st.error(f"Failed to list your datasets: {e}")

    st.markdown("---")

    # -------------------------------------------
    # 3) Update Profile (email/password)
    # -------------------------------------------
    st.subheader("Update Profile")
    with st.form("update_profile_form"):
        new_email = st.text_input("New Email", placeholder="Leave blank if no change")
        new_password = st.text_input(
            "New Password", type="password", placeholder="Leave blank if no change"
        )
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
                    f"Failed to update profile:"
                    f" {response.json().get('detail', 'Unknown error.')}"
                )
        except requests.exceptions.ConnectionError:
            st.error("Unable to connect to the backend. Please try again later.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
