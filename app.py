import streamlit as st
from session_state import get_user_session, clear_user_session
import subprocess
from auth import authenticate_user, get_password_hash, validate_reset_token
from db import SessionLocal, User
from email_utils import send_reset_password_email
from scheduler import schedule_task
from pages.login import login_page  # Ajout de l'importation
from pages.create_task import create_task_page  # Ajout de l'importation
from pages.modify_task import modify_task_page  # Ajout de l'importation

st.set_page_config(initial_sidebar_state="collapsed")

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'user' not in st.session_state:
    st.session_state['user'] = None

def main():
    user_session = get_user_session()
    if not user_session['authenticated']:
        login_page()
    else:
        st.sidebar.title(f"Welcome {user_session['user']['username']}")
        page = st.sidebar.selectbox("Select Page", ["Create Task", "Modify Task"])

        if page == "Create Task":
            create_task_page()
        elif page == "Modify Task":
            modify_task_page()

query_params = st.experimental_get_query_params()
token = query_params.get("token", [None])[0]

if token:
    username = validate_reset_token(token)
    if username:
        st.write(f"Resetting password for {username}")
        new_password = st.text_input("New Password", type="password")
        if st.button("Reset Password"):
            hashed_password = get_password_hash(new_password)
            db = SessionLocal()
            user = db.query(User).filter(User.username == username).first()
            user.hashed_password = hashed_password
            user.reset_token = None  # Clear the reset token
            db.commit()
            db.close()
            st.success("Password reset successfully ✅")
            st.experimental_set_query_params()  # Clear the token from URL
    else:
        st.error("Invalid or expired token 😨")
else:
    if not st.session_state['authenticated']:
        login_page()
    else:
        st.sidebar.title("Navigation")
        page = st.sidebar.selectbox("Select Page", ["Create Task♦️", "Modify Task ♻️"])
        if page == "Create Task":
            create_task_page()
        elif page == "Modify Task":
            modify_task_page()



