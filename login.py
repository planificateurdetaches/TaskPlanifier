import streamlit as st
from auth import authenticate_user, get_password_hash, verify_password
from session_state import get_user_session, set_user_session
from db import SessionLocal, User
from email_utils import send_reset_password_email
import secrets

def login_page():
    st.title("Login/Register")

    # Tabs for Login and Register
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.header("Login")
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            db = SessionLocal()
            user = db.query(User).filter(User.username == login_username).first()
            db.close()
            user = authenticate_user(login_username, login_password)
            
            if user:

                st.success("Logged in successfully")
            # Store user session
            set_user_session(True, {'username': user.username, 'id': user.id, 'name': user.name})
            st.experimental_rerun()

        else:
                st.error("Invalid username or password")

        reset_email = st.text_input("Enter your email", key="reset_email")
        if st.button("Forgot Password"):
            st.write(f"Debug: Reset email entered: {reset_email}")
            if reset_email:
                db = SessionLocal()
                user = db.query(User).filter(User.email == reset_email).first()
                st.write(f"Debug: User found: {user}")
                if user:
                    reset_token = secrets.token_urlsafe(16)
                    user.reset_token = reset_token
                    st.write(f"Debug: Reset token generated: {reset_token}")
                    try:
                        db.commit()  # Ensure changes are committed
                        st.write(f"Debug: Database commit successful")
                    except Exception as e:
                        st.write(f"Debug: Database commit failed: {e}")
                    db.close()  # Close the database session

                    reset_link = f"http://localhost:8501/?token={reset_token}"
                    st.write(f"Debug: Reset link generated: {reset_link}")
                    try:
                        send_reset_password_email(reset_email, reset_link)
                        st.success("Password reset email sent")
                        st.write(f"Debug: Email sent successfully")
                    except Exception as e:
                        st.write(f"Debug: Email sending failed: {e}")
                else:
                    st.error("No user found with that email")
            else:
                st.error("Please enter your email")

    with tab2:
        st.header("Register")
        register_username = st.text_input("New Username", key="register_username")
        register_name = st.text_input("Name", key="register_name")
        register_email = st.text_input("Email", key="register_email")
        register_password = st.text_input("New Password", type="password", key="register_password")
        register_confirm_password = st.text_input("Confirm Password", type="password", key="register_confirm_password")

        if st.button("Register"):
            if register_password != register_confirm_password:
                st.error("Passwords do not match")
            else:
                hashed_password = get_password_hash(register_password)
                db = SessionLocal()
                new_user = User(
                    username=register_username,
                    name=register_name,
                    email=register_email,
                    hashed_password=hashed_password
                )
                db.add(new_user)
                db.commit()
                db.close()
                st.success("User registered successfully")
                st.experimental_rerun()

# Sample usage in main app
if __name__ == "__main__":
    login_page()


